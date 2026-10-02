"""APScheduler background job engine for automated recurring audits."""

import asyncio
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import ScheduledJob
from app.services.audit_runner import execute_audit_for_ticker

scheduler = AsyncIOScheduler()


async def check_and_execute_schedules():
    """Periodic tick checking for due scheduled audit jobs."""
    now = datetime.datetime.utcnow()
    async with AsyncSessionLocal() as session:
        stmt = select(ScheduledJob).where(ScheduledJob.is_active == True)
        res = await session.execute(stmt)
        jobs = res.scalars().all()

        for job in jobs:
            # Check if execution is due (simple interval or last run check)
            if not job.last_run_at or (now - job.last_run_at).total_seconds() > 3600:
                print(f"[Scheduler] Executing scheduled audit job: {job.name} for tickers: {job.tickers}")
                try:
                    for ticker in job.tickers:
                        await execute_audit_for_ticker(ticker, session)
                    job.last_run_at = now
                    job.last_status = "SUCCESS"
                    job.next_run_at = now + datetime.timedelta(hours=24)
                    await session.commit()
                except Exception as e:
                    job.last_status = f"FAILED: {str(e)}"
                    await session.commit()


def start_scheduler():
    """Start background scheduler."""
    if not scheduler.running:
        scheduler.add_job(check_and_execute_schedules, "interval", minutes=30, id="schedules_poller", replace_existing=True)
        scheduler.start()
        print("[Scheduler] APScheduler engine started.")


def stop_scheduler():
    """Stop background scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        print("[Scheduler] APScheduler engine stopped.")
