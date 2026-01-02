# Data Wrangler Plugin for Claude Code

A Claude Code plugin that enables powerful data transformation and export using DuckDB SQL.

## Features

- **Multiple file formats**: CSV, Parquet, JSON/NDJSON, Excel (.xlsx)
- **Database connections**: Postgres, MySQL, SQLite, S3
- **Cloud storage**: AWS S3, Azure Blob, Google Cloud Storage, Cloudflare R2
- **Secrets management**: Secure credential storage with environment variable substitution
- **Direct file queries**: Query files directly by path
- **Aliased sources**: Join multiple datasets with clean SQL
- **Write mode**: Export results to Parquet, CSV, or JSON
- **Partitioning**: Create Hive-style partitioned datasets
- **Advanced SQL**: PIVOT/UNPIVOT, sampling, window functions

## Installation

### From GitHub

Add the marketplace and install:

```
/plugin marketplace add richard-gyiko/data-wrangler-plugin
/plugin install data-wrangler@data-wrangler-marketplace
```

### Local Development

```
/plugin marketplace add ./path/to/data-wrangler-plugin
/plugin install data-wrangler@data-wrangler-marketplace
```

## Usage

Once installed, Claude will automatically use this skill when you ask data transformation questions.

### Examples

**Simple file query:**
> "What are the top 10 products by revenue in sales.csv?"

**Join multiple files:**
> "Join orders.parquet with customers.csv and show total orders per customer"

**Export to Parquet:**
> "Filter active users from users.csv and save as users_active.parquet"

**Create partitioned dataset:**
> "Convert events.json to Parquet partitioned by year and month"

## Secrets Management

Store database and cloud credentials securely using a YAML secrets file with environment variable substitution.

**Create `secrets.yaml`:**
```yaml
secrets:
  my_postgres:
    type: postgres
    host: db.example.com
    user: analyst
    password: "${PGPASSWORD}"  # Uses environment variable
    database: analytics
```

**Supported secret types:**
- **Databases**: PostgreSQL, MySQL
- **Cloud storage**: AWS S3, Azure Blob, Google Cloud Storage, Cloudflare R2
- **HTTP**: Bearer token authentication
- **Other**: HuggingFace, Iceberg, DuckLake

See [SECRETS.md](skills/data-wrangler/SECRETS.md) for full configuration options.

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
data-wrangler-plugin/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace definition
├── skills/
│   └── data-wrangler/
│       ├── SKILL.md         # Skill instructions for Claude
│       ├── SECRETS.md       # Secrets management docs
│       ├── TRANSFORMS.md    # Advanced SQL patterns
│       └── scripts/
│           └── query_duckdb.py  # DuckDB query engine
├── tests/                   # Test suite
└── README.md
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please open an issue or pull request.
