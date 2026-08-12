#!/usr/bin/env python3
"""Download the fixed public TCIA input for EUCAIM abdominal-organ integration testing.

The downloader retrieves only the SeriesInstanceUID recorded in
``test_dataset.yaml``. It validates the complete CT series before publishing it
under the configured ``test/example_input`` directory and never selects a case dynamically.
Run from the tool directory after installing ``test/requirements.txt``:

    python3 test/download_tcia_test_data.py
"""

from __future__ import annotations

import argparse
import math
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import pydicom
import yaml
from tcia_utils import nbia

SCRIPT_DIR = Path(__file__).resolve().parent


class DownloadError(RuntimeError):
    """Raised when a curated test series cannot be downloaded or validated."""


def load_config(path: Path = SCRIPT_DIR / "test_dataset.yaml") -> dict[str, Any]:
    with path.open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)
    required = {
        "collection",
        "patient_id",
        "study_instance_uid",
        "series_instance_uid",
        "modality",
        "expected_instances",
        "output_directory",
    }
    if not isinstance(config, dict):
        raise DownloadError("Invalid test dataset configuration; expected a mapping")
    missing = required - set(config)
    if missing:
        raise DownloadError(f"Invalid test dataset configuration; missing: {', '.join(sorted(missing))}")
    config["_config_directory"] = path.resolve().parent
    return config


def download_series(series_uid: str, destination: Path) -> Path:
    """Download one fixed series using the maintained TCIA client."""
    try:
        nbia.downloadSeries(
            [series_uid],
            input_type="list",
            path=str(destination),
            format="df",
        )
    except Exception as error:
        raise DownloadError(f"TCIA download failed: {error}") from error
    series_directory = destination / series_uid
    if not series_directory.is_dir():
        raise DownloadError(f"TCIA did not create the expected series directory: {series_directory}")
    return series_directory


def _instance_sort_key(dataset: pydicom.Dataset) -> tuple[int, str]:
    try:
        instance_number = int(dataset.InstanceNumber)
    except (AttributeError, TypeError, ValueError):
        instance_number = sys.maxsize
    return instance_number, str(getattr(dataset, "SOPInstanceUID", ""))


def geometry_values(dataset: pydicom.Dataset) -> tuple[int, int, tuple[float, ...], tuple[float, ...]]:
    """Return geometry fields, normalising harmless DICOM decimal rounding."""
    try:
        return (
            int(dataset.Rows),
            int(dataset.Columns),
            tuple(float(value) for value in dataset.PixelSpacing),
            tuple(float(value) for value in dataset.ImageOrientationPatient),
        )
    except (AttributeError, TypeError, ValueError) as error:
        raise DownloadError("Downloaded input has incomplete image geometry") from error


def has_consistent_geometry(first: tuple[int, int, tuple[float, ...], tuple[float, ...]],
                            other: tuple[int, int, tuple[float, ...], tuple[float, ...]]) -> bool:
    if first[:2] != other[:2] or len(first[2]) != len(other[2]) or len(first[3]) != len(other[3]):
        return False
    return all(math.isclose(a, b, rel_tol=0.0, abs_tol=1e-5)
               for values in zip(first[2:], other[2:]) for a, b in zip(*values))


def has_expected_tracer(dataset: pydicom.Dataset, expected_tracer: str) -> bool:
    """Check the PET radiopharmaceutical description when the config pins one."""
    descriptions = [str(getattr(item, "Radiopharmaceutical", ""))
                    for item in getattr(dataset, "RadiopharmaceuticalInformationSequence", [])]
    return any(expected_tracer.casefold() in value.casefold() for value in descriptions)


