import glob
import os
import duckdb

def init_duckdb(dataset_path="Dataset", db_path="src/taxi_data.duckdb", read_only=False):
    """
    Initializes a DuckDB connection. 
    Set read_only=True if another process is already using the database in write mode.
    """
    print(f"Connecting to DuckDB at {db_path} (read_only={read_only})...")
    try:
        con = duckdb.connect(db_path, read_only=read_only)
    except duckdb.IOException as e:
        if "used by another process" in str(e) and not read_only:
            print("  [INFO] Database is locked by another process. Attempting read-only connection...")
            con = duckdb.connect(db_path, read_only=True)
        else:
            raise e
    
    # Enable progress bar for long-running materialization tasks
    con.execute("SET enable_progress_bar = true;")

    periods = ["Pre_2019", "2019-2025", "2026_plus"]
    taxi_types = ["yellow", "green", "fhv", "fhvhv"]
    
    for period in periods:
        for taxi_type in taxi_types:
            # Construct the path pattern: Dataset/<period>/<taxi_type>/*.parquet
            pattern = os.path.join(dataset_path, period, taxi_type, "*.parquet")

            # Check if files exist for this pattern
            files = glob.glob(pattern)
            if files:
                # Table name in SQL: yellow_Pre_2019 (replace '-' with '_')
                table_name = f"{taxi_type}_{period.replace('-', '_')}"
                
                # Use forward slashes for DuckDB
                pattern_str = pattern.replace("\\", "/")
                
                # Create VIEWs for all tables to ensure instant initialization
                print(f"Creating VIEW '{table_name}' from {len(files)} files...")
                
                # Robustly ensure the name is free regardless of whether it was a TABLE or VIEW
                try:
                    con.execute(f"DROP VIEW IF EXISTS {table_name};")
                except duckdb.CatalogException:
                    pass
                try:
                    con.execute(f"DROP TABLE IF EXISTS {table_name};")
                except duckdb.CatalogException:
                    pass
                
                con.execute(f"CREATE OR REPLACE VIEW {table_name} AS SELECT * FROM read_parquet('{pattern_str}', union_by_name=True);")
                print(f"  [OK] View {table_name} created.")
            else:
                # Optional: print debug info if needed
                pass

    # Load taxi zone lookup from the Dataset root
    zone_file = os.path.join(dataset_path, "taxi_zone_lookup.csv")
    if os.path.exists(zone_file):
        print("Creating table 'taxi_zone_lookup' from CSV...")
        zone_file_str = zone_file.replace("\\", "/")
        # Ensure name is free for TABLE
        try:
            con.execute("DROP VIEW IF EXISTS taxi_zone_lookup;")
        except duckdb.CatalogException:
            pass
        con.execute(
            f"CREATE OR REPLACE TABLE taxi_zone_lookup AS SELECT * FROM read_csv_auto('{zone_file_str}');"
        )
        print("  [OK] Table taxi_zone_lookup created.")
    else:
        print("  ! taxi_zone_lookup.csv not found.")

    print("Database initialization complete.")
    return con


if __name__ == "__main__":
    init_duckdb()
