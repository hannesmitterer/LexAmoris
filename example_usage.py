"""
Example script demonstrating internodal connection streams.
Shows a complete communication flow between lex_amoris_compute and bio_synth_ai_control.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from streaming_pipeline import (
    LexAmorisComputePipeline,
    StreamEvent,
    StreamData,
    EventType,
    DataType
)


async def demonstrate_internodal_streams():
    """Demonstrate the complete internodal streaming system."""
    
    print("=" * 70)
    print("LexAmoris Internodal Connection Streams - Demonstration")
    print("=" * 70)
    print()
    
    # Initialize pipeline
    print("🔗 Initializing pipeline: lex_amoris_compute → bio_synth_ai_control")
    pipeline = LexAmorisComputePipeline()
    await pipeline.start()
    print(f"✓ Pipeline started with sync frequency: {pipeline.SYNC_FREQUENCY} Hz")
    print()
    
    # 1. Bio-synchronization
    print("📡 Step 1: Bio-Synchronization")
    print("-" * 70)
    bio_sync_event = StreamEvent(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        event_type=EventType.BIO_SYNC,
        data={
            'frequency': 0.0043,
            'phase': 'synchronizing',
            'mycelium_nodes': ['node_01', 'node_02', 'node_03']
        },
        metadata={'priority': 'high', 'resonance': 'optimal'}
    )
    
    await pipeline.process_event(bio_sync_event)
    print(f"✓ Bio-sync event processed at {bio_sync_event.data['frequency']} Hz")
    print()
    
    # 2. Sensor readings streaming
    print("🌡️  Step 2: Streaming Sensor Readings")
    print("-" * 70)
    for i in range(3):
        sensor_event = StreamEvent(
            source_node="lex_amoris_compute",
            target_node="bio_synth_ai_control",
            event_type=EventType.SENSOR_READING,
            data={
                'sensor_id': f'bio_sensor_{i:02d}',
                'temperature': 22.0 + i * 0.5,
                'humidity': 65 + i,
                'co2': 400 + i * 10,
                'mycelium_growth_rate': 0.0043
            },
            metadata={'location': f'mycelium_wall_section_{i}'}
        )
        
        await pipeline.process_event(sensor_event)
        print(f"  ✓ Sensor {i:02d}: T={sensor_event.data['temperature']}°C, "
              f"H={sensor_event.data['humidity']}%, CO2={sensor_event.data['co2']}ppm")
        await asyncio.sleep(0.1)  # Simulate real-time streaming
    print()
    
    # 3. Climate control data
    print("🌿 Step 3: Climate Control Data Stream")
    print("-" * 70)
    
    # Temperature
    temp_data = StreamData(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        data_type=DataType.TEMPERATURE,
        value=22.5,
        metadata={'target': 'optimal', 'unit': 'celsius'}
    )
    await pipeline.process_data(temp_data)
    print(f"  ✓ Temperature: {temp_data.value}°C")
    
    # Humidity
    humidity_data = StreamData(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        data_type=DataType.HUMIDITY,
        value=65,
        metadata={'target': 'optimal', 'unit': 'percent'}
    )
    await pipeline.process_data(humidity_data)
    print(f"  ✓ Humidity: {humidity_data.value}%")
    
    # CO2
    co2_data = StreamData(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        data_type=DataType.CO2_LEVEL,
        value=400,
        metadata={'target': 'optimal', 'unit': 'ppm'}
    )
    await pipeline.process_data(co2_data)
    print(f"  ✓ CO2 Level: {co2_data.value}ppm")
    print()
    
    # 4. Mycelium status
    print("🍄 Step 4: Mycelium Status Update")
    print("-" * 70)
    mycelium_status = StreamEvent(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        event_type=EventType.MYCELIUM_STATUS,
        data={
            'health': 'optimal',
            'growth_rate': 0.0043,
            'coverage_percent': 95.5,
            'air_filtration_active': True,
            'heat_regulation_active': True
        },
        metadata={'wall_section': 'primary', 'evaluation': 'auto'}
    )
    
    await pipeline.process_event(mycelium_status)
    print(f"  ✓ Health: {mycelium_status.data['health']}")
    print(f"  ✓ Growth Rate: {mycelium_status.data['growth_rate']} Hz")
    print(f"  ✓ Coverage: {mycelium_status.data['coverage_percent']}%")
    print(f"  ✓ Air Filtration: {'Active' if mycelium_status.data['air_filtration_active'] else 'Inactive'}")
    print(f"  ✓ Heat Regulation: {'Active' if mycelium_status.data['heat_regulation_active'] else 'Inactive'}")
    print()
    
    # 5. Mycelium growth data
    print("📊 Step 5: Mycelium Growth Analytics")
    print("-" * 70)
    growth_data = StreamData(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        data_type=DataType.MYCELIUM_GROWTH,
        value=0.0043,
        metadata={
            'unit': 'Hz',
            'resonance': 'optimal',
            'sync_with_nodes': True,
            'bio_feedback_loop': 'active'
        }
    )
    
    await pipeline.process_data(growth_data)
    print(f"  ✓ Growth Rate: {growth_data.value} Hz (Ultra-low frequency resonance)")
    print(f"  ✓ Resonance: {growth_data.metadata['resonance']}")
    print(f"  ✓ Bio-feedback Loop: {growth_data.metadata['bio_feedback_loop']}")
    print()
    
    # 6. Demonstrate NSR protection
    print("🛡️  Step 6: NSR (Non-Slavery Rule) Protection Demonstration")
    print("-" * 70)
    
    malicious_event = StreamEvent(
        source_node="lex_amoris_compute",
        target_node="bio_synth_ai_control",
        event_type=EventType.BIO_SYNC,
        data={'test': 'malicious'},
        metadata={'consent_override': 'force'}  # This will be blocked
    )
    
    processed_count = 0
    
    async def count_handler(event):
        nonlocal processed_count
        processed_count += 1
    
    pipeline.add_event_handler(EventType.BIO_SYNC, count_handler)
    
    await pipeline.process_event(malicious_event)
    
    if processed_count == 0:
        print("  ✓ Malicious event BLOCKED by NSR validation")
        print("  ✓ Constitutional AI protection active")
    else:
        print("  ✗ WARNING: NSR validation failed!")
    print()
    
    # Stop pipeline
    print("⏹️  Stopping pipeline")
    print("-" * 70)
    await pipeline.stop()
    print("✓ Pipeline stopped successfully")
    print()
    
    print("=" * 70)
    print("✅ Demonstration Complete")
    print("=" * 70)
    print()
    print("Lex Amoris Signature: 📜⚖️❤️")
    print("Protection of the Law of Love active.")
    print("Sempre in Costante | Hannes Mitterer")
    print()


if __name__ == "__main__":
    asyncio.run(demonstrate_internodal_streams())
