<script>
  import { onMount } from 'svelte';
  import {
    Sliders,
    CheckCircle2,
    AlertTriangle,
    XCircle,
    Clock,
    ShieldCheck,
    Layers,
    Sparkles,
    ArrowRight,
    RotateCcw,
    Info,
    HelpCircle,
    Building2,
    Briefcase,
  } from '@lucide/svelte';
  import { evaluateTKBISimulator, fetchTKBISDTCatalog } from '../api.js';
  import { t, currentLang } from '../i18n.js';

  let scaleType = $state('KORPORASI'); // KORPORASI or UMKM
  let sectorName = $state('Energi');
  let activityName = $state('Pembangkitan Listrik Tenaga Panas Bumi (PLTP)');
  let eoPrimary = $state('EO1');
  let tscStatus = $state('HIJAU'); // HIJAU, TRANSISI, TIDAK
  let dnshHarm = $state(false);
  let hasRmt = $state(false);
  let socialSafeguardsMet = $state(true);

  // UMKM SDT State
  let sdtCatalog = $state(null);
  let eoAnswers = $state({});
  let dnshAnswers = $state({});
  let socialAnswers = $state({});

  // Result state
  let isEvaluating = $state(false);
  let evaluationResult = $state(null);
  let errorMsg = $state(null);

  const sectorsList = [
    'Energi',
    'Konstruksi dan Real Estat',
    'Transportasi dan Pergudangan',
    'Pertanian, Kehutanan, dan Perikanan',
    'Manufaktur',
    'Pengelolaan Air, Air Limbah, Sampah, dan Remediasi',
    'Informasi dan Komunikasi',
    'Aktivitas Profesional, Ilmiah, dan Teknis',
  ];

  const eoOptions = [
    { id: 'EO1', name: 'EO1: Mitigasi Perubahan Iklim', desc: 'Pengurangan emisi GRK & efisiensi dekarbonisasi' },
    { id: 'EO2', name: 'EO2: Adaptasi Perubahan Iklim', desc: 'Ketahanan terhadap bahaya iklim fisik & ekstrem' },
    { id: 'EO3', name: 'EO3: Perlindungan Biodiversitas & Ekosistem', desc: 'Konservasi keanekaragaman hayati & kualitas air/tanah' },
    { id: 'EO4', name: 'EO4: Ekonomi Sirkular & Pemanfaatan Sumber Daya', desc: 'Daur ulang tertutup & efisiensi material' },
  ];

  onMount(async () => {
    try {
      sdtCatalog = await fetchTKBISDTCatalog();
      initDefaultAnswers();
    } catch (e) {
      console.error('Failed to load SDT catalog:', e);
    }
  });

  function initDefaultAnswers() {
    if (!sdtCatalog) return;
    const currentEoQs = sdtCatalog.criteria?.[eoPrimary]?.questions || [];
    currentEoQs.forEach((q) => {
      eoAnswers[q.id] = true;
    });
    (sdtCatalog.dnsh_questions || []).forEach((q) => {
      dnshAnswers[q.id] = true;
    });
    (sdtCatalog.social_questions || []).forEach((q) => {
      socialAnswers[q.id] = true;
    });
  }

  $effect(() => {
    if (eoPrimary && sdtCatalog) {
      initDefaultAnswers();
    }
  });

  async function handleRunEvaluation() {
    isEvaluating = true;
    errorMsg = null;
    try {
      const payload = {
        scale_type: scaleType,
        sector_name: sectorName,
        activity_name: activityName,
        eo_primary: eoPrimary,
        tsc_status: tscStatus,
        dnsh_harm: dnshHarm,
        has_rmt: hasRmt,
        social_aspects_met: socialSafeguardsMet,
        eo_answers: eoAnswers,
        dnsh_answers: dnshAnswers,
        social_answers: socialAnswers,
      };
      const res = await evaluateTKBISimulator(payload);
      evaluationResult = res;
    } catch (err) {
      errorMsg = err.message || 'Evaluasi simulator gagal.';
    } finally {
      isEvaluating = false;
    }
  }

  function handleReset() {
    scaleType = 'KORPORASI';
    sectorName = 'Energi';
    activityName = 'Pembangkitan Listrik Tenaga Panas Bumi (PLTP)';
    eoPrimary = 'EO1';
    tscStatus = 'HIJAU';
    dnshHarm = false;
    hasRmt = false;
    socialSafeguardsMet = true;
    evaluationResult = null;
    initDefaultAnswers();
  }
