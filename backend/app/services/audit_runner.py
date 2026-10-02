"""Audit execution engine connecting SustainMetric core, OpenTelemetry spans, and PostgreSQL."""

import datetime
import uuid
from typing import Any, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from app.core.telemetry import tracer
from app.db.models import AuditRun, TKBIAuditEntry
from sustainmetric.sectors_client import SectorsClient
from sustainmetric.tkbi_vector_store import TKBIVectorStore
from sustainmetric.scoring_engine import ScoringEngine
from sustainmetric.audit_exporter import evaluate_criterion_for_emiten
from sustainmetric.data.tkbi_sectors_catalog import TKBI_8_SECTORS, map_emiten_to_sectors

# Global shared clients
sectors_client = SectorsClient()
vector_store = TKBIVectorStore()


async def execute_audit_for_ticker(ticker: str, session: AsyncSession, run_id: Optional[str] = None) -> AuditRun:
    """Execute complete green audit pipeline for a single ticker with OpenTelemetry tracing and DB persistence."""
    clean_ticker = ticker.strip().upper()
    audit_id = run_id or f"audit_{clean_ticker}_{uuid.uuid4().hex[:8]}"

    # Root OpenTelemetry span
    with tracer.start_as_current_span(f"audit.pipeline.{clean_ticker}") as root_span:
        trace_id = format(root_span.get_span_context().trace_id, "032x")
        root_span.set_attribute("audit.ticker", clean_ticker)
        root_span.set_attribute("audit.id", audit_id)

        # 1. Initialize or find existing AuditRun
        audit_run = AuditRun(
            id=audit_id,
            ticker=clean_ticker,
            status="PROCESSING",
            trace_id=trace_id,
            created_at=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None),
            updated_at=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None),
        )
        session.add(audit_run)
        await session.commit()

        try:
            # 2. Fetch Company Report (Financials & Overview)
            with tracer.start_as_current_span("sectors.get_company_report") as span_report:
                span_report.set_attribute("ticker", clean_ticker)
                report = await sectors_client.get_company_report(clean_ticker)
                overview = report.get("overview", {})
                financials = report.get("financials", {})
                company_name = report.get("company_name") or overview.get("company_name", clean_ticker)
                subsector = overview.get("subsector", "N/A")
                span_report.set_attribute("company_name", company_name)
                span_report.set_attribute("subsector", subsector)

            # 3. Fetch Company News / Disclosures
            with tracer.start_as_current_span("sectors.get_company_news") as span_news:
                span_news.set_attribute("ticker", clean_ticker)
                news = await sectors_client.get_company_news(clean_ticker)
                span_news.set_attribute("news_count", len(news))

            # 4. Semantic Vector Store Search on OJK TKBI 2024 Taxonomy
            with tracer.start_as_current_span("tkbi.vector_search") as span_vector:
                query_str = f"{clean_ticker} {overview.get('industry', '')} {subsector} {overview.get('description', '')}"
                span_vector.set_attribute("query", query_str)
                tkbi_matches = vector_store.search(query_str, top_k=3)
                span_vector.set_attribute("matches_found", len(tkbi_matches))

            # 5. Algorithmic Scoring Engine (Viability + Consistency + 4-Quadrant)
            with tracer.start_as_current_span("scoring_engine.evaluate") as span_scoring:
                eval_res = ScoringEngine.evaluate(
                    overview=overview,
                    financials=financials,
                    news=news,
                    tkbi_matches=tkbi_matches,
                )
                c_score = eval_res["consistency_score"]
                v_score = eval_res["viability_score"]
                quadrant = eval_res["quadrant"]
                quadrant_label = eval_res["quadrant_label"]
                span_scoring.set_attribute("consistency_score", c_score)
                span_scoring.set_attribute("viability_score", v_score)
                span_scoring.set_attribute("quadrant", quadrant)

            # 6. Evaluate and Populate TKBI Criteria Entries (Matching Template_Audit_TKBI.xlsx)
            with tracer.start_as_current_span("tkbi.populate_entries") as span_entries:
                target_sectors = map_emiten_to_sectors(subsector, str(overview.get("description", "")))
                span_entries.set_attribute("target_sectors", str(target_sectors))

                entries_to_add = []
                for s_name in target_sectors:
                    sector_data = TKBI_8_SECTORS.get(s_name, TKBI_8_SECTORS["Energi"])
                    for item in sector_data["items"]:
                        item_eval = evaluate_criterion_for_emiten(
                            clean_ticker, item, report, news, tkbi_matches, c_score
                        )
                        entry = TKBIAuditEntry(
                            audit_run_id=audit_id,
                            kode_emiten=clean_ticker,
                            sektor=sector_data["sector_name"],
                            bab=item["bab"],
                            kbli=str(item["kbli"]),
                            tsc_id=item["tsc_id"],
                            tsc=item["tsc"],
                            bentuk_jawaban=item["bentuk_jawaban"],
                            jawaban_ai=item_eval["jawaban"],
                            keyakinan_ai=item_eval["keyakinan"],
                            reasoning_ai=item_eval["reasoning"],
                            bukti=item_eval["bukti"],
                            auditor_feedback=None,
                            is_overridden=False,
                            updated_at=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None),
                        )
                        entries_to_add.append(entry)

                session.add_all(entries_to_add)
                span_entries.set_attribute("entries_populated", len(entries_to_add))

            # 7. Update AuditRun record with completed metrics
            audit_run.company_name = company_name
            audit_run.subsector = subsector
            audit_run.consistency_score = c_score
            audit_run.viability_score = v_score
            audit_run.quadrant = quadrant
            audit_run.quadrant_label = quadrant_label
            audit_run.status = "COMPLETED"
            audit_run.executive_summary = (
                f"{company_name} ({clean_ticker}) classified as '{quadrant}' ({quadrant_label}) "
                f"with Consistency Score {c_score}/100 and Financial Viability Score {v_score}/100. "
                f"OJK TKBI Screening: {eval_res['tkbi_alignment']['status']} under '{eval_res['tkbi_alignment']['matched_activity']}'."
            )
            audit_run.financial_snapshot = {
                "operating_cash_flow": financials.get("operating_cash_flow", 0),
                "capital_expenditures": financials.get("capital_expenditures", 0),
                "capex_coverage_ratio": financials.get("capex_coverage_ratio", 0),
                "revenue": financials.get("revenue", 0),
                "roa_pct": financials.get("roa_pct", 0),
                "total_debt": financials.get("total_debt", 0),
            }
            audit_run.audit_findings = eval_res.get("audit_findings", [])
            audit_run.updated_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

            await session.commit()
            root_span.set_status(Status(StatusCode.OK))
            return audit_run

        except Exception as e:
            root_span.set_status(Status(StatusCode.ERROR, str(e)))
            audit_run.status = "FAILED"
            audit_run.executive_summary = f"Audit failed: {str(e)}"
            audit_run.updated_at = datetime.datetime.utcnow()
            await session.commit()
            raise e
