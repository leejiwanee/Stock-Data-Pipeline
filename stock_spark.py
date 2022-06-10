from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
import datetime
time_stamp = datetime.datetime.now()
time_stamp = time_stamp.strftime('%Y_%m_%d')
def write_to_mysql(target_df,batch_id):
    target_df.write \
        .format("jdbc") \
            .option("url","jdbc:mysql://localhost:3306/stockspark") \
                .option("driver","com.mysql.cj.jdbc.Driver") \
                    .option("dbtable",str(time_stamp)+'_stock') \
                        .option("user","root") \
                            .option("password","Wldhks96!") \
                                .save()
    target_df.show()


if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("stock") \
            .config("local[*]") \
                .config("spark.sql.stopGracefullyOnShutDown","true") \
                    .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,mysql:mysql-connector-java:8.0.26") \
                        .getOrCreate()
    

    kafkastream = spark.readStream \
        .format("kafka") \
            .option("kafka.bootstrap.servers","localhost:9092") \
                .option("subscribe","stocks") \
                    .option("startingOffsets","earliest") \
                        .load() \

    print("printing kafkastream Schema")                            
    kafkastream.printSchema()
    kafkadata = kafkastream.select(from_csv(col("value").cast("string"),('Index INT,Name STRING,Price DOUBLE, Change STRING, PercentChange STRING')).alias("stocks"))
    kafkadata.printSchema()

    stock_data = kafkadata.select("stocks.*")
    
    path = os.path.dirname(os.path.realpath(__file__))
    output = stock_data.writeStream \
        .foreachBatch(write_to_mysql) \
            .outputMode("update") \
                .option("checkpointLocation", '/home/jiwan/Python/DE Project/StockDataPipeline/') \
                    .start()
    
    output.awaitTermination()
    

    

