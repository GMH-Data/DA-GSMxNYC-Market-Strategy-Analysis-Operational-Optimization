import duckdb
con = duckdb.connect(":memory:")
con.execute("CREATE VIEW test_v AS SELECT 1")
try:
    con.execute("DROP TABLE IF EXISTS test_v")
    print("DROP TABLE test_v worked")
except Exception as e:
    print(f"DROP TABLE test_v failed: {e}")

con.execute("DROP VIEW IF EXISTS test_v")
print("DROP VIEW test_v worked")

con.execute("CREATE TABLE test_t (id INT)")
try:
    con.execute("DROP VIEW IF EXISTS test_t")
    print("DROP VIEW test_t worked")
except Exception as e:
    print(f"DROP VIEW test_t failed: {e}")

con.execute("DROP TABLE IF EXISTS test_t")
print("DROP TABLE test_t worked")
