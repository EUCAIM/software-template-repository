# **DIGITAL MAMMOGRAPHY DICOM PREPROCESSING**

This is a Python tool that performs preprocessing and quality enhancement on DICOM digital mammography images. It applies configurable image processing pipelines including denoising, contrast enhancement (CLAHE), and normalization.

The output is a processed dataset of DICOM files maintaining the original structure and metadata, with enhanced image quality suitable for federated learning and AI model training in the EUCAIM project.

The main functionalities are:

- Selection and processing of **2D digital mammography (MG) DICOM files only**.
- **Z-score normalization** with percentile-based clipping to standardize intensity ranges.
- **Multiple denoising methods**: adaptive median, gaussian blur, anisotropic diffusion, wavelet denoising, and cascade (unsharp mask + gaussian).
- **CLAHE (Contrast Limited Adaptive Histogram Equalization)** for contrast enhancement.
- **Parallel processing** by patient folders for large datasets.
- **DICOM integrity preservation**: maintains original metadata, applies proper Modality LUT, and saves with correct pixel encoding.
- **Flexible configuration** through JSON files for different preprocessing pipelines.

Optional functionalities are:

- Configurable number of parallel workers for performance optimization.
- Multiple denoising algorithms with customizable parameters.
- Adjustable CLAHE clip limits for different contrast requirements.
- Support for both nested patient/study/series structures and flat file layouts.

---

## Execution model

The tool is CLI-only. It accepts explicit individual arguments and, optionally,
a JSON configuration file via `--config_file`. The precedence is:

1. CLI arguments
2. file provided through `--config_file`
3. built-in defaults defined in the script
4. error if a required value is still missing (`--input_dir` and `--output_dir`)

This means the tool does not require Docker volumes for configuration files; the
JSON file can be mounted or supplied from any path visible to the execution
environment.

The built-in defaults are:

| Argument | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--input_dir` | path | yes | - | Directory containing the input dataset (any nested or flat structure). |
| `--output_dir` | path | yes | - | Directory where processed DICOM files will be saved, mirroring the input structure. |
| `--config_file` | path | no | - | Path to an optional JSON configuration file. CLI arguments override values from this file. |
| `--num_workers` | int | no | `1` | Number of parallel patient workers. Use up to your CPU count for better performance. |
| `--series_number` | int | no | `2301101` | Exact SeriesNumber assigned to all processed images. |
| `--series_description_suffix` | string | no | `_harmonized` | Suffix appended to the original SeriesDescription to distinguish processed series. |
| `--zscore_enabled` | bool | no | `true` | Enable/disable z-score normalization. |
| `--zscore_p_low` | float | no | `1.0` | Lower percentile for z-score clipping. |
| `--zscore_p_high` | float | no | `99.0` | Upper percentile for z-score clipping. |
| `--denoise_method` | enum | no | `cascade` | Denoising algorithm: `none`, `adaptive_median`, `gaussian`, `anisotropic`, `wavelet`, `cascade`. |
| `--clahe_enabled` | bool | no | `true` | Enable/disable CLAHE contrast enhancement. |
| `--clahe_clip_limit` | float | no | `0.01` | CLAHE clip limit, typically between `0.005` and `0.02`. |

Method-specific arguments are also independent CLI arguments:

- Adaptive median: `--adaptive_median_ksize` (default: `3`)
- Gaussian: `--gaussian_ksize` (default: `3`), `--gaussian_sigma` (default: `0.0`)
- Anisotropic: `--anisotropic_niter` (default: `10`), `--anisotropic_kappa` (default: `50.0`), `--anisotropic_gamma` (default: `0.1`), `--anisotropic_option` (default: `1`)
- Wavelet: `--wavelet_wavelet` (default: `db1`), `--wavelet_level` (default: `2`)
- Cascade: `--cascade_unsharp_amount` (default: `1.5`), `--cascade_unsharp_sigma` (default: `1.0`), `--cascade_gaussian_sigma` (default: `0.8`)

## Recommended parameter values

The default pipeline is designed to be robust for general-purpose mammographic
preprocessing and usually provides a good starting point for many datasets:

```bash
--zscore_enabled true \
--zscore_p_low 1.0 \
--zscore_p_high 99.0 \
--denoise_method cascade \
--cascade_unsharp_amount 1.5 \
--cascade_unsharp_sigma 1.0 \
--cascade_gaussian_sigma 0.8 \
--clahe_enabled true \
--clahe_clip_limit 0.01
```

If you want a lighter or more conservative pipeline, you can disable CLAHE or
tune denoising parameters depending on the characteristics of the source data.

---

## Pulling the image from Harbor

Before running the tool locally, pull the image from the project Harbor registry:

```bash
docker pull harbor.eucaim.cancerimage.eu/processing-tools/2d_mammography_preprocessing:2.0.0-fem
```

If you are a user of the federated node, you should ensure that the data holder or
administrator of the federated node where the tool will be executed has already
made the image available in that environment. In other words, local execution is
only possible when the image is present in the node's Docker/Harbor environment.

## 📁 Folder structure overview

This is the expected folder structure for running the tool locally:

```text
local_data_path/
  tool_tests/
    2d_mammography_preprocessing/
      example_input/
        config.json                   # Optional configuration file
        INPUT/                        # Dataset folder
      example_output/                 # Reference output for validation

