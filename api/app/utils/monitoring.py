from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request, Response
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'sib_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'sib_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_SESSIONS = Gauge(
    'sib_active_sessions',
    'Number of active chat sessions'
)

LLM_TOKENS = Counter(
    'sib_llm_tokens_total',
    'Total LLM tokens used',
    ['model']
)

RAG_QUERIES = Counter(
    'sib_rag_queries_total',
    'Total RAG queries processed',
    ['status']
)

RESPONSE_TIME_HISTOGRAM = Histogram(
    'sib_response_time_seconds',
    'Response time distribution',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

def setup_metrics():
    """Initialize metrics"""
    logger.info("Metrics initialized")

def track_metrics(operation_name: str):
    """Decorator to track operation metrics"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                REQUEST_COUNT.labels(
                    method='POST',
                    endpoint=operation_name,
                    status='success'
                ).inc()
                return result
                
            except Exception as e:
                REQUEST_COUNT.labels(
                    method='POST',
                    endpoint=operation_name,
                    status='error'
                ).inc()
                raise
                
            finally:
                duration = time.time() - start_time
                REQUEST_DURATION.labels(
                    method='POST',
                    endpoint=operation_name
                ).observe(duration)
                
                RESPONSE_TIME_HISTOGRAM.observe(duration)
        
        return wrapper
    return decorator

async def metrics_middleware(request: Request, call_next):
    """Middleware to track HTTP metrics"""
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    return response

def get_metrics() -> str:
    """Get Prometheus metrics"""
    return generate_latest()
