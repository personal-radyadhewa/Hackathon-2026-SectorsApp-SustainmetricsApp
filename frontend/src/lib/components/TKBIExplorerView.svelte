<script>
  import { onMount } from 'svelte';
  import {
    Compass,
    Search,
    Tag,
    Layers,
    ShieldCheck,
    CheckCircle2,
    Info,
    ExternalLink,
    Filter,
    Flame,
    Zap,
    Building2,
    Truck,
    Wheat,
    Factory,
    Droplets,
    Radio,
    FileCheck2,
  } from '@lucide/svelte';
  import { fetchTKBITaxonomyExplorer } from '../api.js';
  import { t, currentLang } from '../i18n.js';

  let taxonomyData = $state(null);
  let activeSectorKey = $state('Energi');
  let searchQuery = $state('');
  let isLoading = $state(true);

  const sectorIcons = {
    'Energi': Zap,
    'Konstruksi dan Real Estat': Building2,
    'Transportasi dan Pergudangan': Truck,
    'Pertanian, Kehutanan, dan Perikanan': Wheat,
    'Manufaktur': Factory,
    'Pengelolaan Air, Air Limbah, Sampah, dan Remediasi': Droplets,
    'Informasi dan Komunikasi': Radio,
    'Aktivitas Profesional, Ilmiah, dan Teknis': FileCheck2,
  };

  onMount(async () => {
    try {
      taxonomyData = await fetchTKBITaxonomyExplorer();
    } catch (err) {
      console.error('Failed to load taxonomy explorer:', err);
    } finally {
      isLoading = false;
    }
  });

  let activeSector = $derived(
    taxonomyData?.sectors ? taxonomyData.sectors[activeSectorKey] : null
  );

  let filteredItems = $derived.by(() => {
    if (!activeSector?.items) return [];
    const q = searchQuery.toLowerCase().trim();
    if (!q) return activeSector.items;
    return activeSector.items.filter(
      (item) =>
        (item.bab && item.bab.toLowerCase().includes(q)) ||
        (item.kbli && item.kbli.toLowerCase().includes(q)) ||
        (item.tsc_id && item.tsc_id.toLowerCase().includes(q)) ||
        (item.criteria && item.criteria.toLowerCase().includes(q))
    );
  });
</script>

