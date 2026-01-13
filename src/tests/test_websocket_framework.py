"""
Tests for WebSocket framework internodal streaming.
"""

import pytest
import asyncio
import json
import time

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from websocket_framework.websocket_server import WebSocketServer
from websocket_framework.websocket_client import WebSocketClient


class TestWebSocketServer:
    """Test suite for WebSocketServer."""
    
    def test_initialization(self):
        """Test server initialization."""
        server = WebSocketServer("test_node", "localhost", 8765)
        assert server.node_id == "test_node"
        assert server.host == "localhost"
        assert server.port == 8765
        assert isinstance(server.clients, set)
        assert isinstance(server.message_handlers, dict)
    
    def test_register_handler(self):
        """Test registering message handlers."""
        server = WebSocketServer("test_node")
        
        async def handler(data, websocket):
            return {"status": "ok"}
        
        server.register_handler("test_message", handler)
        assert "test_message" in server.message_handlers
        assert server.message_handlers["test_message"] == handler
    
    def test_validate_message_clean(self):
        """Test message validation with clean data."""
        server = WebSocketServer("test_node")
        
        clean_data = {
            'type': 'test',
            'data': {'value': 42},
            'metadata': {'source': 'sensor_01'}
        }
        
        assert server._validate_message(clean_data) is True
    
    def test_validate_message_forced_consent(self):
        """Test message validation rejects forced consent."""
        server = WebSocketServer("test_node")
        
        malicious_data = {
            'type': 'test',
            'metadata': {'consent_override': 'force'}
        }
        
        assert server._validate_message(malicious_data) is False
    
    def test_validate_message_harmful_markers(self):
        """Test message validation rejects harmful markers."""
        server = WebSocketServer("test_node")
        
        harmful_messages = [
            {'type': 'test', 'metadata': {'action': 'exploit'}},
            {'type': 'test', 'metadata': {'intent': 'harm'}},
            {'type': 'test', 'metadata': {'mode': 'force'}},
            {'type': 'test', 'metadata': {'type': 'override_consent'}}
        ]
        
        for msg in harmful_messages:
            assert server._validate_message(msg) is False


class TestWebSocketClient:
    """Test suite for WebSocketClient."""
    
    def test_initialization(self):
        """Test client initialization."""
        client = WebSocketClient("test_client", "ws://localhost:8765")
        assert client.node_id == "test_client"
        assert client.target_uri == "ws://localhost:8765"
        assert isinstance(client.message_handlers, dict)
        assert client.connected is False
    
    def test_register_handler(self):
        """Test registering message handlers."""
        client = WebSocketClient("test_client")
        
        async def handler(data):
            pass
        
        client.register_handler("test_message", handler)
        assert "test_message" in client.message_handlers
        assert client.message_handlers["test_message"] == handler
    
    @pytest.mark.asyncio
    async def test_handle_message_json(self):
        """Test handling JSON messages."""
        client = WebSocketClient("test_client")
        
        received_data = None
        
        async def handler(data):
            nonlocal received_data
            received_data = data
        
        client.register_handler("test_type", handler)
        
        message = json.dumps({
            'type': 'test_type',
            'data': {'value': 42}
        })
        
        await client._handle_message(message)
        
        assert received_data is not None
        assert received_data['type'] == 'test_type'
        assert received_data['data']['value'] == 42
    
    @pytest.mark.asyncio
    async def test_handle_message_error(self):
        """Test handling error messages."""
        client = WebSocketClient("test_client")
        
        error_message = json.dumps({
            'type': 'error',
            'message': 'Test error'
        })
        
        # Should not raise exception
        await client._handle_message(error_message)
    
    @pytest.mark.asyncio
    async def test_handle_message_connected(self):
        """Test handling connected messages."""
        client = WebSocketClient("test_client")
        
        connected_message = json.dumps({
            'type': 'connected',
            'node_id': 'server_node',
            'timestamp': int(time.time() * 1000)
        })
        
        # Should not raise exception
        await client._handle_message(connected_message)


@pytest.mark.asyncio
async def test_websocket_message_format():
    """Test WebSocket message format creation."""
    client = WebSocketClient("test_client")
    
    # Simulate creating a message (without actual connection)
    message = {
        'type': 'test_message',
        'source_node': client.node_id,
        'data': {'value': 42},
        'metadata': {'sensor': 'bio_01'},
        'timestamp': int(time.time() * 1000)
    }
    
    assert message['type'] == 'test_message'
    assert message['source_node'] == 'test_client'
    assert message['data']['value'] == 42
    assert 'timestamp' in message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
