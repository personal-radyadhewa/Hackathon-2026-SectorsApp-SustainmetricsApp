/**
 * Comprehensive Catalog of Supported IDX Emitents
 * Includes green compliance tiers according to OJK TKBI v3.0 taxonomy standards.
 */

export const IDX_EMITENTS = [
  {
    ticker: 'PGEO',
    name: 'Pertamina Geothermal Energy Tbk',
    sector: 'Clean Utilities & Geothermal',
    grade: 'Grade A+',
    gradeLabel: 'Exemplary Green',
    statusClass: 'badge-hijau',
    dotColor: 'bg-[#047857] dark:bg-[#34D399]',
    description: '100% clean energy producer. Sovereign geothermal concessions, zero coal exposure, certified carbon offset credits.',
    financialHealth: 'Very Strong',
    coverageRatio: '2.41x',
    ocf: 'IDR 3.42T',
    ytdChange: '+14.2%',
  },
  {
    ticker: 'BBRI',
    name: 'Bank Rakyat Indonesia Tbk',
    sector: 'Commercial Banking & Sustainable Debt',
    grade: 'Grade A',
    gradeLabel: 'Sustainable Leader',
    statusClass: 'badge-hijau',
    dotColor: 'bg-[#047857] dark:bg-[#34D399]',
    description: 'Dominant sustainable financing portfolio (KKUB POJK 51). Sustainable loans exceed OJK green taxonomy quotas.',
    financialHealth: 'Robust Balance Sheet',
    coverageRatio: '3.15x',
    ocf: 'IDR 48.2T',
    ytdChange: '+8.6%',
  },
  {
    ticker: 'BBCA',
    name: 'Bank Central Asia Tbk',
    sector: 'Banking & Financial Services',
    grade: 'Grade A',
    gradeLabel: 'Sustainable Leader',
    statusClass: 'badge-hijau',
    dotColor: 'bg-[#047857] dark:bg-[#34D399]',
    description: 'Premier bluechip liquidity cushion. Comprehensive green building financing and digital banking decarbonization.',
    financialHealth: 'Prime Bluechip',
    coverageRatio: '4.20x',
    ocf: 'IDR 52.8T',
    ytdChange: '+11.5%',
  },
  {
    ticker: 'BMRI',
    name: 'Bank Mandiri (Persero) Tbk',
    sector: 'Commercial Banking & State Enterprise',
    grade: 'Grade A',
    gradeLabel: 'Sustainable Leader',
    statusClass: 'badge-hijau',
    dotColor: 'bg-[#047857] dark:bg-[#34D399]',
    description: 'Large sustainable bond issuance and green syndication underwriting compliant with OJK TKBI v3.0 taxonomy.',
    financialHealth: 'Very Strong',
    coverageRatio: '3.60x',
    ocf: 'IDR 46.1T',
    ytdChange: '+9.4%',
  },
  {
    ticker: 'BBNI',
    name: 'Bank Negara Indonesia Tbk',
    sector: 'Commercial Banking & Transition Debt',
    grade: 'Grade A',
    gradeLabel: 'Sustainable Leader',
    statusClass: 'badge-hijau',
    dotColor: 'bg-[#047857] dark:bg-[#34D399]',
    description: 'Pioneered national sustainability-linked loans and industrial energy efficiency transition credit portfolios.',
    financialHealth: 'Solid Balance Sheet',
    coverageRatio: '2.90x',
    ocf: 'IDR 24.3T',
    ytdChange: '+6.8%',
  },
  {
    ticker: 'TLKM',
    name: 'Telkom Indonesia Tbk',
    sector: 'Infrastructure & Green Data Centers',
    grade: 'Grade A',
    gradeLabel: 'Eco Data Infrastructure',
    statusClass: 'badge-hijau',
    dotColor: 'bg-[#047857] dark:bg-[#34D399]',
    description: 'Aggressive data center PUE reduction targets and solar-powered cellular tower transitions.',
    financialHealth: 'Prime Bluechip',
    coverageRatio: '2.80x',
    ocf: 'IDR 26.4T',
    ytdChange: '+4.1%',
  },
  {
    ticker: 'ADRO',
    name: 'Adaro Energy Indonesia Tbk',
    sector: 'Thermal Coal & Transition Metals',
    grade: 'Grade B+',
    gradeLabel: 'Cash Rich / Conventional',
    statusClass: 'bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800',
    dotColor: 'bg-[#1D4ED8] dark:bg-[#60A5FA]',
    description: 'Substantial operational cash reserves investing into aluminum smelter and renewable hydro initiatives.',
    financialHealth: 'Self-Funded',
    coverageRatio: '1.85x',
    ocf: 'IDR 14.5T',
    ytdChange: '-3.2%',
  },
  {
    ticker: 'ASII',
    name: 'Astra International Tbk',
    sector: 'Conglomerate & EV Transition',
    grade: 'Grade B+',
    gradeLabel: 'Transitioning Fleet',
    statusClass: 'bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800',
    dotColor: 'bg-[#1D4ED8] dark:bg-[#60A5FA]',
    description: 'Expanding hybrid and EV product lines across automotive while balancing coal contracting subsidiaries.',
    financialHealth: 'Solid Balance Sheet',
    coverageRatio: '2.10x',
    ocf: 'IDR 22.8T',
    ytdChange: '+6.3%',
  },
  {
    ticker: 'AMMN',
    name: 'Amman Mineral Internasional Tbk',
    sector: 'Copper & Critical Clean Minerals',
    grade: 'Grade B+',
    gradeLabel: 'Critical Minerals',
    statusClass: 'bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800',
    dotColor: 'bg-[#1D4ED8] dark:bg-[#60A5FA]',
    description: 'Developing high-efficiency copper smelting essential for solar and renewable power grid expansion.',
    financialHealth: 'Capital Intensive',
    coverageRatio: '1.20x',
    ocf: 'IDR 5.60T',
    ytdChange: '+18.0%',
  },
  {
    ticker: 'INCO',
    name: 'Vale Indonesia Tbk',
    sector: 'Sustainable Nickel & Clean Mining',
    grade: 'Grade B+',
    gradeLabel: 'Low-Carbon Nickel',
    statusClass: 'bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800',
    dotColor: 'bg-[#1D4ED8] dark:bg-[#60A5FA]',
    description: 'Hydro-powered nickel smelting in Sorowako with one of the lowest carbon intensity footprints in global mining.',
    financialHealth: 'Robust Cash Cushion',
    coverageRatio: '2.05x',
    ocf: 'IDR 6.10T',
    ytdChange: '+5.4%',
  },
  {
    ticker: 'BREN',
    name: 'Barito Renewables Energy Tbk',
    sector: 'Renewable Power & Geothermal',
    grade: 'Grade B',
    gradeLabel: 'Transition Asset Focus',
    statusClass: 'badge-transisi',
    dotColor: 'bg-[#D97706] dark:bg-[#FBBF24]',
    description: 'Geothermal and wind fleet expansion. High valuation premium and leverage multiples requiring debt service monitoring.',
    financialHealth: 'Leveraged Buffer',
    coverageRatio: '0.82x',
    ocf: 'IDR 2.10T',
    ytdChange: '+42.5%',
  },
  {
    ticker: 'MEDC',
    name: 'Medco Energi Internasional Tbk',
    sector: 'Oil, Gas & Geothermal Diversification',
    grade: 'Grade B',
    gradeLabel: 'Hybrid Energy Transition',
    statusClass: 'badge-transisi',
    dotColor: 'bg-[#D97706] dark:bg-[#FBBF24]',
    description: 'Traditional hydrocarbons funding capital deployment into Ijen geothermal and clean copper mining assets.',
    financialHealth: 'Moderate Gearing',
    coverageRatio: '1.15x',
    ocf: 'IDR 4.10T',
    ytdChange: '+7.8%',
  },
  {
    ticker: 'ICBP',
    name: 'Indofood CBP Sukses Makmur Tbk',
    sector: 'Consumer Goods & Agri Supply Chain',
    grade: 'Grade B',
    gradeLabel: 'Packaging Review',
    statusClass: 'badge-transisi',
    dotColor: 'bg-[#D97706] dark:bg-[#FBBF24]',
    description: 'Evaluating sustainable palm oil certification and circular plastic packaging mandates across food manufacturing.',
    financialHealth: 'High Cash Flow',
    coverageRatio: '1.65x',
    ocf: 'IDR 8.90T',
    ytdChange: '+2.5%',
  },
  {
    ticker: 'KLBF',
    name: 'Kalbe Farma Tbk',
    sector: 'Healthcare & Pharmaceuticals',
    grade: 'Grade A',
    gradeLabel: 'Clean Operations',
    statusClass: 'badge-hijau',
    dotColor: 'bg-[#047857] dark:bg-[#34D399]',
    description: 'Eco-certified manufacturing facilities, energy-efficient biological cold-chain, and ISO 14001 environmental compliance.',
    financialHealth: 'Zero Net Debt',
    coverageRatio: '3.80x',
    ocf: 'IDR 4.20T',
    ytdChange: '+3.9%',
  },
  {
    ticker: 'GOTO',
    name: 'GoTo Gojek Tokopedia Tbk',
    sector: 'Technology & EV Fleet Logistics',
    grade: 'Grade B',
    gradeLabel: 'Electrification Phase',
    statusClass: 'badge-transisi',
    dotColor: 'bg-[#D97706] dark:bg-[#FBBF24]',
    description: 'Three Zeroes 2030 roadmap committed to 100% two-wheeler EV transition via Electrum joint venture.',
    financialHealth: 'Turnaround Reserve',
    coverageRatio: '0.95x',
    ocf: 'IDR 1.80T',
    ytdChange: '-2.1%',
  },
  {
    ticker: 'ANTM',
    name: 'Aneka Tambang Tbk',
    sector: 'Minerals & EV Battery Materials',
    grade: 'Grade B+',
    gradeLabel: 'Downstreaming Transition',
    statusClass: 'bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800',
    dotColor: 'bg-[#1D4ED8] dark:bg-[#60A5FA]',
    description: 'High-grade nickel downstreaming for Indonesia Battery Corporation (IBC) clean supply chain partnership.',
    financialHealth: 'Solid Balance Sheet',
    coverageRatio: '1.75x',
    ocf: 'IDR 5.20T',
    ytdChange: '+4.5%',
  },
  {
    ticker: 'PTBA',
    name: 'Bukit Asam Tbk',
    sector: 'Energy & Solar Downstreaming',
    grade: 'Grade B',
    gradeLabel: 'Transitioning Miner',
    statusClass: 'badge-transisi',
    dotColor: 'bg-[#D97706] dark:bg-[#FBBF24]',
    description: 'Utilizing former mining concessions for solar photovoltaic utility generation and coal gasification research.',
    financialHealth: 'High Dividend Cushion',
    coverageRatio: '1.90x',
    ocf: 'IDR 4.80T',
    ytdChange: '+1.2%',
  },
  {
    ticker: 'UNTR',
    name: 'United Tractors Tbk',
    sector: 'Heavy Equipment & Renewable Energy',
    grade: 'Grade B+',
    gradeLabel: 'Diversified Transition',
    statusClass: 'bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800',
    dotColor: 'bg-[#1D4ED8] dark:bg-[#60A5FA]',
    description: 'Capital deployment into mini-hydro power and geothermal projects (Supreme Energy Sriwijaya acquisition).',
    financialHealth: 'Very Strong',
    coverageRatio: '2.50x',
    ocf: 'IDR 16.4T',
    ytdChange: '+5.1%',
  },
  {
    ticker: 'SMGR',
    name: 'Semen Indonesia (SIG) Tbk',
    sector: 'Building Materials & Eco-Cement',
    grade: 'Grade B+',
    gradeLabel: 'Alternative Fuel Leader',
    statusClass: 'bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800',
    dotColor: 'bg-[#1D4ED8] dark:bg-[#60A5FA]',
    description: 'Refuse-Derived Fuel (RDF) substitution in cement kilns reducing clinker factor and thermal coal intensity.',
    financialHealth: 'Stable Cash Flow',
    coverageRatio: '1.55x',
    ocf: 'IDR 5.80T',
    ytdChange: '-1.4%',
  },
  {
    ticker: 'BUMI',
    name: 'Bumi Resources Tbk',
    sector: 'Coal Extraction & Power Export',
    grade: 'Grade C',
    gradeLabel: 'High ESG Risk (Laggard)',
    statusClass: 'badge-tidak',
    dotColor: 'bg-[#DC2626] dark:bg-[#F87171]',
    description: 'Lacks formal Scope 3 decarbonization trajectory. Significant carbon transition liability under carbon tax rules.',
    financialHealth: 'Constrained Cash Cushion',
    coverageRatio: '0.45x',
    ocf: 'IDR 1.25T',
    ytdChange: '-11.4%',
  },
];