def validate_series(directory: Path, config: dict[str, Any]) -> list[tuple[pydicom.Dataset, Path]]:
    datasets: list[tuple[pydicom.Dataset, Path]] = []
    for path in directory.rglob("*"):
        if not path.is_file():
            continue
        try:
            dataset = pydicom.dcmread(path, stop_before_pixels=True)
        except Exception:
            continue
        datasets.append((dataset, path))

    if len(datasets) != int(config["expected_instances"]):
        raise DownloadError(
            f"Expected {config['expected_instances']} DICOM instances, found {len(datasets)}"
        )

    expected_series = str(config["series_instance_uid"])
    expected_study = str(config["study_instance_uid"])
    expected_modality = str(config["modality"])
    expected_tracer = str(config.get("tracer", ""))
    sop_uids: set[str] = set()
    reference_geometry: tuple[int, int, tuple[float, ...], tuple[float, ...]] | None = None

    for dataset, _ in datasets:
        if str(getattr(dataset, "SeriesInstanceUID", "")) != expected_series:
            raise DownloadError("Downloaded instance has an unexpected SeriesInstanceUID")
        if str(getattr(dataset, "StudyInstanceUID", "")) != expected_study:
            raise DownloadError("Downloaded instance has an unexpected StudyInstanceUID")
        if str(getattr(dataset, "Modality", "")) != expected_modality:
            raise DownloadError("Downloaded instance has an unexpected modality")
        if expected_tracer and not has_expected_tracer(dataset, expected_tracer):
            raise DownloadError(f"Downloaded PET instance does not identify tracer {expected_tracer}")
        if str(getattr(dataset, "SOPClassUID", "")) in {
            "1.2.840.10008.5.1.4.1.1.66.4",  # Segmentation Storage
            "1.2.840.10008.5.1.4.1.1.481.3",  # RT Structure Set Storage
        }:
            raise DownloadError("Downloaded input contains a segmentation or RTSTRUCT object")
        sop_uid = str(getattr(dataset, "SOPInstanceUID", ""))
        if not sop_uid or sop_uid in sop_uids:
            raise DownloadError("Downloaded input has missing or duplicate SOPInstanceUID values")
        sop_uids.add(sop_uid)
        geometry = geometry_values(dataset)
        if reference_geometry is None:
            reference_geometry = geometry
        elif not has_consistent_geometry(reference_geometry, geometry):
            raise DownloadError("Downloaded input instances do not have consistent image geometry")

    return sorted(datasets, key=lambda item: _instance_sort_key(item[0]))


def publish_series(files: list[tuple[pydicom.Dataset, Path]], destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for index, (_, source) in enumerate(files, start=1):
        shutil.copyfile(source, destination / f"{index:06d}.dcm")


def target_directory(config: dict[str, Any], output_dir: Path | None) -> Path:
    if output_dir is None:
        return Path(config.get("_config_directory", SCRIPT_DIR)) / str(config["output_directory"])
    return output_dir / str(config["patient_id"])


def download_test_data(config: dict[str, Any], output_dir: Path | None = None, force: bool = False) -> Path:
    target = target_directory(config, output_dir)
    if target.exists() and not force:
        try:
            validate_series(target, config)
            print(f"TCIA test data already present and valid: {target}")
            return target
        except DownloadError as error:
            raise DownloadError(f"Existing test data is invalid ({error}); rerun with --force to replace it") from error

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent, prefix=".tcia-download-") as temporary_name:
        temporary_dir = Path(temporary_name)
        downloaded_dir = download_series(str(config["series_instance_uid"]), temporary_dir / "download")
        validated = validate_series(downloaded_dir, config)
        staged_target = temporary_dir / "published"
        publish_series(validated, staged_target)
        validate_series(staged_target, config)
        if target.exists():
            shutil.rmtree(target)
        shutil.move(str(staged_target), str(target))

    print("Downloaded TCIA test data")
    print(f"  Collection: {config['collection']}")
    print(f"  Patient: {config['patient_id']}")
    print(f"  StudyInstanceUID: {config['study_instance_uid']}")
    print(f"  SeriesInstanceUID: {config['series_instance_uid']}")
    print(f"  Modality: {config['modality']}")
    print(f"  Files downloaded: {config['expected_instances']}")
    print(f"  Output: {target}")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=SCRIPT_DIR / "test_dataset.yaml",
                        help="Path to the fixed test-dataset configuration")
    parser.add_argument("--output-dir", type=Path, help="Parent directory for the fixed test series")
    parser.add_argument("--force", action="store_true", help="Replace an existing curated series")
    args = parser.parse_args()
    try:
        download_test_data(load_config(args.config), args.output_dir, args.force)
    except DownloadError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

