import kafka
import datetime
import os
producer = kafka.KafkaProducer(bootstrap_servers=['localhost:9092'])

time_stamp = datetime.datetime.now()
time_stamp = time_stamp.strftime('%Y-%m-%d')
path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path,"results/",str(time_stamp)+' stock data.csv'), 'r') as f:
  count = 0
  for line in f:
    producer.send('stocks', line.rstrip().encode())
    count += 1
  print(count, "records has been produced in 'stocks'")
producer.flush()