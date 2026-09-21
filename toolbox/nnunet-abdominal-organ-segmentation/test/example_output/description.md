# Expected output

`segmentations/1.2.826.0.1.3680043.2.1125.1.68878959984837726447916707551399667.dcm` is the reference DICOM SEG for the fixed `PANCREAS_0001` input series.

The reference source SeriesInstanceUID is
`1.2.826.0.1.3680043.2.1125.1.68878959984837726447916707551399667`.

## Integration review

This is a committed reference fixture. The onboarding runner never overwrites
it; generated files are written to `test/actual_output/`.

Compare the generated result semantically with this reference:

- it is a valid DICOM Segmentation object that references the supplied series;
- it contains the expected segmentation labels and non-empty regions where
  applicable;
- it is spatially aligned with the source series.

Do not compare generated DICOM identifiers or timestamps byte-for-byte.
Voxel masks are reproducible run to run on the same machine, but small
differences appear across GPU hardware and driver versions. Compare per
label with a Dice threshold of 0.99 rather than expecting exact equality.
Input provenance and licence are documented in
[`../example_input/DATA_LICENSE.md`](../example_input/DATA_LICENSE.md).

