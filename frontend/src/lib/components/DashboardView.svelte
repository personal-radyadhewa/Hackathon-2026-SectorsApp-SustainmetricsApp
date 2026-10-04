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
    Info,
    CheckCircle2,
    AlertTriangle,
  } from '@lucide/svelte';

  let {
    auditRun = null,
    benchmarks = [],
    onSelectTicker,
    onNavigateView,
  } = $props();

  function getQuadrantColor(quadrantCode) {
    if (quadrantCode === 'Q1' || (quadrantCode && quadrantCode.includes('Tangguh'))) {
      return {
        badge: 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/50 dark:text-emerald-300 dark:border-emerald-800',
        label: '🌱 Verified Green Leader',
        desc: 'Strong green practices backed by solid financial cash flow.',
      };
    }
    if (quadrantCode === 'Q2' || (quadrantCode && quadrantCode.includes('Spekulatif'))) {
      return {
        badge: 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/50 dark:text-amber-300 dark:border-amber-800',
        label: '⚠️ Caution: High Claims, Low Funding',
        desc: 'High environmental claims but insufficient investment capital backing them.',
      };
    }
    if (quadrantCode === 'Q3' || (quadrantCode && quadrantCode.includes('Konvensional'))) {
      return {
        badge: 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/50 dark:text-blue-300 dark:border-blue-800',
        label: '💼 Traditional Business Model',
        desc: 'High cash generation but traditional operations with minimal green transition.',
      };
    }
    return {
      badge: 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-950/50 dark:text-rose-300 dark:border-rose-800',
      label: '🚨 High Risk / Needs Improvement',
      desc: 'Low sustainability compliance and limited financial capacity.',
    };
  }

  let quadStyle = $derived(getQuadrantColor(auditRun?.quadrant));
  let coverageRatio = $derived(auditRun?.financial_snapshot?.capex_coverage_ratio ?? 0);
  let capexIDR = $derived((auditRun?.financial_snapshot?.capital_expenditures ?? 0) / 1e9);
  let ocfIDR = $derived((auditRun?.financial_snapshot?.operating_cash_flow ?? 0) / 1e9);
</script>

