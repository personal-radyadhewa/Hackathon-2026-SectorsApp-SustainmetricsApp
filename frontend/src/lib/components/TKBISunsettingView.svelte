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
    TrendingDown,
    Building2,
    DollarSign,
    Check,
    ChevronRight,
    AlertOctagon,
  } from '@lucide/svelte';
  import { fetchTKBIGrandfatheringScenarios } from '../api.js';
  import { t, currentLang } from '../i18n.js';

  let scenariosData = $state(null);
  let isLoading = $state(true);

  // Diagnostic form state for Auditor / Fund Manager
  let instrumentType = $state('BOND'); // 'BOND' (Obligasi Hijau / Sukuk), 'SYNDICATED' (Pinjaman Bertarget / Sindikasi), 'GENERAL' (Fasilitas Kredit Umum)
  let contractAmountMiliar = $state(2500); // Rp 2,500 Miliar = Rp 2.5 Trillion
  let issueYear = $state(2023);
  let facilityTenorYears = $state(7);
  let oldVersionClass = $state('HIJAU');
  let newVersionClass = $state('HIJAU');

  // Real-world Presets for Fund Managers & Auditors
  const PRESETS = [
    {
      id: 'pgeo',
      badge: 'Obligasi Hijau',
      label: 'PGEO Green Bond 2023',
      type: 'BOND',
      name: 'Obligasi Hijau Berkelanjutan PGEO Tahap I',
      amount: 2500,
      issue: 2023,
      tenor: 7,
      oldTier: 'HIJAU',
      newTier: 'HIJAU',
      desc: '100% dialokasikan ke energi panas bumi. Standar tetap terpenuhi penuh.',
    },
    {
      id: 'syndicated',
      badge: 'Sindikasi Bank',
      label: 'Kredit Dekarbonisasi Pabrik',
      type: 'SYNDICATED',
      name: 'Pinjaman Sindikasi Efisiensi Energi & Solar PV',
      amount: 1200,
      issue: 2022,
      tenor: 6,
      oldTier: 'HIJAU',
      newTier: 'TRANSISI',
      desc: 'Ambang batas TSC baru diperketat. Berlaku proteksi OJK maksimal 7 tahun.',
    },
    {
      id: 'coal_rmt',
      badge: 'Transisi Batubara',
      label: 'Early Retirement PLTU (RMT 3 Thn)',
      type: 'SYNDICATED',
      name: 'Pembiayaan Transisi Phase-out PLTU Batubara',
      amount: 850,
      issue: 2023,
      tenor: 5,
      oldTier: 'TRANSISI',
      newTier: 'TIDAK MEMENUHI',
      desc: 'Emisi melebihi ambang baru. Wajib menyusun RMT 3 tahun agar tidak delisted.',
    },
    {
      id: 'general_credit',
      badge: 'Kredit Umum',
      label: 'General Corporate Loan Line',
      type: 'GENERAL',
      name: 'Fasilitas Modal Kerja Korporasi Umum',
      amount: 600,
      issue: 2024,
      tenor: 8,
      oldTier: 'HIJAU',
      newTier: 'TRANSISI',
      desc: 'Fasilitas kredit belum dialokasikan penuh. Proteksi dibatasi maksimal 7 tahun.',
    },
  ];

  function applyPreset(p) {
    instrumentType = p.type;
    contractAmountMiliar = p.amount;
    issueYear = p.issue;
    facilityTenorYears = p.tenor;
    oldVersionClass = p.oldTier;
    newVersionClass = p.newTier;
  }

  onMount(async () => {
    try {
      scenariosData = await fetchTKBIGrandfatheringScenarios();
    } catch (err) {
      console.error('Failed to load grandfathering scenarios:', err);
    } finally {
      isLoading = false;
    }
  });

  // Regulatory Logic: OJK TKBI Fact Sheet Pages 6-8
  let diagnosticResult = $derived.by(() => {
    const maturityYear = issueYear + facilityTenorYears;
    const currentYear = 2026;
    const remainingTenorYears = Math.max(0, maturityYear - currentYear);

    let scenarioCode = 'Skenario A (OJK Pg. 8)';
    let protectionType = 'FULL_MATURITY'; // FULL_MATURITY, CAPPED_7_YEARS, RMT_3_YEARS, LOST
    let protectedYears = remainingTenorYears;
    let rmtRequired = false;
    let riskLevel = 'LOW'; // 'LOW', 'MEDIUM', 'HIGH'
    let statusBadgeText = '';
    let fundVerdictTitle = '';
    let fundActionSummary = '';
    let auditorChecklist = [];

    // Rule 1: Allocated Green Bonds retain status until contractual maturity (Page 6)
    if (instrumentType === 'BOND' && oldVersionClass === 'HIJAU') {
      scenarioCode = newVersionClass === 'HIJAU' ? 'Skenario A (OJK Pg. 8)' : 'Skenario C / E (OJK Pg. 8)';
      protectionType = 'FULL_MATURITY';
      protectedYears = remainingTenorYears;
      riskLevel = newVersionClass === 'HIJAU' ? 'LOW' : 'MEDIUM';
      statusBadgeText = 'PROTEKSI PENUH HINGGA JATUH TEMPO OBLIGASI';
      fundVerdictTitle = 'Status Hijau Aman 100% Sepanjang Tenor Obligasi';
      fundActionSummary = `Berdasarkan POJK & TKBI Hal. 6, Obligasi Hijau/Sukuk yang dananya telah dialokasikan (allocated) mempertahankan label hijau sah hingga jatuh tempo tahun ${maturityYear}. Portofolio dana kelolaan TIDAK terdampak penurunan rating seketika.`;
      auditorChecklist = [
        'Konfirmasi alokasi dana (Use of Proceeds) telah diaudit dan terealisasi 100% pada proyek hijau awal.',
        'Pertahankan pencatatan Green Bond pada rasio portofolio hijau berkelanjutan tanpa reklasifikasi.',
        `Saat jatuh tempo tahun ${maturityYear}, fasilitas penerbitan obligasi baru WAJIB diaudit mengacu pada TSC Versi 3 terbaru.`,
      ];
    } else if (oldVersionClass === 'HIJAU' && newVersionClass === 'HIJAU') {
      scenarioCode = 'Skenario A (OJK Pg. 8)';
      protectionType = 'FULL_MATURITY';
      protectedYears = remainingTenorYears;
      riskLevel = 'LOW';
      statusBadgeText = 'AMAN: KRITERIA HIJAU TETAP TERPENUHI';
      fundVerdictTitle = 'Kepatuhan Hijau Tidak Berubah (Zero Downgrade Risk)';
      fundActionSummary = 'Aktivitas pembiayaan secara konsisten memenuhi kriteria teknis TSC Versi terbaru. Tidak ada risiko penurunan label hijau atau kewajiban pelaporan khusus.';
      auditorChecklist = [
        'Lakukan verifikasi berkala atas data emisi dan DNSH pada Laporan Keberlanjutan tahunan debitur.',
        'Pertahankan pembobotan portofolio hijau 100% pada rasio pembiayaan berkelanjutan institusi.',
      ];
    } else if (oldVersionClass === 'TRANSISI' && newVersionClass === 'TRANSISI') {
      scenarioCode = 'Skenario B (OJK Pg. 8)';
      protectionType = 'FULL_MATURITY';
      protectedYears = remainingTenorYears;
      riskLevel = 'LOW';
      statusBadgeText = 'AMAN: STATUS TRANSISI BERKELANJUTAN';
      fundVerdictTitle = 'Lintasan Transisi Berjalan Normal';
      fundActionSummary = 'Aktivitas tetap tergolong Transisi Terverifikasi. Debitur berada pada lintasan penurunan emisi yang sah dan dilindungi regulasi OJK.';
      auditorChecklist = [
        'Pantau milestone dekarbonisasi tahunan sesuai dokumen roadmap awal.',
        'Pastikan kepatuhan prinsip Do No Significant Harm (DNSH) terhadap keanekaragaman hayati dan pencegahan polusi.',
      ];
    } else if (oldVersionClass === 'HIJAU' && newVersionClass === 'TRANSISI') {
      scenarioCode = 'Skenario C (OJK Pg. 8)';
      protectedYears = Math.min(7, remainingTenorYears);
      protectionType = 'CAPPED_7_YEARS';
      riskLevel = 'MEDIUM';
      statusBadgeText = `MASA TENGGANG ${protectedYears} TAHUN (CAP MAKSIMAL 7 TAHUN)`;
      fundVerdictTitle = 'Terlindungi Grandfathering (Hingga 7 Tahun OJK)';
      fundActionSummary = `Standar TSC diperketat sehingga aktivitas turun ke kategori Transisi. Sesuai regulasi OJK Hal. 7, pembiayaan ini diberikan masa tenggang perlindungan hingga ${protectedYears} tahun kalender untuk mencegah disrupsi portofolio.`;
      auditorChecklist = [
        `Berikan notifikasi resmi kepada debitur bahwa batas proteksi masa tenggang berlaku hingga tahun ${2026 + protectedYears}.`,
        'Minta debitur menyusun rencana aksi penyesuaian teknologi/efisiensi sebelum masa proteksi 7 tahun berakhir.',
        'Setelah tahun ke-7 berakhir, sisa pembiayaan otomatis direklasifikasi menjadi kategori Transisi.',
      ];
    } else if (oldVersionClass === 'TRANSISI' && newVersionClass === 'TIDAK MEMENUHI') {
      scenarioCode = 'Skenario D (OJK Pg. 8)';
      protectionType = 'RMT_3_YEARS';
      protectedYears = 3;
      rmtRequired = true;
      riskLevel = 'HIGH';
      statusBadgeText = 'PERINGATAN: WAJIB RMT 3 TAHUN ATAU DELISTING';
      fundVerdictTitle = 'Berisiko Kehilangan Label Berkelanjutan (Kritis)';
      fundActionSummary = 'Aktivitas tidak lagi memenuhi kriteria ambang batas minimum. Debitur WAJIB menandatangani program Remedial Measures to Transition (RMT) maksimal 3 tahun agar tetap diakui sebagai Transisi Interim. Jika gagal, fasilitas wajib direklasifikasi menjadi Brown.';
      auditorChecklist = [
        'Keluarkan temuan audit kepatuhan: Emisi operasional debitur berada di bawah ambang batas baru.',
        'Wajibkan debitur menyusun dokumen komitmen RMT maksimal 3 tahun yang diaudit pihak ketiga independen.',
        'Jika dalam 3 tahun target perbaikan tidak tercapai, bank/fund manager wajib menghapus fasilitas dari portofolio hijau.',
      ];
    } else if (oldVersionClass === 'HIJAU' && newVersionClass === 'TIDAK MEMENUHI') {
      scenarioCode = 'Skenario E (OJK Pg. 8)';
      protectedYears = remainingTenorYears;
      protectionType = 'FULL_MATURITY';
      riskLevel = 'HIGH';
      statusBadgeText = 'PROTEKSI KONTRAK SAAT INI (REFINANCING WAJIB AUDIT ULANG)';
      fundVerdictTitle = 'Kontrak Lama Terlindungi, Dilarang Perpanjangan Otomatis';
      fundActionSummary = `Sesuai asas kepastian hukum OJK, kontrak yang telah berjalan tetap sah hingga jatuh tempo tahun ${maturityYear}. Namun saat perpanjangan fasilitas atau refinancing, label hijau otomatis gugur kecuali debitur merombak teknologi operasional.`;
      auditorChecklist = [
        `Pertahankan pencatatan status hingga jatuh tempo kontrak (${maturityYear}) tanpa sanksi penalti retroaktif.`,
        'Beri tanda peringatan pada sistem perbankan: Fasilitas DILARANG diperpanjang otomatis dengan label hijau.',
        'Informasikan kepada debitur untuk menyiapkan investasi dekarbonisasi sebelum jatuh tempo agar tidak kehilangan insentif bunga hijau.',
      ];
    }

    const formattedAmount = (contractAmountMiliar * 1_000_000_000).toLocaleString('id-ID');

    return {
      maturityYear,
      remainingTenorYears,
      scenarioCode,
      protectionType,
      protectedYears,
      rmtRequired,
      riskLevel,
      statusBadgeText,
      fundVerdictTitle,
      fundActionSummary,
      auditorChecklist,
      formattedAmount,
    };
  });
