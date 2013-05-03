from kombu import Exchange, Queue
from urllib import quote_plus

from kombu import Connection
from kombu.utils.debug import setup_logging

# setup root logger
setup_logging(loglevel='INFO', loggers=[''])

def create_connection():
  conn_string = 'marconi://%s:%s@166.78.143.130//' % ('jarret', quote_plus('6QlxRC&%b3Mn2Y&f6jL9'))
  transport_options = {
    "tenant_id": 98765,
    "client_id": 12345,
    "auth_endpoint": "https://identity.api.rackspacecloud.com/v2.0"
  }

  return Connection(conn_string, transport_options=transport_options, ssl=False)  

task_exchange = Exchange('tasks', type='direct')
task_queues = [Queue('hipri', task_exchange, routing_key='hipri'),
               Queue('midpri', task_exchange, routing_key='midpri'),
               Queue('lopri', task_exchange, routing_key='lopri')]