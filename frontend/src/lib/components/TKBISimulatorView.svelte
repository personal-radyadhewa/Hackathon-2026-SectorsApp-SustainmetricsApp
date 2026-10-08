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
    { id: 'Energi', labelId: 'Energi', labelEn: 'Energy' },
    { id: 'Konstruksi dan Real Estat', labelId: 'Konstruksi dan Real Estat', labelEn: 'Construction & Real Estate' },
    { id: 'Transportasi dan Pergudangan', labelId: 'Transportasi dan Pergudangan', labelEn: 'Transportation & Storage' },
    { id: 'Pertanian, Kehutanan, dan Perikanan', labelId: 'Pertanian, Kehutanan, dan Perikanan', labelEn: 'Agriculture, Forestry & Fishing' },
    { id: 'Manufaktur', labelId: 'Manufaktur', labelEn: 'Manufacturing' },
    { id: 'Pengelolaan Air, Air Limbah, Sampah, dan Remediasi', labelId: 'Pengelolaan Air, Air Limbah, Sampah, dan Remediasi', labelEn: 'Water, Waste Management & Remediation' },
    { id: 'Informasi dan Komunikasi', labelId: 'Informasi dan Komunikasi', labelEn: 'Information & Communication' },
    { id: 'Aktivitas Profesional, Ilmiah, dan Teknis', labelId: 'Aktivitas Profesional, Ilmiah, dan Teknis', labelEn: 'Professional, Scientific & Technical Activities' },
  ];

  const eoOptions = [
    {
      id: 'EO1',
      nameId: 'EO1: Mitigasi Perubahan Iklim',
      nameEn: 'EO1: Climate Change Mitigation',
      descId: 'Pengurangan emisi GRK & efisiensi dekarbonisasi',
      descEn: 'GHG emission reduction & decarbonization efficiency'
    },
    {
      id: 'EO2',
      nameId: 'EO2: Adaptasi Perubahan Iklim',
      nameEn: 'EO2: Climate Change Adaptation',
      descId: 'Ketahanan terhadap bahaya iklim fisik & cuaca ekstrem',
      descEn: 'Resilience against physical climate hazards & extreme weather'
    },
    {
      id: 'EO3',
      nameId: 'EO3: Perlindungan Biodiversitas & Ekosistem',
      nameEn: 'EO3: Protection of Biodiversity & Ecosystems',
      descId: 'Konservasi keanekaragaman hayati & kualitas air/tanah',
      descEn: 'Conservation of biodiversity & water/soil quality'
    },
    {
      id: 'EO4',
      nameId: 'EO4: Ekonomi Sirkular & Pemanfaatan Sumber Daya',
      nameEn: 'EO4: Circular Economy & Resource Efficiency',
      descId: 'Daur ulang tertutup & efisiensi material',
      descEn: 'Closed-loop recycling & raw material efficiency'
    },
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
            {$currentLang === 'id' ? 'Identifikasi Aktivitas & Skala Usaha' : 'Activity & Business Scale Setup'}
          </span>
          <span class="text-[11px] font-mono text-slate-400">{$currentLang === 'id' ? 'Tahap 1 & 2' : 'Stages 1 & 2'}</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label for="sector-select" class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              {$currentLang === 'id' ? 'Sektor Ekonomi (8 Master Sektor)' : 'Economic Sector (8 Master Sectors)'}
            </label>
            <select
              id="sector-select"
              bind:value={sectorName}
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs font-medium text-slate-900 dark:text-slate-100 focus:outline-none"
            >
              {#each sectorsList as s}
                <option value={s.id}>{$currentLang === 'id' ? s.labelId : s.labelEn}</option>
              {/each}
            </select>
          </div>

          <div>
            <label for="activity-input" class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              {$currentLang === 'id' ? 'Nama Aktivitas / KBLI' : 'Activity Name / KBLI Code'}
            </label>
            <input
              id="activity-input"
              type="text"
              bind:value={activityName}
              placeholder={$currentLang === 'id' ? 'Contoh: PLTP Geothermal KBLI 35101' : 'e.g. Geothermal Power Plant KBLI 35101'}
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs text-slate-900 dark:text-slate-100 focus:outline-none"
            />
          </div>
        </div>

        <div>
          <span class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1.5">
            {$currentLang === 'id' ? 'Jalur Evaluasi Skala Usaha (PP No. 7/2021)' : 'Business Scale Assessment Path (PP No. 7/2021)'}
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
                <span>{$currentLang === 'id' ? 'Korporasi / Non-UMKM' : 'Corporate / Enterprise'}</span>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1 leading-tight">
                {$currentLang === 'id' ? 'Kriteria Teknis Kuantitatif (TSC) ambang batas emisi terstandar.' : 'Quantitative Technical Screening Criteria (TSC) emission thresholds.'}
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
                <span>{$currentLang === 'id' ? 'Koperasi & UMKM' : 'Cooperatives & MSMEs'}</span>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1 leading-tight">
                {$currentLang === 'id' ? 'Sector-Agnostic Decision Tree (SDT) berbasis prinsip sederhana.' : 'Sector-Agnostic Decision Tree (SDT) based on simple qualitative principles.'}
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
            {$currentLang === 'id' ? 'Tujuan Lingkungan Hidup Utama (Primary EO)' : 'Primary Environmental Objective (EO)'}
          </span>
          <span class="text-[11px] font-mono text-slate-400">{$currentLang === 'id' ? 'Tahap 3' : 'Stage 3'}</span>
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
              <div class="text-xs font-headline font-bold text-emerald-800 dark:text-emerald-300">
                {$currentLang === 'id' ? opt.nameId : opt.nameEn}
              </div>
              <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                {$currentLang === 'id' ? opt.descId : opt.descEn}
              </div>
            </button>
          {/each}
        </div>
      </div>

      <!-- Step 4: Technical Screening Criteria (Korporasi) vs SDT Questions (UMKM) -->
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm space-y-3">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <span class="font-mono text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-[#047857] text-white flex items-center justify-center text-[10px]">3</span>
            {scaleType === 'KORPORASI'
              ? ($currentLang === 'id' ? 'Uji Kriteria Teknis (TSC Screening)' : 'Technical Screening Criteria (TSC)')
              : ($currentLang === 'id' ? 'Pertanyaan Prinsip SDT (UMKM)' : 'MSME Checklist Questions (SDT)')}
          </span>
          <span class="text-[11px] font-mono text-slate-400">{$currentLang === 'id' ? 'Tahap 4' : 'Stage 4'}</span>
        </div>

        {#if scaleType === 'KORPORASI'}
          <div>
            <span class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-2">
              {$currentLang === 'id' ? 'Status Pemenuhan Ambang Batas Kuantitatif TSC:' : 'Quantitative TSC Threshold Compliance Status:'}
            </span>
            <div class="grid grid-cols-3 gap-2.5">
              <button
                type="button"
                onclick={() => (tscStatus = 'HIJAU')}
                class="p-2.5 rounded-lg border text-center cursor-pointer transition-all {tscStatus === 'HIJAU'
                  ? 'border-emerald-500 bg-emerald-50 text-emerald-900 font-bold dark:bg-emerald-950/60 dark:text-emerald-200'
                  : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032]'}"
              >
                <div class="text-xs">{$currentLang === 'id' ? 'Hijau (TSC Penuh)' : 'Green (Full TSC)'}</div>
                <div class="text-[10px] text-slate-500 font-mono mt-0.5">&lt; 100 gCO2e/kWh</div>
              </button>

              <button
                type="button"
                onclick={() => (tscStatus = 'TRANSISI')}
                class="p-2.5 rounded-lg border text-center cursor-pointer transition-all {tscStatus === 'TRANSISI'
                  ? 'border-amber-500 bg-amber-50 text-amber-900 font-bold dark:bg-amber-950/60 dark:text-amber-200'
                  : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032]'}"
              >
                <div class="text-xs">{$currentLang === 'id' ? 'Transisi (Roadmap)' : 'Transition (Roadmap)'}</div>
                <div class="text-[10px] text-slate-500 font-mono mt-0.5">{$currentLang === 'id' ? 'Pensiun Dini / Co-fire' : 'Early Phase-Out / Co-fire'}</div>
              </button>

              <button
                type="button"
                onclick={() => (tscStatus = 'TIDAK')}
                class="p-2.5 rounded-lg border text-center cursor-pointer transition-all {tscStatus === 'TIDAK'
                  ? 'border-rose-500 bg-rose-50 text-rose-900 font-bold dark:bg-rose-950/60 dark:text-rose-200'
                  : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032]'}"
              >
                <div class="text-xs">{$currentLang === 'id' ? 'Tidak Memenuhi' : 'Non-Compliant'}</div>
                <div class="text-[10px] text-slate-500 font-mono mt-0.5">{$currentLang === 'id' ? 'Melebihi Batas' : 'Exceeds Threshold'}</div>
              </button>
            </div>
          </div>
        {:else}
          <!-- UMKM SDT Questions -->
          <div class="space-y-2.5">
            <p class="text-xs text-slate-500 dark:text-slate-400">
              {$currentLang === 'id'
                ? 'Evaluasi langkah nyata efisiensi operasional dan ketahanan iklim sesuai prinsip SDT:'
                : 'Evaluate operational efficiency and climate resilience based on SDT principles:'}
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
            {$currentLang === 'id' ? '3 Kriteria Esensial (DNSH, RMT, & Sosial)' : '3 Essential Criteria (DNSH, RMT, & Social)'}
          </span>
          <span class="text-[11px] font-mono text-slate-400">{$currentLang === 'id' ? 'Tahap 5, 6, 7' : 'Stages 5, 6, 7'}</span>
        </div>

        <!-- DNSH Question -->
        <div class="p-3.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-[#162032]/40 space-y-2">
          <div class="flex items-center justify-between">
            <div>
              <span class="text-xs font-bold text-slate-800 dark:text-slate-200">
                {$currentLang === 'id' ? '1. Uji Kerugian Signifikan (Do No Significant Harm / DNSH)' : '1. Do No Significant Harm (DNSH) Test'}
              </span>
              <p class="text-[11px] text-slate-500 dark:text-slate-400">
                {$currentLang === 'id'
                  ? 'Apakah aktivitas menimbulkan bahaya/kerusakan signifikan terhadap salah satu dari 3 EO lainnya?'
                  : 'Does the activity cause significant damage or harm to any of the other 3 Environmental Objectives?'}
              </p>
            </div>
            <button
              type="button"
              onclick={() => (dnshHarm = !dnshHarm)}
              class="px-3 py-1 rounded-full text-xs font-mono font-bold cursor-pointer transition-colors {dnshHarm
                ? 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border border-rose-300'
                : 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300'}"
            >
              {dnshHarm
                ? ($currentLang === 'id' ? 'ADA ISU DNSH' : 'DNSH HARM')
                : ($currentLang === 'id' ? 'LOLOS (AMAN)' : 'PASSED (SAFE)')}
            </button>
          </div>

          <!-- RMT Unlock (Interim Transition 3 Years) -->
          {#if dnshHarm}
            <div class="mt-2 pt-2 border-t border-rose-200 dark:border-rose-900/60 flex items-center justify-between">
              <div>
                <span class="text-xs font-bold text-amber-900 dark:text-amber-300 flex items-center gap-1.5">
                  <Clock size={14} />
                  {$currentLang === 'id' ? 'Rencana Perbaikan Transisi (RMT Plan)' : 'Remedial Measures to Transition (RMT) Plan'}
                </span>
                <p class="text-[11px] text-amber-700 dark:text-amber-400">
                  {$currentLang === 'id'
                    ? 'Apakah entitas memiliki komitmen rencana mitigasi terikat maksimal 3 tahun kalender?'
                    : 'Does the entity commit to a binding remediation plan capped at 3 calendar years?'}
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
              {$currentLang === 'id' ? '2. Perlindungan Sosial Minimum (Social Safeguards)' : '2. Minimum Social Safeguards (Labor & Human Rights)'}
            </span>
            <p class="text-[11px] text-slate-500 dark:text-slate-400">
              {$currentLang === 'id'
                ? 'Kepatuhan penuh pada norma ketenagakerjaan, standar K3, HAM, dan perlindungan masyarakat terdampak.'
                : 'Full compliance with fair labor practices, occupational safety, human rights, and affected communities.'}
            </p>
          </div>
          <button
            type="button"
            onclick={() => (socialSafeguardsMet = !socialSafeguardsMet)}
            class="px-3 py-1 rounded-full text-xs font-mono font-bold cursor-pointer transition-colors {socialSafeguardsMet
              ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300'
              : 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border border-rose-300'}"
          >
            {socialSafeguardsMet
              ? ($currentLang === 'id' ? 'MEMENUHI' : 'COMPLIANT')
              : ($currentLang === 'id' ? 'GAGAL' : 'NON-COMPLIANT')}
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
            <span>{$currentLang === 'id' ? 'Mengevaluasi Flow OJK TKBI...' : 'Running OJK TKBI Decision Engine...'}</span>
          {:else}
            <Sparkles size={15} />
            <span>{$currentLang === 'id' ? 'Jalankan Evaluasi Keputusan OJK TKBI' : 'Run OJK TKBI Decision Engine'}</span>
          {/if}
        </button>
      </div>
    </div>

    <!-- Evaluation Result Panel -->
    <div class="lg:col-span-5 space-y-5">
      {#if evaluationResult}
        <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm space-y-5 sticky top-20">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <span class="font-mono text-xs uppercase font-bold text-slate-400">
              {$currentLang === 'id' ? 'Hasil Klasifikasi OJK' : 'OJK Classification Result'}
            </span>
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
              {evaluationResult.classification === 'HIJAU'
                ? ($currentLang === 'id' ? 'HIJAU' : 'GREEN')
                : evaluationResult.classification === 'TRANSISI'
                ? ($currentLang === 'id' ? 'TRANSISI' : 'TRANSITION')
                : evaluationResult.classification === 'TRANSISI INTERIM'
                ? ($currentLang === 'id' ? 'TRANSISI INTERIM' : 'INTERIM TRANSITION')
                : ($currentLang === 'id' ? 'TIDAK MEMENUHI' : 'NON-COMPLIANT')}
            </div>

            {#if evaluationResult.rmt_clock_years > 0}
              <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-200/60 dark:bg-sky-900/60 text-sky-900 dark:text-sky-200 font-mono text-[11px] font-bold">
                <Clock size={13} />
                <span>{$currentLang === 'id' ? 'Masa Transisi Interim: Maksimal 3 Tahun RMT' : 'Interim Transition Window: Max 3-Year RMT'}</span>
              </div>
            {/if}
          </div>

          <!-- Step-by-Step Decision Breadcrumb -->
          <div class="space-y-2">
            <span class="font-mono text-[10px] uppercase font-bold text-slate-400">
              {$currentLang === 'id' ? 'Jejak Logika Keputusan:' : 'Decision Logic Path:'}
            </span>
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
            <span class="font-bold text-[#047857] dark:text-[#34D399] block mb-1">
              {$currentLang === 'id' ? 'Catatan Kepatuhan OJK:' : 'OJK Compliance Note:'}
            </span>
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
            {$currentLang === 'id' ? 'Simulator Siap Dijalankan' : 'Simulator Ready to Run'}
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 max-w-xs mx-auto leading-relaxed">
            {$currentLang === 'id'
              ? 'Sesuaikan parameter di sebelah kiri, lalu klik tombol "Jalankan Evaluasi Keputusan OJK TKBI" untuk melihat hasil klasifikasi trafik light secara presisi.'
              : 'Configure the parameters on the left, then click "Run OJK TKBI Decision Engine" to view the exact traffic light classification.'}
          </p>
        </div>
      {/if}
    </div>
  </div>
</div>