</script>

<div class="space-y-6">
  <!-- Plain Explanation Top Callout -->
  <div class="p-4 rounded-xl bg-emerald-50/80 dark:bg-[#112028] border border-emerald-200/90 dark:border-emerald-800/80 flex items-start gap-3.5 text-xs shadow-2xs">
    <div class="p-2 rounded-lg bg-emerald-100 dark:bg-emerald-950/80 text-[#047857] dark:text-[#34D399] shrink-0">
      <HelpCircle size={18} />
    </div>
    <div class="space-y-1">
      <div class="font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
        <span>{$currentLang === 'id' ? 'Apa Fungsi Halaman Ini?' : 'What is this page for?'}</span>
        <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-[#047857] dark:text-[#34D399] font-bold">
          {$currentLang === 'id' ? 'Panduan Cepat' : 'Quick Guide'}
        </span>
      </div>
      <p class="text-slate-600 dark:text-slate-300 leading-relaxed font-body">
        {$currentLang === 'id'
          ? 'Halaman ini adalah simulator uji cepat. Fungsinya untuk mengetes apakah kegiatan usaha Anda masuk kategori HIJAU (ramah lingkungan), KUNING (sedang berbenah/transisi), atau MERAH (belum memenuhi syarat). Anda cukup memilih sektor usaha dan mengisi pertanyaan sederhana di bawah.'
          : 'This page is a quick-test simulator. It tests whether a business activity qualifies as GREEN (eco-friendly), YELLOW (transition/improving), or RED (non-compliant) based on official OJK criteria. Simply pick your sector and answer the simple questions below.'}
      </p>
    </div>
  </div>

  <!-- Top Banner -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-[#047857] dark:text-[#34D399] shrink-0">
        <Sliders size={24} />
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-xl font-headline font-bold text-slate-900 dark:text-slate-100">
            {$currentLang === 'id' ? 'Simulasi Aturan Hijau (OJK)' : 'TKBI Decision Tree Simulator'}
          </h1>
          <span class="font-mono text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300">
            OJK Pg. 23
          </span>
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-2xl">
          {$currentLang === 'id'
            ? 'Uji alur verifikasi klasifikasi hijau sesuai kriteria lingkungan & perlindungan sosial.'
            : 'Simulate green and transition verification flow according to environmental objectives and safeguards.'}
        </p>
      </div>
    </div>

    <button
      type="button"
      onclick={handleReset}
      class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-mono text-slate-600 dark:text-slate-300 self-start md:self-auto cursor-pointer"
    >
      <RotateCcw size={13} />
      <span>{$currentLang === 'id' ? 'Reset Pilihan' : 'Reset Inputs'}</span>
    </button>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
    <!-- Simulator Form (Steps 1 to 7) -->
    <div class="lg:col-span-7 space-y-5">
      <!-- Step 1 & 2: Identifikasi Aktivitas & Skala Usaha -->
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <span class="font-mono text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-[#047857] text-white flex items-center justify-center text-[10px]">1</span>
            Identifikasi Aktivitas &amp; Skala Usaha
          </span>
          <span class="text-[11px] font-mono text-slate-400">Tahap 1 &amp; 2</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label for="sector-select" class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Sektor Ekonomi (8 Master Sektor)
            </label>
            <select
              id="sector-select"
              bind:value={sectorName}
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs font-medium text-slate-900 dark:text-slate-100 focus:outline-none"
            >
              {#each sectorsList as s}
                <option value={s}>{s}</option>
              {/each}
            </select>
          </div>

          <div>
            <label for="activity-input" class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Nama Aktivitas / KBLI
            </label>
            <input
              id="activity-input"
              type="text"
              bind:value={activityName}
              placeholder="Contoh: PLTP Geothermal KBLI 35101"
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs text-slate-900 dark:text-slate-100 focus:outline-none"
            />
          </div>
        </div>

        <div>
          <span class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1.5">
            Jalur Evaluasi Skala Usaha (PP No. 7/2021)
          </span>
          <div class="grid grid-cols-2 gap-3">
            <button
              type="button"
              onclick={() => (scaleType = 'KORPORASI')}
              class="p-3 rounded-lg border text-left cursor-pointer transition-all {scaleType === 'KORPORASI'
                ? 'border-[#047857] bg-emerald-50/50 dark:bg-emerald-950/30 text-emerald-900 dark:text-emerald-200'
                : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032]'}"
            >
              <div class="font-headline font-bold text-xs flex items-center gap-1.5">
                <Building2 size={14} class="text-[#047857] dark:text-[#34D399]" />
                <span>Korporasi / Non-UMKM</span>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1 leading-tight">
                Kriteria Teknis Kuantitatif (TSC) ambang batas emisi terstandar.
              </p>
            </button>

            <button
              type="button"
              onclick={() => (scaleType = 'UMKM')}
              class="p-3 rounded-lg border text-left cursor-pointer transition-all {scaleType === 'UMKM'
                ? 'border-[#047857] bg-emerald-50/50 dark:bg-emerald-950/30 text-emerald-900 dark:text-emerald-200'
                : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032]'}"
            >
              <div class="font-headline font-bold text-xs flex items-center gap-1.5">
                <Briefcase size={14} class="text-[#047857] dark:text-[#34D399]" />
                <span>Koperasi &amp; UMKM</span>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1 leading-tight">
                Sector-Agnostic Decision Tree (SDT) berbasis prinsip sederhana.
              </p>
            </button>
          </div>
        </div>
      </div>

      <!-- Step 3: Environmental Objective (EO) -->
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm space-y-3">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <span class="font-mono text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-[#047857] text-white flex items-center justify-center text-[10px]">2</span>
            Tujuan Lingkungan Hidup Utama (Primary EO)
          </span>
          <span class="text-[11px] font-mono text-slate-400">Tahap 3</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          {#each eoOptions as opt}
            <button
              type="button"
              onclick={() => (eoPrimary = opt.id)}
              class="p-2.5 rounded-lg border text-left cursor-pointer transition-all {eoPrimary === opt.id
                ? 'border-[#047857] bg-emerald-50/40 dark:bg-emerald-950/30 text-slate-900 dark:text-slate-100 font-semibold'
                : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032] text-slate-700 dark:text-slate-300'}"
            >
              <div class="text-xs font-headline font-bold text-emerald-800 dark:text-emerald-300">{opt.name}</div>
              <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">{opt.desc}</div>
            </button>
          {/each}
        </div>
      </div>

      <!-- Step 4: Technical Screening Criteria (Korporasi) vs SDT Questions (UMKM) -->
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm space-y-3">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <span class="font-mono text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-[#047857] text-white flex items-center justify-center text-[10px]">3</span>
            {scaleType === 'KORPORASI' ? 'Uji Kriteria Teknis (TSC Screening)' : 'Pertanyaan Prinsip SDT (UMKM)'}
          </span>
          <span class="text-[11px] font-mono text-slate-400">Tahap 4</span>
        </div>

        {#if scaleType === 'KORPORASI'}
          <div>
            <span class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-2">
              Status Pemenuhan Ambang Batas Kuantitatif TSC:
            </span>
            <div class="grid grid-cols-3 gap-2.5">
              <button
                type="button"
                onclick={() => (tscStatus = 'HIJAU')}
                class="p-2.5 rounded-lg border text-center cursor-pointer transition-all {tscStatus === 'HIJAU'
                  ? 'border-emerald-500 bg-emerald-50 text-emerald-900 font-bold dark:bg-emerald-950/60 dark:text-emerald-200'
                  : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032]'}"
              >
                <div class="text-xs">Hijau (TSC Penuh)</div>
                <div class="text-[10px] text-slate-500 font-mono mt-0.5">&lt; 100 gCO2e/kWh</div>
              </button>

              <button
                type="button"
                onclick={() => (tscStatus = 'TRANSISI')}
                class="p-2.5 rounded-lg border text-center cursor-pointer transition-all {tscStatus === 'TRANSISI'
                  ? 'border-amber-500 bg-amber-50 text-amber-900 font-bold dark:bg-amber-950/60 dark:text-amber-200'
                  : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032]'}"
              >
                <div class="text-xs">Transisi (Roadmap)</div>
                <div class="text-[10px] text-slate-500 font-mono mt-0.5">Pensiun Dini / Co-fire</div>
              </button>

              <button
                type="button"
                onclick={() => (tscStatus = 'TIDAK')}
                class="p-2.5 rounded-lg border text-center cursor-pointer transition-all {tscStatus === 'TIDAK'
                  ? 'border-rose-500 bg-rose-50 text-rose-900 font-bold dark:bg-rose-950/60 dark:text-rose-200'
                  : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032]'}"
              >
                <div class="text-xs">Tidak Memenuhi</div>
                <div class="text-[10px] text-slate-500 font-mono mt-0.5">Melebihi Batas</div>
              </button>
            </div>
          </div>
        {:else}
          <!-- UMKM SDT Questions -->
          <div class="space-y-2.5">
            <p class="text-xs text-slate-500 dark:text-slate-400">
              Evaluasi langkah nyata efisiensi operasional dan ketahanan iklim sesuai prinsip SDT:
            </p>
            {#if sdtCatalog?.criteria?.[eoPrimary]?.questions}
              {#each sdtCatalog.criteria[eoPrimary].questions as q}
                <label class="flex items-start gap-2.5 p-2 rounded-lg bg-slate-50 dark:bg-[#162032] border border-slate-100 dark:border-slate-800 cursor-pointer">
                  <input
                    type="checkbox"
                    bind:checked={eoAnswers[q.id]}
                    class="mt-1 rounded text-[#047857] focus:ring-[#047857]"
                  />
                  <div>
                    <span class="text-xs font-medium text-slate-800 dark:text-slate-200">{q.question}</span>
                    <span class="block text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">{q.guidance}</span>
                  </div>
                </label>
              {/each}
            {/if}
          </div>
        {/if}
      </div>

      <!-- Step 5, 6, 7: DNSH, RMT & Aspek Sosial -->
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <span class="font-mono text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-[#047857] text-white flex items-center justify-center text-[10px]">4</span>
            3 Essential Criteria (DNSH, RMT, &amp; Sosial)
          </span>
          <span class="text-[11px] font-mono text-slate-400">Tahap 5, 6, 7</span>
        </div>

        <!-- DNSH Question -->
        <div class="p-3.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-[#162032]/40 space-y-2">
          <div class="flex items-center justify-between">
            <div>
              <span class="text-xs font-bold text-slate-800 dark:text-slate-200">
                1. Uji Kerugian Signifikan (Do No Significant Harm / DNSH)
              </span>
              <p class="text-[11px] text-slate-500 dark:text-slate-400">
                Apakah aktivitas menimbulkan bahaya/kerusakan signifikan terhadap salah satu dari 3 EO lainnya?
              </p>
            </div>
            <button
              type="button"
              onclick={() => (dnshHarm = !dnshHarm)}
              class="px-3 py-1 rounded-full text-xs font-mono font-bold cursor-pointer transition-colors {dnshHarm
                ? 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border border-rose-300'
                : 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300'}"
            >
              {dnshHarm ? 'ADA ISU DNSH' : 'LOLOS (AMAN)'}
            </button>
          </div>

          <!-- RMT Unlock (Interim Transition 3 Years) -->
          {#if dnshHarm}
            <div class="mt-2 pt-2 border-t border-rose-200 dark:border-rose-900/60 flex items-center justify-between">
              <div>
                <span class="text-xs font-bold text-amber-900 dark:text-amber-300 flex items-center gap-1.5">
                  <Clock size={14} />
                  Remedial Measures to Transition (RMT) Plan
                </span>
                <p class="text-[11px] text-amber-700 dark:text-amber-400">
                  Apakah entitas memiliki komitmen rencana mitigasi terikat maksimal 3 tahun kalender?
                </p>
              </div>
              <input
                type="checkbox"
                bind:checked={hasRmt}
                class="w-5 h-5 rounded text-amber-600 focus:ring-amber-500"
              />
            </div>
          {/if}
        </div>

        <!-- Social Safeguards -->
        <div class="p-3.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-[#162032]/40 flex items-center justify-between">
          <div>
            <span class="text-xs font-bold text-slate-800 dark:text-slate-200 flex items-center gap-1.5">
              <ShieldCheck size={14} class="text-[#047857] dark:text-[#34D399]" />
              2. Minimum Social Safeguards (Aspek Sosial Esensial)
            </span>
            <p class="text-[11px] text-slate-500 dark:text-slate-400">
              Kepatuhan penuh pada norma ketenagakerjaan, standar K3, HAM, dan perlindungan masyarakat terdampak.
            </p>
          </div>
          <button
            type="button"
            onclick={() => (socialSafeguardsMet = !socialSafeguardsMet)}
            class="px-3 py-1 rounded-full text-xs font-mono font-bold cursor-pointer transition-colors {socialSafeguardsMet
              ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300'
              : 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border border-rose-300'}"
          >
            {socialSafeguardsMet ? 'MEMENUHI' : 'GAGAL'}
          </button>
        </div>

        <button
          type="button"
          onclick={handleRunEvaluation}
          disabled={isEvaluating}
          class="w-full py-2.5 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-headline font-bold text-xs flex items-center justify-center gap-2 shadow-xs cursor-pointer disabled:opacity-50"
        >
          {#if isEvaluating}
            <div class="w-4 h-4 border-2 border-white dark:border-[#064E3B] border-t-transparent rounded-full animate-spin"></div>
            <span>Mengevaluasi Flow OJK TKBI...</span>
          {:else}
            <Sparkles size={15} />
            <span>Jalankan Evaluasi Keputusan OJK TKBI</span>
          {/if}
        </button>
      </div>
    </div>

    <!-- Evaluation Result Panel -->
    <div class="lg:col-span-5 space-y-5">
      {#if evaluationResult}
        <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm space-y-5 sticky top-20">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <span class="font-mono text-xs uppercase font-bold text-slate-400">Hasil Klasifikasi OJK</span>
            <span class="font-mono text-[10px] px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
              {evaluationResult.tier}
            </span>
          </div>

          <!-- Traffic Light Badge Banner -->
          <div class="p-5 rounded-xl text-center space-y-2 border {evaluationResult.classification === 'HIJAU'
            ? 'bg-emerald-50 text-emerald-950 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-100 dark:border-emerald-800'
            : evaluationResult.classification === 'TRANSISI'
            ? 'bg-amber-50 text-amber-950 border-amber-200 dark:bg-amber-950/40 dark:text-amber-100 dark:border-amber-800'
            : evaluationResult.classification === 'TRANSISI INTERIM'
            ? 'bg-sky-50 text-sky-950 border-sky-200 dark:bg-sky-950/40 dark:text-sky-100 dark:border-sky-800'
            : 'bg-rose-50 text-rose-950 border-rose-200 dark:bg-rose-950/40 dark:text-rose-100 dark:border-rose-800'}">
            
            <div class="text-2xl font-headline font-black tracking-tight">
              {evaluationResult.classification}
            </div>

            {#if evaluationResult.rmt_clock_years > 0}
              <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-200/60 dark:bg-sky-900/60 text-sky-900 dark:text-sky-200 font-mono text-[11px] font-bold">
                <Clock size={13} />
                <span>Masa Transisi Interim: Maksimal 3 Tahun RMT</span>
              </div>
            {/if}
          </div>

          <!-- Step-by-Step Decision Breadcrumb -->
          <div class="space-y-2">
            <span class="font-mono text-[10px] uppercase font-bold text-slate-400">Jejak Logika Keputusan:</span>
            <div class="bg-slate-50 dark:bg-[#162032] p-3 rounded-lg border border-slate-100 dark:border-slate-800 space-y-1.5">
              {#each evaluationResult.decision_path as step}
                <div class="text-xs font-mono text-slate-700 dark:text-slate-300 flex items-start gap-2">
                  <span class="text-[#047857] dark:text-[#34D399] mt-0.5">→</span>
                  <span>{step}</span>
                </div>
              {/each}
            </div>
          </div>

          <!-- Official Regulatory Reasoning -->
          <div class="p-3.5 rounded-lg bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800 text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
            <span class="font-bold text-[#047857] dark:text-[#34D399] block mb-1">Catatan Kepatuhan OJK:</span>
            {evaluationResult.reasoning}
          </div>
        </div>
      {:else}
        <!-- Simulator Empty Guide State -->
        <div class="bg-white dark:bg-[#0F172A] border border-dashed border-slate-300 dark:border-slate-700 rounded-xl p-8 text-center space-y-3 sticky top-20">
          <div class="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-400 mx-auto">
            <Layers size={24} />
          </div>
          <h3 class="text-sm font-headline font-bold text-slate-800 dark:text-slate-200">
            Simulator Siap Dijalankan
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 max-w-xs mx-auto leading-relaxed">
            Sesuaikan parameter di sebelah kiri, lalu klik tombol "Jalankan Evaluasi Keputusan OJK TKBI" untuk melihat hasil klasifikasi trafik light secara presisi.
          </p>
        </div>
      {/if}
    </div>
  </div>
</div>
