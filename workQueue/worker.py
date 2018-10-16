#!/usr/bin/env python
import pika
import time
from subprocess import call

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'$
# can change the localhost with th eip address of the producer of the rabbitmq 
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    #if body == "true":
    call(["sudo","docker","run","--privileged","--name","t4","-it","-p","8080",$

    '''print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)'''

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,queue='task_queue')

channel.start_consuming()