local_sandbox_path/                   
  2d_mammography_preprocessing/       # Processed DICOMs are written here
```

#### Notes:
- The **input folder can have any internal structure**, including mixed or flat layouts.
- The **output folder mirrors the input structure** with processed DICOM files.
- Patient folders at the first level enable parallel processing for better performance.
- The `config.json` file is optional; if provided via `--config_file`, its values are used as a base and can still be overridden by CLI arguments.

---

## Quick start for local testing

For local validation, mount the input dataset and output sandbox to any paths
visible to the container.

A typical layout is:

```text
local_data_path/
  tool_tests/
    2d_mammography_preprocessing/
      example_input/
        config.json
        INPUT/
      example_output/

local_sandbox_path/
```

You can run the tool with mounted directories like this:

```bash
docker run --rm \
  -v /path/to/local_data_path:/data \
  -v /path/to/local_sandbox_path:/sandbox \
  harbor.eucaim.cancerimage.eu/processing-tools/2d_mammography_preprocessing:2.0.0-fem \
  --config_file /data/tool_tests/2d_mammography_preprocessing/example_input/config.json \
  --input_dir /data/tool_tests/2d_mammography_preprocessing/example_input/INPUT \
  --output_dir /sandbox/2d_mammography_preprocessing
```

The validation flow is usually:

- input dataset: `/data/tool_tests/2d_mammography_preprocessing/example_input`
- output folder: `/sandbox/2d_mammography_preprocessing`
- reference output: `/data/tool_tests/2d_mammography_preprocessing/example_output`

The container entrypoint creates or adjusts the runtime user from `HOST_USER`,
`HOST_UID`, and `HOST_GID`, then executes the supplied command as that user.

### Alternative: run with command-line arguments only (no config file)

You can skip the configuration file entirely and pass all parameters via CLI. Below are complete examples for each denoise method.

**Example: Adaptive Median**
```bash
docker run --rm \
  -v /path/to/local_data_path:/data \
  -v /path/to/local_sandbox_path:/sandbox \
  harbor.eucaim.cancerimage.eu/processing-tools/2d_mammography_preprocessing:2.0.0-fem \
  --input_dir /data/INPUT --output_dir /sandbox/OUTPUT --num_workers 4 \
  --series_number 2301101 --series_description_suffix _harmonized \
  --zscore_enabled true --zscore_p_low 1.0 --zscore_p_high 99.0 \
  --denoise_method adaptive_median --adaptive_median_ksize 3 \
  --clahe_enabled true --clahe_clip_limit 0.01
