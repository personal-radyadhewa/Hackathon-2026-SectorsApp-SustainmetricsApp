<script>
  import {
    TrendingUp,
    ShieldAlert,
    DollarSign,
    CheckCircle,
    Building2,
    Calendar,
    ArrowUpRight,
    Scale,
    FileSpreadsheet,
    FileText,
  } from '@lucide/svelte';

  let {
    auditRun = null,
    benchmarks = [],
    onSelectTicker,
    onNavigateView,
  } = $props();

  function getQuadrantColor(quadrantCode) {
    if (quadrantCode === 'Q1' || (quadrantCode && quadrantCode.includes('Tangguh'))) {
      return { bg: 'bg-emerald-500/15', text: 'text-emerald-400', border: 'border-emerald-500/30', label: 'Q1: Authentic Green' };
    }
    if (quadrantCode === 'Q2' || (quadrantCode && quadrantCode.includes('Spekulatif'))) {
      return { bg: 'bg-amber-500/15', text: 'text-amber-400', border: 'border-amber-500/30', label: 'Q2: Greenwashing Risk' };
    }
    if (quadrantCode === 'Q3' || (quadrantCode && quadrantCode.includes('Konvensional'))) {
      return { bg: 'bg-blue-500/15', text: 'text-blue-400', border: 'border-blue-500/30', label: 'Q3: Transition Cash Cow' };
    }
    return { bg: 'bg-rose-500/15', text: 'text-rose-400', border: 'border-rose-500/30', label: 'Q4: Brown / Red Flag' };
  }

  let quadStyle = $derived(getQuadrantColor(auditRun?.quadrant));
  let coverageRatio = $derived(auditRun?.financial_snapshot?.capex_coverage_ratio ?? 0);
  let capexIDR = $derived((auditRun?.financial_snapshot?.capital_expenditures ?? 0) / 1e9);
  let ocfIDR = $derived((auditRun?.financial_snapshot?.operating_cash_flow ?? 0) / 1e9);
</script>