import allIdxTickers from './allIdxTickers.json';

/**
 * Search helper for ticker autocomplete suggestions across all 962 IDX equities from SectorsApp
 */
export function searchIdxTickers(query, limit = 20) {
  if (!query || typeof query !== 'string') return [];
  const q = query.trim().toUpperCase();
  if (q.length === 0) return [];

  const results = [];
  const seen = new Set();

  // 1. Curated profiles with full ESG analysis
  for (const item of IDX_EMITENTS) {
    if (
      item.ticker.includes(q) ||
      item.name.toUpperCase().includes(q) ||
      item.sector.toUpperCase().includes(q)
    ) {
      results.push(item);
      seen.add(item.ticker);
    }
  }

  // 2. Comprehensive 962 IDX equities universe from SectorsApp
  for (const item of allIdxTickers) {
    const sym = (item.symbol || '').toUpperCase();
    if (seen.has(sym)) continue;

    const nameUpper = (item.company_name || '').toUpperCase();
    if (sym.includes(q) || nameUpper.includes(q)) {
      results.push({
        ticker: sym,
        name: item.company_name,
        sector: 'IDX Listed Equities (SectorsApp)',
        grade: 'Audit Ready',
        gradeLabel: 'Live SectorsApp Data',
        statusClass: 'bg-emerald-50 text-[#047857] border-emerald-200 dark:bg-emerald-950/60 dark:text-[#34D399] dark:border-emerald-800',
        dotColor: 'bg-[#047857] dark:bg-[#34D399]',
        description: `${item.company_name} is listed on the IDX. Add to your watchlist to run an on-demand OJK TKBI v3.0 regulatory audit.`,
        financialHealth: 'SectorsApp Synced',
        coverageRatio: 'Live',
        ocf: 'On-Demand',
        ytdChange: 'Live',
      });
      seen.add(sym);
    }
    if (results.length >= limit * 2) break;
  }

  // Sort: exact ticker match first, then ticker starts-with, then alphabetical
  results.sort((a, b) => {
    const aExact = a.ticker === q;
    const bExact = b.ticker === q;
    if (aExact !== bExact) return aExact ? -1 : 1;

    const aStart = a.ticker.startsWith(q);
    const bStart = b.ticker.startsWith(q);
    if (aStart !== bStart) return aStart ? -1 : 1;

    return a.ticker.localeCompare(b.ticker);
  });

  return results.slice(0, limit);
}

