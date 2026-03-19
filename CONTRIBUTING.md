# Contributing to FlowShield

First off, thank you for considering contributing to FlowShield!

## Development Setup

1. **Fork and Clone** the repository.
2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

## Running Tests

FlowShield is optimized for extreme speed (<1ms latency) and zero dependencies. Before submitting a pull request, you must ensure all tests and benchmarks pass:

```bash
# Run the test suite (must pass all 16 tests)
pytest test_flowshield.py -v

# Run performance benchmarks
python benchmark.py
```

## Pull Request Process

1. Ensure any new features include relevant tests, especially concerning thread safety.
2. Update the `README.md` with details of changes to the interface or configuration.
3. **Strict Constraint**: FlowShield relies solely on the standard library and Flask. Do not introduce external dependencies.
4. Ensure your code maintains the O(1) performance standard.
