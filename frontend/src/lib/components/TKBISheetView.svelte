<script>
  import {
    Download,
    FileSpreadsheet,
    FileText,
    Search,
    Check,
    Edit3,
    Save,
    AlertCircle,
    Filter,
    ShieldCheck,
  } from '@lucide/svelte';
  import { updateHITLEntry, getExportXLSXUrl, getExportPDFUrl } from '../api.js';

  let {
    auditRun = null,
    entries = [],
    onReloadEntries,
  } = $props();

  let searchQuery = $state('');
  let filterStatus = $state('ALL');
  let editingId = $state(null);
  let feedbackText = $state('');
  let overrideChoice = $state('');
  let savingId = $state(null);
  let toastMsg = $state('');

  let filteredEntries = $derived(
    entries.filter((item) => {
      const matchSearch =
        searchQuery === '' ||
        item.tsc_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.bab.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.sektor.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (item.reasoning_ai && item.reasoning_ai.toLowerCase().includes(searchQuery.toLowerCase()));

      const effectiveAns = item.auditor_override || item.jawaban_ai;
      const matchStatus =
        filterStatus === 'ALL' ||
        (filterStatus === 'HIJAU' && effectiveAns.includes('HIJAU')) ||
        (filterStatus === 'TRANSISI' && effectiveAns.includes('TRANSISI')) ||
        (filterStatus === 'TIDAK' && effectiveAns.includes('TIDAK'));

      return matchSearch && matchStatus;
    })
  );

  function startEditing(item) {
    editingId = item.id;
    feedbackText = item.auditor_feedback || '';
    overrideChoice = item.auditor_override || item.jawaban_ai;
  }

  function cancelEditing() {
    editingId = null;
    feedbackText = '';
    overrideChoice = '';
  }

  async function saveFeedback(item) {
    if (!auditRun) return;
    savingId = item.id;
    try {
      await updateHITLEntry(auditRun.id, item.id, feedbackText, overrideChoice);
      editingId = null;
      toastMsg = `Criterion ${item.tsc_id} updated successfully!`;
      setTimeout(() => (toastMsg = ''), 3000);
      onReloadEntries();
    } catch (err) {
      alert(`Failed to save feedback: ${err.message}`);
    } finally {
      savingId = null;
    }
  }

  function getAnswerBadge(val) {
    const upper = String(val || '').toUpperCase();
    if (upper.includes('HIJAU')) return 'badge-hijau';
    if (upper.includes('TRANSISI')) return 'badge-transisi';
    return 'badge-tidak';
  }

  function getHumanLabel(val) {
    const upper = String(val || '').toUpperCase();
    if (upper.includes('HIJAU')) return 'Verified Green';
    if (upper.includes('TRANSISI')) return 'Transitioning';
    return 'Not Compliant';
  }
</script>

