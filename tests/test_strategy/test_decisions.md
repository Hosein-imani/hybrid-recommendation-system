# Test Decisions

## Small Deterministic Fixtures for ML Tests

### Decision

Unit and ordinary integration tests use small deterministic movie and ratings frames. A real but lightweight Surprise SVD configuration is used where model training or persistence is the behavior under test.

### Reason

The production ratings file is large enough that full-dataset training would make routine feedback slow and introduce unnecessary resource requirements. Small fixtures retain the relevant schema and interactions while keeping failures local and reproducible.

### Alternative Considered

Running the full MovieLens training workflow for every collaborative and hybrid test.

### Why It Was Not Selected

That would blur unit and integration boundaries, repeat expensive work, and make the suite unsuitable for normal CI feedback.

### Impact on Maintainability

The fixtures make failures readable and keep the unit suite fast. The real SVD integration and E2E tests still protect the production model boundary.

### Future Consideration

Add a separately scheduled full-dataset regression job when model-quality thresholds and resource budgets are defined.

## Controlled Source Outputs for Hybrid Unit Tests

### Decision

Hybrid unit tests provide protocol-compatible content and collaborative recommenders with controlled candidate lists. The real recommenders remain in the end-to-end workflow.

### Reason

The hybrid coordinator's important contract is overlap classification, rank ordering, metadata attachment, seen-item exclusion, and validation. Controlled inputs make those invariants deterministic and failures easy to diagnose.

### Alternative Considered

Training and executing both recommendation models for every hybrid unit test.

### Why It Was Not Selected

It would test model behavior repeatedly while making coordinator failures harder to isolate and more sensitive to ML randomness.

### Impact on Maintainability

The coordinator tests are independent of model implementation details and can remain stable if either recommender is replaced.

### Future Consideration

Each new recommender implementation should be covered by its own integration contract before being used as a hybrid source.

## Artifact Assertions at Workflow Boundaries

### Decision

Integration and E2E tests assert output existence, CSV schema, report content, and recommendation-ID integrity rather than comparing complete files byte-for-byte.

### Reason

The repository produces user-visible artifacts, but ML scores and row ordering can change without violating the core contract. Schema and invariant assertions protect consumers while avoiding brittle snapshots.

### Alternative Considered

Golden-file comparisons for all generated CSV and report files.

### Why It Was Not Selected

Exact snapshots would couple tests to incidental formatting, stochastic scores, and harmless ordering changes.

### Impact on Maintainability

Artifact tests remain useful across refactoring while still detecting missing columns, duplicated movies, failed reports, and broken persistence.

### Future Consideration

Use versioned golden reports only for deliberately stable release-level presentation formats.

## No Speculative Tests for Absent Features

### Decision

The suite does not add tests for GUI, API, database, authentication, Docker, or a standalone movie-search component because those features are not present in the current repository.

### Reason

Tests should document and protect current behavior. Speculative tests would create artificial interfaces and false maintenance obligations.

### Alternative Considered

Creating placeholder directories and tests for the future architecture described in the project brief.

### Why It Was Not Selected

There is no production contract to validate, and the current title-to-ID helper is the only implemented search-like workflow boundary.

### Impact on Maintainability

The suite stays aligned with the current source of truth and leaves clear extension points for future boundary-specific tests.

### Future Consideration

Add contract tests when each feature is introduced, keeping them in a layer that matches its real interface.
