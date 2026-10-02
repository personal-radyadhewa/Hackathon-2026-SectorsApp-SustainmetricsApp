"""Database auto-seeder pre-populating flagship IDX tickers on initial startup."""

import asyncio
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import AuditRun, ScheduledJob
from app.services.audit_runner import execute_audit_for_ticker

DEFAULT_TICKERS = ["PGEO", "ADRO", "BBRI", "BREN", "BUMI"]


async def seed_initial_demo_data():
    """Seed flagship IDX emitents and an initial cron schedule if database is unpopulated."""
    async with AsyncSessionLocal() as session:
        # Check existing audit runs
        stmt = select(AuditRun.ticker).distinct()
        res = await session.execute(stmt)
        existing_tickers = set(res.scalars().all())

        missing = [t for t in DEFAULT_TICKERS if t not in existing_tickers]
        if missing:
            print(f"[Seeder] Pre-populating demo audit data for: {missing}")
            for ticker in missing:
                try:
                    await execute_audit_for_ticker(ticker, session)
                    print(f"[Seeder] Successfully audited and seeded {ticker}")
                except Exception as e:
                    print(f"[Seeder] Failed to seed {ticker}: {e}")

        # Check existing schedules
        sched_stmt = select(ScheduledJob)
        sched_res = await session.execute(sched_stmt)
        schedules = sched_res.scalars().all()

        if len(schedules) == 0:
            demo_job = ScheduledJob(
                id="cron_demo_energy",
                name="Weekly IDX Energy Green Audit",
                cron_expression="0 8 * * 1",
                tickers=["PGEO", "ADRO", "BREN"],
                is_active=True,
                alert_threshold_score=50.0,
            )
            session.add(demo_job)
            await session.commit()
            print("[Seeder] Created default recurring schedule: 'Weekly IDX Energy Green Audit'")
