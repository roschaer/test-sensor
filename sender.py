import pika
import time
import random
import json
import os

print os.environ['HOST_RABBITMQ']
host = os.environ['HOST_RABBITMQ']
connection = 'pika.BlockingConnection(pika.ConnectionParameters(host=%s))'%(host)
channel = connection.channel()
channel.queue_declare(queue='hello')




while True:
    text = '{Sender: Machine%i; Value:%i}'% (random.randint(1,3),random.randint(1,10))
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=text)
    print(" [x] Sent ", text)
    time.sleep(random.randint(1,3))

connection.close()
