
#!/usr/bin/env python
import pika
import sys
import urllib
import json
url = "http://sdnonlinelab.com/webservice.php"
response = urllib.urlopen(url)
data = json.loads(response.read())
print type(data)

#print data
for var, value in data.items():
        if var == 'controller':
                controller = value 

        if var == 'topology':
                topology = value 

        if var == 'hosts':
        		hosts = value 

        if var == 'switches':
                switches = value 

        if var == 'command':        # add extra ifs for any new data from json $
                command = value 


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'$
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

task_message = [controller, topology, hosts, switches, command]
#print task_message 

for i in range(len(task_message)): 
        message = task_message[i]
        channel.basic_publish(exchange='',
        					  routing_key='task_queue',
                              body=message,
                              properties=pika.BasicProperties(
                                 delivery_mode = 2, # make message persistent
                              ))
        print(" [x] Sent %r" % message)

connection.close()






