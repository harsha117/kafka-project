import json
import asyncio
import websockets
from kafka import KafkaConsumer

# Kafka consumer setup
consumer = KafkaConsumer(
    "product-price-update", "product-discount-update", "country-update",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='product-consumers',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

print("Consumer is running...")

# WebSocket URL for FastAPI dashboard
WEB_SOCKET_URL = "ws://localhost:3000/ws"

# Function to send message to WebSocket server
async def send_to_dashboard(message):
    try:
        async with websockets.connect(WEB_SOCKET_URL) as websocket:
            await websocket.send(json.dumps(message))  # Send the message
            print("Message sent to dashboard", message)
    except Exception as e:
        print("Error sending to dashboard:", e)

# Start an asyncio loop to handle sending messages
async def consume_and_send():
    for message in consumer:
        print(f"Received message from topic {message.topic}: {message.value}")
        event_data = {
            "event_type": message.topic,
            "data": message.value
        }

        # Send to the dashboard asynchronously
        await send_to_dashboard(event_data)

        # Simulate processing
        if message.topic == "product-price-update":
            print("Processing price update")
        elif message.topic == "product-discount-update":
            print("Processing discount update")
        elif message.topic == "country-update":
            print("Processing country-specific data")

# Run the consumer asynchronously using asyncio.run
if __name__ == "__main__":
    asyncio.run(consume_and_send())
