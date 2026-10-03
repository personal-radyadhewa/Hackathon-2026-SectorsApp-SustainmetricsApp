<script>
  import {
    LayoutDashboard,
    FileSpreadsheet,
    Activity,
    Clock,
    Bot,
    Play,
    RefreshCw,
    ShieldCheck,
  } from '@lucide/svelte';

  let {
    currentView = 'dashboard',
    onSelectView,
    activeTicker = 'PGEO',
    onSelectTicker,
    onTriggerAudit,
    isAuditing = false,
    onToggleCopilot,
    isCopilotOpen = false,
  } = $props();

  const predefinedTickers = ['PGEO', 'ADRO', 'BBRI', 'BREN', 'BUMI'];
  let customTickerInput = $state('');

  function handleCustomTickerSubmit(e) {
    e.preventDefault();
    if (customTickerInput.trim()) {
      onSelectTicker(customTickerInput.trim().toUpperCase());
      customTickerInput = '';
    }
  }
</script>

<aside class="w-64 bg-slate-50 border-r border-slate-200 flex flex-col justify-between shrink-0 h-screen select-none">
  <div>
    <!-- Logo & Brand Header -->
    <div class="px-5 py-5 border-b border-slate-200 flex items-center justify-between">
      <div class="flex items-center space-x-2.5">
        <div class="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
          <ShieldCheck size={18} />
        </div>
        <div>
          <h1 class="text-sm font-bold tracking-tight text-slate-900 flex items-center gap-1.5">
            SustainMetric <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">IDX</span>
          </h1>
          <p class="text-[11px] text-slate-500 font-medium">Green Auditor</p>
        </div>
      </div>
    </div>

    <!-- Ticker Selection Switcher -->
    <div class="px-4 py-3.5 border-b border-slate-200 bg-white/50">
      <span class="text-[11px] uppercase tracking-wider text-slate-500 font-semibold mb-2 block">
        Active Emitent Ticker
      </span>
      <div class="grid grid-cols-5 gap-1 mb-2.5">
        {#each predefinedTickers as t}
          <button
            type="button"
            onclick={() => onSelectTicker(t)}
            class="py-1 px-1.5 text-xs font-mono font-semibold rounded transition-colors text-center {activeTicker === t ? 'bg-slate-900 text-white font-bold shadow-sm' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}"
          >
            {t}
          </button>
        {/each}
      </div>

      <form onsubmit={handleCustomTickerSubmit} class="flex items-center gap-1.5">
        <input
          type="text"
          bind:value={customTickerInput}
          placeholder="IDX Symbol..."
          class="w-full bg-slate-100 border border-slate-200 rounded px-2.5 py-1 text-xs font-mono text-slate-800 placeholder-slate-500 focus:outline-none focus:border-emerald-500/50"
        />
        <button
          type="submit"
          class="px-2 py-1 bg-slate-200 hover:bg-slate-300 text-slate-700 text-xs font-medium rounded transition-colors"
        >
          Go
        </button>
      </form>
    </div>

    <!-- Quick Run CTA -->
    <div class="px-4 py-3">
      <button
        type="button"
        onclick={onTriggerAudit}
        disabled={isAuditing}
        class="w-full flex items-center justify-center space-x-2 py-2 px-3 rounded-md bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs tracking-wide transition-all shadow-md disabled:opacity-50"
      >
        {#if isAuditing}
          <RefreshCw size={14} class="animate-spin" />
          <span>Auditing {activeTicker}...</span>
        {:else}
          <Play size={14} class="fill-current" />
          <span>Run Green Audit ({activeTicker})</span>
        {/if}
      </button>
    </div>

    <!-- Main Navigation Links -->
    <nav class="px-3 py-2 space-y-1">
      <button
        type="button"
        onclick={() => onSelectView('dashboard')}
        class="w-full flex items-center space-x-3 px-3 py-2 rounded-md text-xs font-medium transition-colors {currentView === 'dashboard' ? 'bg-slate-100 text-emerald-400 font-semibold border-l-2 border-emerald-500' : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'}"
      >
        <LayoutDashboard size={16} />
        <span>Dashboard & 2×2 Matrix</span>
      </button>

      <button
        type="button"
        onclick={() => onSelectView('tkbi')}
        class="w-full flex items-center space-x-3 px-3 py-2 rounded-md text-xs font-medium transition-colors {currentView === 'tkbi' ? 'bg-slate-100 text-emerald-400 font-semibold border-l-2 border-emerald-500' : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'}"
      >
        <FileSpreadsheet size={16} />
        <span>TKBI Audit Sheet (HITL)</span>
      </button>

      <button
        type="button"
        onclick={() => onSelectView('traces')}
        class="w-full flex items-center space-x-3 px-3 py-2 rounded-md text-xs font-medium transition-colors {currentView === 'traces' ? 'bg-slate-100 text-emerald-400 font-semibold border-l-2 border-emerald-500' : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'}"
      >
        <Activity size={16} />
        <span>Trace Waterfall (Otel)</span>
      </button>

      <button
        type="button"
        onclick={() => onSelectView('schedules')}
        class="w-full flex items-center space-x-3 px-3 py-2 rounded-md text-xs font-medium transition-colors {currentView === 'schedules' ? 'bg-slate-100 text-emerald-400 font-semibold border-l-2 border-emerald-500' : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'}"
      >
        <Clock size={16} />
        <span>Scheduled Jobs & Cron</span>
      </button>
    </nav>
  </div>

  <!-- Footer & AI Copilot Trigger -->
  <div class="p-3 border-t border-slate-200 space-y-2">
    <button
      type="button"
      onclick={onToggleCopilot}
      class="w-full flex items-center justify-between px-3 py-2 rounded-lg border {isCopilotOpen ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-400' : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-200'} transition-colors text-xs font-medium"
    >
      <div class="flex items-center space-x-2">
        <Bot size={15} class={isCopilotOpen ? 'text-emerald-400' : 'text-slate-500'} />
        <span>AI Copilot Chat</span>
      </div>
      <span class="w-2 h-2 rounded-full {isCopilotOpen ? 'bg-emerald-400 animate-pulse' : 'bg-slate-600'}"></span>
    </button>

    <div class="px-2 py-1 flex items-center justify-between text-[10px] text-slate-400 font-mono">
      <span>OJK TKBI Versi 3</span>
      <span class="text-emerald-500 font-bold">FastMCP Ready</span>
    </div>
  </div>
</aside>
