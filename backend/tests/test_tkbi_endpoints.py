"""Unit & integration tests for OJK TKBI flow endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_tkbi_taxonomy_explorer():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/tkbi/taxonomy/explorer")
        assert res.status_code == 200
        data = res.json()
        assert "sectors" in data
        assert len(data["sectors"]) == 8
        assert "Energi" in data["sectors"]
        assert "principles" in data
        assert len(data["principles"]["environmental_objectives"]) == 4
        assert len(data["principles"]["essential_criteria"]) == 3
        assert len(data["ndc_targets"]) >= 5


@pytest.mark.asyncio
async def test_tkbi_sdt_catalog():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/tkbi/sdt/catalog")
        assert res.status_code == 200
        data = res.json()
        assert "criteria" in data
        assert "EO1" in data["criteria"]
        assert len(data["dnsh_questions"]) > 0
        assert len(data["social_questions"]) > 0


@pytest.mark.asyncio
async def test_tkbi_simulator_korporasi_scenarios():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Full Green Korporasi
        res = await client.post("/api/v1/tkbi/simulator/evaluate", json={
            "scale_type": "KORPORASI",
            "sector_name": "Energi",
            "eo_primary": "EO1",
            "tsc_status": "HIJAU",
            "dnsh_harm": False,
            "has_rmt": False,
            "social_aspects_met": True,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["classification"] == "HIJAU"
        assert data["dnsh_status"] == "PASS"
        assert data["rmt_clock_years"] == 0

        # 2. Interim Transition with RMT (3-year clock)
        res_interim = await client.post("/api/v1/tkbi/simulator/evaluate", json={
            "scale_type": "KORPORASI",
            "sector_name": "Energi",
            "eo_primary": "EO1",
            "tsc_status": "HIJAU",
            "dnsh_harm": True,
            "has_rmt": True,
            "social_aspects_met": True,
        })
        assert res_interim.status_code == 200
        data_interim = res_interim.json()
        assert data_interim["classification"] == "TRANSISI INTERIM"
        assert data_interim["dnsh_status"] == "RMT_INTERIM"
        assert data_interim["rmt_clock_years"] == 3

        # 3. Failed Social Aspects
        res_social = await client.post("/api/v1/tkbi/simulator/evaluate", json={
            "scale_type": "KORPORASI",
            "sector_name": "Energi",
            "eo_primary": "EO1",
            "tsc_status": "HIJAU",
            "dnsh_harm": False,
            "has_rmt": False,
            "social_aspects_met": False,
        })
        assert res_social.status_code == 200
        assert res_social.json()["classification"] == "TIDAK MEMENUHI KLASIFIKASI"


@pytest.mark.asyncio
async def test_tkbi_simulator_umkm_sdt():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/api/v1/tkbi/simulator/evaluate", json={
            "scale_type": "UMKM",
            "eo_primary": "EO1",
            "eo_answers": {
                "SDT-EO1-Q1": True,
                "SDT-EO1-Q2": True,
                "SDT-EO1-Q3": True,
            },
            "dnsh_answers": {
                "SDT-DNSH-1": True,
                "SDT-DNSH-2": True,
                "SDT-DNSH-3": True,
            },
            "social_answers": {
                "SDT-SA-1": True,
                "SDT-SA-2": True,
            },
            "has_rmt": False,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["classification"] == "HIJAU"
        assert data["scale_type"] == "UMKM"
        assert data["score_pct"] == 100.0


@pytest.mark.asyncio
async def test_tkbi_portfolio_aggregator():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "portfolio_type": "HOLDING_CONSOLIDATED",
            "financing_type": "GENERAL_PURPOSE",
            "items": [
                {"name": "Anak Usaha Geothermal (PGEO)", "amount": 600.0, "classification": "HIJAU"},
                {"name": "Anak Usaha Pembangkit Gas Transisi", "amount": 250.0, "classification": "TRANSISI"},
                {"name": "Anak Usaha Pensiun Dini PLTU (RMT)", "amount": 100.0, "classification": "TRANSISI INTERIM"},
                {"name": "Aktivitas Non-Kepatuhan", "amount": 50.0, "classification": "TIDAK MEMENUHI"},
            ]
        }
        res = await client.post("/api/v1/tkbi/portfolio/evaluate", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["total_exposure"] == 1000.0
        assert data["pct_hijau"] == 60.0
        assert data["pct_transisi"] == 25.0
        assert data["pct_transisi_interim"] == 10.0
        assert data["pct_tidak_memenuhi"] == 5.0
        assert data["weighted_green_transition_ratio"] == 95.0


@pytest.mark.asyncio
async def test_tkbi_grandfathering_scenarios():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/tkbi/grandfathering/scenarios")
        assert res.status_code == 200
        data = res.json()
        assert data["clock_rules"]["unallocated_financing_protection_years"] == 7
        assert len(data["scenarios"]) == 5
