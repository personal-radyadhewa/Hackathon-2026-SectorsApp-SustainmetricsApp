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
    if (expr === '0 8 * * 1') return 'Every Monday at 8:00 AM';
    if (expr === '0 0 * * *') return 'Daily at midnight';
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
      alert('Please specify at least one stock code.');
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
      alert(`Starting automated check for ${job.tickers.join(', ')}...`);
      await triggerAudit(job.tickers);
      alert(`Check completed successfully!`);
      onReloadSchedules();
    } catch (err) {
      alert(`Failed to run check: ${err.message}`);
    }
  }
</script>

<div class="space-y-6">
  <!-- Header -->
  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-xs">
    <div>
      <h2 class="text-base font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
        <Clock size={18} class="text-emerald-500" />
        <span>Automated Monitoring</span>
      </h2>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
        Automatically run periodic sustainability checks on your watchlist companies.
      </p>
    </div>

    <button
      type="button"
      onclick={() => (showModal = true)}
      class="flex items-center space-x-1.5 px-3.5 py-2 bg-slate-900 dark:bg-emerald-500 hover:bg-slate-800 dark:hover:bg-emerald-400 text-white dark:text-slate-950 font-medium rounded-lg text-xs transition-colors self-start sm:self-auto shadow-xs"
    >
      <Plus size={15} />
      <span>New Schedule</span>
    </button>
  </div>

  <!-- Schedules Grid / Table -->
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-xs">
    {#if schedules.length === 0}
      <div class="text-center py-16 text-slate-400 dark:text-slate-500 text-xs">
        No automated schedules set up yet. Click "New Schedule" to start automatic monitoring.
      </div>
    {:else}
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead class="bg-slate-50/80 dark:bg-slate-950/60 text-slate-600 dark:text-slate-400 font-medium text-[11px] border-b border-slate-200 dark:border-slate-800">
            <tr>
              <th class="py-3 px-4">Schedule Name</th>
              <th class="py-3 px-4">Frequency</th>
              <th class="py-3 px-4">Monitored Companies</th>
              <th class="py-3 px-4">Alert Trigger</th>
              <th class="py-3 px-4">Status</th>
              <th class="py-3 px-4">Next Check</th>
              <th class="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800/80 text-slate-700 dark:text-slate-300">
            {#each schedules as job}
              <tr class="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition-colors">
                <td class="py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">{job.name}</td>
                <td class="py-3 px-4 text-slate-600 dark:text-slate-300 font-medium">
                  {getReadableFrequency(job.cron_expression)}
                </td>
                <td class="py-3 px-4">
                  <div class="flex flex-wrap gap-1.5">
                    {#each job.tickers as t}
                      <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 font-mono text-[11px] font-semibold text-slate-800 dark:text-slate-200">
                        {t}
                      </span>
                    {/each}
                  </div>
                </td>
                <td class="py-3 px-4 text-slate-500 dark:text-slate-400">Score &lt; {job.alert_threshold_score}</td>
                <td class="py-3 px-4">
                  {#if job.last_status === 'SUCCESS'}
                    <span class="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 text-[10px] font-medium">
                      Active
                    </span>
                  {:else if job.last_status}
                    <span class="px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 dark:bg-amber-950/50 dark:text-amber-300 text-[10px] font-medium">
                      {job.last_status}
                    </span>
                  {:else}
                    <span class="text-slate-400 text-[11px] italic">Scheduled</span>
                  {/if}
                </td>
                <td class="py-3 px-4 text-slate-500 dark:text-slate-400 text-[11px]">
                  {job.next_run_at ? new Date(job.next_run_at).toLocaleString() : 'Scheduled'}
                </td>
                <td class="py-3 px-4 text-right">
                  <div class="flex items-center justify-end space-x-1.5">
                    <button
                      type="button"
                      onclick={() => handleRunNow(job)}
                      class="p-1.5 rounded-md text-slate-500 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                      title="Run now"
                    >
                      <Play size={14} />
                    </button>
                    <button
                      type="button"
                      onclick={() => handleDelete(job.id)}
                      class="p-1.5 rounded-md text-slate-400 hover:text-rose-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
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
    <!-- Backdrop -->
    <div
      class="fixed inset-0 bg-black/50 backdrop-blur-xs z-50 flex items-center justify-center p-4"
    >
      <div
        class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl max-w-md w-full p-6 shadow-xl text-xs space-y-4 relative z-10"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <h3 id="modal-title" class="text-sm font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <Clock size={16} class="text-emerald-500" />
            <span>Create Automated Schedule</span>
          </h3>
          <button
            type="button"
            onclick={() => (showModal = false)}
            class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
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
              class="w-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
          </div>

          <div>
            <label for="sched-tickers" class="text-[11px] font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Companies (Stock Codes, comma-separated)</label>
            <input
              id="sched-tickers"
              type="text"
              bind:value={tickersText}
              placeholder="e.g. PGEO, ADRO, BREN"
              required
              class="w-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 font-mono placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
          </div>

          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label for="sched-cron" class="text-[11px] font-medium text-slate-700 dark:text-slate-300">Frequency</label>
              <div class="flex gap-2 text-[11px]">
                <button type="button" onclick={() => applyPreset('0 8 * * 1')} class="text-emerald-600 dark:text-emerald-400 hover:underline">Weekly</button>
                <span class="text-slate-300">•</span>
                <button type="button" onclick={() => applyPreset('0 0 * * *')} class="text-emerald-600 dark:text-emerald-400 hover:underline">Daily</button>
                <span class="text-slate-300">•</span>
                <button type="button" onclick={() => applyPreset('0 0 1 * *')} class="text-emerald-600 dark:text-emerald-400 hover:underline">Monthly</button>
              </div>
            </div>
            <input
              id="sched-cron"
              type="text"
              bind:value={cronExpr}
              placeholder="0 8 * * 1"
              required
              class="w-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 font-mono focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
          </div>

          <div>
            <label for="sched-threshold" class="text-[11px] font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Alert if Sustainability Score drops below (0-100)</label>
            <input
              id="sched-threshold"
              type="number"
              bind:value={alertScore}
              min="0"
              max="100"
              class="w-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 font-mono focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
          </div>

          <div class="flex justify-end gap-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button
              type="button"
              onclick={() => (showModal = false)}
              class="px-3.5 py-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              class="px-4 py-2 rounded-lg bg-slate-900 dark:bg-emerald-500 hover:bg-slate-800 dark:hover:bg-emerald-400 text-white dark:text-slate-950 font-medium transition-colors shadow-xs disabled:opacity-50"
            >
              {isSubmitting ? 'Saving...' : 'Create Schedule'}
            </button>
          </div>
        </form>
      </div>
    </div>
  {/if}
</div>