<div class="space-y-5">
  <!-- Header & Export Action Bar -->
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-xs">
    <div>
      <h2 class="text-base font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
        <FileSpreadsheet size={18} class="text-emerald-500" />
        <span>Sustainability Criteria Checklist</span>
        <span class="text-xs font-normal text-slate-500 dark:text-slate-400">
          ({filteredEntries.length} of {entries.length} criteria)
        </span>
      </h2>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
        Official Indonesia Green Taxonomy (TKBI 2024) verification criteria with human review.
      </p>
    </div>

    <!-- Export Action Buttons -->
    <div class="flex items-center gap-2.5">
      {#if auditRun}
        <a
          href={getExportXLSXUrl(auditRun.id)}
          download
          class="flex items-center space-x-1.5 px-3 py-1.5 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700/80 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-medium transition-colors shadow-2xs"
        >
          <Download size={14} class="text-slate-500" />
          <span>Export Excel</span>
        </a>

        <a
          href={getExportPDFUrl(auditRun.id)}
          download
          class="flex items-center space-x-1.5 px-3.5 py-1.5 bg-slate-900 dark:bg-emerald-500 hover:bg-slate-800 dark:hover:bg-emerald-400 text-white dark:text-slate-950 font-medium rounded-lg text-xs transition-colors shadow-xs"
        >
          <FileText size={14} />
          <span>Download Audit PDF</span>
        </a>
      {/if}
    </div>
  </div>

  {#if toastMsg}
    <div class="p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300 text-xs font-medium flex items-center space-x-2">
      <Check size={16} />
      <span>{toastMsg}</span>
    </div>
  {/if}

  <!-- Search & Filter Controls -->
  <div class="flex flex-col sm:flex-row gap-3 items-center justify-between">
    <div class="relative w-full sm:w-80">
      <Search size={14} class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
      <input
        type="text"
        bind:value={searchQuery}
        placeholder="Search criteria, category, sector..."
        class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-emerald-500 shadow-2xs"
      />
    </div>

    <div class="flex items-center space-x-1.5 self-start sm:self-auto bg-slate-100 dark:bg-slate-800 p-1 rounded-lg">
      <span class="text-[11px] text-slate-500 dark:text-slate-400 font-medium px-2 flex items-center gap-1">
        <Filter size={12} /> Status:
      </span>
      {#each [
        { id: 'ALL', label: 'All' },
        { id: 'HIJAU', label: 'Green' },
        { id: 'TRANSISI', label: 'Transition' },
        { id: 'TIDAK', label: 'Non-Compliant' }
      ] as opt}
        <button
          type="button"
          onclick={() => (filterStatus = opt.id)}
          class="px-2.5 py-1 text-xs font-medium rounded-md transition-all {filterStatus === opt.id ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-semibold shadow-2xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'}"
        >
          {opt.label}
        </button>
      {/each}
    </div>
  </div>

  <!-- Data Table -->
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-xs">
    <div class="overflow-x-auto max-h-[620px]">
      <table class="w-full text-left border-collapse text-xs">
        <thead class="bg-slate-50/80 dark:bg-slate-950/60 text-slate-600 dark:text-slate-400 font-medium text-[11px] sticky top-0 z-10 border-b border-slate-200 dark:border-slate-800 backdrop-blur-xs">
          <tr>
            <th class="py-3 px-3.5 w-16">Stock</th>
            <th class="py-3 px-3.5 w-28">Sector</th>
            <th class="py-3 px-3.5 w-40">Category</th>
            <th class="py-3 px-3.5 w-24">Criterion ID</th>
            <th class="py-3 px-3.5 w-44">Requirement</th>
            <th class="py-3 px-3.5 w-28 text-center">Status</th>
            <th class="py-3 px-3.5 min-w-[220px]">Explanation & Analysis</th>
            <th class="py-3 px-3.5 min-w-[180px]">Report Reference</th>
            <th class="py-3 px-3.5 min-w-[220px]">Review & Feedback</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-800/80 text-slate-700 dark:text-slate-300">
          {#if filteredEntries.length === 0}
            <tr>
              <td colspan="9" class="text-center py-12 text-slate-400 dark:text-slate-500 text-xs">
                No sustainability criteria matched your search or filters.
              </td>
            </tr>
          {/if}

          {#each filteredEntries as item (item.id)}
            {@const isEditingThis = editingId === item.id}
            {@const effectiveAns = item.auditor_override || item.jawaban_ai}

            <tr class="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition-colors {item.is_overridden ? 'bg-amber-50/30 dark:bg-amber-950/20' : ''}">
              <td class="py-3 px-3.5 font-bold text-slate-900 dark:text-slate-100 font-mono">{item.kode_emiten}</td>
              <td class="py-3 px-3.5 truncate max-w-[120px]" title={item.sektor}>{item.sektor}</td>
              <td class="py-3 px-3.5 text-[11px] leading-tight max-w-[160px]" title={item.bab}>{item.bab}</td>
              <td class="py-3 px-3.5 font-mono text-emerald-600 dark:text-emerald-400 font-medium">{item.tsc_id}</td>
              <td class="py-3 px-3.5 text-[11px] leading-relaxed max-w-[180px]" title={item.tsc}>{item.tsc}</td>

              <!-- Status Badge -->
              <td class="py-3 px-3.5 text-center">
                <span class="inline-block px-2.5 py-0.5 rounded-full text-[11px] font-medium {getAnswerBadge(effectiveAns)}">
                  {getHumanLabel(effectiveAns)}
                </span>
                {#if item.is_overridden}
                  <div class="text-[10px] text-amber-600 dark:text-amber-400 mt-1 font-medium">Overridden</div>
                {/if}
              </td>

              <!-- AI Reasoning -->
              <td class="py-3 px-3.5 text-[11px] leading-relaxed text-slate-600 dark:text-slate-300">{item.reasoning_ai}</td>

              <!-- Bukti Citation -->
              <td class="py-3 px-3.5 text-[11px] text-slate-500 dark:text-slate-400 leading-snug">{item.bukti || 'Self-declared report'}</td>

              <!-- Auditor Review -->
              <td class="py-3 px-3.5 bg-slate-50/40 dark:bg-slate-950/20">
                {#if isEditingThis}
                  <div class="space-y-2 p-2 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 shadow-xs">
                    <div class="flex items-center gap-2">
                      <span class="text-[10px] text-slate-500 dark:text-slate-400 font-medium uppercase">Change Status:</span>
                      <select
                        bind:value={overrideChoice}
                        class="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 text-xs rounded-md px-2 py-0.5 focus:outline-none"
                      >
                        <option value="HIJAU">Verified Green</option>
                        <option value="TRANSISI">Transitioning</option>
                        <option value="TIDAK">Not Compliant</option>
                      </select>
                    </div>

                    <textarea
                      bind:value={feedbackText}
                      placeholder="Add compliance notes or explanation..."
                      rows="2"
                      class="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-md p-2 text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                    ></textarea>

                    <div class="flex justify-end gap-1.5">
                      <button
                        type="button"
                        onclick={cancelEditing}
                        class="px-2.5 py-1 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-slate-900 rounded-md text-xs"
                      >
                        Cancel
                      </button>
                      <button
                        type="button"
                        onclick={() => saveFeedback(item)}
                        disabled={savingId === item.id}
                        class="px-3 py-1 bg-slate-900 dark:bg-emerald-500 text-white dark:text-slate-950 font-medium rounded-md text-xs flex items-center gap-1 disabled:opacity-50"
                      >
                        <Save size={12} />
                        <span>{savingId === item.id ? 'Saving...' : 'Save'}</span>
                      </button>
                    </div>
                  </div>
                {:else}
                  <div class="flex items-start justify-between gap-1 group">
                    <div class="text-[11px] text-slate-600 dark:text-slate-400 italic flex-1">
                      {item.auditor_feedback || 'No review notes added yet'}
                    </div>
                    <button
                      type="button"
                      onclick={() => startEditing(item)}
                      class="p-1 rounded-md text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                      title="Edit review & override"
                    >
                      <Edit3 size={14} />
                    </button>
                  </div>
                {/if}
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>
