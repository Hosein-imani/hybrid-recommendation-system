# Test Strategy

## Architecture

The suite follows the repository's current boundaries:

- `tests/unit/data/` covers loading, preprocessing, and dataset reporting.
- `tests/unit/content_based/` covers genre feature construction and cosine-similarity behavior.
- `tests/unit/collaborative/` covers recommendation filtering and evaluation result shaping.
- `tests/unit/hybrid/` covers hybrid section construction, input/output contracts, and evaluation metrics.
- `tests/integration/` exercises real component boundaries, including a lightweight Surprise SVD training/persistence path, hybrid report generation, and workflow helpers.
- `tests/e2e/` covers one complete small-data workflow from title selection through model-backed hybrid output and artifact evaluation.

Shared deterministic data is defined in `tests/conftest.py`. Test data is intentionally small and synthetic; the production MovieLens files remain inputs to application workflows rather than test fixtures.

## Scope

The suite protects the currently implemented data, content-based, collaborative, hybrid, and report-generation paths. It verifies public outputs, input validation, important invariants, artifact schemas, model persistence, and the boundaries between recommendation components.

The repository does not currently contain a `MovieSearch` class, API, GUI, database adapter, deployment layer, or separate schema-validation package. Those areas are not represented by speculative tests. The existing title-to-ID helper used by the hybrid script is covered as a workflow boundary.

## Unit Test Strategy

Unit tests isolate deterministic transformations and contracts:

- data preprocessing must preserve caller-owned frames and apply the expected transformations;
- genre features must preserve movie metadata and create binary genre columns;
- similarity must support one or multiple seeds, exclude seeds, rank candidates, and reject invalid IDs;
- collaborative recommendation must exclude known interactions, rank predictions, and attach movie metadata;
- hybrid evaluation must calculate counts, integrity, diversity, score summaries, and overlap metrics;
- invalid source outputs and invalid request parameters must fail at the coordinator boundary.

Tests avoid asserting private local structure or exact implementation call sequences. Where a collaborator is substituted, it is because the unit under test is the boundary or orchestration behavior rather than the collaborator's algorithm.

## Integration Test Strategy

Integration tests retain real project components at meaningful boundaries. The collaborative integration test prepares a real Surprise dataset, trains a small SVD model, persists its artifacts, reloads them, and checks prediction continuity. The evaluation integration test verifies CSV loading, section construction, report creation, and output persistence. Workflow-helper tests cover title resolution and scoped cleanup using temporary directories.

The full MovieLens training path is not repeated in the suite. The repository's raw ratings file contains millions of rows, so using it for ordinary test execution would make local and CI feedback unnecessarily slow and environment-dependent.

## End-to-End Strategy

One end-to-end test uses the real content-based pipeline, a lightweight real SVD model, the hybrid coordinator, CSV serialization, and hybrid evaluation on deterministic small data. It verifies the system-level invariants that matter to a consumer of the workflow: output schema, unique recommendation IDs, exclusion of seen movies, and a passing integrity report.

The E2E layer is intentionally limited. Model quality, alternate parameter combinations, and failure details are covered at lower levels where diagnosis is cheaper.

## ML Testing Strategy

ML tests use deterministic synthetic ratings and a small SVD configuration. Assertions focus on stable contracts and invariants—prepared data, successful training, finite predictions, persistence, schema, filtering, and evaluation metrics—rather than unstable exact rankings from stochastic training.

The coordinator's ranking behavior is tested separately with controlled source outputs so that rank-sum ordering, overlap movement, and seen-item removal remain deterministic. This keeps model randomness from obscuring hybrid orchestration regressions.

## Fixtures and Test Data

`raw_movies` and `raw_ratings` model the columns consumed by the current production modules while remaining small enough for fast execution. `processed_movies` and `genre_matrix` represent the real data-preparation boundary and are reused where the content-based or hybrid components require their actual inputs.

Temporary directories are used for loader inputs, persisted model artifacts, reports, and cleanup tests. No test depends on generated files under the repository's `outputs/` directory or on a developer-specific machine path.

## Mocking Strategy

Mocks are not used to replace the content-similarity algorithm, SVD training in the integration path, or hybrid evaluation. Small protocol-compatible stubs are used only in isolated collaborative and hybrid unit tests to control scores and candidate lists. This allows filtering, ranking, validation, and section assembly to be tested without retraining a model for every case.

## Regression Protection

The suite protects the main regression risks visible in the current implementation:

- title/year/genre preprocessing drift;
- seed movies leaking into content recommendations;
- duplicate or missing seed IDs being accepted silently;
- already-seen movies appearing in collaborative or hybrid output;
- shared recommendations being emitted in multiple hybrid sections;
- source score/rank columns being lost at the hybrid boundary;
- malformed recommender output crossing into the hybrid coordinator;
- model and trainset artifacts becoming non-loadable;
- evaluation reports misrepresenting counts, integrity, diversity, or scores;
- workflow artifacts being written with an unexpected schema.

## Future Extension

New recommendation algorithms should receive their own unit tests and an integration contract before being added to the hybrid coordinator. A web or API layer should add request/response contract tests and a small API-level E2E suite while reusing the existing component tests. A GUI should add user-flow tests around the UI boundary rather than moving core algorithm tests into UI automation. Database integration should introduce isolated repository/contract tests and temporary database fixtures. Docker and CI/CD should execute the existing marker groups in separate jobs, with the lightweight suite required for every change and heavier release checks explicitly scheduled.

Authentication, monitoring, and deployment tests should be added at their respective boundaries; they should not expand the current algorithm unit tests with unrelated concerns. Full-dataset or offline model-quality checks are better treated as release/regression jobs with explicit data and time budgets.
