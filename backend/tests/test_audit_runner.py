"""Integration test for audit runner, OpenTelemetry tracing, and PostgreSQL persistence."""

import pytest
import pytest_asyncio
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import AuditRun, TKBIAuditEntry, AuditTraceSpan
from app.services.audit_runner import execute_audit_for_ticker


@pytest.mark.asyncio
async def test_audit_runner_pgeo():
    async with AsyncSessionLocal() as session:
        audit_run = await execute_audit_for_ticker("PGEO", session)
        assert audit_run.status == "COMPLETED"
        assert audit_run.ticker == "PGEO"
        assert audit_run.consistency_score > 0
        assert audit_run.viability_score > 0
        assert audit_run.trace_id is not None

        # Verify TKBI entries in PostgreSQL
        entries_stmt = select(TKBIAuditEntry).where(TKBIAuditEntry.audit_run_id == audit_run.id)
        entries_res = await session.execute(entries_stmt)
        entries = entries_res.scalars().all()
        assert len(entries) > 0
        print(f"Generated {len(entries)} TKBI criteria rows for PGEO")

        # Verify OpenTelemetry trace spans in PostgreSQL
        traces_stmt = select(AuditTraceSpan).where(AuditTraceSpan.trace_id == audit_run.trace_id)
        traces_res = await session.execute(traces_stmt)
        spans = traces_res.scalars().all()
        print(f"Recorded {len(spans)} OpenTelemetry spans for trace {audit_run.trace_id}")
        assert len(spans) >= 4
