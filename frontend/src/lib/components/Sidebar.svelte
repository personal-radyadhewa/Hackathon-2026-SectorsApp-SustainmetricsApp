<script>
  import {
    Sun,
    Moon,
    LayoutDashboard,
    FileSpreadsheet,
    Activity,
    Clock,
    Sparkles,
    Play,
    RefreshCw,
    ShieldCheck,
    Search,
    ChevronDown,
    MessageSquare,
    Calendar,
    Settings,
    User,
    ChevronsUpDown,
    Check,
  } from '@lucide/svelte';

  let {
    currentView = 'ask-ai',
    onSelectView,
    activeTicker = 'PGEO',
    onSelectTicker,
    onTriggerAudit,
    isAuditing = false,
  } = $props();

  let isDarkMode = $state(false);
  let searchQuery = $state('');

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
</script>

<aside class="w-60 bg-transparent flex flex-col justify-between shrink-0 h-screen select-none pl-4 py-3.5 pr-2">
  <div class="flex flex-col space-y-4">
    <!-- Brand Logo (exact reference styling) -->
    <div class="flex items-center space-x-2.5 px-2 pt-1 pb-1">
      <div class="w-7 h-7 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-xs font-bold text-xs">
        <Sparkles size={16} class="fill-current" />
      </div>
      <h1 class="text-base font-semibold tracking-tight text-slate-900 dark:text-slate-100">
        AI Manager
      </h1>
    </div>

    <!-- Search input with shortcut badge (exact reference) -->
    <div class="px-1">
      <div class="relative flex items-center">
        <Search size={13} class="absolute left-3 text-slate-400" />
        <input
          type="text"
          bind:value={searchQuery}
          placeholder="Search..."
          class="w-full bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl pl-8 pr-10 py-1.5 text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-blue-500 shadow-2xs"
        />
        <div class="absolute right-2 px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-[10px] text-slate-400 font-mono">
          ⌘ S
        </div>
      </div>
    </div>

    <!-- Categorized Menu (exact reference structure) -->
    <div class="space-y-4 overflow-y-auto max-h-[calc(100vh-270px)] pr-1">
      <!-- Section 1: Overview -->
      <div class="space-y-1">
        <div class="flex items-center justify-between px-2 text-[11px] font-medium text-slate-400 dark:text-slate-500">
          <span>Overview</span>
          <div class="w-4 h-4 rounded-full bg-slate-950 dark:bg-slate-800 text-white flex items-center justify-center text-[9px]">
            ▾
          </div>
        </div>

        <button
          type="button"
          onclick={() => onSelectView('ask-ai')}
          class="w-full flex items-center space-x-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all {currentView === 'ask-ai' ? 'bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-semibold shadow-2xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'}"
        >
          <Sparkles size={15} class={currentView === 'ask-ai' ? 'text-blue-600 dark:text-emerald-400' : 'text-slate-400'} />
          <span>Ask AI</span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('dashboard')}
          class="w-full flex items-center space-x-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all {currentView === 'dashboard' ? 'bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-semibold shadow-2xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'}"
        >
          <LayoutDashboard size={15} class={currentView === 'dashboard' ? 'text-blue-600 dark:text-emerald-400' : 'text-slate-400'} />
          <span>Dashboard</span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('tkbi')}
          class="w-full flex items-center space-x-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all {currentView === 'tkbi' ? 'bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-semibold shadow-2xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'}"
        >
          <FileSpreadsheet size={15} class={currentView === 'tkbi' ? 'text-blue-600 dark:text-emerald-400' : 'text-slate-400'} />
          <span>Green Checklist</span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('traces')}
          class="w-full flex items-center space-x-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all {currentView === 'traces' ? 'bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-semibold shadow-2xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'}"
        >
          <Activity size={15} class={currentView === 'traces' ? 'text-blue-600 dark:text-emerald-400' : 'text-slate-400'} />
          <span>Activity Log</span>
        </button>
      </div>

      <!-- Section 2: Tools -->
      <div class="space-y-1">
        <div class="flex items-center justify-between px-2 text-[11px] font-medium text-slate-400 dark:text-slate-500">
          <span>Tools</span>
          <div class="w-4 h-4 rounded-full bg-slate-950 dark:bg-slate-800 text-white flex items-center justify-center text-[9px]">
            ▾
          </div>
        </div>

        <button
          type="button"
          onclick={() => onSelectView('schedules')}
          class="w-full flex items-center space-x-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all {currentView === 'schedules' ? 'bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 font-semibold shadow-2xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'}"
        >
          <Calendar size={15} class={currentView === 'schedules' ? 'text-blue-600 dark:text-emerald-400' : 'text-slate-400'} />
          <span>Automated Monitoring</span>
        </button>

        <!-- Company Switcher Pills -->
        <div class="px-2 pt-1 pb-1">
          <div class="text-[10px] text-slate-400 mb-1">Monitored Ticker:</div>
          <div class="flex flex-wrap gap-1">
            {#each predefinedTickers as t}
              <button
                type="button"
                onclick={() => onSelectTicker(t)}
                class="px-2 py-0.5 rounded-md text-[10px] font-mono font-semibold transition-all {activeTicker === t ? 'bg-slate-900 text-white dark:bg-emerald-500 dark:text-slate-950' : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200/60 dark:border-slate-700'}"
              >
                {t}
              </button>
            {/each}
          </div>
        </div>
      </div>

      <!-- Section 3: Manager -->
      <div class="space-y-1">
        <div class="flex items-center justify-between px-2 text-[11px] font-medium text-slate-400 dark:text-slate-500">
          <span>Manager</span>
          <div class="w-4 h-4 rounded-full bg-slate-950 dark:bg-slate-800 text-white flex items-center justify-center text-[9px]">
            ▾
          </div>
        </div>

        <button
          type="button"
          onclick={onTriggerAudit}
          disabled={isAuditing}
          class="w-full flex items-center space-x-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-800 transition-colors"
        >
          {#if isAuditing}
            <RefreshCw size={14} class="animate-spin text-emerald-500" />
            <span>Analyzing...</span>
          {:else}
            <Play size={14} class="text-slate-400" />
            <span>Run Audit ({activeTicker})</span>
          {/if}
        </button>

        <button
          type="button"
          onclick={toggleTheme}
          class="w-full flex items-center space-x-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-800 transition-colors"
        >
          {#if isDarkMode}
            <Moon size={14} class="text-slate-400" />
            <span>Dark Theme</span>
          {:else}
            <Sun size={14} class="text-amber-500" />
            <span>Light Theme</span>
          {/if}
        </button>
      </div>
    </div>
  </div>

  <!-- Bottom Section: "How can I help?" Card & User Profile (exact reference) -->
  <div class="space-y-3 pt-2">
    <!-- Helper Card -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-2xl p-3.5 text-center shadow-2xs space-y-1.5">
      <div class="text-xs font-semibold text-slate-900 dark:text-slate-100">How can I help?</div>
      <p class="text-[11px] text-slate-400 leading-tight">Ask me anything just a voice</p>
      <div class="pt-1">
        <button
          type="button"
          onclick={() => onSelectView('ask-ai')}
          class="w-full py-1.5 px-3 rounded-full border border-blue-600/30 text-blue-600 dark:text-blue-400 text-xs font-medium hover:bg-blue-50 dark:hover:bg-blue-950/40 transition-colors flex items-center justify-center gap-1.5 shadow-2xs"
        >
          <MessageSquare size={13} />
          <span>Chat with AI</span>
        </button>
      </div>
    </div>

    <!-- User Profile Bar (exact reference) -->
    <div class="flex items-center justify-between px-1 py-1">
      <div class="flex items-center space-x-2.5">
        <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-amber-500 to-amber-300 flex items-center justify-center text-white font-bold text-xs shadow-xs overflow-hidden">
          <span>D</span>
        </div>
        <div>
          <div class="text-xs font-semibold text-slate-900 dark:text-slate-100">David</div>
          <div class="text-[10px] text-slate-400">Admin</div>
        </div>
      </div>
      <button
        type="button"
        onclick={toggleTheme}
        class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1"
        title="Toggle Theme"
      >
        <ChevronsUpDown size={14} />
      </button>
    </div>
  </div>
</aside>
