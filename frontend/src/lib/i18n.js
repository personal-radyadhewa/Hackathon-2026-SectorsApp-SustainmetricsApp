// Simple, accessible bilingual i18n store for SustainMetric IDX
// Plain-language dictionary: eliminates hard jargon, explains metrics simply.

import { writable, derived } from 'svelte/store';

const STORAGE_KEY = 'sustainmetric_language';

const initialLang = (() => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'id' || saved === 'en') return saved;
    return navigator.language.startsWith('id') ? 'id' : 'en';
  } catch (e) {
    return 'id';
  }
})();

export const currentLang = writable(initialLang);

export function setLanguage(lang) {
  if (lang === 'id' || lang === 'en') {
    currentLang.set(lang);
    try {
      localStorage.setItem(STORAGE_KEY, lang);
      document.documentElement.lang = lang;
    } catch (e) {}
  }
}

export function toggleLanguage() {
  currentLang.update((l) => {
    const next = l === 'id' ? 'en' : 'id';
    try {
      localStorage.setItem(STORAGE_KEY, next);
      document.documentElement.lang = next;
    } catch (e) {}
    return next;
  });
}

export const translations = {
  en: {
    // Brand & App
    appName: 'SustainMetric IDX',
    appSubtitle: 'Green & Environmental Checker for Indonesian Companies',
    verifiedData: 'Verified Stock Data: Live',
    selectCompany: 'Pick a Company',
    auditDirectory: 'Company Health Check',
    auditNow: 'Run Check Now',
    auditing: 'Checking',
    askAi: 'Ask Assistant',
    browseWatchlist: 'View Saved Companies',
    loadingProfile: 'Getting company details for',
    esgMandateNotice: 'Green Standards Active',
    esgMandateDesc: 'Monitoring Indonesia (OJK) green business rules.',
    auditorLead: 'Lead Reviewer',

    // Nav sections
    navAnalysis: 'Company Analysis',
    navTkbiFlow: 'Green Rules Guide (OJK)',
    navAiTools: 'AI & Automation',

    // Views
    watchlist: 'My Saved Companies',
    watchlistDesc: 'Pick Indonesian listed companies to review their eco-friendliness and safety.',
    dashboard: 'Company Overview & Health',
    tkbi: 'Green Checklist (OJK TKBI)',
    traces: 'Claim & Evidence Trail',
    simulator: 'Green Checker Simulator',
    explorer: '8 Business Categories',
    sunsetting: 'Green Debt & Grace Period Stress-Test',
    chat: 'Ask AI Assistant',
    schedules: 'Automated Check Schedules',
    analysisOverview: 'Company Analysis Guide',
    tkbiOverview: 'Green Rules Guide & Directory',

    // Watchlist Banner & Cards
    watchlistHeader: 'Company Watchlist & Eco-Checker',
    watchlistSub: 'Select any company to see if they meet Indonesian environmental rules and if their finances can support green improvements.',
    savedCompaniesCard: 'Saved Companies',
    savedCompaniesSub: 'Actively tracked in your list',
    greenAlignmentCard: 'Average Green Score',
    greenAlignmentSub: 'How closely companies follow environmental rules',
    cashCushionCard: 'Financial Cushion',
    cashCushionSub: 'Ability to fund projects with own earnings',
    standardCard: 'Official Standard',
    standardSub: 'Indonesia Green Taxonomy (OJK TKBI)',
    readyForAuditTitle: 'Companies Ready for Free AI Check',
    readyForAuditDesc: 'Click check to automatically see environmental rating and simple summary points.',
    auditAll: 'Check All',
    runAiAudit: 'Run AI Check',
    openProfile: 'Open Details',
    searchWatchlist: 'Search by ticker code or company name...',
    allIdxDatabase: 'Full Stock Directory',
    topGreenLeaders: 'Green Leaders',
    energySector: 'Energy Sector',
    financeSector: 'Finance Sector',
    companiesFound: 'companies shown',
    
    // Status and badges in plain words
    statusGreen: 'Pass (Green)',
    statusYellow: 'In Progress (Yellow)',
    statusRed: 'Not Ready (Red)',
    statusPending: 'Needs Check',
    selfFunded: 'Self-Funded',
    leveraged: 'Needs Borrowing',

    // Common Buttons & Labels
    add: 'Add',
    searchPlaceholder: 'Search company name or 4-letter code...',
    addCompanyPlaceholder: '+ Code (e.g. BBCA, TLKM)',
    availableCodes: 'AVAILABLE INDONESIA (IDX) CODES',
    activeBadge: 'Active',
    addBadge: '+ Add',
    remove: 'Remove',
    save: 'Save',
    cancel: 'Cancel',
    status: 'Status',
    score: 'Eco Score',
    grade: 'Rating',
    actions: 'Actions',
    overview: 'Overview',
    details: 'Details',
    allCompanies: 'All Companies',
    greenStatus: 'Eco-Friendly (Green)',
    yellowStatus: 'In Transition (Yellow)',
    redStatus: 'Not Compliant (Red)',
    naStatus: 'Need More Info',
    
    // Simple explanations
    greenExplanation: 'Meets official green criteria with no environmental harm.',
    yellowExplanation: 'Improving their environmental impact over time.',
    redExplanation: 'Does not meet environmental standards yet.',
    
    // Language Toggle
    langButton: 'Bahasa Indonesia',
    langShort: 'ID',
    themeToggle: 'Switch theme',
  },
  id: {
    // Brand & App
    appName: 'SustainMetric IDX',
    appSubtitle: 'Pemeriksa Ramah Lingkungan untuk Saham Perusahaan Indonesia',
    verifiedData: 'Data Saham Terverifikasi: Aktif',
    selectCompany: 'Pilih Perusahaan',
    auditDirectory: 'Pemeriksaan Perusahaan',
    auditNow: 'Periksa Sekarang',
    auditing: 'Sedang Memeriksa',
    askAi: 'Tanya Asisten AI',
    browseWatchlist: 'Lihat Daftar Pantau',
    loadingProfile: 'Mengambil data perusahaan untuk',
    esgMandateNotice: 'Standar Hijau Aktif',
    esgMandateDesc: 'Memantau kesesuaian aturan Taksonomi Hijau OJK.',
    auditorLead: 'Pemeriksa Utama',

    // Nav sections
    navAnalysis: 'Analisis Perusahaan',
    navTkbiFlow: 'Panduan Aturan Hijau (OJK)',
    navAiTools: 'AI & Otomasi',

    // Views
    watchlist: 'Daftar Pantau',
    watchlistDesc: 'Pilih emiten bursa efek untuk memeriksa seberapa ramah lingkungan bisnis mereka.',
    dashboard: 'Ringkasan Emiten',
    tkbi: 'Cek Standar Hijau',
    traces: 'Jejak Bukti Klaim',
    simulator: 'Simulasi Aturan OJK',
    explorer: '8 Sektor Usaha',
    sunsetting: 'Uji Proteksi Utang Hijau (Grace Period)',
    chat: 'Tanya Asisten AI',
    schedules: 'Jadwal Cek Otomatis',
    analysisOverview: 'Panduan Analisis Perusahaan',
    tkbiOverview: 'Panduan Aturan Hijau (OJK)',

    // Watchlist Banner & Cards
    watchlistHeader: 'Daftar Pantauan Saham & Kategori Hijau',
    watchlistSub: 'Pilih perusahaan mana saja untuk melihat kesesuaian aturan lingkungan hidup OJK dan apakah keuangan mereka sanggup membiayai usaha hijau.',
    savedCompaniesCard: 'Perusahaan Dipantau',
    savedCompaniesSub: 'Tersimpan aktif di daftar Anda',
    greenAlignmentCard: 'Rata-Rata Skor Hijau',
    greenAlignmentSub: 'Seberapa patuh perusahaan terhadap aturan lingkungan',
    cashCushionCard: 'Kekuatan Finansial',
    cashCushionSub: 'Kemampuan mendanai proyek dengan kas sendiri',
    standardCard: 'Standar Resmi',
    standardSub: 'Panduan Taksonomi Hijau OJK (TKBI)',
    readyForAuditTitle: 'Perusahaan Siap Diperiksa AI',
    readyForAuditDesc: 'Klik periksa untuk langsung mengetahui kategori hijau dan rangkuman sederhana dari asisten AI.',
    auditAll: 'Periksa Semua',
    runAiAudit: 'Periksa dengan AI',
    openProfile: 'Buka Detail',
    searchWatchlist: 'Cari kode saham atau nama perusahaan...',
    allIdxDatabase: 'Daftar Semua Saham IDX',
    topGreenLeaders: 'Unggulan Hijau',
    energySector: 'Sektor Energi',
    financeSector: 'Sektor Keuangan',
    companiesFound: 'perusahaan ditemukan',

    // Status and badges in plain words
    statusGreen: 'Lolos (Hijau)',
    statusYellow: 'Berbenah (Kuning)',
    statusRed: 'Belum Sesuai (Merah)',
    statusPending: 'Perlu Cek',
    selfFunded: 'Kas Sendiri Cukup',
    leveraged: 'Perlu Pinjaman',

    // Common Buttons & Labels
    add: 'Tambah',
    searchPlaceholder: 'Cari nama perusahaan atau 4 huruf kode saham...',
    addCompanyPlaceholder: '+ Kode (misal BBCA, TLKM)',
    availableCodes: 'KODE SAHAM BURSA (IDX) TERSEDIA',
    activeBadge: 'Aktif',
    addBadge: '+ Tambah',
    remove: 'Hapus',
    save: 'Simpan',
    cancel: 'Batal',
    status: 'Status',
    score: 'Skor Hijau',
    grade: 'Peringkat',
    actions: 'Aksi',
    overview: 'Ringkasan',
    details: 'Detail',
    allCompanies: 'Semua Perusahaan',
    greenStatus: 'Ramah Lingkungan (Hijau)',
    yellowStatus: 'Masa Perbaikan (Kuning)',
    redStatus: 'Belum Sesuai (Merah)',
    naStatus: 'Perlu Data Tambahan',

    // Simple explanations
    greenExplanation: 'Memenuhi syarat usaha ramah lingkungan tanpa merusak alam.',
    yellowExplanation: 'Sedang berbenah mengurangi dampak lingkungan secara bertahap.',
    redExplanation: 'Belum memenuhi standar lingkungan yang berlaku.',

    // Language Toggle
    langButton: 'English',
    langShort: 'EN',
    themeToggle: 'Ganti tema',
  },
};

export const t = derived(currentLang, ($lang) => translations[$lang] || translations.id);
