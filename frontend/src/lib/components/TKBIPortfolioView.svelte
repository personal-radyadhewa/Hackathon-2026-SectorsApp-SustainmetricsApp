<script>
  import { onMount } from 'svelte';
  import {
    PieChart,
    Plus,
    Trash2,
    Calculator,
    ShieldCheck,
    Layers,
    Building2,
    Landmark,
    TrendingUp,
    Info,
    RotateCcw,
  } from '@lucide/svelte';
  import { evaluateTKBIPortfolio } from '../api.js';
  import { t, currentLang } from '../i18n.js';

  let portfolioType = $state('HOLDING_CONSOLIDATED'); // HOLDING_CONSOLIDATED | FINANCIAL_INSTITUTION
  let financingType = $state('GENERAL_PURPOSE'); // GENERAL_PURPOSE | USE_OF_PROCEEDS

  // Default pre-loaded holding portfolio
  let items = $state([
    { name: 'Anak Usaha Geothermal (Clean Power)', amount: 6500.0, classification: 'HIJAU' },
    { name: 'Anak Usaha Transmisi & Smart Grid', amount: 3200.0, classification: 'HIJAU' },
    { name: 'Anak Usaha Gas Pembangkit Transisi Rendah Emisi', amount: 2800.0, classification: 'TRANSISI' },
    { name: 'Anak Usaha Co-Firing Biomassa (Program RMT 3 Thn)', amount: 1500.0, classification: 'TRANSISI INTERIM' },
    { name: 'Operasional Tambang Konvensional Sub-Kriteria', amount: 1000.0, classification: 'TIDAK MEMENUHI' },
  ]);

  // Form input for adding new item
  let newItemName = $state('');
  let newItemAmount = $state('');
  let newItemClass = $state('HIJAU');

  let result = $state(null);
  let isCalculating = $state(false);

  onMount(async () => {
    await handleCalculate();
  });

  async function handleCalculate() {
    isCalculating = true;
    try {
      const payload = {
        portfolio_type: portfolioType,
        financing_type: financingType,
        items: items.map((i) => ({
          name: i.name,
          amount: parseFloat(i.amount) || 0,
          classification: i.classification,
        })),
      };
      result = await evaluateTKBIPortfolio(payload);
    } catch (err) {
      console.error('Failed to evaluate portfolio:', err);
    } finally {
      isCalculating = false;
    }
  }

  function handleAddItem(e) {
    e.preventDefault();
    if (!newItemName.trim() || !newItemAmount) return;
    items = [
      ...items,
      {
        name: newItemName.trim(),
        amount: parseFloat(newItemAmount) || 0,
        classification: newItemClass,
      },
    ];
    newItemName = '';
    newItemAmount = '';
    handleCalculate();
  }

  function handleRemoveItem(index) {
    items = items.filter((_, i) => i !== index);
    handleCalculate();
  }
</script>

