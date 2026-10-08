<script>
  import { Clock, Plus, Trash2, Play, Calendar, AlertCircle, CheckCircle2, X } from '@lucide/svelte';
  import { createSchedule, deleteSchedule, triggerAudit } from '../api.js';

  let {
    schedules = [],
    onReloadSchedules,
  } = $props();

  let showModal = $state(false);
  let name = $state('');
  let cronExpr = $state('0 8 * * 1');
  let tickersText = $state('PGEO, ADRO, BBRI');
  let alertScore = $state(50.0);
  let isSubmitting = $state(false);

  function applyPreset(presetExpr) {
    cronExpr = presetExpr;
  }

  function getReadableFrequency(expr) {
    if (expr === '0 8 * * 1') return 'Every Monday at 08:00 WIB';
    if (expr === '0 0 * * *') return 'Daily at 00:00 WIB';
    if (expr === '0 0 1 * *') return 'Monthly (1st of month)';
    return expr;
  }

  async function handleCreate(e) {
    e.preventDefault();
    if (!name.trim()) return;

    const tickersList = tickersText
      .split(',')
      .map((t) => t.trim().toUpperCase())
      .filter(Boolean);

    if (tickersList.length === 0) {
      alert('Please specify at least one emitent stock code.');
      return;
    }

    isSubmitting = true;
    try {
      await createSchedule({
        name: name.trim(),
        cron_expression: cronExpr.trim(),
        tickers: tickersList,
        alert_threshold_score: alertScore,
      });
      showModal = false;
      name = '';
      tickersText = 'PGEO, ADRO, BBRI';
      onReloadSchedules();
    } catch (err) {
      alert(`Failed to create schedule: ${err.message}`);
    } finally {
      isSubmitting = false;
    }
  }

  async function handleDelete(id) {
    if (!confirm('Are you sure you want to delete this scheduled check?')) return;
    try {
      await deleteSchedule(id);
      onReloadSchedules();
    } catch (err) {
      alert(`Failed to delete schedule: ${err.message}`);
    }
  }

  async function handleRunNow(job) {
    try {
      alert(`Triggering automated audit check for ${job.tickers.join(', ')}...`);
      await triggerAudit(job.tickers);
      alert(`Audit pipeline completed successfully!`);
      onReloadSchedules();
    } catch (err) {
      alert(`Failed to execute check: ${err.message}`);
    }
  }
</script>

