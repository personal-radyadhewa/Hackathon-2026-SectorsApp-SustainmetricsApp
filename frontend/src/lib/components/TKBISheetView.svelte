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
  import { t, currentLang } from '../i18n.js';

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
      toastMsg = `Criterion ${item.tsc_id} verified and updated.`;
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
    if (upper.includes('INTERIM')) return 'bg-sky-50 text-sky-800 border-sky-200 dark:bg-sky-950/60 dark:text-sky-300 dark:border-sky-800';
    if (upper.includes('HIJAU')) return 'badge-hijau';
    if (upper.includes('TRANSISI')) return 'badge-transisi';
    return 'badge-tidak';
  }

  function getDotColor(val) {
    const upper = String(val || '').toUpperCase();
    if (upper.includes('INTERIM')) return 'bg-[#0284C7] dark:bg-[#38BDF8]';
    if (upper.includes('HIJAU')) return 'bg-[#047857] dark:bg-[#34D399]';
    if (upper.includes('TRANSISI')) return 'bg-[#D97706] dark:bg-[#FBBF24]';
    return 'bg-[#DC2626] dark:bg-[#F87171]';
  }

  function getHumanLabel(val, lang = 'id') {
    const upper = String(val || '').toUpperCase();
    if (upper.includes('INTERIM')) return lang === 'id' ? 'TRANSISI INTERIM' : 'INTERIM TRANSITION';
    if (upper.includes('HIJAU')) return lang === 'id' ? 'HIJAU (SESUAI)' : 'GREEN (ALIGNED)';
    if (upper.includes('TRANSISI')) return lang === 'id' ? 'TRANSISI' : 'TRANSITION';
    return lang === 'id' ? 'TIDAK MEMENUHI' : 'NON-COMPLIANT';
  }
</script>