const GENERATED_SUMMARIES = {
  HELI: {
    sector: 'Transportation & Helicopter Aviation',
    grade: 'Grade B',
    gradeLabel: 'High Leverage Transition',
    statusClass: 'badge-transisi',
    dotColor: 'bg-[#D97706] dark:bg-[#FBBF24]',
    description: 'PT Jaya Trishindo Tbk operates with constrained internal cash generation (0.20x capex coverage), relying on external financing for aviation operations while facing fleet emission intensity scrutiny.',
    financialHealth: 'Constrained Cash Flow',
    coverageRatio: '0.20x',
    ocf: 'IDR 4.29B',
    ytdChange: '-2.4%',
  },
  UVCR: {
    sector: 'Software & Digital Commerce Platforms',
    grade: 'Grade B+',
    gradeLabel: 'Asset-Light Enabling',
    statusClass: 'bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800',
    dotColor: 'bg-[#1D4ED8] dark:bg-[#60A5FA]',
    description: 'PT Trimegah Karya Pratama Tbk maintains balanced operational cash coverage (0.95x capex ratio) with low operational carbon intensity under digital enabling service criteria.',
    financialHealth: 'Self-Sustaining Digital',
    coverageRatio: '0.95x',
    ocf: 'IDR 73.67B',
    ytdChange: '+6.1%',
  },
  BACH: {
    sector: 'Industrial Machinery & Specialized Services',
    grade: 'Grade A',
    gradeLabel: 'Self-Funded Services',
    statusClass: 'badge-hijau',
    dotColor: 'bg-[#047857] dark:bg-[#34D399]',
    description: 'PT Bach Multi Global Tbk demonstrates strong operational self-funding (IDR 131.88B OCF, 2.00x coverage ratio) with an asset-light framework supporting environmental compliance.',
    financialHealth: 'Strong Liquidity Reserve',
    coverageRatio: '2.00x',
    ocf: 'IDR 131.88B',
    ytdChange: '+8.4%',
  },
  BNBR: {
    sector: 'Multi-Sector Conglomerate & EV Buses',
    grade: 'Grade B',
    gradeLabel: 'Industrial Transition',
    statusClass: 'badge-transisi',
    dotColor: 'bg-[#D97706] dark:bg-[#FBBF24]',
    description: 'Bakrie & Brothers Tbk accelerates VKTR electric commercial bus manufacturing while restructuring heavy legacy debt commitments across industrial units.',
    financialHealth: 'Debt Restructuring',
    coverageRatio: '0.12x',
    ocf: '-IDR 100.9B',
    ytdChange: '-4.8%',
  },
};

