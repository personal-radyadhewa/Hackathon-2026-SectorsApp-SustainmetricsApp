<script>
  import { onMount } from 'svelte';
  import Sidebar from './lib/components/Sidebar.svelte';
  import DashboardView from './lib/components/DashboardView.svelte';
  import TKBISheetView from './lib/components/TKBISheetView.svelte';
  import TraceWaterfallView from './lib/components/TraceWaterfallView.svelte';
  import SchedulesView from './lib/components/SchedulesView.svelte';
  import AICopilotDrawer from './lib/components/AICopilotDrawer.svelte';

  import {
    fetchAudits,
    triggerAudit,
    fetchAuditDetail,
    fetchTKBIEntries,
    fetchAuditTraces,
    fetchBenchmarks,
    fetchSchedules,
  } from './lib/api.js';

  let currentView = $state('dashboard');
  let activeTicker = $state('PGEO');
  let auditRun = $state(null);
  let tkbiEntries = $state([]);
  let traces = $state([]);
  let benchmarks = $state([]);
  let schedules = $state([]);
  let isAuditing = $state(false);
  let isCopilotOpen = $state(false);
  let isLoading = $state(true);

  async function loadTickerData(ticker) {
    isLoading = true;
    try {
      // Find latest audit for this ticker in audits list
      const allAudits = await fetchAudits();
      const existing = allAudits.find((a) => a.ticker === ticker);

      if (existing) {
        auditRun = await fetchAuditDetail(existing.id);
        tkbiEntries = await fetchTKBIEntries(existing.id);
        traces = await fetchAuditTraces(existing.id);
      } else {
        // Automatically trigger audit for fresh ticker
        await handleTriggerAudit(ticker);
      }

      // Refresh benchmark scatter plot
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
    loadTickerData(ticker);
  }

  onMount(async () => {
    await loadTickerData(activeTicker);
    await handleReloadSchedules();
  });
  const viewLabels = {
    dashboard: 'Overview',
    tkbi: 'Green Checklist',
    traces: 'Activity Log',
    schedules: 'Automated Monitoring',
  };
</script>

<div class="flex h-screen w-screen overflow-hidden bg-slate-50 dark:bg-[#090D16] text-slate-900 dark:text-slate-100 font-sans">
  <!-- Left Navigation Sidebar -->
  <Sidebar
    {currentView}
    onSelectView={(v) => (currentView = v)}
    {activeTicker}
    onSelectTicker={handleSelectTicker}
    onTriggerAudit={() => handleTriggerAudit(activeTicker)}
    {isAuditing}
    onToggleCopilot={() => (isCopilotOpen = !isCopilotOpen)}
    {isCopilotOpen}
  />

  <!-- Main Viewport Area -->
  <main class="flex-1 flex flex-col h-screen overflow-y-auto bg-slate-50 dark:bg-[#090D16]">
    <!-- Top Bar with status & active emitent badge -->
    <header class="h-14 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/90 backdrop-blur-md px-6 flex items-center justify-between shrink-0 sticky top-0 z-30 shadow-xs">
      <div class="flex items-center space-x-2 text-sm">
        <span class="text-xs font-medium text-slate-400 dark:text-slate-500">Company</span>
        <span class="text-slate-300 dark:text-slate-700">/</span>
        <span class="text-xs font-semibold px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-mono">{activeTicker}</span>
        <span class="text-slate-300 dark:text-slate-700">/</span>
        <span class="text-xs font-medium text-slate-700 dark:text-slate-300">{viewLabels[currentView] || currentView}</span>
      </div>

      <div class="flex items-center space-x-3">
        {#if isAuditing}
          <div class="flex items-center space-x-2 text-xs font-medium text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 px-2.5 py-1 rounded-full">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping"></span>
            <span>Analyzing {activeTicker}...</span>
          </div>
        {/if}

        <button
          type="button"
          onclick={() => (isCopilotOpen = true)}
          class="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 text-xs font-medium text-slate-800 dark:text-slate-200 shadow-xs transition-colors"
        >
          <span class="text-emerald-500">✨</span>
          <span>Ask Sustainability Copilot</span>
        </button>
      </div>
    </header>

    <!-- Main Content Dynamic Container -->
    <div class="p-6 md:p-8 flex-1 max-w-7xl w-full mx-auto">
      {#if isLoading}
        <div class="flex flex-col items-center justify-center h-96 space-y-3 text-slate-500 dark:text-slate-400 text-sm">
          <div class="w-7 h-7 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
          <span>Loading sustainability profile for {activeTicker}...</span>
        </div>
      {:else if currentView === 'dashboard'}
        <DashboardView
          {auditRun}
          {benchmarks}
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
        />
      {:else if currentView === 'schedules'}
        <SchedulesView
          {schedules}
          onReloadSchedules={handleReloadSchedules}
        />
      {/if}
    </div>
  </main>

  <!-- Slide-out AI Copilot Drawer -->
  <AICopilotDrawer
    isOpen={isCopilotOpen}
    onClose={() => (isCopilotOpen = false)}
    {activeTicker}
  />
</div>