<div class="space-y-6">
  <!-- Top Banner: Emitent Identity & Status -->
  <div class="bg-[#0E1527] border border-[#1E293B] rounded-xl p-5 shadow-sm">
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2.5 mb-1.5">
          <span class="text-xl font-mono font-bold text-slate-100 tracking-tight">{auditRun?.ticker || 'TICKER'}</span>
          <span class="text-xs px-2.5 py-0.5 rounded-full font-semibold border {quadStyle.bg} {quadStyle.text} {quadStyle.border}">
            {auditRun?.quadrant_label || 'Pending Audit'}
          </span>
          <span class="text-xs px-2 py-0.5 rounded bg-[#1A2338] text-slate-400 font-mono">
            OJK TKBI Versi 3
          </span>
        </div>
        <p class="text-sm font-medium text-slate-300 flex items-center gap-2">
          <Building2 size={15} class="text-slate-500" />
          <span>{auditRun?.company_name || 'Loading Emitent Data...'}</span>
          <span class="text-slate-600">•</span>
          <span class="text-slate-400 text-xs font-mono">{auditRun?.subsector || 'Energy / Utilities'}</span>
        </p>
      </div>

      <div class="flex items-center gap-2.5">
        <button
          type="button"
          onclick={() => onNavigateView('tkbi')}
          class="flex items-center space-x-1.5 px-3 py-1.5 bg-[#151F36] hover:bg-[#1D2B4A] border border-[#233357] text-xs font-medium text-slate-200 rounded-lg transition-colors"
        >
          <FileSpreadsheet size={14} class="text-emerald-400" />
          <span>Inspect TKBI Sheet</span>
        </button>

        <button
          type="button"
          onclick={() => onNavigateView('traces')}
          class="flex items-center space-x-1.5 px-3 py-1.5 bg-[#151F36] hover:bg-[#1D2B4A] border border-[#233357] text-xs font-medium text-slate-200 rounded-lg transition-colors"
        >
          <TrendingUp size={14} class="text-blue-400" />
          <span>View Otel Traces</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Primary Score Cards Grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <!-- Consistency Score -->
    <div class="bg-[#0E1527] border border-[#1E293B] rounded-xl p-4.5 shadow-sm">
      <div class="flex items-center justify-between text-slate-400 text-xs mb-2 font-medium">
        <span>TKBI Consistency Score</span>
        <CheckCircle size={15} class="text-emerald-400" />
      </div>
      <div class="flex items-baseline space-x-2">
        <span class="text-3xl font-mono font-bold text-slate-100">{auditRun?.consistency_score?.toFixed(1) ?? '--'}</span>
        <span class="text-xs text-slate-500 font-mono">/ 100</span>
      </div>
      <p class="text-[11px] text-slate-400 mt-2">
        Qualitative disclosure alignment against official technical criteria.
      </p>
    </div>

    <!-- Viability Score -->
    <div class="bg-[#0E1527] border border-[#1E293B] rounded-xl p-4.5 shadow-sm">
      <div class="flex items-center justify-between text-slate-400 text-xs mb-2 font-medium">
        <span>Financial Viability Score</span>
        <DollarSign size={15} class="text-blue-400" />
      </div>
      <div class="flex items-baseline space-x-2">
        <span class="text-3xl font-mono font-bold text-slate-100">{auditRun?.viability_score?.toFixed(1) ?? '--'}</span>
        <span class="text-xs text-slate-500 font-mono">/ 100</span>
      </div>
      <p class="text-[11px] text-slate-400 mt-2">
        Balance sheet capacity, operating cash flow, and Capex coverage ratio.
      </p>
    </div>

    <!-- Capex Coverage Ratio -->
    <div class="bg-[#0E1527] border border-[#1E293B] rounded-xl p-4.5 shadow-sm">
      <div class="flex items-center justify-between text-slate-400 text-xs mb-2 font-medium">
        <span>Capex Coverage (OCF/Capex)</span>
        <Scale size={15} class="text-amber-400" />
      </div>
      <div class="flex items-baseline space-x-2">
        <span class="text-3xl font-mono font-bold text-slate-100">{coverageRatio?.toFixed(2) ?? '--'}x</span>
      </div>
      <p class="text-[11px] text-slate-400 mt-2">
        {coverageRatio >= 1.0 ? '✅ Positive cashflow coverage for transition Capex.' : '⚠️ Relies on external debt/equity for Capex.'}
      </p>
    </div>

    <!-- Quadrant Matrix Designation -->
    <div class="bg-[#0E1527] border border-[#1E293B] rounded-xl p-4.5 shadow-sm">
      <div class="flex items-center justify-between text-slate-400 text-xs mb-2 font-medium">
        <span>Matrix Classification</span>
        <ShieldAlert size={15} class="text-purple-400" />
      </div>
      <div class="text-base font-bold text-slate-100 truncate">
        {auditRun?.quadrant || 'Unclassified'}
      </div>
      <p class="text-[11px] text-slate-400 mt-2 truncate">
        {auditRun?.quadrant_label || 'Run audit to determine quadrant'}
      </p>
    </div>
  </div>

  <!-- 2x2 Divergence Heatmap Scatter Matrix -->
  <div class="bg-[#0E1527] border border-[#1E293B] rounded-xl p-6 shadow-sm">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
      <div>
        <h2 class="text-base font-bold text-slate-100 flex items-center gap-2">
          <span>SustainMetric 2×2 Divergence Matrix</span>
          <span class="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-normal">
            Financial Capex vs. ESG Disclosures
          </span>
        </h2>
        <p class="text-xs text-slate-400">
          Cross-references qualitative claims against empirical cash flows to identify greenwashing risk zones.
        </p>
      </div>

      <div class="text-[11px] text-slate-400 flex items-center gap-3">
        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block"></span> Active ({auditRun?.ticker})</span>
        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-slate-500 inline-block"></span> Peers</span>
      </div>
    </div>

    <!-- Visual 2x2 Canvas Container -->
    <div class="relative w-full h-80 bg-[#090E1A] border border-[#1E293B] rounded-lg overflow-hidden p-6 select-none">
      <!-- Grid Crosshair lines (X=50, Y=50) -->
      <div class="absolute left-1/2 top-0 bottom-0 w-px bg-[#1E293B] border-r border-dashed border-slate-700"></div>
      <div class="absolute top-1/2 left-0 right-0 h-px bg-[#1E293B] border-b border-dashed border-slate-700"></div>

      <!-- Quadrant Background Zones -->
      <!-- Q2: Top-Left (Low Viability, High Consistency) -> Greenwashing Risk Zone -->
      <div class="absolute top-3 left-4 text-xs font-semibold text-amber-500/70 pointer-events-none">
        QUADRANT 2: DAMPAK SPEKULATIF<br/>
        <span class="text-[10px] font-normal text-amber-600/80">(High Rhetoric / Weak Capex - Greenwashing Risk)</span>
      </div>

      <!-- Q1: Top-Right (High Viability, High Consistency) -> Authentic Green -->
      <div class="absolute top-3 right-4 text-right text-xs font-semibold text-emerald-400/80 pointer-events-none">
        QUADRANT 1: TRANSISI TANGGUH<br/>
        <span class="text-[10px] font-normal text-emerald-500/80">(Authentic Decarbonization & Strong Cash Flow)</span>
      </div>

      <!-- Q4: Bottom-Left (Low Viability, Low Consistency) -> Brown / Laggard -->
      <div class="absolute bottom-3 left-4 text-xs font-semibold text-rose-500/70 pointer-events-none">
        QUADRANT 4: TERTINGGAL & RED FLAG<br/>
        <span class="text-[10px] font-normal text-rose-600/80">(High Carbon / Distressed Balance Sheet)</span>
      </div>

      <!-- Q3: Bottom-Right (High Viability, Low Consistency) -> Traditional Cash Cow -->
      <div class="absolute bottom-3 right-4 text-right text-xs font-semibold text-blue-400/70 pointer-events-none">
        QUADRANT 3: SUMBER KAS KONVENSIONAL<br/>
        <span class="text-[10px] font-normal text-blue-500/80">(High Profitability / Traditional Brown Model)</span>
      </div>

      <!-- Scatter Points for Peer Tickers -->
      {#each benchmarks as peer}
        {@const posX = Math.min(94, Math.max(6, peer.x_viability))}
        {@const posY = Math.min(94, Math.max(6, 100 - peer.y_consistency))}
        {@const isCurrent = peer.ticker === auditRun?.ticker}

        <button
          type="button"
          onclick={() => onSelectTicker(peer.ticker)}
          style="left: {posX}%; top: {posY}%;"
          class="absolute -translate-x-1/2 -translate-y-1/2 transition-all transform hover:scale-125 z-20 group"
        >
          <div class="w-4 h-4 rounded-full {isCurrent ? 'bg-emerald-400 ring-4 ring-emerald-500/30 animate-pulse' : 'bg-slate-400 ring-2 ring-slate-600'} flex items-center justify-center">
            <span class="w-1.5 h-1.5 rounded-full bg-slate-950"></span>
          </div>

          <!-- Tooltip on hover -->
          <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1.5 hidden group-hover:block bg-[#121B30] border border-[#233357] text-[11px] font-mono text-slate-200 px-2.5 py-1.5 rounded-md shadow-xl whitespace-nowrap z-30">
            <div class="font-bold text-emerald-400">{peer.ticker} ({peer.company_name})</div>
            <div>Viability: {peer.x_viability.toFixed(1)} | Consistency: {peer.y_consistency.toFixed(1)}</div>
            <div class="text-[10px] text-slate-400 font-sans">{peer.quadrant_label}</div>
          </div>
        </button>
      {/each}

      <!-- Current Ticker Highlight Label -->
      {#if auditRun}
        {@const currentX = Math.min(94, Math.max(6, auditRun.viability_score))}
        {@const currentY = Math.min(94, Math.max(6, 100 - auditRun.consistency_score))}
        <div
          style="left: {currentX}%; top: {currentY}%;"
          class="absolute -translate-x-1/2 translate-y-3 font-mono text-[10px] font-bold text-emerald-300 bg-emerald-950/80 px-1.5 py-0.5 rounded border border-emerald-500/40 pointer-events-none"
        >
          {auditRun.ticker} ({auditRun.consistency_score.toFixed(0)}, {auditRun.viability_score.toFixed(0)})
        </div>
      {/if}
    </div>
  </div>

  <!-- Executive Summary & Findings -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Executive Summary Card -->
    <div class="lg:col-span-2 bg-[#0E1527] border border-[#1E293B] rounded-xl p-5 shadow-sm">
      <h3 class="text-sm font-bold text-slate-100 mb-3 flex items-center gap-2">
        <FileText size={16} class="text-emerald-400" />
        <span>Executive Audit Dossier & OJK Alignment</span>
      </h3>
      <div class="text-xs leading-relaxed text-slate-300 bg-[#090E1A] p-4 rounded-lg border border-[#1A253D] font-mono">
        {auditRun?.executive_summary || 'No audit summary generated yet. Click "Run Green Audit" to trigger.'}
      </div>

      {#if auditRun?.audit_findings && auditRun.audit_findings.length > 0}
        <div class="mt-4">
          <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Key Disclosure & Technical Findings</h4>
          <ul class="space-y-2">
            {#each auditRun.audit_findings as finding}
              <li class="text-xs text-slate-300 flex items-start space-x-2 bg-[#121B30]/50 p-2.5 rounded border border-[#1A253D]">
                <span class="text-emerald-400 font-bold shrink-0">•</span>
                <span>{finding}</span>
              </li>
            {/each}
          </ul>
        </div>
      {/if}
    </div>

    <!-- Fundamental Financials Snapshot -->
    <div class="bg-[#0E1527] border border-[#1E293B] rounded-xl p-5 shadow-sm">
      <h3 class="text-sm font-bold text-slate-100 mb-3 flex items-center gap-2">
        <DollarSign size={16} class="text-blue-400" />
        <span>Fundamental Reality Check</span>
      </h3>
      <div class="space-y-3 text-xs">
        <div class="flex justify-between p-2 rounded bg-[#090E1A] border border-[#1A253D]">
          <span class="text-slate-400">Operating Cash Flow</span>
          <span class="font-mono text-slate-200">IDR {ocfIDR.toFixed(2)} B</span>
        </div>
        <div class="flex justify-between p-2 rounded bg-[#090E1A] border border-[#1A253D]">
          <span class="text-slate-400">Capital Expenditures</span>
          <span class="font-mono text-slate-200">IDR {capexIDR.toFixed(2)} B</span>
        </div>
        <div class="flex justify-between p-2 rounded bg-[#090E1A] border border-[#1A253D]">
          <span class="text-slate-400">Capex Coverage Ratio</span>
          <span class="font-mono font-bold {coverageRatio >= 1.0 ? 'text-emerald-400' : 'text-amber-400'}">{coverageRatio.toFixed(2)}x</span>
        </div>
        <div class="flex justify-between p-2 rounded bg-[#090E1A] border border-[#1A253D]">
          <span class="text-slate-400">Return on Assets (ROA)</span>
          <span class="font-mono text-slate-200">{auditRun?.financial_snapshot?.roa_pct ?? 0}%</span>
        </div>
      </div>
    </div>
  </div>
</div>
