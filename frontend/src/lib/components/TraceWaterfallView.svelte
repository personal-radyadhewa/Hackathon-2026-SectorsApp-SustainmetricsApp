<script>
  import { Activity, Clock, CheckCircle, AlertTriangle, ArrowRight, Database, Cpu, Layers } from '@lucide/svelte';

  let {
    auditRun = null,
    traces = [],
  } = $props();

  let selectedSpan = $state(null);

  // Compute maximum duration for timeline scaling
  let maxDuration = $derived(
    traces.length > 0 ? Math.max(...traces.map((s) => s.duration_ms || 1)) : 100
  );

  function getSpanIcon(name) {
    if (name.includes('sectors')) return Database;
    if (name.includes('vector')) return Layers;
    if (name.includes('scoring')) return Cpu;
    return Activity;
  }
</script>

<div class="space-y-6">
  <!-- Trace Overview Header -->
  <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
      <div>
        <div class="flex items-center space-x-2 mb-1">
          <Activity size={18} class="text-blue-400" />
          <h2 class="text-base font-bold text-slate-900">OpenTelemetry Audit Trace Waterfall</h2>
        </div>
        <p class="text-xs text-slate-500">
          Trace ID: <span class="font-mono text-emerald-400 font-semibold">{auditRun?.trace_id || 'N/A'}</span>
          • Total Spans: <span class="font-mono text-slate-800">{traces.length}</span>
        </p>
      </div>

      <div class="flex items-center space-x-3 text-xs font-mono">
        <span class="px-2.5 py-1 rounded bg-white border border-slate-200 text-slate-700">
          Service: <span class="text-emerald-400">sustainmetric</span>
        </span>
        <span class="px-2.5 py-1 rounded bg-white border border-slate-200 text-slate-700">
          Instrumented: <span class="text-blue-400">Otel Python SDK</span>
        </span>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Spans Waterfall Timeline (2 Columns) -->
    <div class="lg:col-span-2 bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
      <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-4 flex items-center justify-between">
        <span>Execution DAG & Span Waterfall</span>
        <span class="text-[11px] font-normal text-slate-400 font-mono">Normalized Duration (ms)</span>
      </h3>

      {#if traces.length === 0}
        <div class="text-center py-12 text-slate-400 text-xs">
          No trace telemetry spans captured yet. Execute a green audit to stream traces.
        </div>
      {/if}

      <div class="space-y-2.5">
        {#each traces as span}
          {@const Icon = getSpanIcon(span.name)}
          {@const isSelected = selectedSpan?.id === span.id}
          {@const barWidthPct = Math.max(12, Math.min(100, (span.duration_ms / maxDuration) * 100))}
          {@const isRoot = !span.parent_span_id}

          <div
            onclick={() => (selectedSpan = span)}
            onkeydown={(e) => e.key === 'Enter' && (selectedSpan = span)}
            role="button"
            tabindex="0"
            class="p-3 rounded-lg border transition-all cursor-pointer {isSelected
              ? 'bg-slate-100 border-emerald-500/50 shadow-md'
              : 'bg-slate-50 border-slate-200 hover:bg-slate-100'}"
          >
            <div class="flex items-center justify-between mb-1.5">
              <div class="flex items-center space-x-2.5">
                <div class="w-6 h-6 rounded bg-slate-100 flex items-center justify-center text-slate-700">
                  <Icon size={13} />
                </div>
                <div>
                  <span class="text-xs font-mono font-bold {isRoot ? 'text-emerald-400' : 'text-slate-800'}">
                    {span.name}
                  </span>
                  <span class="text-[10px] text-slate-400 font-mono ml-2">ID: {span.span_id.slice(0, 8)}</span>
                </div>
              </div>

              <div class="flex items-center space-x-2 text-xs font-mono">
                <span class="text-slate-700 font-bold">{span.duration_ms.toFixed(1)} ms</span>
                <span class="px-1.5 py-0.5 rounded text-[9px] font-bold {span.status === 'OK' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}">
                  {span.status}
                </span>
              </div>
            </div>

            <!-- Latency Bar Visualization -->
            <div class="w-full bg-slate-50 h-2 rounded-full overflow-hidden mt-2">
              <div
                class="h-full rounded-full {isRoot ? 'bg-emerald-500' : 'bg-blue-500'} transition-all duration-300"
                style="width: {barWidthPct}%;"
              ></div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Span Details Inspector (1 Column) -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm h-fit">
      <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 flex items-center justify-between">
        <span>Span Inspector</span>
        {#if selectedSpan}
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-mono">
            {selectedSpan.status}
          </span>
        {/if}
      </h3>

      {#if selectedSpan}
        <div class="space-y-3 text-xs">
          <div>
            <span class="text-[10px] uppercase font-semibold text-slate-400 block mb-0.5">Span Name</span>
            <div class="p-2 rounded bg-slate-50 border border-slate-200 font-mono text-emerald-400 font-bold">
              {selectedSpan.name}
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <span class="text-[10px] uppercase font-semibold text-slate-400 block mb-0.5">Latency</span>
              <div class="p-2 rounded bg-slate-50 border border-slate-200 font-mono text-slate-800">
                {selectedSpan.duration_ms.toFixed(2)} ms
              </div>
            </div>
            <div>
              <span class="text-[10px] uppercase font-semibold text-slate-400 block mb-0.5">Service</span>
              <div class="p-2 rounded bg-slate-50 border border-slate-200 font-mono text-slate-800">
                {selectedSpan.service_name}
              </div>
            </div>
          </div>

          <div>
            <span class="text-[10px] uppercase font-semibold text-slate-400 block mb-0.5">Trace Context</span>
            <div class="p-2 rounded bg-slate-50 border border-slate-200 font-mono text-[10px] text-slate-700 space-y-1">
              <div>Trace ID: <span class="text-slate-500">{selectedSpan.trace_id}</span></div>
              <div>Span ID: <span class="text-slate-500">{selectedSpan.span_id}</span></div>
              <div>Parent ID: <span class="text-slate-500">{selectedSpan.parent_span_id || 'None (Root Span)'}</span></div>
            </div>
          </div>

          <div>
            <span class="text-[10px] uppercase font-semibold text-slate-400 block mb-0.5">Recorded Attributes (Metadata)</span>
            <div class="p-2.5 rounded bg-slate-50 border border-slate-200 font-mono text-[11px] text-slate-700 max-h-48 overflow-y-auto">
              {#if selectedSpan.attributes && Object.keys(selectedSpan.attributes).length > 0}
                <ul class="space-y-1">
                  {#each Object.entries(selectedSpan.attributes) as [key, val]}
                    <li class="flex flex-col">
                      <span class="text-slate-400 text-[10px]">{key}:</span>
                      <span class="text-emerald-300 font-semibold">{val}</span>
                    </li>
                  {/each}
                </ul>
              {:else}
                <span class="text-slate-400 italic">No attributes recorded on this span.</span>
              {/if}
            </div>
          </div>
        </div>
      {:else}
        <div class="text-center py-16 text-slate-400 text-xs">
          Select any span node from the timeline to view its runtime parameters and cache telemetry.
        </div>
      {/if}
    </div>
  </div>
</div>
