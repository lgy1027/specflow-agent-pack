# Deterministic replay scenarios

Use this pattern only when an interactive prototype has multiple scenarios whose differences matter to the decision. It applies to dashboards, device flows, data review tools, and similar prototypes; it does not prescribe a UI framework or implementation language.

## Model each scenario as a bounded replay

- Give each scenario a stable ID, a short label, a fixture, and an expected visible state.
- Keep the fixture deterministic. Selecting the same scenario again starts from the same first event and produces the same expected results.
- Scope counters and event lists to the selected scenario by default. Reset them on scenario selection. If cross-scenario totals are useful, show them separately and label their range.
- Switching scenarios is a boundary: stop the old replay, clear its scenario-local view state, load the new fixture, and render the new state together. Do not briefly mix old events with new KPIs.
- A fixture may be a small inline data array or a project-approved recording. Use synthetic or approved, de-identified data; state the provenance and limits in the UI.

## Failure and recovery behavior

- A signal-loss or unavailable-input fixture stops new detection events and all counters derived from new detections.
- Preserve the last valid result as historical context and label it as the last valid result; do not present it as current.
- Show the fallback state and the recovery action. On recovery, either restart the selected fixture or continue from a defined point; make that behavior visible and repeatable.
- Keep simulation labels close to the values they qualify. A simulated fallback transition does not establish real device, service, or safety behavior.

## Minimal runtime checks

Before calling the prototype verified, operate every scenario in the actual preview:

1. Select each scenario and confirm the selected label, current result, and event list correspond to its fixture.
2. Compare displayed counters with that fixture's records; confirm switching away and back resets to the same starting state unless cumulative scope is explicitly shown.
3. During signal loss, confirm the event count and detection counters stop changing while the last valid result remains visibly marked as historical.
4. Recover or switch back and confirm the documented recovery behavior.

Record what was actually observed. If a scenario cannot be operated or inspected, mark that part unverified rather than inferring success from source code or a generated file.