```

**Example: Gaussian**
```bash
docker run --rm \
  -v /path/to/local_data_path:/data \
  -v /path/to/local_sandbox_path:/sandbox \
  harbor.eucaim.cancerimage.eu/processing-tools/2d_mammography_preprocessing:2.0.0-fem \
  --input_dir /data/INPUT --output_dir /sandbox/OUTPUT --num_workers 4 \
  --series_number 2301101 --series_description_suffix _harmonized \
  --zscore_enabled true --zscore_p_low 1.0 --zscore_p_high 99.0 \
  --denoise_method gaussian --gaussian_ksize 3 --gaussian_sigma 0.8 \
  --clahe_enabled true --clahe_clip_limit 0.01
```

**Example: Anisotropic Diffusion**
```bash
docker run --rm \
  -v /path/to/local_data_path:/data \
  -v /path/to/local_sandbox_path:/sandbox \
  harbor.eucaim.cancerimage.eu/processing-tools/2d_mammography_preprocessing:2.0.0-fem \
  --input_dir /data/INPUT --output_dir /sandbox/OUTPUT --num_workers 4 \
  --series_number 2301101 --series_description_suffix _harmonized \
  --zscore_enabled true --zscore_p_low 1.0 --zscore_p_high 99.0 \
  --denoise_method anisotropic --anisotropic_niter 10 --anisotropic_kappa 50 --anisotropic_gamma 0.1 --anisotropic_option 1 \
  --clahe_enabled true --clahe_clip_limit 0.01
```

**Example: Wavelet**
```bash
docker run --rm \
  -v /path/to/local_data_path:/data \
  -v /path/to/local_sandbox_path:/sandbox \
  harbor.eucaim.cancerimage.eu/processing-tools/2d_mammography_preprocessing:2.0.0-fem \
  --input_dir /data/INPUT --output_dir /sandbox/OUTPUT --num_workers 4 \
  --series_number 2301101 --series_description_suffix _harmonized \
  --zscore_enabled true --zscore_p_low 1.0 --zscore_p_high 99.0 \
  --denoise_method wavelet --wavelet_wavelet db1 --wavelet_level 2 \
  --clahe_enabled true --clahe_clip_limit 0.01
```

**Example: Cascade (Unsharp + Gaussian) — Recommended, complete with all parameters**
```bash
docker run --rm \
  -v /path/to/local_data_path:/data \
  -v /path/to/local_sandbox_path:/sandbox \
  harbor.eucaim.cancerimage.eu/processing-tools/2d_mammography_preprocessing:2.0.0-fem \
  --input_dir /data/INPUT \
  --output_dir /sandbox/OUTPUT \
  --num_workers 4 \
  --series_number 2301101 \
  --series_description_suffix _harmonized \
  --zscore_enabled true \
  --zscore_p_low 1.0 \
  --zscore_p_high 99.0 \
  --denoise_method cascade \
  --cascade_unsharp_amount 1.5 \
  --cascade_unsharp_sigma 1.0 \
  --cascade_gaussian_sigma 0.8 \
  --clahe_enabled true \
  --clahe_clip_limit 0.01
```

---

## Production / FEM execution

In the platform, the orchestrator provides the mounted paths transparently. The
user should not need to know the underlying host filesystem layout; the execution
environment exposes logical paths such as `/data` and `/sandbox`.

Typical execution in FEM is therefore:

```bash
python digital_mammography_preprocessing.py \
  --input_dir /data/input \
  --output_dir /sandbox
```

or, when an explicit config file is provided:

```bash
python digital_mammography_preprocessing.py \
  --config_file /data/config.json \
  --input_dir /data/input \
  --output_dir /sandbox