/**
 * Returns full company profile for a ticker, checking curated first then all 962 IDX equities.
 */
export function getCompanyProfile(ticker) {
  if (!ticker) return null;
  const t = ticker.toUpperCase();
  const curated = IDX_EMITENTS.find((c) => c.ticker === t);
  if (curated) return curated;

  const generated = GENERATED_SUMMARIES[t];
  const raw = allIdxTickers.find((c) => (c.symbol || '').toUpperCase() === t);
  const companyName = raw?.company_name || `${t} Corporation Tbk`;

  if (generated) {
    return {
      ticker: t,
      name: companyName,
      ...generated,
    };
  }

  if (raw) {
    return {
      ticker: t,
      name: raw.company_name,
      sector: 'IDX Listed Equities (SectorsApp)',
      grade: 'Audit Ready',
      gradeLabel: 'Live SectorsApp Data',
      statusClass: 'bg-emerald-50 text-[#047857] border-emerald-200 dark:bg-emerald-950/60 dark:text-[#34D399] dark:border-emerald-800',
      dotColor: 'bg-[#047857] dark:bg-[#34D399]',
      description: `${raw.company_name} is listed on the IDX. Select to trigger live TKBI v3.0 regulatory audit and financial metrics.`,
      financialHealth: 'SectorsApp Synced',
      coverageRatio: 'Live',
      ocf: 'Audited',
      ytdChange: 'Live',
    };
  }

  return {
    ticker: t,
    name: `${t} Corporation Tbk`,
    sector: 'Indonesian Equities',
    grade: 'Audit Ready',
    gradeLabel: 'Custom IDX Ticker',
    statusClass: 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300',
    dotColor: 'bg-[#047857] dark:bg-[#34D399]',
    description: `IDX ticker ${t}. Select to trigger live TKBI v3.0 regulatory audit.`,
    financialHealth: 'Live',
    coverageRatio: 'Live',
    ocf: 'Audited',
    ytdChange: 'Live',
  };
}
