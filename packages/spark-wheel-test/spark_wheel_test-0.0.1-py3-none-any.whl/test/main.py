from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test").getOrCreate()

data = [[1, "Daniel"], [2, "Geri"], [3, "Christopher"]]
df = spark.createDataFrame(data, ["id", "name"])

df.show()