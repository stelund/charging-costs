# Charging Costs

The charging costs is a project to gather energy used from Zaptec REST Api to calculate
the energy costs from a set of chargers. The cost is calculated from an hourly rate from Nordpol
from the mgrey api.

## Getting Started

### Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Installation and Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

### Configuration
The application requires Zaptec API credentials. You can provide them in one of three ways:

1. **Environment variables** (highest priority):
   ```bash
   export ZAPTEC_USERNAME=your_username
   export ZAPTEC_PASSWORD=your_password
   ```

2. **Interactive prompt** (if not found in environment or config):
   The application will prompt for credentials on first run and save them to `~/.charging-costs/config.json`

3. **Manual config file** (lowest priority):
   Create `~/.charging-costs/config.json`:
   ```json
   {
     "zaptec_username": "your_username",
     "zaptec_password": "your_password"
   }
   ```

### Running the Project
```bash
uv run python main.py
```

### Running Tests
```bash
uv run pytest
```
