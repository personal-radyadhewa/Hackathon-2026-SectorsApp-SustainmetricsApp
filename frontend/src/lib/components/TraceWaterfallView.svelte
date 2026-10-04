<script>
  import {
    Activity,
    Clock,
    CheckCircle,
    AlertTriangle,
    ArrowRight,
    Database,
    Cpu,
    Layers,
    FileCheck2,
    SearchCheck,
    CheckCircle2,
  } from '@lucide/svelte';

  let {
    auditRun = null,
    traces = [],
  } = $props();

  let selectedSpan = $state(null);

  // Compute maximum duration for timeline scaling
  let maxDuration = $derived(
    traces.length > 0 ? Math.max(...traces.map((s) => s.duration_ms || 1)) : 100
  );

  let totalDuration = $derived(
    traces.reduce((acc, curr) => acc + (curr.duration_ms || 0), 0)
  );

  function getStepFriendlyInfo(name) {
    if (name.includes('sectors')) {
      return {
        title: 'Retrieve Financial & Company Data',
        desc: 'Loaded audited financial filings and capital expenditure figures.',
        icon: Database,
      };
    }
    if (name.includes('vector') || name.includes('search')) {
      return {
        title: 'Query Green Taxonomy Criteria',
        desc: 'Searched OJK 2024 environmental criteria and requirements.',
        icon: SearchCheck,
      };
    }
    if (name.includes('scoring') || name.includes('consistency')) {
      return {
        title: 'Evaluate Alignment & Matrix Score',
        desc: 'Evaluated qualitative disclosure claims against actual capital expenditures.',
        icon: Cpu,
      };
    }
    return {
      title: name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
      desc: 'Executed pipeline audit step.',
      icon: Activity,
    };
  }
</script>

<div class="space-y-6">
  <!-- Audit Activity Header -->
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-xs">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 mb-1.5">
          <Activity size={18} class="text-emerald-500" />
          <h2 class="text-base font-semibold text-slate-900 dark:text-slate-100">Audit Process & Activity Log</h2>
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400">
          Transparent step-by-step history showing how data was retrieved and analyzed.
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-2 text-xs">
        <span class="px-3 py-1.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-medium">
          Total Steps: <strong class="text-slate-900 dark:text-slate-100">{traces.length}</strong>
        </span>
        <span class="px-3 py-1.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-medium">
          Total Time: <strong class="text-slate-900 dark:text-slate-100 font-mono">{totalDuration.toFixed(0)} ms</strong>
        </span>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Steps Timeline (2 Columns) -->
    <div class="lg:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-xs">
      <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-4 flex items-center justify-between">
        <span>Execution Timeline</span>
        <span class="text-[11px] font-normal text-slate-400 font-sans">Click any step to inspect</span>
      </h3>

      {#if traces.length === 0}
        <div class="text-center py-14 text-slate-400 dark:text-slate-500 text-xs">
          No audit activity captured yet. Click "Analyze" on a company to run the audit pipeline.
        </div>
      {/if}

      <div class="space-y-3">
        {#each traces as span, index}
          {@const stepInfo = getStepFriendlyInfo(span.name)}
          {@const Icon = stepInfo.icon}
          {@const isSelected = selectedSpan?.id === span.id}
          {@const barWidthPct = Math.max(15, Math.min(100, (span.duration_ms / maxDuration) * 100))}

          <div
            onclick={() => (selectedSpan = span)}
            onkeydown={(e) => e.key === 'Enter' && (selectedSpan = span)}
            role="button"
            tabindex="0"
            class="p-4 rounded-xl border transition-all cursor-pointer {isSelected
              ? 'bg-slate-50 dark:bg-slate-800 border-emerald-500 shadow-xs ring-1 ring-emerald-500/30'
              : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'}"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-3">
                <div class="w-7 h-7 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-emerald-600 dark:text-emerald-400 shrink-0">
                  <Icon size={14} />
                </div>
                <div>
                  <div class="text-xs font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                    <span>{stepInfo.title}</span>
                    <span class="text-[10px] text-slate-400 font-mono font-normal">Step {index + 1}</span>
                  </div>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">{stepInfo.desc}</p>
                </div>
              </div>

              <div class="flex items-center space-x-2 text-xs">
                <span class="font-mono text-slate-600 dark:text-slate-400 text-[11px]">{span.duration_ms.toFixed(1)} ms</span>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-medium {span.status === 'OK' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800' : 'bg-rose-50 text-rose-700 dark:bg-rose-950/50 dark:text-rose-300 border border-rose-200 dark:border-rose-800'}">
                  {span.status === 'OK' ? 'Completed' : 'Error'}
                </span>
              </div>
            </div>

            <!-- Progress Bar Representation -->
            <div class="w-full bg-slate-100 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden mt-3">
              <div
                class="h-full rounded-full bg-emerald-500 transition-all duration-300"
                style="width: {barWidthPct}%;"
              ></div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Step Details Inspector (1 Column) -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-xs h-fit">
      <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-4 flex items-center justify-between">
        <span>Step Inspector</span>
        {#if selectedSpan}
          <span class="text-[10px] px-2 py-0.5 rounded-full font-medium {selectedSpan.status === 'OK' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300' : 'bg-rose-50 text-rose-700'}">
            {selectedSpan.status === 'OK' ? 'Success' : 'Failed'}
          </span>
        {/if}
      </h3>

      {#if selectedSpan}
        {@const stepInfo = getStepFriendlyInfo(selectedSpan.name)}
        <div class="space-y-4 text-xs">
          <div>
            <span class="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1">Action Name</span>
            <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 font-semibold text-slate-900 dark:text-slate-100">
              {stepInfo.title}
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <span class="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1">Duration</span>
              <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 font-mono text-slate-800 dark:text-slate-200">
                {selectedSpan.duration_ms.toFixed(1)} ms
              </div>
            </div>
            <div>
              <span class="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1">Status</span>
              <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-emerald-600 dark:text-emerald-400 font-medium">
                {selectedSpan.status === 'OK' ? 'Verified OK' : 'Failed'}
              </div>
            </div>
          </div>

          <div>
            <span class="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1">Parameters & Metadata</span>
            <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-[11px] max-h-48 overflow-y-auto">
              {#if selectedSpan.attributes && Object.keys(selectedSpan.attributes).length > 0}
                <ul class="space-y-2">
                  {#each Object.entries(selectedSpan.attributes) as [key, val]}
                    <li class="flex flex-col">
                      <span class="text-slate-500 dark:text-slate-400 text-[10px] font-medium">{key}</span>
                      <span class="text-slate-900 dark:text-slate-100 font-mono text-[11px] font-medium break-all">{val}</span>
                    </li>
                  {/each}
                </ul>
              {:else}
                <span class="text-slate-400 italic">No extra metadata required for this step.</span>
              {/if}
            </div>
          </div>
        </div>
      {:else}
        <div class="text-center py-16 text-slate-400 dark:text-slate-500 text-xs">
          Select any step from the timeline to see details and runtime parameters.
        </div>
      {/if}
    </div>
  </div>
</div>