<div class="space-y-6">
  <!-- Plain Explanation Top Callout -->
  <div class="p-4 rounded-xl bg-blue-50/80 dark:bg-[#101D2D] border border-blue-200/90 dark:border-blue-800/80 flex items-start gap-3.5 text-xs shadow-2xs">
    <div class="p-2 rounded-lg bg-blue-100 dark:bg-blue-950/80 text-[#1D4ED8] dark:text-[#60A5FA] shrink-0">
      <Compass size={18} />
    </div>
    <div class="space-y-1">
      <div class="font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
        <span>{$currentLang === 'id' ? 'Apa Fungsi Halaman Ini?' : 'What is this page for?'}</span>
        <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/60 text-blue-800 dark:text-blue-300 font-bold">
          {$currentLang === 'id' ? 'Kamus 8 Sektor' : '8 Sector Directory'}
        </span>
      </div>
      <p class="text-slate-600 dark:text-slate-300 leading-relaxed font-body">
        {$currentLang === 'id'
          ? 'Halaman ini adalah kamus lengkap aturan OJK untuk 8 sektor ekonomi (Energi, Manufaktur, Pertanian, Konstruksi, dll). Gunakan halaman ini untuk mencari kode izin usaha (KBLI) dan melihat syarat apa yang wajib dipenuhi agar diakui resmi sebagai usaha hijau.'
          : 'This page is the master directory of official OJK environmental criteria across 8 Indonesian economic sectors. Use it to search any business permit code (KBLI) and see the exact technical thresholds needed to be recognized as green.'}
      </p>
    </div>
  </div>

  <!-- Top Banner -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 flex items-center justify-center text-[#1D4ED8] dark:text-[#60A5FA] shrink-0">
        <Compass size={24} />
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-xl font-headline font-bold text-slate-900 dark:text-slate-100">
            {$currentLang === 'id' ? 'Daftar 8 Sektor Usaha (OJK TKBI)' : 'TKBI Master Taxonomy Explorer'}
          </h1>
          <span class="font-mono text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/60 text-blue-800 dark:text-blue-300">
            Rumah Tumbuh OJK
          </span>
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-2xl">
          {$currentLang === 'id'
            ? 'Cari kriteria teknis TSC dan kode KBLI untuk mengetahui syarat ramah lingkungan tiap industri.'
            : 'Explore OJK taxonomy criteria, national NDC climate commitments, and KBLI activity thresholds.'}
        </p>
      </div>
    </div>
  </div>

  <!-- NDC Target Ribbon -->
  {#if taxonomyData?.ndc_targets}
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-4 shadow-sm">
      <div class="text-[10px] font-mono uppercase font-bold text-slate-400 mb-2 flex items-center gap-1.5">
        <ShieldCheck size={13} class="text-[#047857] dark:text-[#34D399]" />
        <span>Target Komitmen Iklim Nasional (Enhanced NDC Indonesia 2030)</span>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5">
        {#each taxonomyData.ndc_targets as ndc}
          <div class="bg-slate-50 dark:bg-[#162032] p-2.5 rounded-lg border border-slate-100 dark:border-slate-800">
            <span class="text-[11px] font-medium text-slate-600 dark:text-slate-400 block">{ndc.sector}</span>
            <span class="text-xs font-mono font-bold text-[#047857] dark:text-[#34D399]">{ndc.target}</span>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  <!-- 8 Sectors Horizontal Tabs -->
  {#if taxonomyData?.sectors}
    <div class="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-thin">
      {#each Object.keys(taxonomyData.sectors) as secKey}
        {@const IconComp = sectorIcons[secKey] || Layers}
        <button
          type="button"
          onclick={() => {
            activeSectorKey = secKey;
            searchQuery = '';
          }}
          class="flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold shrink-0 cursor-pointer transition-all {activeSectorKey === secKey
            ? 'bg-[#047857] text-white dark:bg-[#34D399] dark:text-[#064E3B] shadow-xs'
            : 'bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-[#162032]'}"
        >
          <IconComp size={15} />
          <span>{secKey}</span>
        </button>
      {/each}
    </div>
  {/if}

  <!-- Sector Details and Item Cards -->
  {#if activeSector}
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm space-y-6">
      <!-- Sector Meta Strip -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-100 dark:border-slate-800">
        <div>
          <div class="flex items-center gap-2">
            <h2 class="text-lg font-headline font-bold text-slate-900 dark:text-slate-100">
              Sektor {activeSector.sector_name}
            </h2>
            <span class="font-mono text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
              {activeSector.sector_type}
            </span>
          </div>
          <span class="text-xs text-slate-500 font-mono mt-0.5 block">
            Adopsi: {activeSector.tkbi_version} • Kategori NDC: {activeSector.ndc_category}
          </span>
        </div>

        <!-- Search Bar within Active Sector -->
        <div class="relative w-full md:w-72">
          <Search size={14} class="absolute left-3 top-2.5 text-slate-400" />
          <input
            type="text"
            bind:value={searchQuery}
            placeholder="Cari Bab, KBLI, atau kriteria..."
            class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none"
          />
        </div>
      </div>

      <!-- Criteria Grid -->
      {#if filteredItems.length > 0}
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          {#each filteredItems as item}
            <div class="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-slate-50/50 dark:bg-[#162032]/40 flex flex-col justify-between gap-3 hover:border-slate-300 dark:hover:border-slate-700 transition-colors">
              <div class="space-y-2">
                <div class="flex items-start justify-between gap-2">
                  <span class="font-mono text-[11px] font-bold px-2 py-0.5 rounded bg-emerald-50 dark:bg-emerald-950/60 text-[#047857] dark:text-[#34D399] border border-emerald-200 dark:border-emerald-800">
                    {item.tsc_id}
                  </span>
                  <span class="font-mono text-[11px] px-2 py-0.5 rounded bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold">
                    KBLI {item.kbli}
                  </span>
                </div>

                <h3 class="text-xs font-headline font-bold text-slate-900 dark:text-slate-100 leading-snug">
                  {item.bab}
                </h3>

                <div class="text-[11px] font-semibold text-[#1D4ED8] dark:text-[#60A5FA]">
                  {item.tsc}
                </div>

                <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed font-body">
                  {item.criteria}
                </p>
              </div>

              <div class="pt-2 border-t border-slate-200/60 dark:border-slate-800/80 flex items-center justify-between text-[11px] font-mono">
                <span class="text-slate-400">Opsi Klasifikasi:</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{item.bentuk_jawaban}</span>
              </div>
            </div>
          {/each}
        </div>
      {:else}
        <div class="text-center py-12 text-slate-400 text-xs font-mono">
          Tidak ada kriteria yang cocok dengan pencarian "{searchQuery}".
        </div>
      {/if}
    </div>
  {:else if isLoading}
    <div class="text-center py-16 text-slate-400 text-xs font-mono">
      Memuat Master Taksonomi TKBI...
    </div>
  {/if}
</div>
