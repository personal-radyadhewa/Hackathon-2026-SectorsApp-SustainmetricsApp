"""SQLAlchemy models for SustainMetric audit persistence."""

import datetime
from typing import Any
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class AuditRun(Base):
    """Represents a full audit execution session for an IDX ticker."""
    __tablename__ = "audit_runs"

    id = Column(String(64), primary_key=True, index=True)
    ticker = Column(String(16), nullable=False, index=True)
    company_name = Column(String(255), nullable=True)
    subsector = Column(String(128), nullable=True)
    consistency_score = Column(Float, nullable=False, default=0.0)
    viability_score = Column(Float, nullable=False, default=0.0)
    quadrant = Column(String(64), nullable=True)
    quadrant_label = Column(String(128), nullable=True)
    status = Column(String(32), nullable=False, default="QUEUED", index=True)
    executive_summary = Column(Text, nullable=True)
    financial_snapshot = Column(JSON, nullable=True, default=dict)
    audit_findings = Column(JSON, nullable=True, default=list)
    trace_id = Column(String(64), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    # Relationships
    tkbi_entries = relationship("TKBIAuditEntry", back_populates="audit_run", cascade="all, delete-orphan")


class TKBIAuditEntry(Base):
    """Represents a single row matching Template_Audit_TKBI.xlsx schema."""
    __tablename__ = "tkbi_audit_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    audit_run_id = Column(String(64), ForeignKey("audit_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    kode_emiten = Column(String(16), nullable=False, index=True)
    sektor = Column(String(128), nullable=False)
    bab = Column(String(255), nullable=False)
    kbli = Column(String(64), nullable=False)
    tsc_id = Column(String(64), nullable=False, index=True)
    tsc = Column(String(255), nullable=False)
    bentuk_jawaban = Column(String(64), nullable=False)
    jawaban_ai = Column(String(32), nullable=False)
    keyakinan_ai = Column(String(32), nullable=False)
    reasoning_ai = Column(Text, nullable=True)
    bukti = Column(Text, nullable=True)
    
    # Human-in-the-loop (HITL) overrides
    auditor_feedback = Column(Text, nullable=True)
    auditor_override = Column(String(32), nullable=True)
    is_overridden = Column(Boolean, default=False, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    audit_run = relationship("AuditRun", back_populates="tkbi_entries")


class AuditTraceSpan(Base):
    """Captures granular OpenTelemetry trace spans for the DAG visualization."""
    __tablename__ = "audit_traces"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String(64), nullable=False, index=True)
    span_id = Column(String(64), nullable=False, index=True)
    parent_span_id = Column(String(64), nullable=True)
    name = Column(String(128), nullable=False)
    service_name = Column(String(64), nullable=False, default="sustainmetric")
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_ms = Column(Float, nullable=False)
    status = Column(String(16), nullable=False, default="OK")
    attributes = Column(JSON, nullable=True, default=dict)


class ScheduledJob(Base):
    """Tracks recurring cron audit schedules."""
    __tablename__ = "scheduled_jobs"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    cron_expression = Column(String(64), nullable=False)
    tickers = Column(JSON, nullable=False, default=list)
    is_active = Column(Boolean, default=True, nullable=False)
    alert_threshold_score = Column(Float, default=50.0, nullable=False)
    last_run_at = Column(DateTime, nullable=True)
    last_status = Column(String(32), nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