<div class="space-y-6">
  <!-- Top Banner: Company Profile & Rating Summary -->
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-xs">
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
      <div>
        <div class="flex flex-wrap items-center gap-2.5 mb-2">
          <span class="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight font-mono">{auditRun?.ticker || 'COMPANY'}</span>
          <span class="text-xs px-3 py-1 rounded-full font-medium border {quadStyle.badge}">
            {quadStyle.label}
          </span>
          <span class="text-xs px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-medium">
            Indonesia Green Taxonomy (TKBI)
          </span>
        </div>
        <p class="text-sm font-medium text-slate-600 dark:text-slate-300 flex items-center gap-2">
          <Building2 size={16} class="text-slate-400 dark:text-slate-500" />
          <span>{auditRun?.company_name || 'Loading Company Information...'}</span>
          <span class="text-slate-300 dark:text-slate-700">•</span>
          <span class="text-slate-500 dark:text-slate-400 text-xs">{auditRun?.subsector || 'Energy / Utilities'}</span>
        </p>
      </div>

      <div class="flex items-center gap-2.5">
        <button
          type="button"
          onclick={() => onNavigateView('tkbi')}
          class="flex items-center space-x-1.5 px-3.5 py-2 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700/80 border border-slate-200 dark:border-slate-700 text-xs font-medium text-slate-800 dark:text-slate-200 rounded-lg shadow-2xs transition-colors"
        >
          <FileSpreadsheet size={15} class="text-emerald-500" />
          <span>View Checklist</span>
        </button>

        <button
          type="button"
          onclick={() => onNavigateView('traces')}
          class="flex items-center space-x-1.5 px-3.5 py-2 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700/80 border border-slate-200 dark:border-slate-700 text-xs font-medium text-slate-800 dark:text-slate-200 rounded-lg shadow-2xs transition-colors"
        >
          <TrendingUp size={15} class="text-blue-500" />
          <span>Activity Log</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Primary Score Cards Grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <!-- Sustainability Score Card -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-xs flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between text-slate-500 dark:text-slate-400 text-xs font-medium mb-3">
          <span>Sustainability Score</span>
          <CheckCircle size={16} class="text-emerald-500" />
        </div>
        <div class="flex items-baseline space-x-2">
          <span class="text-3xl font-bold text-slate-900 dark:text-slate-100 font-mono">{auditRun?.consistency_score?.toFixed(0) ?? '--'}</span>
          <span class="text-xs text-slate-400 font-medium">/ 100</span>
        </div>
      </div>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-3 pt-3 border-t border-slate-100 dark:border-slate-800/80 leading-relaxed">
        {auditRun?.consistency_score >= 70 ? 'High alignment with green standards.' : 'Needs stronger environmental reporting.'}
      </p>
    </div>

    <!-- Financial Health Score Card -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-xs flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between text-slate-500 dark:text-slate-400 text-xs font-medium mb-3">
          <span>Financial Strength</span>
          <DollarSign size={16} class="text-blue-500" />
        </div>
        <div class="flex items-baseline space-x-2">
          <span class="text-3xl font-bold text-slate-900 dark:text-slate-100 font-mono">{auditRun?.viability_score?.toFixed(0) ?? '--'}</span>
          <span class="text-xs text-slate-400 font-medium">/ 100</span>
        </div>
      </div>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-3 pt-3 border-t border-slate-100 dark:border-slate-800/80 leading-relaxed">
        {auditRun?.viability_score >= 60 ? 'Strong operating cash reserves.' : 'Moderate cash cushion for new projects.'}
      </p>
    </div>

    <!-- Green Investment Backing -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-xs flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between text-slate-500 dark:text-slate-400 text-xs font-medium mb-3">
          <span>Investment Backing</span>
          <Scale size={16} class="text-amber-500" />
        </div>
        <div class="flex items-baseline space-x-2">
          <span class="text-3xl font-bold text-slate-900 dark:text-slate-100 font-mono">{coverageRatio?.toFixed(2) ?? '--'}x</span>
        </div>
      </div>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-3 pt-3 border-t border-slate-100 dark:border-slate-800/80 leading-relaxed">
        {coverageRatio >= 1.0 ? 'Self-funded green transition from cash flow.' : 'Relies heavily on debt or external funding.'}
      </p>
    </div>

    <!-- Status Overview -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-xs flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between text-slate-500 dark:text-slate-400 text-xs font-medium mb-3">
          <span>Category</span>
          <ShieldAlert size={16} class="text-purple-500" />
        </div>
        <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">
          {auditRun?.quadrant_label || 'Pending Assessment'}
        </div>
      </div>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-3 pt-3 border-t border-slate-100 dark:border-slate-800/80 leading-relaxed">
        {quadStyle.desc}
      </p>
    </div>
  </div>

  <!-- Comparison Matrix (Scatter Plot) -->
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-xs">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
      <div>
        <h2 class="text-base font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <span>Peer Comparison Matrix</span>
          <span class="text-xs font-normal text-slate-500 dark:text-slate-400">
            (Sustainability Alignment vs. Financial Capacity)
          </span>
        </h2>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
          Shows whether companies have genuine cash flow backing their environmental pledges.
        </p>
      </div>

      <div class="text-xs text-slate-500 dark:text-slate-400 flex items-center gap-4">
        <span class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-emerald-500 inline-block shadow-xs"></span>
          <span class="font-medium text-slate-700 dark:text-slate-300">Selected ({auditRun?.ticker || 'None'})</span>
        </span>
        <span class="flex items-center gap-1.5">
          <span class="w-2.5 h-2.5 rounded-full bg-slate-400 inline-block"></span>
          <span>Peers (Click to compare)</span>
        </span>
      </div>
    </div>

    <!-- Visual 2x2 Canvas Container -->
    <div class="relative w-full h-80 bg-slate-50/70 dark:bg-slate-950/40 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden p-6 select-none">
      <!-- Grid Crosshair lines (X=50, Y=50) -->
      <div class="absolute left-1/2 top-0 bottom-0 w-px border-r border-dashed border-slate-300 dark:border-slate-700"></div>
      <div class="absolute top-1/2 left-0 right-0 h-px border-b border-dashed border-slate-300 dark:border-slate-700"></div>

      <!-- Quadrant Background Zones -->
      <!-- Top-Left: High claims, low cash -->
      <div class="absolute top-3 left-4 text-xs font-medium text-amber-600/90 dark:text-amber-400/90 pointer-events-none">
        ⚠️ High Claims, Low Cash<br/>
        <span class="text-[10px] text-slate-500 dark:text-slate-400">Greenwashing risk area</span>
      </div>

      <!-- Top-Right: High sustainability, high cash -->
      <div class="absolute top-3 right-4 text-right text-xs font-medium text-emerald-700 dark:text-emerald-400 pointer-events-none">
        🌱 Green Leaders<br/>
        <span class="text-[10px] text-slate-500 dark:text-slate-400">Strong pledges & strong funding</span>
      </div>

      <!-- Bottom-Left: Low sustainability, low cash -->
      <div class="absolute bottom-3 left-4 text-xs font-medium text-rose-600/90 dark:text-rose-400/90 pointer-events-none">
        🚨 At Risk<br/>
        <span class="text-[10px] text-slate-500 dark:text-slate-400">Lagging behind standards</span>
      </div>

      <!-- Bottom-Right: Low sustainability, high cash -->
      <div class="absolute bottom-3 right-4 text-right text-xs font-medium text-blue-700 dark:text-blue-400 pointer-events-none">
        💼 Traditional Business<br/>
        <span class="text-[10px] text-slate-500 dark:text-slate-400">High cash, low green focus</span>
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
          class="absolute -translate-x-1/2 -translate-y-1/2 transition-all transform hover:scale-125 z-20 group cursor-pointer"
        >
          <div class="w-4 h-4 rounded-full {isCurrent ? 'bg-emerald-500 ring-4 ring-emerald-300 dark:ring-emerald-700 animate-pulse' : 'bg-slate-400 ring-2 ring-white dark:ring-slate-800'} flex items-center justify-center shadow-xs">
            <span class="w-1.5 h-1.5 rounded-full bg-white"></span>
          </div>

          <!-- Tooltip on hover -->
          <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs text-slate-800 dark:text-slate-200 px-3 py-2 rounded-lg shadow-lg whitespace-nowrap z-30">
            <div class="font-bold text-slate-900 dark:text-slate-100">{peer.ticker} • {peer.company_name}</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
              Sustainability: {peer.y_consistency.toFixed(0)} | Financial: {peer.x_viability.toFixed(0)}
            </div>
            <div class="text-[10px] text-emerald-600 dark:text-emerald-400 font-medium mt-0.5">{peer.quadrant_label}</div>
          </div>
        </button>
      {/each}

      <!-- Current Ticker Highlight Label -->
      {#if auditRun}
        {@const currentX = Math.min(94, Math.max(6, auditRun.viability_score))}
        {@const currentY = Math.min(94, Math.max(6, 100 - auditRun.consistency_score))}
        <div
          style="left: {currentX}%; top: {currentY}%;"
          class="absolute -translate-x-1/2 translate-y-3 text-[11px] font-semibold text-emerald-800 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/80 px-2 py-0.5 rounded-md border border-emerald-300 dark:border-emerald-700 shadow-2xs pointer-events-none"
        >
          {auditRun.ticker}
        </div>
      {/if}
    </div>
  </div>

  <!-- Executive Summary & Key Highlights -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Executive Summary Card -->
    <div class="lg:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-xs">
      <h3 class="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-3 flex items-center gap-2">
        <FileText size={16} class="text-emerald-500" />
        <span>Executive Summary</span>
      </h3>
      <div class="text-xs leading-relaxed text-slate-700 dark:text-slate-300 bg-slate-50 dark:bg-slate-950/40 p-4 rounded-lg border border-slate-100 dark:border-slate-800">
        {auditRun?.executive_summary || 'No audit summary generated yet. Click "Analyze" in the sidebar to generate.'}
      </div>

      {#if auditRun?.audit_findings && auditRun.audit_findings.length > 0}
        <div class="mt-5">
          <h4 class="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2.5">Key Findings & Notes</h4>
          <ul class="space-y-2">
            {#each auditRun.audit_findings as finding}
              <li class="text-xs text-slate-700 dark:text-slate-300 flex items-start space-x-2 bg-slate-50 dark:bg-slate-950/40 p-3 rounded-lg border border-slate-100 dark:border-slate-800">
                <CheckCircle2 size={15} class="text-emerald-500 shrink-0 mt-0.5" />
                <span class="leading-relaxed">{finding}</span>
              </li>
            {/each}
          </ul>
        </div>
      {/if}
    </div>

    <!-- Financial Capacity Snapshot -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-xs">
      <h3 class="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-4 flex items-center gap-2">
        <DollarSign size={16} class="text-blue-500" />
        <span>Financial Metrics</span>
      </h3>
      <div class="space-y-3 text-xs">
        <div class="flex justify-between items-center p-3 rounded-lg bg-slate-50 dark:bg-slate-950/40 border border-slate-100 dark:border-slate-800">
          <span class="text-slate-600 dark:text-slate-400">Cash from Operations</span>
          <span class="font-semibold text-slate-900 dark:text-slate-100 font-mono">IDR {ocfIDR.toFixed(2)} B</span>
        </div>
        <div class="flex justify-between items-center p-3 rounded-lg bg-slate-50 dark:bg-slate-950/40 border border-slate-100 dark:border-slate-800">
          <span class="text-slate-600 dark:text-slate-400">Capital Investments</span>
          <span class="font-semibold text-slate-900 dark:text-slate-100 font-mono">IDR {capexIDR.toFixed(2)} B</span>
        </div>
        <div class="flex justify-between items-center p-3 rounded-lg bg-slate-50 dark:bg-slate-950/40 border border-slate-100 dark:border-slate-800">
          <span class="text-slate-600 dark:text-slate-400">Investment Coverage</span>
          <span class="font-semibold font-mono {coverageRatio >= 1.0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400'}">{coverageRatio.toFixed(2)}x</span>
        </div>
        <div class="flex justify-between items-center p-3 rounded-lg bg-slate-50 dark:bg-slate-950/40 border border-slate-100 dark:border-slate-800">
          <span class="text-slate-600 dark:text-slate-400">Return on Assets</span>
          <span class="font-semibold text-slate-900 dark:text-slate-100 font-mono">{auditRun?.financial_snapshot?.roa_pct ?? 0}%</span>
        </div>
      </div>
    </div>
  </div>
</div>
