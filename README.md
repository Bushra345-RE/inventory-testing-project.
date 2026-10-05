# Inventory Manager - Testing & Quality Assurance Project

A small Python inventory-management library built to demonstrate professional
testing practices: unit, integration, system and user acceptance testing, edge
case handling, performance checks and 100% code coverage.

## Structure
- `inventory/models.py`  - `Product` with input validation
- `inventory/store.py`   - storage layer with JSON save/load
- `inventory/service.py` - business logic (sell, restock, search, low stock)
- `tests/`               - 43 automated tests grouped by testing type

## Run the tests
```
pip install -r requirements.txt
pytest -v --cov=inventory --cov-report=term-missing
```

## Test types
| File | Type |
|---|---|
| test_unit.py | Unit testing |
| test_integration.py | Integration testing |
| test_system.py | System testing |
| test_uat.py | User acceptance testing |
| test_edge_cases.py | Edge cases and error handling |
| test_performance.py | Performance testing |
