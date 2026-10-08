<script>
  import {
    BookOpen,
    Sliders,
    Compass,
    Hourglass,
    ArrowRight,
    CheckCircle2,
    ShieldCheck,
    HelpCircle,
    Building2,
    FileSpreadsheet,
    Activity,
    Star,
    Layers,
    Info,
  } from '@lucide/svelte';
  import { t, currentLang } from '../i18n.js';

  let { onNavigateView } = $props();

  const rulesPages = [
    {
      id: 'simulator',
      icon: Sliders,
      badge: 'Hal. 23 Panduan OJK',
      titleId: 'Simulasi Aturan Hijau',
      titleEn: 'Green Decision Simulator',
      purposeId: 'Alat uji cepat untuk memeriksa apakah proyek atau perusahaan Anda tergolong HIJAU, KUNING (Transisi), atau MERAH.',
      purposeEn: 'Quick interactive test to check if a project qualifies as GREEN, YELLOW (Transition), or RED.',
      howItWorksId: 'Anda cukup menjawab beberapa pertanyaan sederhana tentang dampak lingkungan, rencana perbaikan (maks 3 tahun), dan standar tenaga kerja.',
      howItWorksEn: 'Answer straightforward questions about environmental impact, 3-year improvement plans, and fair labor standards.',
      color: 'emerald',
    },
    {
      id: 'explorer',
      icon: Compass,
      badge: '8 Sektor Resmi OJK',
      titleId: '8 Sektor Usaha Prioritas',
      titleEn: '8 Priority Business Sectors',
      purposeId: 'Daftar resmi 8 kelompok usaha di Indonesia (seperti Energi, Pabrik, Pertanian, Konstruksi) beserta syarat lingkungan masing-masing.',
      purposeEn: 'The official catalog of 8 Indonesian business sectors (Energy, Manufacturing, Agriculture, Construction, etc.) and their rules.',
      howItWorksId: 'Cari kode KBLI atau nama industri perusahaan Anda untuk membaca aturan baku apa yang harus dipenuhi agar diakui ramah lingkungan.',
      howItWorksEn: 'Search any KBLI code or industry name to view what environmental benchmarks must be met to earn official green recognition.',
      color: 'blue',
    },
    {
      id: 'sunsetting',
      icon: Hourglass,
      badge: 'Hal. 6-8 Panduan OJK',
      titleId: 'Uji Proteksi Utang Hijau (Grace Period)',
      titleEn: 'Green Debt & Grace Period Stress-Tester',
      purposeId: 'Stress-test kepastian hukum obligasi hijau dan kredit sindikasi ketika kriteria TSC diperketat (Sunsetting). Menghitung plafon terlindungi vs berisiko brown.',
      purposeEn: 'Stress-test legal grandfathering for green bonds and syndicated loans when TSC rules tighten. Computes protected vs at-risk brown exposures.',
      howItWorksId: 'Pilih jenis fasilitas (obligasi/sindikasi), tahun terbit, sisa tenor, dan skenario OJK untuk melihat persentase proteksi serta memicu AI Audit Copilot.',
      howItWorksEn: 'Select facility type, tenor, and OJK sunsetting scenario to calculate statutory coverage and run live AI Copilot regulatory stress-tests.',
      color: 'amber',
    },
  ];
</script>

<div class="space-y-6 max-w-6xl mx-auto">
  <!-- Hero Banner -->
  <div class="bg-gradient-to-br from-emerald-50 via-white to-slate-50 dark:from-[#0F1D1A] dark:via-[#0F172A] dark:to-[#070A11] border border-emerald-200/80 dark:border-emerald-900/60 rounded-2xl p-6 md:p-8 shadow-sm">
    <div class="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-[#047857] dark:text-[#34D399] mb-2">
      <BookOpen size={16} />
      <span>{$currentLang === 'id' ? 'Panduan Resmi Aturan Hijau (OJK TKBI)' : 'Official Green Rules Guide (OJK TKBI)'}</span>
    </div>
    <h1 class="text-2xl md:text-3xl font-headline font-bold text-slate-900 dark:text-slate-100 tracking-tight">
      {$currentLang === 'id' ? 'Apa Fungsi Menu "Panduan Aturan Hijau"?' : 'What is the "Green Rules Guide" Section?'}
    </h1>
    <p class="font-body text-xs md:text-sm text-slate-600 dark:text-slate-300 mt-2 max-w-3xl leading-relaxed">
      {$currentLang === 'id'
        ? 'Bagian ini berisi 3 modul panduan praktis berdasarkan buku resmi OJK Taksonomi Keuangan Berkelanjutan Indonesia (TKBI). Anda tidak perlu membaca dokumen ratusan halaman—semua aturan telah disederhanakan menjadi simulator interaktif dan panduan yang mudah dipahami.'
        : 'This section contains 3 practical tools based on Indonesia Financial Services Authority (OJK) Green Taxonomy. Instead of parsing hundreds of regulatory pages, you can simulate outcomes and look up requirements directly below.'}
    </p>

    <!-- Fast Stat summary pill ribbon -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-slate-200/80 dark:border-slate-800">
      <div class="flex flex-col">
        <span class="text-[10px] font-mono uppercase text-slate-400 font-semibold">{$currentLang === 'id' ? 'Standar Berlaku' : 'Standard'}</span>
        <span class="text-xs font-bold text-slate-800 dark:text-slate-200 mt-0.5">OJK TKBI v3.0 (2024)</span>
      </div>
      <div class="flex flex-col">
        <span class="text-[10px] font-mono uppercase text-slate-400 font-semibold">{$currentLang === 'id' ? 'Sektor Tercakup' : 'Sectors Covered'}</span>
        <span class="text-xs font-bold text-slate-800 dark:text-slate-200 mt-0.5">8 Sektor Utama</span>
      </div>
      <div class="flex flex-col">
        <span class="text-[10px] font-mono uppercase text-slate-400 font-semibold">{$currentLang === 'id' ? 'Masa Perbaikan' : 'Grace Period'}</span>
        <span class="text-xs font-bold text-slate-800 dark:text-slate-200 mt-0.5">Hingga 7 Tahun</span>
      </div>
      <div class="flex flex-col">
        <span class="text-[10px] font-mono uppercase text-slate-400 font-semibold">{$currentLang === 'id' ? 'Bahasa' : 'Language'}</span>
        <span class="text-xs font-bold text-[#047857] dark:text-[#34D399] mt-0.5">{$currentLang === 'id' ? 'Sederhana & Ramah' : 'Plain Language'}</span>
      </div>
    </div>
  </div>

  <!-- 4 Modular Section Explanations with direct route buttons -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
    {#each rulesPages as page}
      {@const Icon = page.icon}
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:border-[#047857]/40 dark:hover:border-[#34D399]/40 transition-all flex flex-col justify-between gap-5 group">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <div class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-[#162032] flex items-center justify-center text-[#047857] dark:text-[#34D399] group-hover:scale-110 transition-transform">
              <Icon size={20} />
            </div>
            <span class="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
              {page.badge}
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
              {$currentLang === 'id' ? '💡 CARA KERJANYA' : '💡 HOW IT WORKS'}
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
