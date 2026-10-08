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
    Download,
    Leaf,
    ShieldCheck,
    Flame,
    Zap,
    ExternalLink,
  } from '@lucide/svelte';
  import { getExportPDFUrl } from '../api.js';

  let {
    auditRun = null,
    benchmarks = [],
    watchlist = [],
    onSelectTicker,
    onNavigateView,
  } = $props();

  function getQuadrantColor(quadrantCode) {
    if (quadrantCode === 'Q1' || (quadrantCode && quadrantCode.includes('Tangguh'))) {
      return {
        badgeClass: 'bg-emerald-50 text-emerald-800 border-emerald-200 dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800',
        dotColor: 'bg-[#047857] dark:bg-[#34D399]',
        label: 'VERIFIED COMPLIANT',
        grade: 'Grade A+',
        gradeSub: '(Verified Green Leader)',
        desc: 'Full compliance with national green taxonomy (OJK POJK-51) backed by solid self-funded operating cash flow.',
      };
    }
    if (quadrantCode === 'Q2' || (quadrantCode && quadrantCode.includes('Spekulatif'))) {
      return {
        badgeClass: 'bg-amber-50 text-amber-800 border-amber-200 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800',
        dotColor: 'bg-[#D97706] dark:bg-[#FBBF24]',
        label: 'CAUTION: SPEKULATIF',
        grade: 'Grade B',
        gradeSub: '(High Claims, Low Cash)',
        desc: 'Ambitious environmental disclosures without sufficient internal capital expenditure or cash flow backing.',
      };
    }
    if (quadrantCode === 'Q3' || (quadrantCode && quadrantCode.includes('Konvensional'))) {
      return {
        badgeClass: 'bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800',
        dotColor: 'bg-[#1D4ED8] dark:bg-[#60A5FA]',
        label: 'TRADITIONAL CASH COW',
        grade: 'Grade B+',
        gradeSub: '(High Cash, Low ESG)',
        desc: 'Robust operational cash conversion but traditional high-carbon asset base requiring capital reallocation.',
      };
    }
    return {
      badgeClass: 'bg-rose-50 text-rose-800 border-rose-200 dark:bg-rose-950/60 dark:text-rose-300 dark:border-rose-800',
      dotColor: 'bg-[#DC2626] dark:bg-[#F87171]',
      label: 'HIGH ESG RISK',
      grade: 'Grade C',
      gradeSub: '(Non-Compliant & Laggard)',
      desc: 'Sub-threshold taxonomy compliance combined with constrained liquidity and elevated debt service.',
    };
  }

  let quadStyle = $derived(getQuadrantColor(auditRun?.quadrant));
  let coverageRatio = $derived(auditRun?.financial_snapshot?.capex_coverage_ratio ?? 0);
  let capexIDR = $derived((auditRun?.financial_snapshot?.capital_expenditures ?? 0) / 1e9);
  let ocfIDR = $derived((auditRun?.financial_snapshot?.operating_cash_flow ?? 0) / 1e9);
  let consistencyScore = $derived(auditRun?.consistency_score ?? 0);
  let viabilityScore = $derived(auditRun?.viability_score ?? 0);
  let roaPct = $derived(auditRun?.financial_snapshot?.roa_pct ?? 0);

  let activeMetricTab = $state('capex'); // 'capex' | 'revenue' | 'opex'
  let entityAgg = $derived(auditRun?.entity_aggregation || null);
  let activeAggData = $derived.by(() => {
    if (!entityAgg) return null;
    const raw = entityAgg[activeMetricTab];
    if (!raw) return null;
    return {
      ...raw,
      pct_hijau: raw.pct_hijau ?? raw.hijau ?? 0,
      pct_transisi: raw.pct_transisi ?? raw.transisi ?? 0,
      pct_transisi_interim: raw.pct_transisi_interim ?? raw.interim ?? 0,
      pct_tidak_memenuhi: raw.pct_tidak_memenuhi ?? raw.tidak_memenuhi ?? 0,
      pct_out_of_scope: raw.pct_out_of_scope ?? raw.out_of_scope ?? 0,
    };
  });
  let activitiesList = $derived(
    (auditRun?.activities_breakdown || []).map((act) => ({
      ...act,
      eo_category: act.eo_category || act.primary_eo || 'EO1',
      share_capex_pct: act.share_capex_pct ?? act.capex_pct ?? 0,
      share_rev_pct: act.share_rev_pct ?? act.revenue_pct ?? 0,
      share_opex_pct: act.share_opex_pct ?? act.opex_pct ?? 0,
    }))
  );

  let chartPeers = $derived.by(() => {
    // Strictly restrict peer dots to the active watchlist (plus current inspected emiten)
    if (!watchlist || watchlist.length === 0) {
      return benchmarks.filter((b) => b.ticker === auditRun?.ticker);
    }
    return benchmarks.filter(
      (b) => watchlist.includes(b.ticker) || b.ticker === auditRun?.ticker
    );
  });
