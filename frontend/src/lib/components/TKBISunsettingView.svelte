<script>
  import { onMount } from 'svelte';
  import {
    Clock,
    Hourglass,
    Calendar,
    ShieldCheck,
    AlertTriangle,
    CheckCircle2,
    ArrowRight,
    Sparkles,
    Scale,
    FileText,
  } from '@lucide/svelte';
  import { fetchTKBIGrandfatheringScenarios } from '../api.js';
  import { t, currentLang } from '../i18n.js';

  let scenariosData = $state(null);
  let isLoading = $state(true);

  // Diagnostic form state
  let issueYear = $state(2023);
  let facilityTenorYears = $state(5);
  let oldVersionClass = $state('HIJAU');
  let newVersionClass = $state('TRANSISI');

  onMount(async () => {
    try {
      scenariosData = await fetchTKBIGrandfatheringScenarios();
    } catch (err) {
      console.error('Failed to load grandfathering scenarios:', err);
    } finally {
      isLoading = false;
    }
  });

  // Diagnostic logic based on OJK rules
  let diagnosticResult = $derived.by(() => {
    const maturityYear = issueYear + facilityTenorYears;
    const currentYear = 2026;
    const remainingTenorYears = Math.max(0, maturityYear - currentYear);

    let scenarioCode = 'Scenario A';
    let grandfatheringApplies = false;
    let allowedProtectionYears = 0;
    let rmtRequired = false;
    let actionRecommendation = '';

    if (oldVersionClass === 'HIJAU' && newVersionClass === 'HIJAU') {
      scenarioCode = 'Scenario A';
      grandfatheringApplies = true;
      allowedProtectionYears = remainingTenorYears;
      actionRecommendation = 'Status Hijau dipertahankan penuh tanpa perubahan kewajiban.';
    } else if (oldVersionClass === 'TRANSISI' && newVersionClass === 'TRANSISI') {
      scenarioCode = 'Scenario B';
      grandfatheringApplies = true;
      allowedProtectionYears = remainingTenorYears;
      actionRecommendation = 'Status Transisi dipertahankan. Tetap jalankan roadmap dekarbonisasi.';
    } else if (oldVersionClass === 'HIJAU' && newVersionClass === 'TRANSISI') {
      scenarioCode = 'Scenario C';
      grandfatheringApplies = true;
      allowedProtectionYears = Math.min(7, remainingTenorYears);
      actionRecommendation = `Proteksi Grandfathering berlaku selama ${allowedProtectionYears} tahun (maksimal 7 tahun atau hingga jatuh tempo tahun ${maturityYear}). Lakukan review roadmap hijau.`;
    } else if (oldVersionClass === 'TRANSISI' && newVersionClass === 'TIDAK MEMENUHI') {
      scenarioCode = 'Scenario D';
      grandfatheringApplies = false;
      rmtRequired = true;
      allowedProtectionYears = 3;
      actionRecommendation = 'Pembiayaan berisiko kehilangan label hijau. WAJIB menyusun program Remedial Measures to Transition (RMT) maksimal 3 tahun agar memperoleh status Transisi Interim.';
    } else if (oldVersionClass === 'HIJAU' && newVersionClass === 'TIDAK MEMENUHI') {
      scenarioCode = 'Scenario E';
      grandfatheringApplies = true;
      allowedProtectionYears = remainingTenorYears;
      actionRecommendation = `Proteksi berlaku hingga jatuh tempo kontrak awal (${maturityYear}). Saat perpanjangan/refinancing wajib diaudit ulang secara penuh.`;
    }

    return {
      scenarioCode,
      maturityYear,
      remainingTenorYears,
      grandfatheringApplies,
      allowedProtectionYears,
      rmtRequired,
      actionRecommendation,
    };
  });
</script>

