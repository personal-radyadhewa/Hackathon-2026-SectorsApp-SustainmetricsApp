<script>
  import {
    Sun,
    Moon,
    LayoutDashboard,
    FileSpreadsheet,
    Activity,
    Clock,
    Bot,
    Sparkles,
    ShieldCheck,
  } from '@lucide/svelte';

  let {
    currentView = 'dashboard',
    onSelectView,
    activeTicker = 'PGEO',
    onSelectTicker,
  } = $props();

  let isDarkMode = $state(false);

  import { onMount } from 'svelte';
  onMount(() => {
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
      isDarkMode = true;
    } else {
      document.documentElement.classList.remove('dark');
      isDarkMode = false;
    }
  });

  function toggleTheme() {
    isDarkMode = !isDarkMode;
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.theme = 'dark';
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.theme = 'light';
    }
  }

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

<aside class="w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col justify-between shrink-0 h-screen select-none">
  <div class="flex flex-col">
    <!-- Logo & Brand Header -->
    <div class="px-5 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
      <div class="flex items-center space-x-2.5">
        <div class="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800/60 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
          <ShieldCheck size={18} />
        </div>
        <div>
          <h1 class="text-sm font-semibold tracking-tight text-slate-900 dark:text-slate-100 flex items-center gap-1.5">
            SustainMetric <span class="text-[10px] px-1.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 font-medium">IDX</span>
          </h1>
          <p class="text-[11px] text-slate-500 dark:text-slate-400">Green Auditor</p>
        </div>
      </div>
    </div>

    <!-- Company Selector -->
    <div class="p-4 border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/30">
      <span class="text-[11px] uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold mb-2 block">
        Select Company
      </span>
      <div class="grid grid-cols-5 gap-1 mb-2.5">
        {#each predefinedTickers as t}
          <button
            type="button"
            onclick={() => onSelectTicker(t)}
            class="py-1 px-1.5 text-xs font-semibold rounded-md transition-all text-center {activeTicker === t ? 'bg-slate-900 text-white dark:bg-emerald-500 dark:text-slate-950 shadow-xs' : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 border border-slate-200/60 dark:border-slate-700'}"
          >
            {t}
          </button>
        {/each}
      </div>

      <form onsubmit={handleCustomTickerSubmit} class="flex items-center gap-1.5">
        <input
          type="text"
          bind:value={customTickerInput}
          placeholder="Enter stock code..."
          class="w-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-md px-2.5 py-1 text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-emerald-500"
        />
        <button
          type="submit"
          class="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-medium rounded-md border border-slate-200 dark:border-slate-700 transition-colors"
        >
          Go
        </button>
      </form>
    </div>

    <!-- Primary Action: Ask about activeTicker -->
    <div class="p-3">
      <button
        type="button"
        onclick={() => onSelectView('chat')}
        class="w-full flex items-center justify-center space-x-2 py-2 px-3 rounded-lg bg-slate-900 dark:bg-emerald-500 hover:bg-slate-800 dark:hover:bg-emerald-400 text-white dark:text-slate-950 font-medium text-xs transition-all shadow-xs"
      >
        <Sparkles size={14} />
        <span>Ask about {activeTicker}</span>
      </button>
    </div>

    <!-- Main Navigation Links -->
    <nav class="px-3 py-1 space-y-1">
      <button
        type="button"
        onclick={() => onSelectView('chat')}
        class="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium transition-all {currentView === 'chat' ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-semibold shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-slate-100'}"
      >
        <Bot size={16} class={currentView === 'chat' ? 'text-emerald-500' : 'text-slate-400 dark:text-slate-500'} />
        <span>Ask AI Assistant</span>
      </button>

      <button
        type="button"
        onclick={() => onSelectView('dashboard')}
        class="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium transition-all {currentView === 'dashboard' ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-semibold shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-slate-100'}"
      >
        <LayoutDashboard size={16} class={currentView === 'dashboard' ? 'text-emerald-500' : 'text-slate-400 dark:text-slate-500'} />
        <span>Company Overview</span>
      </button>

      <button
        type="button"
        onclick={() => onSelectView('tkbi')}
        class="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium transition-all {currentView === 'tkbi' ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-semibold shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-slate-100'}"
      >
        <FileSpreadsheet size={16} class={currentView === 'tkbi' ? 'text-emerald-500' : 'text-slate-400 dark:text-slate-500'} />
        <span>Green Checklist</span>
      </button>

      <button
        type="button"
        onclick={() => onSelectView('traces')}
        class="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium transition-all {currentView === 'traces' ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-semibold shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-slate-100'}"
      >
        <Activity size={16} class={currentView === 'traces' ? 'text-emerald-500' : 'text-slate-400 dark:text-slate-500'} />
        <span>Activity Log</span>
      </button>

      <button
        type="button"
        onclick={() => onSelectView('schedules')}
        class="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium transition-all {currentView === 'schedules' ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-semibold shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-slate-100'}"
      >
        <Clock size={16} class={currentView === 'schedules' ? 'text-emerald-500' : 'text-slate-400 dark:text-slate-500'} />
        <span>Automated Monitoring</span>
      </button>
    </nav>
  </div>

  <!-- Footer -->
  <div class="p-3 border-t border-slate-100 dark:border-slate-800 space-y-2">
    <button
      type="button"
      onclick={toggleTheme}
      class="w-full flex items-center justify-between px-3 py-2 rounded-lg border bg-white dark:bg-slate-800/80 border-slate-200 dark:border-slate-700/80 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors text-xs font-medium shadow-2xs"
    >
      <div class="flex items-center space-x-2">
        {#if isDarkMode}
          <Moon size={15} class="text-slate-400" />
          <span>Dark Mode</span>
        {:else}
          <Sun size={15} class="text-amber-500" />
          <span>Light Mode</span>
        {/if}
      </div>
      <span class="text-[10px] text-slate-400">Switch</span>
    </button>

    <div class="px-2 py-1 text-center text-[10px] text-slate-400 dark:text-slate-500">
      <span>Indonesia Green Taxonomy (TKBI v3)</span>
    </div>
  </div>
</aside>
