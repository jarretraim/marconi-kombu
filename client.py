from kombu.common import maybe_declare
from kombu.log import get_logger
from kombu.pools import producers

from queues import task_exchange, create_connection

import time

logger = get_logger(__name__)

priority_to_routing_key = {'high': 'hipri',
                           'mid': 'midpri',
                           'low': 'lopri'}


def send_as_task(connection, payload={}, kwargs={}, priority='mid'):
    routing_key = priority_to_routing_key[priority]

    with producers[connection].acquire(block=True) as producer:
        producer.publish(payload,
                         serializer='json',
                         compression='bzip2',
                         exchange=task_exchange,
                         declare=[task_exchange],
                         routing_key=routing_key)

if __name__ == '__main__':
    from tasks import hello_task

    connection = create_connection()
    logger.info (connection.info())    

    #for i in range (1, 10):
    payload = { 'message': 'Test message' }
    send_as_task(connection, payload=payload, kwargs={},
               priority='high')
    #  logger.info ("Message %d sent." % (i))

