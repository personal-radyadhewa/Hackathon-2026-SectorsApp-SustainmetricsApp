<script>
  import {
    Search,
    Star,
    Plus,
    Check,
    ArrowRight,
    TrendingUp,
    Shield,
    Leaf,
    DollarSign,
    Building2,
    Sparkles,
    Trash2,
    ExternalLink,
    Filter,
    RefreshCw,
    Loader2,
  } from '@lucide/svelte';
  import { IDX_EMITENTS, searchIdxTickers, getCompanyProfile } from '../idxTickers.js';
  import { t, currentLang } from '../i18n.js';

  let {
    watchlist = ['PGEO', 'ADRO', 'BBRI', 'BREN', 'BUMI'],
    audits = [],
    auditingTickers = new Set(),
    onSelectTicker,
    onToggleWatchlist,
    onRunAudit,
    onRefreshAudits,
  } = $props();

  let searchQuery = $state('');
  let activeTab = $state('watchlist'); // 'watchlist', 'all', 'leaders', 'energy', 'finance'
  let newTickerInput = $state('');
  let isAddInputFocused = $state(false);
  let addSuggestions = $derived(searchIdxTickers(newTickerInput, 8));

  function enhanceWithAudit(base) {
    if (!base) return null;
    const t = base.ticker;
    const matchingAudit = audits.find((a) => a.ticker === t);
    const isAuditing = auditingTickers ? auditingTickers.has(t) : false;

    if (matchingAudit && matchingAudit.executive_summary) {
      const snap = matchingAudit.financial_snapshot || {};
      const covVal = snap.capex_coverage_ratio !== undefined && snap.capex_coverage_ratio !== null
        ? Number(snap.capex_coverage_ratio)
        : (matchingAudit.viability_score ? matchingAudit.viability_score / 25 : null);

      let ocfStr = base.ocf;
      if (snap.operating_cash_flow !== undefined && snap.operating_cash_flow !== null) {
        const rawOcf = Number(snap.operating_cash_flow);
        if (Math.abs(rawOcf) >= 1e12) {
          ocfStr = `IDR ${(rawOcf / 1e12).toFixed(2)}T`;
        } else if (Math.abs(rawOcf) >= 1e9) {
          ocfStr = `IDR ${(rawOcf / 1e9).toFixed(1)}B`;
        } else {
          ocfStr = `IDR ${(rawOcf / 1e6).toFixed(0)}M`;
        }
      }

      return {
        ...base,
        isAudited: true,
        isAuditing,
        description: matchingAudit.executive_summary,
        grade: matchingAudit.quadrant?.includes('Q1') || matchingAudit.quadrant?.includes('STRONG')
          ? 'Grade A'
          : matchingAudit.quadrant?.includes('Q3') || matchingAudit.quadrant?.includes('KONVENSIONAL')
          ? 'Grade B+'
          : 'Grade B',
        gradeLabel: matchingAudit.quadrant_label || base.gradeLabel,
        coverageRatio: covVal !== null ? `${covVal.toFixed(2)}x` : base.coverageRatio,
        financialHealth: covVal !== null && covVal >= 1.5 ? 'Very Strong' : (covVal !== null && covVal >= 1.0 ? 'Self-Funded' : 'Leveraged / Debt Reliant'),
        ocf: ocfStr,
        ytdChange: matchingAudit.consistency_score ? `${matchingAudit.consistency_score.toFixed(0)}% TKBI` : base.ytdChange,
      };
    }

    return {
      ...base,
      isAudited: false,
      isAuditing,
    };
  }

  let filteredCompanies = $derived.by(() => {
    // When user types a query, search the entire 962 IDX universe from SectorsApp
    if (searchQuery.trim().length > 0) {
      return searchIdxTickers(searchQuery, 40).map(enhanceWithAudit).filter(Boolean);
    }

    // Default Tab: strictly focus on the user's watchlist to preserve tokens and focus
    if (activeTab === 'watchlist') {
      return watchlist
        .map((t) => {
          const base = getCompanyProfile(t);
          return enhanceWithAudit(base);
        })
        .filter(Boolean);
    }

    if (activeTab === 'leaders') {
      return IDX_EMITENTS.filter((item) => item.grade.includes('A')).map(enhanceWithAudit);
    }

    if (activeTab === 'energy') {
      return IDX_EMITENTS.filter(
        (item) => item.sector.toLowerCase().includes('energy') || item.sector.toLowerCase().includes('utilities')
      ).map(enhanceWithAudit);
    }

    if (activeTab === 'finance') {
      return IDX_EMITENTS.filter(
        (item) => item.sector.toLowerCase().includes('banking') || item.sector.toLowerCase().includes('debt')
      ).map(enhanceWithAudit);
    }

    return IDX_EMITENTS.map(enhanceWithAudit);
  });

  let watchlistStats = $derived.by(() => {
    let auditedCount = 0;
    for (const t of watchlist) {
      if (audits.some((a) => a.ticker === t && a.executive_summary)) {
        auditedCount++;
      }
    }
    return {
      total: watchlist.length,
      audited: auditedCount,
      pending: watchlist.length - auditedCount,
    };
  });

  let auditedWatchlistItems = $derived(
    audits.filter((a) => watchlist.includes(a.ticker) && a.consistency_score !== null && a.consistency_score !== undefined)
  );

  let avgWatchlistAlignment = $derived.by(() => {
    if (auditedWatchlistItems.length === 0) return null;
    const sum = auditedWatchlistItems.reduce((acc, a) => acc + (a.consistency_score || 0), 0);
    return (sum / auditedWatchlistItems.length).toFixed(1);
  });

  let avgWatchlistCoverage = $derived.by(() => {
    if (auditedWatchlistItems.length === 0) return null;
    const ratios = auditedWatchlistItems
      .map((a) => a.financial_snapshot?.capex_coverage_ratio ?? (a.viability_score ? a.viability_score / 25 : null))
      .filter((v) => v !== null && v !== undefined && !isNaN(v));
    if (ratios.length === 0) return null;
    return (ratios.reduce((acc, r) => acc + Number(r), 0) / ratios.length).toFixed(2);
  });

  let isAnyAuditing = $derived(auditingTickers && auditingTickers.size > 0);

  function handleAuditAllPending() {
    const unaudited = watchlist.filter((t) => !audits.some((a) => a.ticker === t && a.executive_summary));
    for (const t of unaudited) {
      onRunAudit?.(t);
    }
  }

  function handleAddCustom(e) {
    e.preventDefault();
    const clean = newTickerInput.trim().toUpperCase();
    if (clean) {
      if (!watchlist.includes(clean)) {
        onToggleWatchlist(clean);
      }
      newTickerInput = '';
      isAddInputFocused = false;
    }
  }

  function handleAddSuggestion(ticker) {
    const clean = ticker.toUpperCase();
    if (!watchlist.includes(clean)) {
      onToggleWatchlist(clean);
    }
    newTickerInput = '';
    isAddInputFocused = false;
  }
