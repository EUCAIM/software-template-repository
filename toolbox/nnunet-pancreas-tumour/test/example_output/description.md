# Expected output

`1.2.826.0.1.3680043.2.1125.1.41202274843063370955090296887703130.dcm` is the reference DICOM SEG for the fixed `PANCREAS_0080` input series.

The reference source SeriesInstanceUID is
`1.2.826.0.1.3680043.2.1125.1.41202274843063370955090296887703130`.

## Integration review

This is a committed reference fixture. The onboarding runner never overwrites
it; generated files are written to `test/actual_output/`.

Compare the generated result semantically with this reference:

- it is a valid DICOM Segmentation object that references the supplied series;
- it contains the expected segmentation labels and non-empty regions where
  applicable;
- it is spatially aligned with the source series.

Do not compare generated DICOM identifiers or timestamps byte-for-byte.
Input provenance and licence are documented in
[`../example_input/DATA_LICENSE.md`](../example_input/DATA_LICENSE.md).

