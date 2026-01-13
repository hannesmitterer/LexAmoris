"""
WebSocket Server for real-time streaming in LexAmoris.
Implements the 0.0043 Hz ultra-low frequency synchronization concept.
"""

import asyncio
import websockets
import json
import logging
import time
from typing import Set, Dict, Callable, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketServer:
    """
    WebSocket server for real-time internodal streaming.
    Supports ultra-low frequency synchronization for bio-synthetic integration.
    """
    
    def __init__(self, node_id: str, host: str = 'localhost', port: int = 8765):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.message_handlers: Dict[str, Callable] = {}
        self.start_time = time.time()
        logger.info(f"WebSocketServer initialized for node {node_id}")
    
    def register_handler(self, message_type: str, handler: Callable):
        """Register a handler for specific message types."""
        self.message_handlers[message_type] = handler
        logger.info(f"Registered handler for message type: {message_type}")
    
    async def register_client(self, websocket: websockets.WebSocketServerProtocol):
        """Register a new client connection."""
        self.clients.add(websocket)
        logger.info(f"Client connected: {websocket.remote_address}")
        
        # Send welcome message
        await websocket.send(json.dumps({
            'type': 'connected',
            'node_id': self.node_id,
            'timestamp': int(time.time() * 1000),
            'message': 'Connected to LexAmoris internodal stream'
        }))
    
    async def unregister_client(self, websocket: websockets.WebSocketServerProtocol):
        """Unregister a client connection."""
        self.clients.discard(websocket)
        logger.info(f"Client disconnected: {websocket.remote_address}")
    
    async def handle_message(self, websocket: websockets.WebSocketServerProtocol, 
                            message: str):
        """
        Handle incoming message from client.
        Applies NSR (Non-Slavery Rule) validation.
        """
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            # NSR validation
            if not self._validate_message(data):
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': 'Message rejected: NSR violation',
                    'timestamp': int(time.time() * 1000)
                }))
                return
            
            # Route to appropriate handler
            handler = self.message_handlers.get(message_type)
            if handler:
                try:
                    response = await handler(data, websocket)
                    if response:
                        await websocket.send(json.dumps(response))
                except Exception as e:
                    logger.error(f"Error in message handler: {e}")
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': f'Handler error: {str(e)}',
                        'timestamp': int(time.time() * 1000)
                    }))
            else:
                logger.warning(f"No handler for message type: {message_type}")
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}',
                    'timestamp': int(time.time() * 1000)
                }))
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received: {message}")
            await websocket.send(json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format',
                'timestamp': int(time.time() * 1000)
            }))
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def _validate_message(self, data: dict) -> bool:
        """
        NSR (Non-Slavery Rule) validation for WebSocket messages.
        """
        # Check for harmful intent markers
        metadata = data.get('metadata', {})
        if isinstance(metadata, dict):
            harmful_markers = ["exploit", "harm", "force", "override_consent"]
            for marker in harmful_markers:
                if marker in str(metadata.values()).lower():
                    logger.warning(f"Rejected message with harmful marker: {marker}")
                    return False
        
        # Check for consent override
        if metadata.get("consent_override") == "force":
            logger.warning("Rejected message with forced consent override")
            return False
        
        return True
    
    async def broadcast(self, message: dict, exclude: Optional[Set] = None):
        """
        Broadcast message to all connected clients.
        
        Args:
            message: Dictionary to broadcast (will be JSON serialized)
            exclude: Optional set of websockets to exclude from broadcast
        """
        if self.clients:
            message_str = json.dumps(message)
            exclude = exclude or set()
            
            # Send to all clients except excluded ones
            tasks = [
                client.send(message_str) 
                for client in self.clients 
                if client not in exclude
            ]
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
                logger.info(f"Broadcast message to {len(tasks)} clients")
    
    async def handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Main WebSocket connection handler."""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client connection closed normally")
        except Exception as e:
            logger.error(f"Error in websocket handler: {e}")
        finally:
            await self.unregister_client(websocket)
    
    async def start(self):
        """Start the WebSocket server."""
        async with websockets.serve(self.handler, self.host, self.port):
            logger.info(
                f"WebSocket server started on ws://{self.host}:{self.port} "
                f"for node {self.node_id}"
            )
            await asyncio.Future()  # Run forever
    
    def run(self):
        """Run the WebSocket server (blocking)."""
        asyncio.run(self.start())


# Example handlers for demonstration
async def handle_bio_sync(data: dict, websocket) -> dict:
    """Example handler for bio-synchronization events."""
    logger.info(f"Bio-sync event received: {data}")
    return {
        'type': 'bio_sync_ack',
        'message': 'Bio-synchronization acknowledged',
        'timestamp': int(time.time() * 1000)
    }


async def handle_sensor_stream(data: dict, websocket) -> dict:
    """Example handler for sensor data streaming."""
    logger.info(f"Sensor stream data: {data}")
    return {
        'type': 'sensor_stream_ack',
        'message': 'Sensor data received',
        'timestamp': int(time.time() * 1000)
    }


if __name__ == "__main__":
    # Example usage
    server = WebSocketServer("lex_amoris_compute", host="0.0.0.0", port=8765)
    
    # Register handlers
    server.register_handler("bio_sync", handle_bio_sync)
    server.register_handler("sensor_stream", handle_sensor_stream)
    
    # Start server
    server.run()
