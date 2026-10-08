<script>
  import {
    BarChart3,
    Star,
    LayoutDashboard,
    FileSpreadsheet,
    Activity,
    ArrowRight,
    Building2,
    ShieldCheck,
    CheckCircle2,
    Sparkles,
  } from '@lucide/svelte';
  import { t, currentLang } from '../i18n.js';

  let { onNavigateView, activeTicker = null } = $props();

  const analysisPages = [
    {
      id: 'watchlist',
      icon: Star,
      badge: 'Langkah Pertama',
      badgeEn: 'Step 1: Screener',
      titleId: 'Daftar Pantau Saham (Watchlist)',
      titleEn: 'Stock Watchlist & Screener',
      purposeId: 'Halaman utama untuk memilih atau mencari perusahaan saham yang terdaftar di Bursa Efek Indonesia (IDX).',
      purposeEn: 'The starting hub to search and pick companies listed on the Indonesia Stock Exchange (IDX).',
      howItWorksId: 'Ketik 4 huruf kode saham (seperti PGEO, BBRI, ADRO) untuk menambahkan ke pantauan Anda dan langsung melihat ringkasan hijau atau menjalankan audit AI.',
      howItWorksEn: 'Type a 4-letter stock ticker (e.g. PGEO, BBRI) to add it to your active list, view aggregate metrics, or trigger live checks.',
    },
    {
      id: 'dashboard',
      icon: LayoutDashboard,
      badge: 'Profil Emiten',
      badgeEn: 'Profile Overview',
      titleId: 'Ringkasan Emiten (Dashboard)',
      titleEn: 'Company Overview & Health Pulse',
      purposeId: 'Halaman rangkuman lengkap satu perusahaan terpilih: seberapa ramah lingkungan bisnisnya dan seberapa kuat kemampuan uang kasnya.',
      purposeEn: 'Comprehensive deep dive for a selected company: see their environmental rating and whether their cash flow supports green goals.',
      howItWorksId: 'Melihat diagram kuadran ramah lingkungan vs uang kas, perbandingan dengan perusahaan sejenis di sektornya, dan analisis AI.',
      howItWorksEn: 'Inspect the 4-quadrant cash vs sustainability matrix, peer benchmarks, and plain-language AI recommendations.',
    },
    {
      id: 'tkbi',
      icon: FileSpreadsheet,
      badge: 'Audit Detail',
      badgeEn: 'Detailed Checklist',
      titleId: 'Cek Standar Hijau (Checklist Audit)',
      titleEn: 'Green Regulatory Audit Checklist',
      purposeId: 'Tabel pemeriksaan detail poin demi poin sesuai aturan resmi OJK. Dilengkapi bukti dan alasan AI.',
      purposeEn: 'Point-by-point regulatory compliance grid based on official OJK rules, backed by disclosure evidence.',
      howItWorksId: 'Anda bisa melihat aturan mana yang sudah lolos (Hijau), mana yang masih transisi (Kuning), dan mendownload laporannya dalam bentuk Excel atau PDF.',
      howItWorksEn: 'Check which criteria pass (Green) or are in progress (Yellow), override verdicts if needed, and export to Excel or official PDF.',
    },
    {
      id: 'traces',
      icon: Activity,
      badge: 'Jejak Transparan',
      badgeEn: 'Data Audit Trail',
      titleId: 'Jejak Langkah Data (Waterfall)',
      titleEn: 'Step-by-Step Data Trail (Traces)',
      purposeId: 'Halaman bukti transparansi sistem yang memperlihatkan dari mana data diambil dan berapa detik proses analisis AI berjalan.',
      purposeEn: 'Full transparent audit trail verifying where data was retrieved and step-by-step latency of the AI pipeline.',
      howItWorksId: 'Melihat catatan log komputer mulai dari pengambilan laporan keuangan bursa, pencarian buku aturan OJK, hingga rumus penilaian.',
      howItWorksEn: 'Examine each sub-step from financial filing retrieval to OJK vector lookup and matrix calculation.',
    },
  ];
</script>

