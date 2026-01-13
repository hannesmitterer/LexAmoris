"""
WebSocket Client for real-time streaming in LexAmoris.
"""

import asyncio
import websockets
import json
import logging
import time
from typing import Callable, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketClient:
    """
    WebSocket client for connecting to other nodes in the LexAmoris network.
    """
    
    def __init__(self, node_id: str, target_uri: str = 'ws://localhost:8765'):
        self.node_id = node_id
        self.target_uri = target_uri
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.message_handlers: dict = {}
        self.connected = False
        logger.info(f"WebSocketClient initialized for node {node_id}")
    
    def register_handler(self, message_type: str, handler: Callable):
        """Register a handler for specific message types."""
        self.message_handlers[message_type] = handler
        logger.info(f"Registered handler for message type: {message_type}")
    
    async def connect(self):
        """Establish WebSocket connection to target node."""
        try:
            self.websocket = await websockets.connect(self.target_uri)
            self.connected = True
            logger.info(f"Connected to {self.target_uri}")
            
            # Start receiving messages
            asyncio.create_task(self._receive_messages())
            
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    async def disconnect(self):
        """Close the WebSocket connection."""
        if self.websocket and self.connected:
            await self.websocket.close()
            self.connected = False
            logger.info(f"Disconnected from {self.target_uri}")
    
    async def send_message(self, message_type: str, data: dict, 
                          metadata: Optional[dict] = None):
        """
        Send a message to the target node.
        
        Args:
            message_type: Type of message
            data: Message data dictionary
            metadata: Optional metadata
        """
        if not self.connected or not self.websocket:
            raise ConnectionError("Not connected to server")
        
        message = {
            'type': message_type,
            'source_node': self.node_id,
            'data': data,
            'metadata': metadata or {},
            'timestamp': int(time.time() * 1000)
        }
        
        try:
            await self.websocket.send(json.dumps(message))
            logger.info(f"Sent message type: {message_type}")
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise
    
    async def stream_data(self, stream_type: str, data_generator, 
                         interval: float = 0.1):
        """
        Stream data continuously to the target node.
        
        Args:
            stream_type: Type of stream
            data_generator: Generator yielding data to stream
            interval: Time interval between messages in seconds
        """
        if not self.connected or not self.websocket:
            raise ConnectionError("Not connected to server")
        
        try:
            for data in data_generator:
                await self.send_message(stream_type, data)
                await asyncio.sleep(interval)
        except Exception as e:
            logger.error(f"Error during streaming: {e}")
            raise
    
    async def _receive_messages(self):
        """Continuously receive and process messages from server."""
        try:
            async for message in self.websocket:
                await self._handle_message(message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Server connection closed")
            self.connected = False
        except Exception as e:
            logger.error(f"Error receiving messages: {e}")
            self.connected = False
    
    async def _handle_message(self, message: str):
        """Handle incoming message from server."""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            logger.info(f"Received message type: {message_type}")
            
            # Route to appropriate handler
            handler = self.message_handlers.get(message_type)
            if handler:
                try:
                    await handler(data)
                except Exception as e:
                    logger.error(f"Error in message handler: {e}")
            else:
                # Default handling for common message types
                if message_type == 'connected':
                    logger.info(f"Connected to node: {data.get('node_id')}")
                elif message_type == 'error':
                    logger.error(f"Server error: {data.get('message')}")
                else:
                    logger.debug(f"Unhandled message type: {message_type}")
                    
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received: {message}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def send_bio_sync(self, sync_data: dict):
        """Send bio-synchronization event."""
        await self.send_message('bio_sync', sync_data)
    
    async def send_sensor_stream(self, sensor_data: dict):
        """Send sensor stream data."""
        await self.send_message('sensor_stream', sensor_data)


async def example_usage():
    """Example usage of WebSocketClient."""
    client = WebSocketClient("bio_synth_ai_control", "ws://localhost:8765")
    
    # Define message handlers
    async def handle_ack(data):
        logger.info(f"Acknowledgment received: {data}")
    
    client.register_handler("bio_sync_ack", handle_ack)
    client.register_handler("sensor_stream_ack", handle_ack)
    
    # Connect
    await client.connect()
    
    try:
        # Send bio-sync event
        await client.send_bio_sync({
            'frequency': 0.0043,
            'phase': 'synchronizing',
            'mycelium_nodes': ['node_01', 'node_02', 'node_03']
        })
        
        # Stream sensor data
        async def sensor_data_generator():
            for i in range(5):
                yield {
                    'sensor_id': 'bio_sensor_01',
                    'temperature': 22.5 + i * 0.1,
                    'humidity': 65 + i,
                    'mycelium_growth_rate': 0.0043
                }
        
        await client.stream_data('sensor_stream', sensor_data_generator(), interval=1.0)
        
        # Keep connection alive for a bit
        await asyncio.sleep(5)
        
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(example_usage())
