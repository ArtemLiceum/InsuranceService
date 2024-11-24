from confluent_kafka import Producer
import json
from datetime import datetime
import logging
import os

producer = Producer({
    'bootstrap.servers': f"{os.getenv('KAFKA_IP')}:{os.getenv('KAFKA_PORT')}",
    'client.id': 'insurance_service'
})

# Функция для отправки сообщений в Kafka
def send_kafka_message(topic: str, message: dict):
    try:
        producer.produce(topic, json.dumps(message).encode('utf-8'))
        producer.flush()  # Ожидаем, чтобы сообщение было отправлено
    except Exception as e:
        logging.error(f"Failed to send Kafka message: {e}")
        logging.error(f"Message: {message}")

# Логирование действия
def log_action(action, details):
    event_time = datetime.utcnow().isoformat()  # Время события в UTC
    message = {
        "action": action,
        "details": details,
        "event_time": event_time
    }
    send_kafka_message("rate_changes_topic", message)
