"""
Tests for gRPC framework internodal communication.
"""

import pytest
import time
import asyncio
from unittest.mock import Mock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from grpc_framework.grpc_server import InternodeServicer, GrpcServer
from grpc_framework.grpc_client import GrpcClient, create_event_message


class TestInternodeServicer:
    """Test suite for InternodeServicer."""
    
    def setup_method(self):
        """Setup for each test."""
        self.servicer = InternodeServicer("test_node")
    
    def test_initialization(self):
        """Test servicer initialization."""
        assert self.servicer.node_id == "test_node"
        assert isinstance(self.servicer.event_handlers, dict)
        assert isinstance(self.servicer.data_handlers, dict)
        assert self.servicer.start_time > 0
    
    def test_register_event_handler(self):
        """Test registering event handlers."""
        def handler(event):
            pass
        
        self.servicer.register_event_handler("test_event", handler)
        assert "test_event" in self.servicer.event_handlers
        assert self.servicer.event_handlers["test_event"] == handler
    
    def test_register_data_handler(self):
        """Test registering data handlers."""
        def handler(data):
            return "test_response"
        
        self.servicer.register_data_handler("test_data", handler)
        assert "test_data" in self.servicer.data_handlers
        assert self.servicer.data_handlers["test_data"] == handler
    
    def test_nsr_validation_clean_metadata(self):
        """Test NSR validation with clean metadata."""
        metadata = {"sensor_id": "bio_01", "location": "wall"}
        assert self.servicer._validate_consent(metadata) is True
    
    def test_nsr_validation_forced_consent(self):
        """Test NSR validation rejects forced consent."""
        metadata = {"consent_override": "force"}
        assert self.servicer._validate_consent(metadata) is False
    
    def test_nsr_validation_harmful_markers(self):
        """Test NSR validation rejects harmful markers."""
        harmful_metadata = [
            {"action": "exploit"},
            {"intent": "harm"},
            {"mode": "force"},
            {"type": "override_consent"}
        ]
        
        for metadata in harmful_metadata:
            assert self.servicer._validate_consent(metadata) is False
    
    def test_create_event_response(self):
        """Test creating event responses."""
        response = self.servicer._create_event_response(True, "Success")
        assert response['success'] is True
        assert response['message'] == "Success"
        assert 'timestamp' in response
    
    def test_create_data_response(self):
        """Test creating data responses."""
        response = self.servicer._create_data_response(
            True, "Success", "resp_001"
        )
        assert response['success'] is True
        assert response['message'] == "Success"
        assert response['response_id'] == "resp_001"
        assert 'timestamp' in response
    
    def test_create_health_response(self):
        """Test creating health responses."""
        response = self.servicer._create_health_response(
            True, "test_node", "operational", 3600
        )
        assert response['healthy'] is True
        assert response['node_id'] == "test_node"
        assert response['status'] == "operational"
        assert response['uptime'] == 3600


class TestGrpcServer:
    """Test suite for GrpcServer."""
    
    def test_initialization(self):
        """Test server initialization."""
        server = GrpcServer("test_node", port=50051)
        assert server.node_id == "test_node"
        assert server.port == 50051
        assert server.max_workers == 10
        assert isinstance(server.servicer, InternodeServicer)
    
    def test_register_handlers(self):
        """Test registering handlers through server."""
        server = GrpcServer("test_node")
        
        def event_handler(event):
            pass
        
        def data_handler(data):
            return "response"
        
        server.register_event_handler("test_event", event_handler)
        server.register_data_handler("test_data", data_handler)
        
        assert "test_event" in server.servicer.event_handlers
        assert "test_data" in server.servicer.data_handlers


class TestGrpcClient:
    """Test suite for GrpcClient."""
    
    def test_initialization(self):
        """Test client initialization."""
        client = GrpcClient("test_client", "localhost", 50051)
        assert client.node_id == "test_client"
        assert client.target_host == "localhost"
        assert client.target_port == 50051
    
    def test_simulate_send_data(self):
        """Test simulated data sending."""
        client = GrpcClient("test_client")
        
        message = {
            'source_node': 'test_client',
            'target_node': 'test_server',
            'data_type': 'test',
            'data': b'test_data',
            'timestamp': int(time.time() * 1000),
            'metadata': {}
        }
        
        response = client._simulate_send_data(message)
        assert response['success'] is True
        assert 'response_id' in response
        assert 'timestamp' in response
    
    def test_simulate_health_check(self):
        """Test simulated health check."""
        client = GrpcClient("test_client")
        response = client._simulate_health_check()
        
        assert response['healthy'] is True
        assert 'node_id' in response
        assert response['status'] == 'operational'
        assert 'uptime' in response


class TestEventMessage:
    """Test suite for event message creation."""
    
    def test_create_event_message(self):
        """Test creating event messages."""
        event = create_event_message(
            source_node="node_a",
            target_node="node_b",
            event_type="test_event",
            payload=b"test_payload",
            metadata={"test": "meta"}
        )
        
        assert event['source_node'] == "node_a"
        assert event['target_node'] == "node_b"
        assert event['event_type'] == "test_event"
        assert event['payload'] == b"test_payload"
        assert event['metadata'] == {"test": "meta"}
        assert 'timestamp' in event
    
    def test_create_event_message_default_metadata(self):
        """Test creating event messages with default metadata."""
        event = create_event_message(
            source_node="node_a",
            target_node="node_b",
            event_type="test_event",
            payload=b"test_payload"
        )
        
        assert event['metadata'] == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