<div class="space-y-6 max-w-6xl mx-auto">
  <!-- Hero Banner -->
  <div class="bg-gradient-to-br from-emerald-50 via-white to-slate-50 dark:from-[#0F1D1A] dark:via-[#0F172A] dark:to-[#070A11] border border-emerald-200/80 dark:border-emerald-900/60 rounded-2xl p-6 md:p-8 shadow-sm">
    <div class="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-[#047857] dark:text-[#34D399] mb-2">
      <BarChart3 size={16} />
      <span>{$currentLang === 'id' ? 'Panduan Menu Analisis Emiten' : 'Company Analysis Guide'}</span>
    </div>
    <h1 class="text-2xl md:text-3xl font-headline font-bold text-slate-900 dark:text-slate-100 tracking-tight">
      {$currentLang === 'id' ? 'Apa Fungsi Menu "Analisis Perusahaan"?' : 'What is the "Company Analysis" Section?'}
    </h1>
    <p class="font-body text-xs md:text-sm text-slate-600 dark:text-slate-300 mt-2 max-w-3xl leading-relaxed">
      {$currentLang === 'id'
        ? 'Bagian ini adalah ruang kerja utama untuk memeriksa emiten (perusahaan saham) di Indonesia. Dari memilih saham di Daftar Pantau, membaca ringkasan kesehatan, memeriksa checklist aturan OJK, hingga melihat jejak data audit yang transparan.'
        : 'This section is your core workspace for reviewing Indonesian listed equities. From adding stocks to your Watchlist and reading high-level health verdicts, to inspecting OJK checklists and verifying data telemetry.'}
    </p>

    <!-- Emitent context helper -->
    <div class="mt-6 pt-5 border-t border-slate-200/80 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
      <div class="flex items-center gap-2 text-slate-600 dark:text-slate-300">
        <Building2 size={16} class="text-[#047857] dark:text-[#34D399]" />
        <span>
          {$currentLang === 'id' ? 'Perusahaan yang sedang aktif:' : 'Currently active company:'}
          <strong class="font-mono text-slate-900 dark:text-slate-100 ml-1">
            {activeTicker ? `IDX: ${activeTicker}` : ($currentLang === 'id' ? 'Belum dipilih (Pilih di Daftar Pantau)' : 'None selected (Pick in Watchlist)')}
          </strong>
        </span>
      </div>

      {#if !activeTicker}
        <button
          type="button"
          onclick={() => onNavigateView('watchlist')}
          class="px-3.5 py-1.5 rounded-lg bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-semibold text-xs transition-colors cursor-pointer"
        >
          {$currentLang === 'id' ? 'Buka Daftar Pantau Saham' : 'Open Stock Watchlist'}
        </button>
      {/if}
    </div>
  </div>

  <!-- 4 Modular Sub-page cards -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
    {#each analysisPages as page}
      {@const Icon = page.icon}
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:border-[#047857]/40 dark:hover:border-[#34D399]/40 transition-all flex flex-col justify-between gap-5 group">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <div class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-[#162032] flex items-center justify-center text-[#047857] dark:text-[#34D399] group-hover:scale-110 transition-transform">
              <Icon size={20} />
            </div>
            <span class="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
              {$currentLang === 'id' ? page.badge : page.badgeEn}
            </span>
          </div>

          <div>
            <h2 class="font-headline font-bold text-base text-slate-900 dark:text-slate-100">
              {$currentLang === 'id' ? page.titleId : page.titleEn}
            </h2>
            <p class="text-xs text-slate-600 dark:text-slate-300 mt-1.5 leading-relaxed font-body">
              {$currentLang === 'id' ? page.purposeId : page.purposeEn}
            </p>
          </div>

          <div class="p-3 rounded-xl bg-slate-50 dark:bg-[#162032]/60 border border-slate-100 dark:border-slate-800 text-xs space-y-1">
            <div class="font-mono text-[10px] font-bold uppercase text-slate-400">
              {$currentLang === 'id' ? '💡 CARA PENGGUNAAN' : '💡 HOW TO USE'}
            </div>
            <p class="text-[11px] text-slate-600 dark:text-slate-300 leading-normal">
              {$currentLang === 'id' ? page.howItWorksId : page.howItWorksEn}
            </p>
          </div>
        </div>

        <button
          type="button"
          onclick={() => onNavigateView(page.id)}
          class="w-full flex items-center justify-between px-4 py-2.5 rounded-xl bg-slate-100 dark:bg-[#162032] hover:bg-[#047857] hover:text-white dark:hover:bg-[#34D399] dark:hover:text-[#064E3B] text-slate-800 dark:text-slate-200 text-xs font-semibold transition-all cursor-pointer shadow-2xs group/btn"
        >
          <span>{$currentLang === 'id' ? `Buka Halaman ${page.titleId}` : `Open ${page.titleEn}`}</span>
          <ArrowRight size={14} class="group-hover/btn:translate-x-1 transition-transform" />
        </button>
      </div>
    {/each}
  </div>
</div>
