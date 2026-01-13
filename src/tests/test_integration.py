"""
Integration tests for internodal connection streams.
Tests the complete flow: gRPC + WebSocket + Pipeline
"""

import pytest
import asyncio
import time

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from grpc_framework.grpc_server import GrpcServer
from grpc_framework.grpc_client import GrpcClient
from websocket_framework.websocket_server import WebSocketServer
from websocket_framework.websocket_client import WebSocketClient
from streaming_pipeline.pipeline import (
    LexAmorisComputePipeline,
    StreamEvent,
    StreamData,
    EventType,
    DataType,
)


@pytest.mark.asyncio
async def test_pipeline_event_flow():
    """Test complete event flow through pipeline."""
    pipeline = LexAmorisComputePipeline()
    await pipeline.start()
    
    # Create bio-sync event
    event = StreamEvent(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        event_type=EventType.BIO_SYNC,
        data={
            'frequency': 0.0043,
            'phase': 'synchronizing',
            'mycelium_nodes': ['node_01', 'node_02']
        }
    )
    
    # Process event
    await pipeline.process_event(event)
    
    # Create sensor reading event
    sensor_event = StreamEvent(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        event_type=EventType.SENSOR_READING,
        data={
            'sensor_id': 'bio_sensor_01',
            'temperature': 22.5,
            'humidity': 65,
            'co2': 400
        }
    )
    
    await pipeline.process_event(sensor_event)
    
    await pipeline.stop()
    assert pipeline.is_running is False


@pytest.mark.asyncio
async def test_pipeline_data_flow():
    """Test complete data flow through pipeline."""
    pipeline = LexAmorisComputePipeline()
    await pipeline.start()
    
    # Create temperature data
    temp_data = StreamData(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        data_type=DataType.TEMPERATURE,
        value=22.5,
        metadata={'sensor': 'bio_01', 'location': 'mycelium_wall'}
    )
    
    await pipeline.process_data(temp_data)
    
    # Create humidity data
    humidity_data = StreamData(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        data_type=DataType.HUMIDITY,
        value=65,
        metadata={'sensor': 'bio_01', 'location': 'mycelium_wall'}
    )
    
    await pipeline.process_data(humidity_data)
    
    # Create mycelium growth data
    growth_data = StreamData(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        data_type=DataType.MYCELIUM_GROWTH,
        value=0.0043,
        metadata={'unit': 'Hz', 'resonance': 'optimal'}
    )
    
    await pipeline.process_data(growth_data)
    
    await pipeline.stop()


def test_grpc_server_initialization():
    """Test gRPC server can be initialized."""
    server = GrpcServer("lex_amoris_compute", port=50052)
    
    # Register handlers
    def bio_event_handler(event):
        pass
    
    def sensor_data_handler(data):
        return "response_001"
    
    server.register_event_handler("bio_sync", bio_event_handler)
    server.register_data_handler("sensor_reading", sensor_data_handler)
    
    assert "bio_sync" in server.servicer.event_handlers
    assert "sensor_reading" in server.servicer.data_handlers


def test_grpc_client_initialization():
    """Test gRPC client can be initialized."""
    client = GrpcClient("bio_synth_ai_control", "localhost", 50052)
    
    assert client.node_id == "bio_synth_ai_control"
    assert client.target_host == "localhost"
    assert client.target_port == 50052


def test_websocket_server_initialization():
    """Test WebSocket server can be initialized."""
    server = WebSocketServer("lex_amoris_compute", "localhost", 8766)
    
    # Register handlers
    async def bio_sync_handler(data, websocket):
        return {"status": "ok"}
    
    server.register_handler("bio_sync", bio_sync_handler)
    
    assert "bio_sync" in server.message_handlers


def test_websocket_client_initialization():
    """Test WebSocket client can be initialized."""
    client = WebSocketClient("bio_synth_ai_control", "ws://localhost:8766")
    
    assert client.node_id == "bio_synth_ai_control"
    assert client.target_uri == "ws://localhost:8766"


