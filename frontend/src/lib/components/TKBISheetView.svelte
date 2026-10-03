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
      toastMsg = `Criterion ${item.tsc_id} successfully updated!`;
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
</script>

<div class="space-y-4">
  <!-- Action Toolbar: Header & Export CTA Buttons -->
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
    <div>
      <h2 class="text-base font-bold text-slate-900 flex items-center gap-2">
        <FileSpreadsheet size={18} class="text-emerald-400" />
        <span>Audit Sheet</span>
        <span class="text-xs font-mono font-normal text-slate-500">
          ({filteredEntries.length} / {entries.length} criteria)
        </span>
      </h2>
      <p class="text-xs text-slate-500">
        Template conforming to <span class="font-mono text-emerald-400">Template_Audit_TKBI.xlsx</span> with Human-In-The-Loop (HITL) audit verification.
      </p>
    </div>

    <!-- Export Action Buttons -->
    <div class="flex items-center gap-2">
      {#if auditRun}
        <a
          href={getExportXLSXUrl(auditRun.id)}
          download
          class="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-emerald-400 border border-emerald-500/30 rounded-lg text-xs font-semibold transition-colors"
        >
          <Download size={14} />
          <span>Export Stamped XLSX</span>
        </a>

        <a
          href={getExportPDFUrl(auditRun.id)}
          download
          class="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-lg text-xs transition-colors shadow-sm"
        >
          <FileText size={14} />
          <span>Signed Audit PDF (SHA-256)</span>
        </a>
      {/if}
    </div>
  </div>

  {#if toastMsg}
    <div class="p-2.5 rounded-lg bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-medium flex items-center space-x-2">
      <Check size={15} />
      <span>{toastMsg}</span>
    </div>
  {/if}

  <!-- Filter and Search Bar -->
  <div class="flex flex-col sm:flex-row gap-3 items-center justify-between">
    <div class="relative w-full sm:w-80">
      <Search size={14} class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
      <input
        type="text"
        bind:value={searchQuery}
        placeholder="Filter by TSC ID, Bab, Sector..."
        class="w-full bg-white border border-slate-200 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-800 placeholder-slate-500 focus:outline-none focus:border-emerald-500/50"
      />
    </div>

    <div class="flex items-center space-x-2 self-start sm:self-auto">
      <span class="text-xs text-slate-500 font-medium flex items-center gap-1">
        <Filter size={13} /> Filter:
      </span>
      {#each ['ALL', 'HIJAU', 'TRANSISI', 'TIDAK'] as statusOpt}
        <button
          type="button"
          onclick={() => (filterStatus = statusOpt)}
          class="px-2.5 py-1 text-xs font-mono font-medium rounded-md transition-colors {filterStatus === statusOpt ? 'bg-slate-900 text-white font-bold' : 'bg-white text-slate-500 hover:text-slate-800 border border-slate-200'}"
        >
          {statusOpt}
        </button>
      {/each}
    </div>
  </div>

  <!-- 12-Column Data Grid Table -->
  <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
    <div class="overflow-x-auto max-h-[620px]">
      <table class="w-full text-left border-collapse text-xs">
        <thead class="bg-slate-100 text-slate-700 font-semibold uppercase tracking-wider text-[10px] sticky top-0 z-10 border-b border-slate-200">
          <tr>
            <th class="py-3 px-3 w-16">Ticker</th>
            <th class="py-3 px-3 w-28">Sector</th>
            <th class="py-3 px-3 w-40">Bab</th>
            <th class="py-3 px-3 w-16">KBLI</th>
            <th class="py-3 px-3 w-24">TSCID</th>
            <th class="py-3 px-3 w-36">Technical Criteria (TSC)</th>
            <th class="py-3 px-3 w-20">Allowed</th>
            <th class="py-3 px-3 w-28 text-center">Jawaban AI</th>
            <th class="py-3 px-3 w-20">Confidence</th>
            <th class="py-3 px-3 min-w-[200px]">Reasoning AI</th>
            <th class="py-3 px-3 min-w-[180px]">Bukti (Document Citation)</th>
            <th class="py-3 px-3 min-w-[220px]">Auditor Feedback (HITL)</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-[#1A253D] font-normal text-slate-700">
          {#if filteredEntries.length === 0}
            <tr>
              <td colspan="12" class="text-center py-10 text-slate-400 text-xs">
                No TKBI criteria matched your filter or no audit entries found.
              </td>
            </tr>
          {/if}

          {#each filteredEntries as item (item.id)}
            {@const isEditingThis = editingId === item.id}
            {@const effectiveAns = item.auditor_override || item.jawaban_ai}

            <tr class="hover:bg-slate-50/70 transition-colors {item.is_overridden ? 'bg-amber-950/10' : ''}">
              <td class="py-2.5 px-3 font-mono font-bold text-slate-900">{item.kode_emiten}</td>
              <td class="py-2.5 px-3 truncate max-w-[120px] text-slate-700" title={item.sektor}>{item.sektor}</td>
              <td class="py-2.5 px-3 text-slate-700 text-[11px] leading-tight max-w-[160px]" title={item.bab}>{item.bab}</td>
              <td class="py-2.5 px-3 font-mono text-slate-500">{item.kbli}</td>
              <td class="py-2.5 px-3 font-mono font-semibold text-emerald-400">{item.tsc_id}</td>
              <td class="py-2.5 px-3 text-[11px] leading-tight text-slate-700 max-w-[150px]" title={item.tsc}>{item.tsc}</td>
              <td class="py-2.5 px-3 font-mono text-[10px] text-slate-500">{item.bentuk_jawaban}</td>

              <!-- Jawaban AI / Effective Answer -->
              <td class="py-2.5 px-3 text-center">
                <span class="inline-block px-2 py-0.5 rounded text-[11px] font-bold font-mono {getAnswerBadge(effectiveAns)}">
                  {effectiveAns}
                </span>
                {#if item.is_overridden}
                  <div class="text-[9px] text-amber-400 font-mono mt-0.5">Auditor Overridden</div>
                {/if}
              </td>

              <!-- Keyakinan AI -->
              <td class="py-2.5 px-3 font-mono text-[11px] text-slate-500 text-center">{item.keyakinan_ai}</td>

              <!-- Reasoning AI -->
              <td class="py-2.5 px-3 text-[11px] leading-relaxed text-slate-700">{item.reasoning_ai}</td>

              <!-- Bukti Citation -->
              <td class="py-2.5 px-3 text-[11px] text-slate-500 font-mono leading-tight">{item.bukti}</td>

              <!-- Auditor Feedback & HITL Override Form -->
              <td class="py-2.5 px-3 bg-slate-50/50">
                {#if isEditingThis}
                  <div class="space-y-2 p-1.5 bg-slate-100 rounded-md border border-slate-300">
                    <div class="flex items-center gap-1.5">
                      <span class="text-[10px] text-slate-500 font-semibold uppercase">Override:</span>
                      <select
                        bind:value={overrideChoice}
                        class="bg-slate-50 border border-slate-300 text-slate-800 text-xs rounded px-1.5 py-0.5 focus:outline-none"
                      >
                        <option value="HIJAU">HIJAU</option>
                        <option value="TRANSISI">TRANSISI</option>
                        <option value="TIDAK">TIDAK</option>
                      </select>
                    </div>

                    <textarea
                      bind:value={feedbackText}
                      placeholder="Add compliance notes or justification..."
                      rows="2"
                      class="w-full bg-slate-50 border border-slate-300 rounded p-1.5 text-xs text-slate-800 placeholder-slate-500 focus:outline-none focus:border-emerald-500/50"
                    ></textarea>

                    <div class="flex justify-end gap-1.5">
                      <button
                        type="button"
                        onclick={cancelEditing}
                        class="px-2 py-0.5 bg-slate-200 text-slate-500 hover:text-slate-800 rounded text-[11px]"
                      >
                        Cancel
                      </button>
                      <button
                        type="button"
                        onclick={() => saveFeedback(item)}
                        disabled={savingId === item.id}
                        class="px-2.5 py-0.5 bg-slate-900 text-white font-bold rounded text-[11px] flex items-center gap-1 disabled:opacity-50"
                      >
                        <Save size={12} />
                        <span>{savingId === item.id ? 'Saving...' : 'Save'}</span>
                      </button>
                    </div>
                  </div>
                {:else}
                  <div class="flex items-start justify-between gap-1 group">
                    <div class="text-[11px] text-slate-700 italic flex-1">
                      {item.auditor_feedback || '(No auditor feedback recorded)'}
                    </div>
                    <button
                      type="button"
                      onclick={() => startEditing(item)}
                      class="p-1 rounded text-slate-500 hover:text-emerald-400 hover:bg-slate-200 transition-colors"
                      title="Edit feedback & override"
                    >
                      <Edit3 size={13} />
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
