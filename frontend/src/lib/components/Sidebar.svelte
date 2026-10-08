<script>
  import { onMount } from 'svelte';
  import {
    LayoutDashboard,
    FileSpreadsheet,
    Activity,
    Calendar,
    MessageSquare,
    ChevronsUpDown,
    Sun,
    Moon,
    Search,
    Plus,
    Building2,
    ShieldCheck,
    TrendingUp,
    Sparkles,
    Star,
    Sliders,
    Compass,
    PieChart,
    Hourglass,
    Languages,
  } from '@lucide/svelte';
  import { searchIdxTickers } from '../idxTickers.js';
  import { t, currentLang, toggleLanguage } from '../i18n.js';

  let {
    currentView = 'watchlist',
    onSelectView,
    activeTicker = null,
    onSelectTicker,
    watchlist = ['PGEO', 'ADRO', 'BBRI', 'BREN', 'BUMI'],
    onToggleWatchlist,
  } = $props();

  let isDarkMode = $state(false);
  let searchQuery = $state('');
  let customTickerInput = $state('');
  let isInputFocused = $state(false);
  let tickerSuggestions = $derived(searchIdxTickers(customTickerInput).slice(0, 6));

  onMount(() => {
    if (
      localStorage.theme === 'dark' ||
      (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
    ) {
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

    function handleCustomTickerSubmit(e) {
    e.preventDefault();
    const clean = customTickerInput.trim().toUpperCase();
    if (clean) {
      if (!watchlist.includes(clean)) {
        onToggleWatchlist(clean);
      }
      onSelectTicker(clean);
      customTickerInput = '';
      isInputFocused = false;
    }
  }

  function handleSelectSuggestion(ticker) {
    const clean = ticker.toUpperCase();
    if (!watchlist.includes(clean)) {
      onToggleWatchlist(clean);
    }
    onSelectTicker(clean);
    customTickerInput = '';
    isInputFocused = false;
  }

  function handleRemoveTicker(t, e) {
    e.stopPropagation();
    onToggleWatchlist(t);
    if (activeTicker === t) {
      onSelectTicker(null);
    }
  }
</script>

<aside class="w-64 bg-slate-50/70 dark:bg-[#070A11] border-r border-slate-200/80 dark:border-slate-800/80 flex flex-col justify-between shrink-0 h-screen select-none px-4 py-4 overflow-hidden">
  <!-- Pinned Top Brand & Search Header -->
  <div class="shrink-0 space-y-3 pb-2">
    <!-- Brand / System Title with Sustainability Emblem -->
    <div class="flex items-center space-x-3 px-1 pt-1 pb-1">
      <div class="w-8 h-8 rounded-lg bg-[#047857] dark:bg-[#34D399] flex items-center justify-center text-white dark:text-[#064E3B] font-headline font-bold text-base shadow-xs">
        <svg class="w-5 h-5 text-white dark:text-[#064E3B]" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M6 18C6 11.5 11.5 6 18 6C18 12.5 12.5 18 6 18Z" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.8"/>
          <path d="M6 18C10 14 14 10 18 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
          <path d="M8 13L12 9L15 11L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="flex flex-col">
        <h1 class="text-base font-headline font-bold tracking-tight text-slate-900 dark:text-slate-100 leading-none">
          Sustainmetric
        </h1>
        <span class="text-[10px] font-mono tracking-wider text-slate-500 dark:text-slate-400 uppercase mt-0.5">
          Auditor Workspace
        </span>
      </div>
    </div>

    <!-- Quick Search Input -->
    <div>
      <div class="relative flex items-center">
        <Search size={14} class="absolute left-3 text-slate-400" />
        <input
          type="text"
          bind:value={searchQuery}
          placeholder={$t.searchPlaceholder}
          class="w-full bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-800 rounded-xl pl-9 pr-3 py-1.5 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-[#047857] dark:focus:ring-[#34D399]"
        />
      </div>
    </div>
  </div>

  <!-- Scrollable Middle Section: Watchlist, Menus & Navigation -->
  <div class="flex-1 min-h-0 overflow-y-auto overflow-x-hidden space-y-4 pr-1 sidebar-scroll py-1">
    <!-- Target Emitents Watcher Card -->
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-3 shadow-2xs space-y-2">
      <div class="flex items-center justify-between gap-1">
        <span class="text-[10px] uppercase font-mono font-semibold text-slate-400 dark:text-slate-500 tracking-wider truncate">
          {$t.watchlist}
        </span>
        {#if activeTicker}
          <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/60 text-[#047857] dark:text-[#34D399] shrink-0 whitespace-nowrap">
            {activeTicker}
          </span>
        {:else}
          <span class="text-[9px] font-mono font-medium px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 shrink-0 whitespace-nowrap">
            {$t.selectCompany}
          </span>
        {/if}
      </div>

      <!-- Ticker Chips -->
      <div class="flex flex-wrap gap-1.5">
        {#each watchlist as t_item}
          <button
            type="button"
            onclick={() => onSelectTicker(t_item)}
            class="group flex items-center py-1 px-2.5 text-xs font-mono font-semibold rounded-lg transition-all cursor-pointer {activeTicker === t_item
              ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] shadow-xs'
              : 'bg-slate-100 dark:bg-[#162032] text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'}"
          >
            <span>{t_item}</span>
            <span
              role="button"
              tabindex="0"
              onclick={(e) => handleRemoveTicker(t_item, e)}
              onkeydown={(e) => e.key === 'Enter' && handleRemoveTicker(t_item, e)}
              title="{$t.remove} {t_item}"
              class="ml-1.5 text-[10px] text-slate-400 hover:text-rose-500 opacity-60 hover:opacity-100 transition-opacity"
            >
              ×
            </span>
          </button>
        {/each}
      </div>

      <!-- Add Emitent Code Form with Autocomplete Suggestions -->
      <div class="relative pt-1">
        <form onsubmit={handleCustomTickerSubmit} class="flex items-center gap-1.5">
          <input
            type="text"
            bind:value={customTickerInput}
            onfocus={() => (isInputFocused = true)}
            placeholder={$t.addCompanyPlaceholder}
            class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg px-2.5 py-1 text-xs font-mono text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none uppercase focus:border-[#047857] dark:focus:border-[#34D399]"
          />
          <button
            type="submit"
            class="px-2.5 py-1 bg-slate-900 hover:bg-slate-800 dark:bg-slate-700 dark:hover:bg-slate-600 text-white text-xs font-mono rounded-lg shrink-0 cursor-pointer"
          >
            {$t.add}
          </button>
        </form>

        <!-- Autocomplete Suggestions Popover -->
        {#if isInputFocused && customTickerInput.trim().length > 0}
          <div
            class="absolute left-0 right-0 top-full mt-1.5 bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl z-50 overflow-hidden divide-y divide-slate-100 dark:divide-slate-800 text-xs"
          >
            <div class="px-2.5 py-1 bg-slate-50 dark:bg-[#162032] flex items-center justify-between text-[10px] font-mono text-slate-400">
              <span>AVAILABLE IDX CODES</span>
              <button
                type="button"
                onclick={() => (isInputFocused = false)}
                class="hover:text-slate-700 dark:hover:text-slate-200 cursor-pointer text-xs"
              >
                ✕
              </button>
            </div>

            {#if tickerSuggestions.length > 0}
              <div class="max-h-44 overflow-y-auto divide-y divide-slate-50 dark:divide-slate-800/60">
                {#each tickerSuggestions as s}
                  {@const inWatch = watchlist.includes(s.ticker)}
                  <button
                    type="button"
                    onclick={() => handleSelectSuggestion(s.ticker)}
                    class="w-full text-left px-2.5 py-1.5 hover:bg-slate-50 dark:hover:bg-[#162032] flex items-center justify-between gap-1.5 transition-colors cursor-pointer"
                  >
                    <div class="flex items-center gap-2 min-w-0">
                      <span class="font-mono font-bold text-xs text-slate-900 dark:text-slate-100 px-1.5 py-0.5 rounded bg-slate-100 dark:bg-[#1E293B]">
                        {s.ticker}
                      </span>
                      <div class="truncate">
                        <div class="text-[11px] font-medium text-slate-800 dark:text-slate-200 truncate">{s.name}</div>
                        <div class="text-[9px] text-slate-400 truncate">{s.sector}</div>
                      </div>
                    </div>
                    <div class="shrink-0">
                      {#if inWatch}
                        <span class="text-[9px] font-mono text-emerald-600 dark:text-emerald-400 font-semibold">Active</span>
                      {:else}
                        <span class="text-[9px] font-mono text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded font-medium">+ Add</span>
                      {/if}
                    </div>
                  </button>
                {/each}
              </div>
            {/if}

            <!-- Direct Custom Add Option -->
            <button
              type="button"
              onclick={() => handleSelectSuggestion(customTickerInput)}
              class="w-full text-left px-2.5 py-2 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 text-[#047857] dark:text-[#34D399] font-mono text-[11px] flex items-center gap-1.5 cursor-pointer font-medium"
            >
              <Plus size={13} />
              <span>Confirm &amp; Audit IDX: <strong>{customTickerInput.trim().toUpperCase()}</strong></span>
            </button>
          </div>
        {/if}
      </div>
    </div>

    <!-- Navigation Sections -->
    <div class="space-y-3">
      <!-- Section 1: Analisis Perusahaan (Clickable Header for Definition & Routing) -->
      <div class="space-y-1">
        <button
          type="button"
          onclick={() => onSelectView('analysis-overview')}
          class="w-full text-left px-2 py-1 flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400 hover:text-[#047857] dark:text-slate-500 dark:hover:text-[#34D399] font-bold rounded-lg transition-colors cursor-pointer group"
          title={$currentLang === 'id' ? 'Klik untuk melihat penjelasan menu Analisis Perusahaan' : 'Click to read Company Analysis section guide'}
        >
          <span class="group-hover:underline">{$t.navAnalysis}</span>
          <span class="text-[9px] lowercase font-normal opacity-70 group-hover:opacity-100 flex items-center gap-0.5">
            <span>info</span>
            <span>→</span>
          </span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('watchlist')}
          class="w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer text-left {currentView === 'watchlist'
            ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] font-semibold shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#162032]'}"
        >
          <div class="flex items-center space-x-2.5 min-w-0">
            <Star size={15} class="shrink-0 {currentView === 'watchlist' ? 'fill-current' : ''}" />
            <span class="truncate">{$t.watchlist}</span>
          </div>
          <span class="text-[10px] font-mono px-1.5 py-0.2 rounded-full shrink-0 ml-1.5 {currentView === 'watchlist' ? 'bg-white/20' : 'bg-slate-200 dark:bg-slate-800'}">
            {watchlist.length}
          </span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('dashboard')}
          class="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer text-left {currentView === 'dashboard'
            ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] font-semibold shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#162032]'}"
        >
          <LayoutDashboard size={15} class="shrink-0" />
          <span class="truncate">{$t.dashboard}</span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('tkbi')}
          class="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer text-left {currentView === 'tkbi'
            ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] font-semibold shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#162032]'}"
        >
          <FileSpreadsheet size={15} class="shrink-0" />
          <span class="truncate">{$t.tkbi}</span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('traces')}
          class="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer text-left {currentView === 'traces'
            ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] font-semibold shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#162032]'}"
        >
          <Activity size={15} class="shrink-0" />
          <span class="truncate">{$t.traces}</span>
        </button>
      </div>

      <!-- Section 2: OJK TKBI Regulatory Flow (Clickable Header for Definition & Routing) -->
      <div class="space-y-1 pt-1">
        <button
          type="button"
          onclick={() => onSelectView('tkbi-overview')}
          class="w-full text-left px-2 py-1 flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400 hover:text-[#047857] dark:text-slate-500 dark:hover:text-[#34D399] font-bold rounded-lg transition-colors cursor-pointer group"
          title={$currentLang === 'id' ? 'Klik untuk membaca panduan & fungsi 4 modul aturan OJK' : 'Click to read Green Rules Guide overview'}
        >
          <span class="group-hover:underline">{$t.navTkbiFlow}</span>
          <span class="text-[9px] lowercase font-normal opacity-70 group-hover:opacity-100 flex items-center gap-0.5">
            <span>info</span>
            <span>→</span>
          </span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('simulator')}
          class="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer text-left {currentView === 'simulator'
            ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] font-semibold shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#162032]'}"
        >
          <Sliders size={15} class="shrink-0" />
          <span class="truncate">{$t.simulator}</span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('explorer')}
          class="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer text-left {currentView === 'explorer'
            ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] font-semibold shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#162032]'}"
        >
          <Compass size={15} class="shrink-0" />
          <span class="truncate">{$t.explorer}</span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('sunsetting')}
          class="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer text-left {currentView === 'sunsetting'
            ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] font-semibold shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#162032]'}"
        >
          <Hourglass size={15} class="shrink-0" />
          <span class="truncate">{$t.sunsetting}</span>
        </button>
      </div>

      <!-- Section 3: AI & Automasi -->
      <div class="space-y-1 pt-1">
        <div class="px-2 text-[10px] font-mono uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1 font-semibold">
          {$t.navAiTools}
        </div>

        <button
          type="button"
          onclick={() => onSelectView('chat')}
          class="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer text-left {currentView === 'chat'
            ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] font-semibold shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#162032]'}"
        >
          <MessageSquare size={15} class="shrink-0" />
          <span class="truncate">{$t.chat}</span>
        </button>

        <button
          type="button"
          onclick={() => onSelectView('schedules')}
          class="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer text-left {currentView === 'schedules'
            ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] font-semibold shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#162032]'}"
        >
          <Calendar size={15} class="shrink-0" />
          <span class="truncate">{$t.schedules}</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Bottom Pinned Controls: Helper Card & User Profile Row -->
  <div class="space-y-3 pt-3 shrink-0 border-t border-slate-200/80 dark:border-slate-800">
    <!-- ESG Mandate Badge Card -->
    <div class="p-3 bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl flex flex-col gap-1 shadow-2xs">
      <div class="flex items-center gap-1.5">
        <ShieldCheck size={16} class="text-[#047857] dark:text-[#34D399]" />
        <span class="font-mono text-[10px] font-semibold uppercase text-slate-800 dark:text-slate-200">{$t.esgMandateNotice}</span>
      </div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-tight">
        {$t.esgMandateDesc}
      </p>
    </div>

    <!-- User Profile, Language Switcher & Theme Switch -->
    <div class="flex items-center justify-between px-1 py-1">
      <div class="flex items-center space-x-2.5">
        <div class="w-8 h-8 rounded-full bg-[#047857] dark:bg-[#34D399] flex items-center justify-center text-white dark:text-[#064E3B] font-bold text-xs shadow-xs">
          SJ
        </div>
        <div>
          <div class="text-xs font-semibold text-slate-900 dark:text-slate-100">Sarah Jenkins</div>
          <div class="text-[10px] text-slate-400">{$t.auditorLead}</div>
        </div>
      </div>

      <div class="flex items-center space-x-1">
        <!-- Language Switcher: Exactly on the left side of the light/dark mode button -->
        <button
          type="button"
          onclick={toggleLanguage}
          class="flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-mono font-bold bg-slate-100 dark:bg-slate-800/80 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 transition-colors cursor-pointer"
          title={$currentLang === 'id' ? 'Switch to English' : 'Ganti ke Bahasa Indonesia'}
        >
          <Languages size={13} class="text-[#047857] dark:text-[#34D399]" />
          <span>{$currentLang === 'id' ? 'ID' : 'EN'}</span>
        </button>

        <!-- Theme Switcher Button -->
        <button
          type="button"
          onclick={toggleTheme}
          class="p-1.5 rounded-lg text-slate-500 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors cursor-pointer"
          title={$t.themeToggle}
        >
          {#if isDarkMode}
            <Moon size={15} class="text-[#34D399]" />
          {:else}
            <Sun size={15} class="text-amber-500" />
          {/if}
        </button>
      </div>
    </div>
  </div>
</aside>

<style>
  .sidebar-scroll::-webkit-scrollbar {
    width: 4px;
  }
  .sidebar-scroll::-webkit-scrollbar-track {
    background: transparent;
  }
  .sidebar-scroll::-webkit-scrollbar-thumb {
    background: rgba(148, 163, 184, 0.25);
    border-radius: 4px;
  }
  .sidebar-scroll::-webkit-scrollbar-thumb:hover {
    background: rgba(148, 163, 184, 0.45);
  }
</style>
