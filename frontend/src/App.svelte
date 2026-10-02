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
</script>

<div class="flex h-screen w-screen overflow-hidden bg-[#090D16] text-slate-100">
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
  <main class="flex-1 flex flex-col h-screen overflow-y-auto bg-[#090D16]">
    <!-- Top Bar with status & active emitent badge -->
    <header class="h-14 border-b border-[#1E293B] bg-[#0C1222]/80 backdrop-blur-md px-6 flex items-center justify-between shrink-0 sticky top-0 z-30">
      <div class="flex items-center space-x-3">
        <span class="text-xs uppercase tracking-wider font-bold text-slate-400">Workspace</span>
        <span class="text-slate-600">/</span>
        <span class="text-xs font-semibold text-emerald-400 font-mono">IDX:{activeTicker}</span>
        <span class="text-slate-600">/</span>
        <span class="text-xs font-medium text-slate-300 capitalize">{currentView}</span>
      </div>

      <div class="flex items-center space-x-3">
        {#if isAuditing}
          <div class="flex items-center space-x-2 text-xs font-mono text-emerald-400">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span>Auditing Pipeline Active...</span>
          </div>
        {/if}

        <button
          type="button"
          onclick={() => (isCopilotOpen = true)}
          class="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-[#141E34] hover:bg-[#1D2B4A] border border-[#223154] text-xs font-medium text-slate-200 transition-colors"
        >
          <span>🤖 AI Copilot</span>
        </button>
      </div>
    </header>

    <!-- Main Content Dynamic Container -->
    <div class="p-6 flex-1">
      {#if isLoading}
        <div class="flex flex-col items-center justify-center h-96 space-y-3 text-slate-400 text-xs">
          <div class="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
          <span>Retrieving OJK TKBI data for {activeTicker}...</span>
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