</script>

<div class="space-y-6">
  <!-- Top Executive Header: Plain Language for Auditors & Fund Managers -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-4">
    <div class="flex items-start sm:items-center gap-4">
      <div class="w-12 h-12 rounded-2xl bg-amber-500/10 dark:bg-amber-500/20 border border-amber-300 dark:border-amber-700/60 flex items-center justify-center text-amber-700 dark:text-amber-400 shrink-0">
        <Hourglass size={24} />
      </div>
      <div>
        <div class="flex flex-wrap items-center gap-2">
          <h1 class="text-lg sm:text-xl font-headline font-bold text-slate-900 dark:text-slate-100">
            {$currentLang === 'id' ? 'Uji Masa Tenggang & Proteksi Utang Hijau' : 'Green Debt & Grace Period Stress-Tester'}
          </h1>
          <span class="font-mono text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-950/80 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
            OJK Grandfathering (Pg. 6-8)
          </span>
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-3xl leading-relaxed">
          {$currentLang === 'id'
            ? 'Ketika OJK memperketat standar emisi ramah lingkungan (Sunsetting), apakah obligasi hijau atau pinjaman sindikasi Anda kehilangan status hijau? Periksa berapa tahun kontrak Anda terlindungi secara hukum tanpa risiko penalti.'
            : 'When OJK tightens technical emissions criteria (Sunsetting), does your green bond or loan portfolio lose its verified label? Stress-test how many years your contracts remain legally protected under OJK grandfathering rules.'}
        </p>
      </div>
    </div>
  </div>

  <!-- Real-World Quick Presets (1-Click Realism) -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 shadow-sm space-y-3">
    <div class="flex items-center justify-between">
      <span class="text-xs font-bold text-slate-900 dark:text-slate-100 flex items-center gap-1.5 font-headline">
        <Sparkles size={14} class="text-[#047857] dark:text-[#34D399]" />
        {$currentLang === 'id' ? 'Simulasi Cepat Instrumen Riil (Pilih Salah Satu):' : 'Quick Stress-Test Presets (Select one):'}
      </span>
      <span class="text-[11px] text-slate-400 font-mono">Real IDX Case Studies</span>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
      {#each PRESETS as p}
        <button
          type="button"
          onclick={() => applyPreset(p)}
          class="p-3 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between gap-2 shadow-2xs hover:shadow-xs {instrumentName === p.name
            ? 'bg-emerald-50/70 dark:bg-emerald-950/30 border-emerald-500 dark:border-emerald-600 ring-1 ring-emerald-500'
            : 'bg-slate-50/60 dark:bg-[#162032]/60 border-slate-200/80 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'}"
        >
          <div>
            <div class="flex items-center justify-between mb-1">
              <span class="text-[10px] font-mono font-bold uppercase px-1.5 py-0.5 rounded-md bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300">
                {p.badge}
              </span>
              <span class="text-xs font-mono font-bold text-[#047857] dark:text-[#34D399]">
                Rp {p.amount >= 1000 ? `${(p.amount / 1000).toFixed(1)}T` : `${p.amount}M`}
              </span>
            </div>
            <div class="text-xs font-bold text-slate-900 dark:text-slate-100 leading-snug line-clamp-1">
              {p.label}
            </div>
            <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1 leading-normal">
              {p.desc}
            </p>
          </div>
          <div class="text-[10px] font-mono text-slate-400 flex items-center gap-1 pt-1 border-t border-slate-200/60 dark:border-slate-800">
            <span>{p.issue}–{p.issue + p.tenor} ({p.tenor} Thn)</span>
            <span>•</span>
            <span class="font-bold text-slate-700 dark:text-slate-300">{p.oldTier} → {p.newTier}</span>
          </div>
        </button>
      {/each}
    </div>
  </div>

  <!-- Interactive Simulator Grid: Inputs on Left, Visual Verdict on Right -->
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
    <!-- Left Column: Exposure & Contract Inputs -->
    <div class="lg:col-span-5 bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
      <div class="border-b border-slate-100 dark:border-slate-800 pb-3">
        <h2 class="text-sm font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <FileText size={16} class="text-[#047857] dark:text-[#34D399]" />
          <span>{$currentLang === 'id' ? 'Detail Kontrak & Portofolio' : 'Contract & Portfolio Parameters'}</span>
        </h2>
        <p class="text-xs text-slate-400 mt-0.5">
          {$currentLang === 'id' ? 'Sesuaikan parameter instrumen pembiayaan yang diaudit.' : 'Customize financing instrument parameters.'}
        </p>
      </div>

      <!-- Instrument Type -->
      <div>
        <label for="inst-type" class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
          {$currentLang === 'id' ? 'Jenis Fasilitas Pembiayaan:' : 'Financing Facility Type:'}
        </label>
        <div class="grid grid-cols-3 gap-2 text-xs">
          <button
            type="button"
            onclick={() => (instrumentType = 'BOND')}
            class="p-2 rounded-xl border text-center font-medium transition-colors cursor-pointer {instrumentType === 'BOND'
              ? 'bg-[#047857] text-white border-[#047857] font-bold shadow-xs'
              : 'bg-slate-50 dark:bg-[#162032] border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300'}"
          >
            Obligasi / Sukuk
          </button>
          <button
            type="button"
            onclick={() => (instrumentType = 'SYNDICATED')}
            class="p-2 rounded-xl border text-center font-medium transition-colors cursor-pointer {instrumentType === 'SYNDICATED'
              ? 'bg-[#047857] text-white border-[#047857] font-bold shadow-xs'
              : 'bg-slate-50 dark:bg-[#162032] border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300'}"
          >
            Pinjaman Bertarget
          </button>
          <button
            type="button"
            onclick={() => (instrumentType = 'GENERAL')}
            class="p-2 rounded-xl border text-center font-medium transition-colors cursor-pointer {instrumentType === 'GENERAL'
              ? 'bg-[#047857] text-white border-[#047857] font-bold shadow-xs'
              : 'bg-slate-50 dark:bg-[#162032] border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300'}"
          >
            Kredit Umum
          </button>
        </div>
      </div>

      <!-- Plafon / Nominal Exposure -->
      <div>
        <div class="flex items-center justify-between mb-1">
          <label for="inst-amount" class="text-xs font-semibold text-slate-700 dark:text-slate-300">
            {$currentLang === 'id' ? 'Nilai Kontrak / Plafon:' : 'Nominal Exposure (IDR):'}
          </label>
          <span class="text-xs font-mono font-bold text-[#047857] dark:text-[#34D399]">
            Rp {contractAmountMiliar >= 1000 ? `${(contractAmountMiliar / 1000).toFixed(2)} Triliun` : `${contractAmountMiliar} Miliar`}
          </span>
        </div>
        <div class="flex items-center gap-2">
          <input
            id="inst-amount"
            type="number"
            bind:value={contractAmountMiliar}
            min="10"
            max="50000"
            step="50"
            class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-xs font-mono font-bold text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-1 focus:ring-[#047857]"
          />
          <span class="text-xs font-mono text-slate-400 shrink-0">Miliar IDR</span>
        </div>
      </div>

      <!-- Issue Year & Tenor -->
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label for="issue-yr" class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
            {$currentLang === 'id' ? 'Tahun Akad Diterbitkan:' : 'Issue Year:'}
          </label>
          <select
            id="issue-yr"
            bind:value={issueYear}
            class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-xs font-mono text-slate-900 dark:text-slate-100 focus:outline-none"
          >
            {#each [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] as yr}
              <option value={yr}>{yr}</option>
            {/each}
          </select>
        </div>

        <div>
          <div class="flex items-center justify-between mb-1">
            <label for="tenor-yr" class="text-xs font-semibold text-slate-700 dark:text-slate-300">
              {$currentLang === 'id' ? 'Tenor Kontrak:' : 'Tenor:'}
            </label>
            <span class="text-xs font-mono font-bold text-slate-700 dark:text-slate-300">
              {facilityTenorYears} Thn
            </span>
          </div>
          <input
            id="tenor-yr"
            type="range"
            bind:value={facilityTenorYears}
            min="1"
            max="20"
            class="w-full accent-[#047857] cursor-pointer"
          />
        </div>
      </div>

      <!-- Old vs New Taxonomy Classification -->
      <div class="p-3.5 bg-slate-50 dark:bg-[#162032] rounded-xl border border-slate-200/80 dark:border-slate-700/80 space-y-3">
        <div class="text-[11px] font-bold text-slate-800 dark:text-slate-200 uppercase font-mono tracking-wider">
          {$currentLang === 'id' ? 'Evaluasi Standar OJK (Sunsetting):' : 'Regulatory Evolution Status:'}
        </div>

        <div class="grid grid-cols-2 gap-2 text-xs">
          <div>
            <label for="old-tier" class="block text-[11px] font-medium text-slate-500 mb-1">
              {$currentLang === 'id' ? 'Status Awal (Versi 1/2):' : 'Original Label:'}
            </label>
            <select
              id="old-tier"
              bind:value={oldVersionClass}
              class="w-full bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-lg p-1.5 text-xs font-bold text-slate-900 dark:text-slate-100 focus:outline-none"
            >
              <option value="HIJAU">🟢 HIJAU</option>
              <option value="TRANSISI">🟡 TRANSISI</option>
            </select>
          </div>

          <div>
            <label for="new-tier" class="block text-[11px] font-medium text-slate-500 mb-1">
              {$currentLang === 'id' ? 'Kriteria TSC Baru (Versi 3):' : 'New Standard TSC:'}
            </label>
            <select
              id="new-tier"
              bind:value={newVersionClass}
              class="w-full bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-lg p-1.5 text-xs font-bold text-slate-900 dark:text-slate-100 focus:outline-none"
            >
              <option value="HIJAU">🟢 HIJAU</option>
              <option value="TRANSISI">🟡 TRANSISI</option>
              <option value="TIDAK MEMENUHI">🔴 TIDAK MEMENUHI</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Visual Lifecycle Timeline & Executive Auditor Verdict -->
    <div class="lg:col-span-7 space-y-4">
      <!-- 1. Interactive Lifecycle Timeline -->
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-900 dark:text-slate-100 font-headline flex items-center gap-1.5">
            <Clock size={15} class="text-[#047857] dark:text-[#34D399]" />
            {$currentLang === 'id' ? 'Garis Waktu Proteksi Regulasi (Contract Lifecycle):' : 'Regulatory Protection Timeline:'}
          </span>
          <span class="text-xs font-mono font-bold text-slate-500">
            {issueYear} → {diagnosticResult.maturityYear}
          </span>
        </div>

        <!-- The Visual Timeline Bar -->
        <div class="p-4 bg-slate-50 dark:bg-[#162032] rounded-xl border border-slate-100 dark:border-slate-800 space-y-2">
          <div class="relative w-full h-3 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden flex">
            <!-- Elapsed bar (past) -->
            <div
              class="h-full bg-slate-400 dark:bg-slate-500"
              style="width: {Math.min(100, Math.max(0, ((2026 - issueYear) / facilityTenorYears) * 100))}%"
              title="Masa kontrak yang telah berjalan"
            ></div>
            <!-- Protected Grace Window bar -->
            <div
              class="h-full {diagnosticResult.riskLevel === 'LOW' ? 'bg-emerald-500' : diagnosticResult.riskLevel === 'MEDIUM' ? 'bg-amber-500' : 'bg-rose-500'}"
              style="width: {Math.min(100, (diagnosticResult.protectedYears / facilityTenorYears) * 100)}%"
              title="Masa tenggang perlindungan hukum OJK"
            ></div>
          </div>

          <!-- Milestones Flags -->
          <div class="flex items-center justify-between text-[11px] font-mono text-slate-500 dark:text-slate-400 pt-1">
            <div class="flex flex-col items-start">
              <span class="font-bold text-slate-700 dark:text-slate-300">Akad Diterbitkan</span>
              <span>Thn {issueYear}</span>
            </div>
            <div class="flex flex-col items-center px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
              <span class="font-bold">2026 (Hari Ini)</span>
              <span>{diagnosticResult.remainingTenorYears} Thn Sisa</span>
            </div>
            <div class="flex flex-col items-end">
              <span class="font-bold text-slate-700 dark:text-slate-300">Jatuh Tempo</span>
              <span>Thn {diagnosticResult.maturityYear}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Auditor & Fund Manager Executive Verdict Card -->
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
          <div>
            <span class="text-[10px] font-mono font-bold tracking-wider uppercase text-slate-400 block mb-1">
              {$currentLang === 'id' ? 'Hasil Telaah Auditor Keberlanjutan:' : 'Sustainability Auditor Verdict:'}
            </span>
            <h3 class="text-base font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
              {#if diagnosticResult.riskLevel === 'LOW'}
                <ShieldCheck size={20} class="text-emerald-600 dark:text-emerald-400 shrink-0" />
              {:else if diagnosticResult.riskLevel === 'MEDIUM'}
                <AlertTriangle size={20} class="text-amber-600 dark:text-amber-400 shrink-0" />
              {:else}
                <AlertOctagon size={20} class="text-rose-600 dark:text-rose-400 shrink-0" />
              {/if}
              <span>{diagnosticResult.fundVerdictTitle}</span>
            </h3>
          </div>
          <span class="font-mono text-xs font-bold px-3 py-1 rounded-full whitespace-nowrap {diagnosticResult.riskLevel === 'LOW'
            ? 'bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800'
            : diagnosticResult.riskLevel === 'MEDIUM'
            ? 'bg-amber-100 dark:bg-amber-950/80 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-800'
            : 'bg-rose-100 dark:bg-rose-950/80 text-rose-800 dark:text-rose-300 border border-rose-300 dark:border-rose-800'}">
            {diagnosticResult.statusBadgeText}
          </span>
        </div>

        <!-- 3 Quantitative Impact Metrics for Fund Managers -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="p-3 bg-slate-50 dark:bg-[#162032] rounded-xl border border-slate-100 dark:border-slate-800">
            <span class="text-[10px] font-mono text-slate-400 block mb-0.5">Plafon Terlindungi</span>
            <span class="text-base font-mono font-bold text-slate-900 dark:text-slate-100 block">
              Rp {diagnosticResult.formattedAmount}
            </span>
            <span class="text-[10px] text-emerald-600 dark:text-emerald-400 font-medium">100% Proteksi Hukum</span>
          </div>

          <div class="p-3 bg-slate-50 dark:bg-[#162032] rounded-xl border border-slate-100 dark:border-slate-800">
            <span class="text-[10px] font-mono text-slate-400 block mb-0.5">Sisa Masa Proteksi</span>
            <span class="text-base font-mono font-bold {diagnosticResult.riskLevel === 'LOW' ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400'} block">
              {diagnosticResult.protectedYears} Tahun
            </span>
            <span class="text-[10px] text-slate-400 font-medium">Hingga Thn {2026 + diagnosticResult.protectedYears}</span>
          </div>

          <div class="p-3 bg-slate-50 dark:bg-[#162032] rounded-xl border border-slate-100 dark:border-slate-800">
            <span class="text-[10px] font-mono text-slate-400 block mb-0.5">Kewajiban RMT OJK</span>
            <span class="text-base font-mono font-bold {diagnosticResult.rmtRequired ? 'text-rose-600 dark:text-rose-400' : 'text-slate-700 dark:text-slate-300'} block">
              {diagnosticResult.rmtRequired ? 'WAJIB (Maks 3 Thn)' : 'TIDAK PERLU'}
            </span>
            <span class="text-[10px] text-slate-400 font-medium">{diagnosticResult.scenarioCode}</span>
          </div>
        </div>

        <!-- Plain Language Regulatory Interpretation -->
        <div class="p-3.5 bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200/80 dark:border-amber-800/60 rounded-xl text-xs text-amber-900 dark:text-amber-200 leading-relaxed font-body">
          <span class="font-bold block mb-1 text-amber-950 dark:text-amber-100">
            📌 Ringkasan Implikasi Portofolio & Dampak Finansial:
          </span>
          {diagnosticResult.fundActionSummary}
        </div>

        <!-- Actionable Auditor Checklist -->
        <div class="space-y-2 pt-1">
          <span class="text-xs font-bold text-slate-900 dark:text-slate-100 font-headline block">
            📋 Checklist Tindakan Wajib bagi Auditor / Manajer Investasi:
          </span>
          <div class="space-y-2">
            {#each diagnosticResult.auditorChecklist as item, idx}
              <div class="flex items-start gap-2.5 text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
                <div class="w-5 h-5 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300 font-mono text-[10px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                  {idx + 1}
                </div>
                <span>{item}</span>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Official OJK 5 Scenarios Reference Card Grid (Page 8) -->
  {#if scenariosData?.scenarios}
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
      <div class="border-b border-slate-100 dark:border-slate-800 pb-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h2 class="text-sm font-headline font-bold text-slate-900 dark:text-slate-100">
            {$currentLang === 'id' ? 'Matriks Resmi 5 Skenario Grandfathering OJK (Dokumen Hal. 8)' : 'Official OJK 5 Grandfathering Scenarios Matrix (Page 8)'}
          </h2>
          <p class="text-xs text-slate-400 mt-0.5">
            {$currentLang === 'id'
              ? 'Rujukan regulasi resmi atas setiap kemungkinan transisi status kriteria hijau.'
              : 'Official statutory reference for all potential green taxonomy transitions.'}
          </p>
        </div>
        <span class="font-mono text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 shrink-0">
          POJK 18/2023 & TKBI Versi 3
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
        {#each scenariosData.scenarios as sc}
          <div class="p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-slate-50/50 dark:bg-[#162032]/40 flex flex-col justify-between gap-2.5">
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <span class="font-mono text-xs font-bold text-[#047857] dark:text-[#34D399]">
                  {sc.code}
                </span>
                <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
                  {sc.from_status} → {sc.to_status}
                </span>
              </div>
              <div class="text-xs font-semibold text-slate-800 dark:text-slate-200 leading-snug">
                {sc.impact}
              </div>
            </div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 pt-2 border-t border-slate-200/60 dark:border-slate-800 leading-relaxed font-body">
              <strong>Kewajiban:</strong> {sc.action_required}
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>
