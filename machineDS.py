# Datastructure for a machine object
# {
#   id : someid,
#   type : undefined,
#   timestamp : timestamp
#   data : [
#     {
#       value : val,
#       type  : temperatur | level | hummidity | power
#       unit : C | F | %
#     } ,
#     {
#       value : val,
#       type  : temperatur | level | hummidity
#       unit : C | F | % | W
#     } ,
#     {
#       value : val,
#       type  : temperatur | level | hummidity
#       unit : C | F | %
#     } ,
#     ]
#
#
#

import random
import json
import time
import os
import pika

def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

def valStruct(val, type="temperatur", unit="C", description=""):
    return { "value": val, "type": type, "unit":unit, "description":description}

try:

    ids = []
    supply = []
    unique_sequence = uniqueid()

    host = os.environ.get('HOST_RABBITMQ')
    max_machine = os.environ.get('SENSOR')
    print os.environ.get('HOME')
    print host
    print max_machine

    if host == None:
        host = "192.168.99.100"
    if max_machine == None:
        max_machine = 3
    else:
        max_machine = int(max_machine)

    print "################################"
    print "# Starting IoT Sensor Simulator "
    print "# Queue: %s" % (host)
    print "# Sensor: %i" % (max_machine)
    print "################################"

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.99.100"))
    channel = connection.channel()
    channel.queue_declare(queue='HackZurich16')

    for i in range(0,max_machine):
        ids.append(next(unique_sequence))
        supply.append(100.0)
    print ids
    print supply

    while True:

        for i in range(0,max_machine):
            supply[i] = supply[i] - random.randint(0,30)/10
            if supply[i] <= 0.0:
                supply[i] = 100.0
            myData = { 'id' : ids[i], 'type' : 'undefined', 'timestamp': time.time(),'data' : [] }
            myData['data'].append(valStruct(random.randint(0,30),description='Environment Temp'))
            myData['data'].append(valStruct(random.randint(20,50),description='Operational Temp'))
            myData['data'].append(valStruct(random.randint(0,100),type='humidity',unit="%", description='Environment Humidity'))
            myData['data'].append(valStruct(random.randint(300,1500),type='power',unit="W", description='Power Consumption'))
            myData['data'].append(valStruct(supply[i],type='level',unit="%", description='Supply Fill Level'))

            channel.basic_publish(exchange='',
                              routing_key='HackZurich16',
                              body=json.dumps(myData))
            print "[x] sent Data:", myData
            time.sleep(random.randint(0,3))

except KeyboardInterrupt:
    pass

