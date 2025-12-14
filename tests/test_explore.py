"""Tests for explore mode functionality."""

import json
import subprocess
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).parent.parent / "skills" / "data-wrangler" / "scripts" / "query_duckdb.py"


def run_script(request: dict) -> dict:
    """Run the query script with the given request and return parsed output."""
    result = subprocess.run(
        ["uv", "run", str(SCRIPT_PATH)],
        input=json.dumps(request),
        capture_output=True,
        text=True,
        cwd=SCRIPT_PATH.parent,
    )
    
    # Try to parse as JSON
    output = result.stdout.strip()
    if not output:
        return {"error": f"No output. stderr: {result.stderr}"}
    
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        # Might be markdown output, return as-is
        return {"raw_output": output}


class TestExploreCSV:
    """Test explore mode with CSV files."""

    def test_explore_csv_returns_schema(self, tmp_path):
        """Test that explore returns column names and types."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("id,name,value\n1,alice,100\n2,bob,200\n")
        
        req = {"mode": "explore", "path": str(csv_file)}
        result = run_script(req)
        
        assert "error" not in result, f"Explore failed: {result}"
        assert "columns" in result
        columns = result["columns"]
        assert len(columns) == 3
        
        col_names = [c["name"] for c in columns]
        assert "id" in col_names
        assert "name" in col_names
        assert "value" in col_names

    def test_explore_csv_returns_row_count(self, tmp_path):
        """Test that explore returns correct row count."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("id,name\n1,a\n2,b\n3,c\n4,d\n5,e\n")
        
        req = {"mode": "explore", "path": str(csv_file)}
        result = run_script(req)
        
        assert result.get("row_count") == 5

    def test_explore_csv_returns_null_counts(self, tmp_path):
        """Test that explore returns null counts per column."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("id,name,value\n1,alice,100\n2,,200\n3,charlie,\n")
        
        req = {"mode": "explore", "path": str(csv_file)}
        result = run_script(req)
        
        columns = result["columns"]
        name_col = next(c for c in columns if c["name"] == "name")
        value_col = next(c for c in columns if c["name"] == "value")
        
        assert name_col["null_count"] == 1
        assert value_col["null_count"] == 1

    def test_explore_csv_returns_sample(self, tmp_path):
        """Test that explore returns sample rows as markdown."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("id,name\n1,alice\n2,bob\n")
        
        req = {"mode": "explore", "path": str(csv_file)}
        result = run_script(req)
        
        assert "sample" in result
        sample = result["sample"]
        assert "id" in sample
        assert "name" in sample
        assert "alice" in sample

    def test_explore_csv_returns_format(self, tmp_path):
        """Test that explore detects file format."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("id\n1\n")
        
        req = {"mode": "explore", "path": str(csv_file)}
        result = run_script(req)
        
        assert result.get("format") == "csv"
        assert result.get("file") == str(csv_file)


class TestExploreParquet:
    """Test explore mode with Parquet files."""

    def test_explore_parquet(self, tmp_path):
        """Test explore works with Parquet files."""
        # First create a parquet file using write mode
        parquet_file = tmp_path / "data.parquet"
        write_req = {
            "query": "SELECT 1 as id, 'hello' as msg UNION ALL SELECT 2, 'world'",
            "output": {"path": str(parquet_file), "format": "parquet"},
        }
        run_script(write_req)
        
        # Now explore it
        req = {"mode": "explore", "path": str(parquet_file)}
        result = run_script(req)
        
        assert result.get("format") == "parquet"
        assert result.get("row_count") == 2
        assert len(result.get("columns", [])) == 2


class TestExploreJSON:
    """Test explore mode with JSON files."""

    def test_explore_json_array(self, tmp_path):
        """Test explore works with JSON array files."""
        json_file = tmp_path / "data.json"
        json_file.write_text('[{"id": 1, "name": "alice"}, {"id": 2, "name": "bob"}]')
        
        req = {"mode": "explore", "path": str(json_file)}
        result = run_script(req)
        
        assert result.get("format") == "json"
        assert result.get("row_count") == 2

    def test_explore_ndjson(self, tmp_path):
        """Test explore works with newline-delimited JSON."""
        ndjson_file = tmp_path / "data.ndjson"
        ndjson_file.write_text('{"id": 1}\n{"id": 2}\n{"id": 3}\n')
        
        req = {"mode": "explore", "path": str(ndjson_file)}
        result = run_script(req)
        
        assert result.get("format") == "ndjson"
        assert result.get("row_count") == 3


class TestExploreOptions:
    """Test explore mode options."""

    def test_sample_rows_parameter(self, tmp_path):
        """Test sample_rows controls sample size."""
        csv_file = tmp_path / "data.csv"
        # Create 20 rows
        lines = ["id"] + [str(i) for i in range(20)]
        csv_file.write_text("\n".join(lines))
        
        req = {"mode": "explore", "path": str(csv_file), "sample_rows": 5}
        result = run_script(req)
        
        # Sample should show only 5 rows
        sample_lines = result["sample"].strip().split("\n")
        # Markdown table: header + separator + 5 data rows = 7 lines
        assert len(sample_lines) <= 8  # Allow some flexibility


class TestExploreErrors:
    """Test explore mode error handling."""

    def test_explore_nonexistent_file(self, tmp_path):
        """Test explore returns error for missing file."""
        req = {"mode": "explore", "path": str(tmp_path / "nonexistent.csv")}
        result = run_script(req)
        
        assert "error" in result

    def test_explore_requires_path_or_sources(self):
        """Test explore requires path or sources."""
        req = {"mode": "explore"}
        result = run_script(req)
        
        assert "error" in result
        assert "path" in result["error"].lower() or "sources" in result["error"].lower()


class TestExploreWithSources:
    """Test explore mode with database-style sources."""

    def test_explore_via_source_alias(self, tmp_path):
        """Test explore works with sources array."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("id,value\n1,100\n2,200\n")
        
        req = {
            "mode": "explore",
            "sources": [
                {"type": "file", "alias": "mydata", "path": str(csv_file)}
            ],
        }
        result = run_script(req)
        
        assert "error" not in result, f"Explore failed: {result}"
        assert result.get("row_count") == 2
        assert result.get("source") == "mydata"
