"""Multi-Provider LLM Gateway supporting Gemini, OpenAI, Claude, and Ollama with tool execution."""

import json
from typing import AsyncGenerator, Any, Optional
import httpx
from app.core.config import settings
from sustainmetric.tkbi_vector_store import TKBIVectorStore
from sustainmetric.sectors_client import SectorsClient

vector_store = TKBIVectorStore()
sectors_client = SectorsClient()

AVAILABLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "inspect_ticker_evidence",
            "description": "Inspect the 4-pillar TKBI evidence dossier (TSC, DNSH, MSS, Capital Allocation) for an IDX ticker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "IDX stock ticker, e.g. PGEO, ADRO, BREN"}
                },
                "required": ["ticker"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_tkbi_knowledge_base",
            "description": "Search official OJK TKBI 2024 Taxonomy guidelines, Technical Screening Criteria, and DNSH rules.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query regarding sustainable finance rules or thresholds"}
                },
                "required": ["query"],
            },
        },
    },
]


async def execute_tool_call(tool_name: str, arguments: dict[str, Any]) -> str:
    """Execute local FastMCP tool for LLM agent loops."""
    if tool_name == "inspect_ticker_evidence":
        ticker = arguments.get("ticker", "").strip().upper()
        try:
            from sustainmetric.scoring_engine import ScoringEngine
            rep = await sectors_client.get_company_report(ticker)
            news = await sectors_client.get_company_news(ticker)
            matches = vector_store.search(ticker, top_k=2)
            eval_res = ScoringEngine.evaluate(
                overview=rep.get("overview", {}),
                financials=rep.get("financials", {}),
                news=news,
                tkbi_matches=matches,
            )
            return json.dumps({
                "ticker": ticker,
                "quadrant": eval_res["quadrant"],
                "consistency_score": eval_res["consistency_score"],
                "viability_score": eval_res["viability_score"],
                "audit_findings": eval_res["audit_findings"],
            })
        except Exception as e:
            return json.dumps({"error": str(e)})

    elif tool_name == "query_tkbi_knowledge_base":
        q = arguments.get("query", "")
        results = vector_store.search(q, top_k=3)
        return json.dumps({"results": results})

    return json.dumps({"error": f"Unknown tool: {tool_name}"})


import re
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AuditRun
from sustainmetric.scoring_engine import ScoringEngine


