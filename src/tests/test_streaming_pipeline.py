"""
Tests for streaming pipeline internodal data flow.
"""

import pytest
import asyncio
import time

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from streaming_pipeline.pipeline import (
    StreamPipeline,
    LexAmorisComputePipeline,
    StreamEvent,
    StreamData,
    EventType,
    DataType,
)


class TestStreamEvent:
    """Test suite for StreamEvent."""
    
    def test_initialization(self):
        """Test event initialization."""
        event = StreamEvent(
            source_node="node_a",
            target_node="node_b",
            event_type=EventType.BIO_SYNC,
            data={"frequency": 0.0043}
        )
        
        assert event.source_node == "node_a"
        assert event.target_node == "node_b"
        assert event.event_type == EventType.BIO_SYNC
        assert event.data == {"frequency": 0.0043}
        assert event.timestamp > 0
        assert isinstance(event.metadata, dict)
    
    def test_to_dict(self):
        """Test converting event to dictionary."""
        event = StreamEvent(
            source_node="node_a",
            target_node="node_b",
            event_type=EventType.SENSOR_READING,
            data={"temp": 22.5}
        )
        
        event_dict = event.to_dict()
        assert event_dict['source_node'] == "node_a"
        assert event_dict['target_node'] == "node_b"
        assert event_dict['event_type'] == "sensor_reading"
        assert event_dict['data'] == {"temp": 22.5}


class TestStreamData:
    """Test suite for StreamData."""
    
    def test_initialization(self):
        """Test data initialization."""
        data = StreamData(
            source_node="node_a",
            target_node="node_b",
            data_type=DataType.TEMPERATURE,
            value=22.5
        )
        
        assert data.source_node == "node_a"
        assert data.target_node == "node_b"
        assert data.data_type == DataType.TEMPERATURE
        assert data.value == 22.5
        assert data.timestamp > 0
        assert isinstance(data.metadata, dict)
    
    def test_to_dict(self):
        """Test converting data to dictionary."""
        data = StreamData(
            source_node="node_a",
            target_node="node_b",
            data_type=DataType.HUMIDITY,
            value=65
        )
        
        data_dict = data.to_dict()
        assert data_dict['source_node'] == "node_a"
        assert data_dict['target_node'] == "node_b"
        assert data_dict['data_type'] == "humidity"
        assert data_dict['value'] == 65


class TestStreamPipeline:
    """Test suite for StreamPipeline."""
    
    def test_initialization(self):
        """Test pipeline initialization."""
        pipeline = StreamPipeline("source_node", "target_node")
        
        assert pipeline.source_node == "source_node"
        assert pipeline.target_node == "target_node"
        assert isinstance(pipeline.event_handlers, dict)
        assert isinstance(pipeline.data_handlers, dict)
        assert isinstance(pipeline.filters, list)
        assert isinstance(pipeline.transformers, list)
        assert pipeline.is_running is False
    
    def test_add_event_handler(self):
        """Test adding event handlers."""
        pipeline = StreamPipeline("source", "target")
        
        async def handler(event):
            pass
        
        pipeline.add_event_handler(EventType.BIO_SYNC, handler)
        assert EventType.BIO_SYNC in pipeline.event_handlers
        assert handler in pipeline.event_handlers[EventType.BIO_SYNC]
    
    def test_add_data_handler(self):
        """Test adding data handlers."""
        pipeline = StreamPipeline("source", "target")
        
        async def handler(data):
            pass
        
        pipeline.add_data_handler(DataType.TEMPERATURE, handler)
        assert DataType.TEMPERATURE in pipeline.data_handlers
        assert handler in pipeline.data_handlers[DataType.TEMPERATURE]
    
    def test_add_filter(self):
        """Test adding filters."""
        pipeline = StreamPipeline("source", "target")
        
        def filter_func(item):
            return True
        
        pipeline.add_filter(filter_func)
        assert filter_func in pipeline.filters
    
    def test_add_transformer(self):
        """Test adding transformers."""
        pipeline = StreamPipeline("source", "target")
        
        def transformer_func(item):
            return item
        
        pipeline.add_transformer(transformer_func)
        assert transformer_func in pipeline.transformers
    
    def test_nsr_validation_clean(self):
        """Test NSR validation with clean metadata."""
        pipeline = StreamPipeline("source", "target")
        metadata = {"sensor_id": "bio_01"}
        
        assert pipeline._validate_nsr(metadata) is True
    
    def test_nsr_validation_forced_consent(self):
        """Test NSR validation rejects forced consent."""
        pipeline = StreamPipeline("source", "target")
        metadata = {"consent_override": "force"}
        
        assert pipeline._validate_nsr(metadata) is False
    
    def test_nsr_validation_harmful_markers(self):
        """Test NSR validation rejects harmful markers."""
        pipeline = StreamPipeline("source", "target")
        
        harmful_metadata = [
            {"action": "exploit"},
            {"intent": "harm"},
            {"mode": "force"},
            {"type": "override_consent"}
        ]
        
        for metadata in harmful_metadata:
            assert pipeline._validate_nsr(metadata) is False
    
    @pytest.mark.asyncio
    async def test_start_stop(self):
        """Test starting and stopping pipeline."""
        pipeline = StreamPipeline("source", "target")
        
        await pipeline.start()
        assert pipeline.is_running is True
        
        await pipeline.stop()
        assert pipeline.is_running is False
    
    @pytest.mark.asyncio
    async def test_process_event(self):
        """Test processing events through pipeline."""
        pipeline = StreamPipeline("source", "target")
        
        handled = []
        
        async def handler(event):
            handled.append(event)
        
        pipeline.add_event_handler(EventType.BIO_SYNC, handler)
        
        event = StreamEvent(
            source_node="source",
            target_node="target",
            event_type=EventType.BIO_SYNC,
            data={"test": "data"}
        )
        
        await pipeline.process_event(event)
        
        assert len(handled) == 1
        assert handled[0].data == {"test": "data"}
    
    @pytest.mark.asyncio
    async def test_process_data(self):
        """Test processing data through pipeline."""
        pipeline = StreamPipeline("source", "target")
        
        handled = []
        
        async def handler(data):
            handled.append(data)
        
        pipeline.add_data_handler(DataType.TEMPERATURE, handler)
        
        data = StreamData(
            source_node="source",
            target_node="target",
            data_type=DataType.TEMPERATURE,
            value=22.5
        )
        
        await pipeline.process_data(data)
        
        assert len(handled) == 1
        assert handled[0].value == 22.5
    
    @pytest.mark.asyncio
    async def test_filter_blocks_event(self):
        """Test that filters can block events."""
        pipeline = StreamPipeline("source", "target")
        
        handled = []
        
        async def handler(event):
            handled.append(event)
        
        def filter_func(item):
            return False  # Block everything
        
        pipeline.add_event_handler(EventType.BIO_SYNC, handler)
        pipeline.add_filter(filter_func)
        
        event = StreamEvent(
            source_node="source",
            target_node="target",
            event_type=EventType.BIO_SYNC,
            data={"test": "data"}
        )
        
        await pipeline.process_event(event)
        
        assert len(handled) == 0  # Event was filtered out
    
    @pytest.mark.asyncio
    async def test_transformer_modifies_event(self):
        """Test that transformers can modify events."""
        pipeline = StreamPipeline("source", "target")
        
        handled = []
        
        async def handler(event):
            handled.append(event)
        
        def transformer_func(event):
            event.data['transformed'] = True
            return event
        
        pipeline.add_event_handler(EventType.BIO_SYNC, handler)
        pipeline.add_transformer(transformer_func)
        
        event = StreamEvent(
            source_node="source",
            target_node="target",
            event_type=EventType.BIO_SYNC,
            data={"test": "data"}
        )
        
        await pipeline.process_event(event)
        
        assert len(handled) == 1
        assert handled[0].data['transformed'] is True


