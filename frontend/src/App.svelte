<script>
  import { onMount } from 'svelte';
  import {
    ChevronLeft,
    Bell,
    MessageSquare,
    Headphones,
    Sparkles,
  } from '@lucide/svelte';

  import Sidebar from './lib/components/Sidebar.svelte';
  import AskAIView from './lib/components/AskAIView.svelte';
  import DashboardView from './lib/components/DashboardView.svelte';
  import TKBISheetView from './lib/components/TKBISheetView.svelte';
  import TraceWaterfallView from './lib/components/TraceWaterfallView.svelte';
  import SchedulesView from './lib/components/SchedulesView.svelte';

  import {
    fetchAudits,
    triggerAudit,
    fetchAuditDetail,
    fetchTKBIEntries,
    fetchAuditTraces,
    fetchBenchmarks,
    fetchSchedules,
  } from './lib/api.js';

  let currentView = $state('ask-ai');
  let activeTicker = $state('PGEO');
  let auditRun = $state(null);
  let tkbiEntries = $state([]);
  let traces = $state([]);
  let benchmarks = $state([]);
  let schedules = $state([]);
  let isAuditing = $state(false);
  let isLoading = $state(true);

  async function loadTickerData(ticker) {
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

      const benchData = await fetchBenchmarks();
      benchmarks = benchData.tickers || [];
    } catch (err) {
      console.error('Failed to load ticker data:', err);
    } finally {
      isLoading = false;
    }
  }

  async function handleTriggerAudit(targetTicker = activeTicker) {
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
      alert(`Audit error: ${err.message}`);
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
    loadTickerData(ticker);
  }

  onMount(async () => {
    await loadTickerData(activeTicker);
    await handleReloadSchedules();
  });

  const viewLabels = {
    'ask-ai': 'Ask AI',
    dashboard: 'Dashboard',
    tkbi: 'Green Checklist',
    traces: 'Activity Log',
    schedules: 'Automated Monitoring',
  };
</script>

<div class="flex h-screen w-screen overflow-hidden bg-[#f4f5f7] dark:bg-[#080b11] text-slate-900 dark:text-slate-100 font-sans">
  <!-- Left Navigation Sidebar -->
  <Sidebar
    {currentView}
    onSelectView={(v) => (currentView = v)}
    {activeTicker}
    onSelectTicker={handleSelectTicker}
    onTriggerAudit={() => handleTriggerAudit(activeTicker)}
    {isAuditing}
  />

  <!-- Main Viewport Area (curved canvas container matching reference) -->
  <main class="flex-1 flex flex-col h-[calc(100vh-1.75rem)] my-3.5 mr-3.5 rounded-[30px] bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm overflow-hidden">
    <!-- Top Bar inside Canvas (exact reference styling) -->
    <header class="h-14 border-b border-slate-100 dark:border-slate-800/80 px-6 flex items-center justify-between shrink-0 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md">
      <div class="flex items-center space-x-3 text-xs">
        <button
          type="button"
          class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1"
          title="Toggle view"
        >
          <ChevronLeft size={16} />
        </button>
        <div class="flex items-center space-x-1.5 text-slate-400">
          <span>Overview</span>
          <span>/</span>
          <span class="font-medium text-slate-900 dark:text-slate-100">{viewLabels[currentView] || currentView}</span>
        </div>
      </div>

      <div class="flex items-center space-x-3">
        {#if isAuditing}
          <div class="flex items-center space-x-2 text-xs font-medium text-blue-600 dark:text-emerald-400 bg-blue-50 dark:bg-emerald-950/40 border border-blue-200 dark:border-emerald-800 px-2.5 py-1 rounded-full">
            <span class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-ping"></span>
            <span>Analyzing {activeTicker}...</span>
          </div>
        {/if}

        <!-- Header Icons (exact reference: Notification bell with badge, chat, headset) -->
        <button
          type="button"
          class="relative p-2 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
          title="Notifications"
        >
          <Bell size={16} />
          <span class="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-rose-500"></span>
        </button>

        <button
          type="button"
          onclick={() => (currentView = 'ask-ai')}
          class="p-2 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
          title="Ask AI"
        >
          <MessageSquare size={16} />
        </button>

        <button
          type="button"
          class="p-2 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
          title="Support & Guides"
        >
          <Headphones size={16} />
        </button>
      </div>
    </header>

    <!-- Main Content Container -->
    <div class="flex-1 overflow-y-auto">
      {#if isLoading && currentView !== 'ask-ai'}
        <div class="flex flex-col items-center justify-center h-96 space-y-3 text-slate-500 dark:text-slate-400 text-sm">
          <div class="w-7 h-7 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <span>Loading company data for {activeTicker}...</span>
        </div>
      {:else if currentView === 'ask-ai'}
        <AskAIView
          {activeTicker}
          onSelectTicker={handleSelectTicker}
        />
      {:else if currentView === 'dashboard'}
        <div class="p-6 md:p-8 max-w-7xl mx-auto">
          <DashboardView
            {auditRun}
            {benchmarks}
            onSelectTicker={handleSelectTicker}
            onNavigateView={(v) => (currentView = v)}
          />
        </div>
      {:else if currentView === 'tkbi'}
        <div class="p-6 md:p-8 max-w-7xl mx-auto">
          <TKBISheetView
            {auditRun}
            entries={tkbiEntries}
            onReloadEntries={handleReloadEntries}
          />
        </div>
      {:else if currentView === 'traces'}
        <div class="p-6 md:p-8 max-w-7xl mx-auto">
          <TraceWaterfallView
            {auditRun}
            {traces}
          />
        </div>
      {:else if currentView === 'schedules'}
        <div class="p-6 md:p-8 max-w-7xl mx-auto">
          <SchedulesView
            {schedules}
            onReloadSchedules={handleReloadSchedules}
          />
        </div>
      {/if}
    </div>
  </main>
</div>
