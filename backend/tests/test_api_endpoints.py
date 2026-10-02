"""End-to-end API integration tests for Phase 2 endpoints."""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_and_audit_endpoints():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Health check
        res = await client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "HEALTHY"

        # 2. Trigger audit for ADRO
        trigger_res = await client.post("/api/v1/audits/trigger", json={"tickers": ["ADRO"]})
        assert trigger_res.status_code == 200
        runs = trigger_res.json()["runs"]
        assert len(runs) == 1
        audit_id = runs[0]["id"]
        assert runs[0]["ticker"] == "ADRO"

        # 3. Retrieve audit detail
        detail_res = await client.get(f"/api/v1/audits/{audit_id}")
        assert detail_res.status_code == 200
        detail = detail_res.json()
        assert detail["status"] == "COMPLETED"
        assert "consistency_score" in detail

        # 4. Retrieve TKBI entries
        tkbi_res = await client.get(f"/api/v1/audits/{audit_id}/tkbi")
        assert tkbi_res.status_code == 200
        entries = tkbi_res.json()
        assert len(entries) > 0
        first_entry_id = entries[0]["id"]

        # 5. HITL Patch: update feedback and override
        patch_res = await client.patch(
            f"/api/v1/audits/{audit_id}/tkbi/{first_entry_id}",
            json={"auditor_feedback": "Auditor checked coal phaseout plan", "auditor_override": "TRANSISI"}
        )
        assert patch_res.status_code == 200

        # Verify entry updated
        tkbi_res_updated = await client.get(f"/api/v1/audits/{audit_id}/tkbi")
        updated_first = next(e for e in tkbi_res_updated.json() if e["id"] == first_entry_id)
        assert updated_first["auditor_override"] == "TRANSISI"
        assert updated_first["is_overridden"] is True

        # 6. Retrieve OpenTelemetry traces
        traces_res = await client.get(f"/api/v1/audits/{audit_id}/traces")
        assert traces_res.status_code == 200
        traces = traces_res.json()
        assert len(traces) >= 4

        # 7. Test Stamped Excel export
        xlsx_res = await client.get(f"/api/v1/audits/{audit_id}/export/xlsx")
        assert xlsx_res.status_code == 200
        assert len(xlsx_res.content) > 1000  # Valid binary Excel file

        # 8. Test Signed PDF export
        pdf_res = await client.get(f"/api/v1/audits/{audit_id}/export/pdf")
        assert pdf_res.status_code == 200
        assert pdf_res.content.startswith(b"%PDF")

        # 9. Test Benchmarks
        bench_res = await client.get("/api/v1/benchmarks")
        assert bench_res.status_code == 200
        assert bench_res.json()["count"] >= 1

        # 10. Test Schedules CRUD
        sched_create = await client.post(
            "/api/v1/schedules",
            json={"name": "Weekly Energy Audit", "cron_expression": "0 8 * * 1", "tickers": ["PGEO", "ADRO"]}
        )
        assert sched_create.status_code == 200
        sched_id = sched_create.json()["schedule_id"]

        sched_list = await client.get("/api/v1/schedules")
        assert sched_list.status_code == 200
        assert any(s["id"] == sched_id for s in sched_list.json())

        # 11. Test Chat Endpoint streaming
        chat_res = await client.post(
            "/api/v1/chat",
            json={"messages": [{"role": "user", "content": "Tell me about ADRO green audit"}]}
        )
        assert chat_res.status_code == 200
        assert "event: delta" in chat_res.text
