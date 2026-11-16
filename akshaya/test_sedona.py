
from sedona.spark import SedonaContext

# Configure Spark with the matching Apache Sedona library
config = (
    SedonaContext.builder()
    .master("local[2]")
    .appName("GeoPulse-Sedona-Test")
    .config(
        "spark.jars.packages",
        "org.apache.sedona:sedona-spark-3.5_2.12:1.9.1"
    )
    .getOrCreate()
)

# Initialize Sedona
sedona = SedonaContext.create(config)

print("Spark and Sedona started successfully!")

# Test a geographic point
sedona.sql("""
    SELECT ST_AsText(
        ST_Point(78.4867, 17.3850)
    ) AS location
""").show(truncate=False)

# Stop Spark
sedona.stop()
