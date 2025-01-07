from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json
from pathlib import Path
import asyncio

app = FastAPI()

# WebSocket connections storage
active_connections = set()

# Path to the HTML file
dashboard_html_path = Path("html/dashboard.html")

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serves a simple HTML dashboard."""
    if not dashboard_html_path.exists():
        return HTMLResponse(content="<h1>Dashboard HTML file not found.</h1>", status_code=404)
    return HTMLResponse(content=dashboard_html_path.read_text())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    active_connections.add(websocket)
    print("Websocket connected:", websocket)

    try:
        while True:
            # Receive a message from a WebSocket client
            message = await websocket.receive_text()
            print("Received message from WebSocket client:", message)
            
            # Parse the message and broadcast it to all active connections
            try:
                parsed_message = json.loads(message)
                send_message_to_clients(parsed_message)
            except json.JSONDecodeError:
                print("Invalid JSON format received from client:", message)
    except Exception as e:
        print("Error in WebSocket connection:", e)
    finally:
        active_connections.remove(websocket)
        print("WebSocket disconnected:", websocket)

def send_message_to_clients(message: dict):
    """Sends a message to all active WebSocket clients."""
    if not active_connections:
        print("No active WebSocket connections.")
        return

    for connection in active_connections:
        try:
            print("Attempting to send message to connection:", connection)
            asyncio.create_task(connection.send_text(json.dumps(message)))
        except Exception as e:
            print(f"Error sending message to connection {connection}: {e}")
    else:
        print("Message sent to all active WebSocket clients.")

# This endpoint will be triggered by the consumer (via WebSocket message)
@app.on_event("startup")
async def on_startup():
    print("FastAPI Dashboard Started")
