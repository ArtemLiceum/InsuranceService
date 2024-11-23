from confluent_kafka import Producer
import json
from datetime import datetime
import logging
import os


producer = Producer({
    'bootstrap.servers': f'{os.getenv('KAFKA_IP')}:{os.getenv('KAFKA_PORT')}',  #('localhost:29092'),  # Укажите адрес вашего Kafka брокера
    'client.id': 'insurance_service'
})

# Функция для отправки сообщений в Kafka
def send_kafka_message(topic: str, message: dict):
    producer.produce(topic, json.dumps(message).encode('utf-8'))
    producer.flush()  # Ожидаем, чтобы сообщение было отправлено

# Логирование действия
def log_action(action, details):
    event_time = datetime.utcnow().isoformat()  # Время события в UTC
    message = {
        "action": action,
        "details": details,
        "event_time": event_time
    }
    send_kafka_message("rate_changes_topic", message)
    logging.info(f"Performed {action} at {event_time} with details: {details}")