</script>

<div class="space-y-6">
  <!-- Top Company Header Banner (Exact match to reference style) -->
  <div class="w-full bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-6">
    <div class="flex items-start md:items-center gap-5">
      <!-- Monogram Logo Badge -->
      <div class="relative w-16 h-16 rounded-xl bg-slate-100 dark:bg-[#162032] flex items-center justify-center shrink-0 overflow-hidden shadow-2xs border border-slate-200/60 dark:border-slate-700">
        <span class="font-headline font-bold text-2xl text-[#047857] dark:text-[#34D399]">
          {auditRun?.ticker?.slice(0, 2) || 'SM'}
        </span>
        <div class="absolute bottom-1 right-1 w-3 h-3 rounded-full {quadStyle.dotColor} ring-2 ring-white dark:ring-[#0F172A]"></div>
      </div>

      <div class="flex flex-col gap-1">
        <div class="flex flex-wrap items-center gap-2.5">
          <h1 class="font-headline font-bold text-xl md:text-2xl text-slate-900 dark:text-slate-100 tracking-tight">
            {auditRun?.company_name || 'Loading Company Profile...'}
          </h1>
          <span class="font-mono text-xs font-bold px-2 py-0.5 rounded-md bg-[#dce1ff] dark:bg-[#1e3a8a]/60 text-[#1d4ed8] dark:text-[#93c5fd]">
            {auditRun?.ticker || 'TICKER'}
          </span>
          <span class="px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-[#162032] text-slate-600 dark:text-slate-400 font-body text-xs font-medium">
            {auditRun?.subsector || 'Clean Utilities & Renewable Power'}
          </span>
        </div>
        <p class="font-body text-xs md:text-sm text-slate-500 dark:text-slate-400 max-w-2xl leading-relaxed">
          {auditRun?.executive_summary ? auditRun.executive_summary.slice(0, 160) + '...' : 'State-backed Indonesia clean transition issuer monitored under OJK POJK-51 and Taksonomi Keuangan Berkelanjutan Indonesia (TKBI 2024).'}
        </p>
      </div>
    </div>

    <!-- Action Triggers -->
    <div class="flex flex-wrap sm:flex-nowrap items-center gap-2.5 shrink-0">
      {#if auditRun}
        <a
          href={getExportPDFUrl(auditRun.id)}
          download
          class="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#162032] dark:hover:bg-slate-800 text-slate-800 dark:text-slate-200 font-medium text-xs transition-colors shadow-2xs border border-slate-200/80 dark:border-slate-700"
        >
          <Download size={15} class="text-[#047857] dark:text-[#34D399]" />
          <span>Audit Dossier (PDF)</span>
        </a>
      {/if}

      <button
        type="button"
        onclick={() => onNavigateView('tkbi')}
        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-medium text-xs transition-colors shadow-xs cursor-pointer font-semibold"
      >
        <FileSpreadsheet size={15} />
        <span>View TKBI Checklist</span>
      </button>
    </div>
  </div>

  <!-- Executive Audit Summary Cards (Top Verdict) -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <!-- Card 1: ESG Regulatory Verdict Card -->
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col justify-between gap-5 relative overflow-hidden">
      <div class="flex flex-col gap-3">
        <div class="flex items-center justify-between">
          <span class="font-mono text-xs uppercase tracking-wider text-slate-400 dark:text-slate-500 font-semibold">
            ESG Regulatory Verdict
          </span>
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold border {quadStyle.badgeClass}">
            <span class="w-2 h-2 rounded-full {quadStyle.dotColor}"></span>
            {quadStyle.label}
          </span>
        </div>

        <div class="flex items-baseline gap-3">
          <div class="flex items-center gap-2">
            <Leaf size={28} class="text-[#047857] dark:text-[#34D399]" />
            <span class="font-headline text-3xl font-bold text-slate-900 dark:text-slate-100 tracking-tight">
              {consistencyScore.toFixed(0)} <span class="text-sm font-mono text-slate-400 font-normal">/ 100</span>
            </span>
          </div>
          <span class="font-headline text-sm font-semibold text-[#047857] dark:text-[#34D399]">{quadStyle.gradeSub}</span>
        </div>

        <p class="font-body text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
          {quadStyle.desc}
        </p>
      </div>

      <!-- 3-Column Micro-Stats Strip -->
      <div class="grid grid-cols-3 gap-2 pt-3 bg-slate-50 dark:bg-[#162032] p-3 rounded-lg border border-slate-100 dark:border-slate-800">
        <div class="flex flex-col">
          <span class="text-[10px] font-mono text-slate-400">Taxonomy Score</span>
          <span class="font-mono text-sm font-bold text-slate-900 dark:text-slate-100 tabular-nums">{consistencyScore.toFixed(1)}%</span>
        </div>
        <div class="flex flex-col">
          <span class="text-[10px] font-mono text-slate-400">Viability Score</span>
          <span class="font-mono text-sm font-bold text-[#047857] dark:text-[#34D399] tabular-nums">{viabilityScore.toFixed(0)} / 100</span>
        </div>
        <div class="flex flex-col">
          <span class="text-[10px] font-mono text-slate-400">Framework</span>
          <span class="font-mono text-sm font-bold text-[#1D4ED8] dark:text-[#60A5FA]">OJK TKBI v3.0</span>
        </div>
      </div>
    </div>

    <!-- Card 2: Financial Health & Balance Sheet Cushion Card -->
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col justify-between gap-5 relative overflow-hidden">
      <div class="flex flex-col gap-3">
        <div class="flex items-center justify-between">
          <span class="font-mono text-xs uppercase tracking-wider text-slate-400 dark:text-slate-500 font-semibold">
            Financial Health &amp; Cash Cushion
          </span>
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold bg-blue-50 text-blue-800 border border-blue-200 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800">
            <span class="w-2 h-2 rounded-full bg-[#1D4ED8] dark:bg-[#60A5FA]"></span>
            {coverageRatio >= 1.0 ? 'SELF-FUNDED TRANSITION' : 'RELIANT ON EXTERNAL DEBT'}
          </span>
        </div>

        <div class="flex items-baseline gap-3">
          <span class="font-headline text-3xl font-bold text-slate-900 dark:text-slate-100 tracking-tight">
            {viabilityScore.toFixed(0)} <span class="text-sm font-mono text-slate-400 font-normal">/ 100</span>
          </span>
          <span class="font-headline text-sm font-semibold text-[#1D4ED8] dark:text-[#60A5FA]">
            {viabilityScore >= 60 ? 'Strong Operating Cushion' : 'Moderate Liquidity Reserve'}
          </span>
        </div>

        <p class="font-body text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
          Operating cash flow generated from core operations covers {coverageRatio.toFixed(2)}x of planned capital expenditure investments.
        </p>
      </div>

      <!-- 3-Column Micro-Stats Strip -->
      <div class="grid grid-cols-3 gap-2 pt-3 bg-slate-50 dark:bg-[#162032] p-3 rounded-lg border border-slate-100 dark:border-slate-800">
        <div class="flex flex-col">
          <span class="text-[10px] font-mono text-slate-400">Cash Flow (OCF)</span>
          <span class="font-mono text-sm font-bold text-slate-900 dark:text-slate-100 tabular-nums">IDR {ocfIDR.toFixed(1)}B</span>
        </div>
        <div class="flex flex-col">
          <span class="text-[10px] font-mono text-slate-400">Capex Coverage</span>
          <span class="font-mono text-sm font-bold {coverageRatio >= 1.0 ? 'text-[#047857] dark:text-[#34D399]' : 'text-amber-600 dark:text-amber-400'} tabular-nums">{coverageRatio.toFixed(2)}x</span>
        </div>
        <div class="flex flex-col">
          <span class="text-[10px] font-mono text-slate-400">Return on Assets</span>
          <span class="font-mono text-sm font-bold text-[#1D4ED8] dark:text-[#60A5FA] tabular-nums">{roaPct.toFixed(1)}%</span>
        </div>
      </div>
    </div>
  </div>

  <!-- OJK Tingkat 2: Entity Aggregation (Revenue, CapEx, OpEx) -->
  {#if entityAgg}
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm space-y-5">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-3 border-b border-slate-100 dark:border-slate-800">
        <div>
          <div class="flex items-center gap-2">
            <h2 class="text-base font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <Building2 size={18} class="text-[#047857] dark:text-[#34D399]" />
              <span>OJK Tingkat 2: Agregasi Entitas ({auditRun?.ticker || 'Emiten'})</span>
            </h2>
            <span class="font-mono text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300">
              OJK Fact Sheets Pg. 4-5
            </span>
          </div>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Proporsi klasifikasi aktivitas teragregasi terhadap total metrik keuangan entitas.
          </p>
        </div>

        <!-- Metric Switcher Tabs -->
        <div class="flex items-center gap-1.5 p-1 bg-slate-100 dark:bg-[#162032] rounded-lg">
          <button
            type="button"
            onclick={() => (activeMetricTab = 'capex')}
            class="px-3 py-1 rounded-md text-xs font-mono font-semibold transition-all cursor-pointer {activeMetricTab === 'capex'
              ? 'bg-white dark:bg-[#0F172A] text-[#047857] dark:text-[#34D399] shadow-2xs'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'}"
          >
            CapEx (Kredibilitas)
          </button>
          <button
            type="button"
            onclick={() => (activeMetricTab = 'revenue')}
            class="px-3 py-1 rounded-md text-xs font-mono font-semibold transition-all cursor-pointer {activeMetricTab === 'revenue'
              ? 'bg-white dark:bg-[#0F172A] text-[#047857] dark:text-[#34D399] shadow-2xs'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'}"
          >
            Revenue / Omset
          </button>
          <button
            type="button"
            onclick={() => (activeMetricTab = 'opex')}
            class="px-3 py-1 rounded-md text-xs font-mono font-semibold transition-all cursor-pointer {activeMetricTab === 'opex'
              ? 'bg-white dark:bg-[#0F172A] text-[#047857] dark:text-[#34D399] shadow-2xs'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'}"
          >
            OpEx Operasional
          </button>
        </div>
      </div>

      {#if activeAggData}
        <!-- Segmented Stacked Progress Bar -->
        <div class="space-y-2">
          <div class="flex items-center justify-between text-xs font-mono">
            <span class="text-slate-500">Bobot {activeMetricTab.toUpperCase()} Hijau &amp; Transisi:</span>
            <span class="font-bold text-[#047857] dark:text-[#34D399]">
              {(activeAggData.pct_hijau + activeAggData.pct_transisi + (activeAggData.pct_transisi_interim || 0)).toFixed(1)}% Terverifikasi OJK
            </span>
          </div>

          <div class="h-3.5 w-full rounded-full bg-slate-100 dark:bg-slate-800 flex overflow-hidden">
            <div style="width: {activeAggData.pct_hijau}%" class="bg-[#047857]" title="Hijau: {activeAggData.pct_hijau}%"></div>
            <div style="width: {activeAggData.pct_transisi}%" class="bg-[#D97706]" title="Transisi: {activeAggData.pct_transisi}%"></div>
            <div style="width: {activeAggData.pct_transisi_interim || 0}%" class="bg-[#0284C7]" title="Transisi Interim: {activeAggData.pct_transisi_interim || 0}%"></div>
            <div style="width: {activeAggData.pct_tidak_memenuhi}%" class="bg-[#DC2626]" title="Tidak Memenuhi: {activeAggData.pct_tidak_memenuhi}%"></div>
            <div style="width: {activeAggData.pct_out_of_scope}%" class="bg-slate-300 dark:bg-slate-700" title="Out of Scope: {activeAggData.pct_out_of_scope}%"></div>
          </div>
        </div>

        <!-- 5 KPI Chips -->
        <div class="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
          <div class="p-2.5 rounded-lg bg-emerald-50/50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800">
            <span class="text-[10px] font-mono uppercase text-[#047857] dark:text-[#34D399] font-bold block">Hijau (TSC)</span>
            <span class="font-mono text-sm font-bold text-[#047857] dark:text-[#34D399]">{activeAggData.pct_hijau}%</span>
          </div>
          <div class="p-2.5 rounded-lg bg-amber-50/50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800">
            <span class="text-[10px] font-mono uppercase text-amber-700 dark:text-amber-400 font-bold block">Transisi</span>
            <span class="font-mono text-sm font-bold text-amber-700 dark:text-amber-400">{activeAggData.pct_transisi}%</span>
          </div>
          <div class="p-2.5 rounded-lg bg-sky-50/50 dark:bg-sky-950/30 border border-sky-200 dark:border-sky-800">
            <span class="text-[10px] font-mono uppercase text-sky-700 dark:text-sky-400 font-bold block">Transisi Interim</span>
            <span class="font-mono text-sm font-bold text-sky-700 dark:text-sky-400">{activeAggData.pct_transisi_interim || 0}%</span>
          </div>
          <div class="p-2.5 rounded-lg bg-rose-50/50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800">
            <span class="text-[10px] font-mono uppercase text-rose-700 dark:text-rose-400 font-bold block">Tidak Memenuhi</span>
            <span class="font-mono text-sm font-bold text-rose-700 dark:text-rose-400">{activeAggData.pct_tidak_memenuhi}%</span>
          </div>
          <div class="p-2.5 rounded-lg bg-slate-100 dark:bg-[#162032] border border-slate-200 dark:border-slate-800">
            <span class="text-[10px] font-mono uppercase text-slate-500 font-bold block">Out of Scope</span>
            <span class="font-mono text-sm font-bold text-slate-700 dark:text-slate-300">{activeAggData.pct_out_of_scope}%</span>
          </div>
        </div>
      {/if}

      <!-- Multi-Activity Composition Table -->
      {#if activitiesList && activitiesList.length > 0}
        <div class="overflow-x-auto pt-2">
          <table class="w-full text-xs text-left">
            <thead class="text-[11px] font-mono uppercase bg-slate-50 dark:bg-[#162032] text-slate-400 border-b border-slate-100 dark:border-slate-800">
              <tr>
                <th class="py-2 px-3">Nama Aktivitas Bisnis</th>
                <th class="py-2 px-3">KBLI</th>
                <th class="py-2 px-3">EO Primer</th>
                <th class="py-2 px-3">Pangsa CapEx</th>
                <th class="py-2 px-3">Pangsa Revenue</th>
                <th class="py-2 px-3">Klasifikasi OJK</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800 font-body">
              {#each activitiesList as act}
                <tr class="hover:bg-slate-50/50 dark:hover:bg-[#162032]/40">
                  <td class="py-2 px-3 font-medium text-slate-900 dark:text-slate-100">{act.activity_name}</td>
                  <td class="py-2 px-3 font-mono text-slate-500">{act.kbli}</td>
                  <td class="py-2 px-3 font-mono font-semibold text-[#1D4ED8] dark:text-[#60A5FA]">{act.eo_category}</td>
                  <td class="py-2 px-3 font-mono font-bold text-slate-800 dark:text-slate-200">{act.share_capex_pct}%</td>
                  <td class="py-2 px-3 font-mono text-slate-600 dark:text-slate-400">{act.share_rev_pct}%</td>
                  <td class="py-2 px-3">
                    <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold {act.classification === 'HIJAU'
                      ? 'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300'
                      : act.classification === 'TRANSISI'
                      ? 'bg-amber-50 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300'
                      : act.classification === 'TRANSISI INTERIM'
                      ? 'bg-sky-50 text-sky-800 dark:bg-sky-950/60 dark:text-sky-300'
                      : 'bg-rose-50 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300'}">
                      {act.classification}
                    </span>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </div>
  {/if}

  <!-- Peer Comparison: 2x2 Divergence Radar Section -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-100 dark:border-slate-800">
      <div>
        <h2 class="text-base font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <span>Peer Divergence Radar: Sustainability vs. Financial Health</span>
        </h2>
        <p class="text-xs font-body text-slate-500 dark:text-slate-400 mt-0.5">
          Cartesian scatter verifying whether corporate ESG claims are backed by internal cash flow generation.
        </p>
      </div>

      <div class="text-xs font-mono text-slate-500 dark:text-slate-400 flex items-center gap-4">
        <span class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-[#047857] dark:bg-[#34D399] inline-block shadow-2xs"></span>
          <span class="font-semibold text-slate-900 dark:text-slate-100">Selected ({auditRun?.ticker || 'None'})</span>
        </span>
        <span class="flex items-center gap-1.5">
          <span class="w-2.5 h-2.5 rounded-full bg-slate-400 inline-block"></span>
          <span>Watchlist Peers ({chartPeers.filter(p => p.ticker !== auditRun?.ticker).length})</span>
        </span>
      </div>
    </div>

    <!-- Visual 2x2 Canvas Container -->
    <div class="relative w-full h-80 bg-slate-50/70 dark:bg-[#070A11] border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden p-6 select-none font-mono">
      <!-- Axis Labels -->
      <div class="absolute top-2.5 left-1/2 -translate-x-1/2 text-[9px] uppercase tracking-widest text-slate-400 font-semibold pointer-events-none">
        ▲ TKBI Alignment &amp; Sustainability Consistency (Y)
      </div>
      <div class="absolute right-4 bottom-2.5 text-[9px] uppercase tracking-widest text-slate-400 font-semibold pointer-events-none">
        Financial Health &amp; Cash Cushion (X) ▶
      </div>

      <!-- Grid Crosshairs (X=50, Y=50) -->
      <div class="absolute left-1/2 top-0 bottom-0 w-px border-r border-dashed border-slate-300 dark:border-slate-700"></div>
      <div class="absolute top-1/2 left-0 right-0 h-px border-b border-dashed border-slate-300 dark:border-slate-700"></div>

      <!-- Quadrant Diagnostics -->
      <div class="absolute top-3 left-4 text-[10px] text-amber-700 dark:text-[#FBBF24] pointer-events-none">
        <span class="font-bold">Q2: SPEKULATIF</span><br/>
        <span class="text-[9px] text-slate-500 dark:text-slate-400">High Claims / Low Cash Reserve</span>
      </div>

      <div class="absolute top-3 right-4 text-right text-[10px] text-[#047857] dark:text-[#34D399] pointer-events-none">
        <span class="font-bold">Q1: TANGGUH (LEADERS)</span><br/>
        <span class="text-[9px] text-slate-500 dark:text-slate-400">Verified Green &amp; Self-Funded</span>
      </div>

      <div class="absolute bottom-4 left-4 text-[10px] text-rose-700 dark:text-[#F87171] pointer-events-none">
        <span class="font-bold">Q4: RENTAN</span><br/>
        <span class="text-[9px] text-slate-500 dark:text-slate-400">Lagging Standards / High Risk</span>
      </div>

      <div class="absolute bottom-4 right-4 text-right text-[10px] text-blue-700 dark:text-[#60A5FA] pointer-events-none">
        <span class="font-bold">Q3: KONVENSIONAL</span><br/>
        <span class="text-[9px] text-slate-500 dark:text-slate-400">Cash Rich / Conventional Focus</span>
      </div>

      <!-- Peer Scatter Dots (Restricted strictly to user's active watchlist) -->
      {#each chartPeers as peer}
        {@const posX = Math.min(93, Math.max(7, peer.x_viability))}
        {@const posY = Math.min(93, Math.max(7, 100 - peer.y_consistency))}
        {@const isCurrent = peer.ticker === auditRun?.ticker}

        <button
          type="button"
          onclick={() => onSelectTicker(peer.ticker)}
          style="left: {posX}%; top: {posY}%;"
          class="absolute -translate-x-1/2 -translate-y-1/2 transition-all transform hover:scale-125 z-20 group cursor-pointer"
        >
          <div class="w-4 h-4 rounded-full {isCurrent ? 'bg-[#047857] dark:bg-[#34D399] ring-4 ring-emerald-300 dark:ring-emerald-700 animate-pulse' : 'bg-slate-400 ring-2 ring-white dark:ring-slate-800'} flex items-center justify-center shadow-xs">
            <span class="w-1.5 h-1.5 rounded-full bg-white dark:bg-[#0F172A]"></span>
          </div>

          <!-- Tooltip on hover -->
          <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block bg-white dark:bg-[#0B1120] border border-slate-200 dark:border-slate-700 text-xs text-slate-800 dark:text-slate-200 p-2.5 rounded-xl shadow-lg whitespace-nowrap z-30 font-mono">
            <div class="font-bold text-slate-900 dark:text-slate-100 flex items-center gap-1.5">
              <span>{peer.ticker}</span>
              <span class="text-[10px] text-slate-400 font-normal">({peer.company_name})</span>
            </div>
            <div class="text-[10px] text-slate-500 dark:text-slate-400 mt-1">
              Sustainability: {peer.y_consistency.toFixed(1)} | Financial Health: {peer.x_viability.toFixed(1)}
            </div>
            <div class="text-[10px] text-[#047857] dark:text-[#34D399] font-medium mt-0.5">
              {peer.quadrant_label}
            </div>
          </div>
        </button>
      {/each}

      <!-- Current Ticker Highlight Label -->
      {#if auditRun}
        {@const currentX = Math.min(93, Math.max(7, auditRun.viability_score))}
        {@const currentY = Math.min(93, Math.max(7, 100 - auditRun.consistency_score))}
        <div
          style="left: {currentX}%; top: {currentY}%;"
          class="absolute -translate-x-1/2 translate-y-3 text-[10px] font-mono font-bold text-[#047857] dark:text-[#34D399] bg-[#ECFDF5] dark:bg-[#064E3B] px-2 py-0.5 rounded-md border border-[#A7F3D0] dark:border-[#10B981] pointer-events-none shadow-2xs"
        >
          {auditRun.ticker} (Active)
        </div>
      {/if}
    </div>
  </div>

  <!-- Detailed Audit & Investment Breakdown (Two-Column Layout) -->
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
    <!-- LEFT COLUMN: Green & Sustainability Audit Scopes -->
    <div class="lg:col-span-6 flex flex-col gap-5">
      <div class="flex items-center justify-between pb-1">
        <div class="flex items-center gap-2.5">
          <div class="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-950/60 text-[#047857] dark:text-[#34D399] border border-emerald-200 dark:border-emerald-800">
            <Leaf size={18} />
          </div>
          <div>
            <h2 class="font-headline font-bold text-base text-slate-900 dark:text-slate-100">
              Green &amp; Sustainability Audit
            </h2>
            <span class="font-mono text-[10px] uppercase text-slate-400">OJK POJK-51 &amp; TKBI Standards</span>
          </div>
        </div>
        <span class="text-xs font-mono font-semibold px-2 py-0.5 bg-slate-100 dark:bg-[#162032] text-slate-700 dark:text-slate-300 rounded-md">
          Audited FY2024
        </span>
      </div>

      <!-- Scope 1, 2, 3 Emissions & Environmental Alignment -->
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="font-headline font-bold text-sm text-slate-900 dark:text-slate-100">
            Carbon &amp; Transition Scope Alignment
          </h3>
          <span class="text-[10px] font-mono text-slate-400">Unit: Metric tCO₂e</span>
        </div>

        <!-- Scope 1 -->
        <div class="space-y-1.5 p-3 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-100 dark:border-slate-800">
          <div class="flex items-center justify-between text-xs">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-[#047857] dark:bg-[#34D399]"></span>
              <span class="font-semibold text-slate-900 dark:text-slate-100 font-body">Direct Emissions (Scope 1)</span>
            </div>
            <span class="font-mono font-bold text-slate-900 dark:text-slate-100">18,400 t</span>
          </div>
          <div class="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
            <div class="bg-[#047857] dark:bg-[#34D399] h-full rounded-full" style="width: 32%"></div>
          </div>
          <div class="flex items-center justify-between text-[11px] font-mono">
            <span class="text-[#047857] dark:text-[#34D399] font-medium">▼ Down 4.2% YoY</span>
            <span class="text-slate-500">Benchmark: 95% below gas turbine threshold</span>
          </div>
        </div>

        <!-- Scope 2 -->
        <div class="space-y-1.5 p-3 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-100 dark:border-slate-800">
          <div class="flex items-center justify-between text-xs">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-[#1D4ED8] dark:bg-[#60A5FA]"></span>
              <span class="font-semibold text-slate-900 dark:text-slate-100 font-body">Purchased Power (Scope 2)</span>
            </div>
            <span class="font-mono font-bold text-slate-900 dark:text-slate-100">2,100 t</span>
          </div>
          <div class="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
            <div class="bg-[#1D4ED8] dark:bg-[#60A5FA] h-full rounded-full" style="width: 14%"></div>
          </div>
          <div class="flex items-center justify-between text-[11px] font-mono">
            <span class="text-[#047857] dark:text-[#34D399] font-medium">▼ Down 12.8% YoY</span>
            <span class="text-slate-500">Solar rooftop additions on steam facilities</span>
          </div>
        </div>

        <!-- Scope 3 -->
        <div class="space-y-1.5 p-3 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-100 dark:border-slate-800">
          <div class="flex items-center justify-between text-xs">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-[#D97706] dark:bg-[#FBBF24]"></span>
              <span class="font-semibold text-slate-900 dark:text-slate-100 font-body">Supply Chain &amp; Drilling (Scope 3)</span>
            </div>
            <span class="font-mono font-bold text-slate-900 dark:text-slate-100">38,900 t</span>
          </div>
          <div class="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
            <div class="bg-[#D97706] dark:bg-[#FBBF24] h-full rounded-full" style="width: 58%"></div>
          </div>
          <div class="flex items-center justify-between text-[11px] font-mono">
            <span class="text-slate-500 font-medium">● Stable Baseline</span>
            <span class="text-slate-500">Well drilling lifecycle emissions tracked</span>
          </div>
        </div>

        <!-- Plain English Audit Synthesis -->
        <div class="p-3.5 rounded-lg bg-emerald-50/60 dark:bg-emerald-950/30 border border-emerald-200/80 dark:border-emerald-800 flex items-start gap-3">
          <ShieldCheck size={20} class="text-[#047857] dark:text-[#34D399] shrink-0 mt-0.5" />
          <div>
            <span class="font-mono text-[10px] font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
              Audit Synthesis &amp; Avoided Carbon
            </span>
            <p class="font-body text-xs text-slate-600 dark:text-slate-300 mt-0.5 leading-relaxed">
              {auditRun?.ticker || 'Emitent'} mitigates approximately <strong class="text-[#047857] dark:text-[#34D399]">19x more emissions</strong> per fiscal quarter than its total Scope 1, 2, and 3 lifecycle outputs combined.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- RIGHT COLUMN: Financial Health & Regulatory Findings -->
    <div class="lg:col-span-6 flex flex-col gap-5">
      <div class="flex items-center justify-between pb-1">
        <div class="flex items-center gap-2.5">
          <div class="p-2 rounded-lg bg-blue-50 dark:bg-blue-950/60 text-[#1D4ED8] dark:text-[#60A5FA] border border-blue-200 dark:border-blue-800">
            <DollarSign size={18} />
          </div>
          <div>
            <h2 class="font-headline font-bold text-base text-slate-900 dark:text-slate-100">
              Financial Health &amp; Capex Ledger
            </h2>
            <span class="font-mono text-[10px] uppercase text-slate-400">Audited IDX Financials</span>
          </div>
        </div>
        <span class="text-xs font-mono font-semibold px-2 py-0.5 bg-slate-100 dark:bg-[#162032] text-slate-700 dark:text-slate-300 rounded-md">
          SectorsApp Synced
        </span>
      </div>

      <!-- Financial Metrics Grid -->
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
        <div class="grid grid-cols-2 gap-3 text-xs font-mono">
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-100 dark:border-slate-800">
            <span class="text-slate-400 text-[10px] block">Cash from Operations</span>
            <span class="text-base font-bold text-slate-900 dark:text-slate-100 tabular-nums">IDR {ocfIDR.toFixed(2)} B</span>
          </div>

          <div class="p-3 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-100 dark:border-slate-800">
            <span class="text-slate-400 text-[10px] block">Capex Investments</span>
            <span class="text-base font-bold text-slate-900 dark:text-slate-100 tabular-nums">IDR {capexIDR.toFixed(2)} B</span>
          </div>

          <div class="p-3 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-100 dark:border-slate-800">
            <span class="text-slate-400 text-[10px] block">Capex Coverage Ratio</span>
            <span class="text-base font-bold tabular-nums {coverageRatio >= 1.0 ? 'text-[#047857] dark:text-[#34D399]' : 'text-amber-600 dark:text-amber-400'}">
              {coverageRatio.toFixed(2)}x
            </span>
          </div>

          <div class="p-3 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-100 dark:border-slate-800">
            <span class="text-slate-400 text-[10px] block">Return on Assets (RoA)</span>
            <span class="text-base font-bold text-slate-900 dark:text-slate-100 tabular-nums">{roaPct.toFixed(1)}%</span>
          </div>
        </div>

        <!-- Disclosed Findings from OJK Audit -->
        <div class="pt-2 border-t border-slate-100 dark:border-slate-800">
          <h4 class="font-mono text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2.5">
            Key Disclosed Findings &amp; Observations
          </h4>
          <ul class="space-y-2">
            {#if auditRun?.audit_findings && auditRun.audit_findings.length > 0}
              {#each auditRun.audit_findings as finding}
                <li class="text-xs font-body text-slate-700 dark:text-slate-300 flex items-start space-x-2 bg-slate-50 dark:bg-[#162032] p-2.5 rounded-lg border border-slate-100 dark:border-slate-800">
                  <CheckCircle2 size={15} class="text-[#047857] dark:text-[#34D399] shrink-0 mt-0.5" />
                  <span class="leading-relaxed">{finding}</span>
                </li>
              {/each}
            {:else}
              <li class="text-xs text-slate-400 italic">No specific anomaly or warning findings reported in latest filing.</li>
            {/if}
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