class TestLexAmorisComputePipeline:
    """Test suite for LexAmorisComputePipeline."""
    
    def test_initialization(self):
        """Test specialized pipeline initialization."""
        pipeline = LexAmorisComputePipeline()
        
        assert pipeline.source_node == "lex_amoris_compute"
        assert pipeline.target_node == "bio_synth_ai_control"
        assert pipeline.SYNC_FREQUENCY == 0.0043
        
        # Check default handlers are registered
        assert EventType.BIO_SYNC in pipeline.event_handlers
        assert EventType.SENSOR_READING in pipeline.event_handlers
        assert EventType.MYCELIUM_STATUS in pipeline.event_handlers
        assert DataType.TEMPERATURE in pipeline.data_handlers
        assert DataType.HUMIDITY in pipeline.data_handlers
        assert DataType.MYCELIUM_GROWTH in pipeline.data_handlers
    
    @pytest.mark.asyncio
    async def test_process_bio_sync_event(self):
        """Test processing bio-sync event."""
        pipeline = LexAmorisComputePipeline()
        
        event = StreamEvent(
            source_node="lex_amoris_compute",
            target_node="bio_synth_ai_control",
            event_type=EventType.BIO_SYNC,
            data={
                'frequency': 0.0043,
                'phase': 'synchronizing'
            }
        )
        
        # Should not raise exception
        await pipeline.process_event(event)
    
    @pytest.mark.asyncio
    async def test_process_sensor_reading(self):
        """Test processing sensor reading event."""
        pipeline = LexAmorisComputePipeline()
        
        event = StreamEvent(
            source_node="lex_amoris_compute",
            target_node="bio_synth_ai_control",
            event_type=EventType.SENSOR_READING,
            data={
                'sensor_id': 'bio_sensor_01',
                'temperature': 22.5,
                'humidity': 65
            }
        )
        
        # Should not raise exception
        await pipeline.process_event(event)
    
    @pytest.mark.asyncio
    async def test_process_temperature_data(self):
        """Test processing temperature data."""
        pipeline = LexAmorisComputePipeline()
        
        data = StreamData(
            source_node="lex_amoris_compute",
            target_node="bio_synth_ai_control",
            data_type=DataType.TEMPERATURE,
            value=22.5
        )
        
        # Should not raise exception
        await pipeline.process_data(data)
    
    @pytest.mark.asyncio
    async def test_process_mycelium_growth_data(self):
        """Test processing mycelium growth data."""
        pipeline = LexAmorisComputePipeline()
        
        data = StreamData(
            source_node="lex_amoris_compute",
            target_node="bio_synth_ai_control",
            data_type=DataType.MYCELIUM_GROWTH,
            value=0.0043,
            metadata={'unit': 'Hz'}
        )
        
        # Should not raise exception
        await pipeline.process_data(data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
