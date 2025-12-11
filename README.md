# DuckDB Analytics Plugin for Claude Code

A Claude Code plugin that enables powerful SQL analytics over tabular data using DuckDB.

## Features

- **Multiple file formats**: CSV, Parquet, JSON/NDJSON, Excel (.xlsx)
- **Database connections**: Postgres, MySQL, SQLite, S3
- **Direct file queries**: Query files directly by path
- **Aliased sources**: Join multiple datasets with clean SQL
- **Smart truncation**: Handles large datasets with automatic result limiting

## Installation

### From GitHub

Add the marketplace and install:

```
/plugin marketplace add richard-gyiko/duckdb-analytics-plugin
/plugin install duckdb-analytics@duckdb-analytics-marketplace
```

### Local Development

```
/plugin marketplace add ./path/to/duckdb-analytics-plugin
/plugin install duckdb-analytics@duckdb-analytics-marketplace
```

## Usage

Once installed, Claude will automatically use this skill when you ask data analysis questions.

### Examples

**Simple file query:**
> "What are the top 10 products by revenue in sales.csv?"

**Join multiple files:**
> "Join orders.parquet with customers.csv and show total orders per customer"

**Database query:**
> "Query the events table from our Postgres database and show events from the last 7 days"

## How It Works

The skill uses DuckDB, an embedded analytical database that excels at:
- Columnar storage and vectorized execution
- Direct querying of files without loading into memory
- Automatic format detection
- Efficient aggregations on large datasets

## Requirements

- Python 3.11+
- `uv` package manager (for running the script)

Dependencies are automatically installed via the inline script metadata:
- `duckdb>=1.4.3`
- `polars[pyarrow]>=1.36.1`

## File Structure

```
duckdb-analytics-plugin/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace definition
├── skills/
│   └── duckdb-analytics/
│       ├── SKILL.md         # Skill instructions for Claude
│       └── scripts/
│           └── query_duckdb.py  # DuckDB query engine
└── README.md
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please open an issue or pull request.
