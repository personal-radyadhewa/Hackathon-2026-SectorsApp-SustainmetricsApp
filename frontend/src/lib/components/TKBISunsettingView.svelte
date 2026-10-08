<script>
  import { onMount } from 'svelte';
  import { marked } from 'marked';
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
    Bot,
    Loader2,
    Copy,
    ShieldAlert,
    ShieldX,
  } from '@lucide/svelte';
  import { fetchTKBIGrandfatheringScenarios } from '../api.js';
  import { t, currentLang } from '../i18n.js';

  marked.setOptions({
    gfm: true,
    breaks: true,
  });

  function stripThinkingProcess(text) {
    if (!text) return '';
    let clean = text.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();
    if (clean.includes('</think>')) {
      clean = clean.split('</think>').pop().trim();
    }
    return clean;
  }

  function renderMarkdown(content) {
    if (!content) return '';
    try {
      return marked.parse(stripThinkingProcess(content));
    } catch {
      return content;
    }
  }

  let scenariosData = $state(null);
  let isLoading = $state(true);

  // Diagnostic form state for Auditor / Fund Manager
  let instrumentType = $state('BOND'); // 'BOND' (Obligasi Hijau / Sukuk), 'SYNDICATED' (Pinjaman Bertarget / Sindikasi), 'GENERAL' (Fasilitas Kredit Umum)
  let contractAmountMiliar = $state(2500); // Rp 2,500 Miliar = Rp 2.5 Trillion
  let issueYear = $state(2023);
  let facilityTenorYears = $state(7);
  let oldVersionClass = $state('HIJAU');
  let newVersionClass = $state('HIJAU');

  // AI Copilot Live Audit Stress-Tester State
  let isAiAnalyzing = $state(false);
  let aiAnalysisResult = $state('');
  let showAiResult = $state(false);
  let aiError = $state('');
  let isCopied = $state(false);

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

  // Regulatory Logic & Quantitative Calculations: OJK TKBI Fact Sheet Pages 6-8
  let diagnosticResult = $derived.by(() => {
    const maturityYear = issueYear + facilityTenorYears;
    const currentYear = 2026;
    const remainingTenorYears = Math.max(0, maturityYear - currentYear);

    let scenarioCode = 'Skenario A (OJK Pg. 8)';
    let protectionType = 'FULL_MATURITY'; // FULL_MATURITY, CAPPED_7_YEARS, RMT_3_YEARS, ZERO_PROTECTION
    let protectedYears = remainingTenorYears;
    let rmtRequired = false;
    let riskLevel = 'LOW'; // 'LOW', 'MEDIUM', 'HIGH'
    let statusBadgeText = '';
    let fundVerdictTitle = '';
    let fundActionSummary = '';
    let auditorChecklist = [];

    let protectedPct = 100;
    let atRiskPct = 0;

    // Skenario A: Hijau -> Hijau
    if (oldVersionClass === 'HIJAU' && newVersionClass === 'HIJAU') {
      scenarioCode = 'Skenario A (OJK Pg. 8)';
      protectionType = 'FULL_MATURITY';
      protectedYears = remainingTenorYears;
      protectedPct = 100;
      atRiskPct = 0;
      riskLevel = 'LOW';
      statusBadgeText = 'AMAN: KRITERIA HIJAU TETAP TERPENUHI';
      fundVerdictTitle = 'Kepatuhan Hijau Tidak Berubah (Zero Downgrade Risk)';
      fundActionSummary = 'Aktivitas pembiayaan secara konsisten memenuhi kriteria teknis TSC Versi terbaru. Tidak ada risiko penurunan label hijau atau kewajiban pelaporan khusus.';
      auditorChecklist = [
        'Lakukan verifikasi berkala atas data emisi dan DNSH pada Laporan Keberlanjutan tahunan debitur.',
        'Pertahankan pembobotan portofolio hijau 100% pada rasio pembiayaan berkelanjutan institusi.',
      ];
    }
    // Skenario B: Transisi -> Transisi
    else if (oldVersionClass === 'TRANSISI' && newVersionClass === 'TRANSISI') {
      scenarioCode = 'Skenario B (OJK Pg. 8)';
      protectionType = 'FULL_MATURITY';
      protectedYears = remainingTenorYears;
      protectedPct = 100;
      atRiskPct = 0;
      riskLevel = 'LOW';
      statusBadgeText = 'AMAN: STATUS TRANSISI BERKELANJUTAN';
      fundVerdictTitle = 'Lintasan Transisi Berjalan Normal';
      fundActionSummary = 'Aktivitas tetap tergolong Transisi Terverifikasi. Debitur berada pada lintasan penurunan emisi yang sah dan dilindungi regulasi OJK.';
      auditorChecklist = [
        'Pantau milestone dekarbonisasi tahunan sesuai dokumen roadmap awal.',
        'Pastikan kepatuhan prinsip Do No Significant Harm (DNSH) terhadap keanekaragaman hayati dan pencegahan polusi.',
      ];
    }
    // Skenario C: Hijau -> Transisi (Cap 7 Tahun OJK)
    else if (oldVersionClass === 'HIJAU' && newVersionClass === 'TRANSISI') {
      scenarioCode = 'Skenario C (OJK Pg. 8)';
      if (remainingTenorYears <= 7) {
        protectedYears = remainingTenorYears;
        protectedPct = 100;
        atRiskPct = 0;
        protectionType = 'FULL_MATURITY';
        riskLevel = 'LOW';
        statusBadgeText = `TERLINDUNGI PENUH: SISA TENOR ${protectedYears} THN (DALAM CAP 7 THN)`;
        fundVerdictTitle = 'Terlindungi Grandfathering Sepenuhnya';
        fundActionSummary = `Standar TSC diperketat sehingga aktivitas turun ke kategori Transisi. Sisa tenor kontrak (${remainingTenorYears} thn) berada dalam batas toleransi OJK (maks 7 tahun), sehingga 100% plafon terlindungi hingga jatuh tempo thn ${maturityYear}.`;
      } else {
        protectedYears = 7;
        protectedPct = Math.round((7 / remainingTenorYears) * 100);
        atRiskPct = 100 - protectedPct;
        protectionType = 'CAPPED_7_YEARS';
        riskLevel = 'MEDIUM';
        statusBadgeText = `MASA TENGGANG 7 TAHUN (SISA ${remainingTenorYears - 7} THN TERANCAM REKLASIFIKASI)`;
        fundVerdictTitle = 'Proteksi Parsial: Terkena Plafon Waktu 7 Tahun OJK';
        fundActionSummary = `Sisa tenor (${remainingTenorYears} tahun) melampaui batas maksimal masa tenggang OJK (7 tahun). Hanya porsi tahun 2026-2033 (${protectedPct}%) yang terlindungi status hijau. Sisa ${atRiskPct}% plafon berisiko turun ke Transisi setelah tahun ke-7 jika debitur tidak meng-upgrade teknologi.`;
      }
      auditorChecklist = [
        `Berikan notifikasi resmi kepada debitur bahwa batas proteksi masa tenggang berlaku hingga tahun ${2026 + protectedYears}.`,
        'Minta debitur menyusun rencana aksi penyesuaian teknologi/efisiensi sebelum masa proteksi 7 tahun berakhir.',
        'Setelah tahun ke-7 berakhir, sisa pembiayaan otomatis direklasifikasi menjadi kategori Transisi.',
      ];
    }
    // Skenario D: Transisi -> Tidak Memenuhi (Kritis! Grandfathering Tidak Berlaku Otomatis)
    else if (oldVersionClass === 'TRANSISI' && newVersionClass === 'TIDAK MEMENUHI') {
      scenarioCode = 'Skenario D (OJK Pg. 8)';
      protectionType = 'RMT_3_YEARS';
      rmtRequired = true;
      riskLevel = 'HIGH';
      protectedYears = 0; // 0 tahun proteksi otomatis
      protectedPct = 0;   // 0% proteksi hukum otomatis!
      atRiskPct = 100;    // 100% plafon terancam delisting/brown!
      statusBadgeText = 'KRITIS: 0% PROTEKSI OTOMATIS (100% TERANCAM BROWN/DELISTING)';
      fundVerdictTitle = 'Gugur dari Portofolio Berkelanjutan (Wajib RMT 3 Tahun)';
      fundActionSummary = 'Berdasarkan Panduan OJK Hal. 8, grandfathering TIDAK berlaku otomatis untuk fasilitas yang gagal memenuhi kriteria transisi minimum. 100% plafon wajib direklasifikasi menjadi Brown KECUALI debitur menandatangani program RMT (Remedial Measures to Transition) maksimal 3 tahun.';
      auditorChecklist = [
        'Keluarkan temuan audit kepatuhan: Emisi operasional debitur berada di bawah ambang batas baru.',
        'Wajibkan debitur menyusun dokumen komitmen RMT maksimal 3 tahun yang diaudit pihak ketiga independen agar mendapat status Transisi Interim.',
        'Jika dalam 3 tahun target perbaikan tidak tercapai, bank/fund manager wajib mencabut label hijau dan mereklasifikasi plafon ke non-eligible.',
      ];
    }
    // Skenario E: Hijau -> Tidak Memenuhi (Kontrak Lama Dilindungi, Refinancing 100% Gugur)
    else if (oldVersionClass === 'HIJAU' && newVersionClass === 'TIDAK MEMENUHI') {
      scenarioCode = 'Skenario E (OJK Pg. 8)';
      riskLevel = 'HIGH';
      if (instrumentType === 'GENERAL') {
        // Fasilitas kredit umum tanpa komitmen alokasi proyek spesifik
        protectedYears = Math.min(7, remainingTenorYears);
        protectedPct = remainingTenorYears > 7 ? Math.round((7 / remainingTenorYears) * 50) : 50;
        atRiskPct = 100 - protectedPct;
        protectionType = 'CAPPED_7_YEARS';
        statusBadgeText = 'RISIKO TINGGI: KREDIT UMUM DIPANGKAS (CAP 7 THN & NO ROLLOVER)';
        fundVerdictTitle = 'Fasilitas Umum Terkena Penalti Sunsetting OJK';
        fundActionSummary = `Karena fasilitas berbentuk kredit umum tanpa penelusuran aset proyek hijau (unallocated), OJK membatasi toleransi perlindungan sebesar ${protectedPct}%. Sisa plafon ${atRiskPct}% wajib dicabut dari klaim taksonomi hijau.`;
      } else if (instrumentType === 'BOND') {
        // Green bond dengan alokasi awal: kontrak lama terlindungi sepanjang sisa tenor, namun rollover 0%
        protectedYears = remainingTenorYears;
        protectedPct = 100;
        atRiskPct = 0;
        protectionType = 'FULL_MATURITY';
        statusBadgeText = 'PROTEKSI KONTRAK SAAT INI (REFINANCING 100% DITOLAK)';
        fundVerdictTitle = 'Obligasi Lama Terlindungi, Dilarang Rollover Berlabel Hijau';
        fundActionSummary = `Sesuai asas kepastian hukum OJK Hal. 6 & 8, dana obligasi hijau yang telah dialokasikan tetap diakui hingga jatuh tempo thn ${maturityYear} (100% terlindungi). Namun, penerbitan refinancing mendatang berstatus 0% proteksi dan dilarang menyandang label hijau.`;
      } else {
        // Pinjaman Sindikasi / Terarah
        if (remainingTenorYears <= 7) {
          protectedYears = remainingTenorYears;
          protectedPct = 100;
          atRiskPct = 0;
        } else {
          protectedYears = 7;
          protectedPct = Math.round((7 / remainingTenorYears) * 100);
          atRiskPct = 100 - protectedPct;
        }
        protectionType = 'CAPPED_7_YEARS';
        statusBadgeText = `PROTEKSI TERBATAS ${protectedYears} TAHUN (REFINANCING DILARANG)`;
        fundVerdictTitle = 'Pinjaman Terarah: Terlindungi Parsial (Cap 7 Tahun)';
        fundActionSummary = `Kontrak sindikasi yang telah berjalan diakui selama ${protectedYears} tahun (${protectedPct}% plafon). Reklasifikasi wajib dilakukan setelah batas waktu atau saat perpanjangan tenor fasilitas.`;
      }
      auditorChecklist = [
        `Pertahankan pencatatan status kontrak lama hingga ${maturityYear} tanpa sanksi penalti retroaktif.`,
        'Beri tanda peringatan pada sistem: Fasilitas DILARANG diperpanjang otomatis (rollover) dengan label hijau.',
        'Informasikan kepada debitur untuk menyiapkan belanja modal dekarbonisasi baru sebelum jatuh tempo.',
      ];
    }

    const protectedAmountMiliar = Math.round((contractAmountMiliar * protectedPct) / 100);
    const atRiskAmountMiliar = Math.max(0, contractAmountMiliar - protectedAmountMiliar);

    const protectedAmountFormatted = (protectedAmountMiliar * 1_000_000_000).toLocaleString('id-ID');
    const atRiskAmountFormatted = (atRiskAmountMiliar * 1_000_000_000).toLocaleString('id-ID');
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
      protectedPct,
      atRiskPct,
      protectedAmountMiliar,
      atRiskAmountMiliar,
      protectedAmountFormatted,
      atRiskAmountFormatted,
    };
  });

  async function runAiStressTest() {
    isAiAnalyzing = true;
    showAiResult = true;
    aiAnalysisResult = '';
    aiError = '';

    const instrumentLabel = instrumentType === 'BOND'
      ? 'Obligasi Hijau / Sukuk Berkelanjutan'
      : instrumentType === 'SYNDICATED'
      ? 'Pinjaman Sindikasi / Project Finance Bertarget'
      : 'Fasilitas Kredit Korporasi Umum (General Corporate Loan)';

    const promptText = `Lakukan audit regulasi OJK & stress-test hukum mendalam berdasarkan POJK 18/2023 dan Panduan TKBI Hal. 6-8 untuk fasilitas pembiayaan berikut:
- Tipe Fasilitas: ${instrumentLabel}
- Plafon Kontrak: Rp ${diagnosticResult.formattedAmount} (${contractAmountMiliar} Miliar IDR)
- Tahun Terbit / Akad: ${issueYear}
- Total Tenor Kontrak: ${facilityTenorYears} tahun (Jatuh tempo: ${diagnosticResult.maturityYear}, Sisa tenor: ${diagnosticResult.remainingTenorYears} tahun)
- Status Taksonomi Awal: ${oldVersionClass}
- Klasifikasi Kriteria Baru (Sunsetting): ${newVersionClass}
- Skenario OJK: ${diagnosticResult.scenarioCode}
- Plafon Terlindungi: Rp ${diagnosticResult.protectedAmountFormatted} (${diagnosticResult.protectedPct}%)
- Plafon Berisiko Brown/Delisting: Rp ${diagnosticResult.atRiskAmountFormatted} (${diagnosticResult.atRiskPct}%)
- Sisa Masa Proteksi: ${diagnosticResult.protectedYears} Tahun
- Status RMT: ${diagnosticResult.rmtRequired ? 'Wajib Remedial Measures 3 Tahun' : 'Bebas RMT'}

Berikan audit memo resmi terstruktur untuk Auditor Keberlanjutan & Portfolio Fund Manager:
1. **Kepastian Hukum & Masa Tenggang (Grandfathering vs Sunsetting OJK)**
2. **Kalkulasi & Risiko Revaluasi Portofolio (Greenium, Haircut Agunan, atau Delisting)**
3. **Audit Kepatuhan Pelaporan POJK 18/2023**
4. **Rekomendasi Aksi Mitigasi Segera (Mitigation Action Plan)**
Gunakan gaya bahasa profesional, padat, akurat, dan merujuk ketentuan OJK.`;

    const savedProvider = localStorage.getItem('sustainmetric_chat_provider') || 'gemini';
    const savedModel = localStorage.getItem('sustainmetric_chat_model') || 'gemini-2.5-flash';
    const savedKey = localStorage.getItem('sustainmetric_chat_api_key') || '';

    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [{ role: 'user', content: promptText }],
          provider: savedProvider,
          model: savedModel,
          api_key: savedKey,
          ticker: 'TKBI-AUDIT',
        }),
      });

      if (!response.ok) {
        aiError = `Gagal menghubungi server AI: ${response.statusText}`;
        isAiAnalyzing = false;
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.includes('event: delta')) {
            const dataMatch = line.match(/data: (.+)/);
            if (dataMatch) {
              try {
                const parsed = JSON.parse(dataMatch[1]);
                if (parsed.content) {
                  aiAnalysisResult += parsed.content;
                }
              } catch (e) {}
            }
          } else if (line.includes('event: done')) {
            isAiAnalyzing = false;
          }
        }
      }
    } catch (err) {
      aiError = `Error koneksi: ${err.message}`;
    } finally {
      isAiAnalyzing = false;
    }
  }

  function copyAiMemo() {
    if (!aiAnalysisResult) return;
    navigator.clipboard.writeText(aiAnalysisResult);
    isCopied = true;
    setTimeout(() => {
      isCopied = false;
    }, 2000);
  }
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

        <!-- 4 Quantitative Impact Metrics for Fund Managers & Auditors -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <!-- Card 1: Plafon Terlindungi -->
          <div class="p-3 bg-slate-50 dark:bg-[#162032] rounded-xl border {diagnosticResult.protectedPct === 100 ? 'border-emerald-200 dark:border-emerald-800/80 bg-emerald-50/20 dark:bg-emerald-950/10' : diagnosticResult.protectedPct > 0 ? 'border-amber-200 dark:border-amber-800/80 bg-amber-50/20 dark:bg-amber-950/10' : 'border-rose-200 dark:border-rose-800/80 bg-rose-50/20 dark:bg-rose-950/10'}">
            <span class="text-[10px] font-mono text-slate-400 block mb-0.5">Plafon Terlindungi</span>
            <span class="text-base font-mono font-bold {diagnosticResult.protectedPct === 100 ? 'text-emerald-700 dark:text-emerald-400' : diagnosticResult.protectedPct > 0 ? 'text-amber-700 dark:text-amber-400' : 'text-rose-700 dark:text-rose-400'} block">
              Rp {diagnosticResult.protectedAmountFormatted}
            </span>
            <span class="text-[10px] font-medium {diagnosticResult.protectedPct === 100 ? 'text-emerald-600 dark:text-emerald-400' : diagnosticResult.protectedPct > 0 ? 'text-amber-600 dark:text-amber-400' : 'text-rose-600 dark:text-rose-400'}">
              {diagnosticResult.protectedPct}% Proteksi Regulasi
            </span>
          </div>

          <!-- Card 2: Plafon Berisiko Terdegradasi -->
          <div class="p-3 bg-slate-50 dark:bg-[#162032] rounded-xl border {diagnosticResult.atRiskPct > 0 ? 'border-rose-200 dark:border-rose-800/80 bg-rose-50/30 dark:bg-rose-950/20' : 'border-slate-100 dark:border-slate-800'}">
            <span class="text-[10px] font-mono text-slate-400 block mb-0.5">Plafon Berisiko Terdegradasi</span>
            <span class="text-base font-mono font-bold {diagnosticResult.atRiskPct > 0 ? 'text-rose-600 dark:text-rose-400' : 'text-slate-700 dark:text-slate-300'} block">
              Rp {diagnosticResult.atRiskAmountFormatted}
            </span>
            <span class="text-[10px] font-medium {diagnosticResult.atRiskPct > 0 ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'}">
              {diagnosticResult.atRiskPct > 0 ? `${diagnosticResult.atRiskPct}% Terancam Brown/Delisting` : '0% Risiko Degradasi (Aman)'}
            </span>
          </div>

          <!-- Card 3: Sisa Masa Proteksi -->
          <div class="p-3 bg-slate-50 dark:bg-[#162032] rounded-xl border border-slate-100 dark:border-slate-800">
            <span class="text-[10px] font-mono text-slate-400 block mb-0.5">Sisa Masa Proteksi</span>
            <span class="text-base font-mono font-bold {diagnosticResult.riskLevel === 'LOW' ? 'text-emerald-600 dark:text-emerald-400' : diagnosticResult.riskLevel === 'MEDIUM' ? 'text-amber-600 dark:text-amber-400' : 'text-rose-600 dark:text-rose-400'} block">
              {diagnosticResult.protectedYears} Tahun
            </span>
            <span class="text-[10px] text-slate-400 font-medium">Hingga Thn {2026 + diagnosticResult.protectedYears}</span>
          </div>

          <!-- Card 4: Kewajiban RMT OJK -->
          <div class="p-3 bg-slate-50 dark:bg-[#162032] rounded-xl border border-slate-100 dark:border-slate-800">
            <span class="text-[10px] font-mono text-slate-400 block mb-0.5">Kewajiban RMT OJK</span>
            <span class="text-base font-mono font-bold {diagnosticResult.rmtRequired ? 'text-rose-600 dark:text-rose-400' : 'text-slate-700 dark:text-slate-300'} block">
              {diagnosticResult.rmtRequired ? 'WAJIB (Maks 3 Thn)' : 'BEBAS RMT'}
            </span>
            <span class="text-[10px] text-slate-400 font-medium truncate block">{diagnosticResult.scenarioCode}</span>
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

        <!-- Real AI Copilot Stress-Test Action Bar & Audit Memo Display -->
        <div class="pt-2 border-t border-slate-100 dark:border-slate-800/80 space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-gradient-to-r from-emerald-500/5 via-teal-500/5 to-transparent dark:from-emerald-950/30 dark:via-teal-950/20 p-3.5 rounded-xl border border-emerald-500/20 dark:border-emerald-500/30">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-emerald-600/10 dark:bg-emerald-400/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
                <Bot size={18} />
              </div>
              <div>
                <span class="text-xs font-bold text-slate-900 dark:text-slate-100 block">
                  AI Copilot Auditor Kepatuhan POJK
                </span>
                <span class="text-[11px] text-slate-500 dark:text-slate-400">
                  Stress-test kepatuhan hukum, risiko greenium haircut, dan mitigasi spesifik skenario ini secara real-time.
                </span>
              </div>
            </div>

            <button
              type="button"
              onclick={runAiStressTest}
              disabled={isAiAnalyzing}
              class="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-xs font-bold bg-[#047857] hover:bg-[#065f46] text-white shadow-sm transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
            >
              {#if isAiAnalyzing}
                <Loader2 size={14} class="animate-spin" />
                <span>Menganalisis Regulasi...</span>
              {:else}
                <Sparkles size={14} />
                <span>Jalankan AI Stress-Test</span>
              {/if}
            </button>
          </div>

          <!-- Live AI Memo Output Box -->
          {#if showAiResult}
            <div class="rounded-xl border border-emerald-500/30 bg-white dark:bg-[#0c1322] p-4.5 shadow-sm space-y-3">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2.5">
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full {isAiAnalyzing ? 'bg-amber-400 animate-pulse' : 'bg-emerald-500'}"></span>
                  <span class="text-xs font-headline font-bold text-slate-900 dark:text-slate-100">
                    Memo Resmi Auditor AI (POJK 18/2023 & TKBI Sunsetting)
                  </span>
                  {#if isAiAnalyzing}
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300">
                      Streaming Evaluasi...
                    </span>
                  {/if}
                </div>

                {#if aiAnalysisResult && !isAiAnalyzing}
                  <button
                    type="button"
                    onclick={copyAiMemo}
                    class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] font-mono text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700 transition-colors cursor-pointer"
                  >
                    {#if isCopied}
                      <Check size={12} class="text-emerald-500" />
                      <span>Tersalin</span>
                    {:else}
                      <Copy size={12} />
                      <span>Salin Memo</span>
                    {/if}
                  </button>
                {/if}
              </div>

              {#if aiError}
                <div class="p-3 bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800 rounded-lg text-xs text-rose-700 dark:text-rose-300">
                  {aiError}
                </div>
              {:else if aiAnalysisResult}
                <div class="prose prose-sm dark:prose-invert max-w-none text-xs leading-relaxed text-slate-800 dark:text-slate-200 space-y-2">
                  {@html renderMarkdown(aiAnalysisResult)}
                </div>
              {:else if isAiAnalyzing}
                <div class="flex items-center gap-2.5 py-4 text-xs text-slate-500">
                  <Loader2 size={16} class="animate-spin text-emerald-600" />
                  <span>AI Copilot sedang memetakan implikasi klausul POJK 18/2023 untuk instrumen ini...</span>
                </div>
              {/if}
            </div>
          {/if}
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
