# Expected output — what to compare

The tool writes a single JSON report (`dedup_report.json` here is a representative
run over `tests/input/`). The report is **not byte-for-byte reproducible**, so
integration testing should compare the *stable properties* below rather than
diffing the whole file.

## Why the output is not byte-identical

- **Ordering is not fixed.** Series within a duplicate group, the entries in a
  finding's `locations` list, and the order of findings are produced from hash
  maps and a thread pool, so their order varies between runs.
- **The representative instance can differ.** For a `cross_series_sop` finding,
  the specific `sop_uid` / `path` shown as the example is any one of the
  duplicated instances and may change from run to run.
- **Paths are environment-specific.** The `path` values reflect wherever the
  dataset is mounted at run time (shown here as `/data/...`). They are not part
  of the tool's logical result.
- **Pixel-similarity scores are floating point.** `mean_similarity` and the
  per-metric values under `pixel_near_duplicate` findings may differ slightly
  across NumPy / scikit-image versions and hardware.

## Stable properties to check

Compare these fields, which are deterministic for a given input dataset:

- `summary.files_scanned` = **1670**
- `summary.series_after_filtering` = **10**
- `summary.errors` = **0**
- `summary.findings_total` = **417**
- `summary.findings_confirmed` = **411**
- `summary.findings_probable` = **6**
- Count of findings per `type`:
  - `hash_identical` = **2**
  - `cross_series_sop` = **409**
  - `intra_series_sop` = **0**
  - `pixel_near_duplicate` = **6**
- `pipeline_detail.cross_series_dup_sop_count` = **409**
- `pipeline_detail.unique_hashes` = **6**
- `pipeline_detail.hash_duplicate_groups` = **2**
- `pipeline_detail.pixel_near_duplicates` = **6**

For the `pixel_near_duplicate` findings, check that each `mean_similarity` is
`>= pipeline_detail.pixel_threshold` (0.95) rather than matching an exact value.
