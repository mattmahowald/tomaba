# Tomaba

## Set up instructions

### 1. Get the environment variables

Create a file called `.env` at `tomaba/.env`. Get the required variables from Matt.

### 2. Install poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Follow the output instructions to add the path to the poetry executable to your path
variable in your .zprofile.

```bash
export PATH="/Users/mattmahowald/.local/bin:$PATH"
```

Test poetry exists

```bash
poetry --version
```
