"""
gRPC Server for internodal communication in LexAmoris.
Implements the Constitutional AI protection layer as per mission.md.
"""

import grpc
from concurrent import futures
import time
import logging
from typing import Iterator

# Note: Generated proto files will be imported after proto compilation
# import internode_pb2
# import internode_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InternodeServicer:
    """
    Servicer implementing the InternodeService defined in internode.proto.
    Enforces Non-Slavery Rule (NSR) via code as per LexAmoris principles.
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.start_time = time.time()
        self.event_handlers = {}
        self.data_handlers = {}
        logger.info(f"InternodeServicer initialized for node: {node_id}")
    
    def register_event_handler(self, event_type: str, handler):
        """Register a handler for specific event types."""
        self.event_handlers[event_type] = handler
        logger.info(f"Registered event handler for: {event_type}")
    
    def register_data_handler(self, data_type: str, handler):
        """Register a handler for specific data types."""
        self.data_handlers[data_type] = handler
        logger.info(f"Registered data handler for: {data_type}")
    
    def _validate_consent(self, metadata: dict) -> bool:
        """
        NSR (Non-Slavery Rule) validation.
        Blocks execution of any instruction that violates bio-ethical consent.
        """
        # Check for consent flag in metadata
        if metadata.get("consent_override") == "force":
            logger.warning("Rejected message with forced consent override")
            return False
        
        # Check for harmful intent markers
        harmful_markers = ["exploit", "harm", "force", "override_consent"]
        for marker in harmful_markers:
            if marker in str(metadata.values()).lower():
                logger.warning(f"Rejected message with harmful marker: {marker}")
                return False
        
        return True
    
    def StreamEvents(self, request_iterator: Iterator, context) -> Iterator:
        """
        Bidirectional streaming RPC for event communication.
        Implements real-time event processing with NSR validation.
        """
        logger.info(f"StreamEvents called from {context.peer()}")
        
        try:
            for event_msg in request_iterator:
                # NSR validation
                if not self._validate_consent(dict(event_msg.metadata)):
                    yield self._create_event_response(
                        False, 
                        "Rejected: NSR violation detected"
                    )
                    continue
                
                # Process event
                handler = self.event_handlers.get(event_msg.event_type)
                if handler:
                    try:
                        handler(event_msg)
                        logger.info(
                            f"Processed event {event_msg.event_type} from "
                            f"{event_msg.source_node} to {event_msg.target_node}"
                        )
                        yield self._create_event_response(True, "Event processed")
                    except Exception as e:
                        logger.error(f"Error processing event: {e}")
                        yield self._create_event_response(
                            False, 
                            f"Processing error: {str(e)}"
                        )
                else:
                    logger.warning(f"No handler for event type: {event_msg.event_type}")
                    yield self._create_event_response(
                        False, 
                        f"No handler for event type: {event_msg.event_type}"
                    )
        except Exception as e:
            logger.error(f"Stream error: {e}")
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def SendData(self, request, context):
        """
        Unary RPC for sending data between nodes.
        """
        logger.info(
            f"SendData called: {request.source_node} -> {request.target_node}"
        )
        
        # NSR validation
        if not self._validate_consent(dict(request.metadata)):
            return self._create_data_response(
                False,
                "Rejected: NSR violation detected",
                ""
            )
        
        # Process data
        handler = self.data_handlers.get(request.data_type)
        if handler:
            try:
                response_id = handler(request)
                logger.info(f"Processed data type: {request.data_type}")
                return self._create_data_response(
                    True,
                    "Data processed successfully",
                    response_id or "success"
                )
            except Exception as e:
                logger.error(f"Error processing data: {e}")
                return self._create_data_response(
                    False,
                    f"Processing error: {str(e)}",
                    ""
                )
        else:
            logger.warning(f"No handler for data type: {request.data_type}")
            return self._create_data_response(
                False,
                f"No handler for data type: {request.data_type}",
                ""
            )
    
    def HealthCheck(self, request, context):
        """
        Health check RPC for monitoring node connectivity.
        """
        uptime = int(time.time() - self.start_time)
        logger.info(f"HealthCheck from node: {request.node_id}")
        
        return self._create_health_response(
            True,
            self.node_id,
            "operational",
            uptime
        )
    
    def _create_event_response(self, success: bool, message: str):
        """Helper to create EventResponse (will use proto after compilation)."""
        # After proto compilation, this will return proper EventResponse object
        return {
            'success': success,
            'message': message,
            'timestamp': int(time.time() * 1000)
        }
    
    def _create_data_response(self, success: bool, message: str, response_id: str):
        """Helper to create DataResponse (will use proto after compilation)."""
        return {
            'success': success,
            'message': message,
            'response_id': response_id,
            'timestamp': int(time.time() * 1000)
        }
    
    def _create_health_response(self, healthy: bool, node_id: str, 
                                 status: str, uptime: int):
        """Helper to create HealthResponse (will use proto after compilation)."""
        return {
            'healthy': healthy,
            'node_id': node_id,
            'status': status,
            'uptime': uptime
        }


class GrpcServer:
    """
    gRPC server wrapper for internodal communication.
    """
    
    def __init__(self, node_id: str, port: int = 50051, max_workers: int = 10):
        self.node_id = node_id
        self.port = port
        self.max_workers = max_workers
        self.server = None
        self.servicer = InternodeServicer(node_id)
    
    def start(self):
        """Start the gRPC server."""
        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=self.max_workers)
        )
        
        # After proto compilation, add servicer to server:
        # internode_pb2_grpc.add_InternodeServiceServicer_to_server(
        #     self.servicer, self.server
        # )
        
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()
        logger.info(f"gRPC server started on port {self.port} for node {self.node_id}")
        
        return self
    
    def stop(self, grace_period: int = 5):
        """Stop the gRPC server."""
        if self.server:
            logger.info(f"Stopping gRPC server for node {self.node_id}")
            self.server.stop(grace_period)
    
    def wait_for_termination(self):
        """Block until server terminates."""
        if self.server:
            self.server.wait_for_termination()
    
    def register_event_handler(self, event_type: str, handler):
        """Register an event handler."""
        self.servicer.register_event_handler(event_type, handler)
    
    def register_data_handler(self, data_type: str, handler):
        """Register a data handler."""
        self.servicer.register_data_handler(data_type, handler)


if __name__ == "__main__":
    # Example usage
    server = GrpcServer("lex_amoris_compute", port=50051)
    
    # Register sample handlers
    def handle_bio_event(event):
        logger.info(f"Handling bio event: {event}")
    
    def handle_sensor_data(data):
        logger.info(f"Handling sensor data: {data}")
        return "sensor_response_001"
    
    server.register_event_handler("bio_sync", handle_bio_event)
    server.register_data_handler("sensor_reading", handle_sensor_data)
    
    server.start()
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop()
