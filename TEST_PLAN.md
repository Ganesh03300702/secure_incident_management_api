# Test Plan

## Scope
Authentication, protected endpoints, CRUD operations, validation, error handling, and health checks.

## Positive tests
- Successful login
- Authenticated incident creation
- Incident update
- Incident retrieval

## Negative tests
- Invalid credentials
- Missing authentication
- Invalid payload
- Missing incident
- Empty update

## Test execution
`pytest -q`

## CI
GitHub Actions executes the automated test suite on pushes and pull requests.