<div class="space-y-6">
  <!-- Plain Explanation Top Callout -->
  <div class="p-4 rounded-xl bg-indigo-50/80 dark:bg-[#131A2E] border border-indigo-200/90 dark:border-indigo-800/80 flex items-start gap-3.5 text-xs shadow-2xs">
    <div class="p-2 rounded-lg bg-indigo-100 dark:bg-indigo-950/80 text-indigo-700 dark:text-indigo-400 shrink-0">
      <PieChart size={18} />
    </div>
    <div class="space-y-1">
      <div class="font-headline font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
        <span>{$currentLang === 'id' ? 'Apa Fungsi Halaman Ini?' : 'What is this page for?'}</span>
        <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-900/60 text-indigo-800 dark:text-indigo-300 font-bold">
          {$currentLang === 'id' ? 'Kalkulator Grup & Holding' : 'Group Calculator'}
        </span>
      </div>
      <p class="text-slate-600 dark:text-slate-300 leading-relaxed font-body">
        {$currentLang === 'id'
          ? 'Halaman ini adalah kalkulator portofolio. Jika satu induk perusahaan (holding) atau bank memiliki banyak anak usaha atau pinjaman proyek, halaman ini menghitung berapa persen total aset yang sudah berstatus Hijau vs yang masih Kuning atau belum sesuai.'
          : 'This page is a portfolio aggregator. When a holding conglomerate or commercial bank finances multiple subsidiaries or projects, this calculator aggregates the exact weighted percentage of green vs transition assets.'}
      </p>
    </div>
  </div>

  <!-- Top Banner -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-[#047857] dark:text-[#34D399] shrink-0">
        <PieChart size={24} />
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-xl font-headline font-bold text-slate-900 dark:text-slate-100">
            {$currentLang === 'id' ? 'Kalkulator Portofolio & Holding (OJK)' : 'OJK Tingkat 2 & 3 Aggregator'}
          </h1>
          <span class="font-mono text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300">
            OJK Pg. 4-5
          </span>
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-2xl">
          {$currentLang === 'id'
            ? 'Hitung proporsi gabungan aset Hijau, Transisi, dan Interim untuk entitas holding korporasi atau bank.'
            : 'Aggregates weighted green, transition, and interim compliance scores for corporate holdings and financial institutions.'}
        </p>
      </div>
    </div>
  </div>

  <!-- Configuration Mode Selector -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <!-- Mode 1: Tingkat Agregasi -->
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-4 shadow-sm space-y-2">
      <span class="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider block">
        1. Hierarki Agregasi OJK
      </span>
      <div class="grid grid-cols-2 gap-2">
        <button
          type="button"
          onclick={() => {
            portfolioType = 'HOLDING_CONSOLIDATED';
            handleCalculate();
          }}
          class="p-2.5 rounded-lg border text-left cursor-pointer transition-all {portfolioType === 'HOLDING_CONSOLIDATED'
            ? 'border-[#047857] bg-emerald-50/50 dark:bg-emerald-950/40 text-[#047857] dark:text-[#34D399] font-bold'
            : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032] text-slate-600 dark:text-slate-400'}"
        >
          <div class="flex items-center gap-1.5 text-xs font-headline">
            <Building2 size={14} />
            <span>Tingkat 2: Holding Korporasi</span>
          </div>
          <span class="text-[10px] text-slate-500 font-normal block mt-0.5">Konsolidasi anak usaha</span>
        </button>

        <button
          type="button"
          onclick={() => {
            portfolioType = 'FINANCIAL_INSTITUTION';
            handleCalculate();
          }}
          class="p-2.5 rounded-lg border text-left cursor-pointer transition-all {portfolioType === 'FINANCIAL_INSTITUTION'
            ? 'border-[#047857] bg-emerald-50/50 dark:bg-emerald-950/40 text-[#047857] dark:text-[#34D399] font-bold'
            : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032] text-slate-600 dark:text-slate-400'}"
        >
          <div class="flex items-center gap-1.5 text-xs font-headline">
            <Landmark size={14} />
            <span>Tingkat 3: Portofolio Bank / LJK</span>
          </div>
          <span class="text-[10px] text-slate-500 font-normal block mt-0.5">Eksposur pinjaman/investasi</span>
        </button>
      </div>
    </div>

    <!-- Mode 2: Jenis Pembiayaan -->
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-4 shadow-sm space-y-2">
      <span class="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider block">
        2. Ketentuan Jenis Pembiayaan OJK
      </span>
      <div class="grid grid-cols-2 gap-2">
        <button
          type="button"
          onclick={() => {
            financingType = 'GENERAL_PURPOSE';
            handleCalculate();
          }}
          class="p-2.5 rounded-lg border text-left cursor-pointer transition-all {financingType === 'GENERAL_PURPOSE'
            ? 'border-blue-500 bg-blue-50/50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 font-bold'
            : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032] text-slate-600 dark:text-slate-400'}"
        >
          <div class="text-xs font-headline">General Purpose Financing</div>
          <span class="text-[10px] text-slate-500 font-normal block mt-0.5">Penilaian agregasi entitas debitur</span>
        </button>

        <button
          type="button"
          onclick={() => {
            financingType = 'USE_OF_PROCEEDS';
            handleCalculate();
          }}
          class="p-2.5 rounded-lg border text-left cursor-pointer transition-all {financingType === 'USE_OF_PROCEEDS'
            ? 'border-blue-500 bg-blue-50/50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 font-bold'
            : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-[#162032] text-slate-600 dark:text-slate-400'}"
        >
          <div class="text-xs font-headline">Use of Proceeds Financing</div>
          <span class="text-[10px] text-slate-500 font-normal block mt-0.5">Penilaian langsung aktivitas proyek</span>
        </button>
      </div>
    </div>
  </div>

  <!-- KPI Result Summary Cards -->
  {#if result}
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-3.5 shadow-sm">
        <span class="text-[10px] font-mono uppercase text-slate-400 block font-semibold">Total Eksposur</span>
        <span class="font-mono text-base font-bold text-slate-900 dark:text-slate-100 mt-1 block">
          IDR {result.total_exposure.toLocaleString()}B
        </span>
      </div>

      <div class="bg-white dark:bg-[#0F172A] border border-emerald-200 dark:border-emerald-800 rounded-xl p-3.5 shadow-sm bg-emerald-50/20">
        <span class="text-[10px] font-mono uppercase text-[#047857] dark:text-[#34D399] block font-semibold">Hijau (TSC)</span>
        <span class="font-mono text-base font-bold text-[#047857] dark:text-[#34D399] mt-1 block">
          {result.pct_hijau}%
        </span>
      </div>

      <div class="bg-white dark:bg-[#0F172A] border border-amber-200 dark:border-amber-800 rounded-xl p-3.5 shadow-sm bg-amber-50/20">
        <span class="text-[10px] font-mono uppercase text-amber-700 dark:text-amber-400 block font-semibold">Transisi</span>
        <span class="font-mono text-base font-bold text-amber-700 dark:text-amber-400 mt-1 block">
          {result.pct_transisi}%
        </span>
      </div>

      <div class="bg-white dark:bg-[#0F172A] border border-sky-200 dark:border-sky-800 rounded-xl p-3.5 shadow-sm bg-sky-50/20">
        <span class="text-[10px] font-mono uppercase text-sky-700 dark:text-sky-400 block font-semibold">Transisi Interim</span>
        <span class="font-mono text-base font-bold text-sky-700 dark:text-sky-400 mt-1 block">
          {result.pct_transisi_interim}%
        </span>
      </div>

      <div class="bg-white dark:bg-[#0F172A] border border-rose-200 dark:border-rose-800 rounded-xl p-3.5 shadow-sm bg-rose-50/20">
        <span class="text-[10px] font-mono uppercase text-rose-700 dark:text-rose-400 block font-semibold">Tidak Memenuhi</span>
        <span class="font-mono text-base font-bold text-rose-700 dark:text-rose-400 mt-1 block">
          {result.pct_tidak_memenuhi}%
        </span>
      </div>

      <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-3.5 shadow-sm bg-slate-50 dark:bg-[#162032]">
        <span class="text-[10px] font-mono uppercase text-slate-600 dark:text-slate-300 block font-semibold">Total Rasio Hijau</span>
        <span class="font-mono text-base font-bold text-[#047857] dark:text-[#34D399] mt-1 block">
          {result.weighted_green_transition_ratio}%
        </span>
      </div>
    </div>

    <!-- Segmented Stacked Progress Bar -->
    <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-4 shadow-sm space-y-2">
      <div class="flex items-center justify-between text-xs font-mono">
        <span class="font-bold text-slate-700 dark:text-slate-300">Komposisi Portofolio Teragregasi</span>
        <span class="text-[#047857] dark:text-[#34D399] font-bold">
          {result.weighted_green_transition_ratio}% Memenuhi Ambang Batas OJK
        </span>
      </div>

      <div class="h-4 w-full rounded-full bg-slate-100 dark:bg-slate-800 flex overflow-hidden">
        <div style="width: {result.pct_hijau}%" class="bg-[#047857]" title="Hijau: {result.pct_hijau}%"></div>
        <div style="width: {result.pct_transisi}%" class="bg-[#D97706]" title="Transisi: {result.pct_transisi}%"></div>
        <div style="width: {result.pct_transisi_interim}%" class="bg-[#0284C7]" title="Transisi Interim: {result.pct_transisi_interim}%"></div>
        <div style="width: {result.pct_tidak_memenuhi}%" class="bg-[#DC2626]" title="Tidak Memenuhi: {result.pct_tidak_memenuhi}%"></div>
        <div style="width: {result.pct_out_of_scope}%" class="bg-slate-400" title="Out of Scope: {result.pct_out_of_scope}%"></div>
      </div>

      <p class="text-xs text-slate-500 dark:text-slate-400 pt-1 font-body">
        {result.regulatory_summary}
      </p>
    </div>
  {/if}

  <!-- Asset / Debitur Table & Add Form -->
  <div class="bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-xl p-6 shadow-sm space-y-5">
    <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
      <h2 class="text-base font-headline font-bold text-slate-900 dark:text-slate-100">
        Rincian Entitas / Eksposur Kredit
      </h2>
      <span class="font-mono text-xs text-slate-400">{items.length} Entitas Terdaftar</span>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-xs text-left">
        <thead class="text-[11px] font-mono uppercase bg-slate-50 dark:bg-[#162032] text-slate-400 border-b border-slate-100 dark:border-slate-800">
          <tr>
            <th class="py-2.5 px-3">Nama Entitas / Aset</th>
            <th class="py-2.5 px-3">Eksposur (IDR B)</th>
            <th class="py-2.5 px-3">Klasifikasi OJK</th>
            <th class="py-2.5 px-3 text-right">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-800 font-body">
          {#each items as item, idx}
            <tr class="hover:bg-slate-50/50 dark:hover:bg-[#162032]/40">
              <td class="py-2.5 px-3 font-medium text-slate-900 dark:text-slate-100">{item.name}</td>
              <td class="py-2.5 px-3 font-mono font-bold text-slate-700 dark:text-slate-300">
                IDR {item.amount.toLocaleString()}B
              </td>
              <td class="py-2.5 px-3">
                <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold {item.classification === 'HIJAU'
                  ? 'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300'
                  : item.classification === 'TRANSISI'
                  ? 'bg-amber-50 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300'
                  : item.classification === 'TRANSISI INTERIM'
                  ? 'bg-sky-50 text-sky-800 dark:bg-sky-950/60 dark:text-sky-300'
                  : 'bg-rose-50 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300'}">
                  {item.classification}
                </span>
              </td>
              <td class="py-2.5 px-3 text-right">
                <button
                  type="button"
                  onclick={() => handleRemoveItem(idx)}
                  class="text-slate-400 hover:text-rose-500 cursor-pointer p-1"
                  title="Hapus baris"
                >
                  <Trash2 size={13} />
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <!-- Add Item Form -->
    <form onsubmit={handleAddItem} class="pt-3 border-t border-slate-100 dark:border-slate-800 flex flex-wrap sm:flex-nowrap items-center gap-2.5">
      <input
        type="text"
        bind:value={newItemName}
        placeholder="Nama Anak Usaha / Debitur Pinjaman..."
        class="flex-1 bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-900 dark:text-slate-100 focus:outline-none"
      />
      <input
        type="number"
        step="0.1"
        bind:value={newItemAmount}
        placeholder="Nilai (IDR B)..."
        class="w-36 bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs font-mono text-slate-900 dark:text-slate-100 focus:outline-none"
      />
      <select
        bind:value={newItemClass}
        class="bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-medium text-slate-900 dark:text-slate-100 focus:outline-none"
      >
        <option value="HIJAU">HIJAU</option>
        <option value="TRANSISI">TRANSISI</option>
        <option value="TRANSISI INTERIM">TRANSISI INTERIM</option>
        <option value="TIDAK MEMENUHI">TIDAK MEMENUHI</option>
      </select>
      <button
        type="submit"
        class="px-3.5 py-1.5 bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] font-semibold text-xs rounded-lg flex items-center gap-1.5 shrink-0 cursor-pointer shadow-2xs"
      >
        <Plus size={14} />
        <span>Tambah</span>
      </button>
    </form>
  </div>
</div>
