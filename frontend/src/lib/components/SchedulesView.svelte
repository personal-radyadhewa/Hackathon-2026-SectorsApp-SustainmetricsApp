<script>
  import { Clock, Plus, Trash2, Play, Calendar, AlertCircle, CheckCircle2 } from '@lucide/svelte';
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

  async function handleCreate(e) {
    e.preventDefault();
    if (!name.trim()) return;

    const tickersList = tickersText
      .split(',')
      .map((t) => t.trim().toUpperCase())
      .filter(Boolean);

    if (tickersList.length === 0) {
      alert('Please specify at least one ticker.');
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
    if (!confirm('Are you sure you want to delete this scheduled audit job?')) return;
    try {
      await deleteSchedule(id);
      onReloadSchedules();
    } catch (err) {
      alert(`Failed to delete schedule: ${err.message}`);
    }
  }

  async function handleRunNow(job) {
    try {
      alert(`Triggering batch audit for ${job.tickers.join(', ')}...`);
      await triggerAudit(job.tickers);
      alert(`Batch audit successfully triggered!`);
      onReloadSchedules();
    } catch (err) {
      alert(`Failed to trigger job: ${err.message}`);
    }
  }
</script>

<div class="space-y-6">
  <!-- Header -->
  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
    <div>
      <h2 class="text-base font-bold text-slate-900 flex items-center gap-2">
        <Clock size={18} class="text-emerald-400" />
        <span>Scheduled Audit Jobs & Watchlists</span>
      </h2>
      <p class="text-xs text-slate-500">
        Automate recurring background green audits via Python APScheduler daemon.
      </p>
    </div>

    <button
      type="button"
      onclick={() => (showModal = true)}
      class="flex items-center space-x-1.5 px-3 py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-lg text-xs transition-colors self-start sm:self-auto shadow-sm"
    >
      <Plus size={15} />
      <span>New Audit Schedule</span>
    </button>
  </div>

  <!-- Schedules Grid / Table -->
  <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
    {#if schedules.length === 0}
      <div class="text-center py-16 text-slate-400 text-xs">
        No recurring audit schedules configured. Click "New Audit Schedule" to automate your portfolio monitoring.
      </div>
    {:else}
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead class="bg-slate-100 text-slate-700 font-semibold uppercase tracking-wider text-[10px] border-b border-slate-200">
            <tr>
              <th class="py-3 px-4">Schedule Name</th>
              <th class="py-3 px-4">Cron Expression</th>
              <th class="py-3 px-4">Watchlist Tickers</th>
              <th class="py-3 px-4">Threshold Alert</th>
              <th class="py-3 px-4">Last Status</th>
              <th class="py-3 px-4">Next Trigger</th>
              <th class="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-[#1A253D] text-slate-700">
            {#each schedules as job}
              <tr class="hover:bg-slate-50/60 transition-colors">
                <td class="py-3 px-4 font-semibold text-slate-900">{job.name}</td>
                <td class="py-3 px-4 font-mono text-emerald-400 font-bold">{job.cron_expression}</td>
                <td class="py-3 px-4">
                  <div class="flex flex-wrap gap-1">
                    {#each job.tickers as t}
                      <span class="px-1.5 py-0.5 rounded bg-slate-100 border border-slate-300 font-mono text-[10px] text-slate-800">
                        {t}
                      </span>
                    {/each}
                  </div>
                </td>
                <td class="py-3 px-4 font-mono text-slate-500">&lt; {job.alert_threshold_score} pts</td>
                <td class="py-3 px-4">
                  {#if job.last_status === 'SUCCESS'}
                    <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-mono text-[10px] font-bold">
                      SUCCESS
                    </span>
                  {:else if job.last_status}
                    <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 font-mono text-[10px]">
                      {job.last_status}
                    </span>
                  {:else}
                    <span class="text-slate-400 text-[10px] italic">Pending First Run</span>
                  {/if}
                </td>
                <td class="py-3 px-4 font-mono text-slate-500 text-[11px]">
                  {job.next_run_at ? new Date(job.next_run_at).toLocaleString() : 'Next Poller Interval'}
                </td>
                <td class="py-3 px-4 text-right">
                  <div class="flex items-center justify-end space-x-1.5">
                    <button
                      type="button"
                      onclick={() => handleRunNow(job)}
                      class="p-1.5 rounded text-slate-500 hover:text-emerald-400 hover:bg-slate-200 transition-colors"
                      title="Run immediately"
                    >
                      <Play size={13} />
                    </button>
                    <button
                      type="button"
                      onclick={() => handleDelete(job.id)}
                      class="p-1.5 rounded text-slate-500 hover:text-rose-400 hover:bg-slate-200 transition-colors"
                      title="Delete schedule"
                    >
                      <Trash2 size={13} />
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
      class="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex items-center justify-center p-4"
    >
      <div
        class="bg-white border border-slate-200 rounded-xl max-w-md w-full p-5 shadow-2xl text-xs space-y-4 relative z-10"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <div class="flex items-center justify-between border-b border-slate-200 pb-3">
          <h3 id="modal-title" class="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Clock size={16} class="text-emerald-400" />
            <span>Create Recurring Green Audit Schedule</span>
          </h3>
          <button
            type="button"
            onclick={() => (showModal = false)}
            class="text-slate-500 hover:text-slate-800"
          >
            ✕
          </button>
        </div>

        <form onsubmit={handleCreate} class="space-y-3.5">
          <div>
            <label for="sched-name" class="text-[10px] uppercase font-semibold text-slate-500 block mb-1">Schedule Name</label>
            <input
              id="sched-name"
              type="text"
              bind:value={name}
              placeholder="e.g. Weekly Geothermal Audit"
              required
              class="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-slate-800 focus:outline-none focus:border-emerald-500/50"
            />
          </div>

          <div>
            <label for="sched-tickers" class="text-[10px] uppercase font-semibold text-slate-500 block mb-1">Target Emitents (Comma-separated)</label>
            <input
              id="sched-tickers"
              type="text"
              bind:value={tickersText}
              placeholder="e.g. PGEO, ADRO, BREN"
              required
              class="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-slate-800 font-mono focus:outline-none focus:border-emerald-500/50"
            />
          </div>

          <div>
            <div class="flex items-center justify-between mb-1">
              <label for="sched-cron" class="text-[10px] uppercase font-semibold text-slate-500">Cron Expression</label>
              <div class="flex gap-1 text-[10px] text-slate-500">
                <button type="button" onclick={() => applyPreset('0 8 * * 1')} class="text-emerald-400 hover:underline">Weekly Mon</button>
                <span>•</span>
                <button type="button" onclick={() => applyPreset('0 0 * * *')} class="text-emerald-400 hover:underline">Daily</button>
              </div>
            </div>
            <input
              id="sched-cron"
              type="text"
              bind:value={cronExpr}
              placeholder="0 8 * * 1"
              required
              class="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-slate-800 font-mono focus:outline-none focus:border-emerald-500/50"
            />
          </div>

          <div>
            <label for="sched-threshold" class="text-[10px] uppercase font-semibold text-slate-500 block mb-1">Alert Threshold Score (&lt; Consistency Score)</label>
            <input
              id="sched-threshold"
              type="number"
              bind:value={alertScore}
              min="0"
              max="100"
              class="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-slate-800 font-mono focus:outline-none focus:border-emerald-500/50"
            />
          </div>

          <div class="flex justify-end gap-2 pt-2 border-t border-slate-200">
            <button
              type="button"
              onclick={() => (showModal = false)}
              class="px-3 py-1.5 rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              class="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-bold transition-colors disabled:opacity-50"
            >
              {isSubmitting ? 'Creating...' : 'Register Schedule'}
            </button>
          </div>
        </form>
      </div>
    </div>
  {/if}
</div>
