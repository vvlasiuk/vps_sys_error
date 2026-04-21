import pika
import json
import time
from config import get_env

RABBITMQ_HOST = get_env('RABBITMQ_HOST')
RABBITMQ_PORT = int(get_env('RABBITMQ_PORT', 5672))
RABBITMQ_USER = get_env('RABBITMQ_USER')
RABBITMQ_PASSWORD = get_env('RABBITMQ_PASSWORD')
RABBITMQ_VHOST = get_env('RABBITMQ_VHOST', '/')
RABBITMQ_QUEUE = get_env('RABBITMQ_QUEUE')
OUTPUT_QUEUES = {
    'telegram': {
        'queue': get_env('OUTPUT_TELEGRAM_QUEUE'),
        'exchange': get_env('OUTPUT_TELEGRAM_EXCHANGE'),
        'routing_key': get_env('OUTPUT_TELEGRAM_ROUTING_KEY'),
    },
    'email': {
        'queue': get_env('OUTPUT_EMAIL_QUEUE'),
        'exchange': get_env('OUTPUT_EMAIL_EXCHANGE'),
        'routing_key': get_env('OUTPUT_EMAIL_ROUTING_KEY'),
    },
    'slack': {
        'queue': get_env('OUTPUT_SLACK_QUEUE'),
        'exchange': get_env('OUTPUT_SLACK_EXCHANGE'),
        'routing_key': get_env('OUTPUT_SLACK_ROUTING_KEY'),
    },
}
RETRY_DELAY = int(get_env('RETRY_DELAY', 60))

class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
        creds = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        params = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            virtual_host=RABBITMQ_VHOST,
            credentials=creds
        )
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        # Не конфігуруємо черги, лише використовуємо існуючі

    def get_message(self):
        method, props, body = self.channel.basic_get(queue=RABBITMQ_QUEUE, auto_ack=True)
        if body:
            return json.loads(body)
        return None

    def send_message(self, queue_name, msg):
        # queue_name: логічне ім'я ('telegram', 'email', 'slack')
        qcfg = OUTPUT_QUEUES.get(queue_name)
        if not qcfg:
            print(f"[RabbitMQ] Unknown queue: {queue_name}")
            return
        self.channel.basic_publish(
            exchange=qcfg['exchange'],
            routing_key=qcfg['routing_key'],
            body=json.dumps(msg, ensure_ascii=False).encode('utf-8'),
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def close(self):
        if self.connection:
            self.connection.close()
