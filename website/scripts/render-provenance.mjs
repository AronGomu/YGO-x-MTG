export function isSupportedRenderProvenance(provenance) {
  return (
    provenance.schemaVersion === 1 ||
    (provenance.schemaVersion === 2 &&
      provenance.renderTransform?.id === 'transparent-white-corners' &&
      provenance.renderTransform?.version === 1)
  );
}