<div class="space-y-6">
  <!-- Plain Explanation Top Callout -->
  <div class="p-4 rounded-xl bg-amber-50/80 dark:bg-[#201A10] border border-amber-200/90 dark:border-amber-800/80 flex items-start gap-3.5 text-xs shadow-2xs">
    <div class="p-2 rounded-lg bg-amber-100 dark:bg-amber-950/80 text-amber-700 dark:text-amber-400 shrink-0">
      <Hourglass size={18} />
    </div>
    <div class="space-y-1">
      <div class="font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
        <span>{$currentLang === 'id' ? 'Apa Fungsi Halaman Ini?' : 'What is this page for?'}</span>
        <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/60 text-amber-800 dark:text-amber-300 font-bold">
          {$currentLang === 'id' ? 'Masa Perlindungan Aturan' : 'Grace Period Rules'}
        </span>
      </div>
      <p class="text-slate-600 dark:text-slate-300 leading-relaxed font-body">
        {$currentLang === 'id'
          ? 'Halaman ini menjelaskan aturan masa tenggang (perlindungan). Ketika pemerintah atau OJK memperketat kriteria ramah lingkungan, proyek atau pinjaman lama yang sudah terlanjur berjalan tetap diakui sah (terlindungi hingga 7 tahun) agar bisnis memiliki waktu yang adil untuk berbenah.'
          : 'This page explains transition grace periods (Grandfathering & Sunsetting). When OJK updates and tightens green technical criteria, existing financing contracts remain legally protected for up to 7 years or until maturity, giving businesses fair transition time.'}
      </p>
    </div>
  </div>

  <!-- Top Banner -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800 flex items-center justify-center text-amber-700 dark:text-amber-400 shrink-0">
        <Hourglass size={24} />
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-xl font-headline font-bold text-slate-900 dark:text-slate-100">
            {$currentLang === 'id' ? 'Masa Transisi & Perlindungan (OJK)' : 'Mekanisme Grandfathering & Sunsetting'}
          </h1>
          <span class="font-mono text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/60 text-amber-800 dark:text-amber-300">
            OJK Pg. 6-8
          </span>
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-2xl">
          {$currentLang === 'id'
            ? 'Cek berapa tahun proyek Anda terlindungi dari perubahan standar teknis baru OJK.'
            : 'Ketentuan masa transisi perlindungan regulasi (hingga 7 tahun atau jatuh tempo tenor) saat kriteria teknis TSC diperbarui.'}
        </p>
      </div>
    </div>
  </div>

  <!-- 3 Regulatory Pillars Ribbon -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-4 shadow-sm flex items-start gap-3">
      <div class="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-950/60 text-[#047857] dark:text-[#34D399] shrink-0">
        <Clock size={18} />
      </div>
      <div>
        <span class="font-headline font-bold text-xs text-slate-900 dark:text-slate-100 block">
          Proteksi 7 Tahun (Unallocated)
        </span>
        <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 leading-relaxed font-body">
          Instrumen kredit &amp; pembiayaan umum yang belum dialokasikan penuh terlindungi hingga 7 tahun kalender dari perubahan ambang batas baru.
        </p>
      </div>
    </div>

    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-4 shadow-sm flex items-start gap-3">
      <div class="p-2 rounded-lg bg-blue-50 dark:bg-blue-950/60 text-[#1D4ED8] dark:text-[#60A5FA] shrink-0">
        <ShieldCheck size={18} />
      </div>
      <div>
        <span class="font-headline font-bold text-xs text-slate-900 dark:text-slate-100 block">
          Tenor Obligasi Hijau (Allocated)
        </span>
        <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 leading-relaxed font-body">
          Obligasi/Sukuk Tematik Berkelanjutan yang dananya telah dialokasikan tetap mempertahankan status label hijaunya sampai jatuh tempo (maturity).
        </p>
      </div>
    </div>

    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-4 shadow-sm flex items-start gap-3">
      <div class="p-2 rounded-lg bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-400 shrink-0">
        <Scale size={18} />
      </div>
      <div>
        <span class="font-headline font-bold text-xs text-slate-900 dark:text-slate-100 block">
          Mekanisme Sunsetting Berkala
        </span>
        <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 leading-relaxed font-body">
          Kriteria TSC disesuaikan bertahap menuju target penurunan emisi NDC 2030 dan NZE 2060, mencegah penguncian aset emisi tinggi (lock-in).
        </p>
      </div>
    </div>
  </div>

  <!-- Interactive Diagnostic Simulator -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm space-y-5">
    <div class="border-b border-slate-100 dark:border-slate-800 pb-3">
      <h2 class="text-base font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
        <Sparkles size={16} class="text-amber-600 dark:text-amber-400" />
        <span>Kalkulator Diagnostik Grandfathering Fasilitas Pembiayaan</span>
      </h2>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
        Periksa sisa masa tenggang perlindungan regulasi untuk kontrak pembiayaan / portofolio Anda.
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Input Controls -->
      <div class="lg:col-span-5 space-y-3.5">
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label for="issue-year-input" class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Tahun Akad Fasilitas
            </label>
            <input
              id="issue-year-input"
              type="number"
              bind:value={issueYear}
              min="2018"
              max="2026"
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs font-mono text-slate-900 dark:text-slate-100 focus:outline-none"
            />
          </div>

          <div>
            <label for="tenor-input" class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Tenor Kontrak (Tahun)
            </label>
            <input
              id="tenor-input"
              type="number"
              bind:value={facilityTenorYears}
              min="1"
              max="30"
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs font-mono text-slate-900 dark:text-slate-100 focus:outline-none"
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label for="old-version-select" class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Status Versi Lama
            </label>
            <select
              id="old-version-select"
              bind:value={oldVersionClass}
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs font-medium text-slate-900 dark:text-slate-100 focus:outline-none"
            >
              <option value="HIJAU">HIJAU</option>
              <option value="TRANSISI">TRANSISI</option>
            </select>
          </div>

          <div>
            <label for="new-version-select" class="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Evaluasi Versi Baru (TSC Baru)
            </label>
            <select
              id="new-version-select"
              bind:value={newVersionClass}
              class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs font-medium text-slate-900 dark:text-slate-100 focus:outline-none"
            >
              <option value="HIJAU">HIJAU</option>
              <option value="TRANSISI">TRANSISI</option>
              <option value="TIDAK MEMENUHI">TIDAK MEMENUHI</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Live Diagnosis Output Card -->
      <div class="lg:col-span-7 bg-slate-50 dark:bg-[#162032] rounded-xl p-5 border border-slate-100 dark:border-slate-800 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-700 pb-2.5">
          <span class="font-mono text-xs font-bold text-slate-500">
            Hasil Klasifikasi: <span class="text-[#047857] dark:text-[#34D399] font-black">{diagnosticResult.scenarioCode}</span>
          </span>
          <span class="font-mono text-xs text-slate-400">Jatuh Tempo: Thn {diagnosticResult.maturityYear}</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <div class="bg-white dark:bg-[#0F172A] p-2.5 rounded-lg border border-slate-200/80 dark:border-slate-800">
            <span class="text-[10px] font-mono text-slate-400 block">Sisa Tenor</span>
            <span class="font-mono text-sm font-bold text-slate-900 dark:text-slate-100">
              {diagnosticResult.remainingTenorYears} Tahun
            </span>
          </div>

          <div class="bg-white dark:bg-[#0F172A] p-2.5 rounded-lg border border-slate-200/80 dark:border-slate-800">
            <span class="text-[10px] font-mono text-slate-400 block">Proteksi Diberikan</span>
            <span class="font-mono text-sm font-bold {diagnosticResult.grandfatheringApplies ? 'text-[#047857] dark:text-[#34D399]' : 'text-rose-600 dark:text-rose-400'}">
              {diagnosticResult.allowedProtectionYears} Tahun
            </span>
          </div>

          <div class="bg-white dark:bg-[#0F172A] p-2.5 rounded-lg border border-slate-200/80 dark:border-slate-800 col-span-2 sm:col-span-1">
            <span class="text-[10px] font-mono text-slate-400 block">Syarat RMT 3 Tahun</span>
            <span class="font-mono text-sm font-bold {diagnosticResult.rmtRequired ? 'text-amber-600 dark:text-amber-400' : 'text-slate-600 dark:text-slate-300'}">
              {diagnosticResult.rmtRequired ? 'WAJIB RMT' : 'TIDAK PERLU'}
            </span>
          </div>
        </div>

        <div class="p-3 bg-white dark:bg-[#0F172A] rounded-lg border border-slate-200/80 dark:border-slate-800 text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-body">
          <span class="font-bold text-slate-900 dark:text-slate-100 block mb-0.5">Panduan Aksi Auditor OJK:</span>
          {diagnosticResult.actionRecommendation}
        </div>
      </div>
    </div>
  </div>

  <!-- 5 Official Scenarios Matrix -->
  {#if scenariosData?.scenarios}
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm space-y-4">
      <div class="border-b border-slate-100 dark:border-slate-800 pb-3">
        <h2 class="text-base font-headline font-bold text-slate-900 dark:text-slate-100">
          Matriks 5 Skenario Grandfathering OJK (Halaman 8)
        </h2>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
          Tinjauan lengkap implikasi hukum dan kewajiban pelaporan untuk setiap kemungkinan transisi status.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {#each scenariosData.scenarios as sc}
          <div class="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-slate-50/50 dark:bg-[#162032]/40 flex flex-col justify-between gap-3">
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-headline font-bold text-xs text-[#047857] dark:text-[#34D399]">
                  {sc.code}
                </span>
                <span class="font-mono text-[10px] text-slate-400">OJK Fact Sheet</span>
              </div>

              <!-- From -> To Badges -->
              <div class="flex items-center gap-1.5 text-xs font-mono font-bold">
                <span class="px-2 py-0.5 rounded bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 text-[10px]">
                  {sc.from_status}
                </span>
                <ArrowRight size={12} class="text-slate-400" />
                <span class="px-2 py-0.5 rounded bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 text-[10px]">
                  {sc.to_status}
                </span>
              </div>

              <p class="text-xs text-slate-700 dark:text-slate-300 font-body leading-relaxed">
                {sc.impact}
              </p>
            </div>

            <div class="pt-2 border-t border-slate-200/60 dark:border-slate-800/80 text-[11px] font-mono text-slate-500 dark:text-slate-400">
              <span class="font-bold text-slate-700 dark:text-slate-300">Tindakan: </span>
              <span>{sc.action_required}</span>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>