@pytest.mark.asyncio
async def test_nsr_protection_across_systems():
    """Test NSR (Non-Slavery Rule) protection across all systems."""
    
    # Test pipeline NSR
    pipeline = LexAmorisComputePipeline()
    
    malicious_event = StreamEvent(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        event_type=EventType.BIO_SYNC,
        data={'test': 'data'},
        metadata={'consent_override': 'force'}  # Should be rejected
    )
    
    handled = []
    
    async def capture_handler(event):
        handled.append(event)
    
    pipeline.add_event_handler(EventType.BIO_SYNC, capture_handler)
    
    await pipeline.process_event(malicious_event)
    
    # Event should be blocked by NSR
    assert len(handled) == 0
    
    # Test WebSocket server NSR
    ws_server = WebSocketServer("test_node")
    
    malicious_ws_message = {
        'type': 'bio_sync',
        'metadata': {'action': 'exploit'}  # Should be rejected
    }
    
    assert ws_server._validate_message(malicious_ws_message) is False
    
    # Test gRPC server NSR
    grpc_server = GrpcServer("test_node")
    
    malicious_metadata = {'intent': 'harm'}  # Should be rejected
    assert grpc_server.servicer._validate_consent(malicious_metadata) is False


@pytest.mark.asyncio
async def test_complete_node_communication_scenario():
    """Test a complete communication scenario between nodes."""
    
    # Initialize pipeline
    pipeline = LexAmorisComputePipeline()
    await pipeline.start()
    
    # Simulate lex_amoris_compute sending data to bio_synth_ai_control
    
    # 1. Send bio-synchronization event
    bio_sync = StreamEvent(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        event_type=EventType.BIO_SYNC,
        data={
            'frequency': 0.0043,
            'phase': 'synchronizing',
            'mycelium_nodes': ['node_01', 'node_02', 'node_03']
        },
        metadata={'priority': 'high', 'retry': False}
    )
    
    await pipeline.process_event(bio_sync)
    
    # 2. Stream sensor readings
    for i in range(3):
        sensor_event = StreamEvent(
            source_node="lex_amoris_compute",
            target_node="bio_synth_ai_control",
            event_type=EventType.SENSOR_READING,
            data={
                'sensor_id': f'bio_sensor_{i:02d}',
                'temperature': 22.0 + i * 0.5,
                'humidity': 65 + i,
                'co2': 400 + i * 10
            },
            metadata={'location': f'wall_section_{i}'}
        )
        
        await pipeline.process_event(sensor_event)
    
    # 3. Send climate control data
    climate_data = [
        StreamData(
            source_node="lex_amoris_compute",
            target_node="bio_synth_ai_control",
            data_type=DataType.TEMPERATURE,
            value=22.5,
            metadata={'target': 'optimal'}
        ),
        StreamData(
            source_node="lex_amoris_compute",
            target_node="bio_synth_ai_control",
            data_type=DataType.HUMIDITY,
            value=65,
            metadata={'target': 'optimal'}
        ),
        StreamData(
            source_node="lex_amoris_compute",
            target_node="bio_synth_ai_control",
            data_type=DataType.MYCELIUM_GROWTH,
            value=0.0043,
            metadata={'unit': 'Hz', 'resonance': 'optimal'}
        )
    ]
    
    for data in climate_data:
        await pipeline.process_data(data)
    
    # 4. Send mycelium status event
    mycelium_status = StreamEvent(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        event_type=EventType.MYCELIUM_STATUS,
        data={
            'health': 'optimal',
            'growth_rate': 0.0043,
            'coverage': 95.5
        },
        metadata={'wall_section': 'primary'}
    )
    
    await pipeline.process_event(mycelium_status)
    
    await pipeline.stop()
    
    # Verify pipeline completed
    assert pipeline.is_running is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