async def get_emiten_audit_context(ticker: str, db: Optional[AsyncSession] = None) -> str:
    """Retrieve saved DB audit result or compute live audit context for system prompt."""
    clean = ticker.strip().upper()
    audit: Optional[AuditRun] = None
    if db:
        try:
            stmt = select(AuditRun).where(AuditRun.ticker == clean).order_by(AuditRun.created_at.desc()).limit(1)
            res = await db.execute(stmt)
            audit = res.scalar_one_or_none()
        except Exception:
            pass

    if audit:
        findings_bullets = "\n".join([f"- {f}" for f in (audit.audit_findings or [])[:6]])
        fin = audit.financial_snapshot or {}
        fin_bullets = ", ".join([f"{k}: {v}" for k, v in list(fin.items())[:5]]) if fin else "Audited regular filings"
        return (
            f"You are the expert SustainMetric AI Green Auditor for Indonesian listed companies.\n"
            f"The user is inspecting Indonesian Stock Exchange company: {audit.company_name or clean} (IDX: {clean}).\n\n"
            f"### Official Audit Results for IDX:{clean}:\n"
            f"- Company Name: {audit.company_name or clean}\n"
            f"- Subsector: {audit.subsector or 'Transportation & Logistics'}\n"
            f"- OJK TKBI Quadrant: {audit.quadrant} ({audit.quadrant_label or ''})\n"
            f"- Consistency Score: {audit.consistency_score}/100\n"
            f"- Viability Score: {audit.viability_score}/100\n"
            f"- Executive Summary: {audit.executive_summary or 'Audit completed.'}\n"
            f"- Key Audit Findings & Disclosures:\n{findings_bullets or '- Disclosures audited against OJK TKBI guidelines.'}\n"
            f"- Financial & ESG Data: {fin_bullets}\n\n"
            f"### Instructions for Response:\n"
            f"1. Interpret any user query about '{clean}' or company performance as referring to this Indonesian public company ({audit.company_name or clean}, IDX: {clean}). NEVER answer with dictionary words, Greek mythology, or unrelated meanings.\n"
            f"2. Explain its real business, its OJK TKBI sustainability/green rating, and its ESG transition viability.\n"
            f"3. Format your response cleanly using Markdown (bold headings, bullet points, structured analysis)."
        )

    # Fallback to SectorsClient & ScoringEngine if not yet in DB
    try:
        rep = await sectors_client.get_company_report(clean)
        overview = rep.get("overview", {})
        financials = rep.get("financials", {})
        news = await sectors_client.get_company_news(clean)
        matches = vector_store.search(clean, top_k=2)
        eval_res = ScoringEngine.evaluate(overview, financials, news, matches)
        comp_name = overview.get("company_name") or clean
        subsector = overview.get("subsector") or overview.get("sector") or "Transportation & Logistics"
        findings_bullets = "\n".join([f"- {f}" for f in eval_res.get("audit_findings", [])[:5]])
        return (
            f"You are the expert SustainMetric AI Green Auditor for Indonesian listed companies.\n"
            f"The user is inspecting Indonesian Stock Exchange company: {comp_name} (IDX: {clean}).\n\n"
            f"### Official Profile & Live Audit for IDX:{clean}:\n"
            f"- Company Name: {comp_name}\n"
            f"- Subsector: {subsector}\n"
            f"- Business Description: {overview.get('description', '')}\n"
            f"- OJK TKBI Quadrant: {eval_res.get('quadrant')}\n"
            f"- Consistency Score: {eval_res.get('consistency_score')}/100\n"
            f"- Viability Score: {eval_res.get('viability_score')}/100\n"
            f"- Key Findings:\n{findings_bullets}\n\n"
            f"### Instructions for Response:\n"
            f"1. Ground your response strictly in the context of this IDX listed company ({comp_name}, IDX: {clean}). NEVER answer with dictionary words or mythology.\n"
            f"2. Detail its core business, its sustainability standing, and transition risks under OJK TKBI.\n"
            f"3. Format your response cleanly using Markdown (bold headings, bullet points, structured analysis)."
        )
    except Exception:
        return (
            f"You are the expert SustainMetric AI Green Auditor for Indonesian listed companies.\n"
            f"The user is inspecting Indonesian Stock Exchange company IDX: {clean}.\n"
            f"Always ground your response in the context of this IDX listed company. Do not interpret '{clean}' as a generic English word or mythological figure. Format using Markdown."
        )


