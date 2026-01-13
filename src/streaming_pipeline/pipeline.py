"""
Streaming Pipeline for LexAmoris internodal data flow.
Implements the lex_amoris_compute -> bio_synth_ai_control pipeline.
"""

import asyncio
import logging
import time
from typing import Dict, Callable, List, Optional
from dataclasses import dataclass, field
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventType(Enum):
    """Event types for internodal communication."""
    BIO_SYNC = "bio_sync"
    SENSOR_READING = "sensor_reading"
    MYCELIUM_STATUS = "mycelium_status"
    CLIMATE_CONTROL = "climate_control"
    HEALTH_CHECK = "health_check"
    ERROR = "error"


class DataType(Enum):
    """Data types for internodal communication."""
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    CO2_LEVEL = "co2_level"
    MYCELIUM_GROWTH = "mycelium_growth"
    FREQUENCY_SYNC = "frequency_sync"


@dataclass
class StreamEvent:
    """Event object for streaming pipeline."""
    source_node: str
    target_node: str
    event_type: EventType
    data: Dict
    timestamp: int = field(default_factory=lambda: int(time.time() * 1000))
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'source_node': self.source_node,
            'target_node': self.target_node,
            'event_type': self.event_type.value,
            'data': self.data,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }


@dataclass
class StreamData:
    """Data object for streaming pipeline."""
    source_node: str
    target_node: str
    data_type: DataType
    value: any
    timestamp: int = field(default_factory=lambda: int(time.time() * 1000))
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'source_node': self.source_node,
            'target_node': self.target_node,
            'data_type': self.data_type.value,
            'value': self.value,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }


class StreamPipeline:
    """
    Pipeline for streaming data between nodes.
    Implements the Constitutional AI protection layer.
    """
    
    def __init__(self, source_node: str, target_node: str):
        self.source_node = source_node
        self.target_node = target_node
        self.event_handlers: Dict[EventType, List[Callable]] = {}
        self.data_handlers: Dict[DataType, List[Callable]] = {}
        self.filters: List[Callable] = []
        self.transformers: List[Callable] = []
        self.is_running = False
        logger.info(
            f"StreamPipeline created: {source_node} -> {target_node}"
        )
    
    def add_event_handler(self, event_type: EventType, handler: Callable):
        """Add a handler for specific event type."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        logger.info(f"Added handler for event type: {event_type.value}")
    
    def add_data_handler(self, data_type: DataType, handler: Callable):
        """Add a handler for specific data type."""
        if data_type not in self.data_handlers:
            self.data_handlers[data_type] = []
        self.data_handlers[data_type].append(handler)
        logger.info(f"Added handler for data type: {data_type.value}")
    
    def add_filter(self, filter_func: Callable):
        """Add a filter function to the pipeline."""
        self.filters.append(filter_func)
        logger.info("Added filter to pipeline")
    
    def add_transformer(self, transformer_func: Callable):
        """Add a transformer function to the pipeline."""
        self.transformers.append(transformer_func)
        logger.info("Added transformer to pipeline")
    
    async def process_event(self, event: StreamEvent):
        """
        Process an event through the pipeline.
        Applies NSR validation, filters, and transformers.
        """
        # NSR validation
        if not self._validate_nsr(event.metadata):
            logger.warning(f"Event rejected by NSR: {event.event_type.value}")
            return
        
        # Apply filters
        for filter_func in self.filters:
            if not await self._async_safe_call(filter_func, event):
                logger.info(f"Event filtered out: {event.event_type.value}")
                return
        
        # Apply transformers
        transformed_event = event
        for transformer in self.transformers:
            transformed_event = await self._async_safe_call(
                transformer, transformed_event
            )
        
        # Route to handlers
        handlers = self.event_handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                await self._async_safe_call(handler, transformed_event)
            except Exception as e:
                logger.error(
                    f"Error in event handler for {event.event_type.value}: {e}"
                )
    
    async def process_data(self, data: StreamData):
        """
        Process data through the pipeline.
        Applies NSR validation, filters, and transformers.
        """
        # NSR validation
        if not self._validate_nsr(data.metadata):
            logger.warning(f"Data rejected by NSR: {data.data_type.value}")
            return
        
        # Apply filters
        for filter_func in self.filters:
            if not await self._async_safe_call(filter_func, data):
                logger.info(f"Data filtered out: {data.data_type.value}")
                return
        
        # Apply transformers
        transformed_data = data
        for transformer in self.transformers:
            transformed_data = await self._async_safe_call(
                transformer, transformed_data
            )
        
        # Route to handlers
        handlers = self.data_handlers.get(data.data_type, [])
        for handler in handlers:
            try:
                await self._async_safe_call(handler, transformed_data)
            except Exception as e:
                logger.error(
                    f"Error in data handler for {data.data_type.value}: {e}"
                )
    
    def _validate_nsr(self, metadata: dict) -> bool:
        """
        NSR (Non-Slavery Rule) validation.
        Constitutional AI protection against harmful instructions.
        """
        # Check for consent override
        if metadata.get("consent_override") == "force":
            logger.warning("Rejected: forced consent override")
            return False
        
        # Check for harmful intent markers
        harmful_markers = ["exploit", "harm", "force", "override_consent"]
        for marker in harmful_markers:
            if marker in str(metadata.values()).lower():
                logger.warning(f"Rejected: harmful marker detected: {marker}")
                return False
        
        return True
    
    async def _async_safe_call(self, func: Callable, *args):
        """Safely call a function, handling both sync and async."""
        if asyncio.iscoroutinefunction(func):
            return await func(*args)
        else:
            return func(*args)
    
    async def start(self):
        """Start the pipeline."""
        self.is_running = True
        logger.info(f"Pipeline started: {self.source_node} -> {self.target_node}")
    
    async def stop(self):
        """Stop the pipeline."""
        self.is_running = False
        logger.info(f"Pipeline stopped: {self.source_node} -> {self.target_node}")


class LexAmorisComputePipeline(StreamPipeline):
    """
    Specialized pipeline for lex_amoris_compute -> bio_synth_ai_control.
    Implements the 0.0043 Hz synchronization frequency.
    """
    
    SYNC_FREQUENCY = 0.0043  # Hz - Ultra-low frequency for bio-synchronization
    
    def __init__(self):
        super().__init__("lex_amoris_compute", "bio_synth_ai_control")
        self._setup_default_handlers()
    
    def _setup_default_handlers(self):
        """Setup default handlers for the pipeline."""
        
        # Bio-sync event handler
        async def handle_bio_sync(event: StreamEvent):
            logger.info(
                f"Bio-sync event: frequency={event.data.get('frequency')}, "
                f"phase={event.data.get('phase')}"
            )
            # In real implementation, this would trigger mycelium synchronization
        
        # Sensor reading handler
        async def handle_sensor_reading(event: StreamEvent):
            logger.info(f"Sensor reading: {event.data}")
            # In real implementation, this would process sensor data
        
        # Mycelium status handler
        async def handle_mycelium_status(event: StreamEvent):
            logger.info(f"Mycelium status: {event.data}")
            # In real implementation, this would update mycelium state
        
        # Temperature data handler
        async def handle_temperature(data: StreamData):
            logger.info(f"Temperature reading: {data.value}°C")
            # In real implementation, this would control climate
        
        # Humidity data handler
        async def handle_humidity(data: StreamData):
            logger.info(f"Humidity reading: {data.value}%")
            # In real implementation, this would control climate
        
        # Mycelium growth data handler
        async def handle_mycelium_growth(data: StreamData):
            logger.info(f"Mycelium growth rate: {data.value}")
            # In real implementation, this would optimize growth conditions
        
        # Register handlers
        self.add_event_handler(EventType.BIO_SYNC, handle_bio_sync)
        self.add_event_handler(EventType.SENSOR_READING, handle_sensor_reading)
        self.add_event_handler(EventType.MYCELIUM_STATUS, handle_mycelium_status)
        
        self.add_data_handler(DataType.TEMPERATURE, handle_temperature)
        self.add_data_handler(DataType.HUMIDITY, handle_humidity)
        self.add_data_handler(DataType.MYCELIUM_GROWTH, handle_mycelium_growth)
        
        # Add frequency synchronization filter
        def sync_frequency_filter(item):
            """Filter to ensure synchronization at 0.0043 Hz."""
            # In real implementation, this would check timing
            return True
        
        self.add_filter(sync_frequency_filter)


async def example_usage():
    """Example usage of the streaming pipeline."""
    
    # Create pipeline
    pipeline = LexAmorisComputePipeline()
    await pipeline.start()
    
    # Create and process bio-sync event
    bio_sync_event = StreamEvent(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        event_type=EventType.BIO_SYNC,
        data={
            'frequency': 0.0043,
            'phase': 'synchronizing',
            'mycelium_nodes': ['node_01', 'node_02', 'node_03']
        }
    )
    await pipeline.process_event(bio_sync_event)
    
    # Create and process sensor reading event
    sensor_event = StreamEvent(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        event_type=EventType.SENSOR_READING,
        data={
            'sensor_id': 'bio_sensor_01',
            'readings': {
                'temperature': 22.5,
                'humidity': 65,
                'co2': 400
            }
        }
    )
    await pipeline.process_event(sensor_event)
    
    # Create and process temperature data
    temp_data = StreamData(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        data_type=DataType.TEMPERATURE,
        value=22.5
    )
    await pipeline.process_data(temp_data)
    
    # Create and process mycelium growth data
    growth_data = StreamData(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        data_type=DataType.MYCELIUM_GROWTH,
        value=0.0043,
        metadata={'unit': 'Hz', 'resonance': 'optimal'}
    )
    await pipeline.process_data(growth_data)
    
    await pipeline.stop()


if __name__ == "__main__":
    asyncio.run(example_usage())
