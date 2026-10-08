<script>
  import { onMount } from 'svelte';
  import Sidebar from './lib/components/Sidebar.svelte';
  import WatchlistView from './lib/components/WatchlistView.svelte';
  import DashboardView from './lib/components/DashboardView.svelte';
  import AIChatView from './lib/components/AIChatView.svelte';
  import TKBISheetView from './lib/components/TKBISheetView.svelte';
  import TraceWaterfallView from './lib/components/TraceWaterfallView.svelte';
  import SchedulesView from './lib/components/SchedulesView.svelte';
  import TKBISimulatorView from './lib/components/TKBISimulatorView.svelte';
  import TKBIExplorerView from './lib/components/TKBIExplorerView.svelte';
  import TKBIPortfolioView from './lib/components/TKBIPortfolioView.svelte';
  import TKBISunsettingView from './lib/components/TKBISunsettingView.svelte';
  import TKBIRulesOverviewView from './lib/components/TKBIRulesOverviewView.svelte';
  import AnalysisOverviewView from './lib/components/AnalysisOverviewView.svelte';
  import { Sparkles, RefreshCw, ShieldCheck, Star, Building2, ArrowRight } from '@lucide/svelte';
  import { t, currentLang } from './lib/i18n.js';

  import {
    fetchAudits,
    triggerAudit,
    fetchAuditDetail,
    fetchTKBIEntries,
    fetchAuditTraces,
    fetchBenchmarks,
    fetchSchedules,
  } from './lib/api.js';

  // Start with no emiten selected; user lands on Watchlist to pick or add companies
  let activeTicker = $state(null);
  let currentView = $state('watchlist');

  let watchlist = $state(['PGEO', 'ADRO', 'BBRI', 'BREN', 'BUMI']);
  let allAudits = $state([]);
  let auditRun = $state(null);
  let tkbiEntries = $state([]);
  let traces = $state([]);
  let benchmarks = $state([]);
  let schedules = $state([]);
  let isAuditing = $state(false);
  let isLoading = $state(false);

  let auditingTickers = $state(new Set());

  function loadSavedWatchlist() {
    try {
      const saved = localStorage.getItem('sustainmetric_tickers');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          watchlist = parsed;
        }
      }
    } catch (e) {}
  }

  async function handleRefreshAllAudits() {
    try {
      allAudits = await fetchAudits();
    } catch (e) {
      console.error('Failed to reload audits:', e);
    }
  }

  async function handleRunAuditForTicker(ticker) {
    if (!ticker) return;
    const clean = ticker.toUpperCase();
    auditingTickers = new Set([...auditingTickers, clean]);
    try {
      await triggerAudit([clean]);
      allAudits = await fetchAudits();
      if (activeTicker === clean) {
        await loadTickerData(clean);
      }
    } catch (err) {
      console.error(`Audit trigger error for ${clean}:`, err);
    } finally {
      const next = new Set(auditingTickers);
      next.delete(clean);
      auditingTickers = next;
    }
  }

  async function handleToggleWatchlist(ticker) {
    const clean = ticker.toUpperCase();
    if (watchlist.includes(clean)) {
      if (watchlist.length <= 1) {
        alert('Keep at least one company in your watchlist.');
        return;
      }
      watchlist = watchlist.filter((t) => t !== clean);
      // If active ticker was removed, switch to first available watchlist item
      if (activeTicker === clean) {
        handleSelectTicker(watchlist[0]);
      }
    } else {
      watchlist = [...watchlist, clean];
      // Automatically trigger live audit if it doesn't already have an executive summary
      const hasSummary = allAudits.some((a) => a.ticker === clean && a.executive_summary);
      if (!hasSummary) {
        handleRunAuditForTicker(clean);
      }
    }
    try {
      localStorage.setItem('sustainmetric_tickers', JSON.stringify(watchlist));
    } catch (e) {}

    // Synchronize peer scatter matrix to only reflect active watchlist
    try {
      const targetList = [...new Set([...watchlist, ...(activeTicker ? [activeTicker] : [])])];
      const benchData = await fetchBenchmarks(targetList);
      benchmarks = benchData.tickers || [];
    } catch (e) {}
  }

  async function loadTickerData(ticker) {
    if (!ticker) return;
    isLoading = true;
    try {
      const allAudits = await fetchAudits();
      const existing = allAudits.find((a) => a.ticker === ticker);

      if (existing) {
        auditRun = await fetchAuditDetail(existing.id);
        tkbiEntries = await fetchTKBIEntries(existing.id);
        traces = await fetchAuditTraces(existing.id);
      } else {
        await handleTriggerAudit(ticker);
      }

      const targetList = [...new Set([...watchlist, ticker])];
      const benchData = await fetchBenchmarks(targetList);
      benchmarks = benchData.tickers || [];
    } catch (err) {
      console.error('Failed to load ticker data:', err);
    } finally {
      isLoading = false;
    }
  }

  async function handleTriggerAudit(targetTicker = activeTicker) {
    if (!targetTicker) return;
    isAuditing = true;
    try {
      const res = await triggerAudit([targetTicker]);
      if (res.runs && res.runs.length > 0) {
        const runId = res.runs[0].id;
        auditRun = await fetchAuditDetail(runId);
        tkbiEntries = await fetchTKBIEntries(runId);
        traces = await fetchAuditTraces(runId);
        const benchData = await fetchBenchmarks();
        benchmarks = benchData.tickers || [];
      }
    } catch (err) {
      alert(`Audit trigger error: ${err.message}`);
    } finally {
      isAuditing = false;
    }
  }

  async function handleReloadEntries() {
    if (auditRun) {
      tkbiEntries = await fetchTKBIEntries(auditRun.id);
    }
  }

  async function handleReloadSchedules() {
    try {
      schedules = await fetchSchedules();
    } catch (err) {
      console.error('Failed to reload schedules:', err);
    }
  }

  function handleSelectTicker(ticker) {
    activeTicker = ticker;
    if (ticker) {
      loadTickerData(ticker);
      currentView = 'dashboard';
    } else {
      auditRun = null;
      tkbiEntries = [];
      traces = [];
      currentView = 'watchlist';
    }
  }

  onMount(async () => {
    loadSavedWatchlist();
    await handleReloadSchedules();
    try {
      allAudits = await fetchAudits();
    } catch (e) {}
    try {
      const benchData = await fetchBenchmarks();
      benchmarks = benchData.tickers || [];
    } catch (e) {}
  });

  let viewLabels = $derived({
    watchlist: $t.watchlist,
    dashboard: $t.dashboard,
    chat: $t.chat,
    tkbi: $t.tkbi,
    traces: $t.traces,
    schedules: $t.schedules,
    simulator: $t.simulator,
    explorer: $t.explorer,
    portfolio: $t.portfolio,
    sunsetting: $t.sunsetting,
    'analysis-overview': $t.analysisOverview,
    'tkbi-overview': $t.tkbiOverview,
  });
