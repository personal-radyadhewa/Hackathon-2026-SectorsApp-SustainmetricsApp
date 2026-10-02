"""Multi-Provider LLM Gateway supporting Gemini, OpenAI, Claude, and Ollama with tool execution."""

import json
from typing import AsyncGenerator, Any
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


async def stream_chat_completion(
    messages: list[dict[str, str]],
    provider: str = "gemini",
    model: str = "gemini-2.5-flash",
    api_key: str = "",
) -> AsyncGenerator[str, None]:
    """Stream chat responses with tool-calling support."""
    key = api_key or (settings.GEMINI_API_KEY if provider == "gemini" else settings.OPENAI_API_KEY)
    last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    
    # 1. Fallback / Offline intelligent synthesis mode if API key not provided
    if not key and provider != "ollama":
        yield f"event: delta\ndata: {json.dumps({'content': f'*(Operating in Offline Heuristic Mode - No API key provided)*\\n\\nAnalyzing query: \"{last_user_msg}\"...\\n\\n'})}\n\n"
        
        # Check if user mentioned an IDX ticker
        tickers = ["PGEO", "ADRO", "BBRI", "BREN", "BUMI"]
        detected = next((t for t in tickers if t in last_user_msg.upper()), None)
        if detected:
            yield f"event: delta\ndata: {json.dumps({'content': f'🔍 **Inspecting TKBI Evidence Dossier for {detected}**...\\n\\n'})}\n\n"
            evidence_json = await execute_tool_call("inspect_ticker_evidence", {"ticker": detected})
            data = json.loads(evidence_json)
            findings_bullets = "\\n".join([f"- {f}" for f in data.get("audit_findings", [])])
            resp = (
                f"### TKBI Audit Synthesis for {detected}\\n"
                f"- **Quadrant Classification**: {data.get('quadrant')}\\n"
                f"- **Consistency Score**: {data.get('consistency_score')}/100\\n"
                f"- **Viability Score**: {data.get('viability_score')}/100\\n\\n"
                f"**Audit Findings & Disclosures Analysis:**\\n{findings_bullets}\\n\\n"
                f"*To enable live generative multi-step LLM reasoning, configure your GEMINI_API_KEY or OPENAI_API_KEY in Settings.*"
            )
            yield f"event: delta\ndata: {json.dumps({'content': resp})}\n\n"
        else:
            search_res = json.loads(await execute_tool_call("query_tkbi_knowledge_base", {"query": last_user_msg}))
            matches = search_res.get("results", [])
            summary = "\\n".join([f"• **{m.get('activity')}** ({m.get('id')}): {m.get('tsc')[:120]}..." for m in matches[:2]])
            resp = (
                f"### OJK TKBI 2024 Taxonomy Query Results:\\n{summary}\\n\\n"
                f"*Provide an IDX ticker (e.g. PGEO, ADRO, BREN) to execute an automated green audit analysis.*"
            )
            yield f"event: delta\ndata: {json.dumps({'content': resp})}\n\n"

        yield f"event: done\ndata: [DONE]\n\n"
        return

    # 2. OpenAI / Gemini OpenAI-compatible endpoint
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/" if provider == "gemini" else (
        settings.OLLAMA_BASE_URL if provider == "ollama" else "https://api.openai.com/v1"
    )

    client_headers = {"Authorization": f"Bearer {key}"} if key else {}
    req_payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "tools": AVAILABLE_TOOLS,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", f"{base_url}/chat/completions", headers=client_headers, json=req_payload) as response:
                if response.status_code != 200:
                    err_text = await response.aread()
                    yield f"event: error\ndata: {json.dumps({'error': err_text.decode('utf-8')})}\n\n"
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
        yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
