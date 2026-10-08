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
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2.5 mb-1.5">
          <Activity size={18} class="text-[#047857] dark:text-[#34D399]" />
          <h2 class="text-base font-headline font-bold text-slate-900 dark:text-slate-100">Audit Process &amp; Activity Log</h2>
        </div>
        <p class="text-xs font-body text-slate-500 dark:text-slate-400">
          Transparent step-by-step history showing how data was retrieved and analyzed.
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-2 text-xs font-mono">
        <span class="px-3 py-1.5 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-medium">
          Total Steps: <strong class="text-slate-900 dark:text-slate-100">{traces.length}</strong>
        </span>
        <span class="px-3 py-1.5 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-medium">
          Total Latency: <strong class="text-[#047857] dark:text-[#34D399] tabular-nums">{totalDuration.toFixed(0)} ms</strong>
        </span>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Steps Timeline (2 Columns) -->
    <div class="lg:col-span-2 bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
      <h3 class="text-xs font-mono font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-4 flex items-center justify-between">
        <span>Execution Timeline</span>
        <span class="text-xs font-normal text-slate-400 font-sans">Click step to inspect telemetry</span>
      </h3>

      {#if traces.length === 0}
        <div class="text-center py-14 text-slate-400 dark:text-slate-500 text-xs font-mono">
          No audit activity captured yet. Click "Audit Now" to run the audit pipeline.
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
              ? 'bg-slate-50 dark:bg-[#162032] border-[#047857] dark:border-[#34D399] shadow-xs'
              : 'bg-white dark:bg-[#0F172A] border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'}"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-3">
                <div class="w-7 h-7 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-[#047857] dark:text-[#34D399] shrink-0">
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

              <div class="flex items-center space-x-2 text-xs font-mono">
                <span class="text-slate-600 dark:text-slate-400 text-[11px] tabular-nums">{span.duration_ms.toFixed(1)} ms</span>
                <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold border {span.status === 'OK' ? 'badge-hijau' : 'badge-tidak'}">
                  <span class="w-1.5 h-1.5 rounded-full {span.status === 'OK' ? 'bg-[#047857] dark:bg-[#34D399]' : 'bg-[#DC2626] dark:bg-[#F87171]'}"></span>
                  <span>{span.status === 'OK' ? 'Completed' : 'Error'}</span>
                </span>
              </div>
            </div>

            <!-- Progress Bar Representation -->
            <div class="w-full bg-slate-100 dark:bg-[#162032] h-1.5 rounded-full overflow-hidden mt-3">
              <div
                class="h-full rounded-full bg-[#047857] dark:bg-[#34D399] transition-all duration-300"
                style="width: {barWidthPct}%;"
              ></div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Step Details Inspector (1 Column) -->
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm h-fit">
      <h3 class="text-xs font-mono font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-4 flex items-center justify-between">
        <span>Step Inspector</span>
        {#if selectedSpan}
          <span class="text-[10px] px-2.5 py-0.5 rounded-full font-mono font-bold border {selectedSpan.status === 'OK' ? 'badge-hijau' : 'badge-tidak'}">
            {selectedSpan.status === 'OK' ? 'Success' : 'Failed'}
          </span>
        {/if}
      </h3>

      {#if selectedSpan}
        {@const stepInfo = getStepFriendlyInfo(selectedSpan.name)}
        <div class="space-y-4 text-xs">
          <div>
            <span class="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1">Action Name</span>
            <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 font-semibold text-slate-900 dark:text-slate-100 font-mono">
              {stepInfo.title}
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <span class="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1">Duration</span>
              <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 font-mono text-slate-800 dark:text-slate-200 tabular-nums">
                {selectedSpan.duration_ms.toFixed(1)} ms
              </div>
            </div>
            <div>
              <span class="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1">Status</span>
              <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 text-[#047857] dark:text-[#34D399] font-mono font-medium">
                {selectedSpan.status === 'OK' ? 'Verified OK' : 'Failed'}
              </div>
            </div>
          </div>

          <div>
            <span class="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1">Parameters &amp; Metadata</span>
            <div class="p-3 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 text-[11px] max-h-48 overflow-y-auto font-mono">
              {#if selectedSpan.attributes && Object.keys(selectedSpan.attributes).length > 0}
                <ul class="space-y-2">
                  {#each Object.entries(selectedSpan.attributes) as [key, val]}
                    <li class="flex flex-col">
                      <span class="text-slate-500 dark:text-slate-400 text-[10px]">{key}</span>
                      <span class="text-slate-900 dark:text-slate-100 font-medium break-all">{val}</span>
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