```

If you need to inspect the available CLI arguments and their default values, you
can run:

```bash
python digital_mammography_preprocessing.py --help
```
---

## Configuration file reference (`--config_file`)

When a JSON configuration file is provided, all parameters live under the `"preprocessing"` key. CLI arguments always take precedence over values in this file.

**Example configuration:**
```json
{
  "preprocessing": {
    "num_workers": 4,
    "zscore": {
      "enabled": true,
      "percentiles": [1.0, 99.0]
    },
    "denoise": {
      "method": "cascade",
      "params": {
        "cascade": {
          "unsharp_amount": 1.5,
          "unsharp_sigma": 1.0,
          "gaussian_sigma": 0.8
        }
      }
    },
    "clahe": {
      "enabled": true,
      "clip_limit": 0.01
    }
  }
}
```

### Mandatory parameters within `"preprocessing"` (when using a config file)

- `zscore`: Z-score normalization settings (object)
  - `enabled`: Enable/disable z-score normalization (boolean)
  - `percentiles`: Array `[low, high]` for percentile clipping. Example: `[1.0, 99.0]` (array of floats)

- `denoise`: Denoising settings (object)
  - `method`: Denoising method. Options: `"none"`, `"adaptive_median"`, `"gaussian"`, `"anisotropic"`, `"wavelet"`, `"cascade"` (string)
  - `params`: Method-specific parameters (object, see examples below)

- `clahe`: CLAHE settings (object)
  - `enabled`: Enable/disable CLAHE (boolean)
  - `clip_limit`: Contrast clip limit, typically between `0.005` and `0.02`. Default: `0.01` (float)

### Optional parameters within `"preprocessing"`

- `num_workers`: Number of parallel patient workers for processing. Default: `1`. Use up to your CPU count for better performance (int)
- `series_number`: Exact SeriesNumber value for preprocessed series. Default: `2301101` (int)
- `series_description_suffix`: Suffix appended to SeriesDescription for preprocessed images. Default: `_harmonized`. Helps distinguish processed series in DICOM viewers (string)

> Note: `input_dir` and `output_dir` are provided via CLI (`--input_dir` / `--output_dir`), not through the config file.

### Denoising methods and parameters

**No Denoising:**
```json
"denoise": {
  "method": "none",
  "params": {}
}
```

**Adaptive Median Filter (requires opencv-python):**
```json
"denoise": {
  "method": "adaptive_median",
  "params": {
    "adaptive_median": {
      "ksize": 3
    }
  }
}
```

**Gaussian Blur (requires opencv-python):**
```json
"denoise": {
  "method": "gaussian",
  "params": {
    "gaussian": {
      "ksize": 3,
      "sigma": 0.0
    }
  }
}
```

**Anisotropic Diffusion:**
```json
"denoise": {
  "method": "anisotropic",
  "params": {
    "anisotropic": {
      "niter": 10,
      "kappa": 50.0,
      "gamma": 0.1,
      "option": 1
    }
  }
}
```

**Wavelet Denoising:**
```json
"denoise": {
  "method": "wavelet",
  "params": {
    "wavelet": {
      "wavelet": "db1",
      "level": 2
    }
  }
}
```

**Cascade (Unsharp Mask + Gaussian) — Recommended:**
```json
"denoise": {
  "method": "cascade",
  "params": {
    "cascade": {
      "unsharp_amount": 1.5,
      "unsharp_sigma": 1.0,
      "gaussian_sigma": 0.8
    }
  }
}
```

---

## **Functionality**

### Mammogram Selection (Filter)
A DICOM file is processed **only if ALL** of the following are true:
1. `Modality == "MG"` (mammography, case-insensitive).
2. `NumberOfFrames == 1` (single frame, not tomosynthesis).
3. `SamplesPerPixel == 1` (grayscale, not color).
4. `PhotometricInterpretation ∈ {"MONOCHROME1", "MONOCHROME2"}`.
5. `Rows` and `Columns` are present and valid.
6. Pixel data decodes successfully and results in a **2D array** (H×W).

**Skipped files**: RTSTRUCT, SEG, SC, CT, MR, tomosynthesis (multi-frame), color images, and any non-MG modality.

**Output format**: Same filenames and relative paths as input. Transfer Syntax set to **Explicit VR Little Endian**. Pixel data is replaced with processed values; header fields are updated accordingly. Photometric interpretation is preserved.

**DICOM Metadata for Derived Series**: To prevent DICOM viewers from confusing or overwriting preprocessed images with originals, the following metadata is automatically modified:
- **SeriesInstanceUID** → New UID generated deterministically from original series UID. All images from the same original series will share the same new SeriesInstanceUID, so they group together as one preprocessed series in the viewer.
- **SOPInstanceUID** → New unique UID for each processed instance (file)
- **SeriesNumber** → Set to configured value (default: `2301101`, configurable via `--series_number` / `series_number`)
- **SeriesDescription** → Appends suffix (default `_harmonized`, configurable via `--series_description_suffix` / `series_description_suffix`)
- **DerivationDescription** → Documents processing steps applied (z-score, denoising method, CLAHE)
- **StudyInstanceUID** → Preserved (unchanged) to maintain study grouping
- **PatientID/Name/StudyDate** → Preserved for identification

**Example**: If original Series A has 50 images with SeriesInstanceUID=1.2.3.4, all 50 preprocessed images will have the same new SeriesInstanceUID (e.g., 2.25.12345...), but each will have a unique SOPInstanceUID. The viewer will display them as a single preprocessed series with 50 images.

### Processing Pipeline (per image)
The tool applies the following steps to each valid mammography DICOM file:

1. **Load DICOM** → Read pixel data and apply Modality LUT (Rescale Slope/Intercept to get physical intensity values).
2. **Z-Score Normalization** (optional) → Percentile-based clipping and standardization to normalize intensity ranges.
3. **Denoising** (optional) → Apply selected denoising method (adaptive median, gaussian, anisotropic diffusion, wavelet, or cascade).
4. **CLAHE** (optional) → Contrast-limited adaptive histogram equalization for local contrast enhancement.
5. **Rescale** → Map processed values back to the original physical intensity range.
6. **Re-encode** → Convert to stored pixel values using the original Rescale Slope/Intercept.
7. **Generate new metadata** → Create new SeriesInstanceUID, SOPInstanceUID, update SeriesNumber/Description, and add DerivationDescription.
8. **Save DICOM** → Write as DICOM file with updated pixel data and metadata. Windowing tags (WindowCenter, WindowWidth, VOILUTSequence) are removed to avoid stale values.

**Notes**:
- Z-score normalization standardizes the input for consistent denoising and CLAHE application.
- The final rescaling ensures the output maintains the original intensity scale.
- CLAHE internally works in [0,1] range; the tool automatically maps to/from the original dynamic range.
- All processing preserves DICOM metadata and structure.

---

## **Acknowledgements**

This tool was developed for digital mammography quality enhancement and standardization in the EUCAIM project context. It is designed to work within federated learning infrastructures and imaging data federations.

Developed by Manuel Marfil-Trujillo, Pedro Miguel Martínez-Gironés (adaptation), Luis Marti-Bonmati (supervision) at **GIBI230 Research Group**, **La Fe Health Research Institute (IIS La Fe)**, Valencia, Spain.

---

## **License**

This software is provided under a limited-use license for academic and research purposes within the EUCAIM project.

**Key restrictions**:
- Use is permitted exclusively for EUCAIM project activities and related European public research infrastructures.
- Commercial use, redistribution, or integration into products/services requires prior written authorization.
- Attribution to IIS La Fe and the GIBI230 Research Group must be preserved.

**Disclaimer**:
- The software is provided "as-is" without warranty of any kind.
- The developers assume no responsibility for data handling, configuration errors, or results obtained.
- Users are responsible for ensuring compliance with applicable data protection and ethics regulations.

For full license terms, see `LICENSE.txt`. For permissions or questions, contact: **gibi230@iislafe.es**

**Contact**: https://www.iislafe.es/en/ | https://www.acim.lafe.san.gva.es/acim | https://cancerimage.eu/