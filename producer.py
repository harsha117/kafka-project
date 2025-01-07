# producer.py: A FastAPI application to publish messages to Kafka.

from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer
from pydantic import BaseModel
import json

app = FastAPI()

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)

class EventData(BaseModel):
    event_type: str
    data: dict

@app.post("/publish-event")
async def publish_event(event: EventData):
    """Endpoint to publish product-related events."""
    if event.event_type not in ["product-price-update", "product-discount-update", "country-update"]:
        raise HTTPException(status_code=400, detail="Invalid event type")

    try:
        producer.send(event.event_type, value=event.data)
        producer.flush()
        return {"status": "success", "event_type": event.event_type, "data": event.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish event: {str(e)}")