<div class="space-y-6">
  <!-- Header -->
  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm">
    <div>
      <h2 class="text-base font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
        <Clock size={18} class="text-[#047857] dark:text-[#34D399]" />
        <span>Automated Monitoring Schedules</span>
      </h2>
      <p class="text-xs font-body text-slate-500 dark:text-slate-400 mt-1">
        Scheduled cron monitoring jobs executing periodic OJK TKBI evaluation pipelines across IDX emitents.
      </p>
    </div>

    <button
      type="button"
      onclick={() => (showModal = true)}
      class="flex items-center space-x-1.5 px-4 py-2 bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-medium rounded-lg text-xs transition-colors self-start sm:self-auto cursor-pointer shadow-xs font-semibold"
    >
      <Plus size={14} />
      <span>New Schedule</span>
    </button>
  </div>

  <!-- Schedules Grid / Table -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm">
    {#if schedules.length === 0}
      <div class="text-center py-16 text-slate-400 dark:text-slate-500 text-xs font-mono">
        No automated schedules configured. Click "New Schedule" to create a pipeline monitor.
      </div>
    {:else}
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead class="bg-slate-50/80 dark:bg-[#162032]/80 text-slate-500 dark:text-slate-400 font-mono text-[10px] uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
            <tr>
              <th class="py-3 px-4">Schedule Name</th>
              <th class="py-3 px-4">Frequency</th>
              <th class="py-3 px-4">Target Emitents</th>
              <th class="py-3 px-4">Threshold Trigger</th>
              <th class="py-3 px-4">Status</th>
              <th class="py-3 px-4">Next Execution</th>
              <th class="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800/80 text-slate-700 dark:text-slate-300">
            {#each schedules as job}
              <tr class="hover:bg-slate-50/70 dark:hover:bg-[#162032]/50 transition-colors">
                <td class="py-3 px-4 font-semibold text-slate-900 dark:text-slate-100 font-headline">{job.name}</td>
                <td class="py-3 px-4 text-slate-600 dark:text-slate-300 font-mono text-[11px]">
                  {getReadableFrequency(job.cron_expression)}
                </td>
                <td class="py-3 px-4">
                  <div class="flex flex-wrap gap-1.5">
                    {#each job.tickers as t}
                      <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-[#162032] font-mono text-[11px] font-semibold text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-800">
                        {t}
                      </span>
                    {/each}
                  </div>
                </td>
                <td class="py-3 px-4 font-mono text-slate-500 dark:text-slate-400 text-[11px]">Score &lt; {job.alert_threshold_score}</td>
                <td class="py-3 px-4">
                  {#if job.last_status === 'SUCCESS'}
                    <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full badge-hijau text-[10px] font-mono font-bold">
                      <span class="w-1.5 h-1.5 rounded-full bg-[#047857] dark:bg-[#34D399]"></span>
                      ACTIVE
                    </span>
                  {:else if job.last_status}
                    <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full badge-transisi text-[10px] font-mono font-bold">
                      <span class="w-1.5 h-1.5 rounded-full bg-[#D97706] dark:bg-[#FBBF24]"></span>
                      {job.last_status}
                    </span>
                  {:else}
                    <span class="text-slate-400 font-mono text-[11px]">SCHEDULED</span>
                  {/if}
                </td>
                <td class="py-3 px-4 text-slate-500 dark:text-slate-400 text-[11px] font-mono">
                  {job.next_run_at ? new Date(job.next_run_at).toLocaleString() : 'Scheduled'}
                </td>
                <td class="py-3 px-4 text-right">
                  <div class="flex items-center justify-end space-x-1.5">
                    <button
                      type="button"
                      onclick={() => handleRunNow(job)}
                      class="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-[#162032] transition-colors cursor-pointer"
                      title="Run now"
                    >
                      <Play size={14} />
                    </button>
                    <button
                      type="button"
                      onclick={() => handleDelete(job.id)}
                      class="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-slate-100 dark:hover:bg-[#162032] transition-colors cursor-pointer"
                      title="Delete schedule"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>

  <!-- Create Schedule Modal -->
  {#if showModal}
    <div class="fixed inset-0 bg-black/50 backdrop-blur-xs z-50 flex items-center justify-center p-4">
      <div
        class="bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-800 rounded-xl max-w-md w-full p-6 shadow-xl text-xs space-y-4 relative z-10"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <h3 id="modal-title" class="text-sm font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <Clock size={16} class="text-[#047857] dark:text-[#34D399]" />
            <span>Create Automated Schedule</span>
          </h3>
          <button
            type="button"
            onclick={() => (showModal = false)}
            class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 cursor-pointer"
          >
            <X size={16} />
          </button>
        </div>

        <form onsubmit={handleCreate} class="space-y-4">
          <div>
            <label for="sched-name" class="text-[11px] font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Schedule Name</label>
            <input
              id="sched-name"
              type="text"
              bind:value={name}
              placeholder="e.g. Energy Sector Weekly Check"
              required
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-[#047857]"
            />
          </div>

          <div>
            <label for="sched-tickers" class="text-[11px] font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Target Emitents (Comma-Separated Tickers)</label>
            <input
              id="sched-tickers"
              type="text"
              bind:value={tickersText}
              placeholder="e.g. PGEO, ADRO, BREN"
              required
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 font-mono placeholder-slate-400 focus:outline-none uppercase focus:ring-1 focus:ring-[#047857]"
            />
          </div>

          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label for="sched-cron" class="text-[11px] font-medium text-slate-700 dark:text-slate-300">Cron Schedule Frequency</label>
              <div class="flex gap-2 text-[11px] font-mono">
                <button type="button" onclick={() => applyPreset('0 8 * * 1')} class="text-[#047857] dark:text-[#34D399] hover:underline cursor-pointer">Weekly</button>
                <span class="text-slate-300">•</span>
                <button type="button" onclick={() => applyPreset('0 0 * * *')} class="text-[#047857] dark:text-[#34D399] hover:underline cursor-pointer">Daily</button>
                <span class="text-slate-300">•</span>
                <button type="button" onclick={() => applyPreset('0 0 1 * *')} class="text-[#047857] dark:text-[#34D399] hover:underline cursor-pointer">Monthly</button>
              </div>
            </div>
            <input
              id="sched-cron"
              type="text"
              bind:value={cronExpr}
              placeholder="0 8 * * 1"
              required
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 font-mono focus:outline-none focus:ring-1 focus:ring-[#047857]"
            />
          </div>

          <div>
            <label for="sched-threshold" class="text-[11px] font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Alert Threshold Score Floor (0-100)</label>
            <input
              id="sched-threshold"
              type="number"
              bind:value={alertScore}
              min="0"
              max="100"
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 font-mono focus:outline-none focus:ring-1 focus:ring-[#047857]"
            />
          </div>

          <div class="flex justify-end gap-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button
              type="button"
              onclick={() => (showModal = false)}
              class="px-3.5 py-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 transition-colors font-medium cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              class="px-4 py-2 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-semibold transition-colors disabled:opacity-50 cursor-pointer shadow-xs"
            >
              {isSubmitting ? 'Saving...' : 'Deploy Schedule'}
            </button>
          </div>
        </form>
      </div>
    </div>
  {/if}
</div>
