"""OpenTelemetry Tracer SDK and custom database span exporter for audit trace playback."""

import datetime
import uuid
from typing import Any, Optional
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, SpanProcessor, ReadableSpan
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import Status, StatusCode

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.db.models import AuditTraceSpan

# Setup OpenTelemetry TracerProvider
resource = Resource.create({"service.name": settings.OTEL_SERVICE_NAME})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("sustainmetric")


class DatabaseSpanRecorder(SpanProcessor):
    """Custom OpenTelemetry SpanProcessor that records finished spans to PostgreSQL."""

    def on_start(self, span: Any, parent_context: Optional[Any] = None) -> None:
        pass

    def on_end(self, span: ReadableSpan) -> None:
        """Invoked synchronously by OpenTelemetry when a span finishes."""
        trace_id = format(span.context.trace_id, "032x")
        span_id = format(span.context.span_id, "016x")
        parent_span_id = format(span.parent.span_id, "016x") if span.parent else None
        
        start_time = datetime.datetime.fromtimestamp(span.start_time / 1e9)
        end_time = datetime.datetime.fromtimestamp(span.end_time / 1e9)
        duration_ms = round((span.end_time - span.start_time) / 1e6, 2)
        
        status_name = "OK"
        if span.status.status_code == StatusCode.ERROR:
            status_name = "ERROR"

        # Serialize attributes safely
        clean_attrs = {}
        if span.attributes:
            for k, v in span.attributes.items():
                if isinstance(v, (str, int, float, bool)):
                    clean_attrs[k] = v
                else:
                    clean_attrs[k] = str(v)

        # Store synchronously or fire async task to persist span
        import asyncio
        async def _persist():
            async with AsyncSessionLocal() as session:
                record = AuditTraceSpan(
                    trace_id=trace_id,
                    span_id=span_id,
                    parent_span_id=parent_span_id,
                    name=span.name,
                    service_name=settings.OTEL_SERVICE_NAME,
                    start_time=start_time,
                    end_time=end_time,
                    duration_ms=duration_ms,
                    status=status_name,
                    attributes=clean_attrs,
                )
                session.add(record)
                await session.commit()

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(_persist())
            else:
                loop.run_until_complete(_persist())
        except Exception:
            # Fallback if no loop is running
            pass

    def shutdown(self) -> None:
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


# Register database span recorder
provider.add_span_processor(DatabaseSpanRecorder())


def generate_trace_id() -> str:
    """Generate a valid 32-character hex trace ID."""
    return uuid.uuid4().hex