</script>

<div class="space-y-6">
  <!-- Top IDX Green Watchlist Header & Market Pulse Banner -->
  <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-4">
    <div class="flex flex-col gap-1.5">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 dark:bg-[#162032] text-slate-700 dark:text-slate-300 w-fit font-mono text-[11px] font-semibold uppercase tracking-wider border border-slate-200 dark:border-slate-800">
        <Sparkles size={14} class="text-[#047857] dark:text-[#34D399]" />
        <span>{$t.appName}</span>
      </div>
      <h1 class="text-2xl md:text-3xl font-headline font-bold text-slate-900 dark:text-slate-100 tracking-tight">
        {$t.watchlistHeader}
      </h1>
      <p class="font-body text-xs md:text-sm text-slate-500 dark:text-slate-400 max-w-2xl">
        {$t.watchlistSub}
      </p>
    </div>

    <!-- Quick Add Form with Autocomplete Dropdown & Sync Button -->
    <div class="relative self-start lg:self-auto flex items-center gap-2">
      <form onsubmit={handleAddCustom} class="flex items-center gap-2">
        <div class="relative">
          <input
            type="text"
            bind:value={newTickerInput}
            onfocus={() => (isAddInputFocused = true)}
            placeholder={$t.addCompanyPlaceholder}
            class="bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-xs font-mono text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none uppercase focus:border-[#047857] w-60 shadow-2xs"
          />
        </div>
        <button
          type="submit"
          class="px-4 py-2 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-semibold text-xs transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer"
        >
          <Plus size={14} />
          <span>{$t.add}</span>
        </button>
      </form>

      <button
        type="button"
        onclick={() => onRefreshAudits?.()}
        class="px-3 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#162032] dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 font-mono text-xs font-semibold flex items-center gap-1.5 border border-slate-200 dark:border-slate-800 cursor-pointer transition-colors shadow-2xs"
        title="Sync"
      >
        <RefreshCw size={13} class={isAnyAuditing ? 'animate-spin text-[#047857] dark:text-[#34D399]' : ''} />
        <span class="hidden sm:inline">Sync</span>
      </button>

      <!-- Autocomplete Dropdown for Watchlist Add -->
      {#if isAddInputFocused && newTickerInput.trim().length > 0}
        <div
          class="absolute left-0 right-0 top-full mt-1.5 bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl z-50 overflow-hidden divide-y divide-slate-100 dark:divide-slate-800 text-xs"
        >
          <div class="px-3 py-1.5 bg-slate-50 dark:bg-[#162032] flex items-center justify-between text-[10px] font-mono text-slate-400">
            <span>{$t.availableCodes}</span>
            <button
              type="button"
              onclick={() => (isAddInputFocused = false)}
              class="hover:text-slate-700 dark:hover:text-slate-200 cursor-pointer text-xs"
            >
              ✕
            </button>
          </div>

          {#if addSuggestions.length > 0}
            <div class="max-h-56 overflow-y-auto divide-y divide-slate-50 dark:divide-slate-800/60">
              {#each addSuggestions as s}
                {@const inWatch = watchlist.includes(s.ticker)}
                <button
                  type="button"
                  onclick={() => handleAddSuggestion(s.ticker)}
                  class="w-full text-left px-3 py-2 hover:bg-slate-50 dark:hover:bg-[#162032] flex items-center justify-between gap-2 transition-colors cursor-pointer"
                >
                  <div class="flex items-center gap-2.5 min-w-0">
                    <span class="font-mono font-bold text-xs text-slate-900 dark:text-slate-100 px-2 py-0.5 rounded bg-slate-100 dark:bg-[#1E293B]">
                      {s.ticker}
                    </span>
                    <div class="truncate">
                      <div class="text-xs font-semibold text-slate-800 dark:text-slate-200 truncate">{s.name}</div>
                      <div class="text-[10px] text-slate-400 truncate">{s.sector} • <span class="font-mono font-medium">{s.grade}</span></div>
                    </div>
                  </div>
                  <div class="shrink-0">
                    {#if inWatch}
                      <span class="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 font-semibold px-2 py-0.5 rounded bg-emerald-50 dark:bg-emerald-950/60">In Watchlist</span>
                    {:else}
                      <span class="text-[10px] font-mono text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded font-medium hover:bg-emerald-100 dark:hover:bg-emerald-900">+ Add to Watchlist</span>
                    {/if}
                  </div>
                </button>
              {/each}
            </div>
          {/if}

          <!-- Direct Custom Add Option -->
          <button
            type="button"
            onclick={() => handleAddSuggestion(newTickerInput)}
            class="w-full text-left px-3 py-2.5 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 text-[#047857] dark:text-[#34D399] font-mono text-xs flex items-center gap-2 cursor-pointer font-medium"
          >
            <Plus size={14} />
            <span>Add Custom IDX Ticker: <strong>{newTickerInput.trim().toUpperCase()}</strong></span>
          </button>
        </div>
      {/if}
    </div>
  </div>

  <!-- 4 Market Pulse Cards (100% Real Live Computed Watchlist Metrics) -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
    <div class="p-4 rounded-xl bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between text-[11px] font-mono text-slate-400 uppercase">
        <span>{$t.savedCompaniesCard}</span>
        <span class="w-2 h-2 rounded-full bg-[#047857] dark:bg-[#34D399]"></span>
      </div>
      <div class="mt-2 font-headline text-2xl font-bold text-slate-900 dark:text-slate-100">
        {watchlist.length} <span class="text-xs font-normal text-slate-400">{watchlist.length === 1 ? 'Emitent' : 'Emitents'}</span>
      </div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">{$t.savedCompaniesSub}</p>
    </div>

    <div class="p-4 rounded-xl bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between text-[11px] font-mono text-slate-400 uppercase">
        <span>{$t.greenAlignmentCard}</span>
        <span class="w-2 h-2 rounded-full bg-[#1D4ED8] dark:bg-[#60A5FA]"></span>
      </div>
      <div class="mt-2 font-headline text-2xl font-bold text-slate-900 dark:text-slate-100">
        {#if avgWatchlistAlignment !== null}
          {avgWatchlistAlignment}% <span class="text-xs font-normal text-[#047857] dark:text-[#34D399] font-mono">({auditedWatchlistItems.length}/{watchlist.length})</span>
        {:else}
          <span class="text-lg font-mono text-slate-400">-</span>
        {/if}
      </div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">{$t.greenAlignmentSub}</p>
    </div>

    <div class="p-4 rounded-xl bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between text-[11px] font-mono text-slate-400 uppercase">
        <span>{$t.cashCushionCard}</span>
        <span class="w-2 h-2 rounded-full bg-[#D97706] dark:bg-[#FBBF24]"></span>
      </div>
      <div class="mt-2 font-headline text-2xl font-bold text-slate-900 dark:text-slate-100">
        {#if avgWatchlistCoverage !== null}
          {avgWatchlistCoverage}x <span class="text-xs font-normal font-mono {parseFloat(avgWatchlistCoverage) >= 1.0 ? 'text-[#047857] dark:text-[#34D399]' : 'text-amber-600 dark:text-amber-400'}">({parseFloat(avgWatchlistCoverage) >= 1.0 ? $t.selfFunded : $t.leveraged})</span>
        {:else}
          <span class="text-lg font-mono text-slate-400">-</span>
        {/if}
      </div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">{$t.cashCushionSub}</p>
    </div>

    <div class="p-4 rounded-xl bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between text-[11px] font-mono text-slate-400 uppercase">
        <span>{$t.standardCard}</span>
        <span class="w-2 h-2 rounded-full bg-[#047857] dark:bg-[#34D399]"></span>
      </div>
      <div class="mt-2 font-headline text-2xl font-bold text-[#047857] dark:text-[#34D399]">
        OJK TKBI <span class="text-xs font-normal text-slate-400 font-mono">v3.0</span>
      </div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">{$t.standardSub}</p>
    </div>
  </div>

  <!-- Guidance Callout: Direct User to Run AI Audit for Unaudited Watchlist Emitents -->
  {#if activeTab === 'watchlist' && watchlistStats.pending > 0}
    <div class="p-4 rounded-xl bg-emerald-50/80 dark:bg-[#112028] border border-emerald-200/90 dark:border-emerald-800/80 flex flex-col md:flex-row md:items-center justify-between gap-3.5 text-xs shadow-2xs">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-emerald-100 dark:bg-emerald-950/80 text-[#047857] dark:text-[#34D399] flex items-center justify-center shrink-0">
          <Sparkles size={17} />
        </div>
        <div>
          <div class="font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <span>{watchlistStats.pending} {$t.readyForAuditTitle}</span>
          </div>
          <div class="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5">
            {$t.readyForAuditDesc}
          </div>
        </div>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <button
          type="button"
          onclick={handleAuditAllPending}
          disabled={isAnyAuditing}
          class="px-4 py-2 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-semibold text-xs transition-colors flex items-center gap-1.5 cursor-pointer shadow-xs disabled:opacity-50"
        >
          {#if isAnyAuditing}
            <Loader2 size={13} class="animate-spin" />
            <span>{$t.auditing}...</span>
          {:else}
            <Sparkles size={13} />
            <span>{$t.auditAll} ({watchlistStats.pending})</span>
          {/if}
        </button>
      </div>
    </div>
  {/if}

  <!-- Search & Category Tabs Bar -->
  <div class="p-5 rounded-xl bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-4">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
      <!-- Search Input -->
      <div class="relative w-full md:w-96">
        <Search size={15} class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
        <input
          type="text"
          bind:value={searchQuery}
          placeholder={$t.searchWatchlist}
          class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-[#047857]"
        />
      </div>

      <!-- Tab Category Filters -->
      <div class="flex flex-wrap items-center gap-1.5">
        {#each [
          { id: 'watchlist', label: `⭐ ${$t.watchlist} (${watchlist.length})` },
          { id: 'all', label: $t.allIdxDatabase },
          { id: 'leaders', label: `🌿 ${$t.topGreenLeaders}` },
          { id: 'energy', label: `⚡ ${$t.energySector}` },
          { id: 'finance', label: `🏦 ${$t.financeSector}` },
        ] as tab}
          <button
            type="button"
            onclick={() => (activeTab = tab.id)}
            class="px-3 py-1.5 rounded-full text-xs font-medium transition-all cursor-pointer {activeTab === tab.id
              ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] font-semibold shadow-xs'
              : 'bg-slate-100 dark:bg-[#162032] text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800'}"
          >
            {tab.label}
          </button>
        {/each}
      </div>
    </div>

    <!-- IDX Green Company Screener Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse text-xs">
        <thead class="bg-slate-50/80 dark:bg-[#162032]/80 text-slate-500 dark:text-slate-400 font-mono text-[10px] uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
          <tr>
            <th class="py-3 px-4 w-12 text-center">⭐</th>
            <th class="py-3 px-4 w-64">{$currentLang === 'id' ? 'Perusahaan & Kode' : 'Company & Code'}</th>
            <th class="py-3 px-4 w-44">{$currentLang === 'id' ? 'Status Kategori Hijau' : 'Green Category Status'}</th>
            <th class="py-3 px-4 min-w-[240px]">{$currentLang === 'id' ? 'Ringkasan & Temuan AI' : 'AI Summary & Key Takeaway'}</th>
            <th class="py-3 px-4 w-36">{$currentLang === 'id' ? 'Kekuatan Finansial' : 'Financial Strength'}</th>
            <th class="py-3 px-4 w-28 text-right">{$currentLang === 'id' ? 'Kas Usaha' : 'Operating Cash'}</th>
            <th class="py-3 px-4 w-32 text-center">{$t.actions}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-800/80 text-slate-700 dark:text-slate-300">
          {#if filteredCompanies.length === 0}
            <tr>
              <td colspan="7" class="text-center py-16 text-slate-400 dark:text-slate-500 text-xs font-mono">
                {$currentLang === 'id' ? 'Tidak ada perusahaan yang cocok dengan pencarian Anda.' : 'No companies matched your active filter or search query.'}
              </td>
            </tr>
          {/if}

          {#each filteredCompanies as company}
            {@const isWatchlisted = watchlist.includes(company.ticker)}

            <tr class="hover:bg-slate-50/80 dark:hover:bg-[#162032]/50 transition-colors">
              <!-- Star Toggle -->
              <td class="py-3 px-4 text-center">
                <button
                  type="button"
                  onclick={() => onToggleWatchlist(company.ticker)}
                  class="p-1 rounded-md text-slate-400 hover:text-amber-500 transition-colors cursor-pointer"
                  title={isWatchlisted ? `${$t.remove} ${company.ticker}` : `${$t.add} ${company.ticker}`}
                >
                  <Star
                    size={16}
                    class={isWatchlisted ? 'fill-amber-400 text-amber-400' : 'text-slate-300 dark:text-slate-600 hover:text-amber-400'}
                  />
                </button>
              </td>

              <!-- Company & Ticker -->
              <td class="py-3 px-4">
                <div class="flex items-center space-x-3">
                  <div class="w-9 h-9 rounded-lg bg-slate-100 dark:bg-[#162032] border border-slate-200/80 dark:border-slate-700 flex items-center justify-center font-mono font-bold text-xs text-[#047857] dark:text-[#34D399] shrink-0">
                    {company.ticker.slice(0, 3)}
                  </div>
                  <div>
                    <div class="font-headline font-bold text-sm text-slate-900 dark:text-slate-100 flex items-center gap-1.5">
                      <span>{company.ticker}</span>
                      <span class="text-[10px] font-mono font-normal text-slate-400">:IDX</span>
                    </div>
                    <div class="text-[11px] text-slate-500 dark:text-slate-400 truncate max-w-[200px]" title={company.name}>
                      {company.name}
                    </div>
                    <div class="text-[10px] text-slate-400 font-mono mt-0.5">
                      {company.sector}
                    </div>
                  </div>
                </div>
              </td>

              <!-- Green Compliance Grade -->
              <td class="py-3 px-4 whitespace-nowrap">
                {#if company.isAuditing}
                  <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-mono font-bold border bg-emerald-50 text-[#047857] border-emerald-200 dark:bg-emerald-950/60 dark:text-[#34D399] dark:border-emerald-800 animate-pulse">
                    <Loader2 size={11} class="animate-spin" />
                    <span>{$t.auditing}...</span>
                  </span>
                {:else if !company.isAudited}
                  <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-mono font-bold border bg-amber-50 text-amber-800 border-amber-200 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800">
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                    <span>{$t.statusPending}</span>
                  </span>
                {:else}
                  <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-mono font-bold border {company.statusClass}">
                    <span class="w-1.5 h-1.5 rounded-full {company.dotColor}"></span>
                    <span>{company.grade} • {company.gradeLabel}</span>
                  </span>
                {/if}
              </td>

              <!-- Audit Takeaway -->
              <td class="py-3 px-4">
                {#if company.isAuditing}
                  <div class="flex items-center gap-2 text-xs text-[#047857] dark:text-[#34D399] font-mono py-1">
                    <Loader2 size={13} class="animate-spin shrink-0" />
                    <span class="truncate">{$t.auditing}...</span>
                  </div>
                {:else if !company.isAudited}
                  <div class="flex items-center gap-2.5">
                    <button
                      type="button"
                      onclick={() => onRunAudit?.(company.ticker)}
                      class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-mono font-bold text-[11px] shadow-2xs hover:shadow transition-all cursor-pointer group shrink-0"
                    >
                      <Sparkles size={12} class="group-hover:rotate-12 transition-transform" />
                      <span>{$t.runAiAudit}</span>
                    </button>
                    <span class="text-[11px] text-slate-500 dark:text-slate-400 font-body">
                      {$currentLang === 'id' ? 'Klik untuk cek status ramah lingkungan & temuan utama' : 'Click to check green status and AI summary'}
                    </span>
                  </div>
                {:else}
                  <p class="text-xs font-body text-slate-600 dark:text-slate-300 leading-snug">
                    {company.description}
                  </p>
                {/if}
              </td>

              <!-- Financial Health -->
              <td class="py-3 px-4 whitespace-nowrap">
                <div class="flex flex-col">
                  <span class="font-semibold text-slate-900 dark:text-slate-100">{company.financialHealth}</span>
                  <span class="text-[10px] font-mono text-slate-500 mt-0.5">Coverage: {company.coverageRatio}</span>
                </div>
              </td>

              <!-- Cash Flow -->
              <td class="py-3 px-4 text-right whitespace-nowrap font-mono">
                <span class="font-bold text-slate-900 dark:text-slate-100">{company.ocf}</span>
                <div class="text-[10px] font-semibold text-[#047857] dark:text-[#34D399]">{company.ytdChange} YTD</div>
              </td>

              <!-- Action: Open Audit -->
              <td class="py-3 px-4 text-center whitespace-nowrap">
                <div class="flex items-center justify-center gap-1.5">
                  {#if !company.isAudited && !company.isAuditing}
                    <button
                      type="button"
                      onclick={() => onRunAudit?.(company.ticker)}
                      class="px-2.5 py-1.5 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-semibold text-xs transition-colors shadow-2xs flex items-center gap-1 cursor-pointer"
                      title="Run AI audit for {company.ticker}"
                    >
                      <Sparkles size={12} />
                      <span>Audit</span>
                    </button>
                  {/if}
                  <button
                    type="button"
                    onclick={() => onSelectTicker(company.ticker)}
                    class="px-3 py-1.5 rounded-lg {company.isAudited ? 'bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B]' : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700'} font-semibold text-xs transition-colors shadow-2xs flex items-center gap-1 cursor-pointer"
                  >
                    <span>{$t.openProfile}</span>
                    <ArrowRight size={13} />
                  </button>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>