</script>

<div class="flex h-screen w-screen overflow-hidden bg-[#faf8ff] dark:bg-[#070A11] text-slate-900 dark:text-slate-100 font-body">
  <!-- Left Navigation Sidebar -->
  <Sidebar
    {currentView}
    onSelectView={(v) => (currentView = v)}
    {activeTicker}
    onSelectTicker={handleSelectTicker}
    {watchlist}
    onToggleWatchlist={handleToggleWatchlist}
  />

  <!-- Main Viewport Area -->
  <main class="flex-1 flex flex-col h-screen overflow-y-auto bg-[#faf8ff] dark:bg-[#070A11]">
    <!-- Top Bar: Executive Workspace Header -->
    <header class="h-14 border-b border-slate-200/80 dark:border-slate-800 bg-white/90 dark:bg-[#0F172A]/90 backdrop-blur-md px-6 flex items-center justify-between shrink-0 sticky top-0 z-30 shadow-[0_1px_8px_rgba(0,0,0,0.03)] select-none">
      <!-- Breadcrumb & Emitent Context -->
      <div class="flex items-center space-x-2 text-xs">
        <span class="text-[11px] font-mono uppercase text-slate-400 dark:text-slate-500 font-semibold">{$t.auditDirectory}</span>
        <span class="text-slate-300 dark:text-slate-700">/</span>
        {#if activeTicker}
          <span class="text-xs font-mono font-bold px-2 py-0.5 rounded-md bg-slate-100 dark:bg-[#162032] text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-800">
            IDX: {activeTicker}
          </span>
        {:else}
          <span class="text-xs font-mono px-2 py-0.5 rounded-md bg-amber-50 dark:bg-amber-950/40 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
            {$t.selectCompany}
          </span>
        {/if}
        <span class="text-slate-300 dark:text-slate-700">/</span>
        <span class="text-xs font-semibold text-slate-700 dark:text-slate-300 font-headline">{viewLabels[currentView] || currentView}</span>
        
        {#if auditRun?.subsector}
          <span class="hidden md:inline-flex text-[10px] font-mono text-slate-500 dark:text-slate-400 ml-2 px-2 py-0.5 rounded-full bg-slate-100 dark:bg-[#162032] border border-slate-200 dark:border-slate-800">
            {auditRun.subsector}
          </span>
        {/if}
      </div>

      <!-- Action & Live Telemetry -->
      <div class="flex items-center space-x-3">
        <div class="hidden lg:flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-[#047857] dark:text-[#34D399] border border-emerald-200 dark:border-emerald-800 text-[11px] font-mono font-semibold">
          <span class="w-2 h-2 rounded-full bg-[#047857] dark:bg-[#34D399] animate-pulse"></span>
          <span>{$t.verifiedData}</span>
        </div>

        {#if activeTicker}
          {#if isAuditing}
            <div class="flex items-center space-x-1.5 text-xs font-mono font-medium text-[#047857] dark:text-[#34D399] bg-[#ECFDF5] dark:bg-[rgba(52,211,153,0.12)] border border-[#A7F3D0] dark:border-[rgba(52,211,153,0.35)] px-3 py-1 rounded-full">
              <span class="w-2 h-2 rounded-full bg-[#047857] dark:bg-[#34D399] animate-ping"></span>
              <span>{$t.auditing} {activeTicker}...</span>
            </div>
          {:else}
            <button
              type="button"
              onclick={() => handleTriggerAudit(activeTicker)}
              class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#162032] dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-800 text-xs font-medium cursor-pointer transition-colors shadow-2xs"
              title={$t.auditNow}
            >
              <RefreshCw size={13} class="text-slate-500" />
              <span class="hidden sm:inline">{$t.auditNow}</span>
            </button>
          {/if}

          <button
            type="button"
            onclick={() => (currentView = 'chat')}
            class="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] text-xs font-medium cursor-pointer transition-colors shadow-xs"
          >
            <Sparkles size={13} />
            <span>{$t.askAi} ({activeTicker})</span>
          </button>
        {:else}
          <button
            type="button"
            onclick={() => (currentView = 'watchlist')}
            class="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] text-xs font-semibold cursor-pointer transition-colors shadow-xs"
          >
            <Star size={13} class="fill-current" />
            <span>{$t.browseWatchlist}</span>
          </button>
        {/if}
      </div>
    </header>

    <!-- Main Content Dynamic Container -->
    <div class="p-5 md:p-7 flex-1 max-w-7xl w-full mx-auto">
      {#if isLoading}
        <div class="flex flex-col items-center justify-center h-96 space-y-3 text-slate-500 dark:text-slate-400 text-xs font-mono">
          <div class="w-7 h-7 border-2 border-[#047857] dark:border-[#34D399] border-t-transparent rounded-full animate-spin"></div>
          <span>{$t.loadingProfile} {activeTicker}...</span>
        </div>
      {:else if currentView === 'watchlist'}
        <!-- IDX Green Watchlist & Screener Page -->
        <WatchlistView
          {watchlist}
          audits={allAudits}
          {auditingTickers}
          onSelectTicker={handleSelectTicker}
          onToggleWatchlist={handleToggleWatchlist}
          onRunAudit={handleRunAuditForTicker}
          onRefreshAudits={handleRefreshAllAudits}
        />
      {:else if currentView === 'analysis-overview'}
        <AnalysisOverviewView
          {activeTicker}
          onNavigateView={(v) => (currentView = v)}
        />
      {:else if currentView === 'tkbi-overview'}
        <TKBIRulesOverviewView
          onNavigateView={(v) => (currentView = v)}
        />
      {:else if currentView === 'simulator'}
        <TKBISimulatorView />
      {:else if currentView === 'explorer'}
        <TKBIExplorerView />
      {:else if currentView === 'portfolio'}
        <TKBIPortfolioView />
      {:else if currentView === 'sunsetting'}
        <TKBISunsettingView />
      {:else if !activeTicker}
        <!-- Friendly Empty State when in sub-views without selected emiten -->
        <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-12 text-center max-w-xl mx-auto my-12 shadow-sm space-y-4">
          <div class="w-14 h-14 rounded-2xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-[#047857] dark:text-[#34D399] mx-auto shadow-xs">
            <Building2 size={28} />
          </div>
          <div>
            <h2 class="text-lg font-headline font-bold text-slate-900 dark:text-slate-100">
              No Emitent Selected
            </h2>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-sm mx-auto leading-relaxed">
              Please choose a company from your watchlist or browse the IDX screener to inspect its regulatory audit, scores, and activity log.
            </p>
          </div>
          <button
            type="button"
            onclick={() => (currentView = 'watchlist')}
            class="px-5 py-2.5 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-semibold text-xs transition-colors inline-flex items-center gap-2 shadow-xs cursor-pointer"
          >
            <span>Open Watchlist &amp; Screener</span>
            <ArrowRight size={14} />
          </button>
        </div>
      {:else if currentView === 'chat'}
        <AIChatView
          {activeTicker}
          companyName={auditRun?.company_name || ''}
        />
      {:else if currentView === 'dashboard'}
        <DashboardView
          {auditRun}
          {benchmarks}
          {watchlist}
          onSelectTicker={handleSelectTicker}
          onNavigateView={(v) => (currentView = v)}
        />
      {:else if currentView === 'tkbi'}
        <TKBISheetView
          {auditRun}
          entries={tkbiEntries}
          onReloadEntries={handleReloadEntries}
        />
      {:else if currentView === 'traces'}
        <TraceWaterfallView
          {auditRun}
          {traces}
          {tkbiEntries}
          onNavigateView={(v) => (currentView = v)}
        />
      {:else if currentView === 'schedules'}
        <SchedulesView
          {schedules}
          onReloadSchedules={handleReloadSchedules}
        />
      {/if}
    </div>
  </main>
</div>