async def stream_chat_completion(
    messages: list[dict[str, str]],
    provider: str = "gemini",
    model: str = "gemini-2.5-flash",
    api_key: str = "",
    ticker: Optional[str] = None,
    db: Optional[AsyncSession] = None,
) -> AsyncGenerator[str, None]:
    """Stream chat responses grounded in Indonesian emiten data with tool-calling support."""
    key = api_key or (
        settings.GEMINI_API_KEY if provider == "gemini"
        else getattr(settings, "OPENROUTER_API_KEY", "") if provider == "openrouter"
        else settings.OPENAI_API_KEY
    )
    last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    
    # 1. Resolve active emiten
    active_ticker = (ticker or "").strip().upper()
    if not active_ticker:
        known_tickers = ["HELI", "PGEO", "ADRO", "BBRI", "BREN", "BUMI", "UVCR", "IDEA", "TLKM", "ASII", "GOTO", "BMRI"]
        for t in known_tickers:
            if re.search(rf"\b{t}\b", last_user_msg, re.IGNORECASE):
                active_ticker = t
                break

    # 2. Build emiten system context prompt
    if active_ticker:
        system_prompt = await get_emiten_audit_context(active_ticker, db)
    else:
        system_prompt = (
            "You are the expert SustainMetric AI Green Auditor for Indonesian listed companies.\n"
            "You assist auditors, asset managers, and banks in assessing OJK TKBI (Taksonomi Keuangan Berkelanjutan Indonesia) "
            "compliance, greenwashing risks, and sustainability transition viability. Format your response cleanly using Markdown."
        )

    # 3. Fallback / Offline intelligent synthesis mode if API key not provided
    if not key and provider != "ollama":
        yield f"event: delta\ndata: {json.dumps({'content': f'*(Operating in Offline Heuristic Mode - No API key provided)*\\n\\nAnalyzing query: \"{last_user_msg}\"...\\n\\n'})}\n\n"
        
        if active_ticker:
            yield f"event: delta\ndata: {json.dumps({'content': f'🔍 **Inspecting TKBI Evidence Dossier for IDX: {active_ticker}**...\\n\\n{system_prompt}\\n\\n*To enable live generative multi-step LLM reasoning, configure your API Key in Settings.*'})}\n\n"
        else:
            search_res = json.loads(await execute_tool_call("query_tkbi_knowledge_base", {"query": last_user_msg}))
            matches = search_res.get("results", [])
            summary = "\\n".join([f"• **{m.get('activity')}** ({m.get('id')}): {m.get('tsc')[:120]}..." for m in matches[:2]])
            resp = (
                f"### OJK TKBI 2024 Taxonomy Query Results:\\n{summary}\\n\\n"
                f"*Provide an IDX ticker (e.g. PGEO, ADRO, HELI, BREN) to execute an automated green audit analysis.*"
            )
            yield f"event: delta\ndata: {json.dumps({'content': resp})}\n\n"

        yield f"event: done\ndata: [DONE]\n\n"
        return

    # 4. OpenAI / Gemini / OpenRouter OpenAI-compatible endpoint
    base_url = (
        "https://generativelanguage.googleapis.com/v1beta/openai/" if provider == "gemini"
        else "https://openrouter.ai/api/v1" if provider == "openrouter"
        else settings.OLLAMA_BASE_URL if provider == "ollama"
        else "https://api.openai.com/v1"
    )

    client_headers = {"Authorization": f"Bearer {key}"} if key else {}
    if provider == "openrouter":
        client_headers["HTTP-Referer"] = "https://sustainmetric.app"
        client_headers["X-Title"] = "SustainMetric IDX Harness"

    # Prepend or inject system prompt into messages payload
    augmented_messages: list[dict[str, str]] = []
    has_system = False
    for m in messages:
        if m.get("role") == "system":
            has_system = True
            augmented_messages.append({"role": "system", "content": f"{system_prompt}\n\n{m.get('content', '')}"})
        else:
            augmented_messages.append(m)
    if not has_system:
        augmented_messages.insert(0, {"role": "system", "content": system_prompt})

    req_payload: dict[str, Any] = {
        "model": model,
        "messages": augmented_messages,
        "stream": True,
    }
    # Free models / OpenRouter / Ollama often reject OpenAI `tools` schema with 400 Bad Request
    if provider in ("openai", "gemini"):
        req_payload["tools"] = AVAILABLE_TOOLS

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", f"{base_url}/chat/completions", headers=client_headers, json=req_payload) as response:
                if response.status_code != 200:
                    err_bytes = await response.aread()
                    err_raw = err_bytes.decode("utf-8", errors="replace")
                    try:
                        err_json = json.loads(err_raw)
                        err_msg = err_json.get("error", {}).get("message") or err_json.get("message") or err_raw
                    except Exception:
                        err_msg = err_raw
                    yield f"event: error\ndata: {json.dumps({'error': f'[{provider} HTTP {response.status_code}] {err_msg}'})}\n\n"
                    return

                async for line in response.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        raw = line[6:].strip()
                        try:
                            chunk = json.loads(raw)
                            delta = chunk["choices"][0]["delta"]
                            content = delta.get("content")
                            if content:
                                yield f"event: delta\ndata: {json.dumps({'content': content})}\n\n"
                        except Exception:
                            continue
                    elif line == "data: [DONE]":
                        yield "event: done\ndata: [DONE]\n\n"
                        break
    except Exception as e:
        yield f"event: error\ndata: {json.dumps({'error': f'Gateway exception: {str(e)}'})}\n\n"
