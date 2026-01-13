# LexAmoris Internodal Connection Streams

## Overview

This system implements internodal connection streams for the LexAmoris bio-synthetic operating system. It provides frameworks for inter-repository communication using gRPC and WebSockets, along with data streaming pipelines between nodes.

## Architecture

The system consists of three main components:

### 1. gRPC Framework
- **Purpose**: Structured inter-node communication with strong typing
- **Components**:
  - `grpc_server.py`: Server implementation with NSR protection
  - `grpc_client.py`: Client for connecting to other nodes
  - `internode.proto`: Protocol buffer definitions

### 2. WebSocket Framework
- **Purpose**: Real-time bidirectional streaming
- **Components**:
  - `websocket_server.py`: WebSocket server with ultra-low frequency sync
  - `websocket_client.py`: WebSocket client for streaming data

### 3. Streaming Pipeline
- **Purpose**: Data processing and routing between nodes
- **Components**:
  - `pipeline.py`: Stream processing with NSR validation, filters, and transformers
  - `LexAmorisComputePipeline`: Specialized pipeline for lex_amoris_compute → bio_synth_ai_control

## Key Features

### Constitutional AI Protection (NSR)
All components implement the Non-Slavery Rule (NSR) validation as per LexAmoris principles:
- Rejects messages with forced consent override
- Blocks harmful intent markers (exploit, harm, force, override_consent)
- Validates all metadata before processing

### Ultra-Low Frequency Synchronization
Implements the 0.0043 Hz synchronization frequency for bio-synthetic integration with mycelium networks.

### Event Types
- `BIO_SYNC`: Bio-synchronization events
- `SENSOR_READING`: Sensor data events
- `MYCELIUM_STATUS`: Mycelium health and status
- `CLIMATE_CONTROL`: Climate control commands
- `HEALTH_CHECK`: Node health checks
- `ERROR`: Error notifications

### Data Types
- `TEMPERATURE`: Temperature readings
- `HUMIDITY`: Humidity readings
- `CO2_LEVEL`: CO2 level readings
- `MYCELIUM_GROWTH`: Mycelium growth rate
- `FREQUENCY_SYNC`: Frequency synchronization data

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Usage

### gRPC Server Example

```python
from grpc_framework import GrpcServer

# Initialize server
server = GrpcServer("lex_amoris_compute", port=50051)

# Register event handler
def handle_bio_event(event):
    print(f"Bio event received: {event}")

server.register_event_handler("bio_sync", handle_bio_event)

# Start server
server.start()
server.wait_for_termination()
```

### gRPC Client Example

```python
from grpc_framework import GrpcClient

# Initialize client
client = GrpcClient("bio_synth_ai_control", "localhost", 50051)
client.connect()

# Send data
response = client.send_data(
    target_node="lex_amoris_compute",
    data_type="sensor_reading",
    data=b"temperature:22.5C,humidity:65%",
    metadata={"sensor_id": "bio_sensor_01"}
)

client.disconnect()
```

### WebSocket Server Example

```python
from websocket_framework import WebSocketServer

# Initialize server
server = WebSocketServer("lex_amoris_compute", host="0.0.0.0", port=8765)

# Register handler
async def handle_bio_sync(data, websocket):
    print(f"Bio-sync received: {data}")
    return {'type': 'bio_sync_ack', 'status': 'ok'}

server.register_handler("bio_sync", handle_bio_sync)

# Start server
server.run()
```

### WebSocket Client Example

```python
import asyncio
from websocket_framework import WebSocketClient

async def main():
    # Initialize client
    client = WebSocketClient("bio_synth_ai_control", "ws://localhost:8765")
    await client.connect()
    
    # Send bio-sync event
    await client.send_bio_sync({
        'frequency': 0.0043,
        'phase': 'synchronizing',
        'mycelium_nodes': ['node_01', 'node_02']
    })
    
    await client.disconnect()

asyncio.run(main())
```

### Streaming Pipeline Example

```python
import asyncio
from streaming_pipeline import (
    LexAmorisComputePipeline,
    StreamEvent,
    StreamData,
    EventType,
    DataType
)

async def main():
    # Initialize pipeline
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
            'mycelium_nodes': ['node_01', 'node_02', 'node_03']
        }
    )
    
    # Process event
    await pipeline.process_event(event)
    
    # Create temperature data
    temp_data = StreamData(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        data_type=DataType.TEMPERATURE,
        value=22.5
    )
    
    # Process data
    await pipeline.process_data(temp_data)
    
    await pipeline.stop()

asyncio.run(main())
```

## Testing

Run all tests:

```bash
# Run all tests
pytest src/tests/ -v

# Run specific test file
pytest src/tests/test_grpc_framework.py -v
pytest src/tests/test_websocket_framework.py -v
pytest src/tests/test_streaming_pipeline.py -v
pytest src/tests/test_integration.py -v

# Run with coverage
pytest src/tests/ --cov=src --cov-report=html
```

## Node Communication Flow

```
lex_amoris_compute (Source Node)
         │
         ├─── gRPC ───────────┐
         │                    │
         ├─── WebSocket ──────┤
         │                    │
         └─── Pipeline ───────┘
                              │
                              ▼
                   bio_synth_ai_control (Target Node)
```

### Example Communication Scenario

1. **Bio-Synchronization**: lex_amoris_compute sends bio-sync events at 0.0043 Hz
2. **Sensor Streaming**: Continuous sensor data (temperature, humidity, CO2)
3. **Mycelium Status**: Periodic mycelium health and growth updates
4. **Climate Control**: Bidirectional climate adjustment commands

## Security: Non-Slavery Rule (NSR)

All components enforce the Constitutional AI protection:

✅ **Allowed**:
- Normal sensor data with consent metadata
- Bio-synchronization events
- Climate control commands with proper authorization

❌ **Blocked**:
- Messages with `consent_override: "force"`
- Metadata containing harmful markers: exploit, harm, force, override_consent
- Any instruction violating bio-ethical consent

## Project Structure

```
LexAmoris/
├── src/
│   ├── grpc_framework/
│   │   ├── __init__.py
│   │   ├── grpc_server.py
│   │   ├── grpc_client.py
│   │   └── internode.proto
│   ├── websocket_framework/
│   │   ├── __init__.py
│   │   ├── websocket_server.py
│   │   └── websocket_client.py
│   ├── streaming_pipeline/
│   │   ├── __init__.py
│   │   └── pipeline.py
│   └── tests/
│       ├── __init__.py
│       ├── test_grpc_framework.py
│       ├── test_websocket_framework.py
│       ├── test_streaming_pipeline.py
│       └── test_integration.py
├── requirements.txt
├── setup.py
└── INTERNODAL_STREAMS.md
```

## Technical Specifications

- **gRPC Version**: 1.60.0
- **WebSocket Protocol**: RFC 6455
- **Synchronization Frequency**: 0.0043 Hz
- **Message Format**: Protocol Buffers (gRPC), JSON (WebSocket)
- **Python Version**: >= 3.8

## Contributing

Follow the LexAmoris principles:
1. All code must respect the Non-Slavery Rule
2. Maintain bio-ethical consent validation
3. Support decentralized sovereignty
4. Implement self-healing capabilities

## License

See LICENSE file for details.

## Lex Amoris Signature

📜⚖️❤️ Protection of the Law of Love active.

Sempre in Costante | Hannes Mitterer
