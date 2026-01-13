"""
gRPC Client for internodal communication in LexAmoris.
"""

import grpc
import time
import logging
from typing import Iterator, Callable, Optional

# Note: Generated proto files will be imported after proto compilation
# import internode_pb2
# import internode_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GrpcClient:
    """
    gRPC client for connecting to other nodes in the LexAmoris network.
    """
    
    def __init__(self, node_id: str, target_host: str = 'localhost', 
                 target_port: int = 50051):
        self.node_id = node_id
        self.target_host = target_host
        self.target_port = target_port
        self.channel = None
        self.stub = None
        logger.info(
            f"GrpcClient initialized for node {node_id} "
            f"targeting {target_host}:{target_port}"
        )
    
    def connect(self):
        """Establish connection to target node."""
        self.channel = grpc.insecure_channel(
            f'{self.target_host}:{self.target_port}'
        )
        
        # After proto compilation:
        # self.stub = internode_pb2_grpc.InternodeServiceStub(self.channel)
        
        logger.info(f"Connected to {self.target_host}:{self.target_port}")
        return self
    
    def disconnect(self):
        """Close the connection."""
        if self.channel:
            self.channel.close()
            logger.info(f"Disconnected from {self.target_host}:{self.target_port}")
    
    def stream_events(self, event_generator: Iterator, 
                      response_callback: Optional[Callable] = None):
        """
        Send streaming events to the target node.
        
        Args:
            event_generator: Iterator yielding event messages
            response_callback: Optional callback for processing responses
        """
        try:
            logger.info("Starting event stream")
            
            # After proto compilation, use:
            # responses = self.stub.StreamEvents(event_generator)
            
            # Simulated for now
            responses = self._simulate_stream_events(event_generator)
            
            for response in responses:
                logger.info(
                    f"Received response: success={response.get('success')}, "
                    f"message={response.get('message')}"
                )
                if response_callback:
                    response_callback(response)
                    
        except grpc.RpcError as e:
            logger.error(f"RPC error during event streaming: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during event streaming: {e}")
            raise
    
    def send_data(self, target_node: str, data_type: str, data: bytes, 
                  metadata: dict = None) -> dict:
        """
        Send data to target node.
        
        Args:
            target_node: ID of the target node
            data_type: Type of data being sent
            data: Binary data payload
            metadata: Optional metadata dictionary
            
        Returns:
            Response dictionary from the server
        """
        try:
            # After proto compilation, create DataMessage:
            # message = internode_pb2.DataMessage(
            #     source_node=self.node_id,
            #     target_node=target_node,
            #     data_type=data_type,
            #     data=data,
            #     timestamp=int(time.time() * 1000),
            #     metadata=metadata or {}
            # )
            # response = self.stub.SendData(message)
            
            # Simulated for now
            message = {
                'source_node': self.node_id,
                'target_node': target_node,
                'data_type': data_type,
                'data': data,
                'timestamp': int(time.time() * 1000),
                'metadata': metadata or {}
            }
            
            response = self._simulate_send_data(message)
            
            logger.info(
                f"Data sent to {target_node}: type={data_type}, "
                f"success={response.get('success')}"
            )
            
            return response
            
        except grpc.RpcError as e:
            logger.error(f"RPC error during data send: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during data send: {e}")
            raise
    
    def health_check(self) -> dict:
        """
        Perform health check on target node.
        
        Returns:
            Health status dictionary
        """
        try:
            # After proto compilation:
            # request = internode_pb2.HealthRequest(node_id=self.node_id)
            # response = self.stub.HealthCheck(request)
            
            # Simulated for now
            response = self._simulate_health_check()
            
            logger.info(
                f"Health check: healthy={response.get('healthy')}, "
                f"status={response.get('status')}"
            )
            
            return response
            
        except grpc.RpcError as e:
            logger.error(f"RPC error during health check: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during health check: {e}")
            raise
    
    def _simulate_stream_events(self, event_generator: Iterator):
        """Simulate streaming events (until proto is compiled)."""
        for event in event_generator:
            yield {
                'success': True,
                'message': 'Event received (simulated)',
                'timestamp': int(time.time() * 1000)
            }
    
    def _simulate_send_data(self, message: dict):
        """Simulate sending data (until proto is compiled)."""
        return {
            'success': True,
            'message': 'Data received (simulated)',
            'response_id': f"resp_{int(time.time())}",
            'timestamp': int(time.time() * 1000)
        }
    
    def _simulate_health_check(self):
        """Simulate health check (until proto is compiled)."""
        return {
            'healthy': True,
            'node_id': 'target_node',
            'status': 'operational',
            'uptime': 3600
        }


def create_event_message(source_node: str, target_node: str, 
                        event_type: str, payload: bytes, 
                        metadata: dict = None) -> dict:
    """
    Helper function to create event messages.
    
    Args:
        source_node: Source node ID
        target_node: Target node ID
        event_type: Type of event
        payload: Binary payload
        metadata: Optional metadata
        
    Returns:
        Event message dictionary (will be EventMessage proto after compilation)
    """
    return {
        'source_node': source_node,
        'target_node': target_node,
        'event_type': event_type,
        'payload': payload,
        'timestamp': int(time.time() * 1000),
        'metadata': metadata or {}
    }


if __name__ == "__main__":
    # Example usage
    client = GrpcClient("bio_synth_ai_control", "localhost", 50051)
    client.connect()
    
    try:
        # Health check
        health = client.health_check()
        logger.info(f"Health check result: {health}")
        
        # Send data
        response = client.send_data(
            target_node="lex_amoris_compute",
            data_type="sensor_reading",
            data=b"temperature:22.5C,humidity:65%",
            metadata={"sensor_id": "bio_sensor_01", "location": "mycelium_wall"}
        )
        logger.info(f"Send data result: {response}")
        
    finally:
        client.disconnect()