<div class="space-y-5">
  <!-- Top Action & Header Bar -->
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm">
    <div>
      <h2 class="text-base font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
        <FileSpreadsheet size={18} class="text-[#047857] dark:text-[#34D399]" />
        <span>{$currentLang === 'id' ? 'Tabel Audit Regulasi OJK TKBI' : 'OJK TKBI Regulatory Audit Grid'}</span>
        <span class="text-xs font-mono font-normal text-slate-500 dark:text-slate-400">
          {$currentLang === 'id' ? `(${filteredEntries.length} / ${entries.length} kriteria aktif)` : `(${filteredEntries.length} / ${entries.length} criteria active)`}
        </span>
      </h2>
      <p class="text-xs font-body text-slate-500 dark:text-slate-400 mt-1">
        {$currentLang === 'id'
          ? 'Kriteria Teknis Kuantitatif (TSC) Taksonomi Keuangan Berkelanjutan Indonesia (TKBI 2024) & Validasi Auditor HIT.'
          : 'Technical Screening Criteria (TSC) Indonesia Sustainable Finance Taxonomy (TKBI 2024) & Auditor HIT Sign-Off.'}
      </p>
    </div>

    <!-- Export Actions -->
    <div class="flex items-center gap-2.5">
      {#if auditRun}
        <a
          href={getExportXLSXUrl(auditRun.id)}
          download
          class="flex items-center space-x-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-[#162032] dark:hover:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-medium transition-colors shadow-2xs"
        >
          <Download size={14} class="text-slate-500" />
          <span>{$currentLang === 'id' ? 'Ekspor Excel' : 'Export Excel'}</span>
        </a>

        <a
          href={getExportPDFUrl(auditRun.id)}
          download
          class="flex items-center space-x-1.5 px-4 py-2 bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-medium rounded-lg text-xs transition-colors shadow-xs"
        >
          <FileText size={14} />
          <span>{$currentLang === 'id' ? 'Unduh PDF Audit' : 'Download Audit PDF'}</span>
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
        placeholder={$currentLang === 'id' ? 'Cari ID Kriteria, kategori, kata kunci...' : 'Filter by TSC-ID, category, keyword...'}
        class="w-full bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-800 rounded-xl pl-9 pr-3 py-1.5 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-[#047857] dark:focus:ring-[#34D399]"
      />
    </div>

    <!-- Status Filters -->
    <div class="flex items-center space-x-1 self-start sm:self-auto bg-slate-100 dark:bg-[#162032] p-1 rounded-xl border border-slate-200/80 dark:border-slate-800">
      <span class="text-[11px] font-mono text-slate-400 px-2 flex items-center gap-1">
        <Filter size={12} /> Status:
      </span>
      {#each [
        { id: 'ALL', labelId: 'Semua', labelEn: 'All' },
        { id: 'HIJAU', labelId: 'Hijau', labelEn: 'Green' },
        { id: 'TRANSISI', labelId: 'Transisi', labelEn: 'Transition' },
        { id: 'TIDAK', labelId: 'Tidak Memenuhi', labelEn: 'Non-Compliant' }
      ] as opt}
        <button
          type="button"
          onclick={() => (filterStatus = opt.id)}
          class="px-2.5 py-1 text-xs font-medium rounded-lg transition-all cursor-pointer {filterStatus === opt.id
            ? 'bg-white dark:bg-[#0F172A] text-slate-900 dark:text-slate-100 font-bold shadow-2xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'}"
        >
          {$currentLang === 'id' ? opt.labelId : opt.labelEn}
        </button>
      {/each}
    </div>
  </div>

  <!-- Data Table -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm">
    <div class="overflow-x-auto max-h-[640px]">
      <table class="w-full text-left border-collapse text-xs">
        <thead class="bg-slate-50/90 dark:bg-[#162032]/80 text-slate-500 dark:text-slate-400 font-mono text-[10px] uppercase tracking-wider sticky top-0 z-10 border-b border-slate-200 dark:border-slate-800 backdrop-blur-xs">
          <tr>
            <th class="py-3 px-3.5 w-16">{$currentLang === 'id' ? 'Emiten' : 'Stock'}</th>
            <th class="py-3 px-3.5 w-28">{$currentLang === 'id' ? 'Sektor' : 'Sector'}</th>
            <th class="py-3 px-3.5 w-36">{$currentLang === 'id' ? 'Kategori' : 'Category'}</th>
            <th class="py-3 px-3.5 w-24">{$currentLang === 'id' ? 'ID Kriteria' : 'Criterion ID'}</th>
            <th class="py-3 px-3.5 w-48">{$currentLang === 'id' ? 'Ketentuan' : 'Requirement'}</th>
            <th class="py-3 px-3.5 w-32 text-center">{$currentLang === 'id' ? 'Status OJK' : 'OJK Status'}</th>
            <th class="py-3 px-3.5 min-w-[200px]">{$currentLang === 'id' ? 'Analisis AI' : 'AI Reasoning & Analysis'}</th>
            <th class="py-3 px-3.5 min-w-[160px]">{$currentLang === 'id' ? 'Bukti Dokumen' : 'Evidence Citation'}</th>
            <th class="py-3 px-3.5 min-w-[220px]">{$currentLang === 'id' ? 'Tinjauan Auditor (HIT)' : 'Auditor Review (HIT)'}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-800/80 text-slate-700 dark:text-slate-300">
          {#if filteredEntries.length === 0}
            <tr>
              <td colspan="9" class="text-center py-12 text-slate-400 dark:text-slate-500 text-xs font-mono">
                {$currentLang === 'id' ? 'Tidak ada kriteria keberlanjutan yang cocok dengan pencarian atau filter Anda.' : 'No sustainability criteria matched your search or filters.'}
              </td>
            </tr>
          {/if}

          {#each filteredEntries as item (item.id)}
            {@const isEditingThis = editingId === item.id}
            {@const effectiveAns = item.auditor_override || item.jawaban_ai}

            <tr class="hover:bg-slate-50/70 dark:hover:bg-[#162032]/50 transition-colors {item.is_overridden ? 'bg-amber-50/20 dark:bg-[rgba(251,191,36,0.06)]' : ''}">
              <td class="py-3 px-3.5 font-bold text-slate-900 dark:text-slate-100 font-mono">{item.kode_emiten}</td>
              <td class="py-3 px-3.5 truncate max-w-[120px] font-mono text-[11px]" title={item.sektor}>{item.sektor}</td>
              <td class="py-3 px-3.5 text-[11px] leading-tight max-w-[150px]" title={item.bab}>{item.bab}</td>
              <td class="py-3 px-3.5 font-mono text-[11px]">
                <div class="text-[#047857] dark:text-[#34D399] font-bold">{item.tsc_id}</div>
                {#if item.eo_category}
                  <span class="inline-block mt-0.5 px-1.5 py-0.2 rounded bg-blue-50 dark:bg-blue-950/60 text-[#1D4ED8] dark:text-[#60A5FA] text-[9px] font-bold">
                    {item.eo_category}
                  </span>
                {/if}
              </td>
              <td class="py-3 px-3.5 text-[11px] leading-snug max-w-[180px]" title={item.tsc}>{item.tsc}</td>

              <!-- Status Badge (Pill with dot) -->
              <td class="py-3 px-3.5 text-center">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-mono font-bold border {getAnswerBadge(effectiveAns)}">
                  <span class="w-1.5 h-1.5 rounded-full {getDotColor(effectiveAns)}"></span>
                  <span>{getHumanLabel(effectiveAns, $currentLang)}</span>
                </span>
                {#if item.is_overridden}
                  <div class="text-[9px] font-mono text-[#D97706] dark:text-[#FBBF24] mt-1 uppercase font-semibold">
                    {$currentLang === 'id' ? 'Diubah Manual' : 'Overridden'}
                  </div>
                {/if}
              </td>

              <!-- AI Reasoning -->
              <td class="py-3 px-3.5 text-[11px] leading-relaxed text-slate-600 dark:text-slate-300 font-body">
                {item.reasoning_ai}
              </td>

              <!-- Evidence Citation -->
              <td class="py-3 px-3.5 text-[11px] font-mono text-slate-500 dark:text-slate-400">
                {item.bukti || ($currentLang === 'id' ? 'Menunggu Referensi Dokumen' : 'Filing Reference Pending')}
              </td>

              <!-- Auditor Review & Override Form -->
              <td class="py-3 px-3.5 bg-slate-50/40 dark:bg-[#162032]/30">
                {#if isEditingThis}
                  <div class="space-y-2 p-2.5 bg-white dark:bg-[#0F172A] rounded-xl border border-slate-200 dark:border-slate-700 shadow-xs">
                    <div class="flex items-center gap-2">
                      <span class="text-[10px] font-mono uppercase text-slate-400 font-semibold">Status:</span>
                      <select
                        bind:value={overrideChoice}
                        class="bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 text-xs font-mono rounded-lg px-2 py-1 focus:outline-none"
                      >
                        <option value="HIJAU">{$currentLang === 'id' ? 'HIJAU (Sesuai)' : 'HIJAU (Aligned)'}</option>
                        <option value="TRANSISI">{$currentLang === 'id' ? 'TRANSISI (Masa Transisi)' : 'TRANSISI (Transition)'}</option>
                        <option value="TIDAK">{$currentLang === 'id' ? 'TIDAK MEMENUHI' : 'NON-COMPLIANT'}</option>
                      </select>
                    </div>

                    <textarea
                      bind:value={feedbackText}
                      placeholder={$currentLang === 'id' ? 'Catatan verifikasi auditor / dasar bukti...' : 'Auditor rationale / evidence note...'}
                      rows="2"
                      class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none"
                    ></textarea>

                    <div class="flex justify-end gap-1.5">
                      <button
                        type="button"
                        onclick={cancelEditing}
                        class="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:text-slate-900 rounded-lg text-xs font-medium cursor-pointer"
                      >
                        {$currentLang === 'id' ? 'Batal' : 'Cancel'}
                      </button>
                      <button
                        type="button"
                        onclick={() => saveFeedback(item)}
                        disabled={savingId === item.id}
                        class="px-3 py-1 bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-medium rounded-lg text-xs flex items-center gap-1 cursor-pointer disabled:opacity-50"
                      >
                        <Save size={12} />
                        <span>{savingId === item.id ? ($currentLang === 'id' ? 'Menyimpan...' : 'Saving...') : ($currentLang === 'id' ? 'Simpan' : 'Save')}</span>
                      </button>
                    </div>
                  </div>
                {:else}
                  <div class="flex items-start justify-between gap-1 group">
                    <div class="text-[11px] font-body text-slate-600 dark:text-slate-400 italic flex-1">
                      {item.auditor_feedback || ($currentLang === 'id' ? 'Belum ada catatan verifikasi' : 'No review notes recorded yet')}
                    </div>
                    <button
                      type="button"
                      onclick={() => startEditing(item)}
                      class="p-1 rounded-md text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                      title={$currentLang === 'id' ? 'Ubah penilaian' : 'Edit assessment'}
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
