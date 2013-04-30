from __future__ import with_statement

from kombu.mixins import ConsumerMixin
from kombu.utils import kwdict, reprcall

from queues import task_queues


class Worker(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=task_queues,
                         callbacks=[self.process_task])]

    def process_task(self, body, message):
        fun = body['fun']
        args = body['args']
        kwargs = body['kwargs']
        print 'Got task: %s', reprcall(fun.__name__, args, kwargs)
        try:
            fun(*args, **kwdict(kwargs))
        except Exception, exc:
            print 'task raised exception: %r', exc
        message.ack()

    def on_connection_error(self, exc, interval):
        print "Connection error"

    def on_consume_ready(self, connection, channel, consumers):
        print "Ready to consume messages"


if __name__ == '__main__':
    from kombu import Connection

    with Connection('amqp://guest:guest@192.168.64.10:5672//') as conn:
        try:
            print "Starting Worker"
            Worker(conn).run()
        except KeyboardInterrupt:
            print('bye bye')







