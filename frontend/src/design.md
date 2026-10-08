# SustainMetric IDX — Design System: "Executive Precision"

**Metaphor**: Swiss Regulatory Terminal × High-Density Financial Ledger  
**Aesthetic Profile**: Executive Precision (Light & Dark System)  
**Target Stack**: Svelte 5 (Runes) + Tailwind CSS v4  

---

## 1. Palette Architecture: Light & Dark Token Mapping

Direct extraction from Executive Precision reference boards:

```text
ROLE         LIGHT MODE ("EXECUTIVE PRECISION")   DARK MODE ("EXECUTIVE PRECISION DARK")
────────────────────────────────────────────────────────────────────────────────────────────
Primary      #047857 (Forest Emerald)             #34D399 (Mint Emerald)
Secondary    #1D4ED8 (Royal Cobalt)               #60A5FA (Sky Cobalt)
Tertiary     #D97706 (Amber Ochre)                #FBBF24 (Warm Gold)
Neutral      #0F172A (Deep Slate)                 #0B1120 / #0F172A (Abyss Navy)
Destructive  #DC2626 (Crimson)                    #F87171 (Coral Red)
Canvas       #F8FAFC (Slate White)                #070A11 (Terminal Canvas)
Panel Surface#FFFFFF (Pure White)                 #0F172A (Dark Panel)
Input Fill   #F1F5F9 (Soft Muted)                 #162032 (Muted Ink)
Border       #E2E8F0 (Hairline Gray)              #1E293B (Hairline Slate)
```

### 1.1 Complete Color Swatch Ramp

#### Primary (Forest Emerald → Mint Emerald)
*Role: OJK Hijau, primary action buttons, verified green credentials, positive deltas.*

| Token | Light Hex | Dark Hex | Dark Role |
|---|---|---|---|
| `--color-primary` (Core) | `#047857` | `#34D399` | Button fill, active highlight, data bars |
| `--color-primary-text` | `#047857` | `#34D399` | Text indicator, status badge label |
| `--color-primary-surface` | `#ECFDF5` | `rgba(52, 211, 153, 0.12)` | Badge background, selected row tint |
| `--color-primary-border` | `#A7F3D0` | `rgba(52, 211, 153, 0.35)` | Badge border, active ring |
| `--color-primary-contrast` | `#FFFFFF` | `#064E3B` | Text on solid primary button |

#### Secondary (Royal Cobalt → Sky Cobalt)
*Role: Financial metrics, OCF/Capex ratios, peer scatter benchmark markers, outline actions.*

| Token | Light Hex | Dark Hex | Dark Role |
|---|---|---|---|
| `--color-secondary` (Core) | `#1D4ED8` | `#60A5FA` | Secondary bars, active scatter points |
| `--color-secondary-text` | `#1D4ED8` | `#60A5FA` | Financial metric labels, links |
| `--color-secondary-surface`| `#EFF6FF` | `rgba(96, 165, 250, 0.12)` | Secondary pill background |
| `--color-secondary-border` | `#BFDBFE` | `rgba(96, 165, 250, 0.35)` | Secondary border |
| `--color-secondary-contrast`|`#FFFFFF` | `#0F172A` | Text on secondary elements |

#### Tertiary (Amber Ochre → Warm Gold)
*Role: OJK Transisi, caution alerts, divergence warnings, edit triggers.*

| Token | Light Hex | Dark Hex | Dark Role |
|---|---|---|---|
| `--color-tertiary` (Core) | `#D97706` | `#FBBF24` | Transition indicator, warning bar |
| `--color-tertiary-text` | `#D97706` | `#FBBF24` | Transition badge label |
| `--color-tertiary-surface` | `#FFFBEB` | `rgba(251, 191, 36, 0.12)` | Transition badge background |
| `--color-tertiary-border` | `#FDE68A` | `rgba(251, 191, 36, 0.35)` | Transition badge border |
| `--color-tertiary-contrast`|`#FFFFFF` | `#0F172A` | Text on tertiary elements |

#### Neutral (Deep Slate → Abyss Navy & Slate)
*Role: Structural scaffolding, typography contrast, hairline borders, terminal backdrops.*

| Token | Light Hex | Dark Hex | Usage |
|---|---|---|---|
| `--color-canvas` | `#F8FAFC` | `#070A11` | Root page background |
| `--color-surface` | `#FFFFFF` | `#0F172A` | Main cards, tables, panels |
| `--color-surface-subtle` | `#F1F5F9` | `#162032` | Header strips, input fields |
| `--color-border-hairline`| `#E2E8F0` | `#1E293B` | 1px grid dividing lines |
| `--color-text-title` | `#0F172A` | `#F8FAFC` | Hanken Grotesk headings |
| `--color-text-body` | `#334155` | `#CBD5E1` | Inter narrative body text |
| `--color-text-muted` | `#64748B` | `#94A3B8` | JetBrains Mono table headers & sublabels |

#### Destructive (Crimson → Coral Red)
*Role: OJK Tidak Memenuhi, high risk warnings, anomalies.*

| Token | Light Hex | Dark Hex | Dark Role |
|---|---|---|---|
| `--color-destructive` (Core)| `#DC2626` | `#F87171` | Delete button, critical indicator |
| `--color-destructive-text` | `#B91C1C` | `#F87171` | Excluded status label |
| `--color-destructive-surface`|`#FEF2F2`| `rgba(248, 113, 113, 0.12)`| Non-compliant badge bg |
| `--color-destructive-border` |`#FECACA`| `rgba(248, 113, 113, 0.35)`| Non-compliant badge border |

---

## 2. Typography Spec (Executive Precision Trio)

Strict three-tiered typographic hierarchy mapping semantic intent to font anatomy:

| Role | Font Family | Weights | Letter Spacing | Purpose & Usage |
|---|---|---|---|---|
| **Headline** | `Hanken Grotesk`, sans-serif | 600, 700, 800 | `-0.025em` (tight) | Emitent names, view titles, primary score KPIs, hero banners |
| **Body** | `Inter`, sans-serif | 400, 500, 600 | `-0.011em` | Executive summaries, audit notes, AI explanations, tooltips |
| **Label / Data**| `JetBrains Mono`, monospace | 400, 500, 600 | `+0.02em` (`tabular-nums`) | TSC IDs, financial ratios, coordinates, status badges, timestamps |

### Google Fonts Import
```css
@import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
```

---

## 3. Component Kit Guidelines (Executive Precision & Dark)

### 3.1 Button Variants

1. **Primary**:
   - Light: `bg-[#047857] text-white hover:bg-[#065F46] border border-[#047857]`
   - Dark: `bg-[#34D399] text-[#064E3B] hover:bg-[#10B981] font-semibold border border-[#34D399]`
2. **Secondary**:
   - Light: `bg-[#F1F5F9] text-[#1E293B] hover:bg-[#E2E8F0] border border-[#E2E8F0]`
   - Dark: `bg-[#162032] text-[#CBD5E1] hover:bg-[#1E293B] border border-[#1E293B]`
3. **Inverted**:
   - Light: `bg-[#0F172A] text-white hover:bg-[#1E293B] border border-[#0F172A]`
   - Dark: `bg-[#F1F5F9] text-[#0F172A] hover:bg-white font-semibold border border-[#E2E8F0]`
4. **Outlined**:
   - Light: `bg-transparent text-[#0F172A] border border-[#CBD5E1] hover:bg-slate-100`
   - Dark: `bg-transparent text-[#F8FAFC] border border-[#334155] hover:bg-[#162032]`

### 3.2 Search & Inputs
- Light: `bg-[#FFFFFF] border border-[#E2E8F0] text-[#0F172A] placeholder:text-[#94A3B8]`
- Dark: `bg-[#162032] border border-[#1E293B] text-[#F8FAFC] placeholder:text-[#64748B]`
- Radius: `rounded-[3px]` or `rounded-none`, strict `shadow-none`.

### 3.3 Metric Progress Bars
- Height: `h-1.5` with track `bg-[#E2E8F0]` (light) / `bg-[#1E293B]` (dark).
- Fills:
  - Green / Alignment: `#047857` (light) / `#34D399` (dark)
  - Blue / Financial Health: `#1D4ED8` (light) / `#60A5FA` (dark)
  - Amber / Transition: `#D97706` (light) / `#FBBF24` (dark)

### 3.4 Regulatory Status Badges (OJK TKBI)
- Standard: `px-2 py-0.5 font-mono text-[11px] font-medium tracking-wide uppercase rounded-[2px] border`
- **HIJAU**:
  - Light: `bg-[#ECFDF5] text-[#047857] border-[#A7F3D0]`
  - Dark: `bg-[rgba(52,211,153,0.12)] text-[#34D399] border-[rgba(52,211,153,0.35)]`
- **TRANSISI**:
  - Light: `bg-[#FFFBEB] text-[#D97706] border-[#FDE68A]`
  - Dark: `bg-[rgba(251,191,36,0.12)] text-[#FBBF24] border-[rgba(251,191,36,0.35)]`
- **TIDAK MEMENUHI**:
  - Light: `bg-[#FEF2F2] text-[#DC2626] border-[#FECACA]`
  - Dark: `bg-[rgba(248,113,113,0.12)] text-[#F87171] border-[rgba(248,113,113,0.35)]`

---

## 4. Screen Blueprints (Terminal Execution)

### 4.1 Live Emitent Dashboard
```text
+------------------------------------------------------------------------------------------------------------------------+
| [TICKER WATCHER TAPE] PGEO: 88.5% [HIJAU] | ADRO: 42.1% [TRANSISI] | BBRI: 78.4% [HIJAU] | BREN: 91.0% | + ADD TICKER  |
+------------------------------------------------------------------------------------------------------------------------+
| [EMITENT BANNER] Hanken Grotesk Bold                                                                                   |
| PGEO:IJ  Pertamina Geothermal Energy Tbk       [SEKTOR: Utilities / Geothermal]       [RUN AUDIT] [EXPORT XLSX] [PDF]   |
+-------------------------------------+------------------------------------+---------------------------------------------+
| 1. TKBI CONSISTENCY (Primary)       | 2. VIABILITY SCORE (Secondary)     | 3. CAPEX COVERAGE (Ratio)                   |
|    88.5 / 100 [Hanken Grotesk]      |    74.2 / 100 [Hanken Grotesk]     |    2.41x (Self-Funded Transition)           |
|    ====[#047857 / #34D399]====      |    ====[#1D4ED8 / #60A5FA]====     |    ====[#047857 / #34D399]====              |
|    JetBrains Mono: +4.2% YoY        |    JetBrains Mono: OCF IDR 3.42T   |    JetBrains Mono: Capex IDR 1.42T          |
+-------------------------------------+------------------------------------+---------------------------------------------+
| 2x2 DIVERGENCE RADAR                | FINANCIAL HEALTH & CASH LEDGER     | REGULATORY AUDIT FINDINGS (OJK)             |
|                                     |                                    |                                             |
|  Y: TKBI Alignment                  | OCF (Cash from Ops): IDR 3,420.00 B| [HIJAU] Zero direct coal exposure (TSC-E01) |
|  100 | Q2 SPEKULATIF | Q1 TANGGUH   | Green CAPEX Budget : IDR 1,418.50 B| [HIJAU] Steam efficiency >85% (TSC-E02)     |
|      |               |   * PGEO     | Free Cash Cushion  : IDR 2,001.50 B| [TRANSISI] Scope 3 inventory partial        |
|   50 +---------------+------------+ | RoA Standard       : 7.82%         |            disclosure in Progress (TSC-E03) |
|      | Q4 RENTAN     | Q3 KONVENS   | Debt-to-Equity     : 0.44x         | [ACTION] 2 criteria pending auditor sign-off|
|    0 +---------------+------------+ |                                    |                                             |
|      0              50         100  |                                    |                                             |
|        X: Financial Viability       |                                    |                                             |
+-------------------------------------+------------------------------------+---------------------------------------------+
```

### 4.2 12-Column TKBI Audit Grid
```text
+------+-----------+---------+--------------------+---------------+---------+----------+----------+----------+---------+----------+--------+
| #    | SEKTOR    | TSC-ID  | KRITERIA UTAMA     | AMBANG BATAS  | METRIK  | BUKTI    | AI STATUS| HIT REV  | AUDITOR | LOG TIME | ACTION |
+------+-----------+---------+--------------------+---------------+---------+----------+----------+----------+---------+----------+--------+
| 001  | Utilities | TSC-E01 | Direct Emisi CO2eq | <100 gCO2/kWh | 38.4    | AR24 p.88| [HIJAU]  | [HIJAU]  | ADM_SYS | 09:22:10 | [EDIT] |
| 002  | Utilities | TSC-E02 | Water Reinjection  | >=95% Return  | 98.2%   | SR24 p.42| [HIJAU]  | [HIJAU]  | ADM_SYS | 09:22:11 | [EDIT] |
| 003  | Utilities | TSC-E03 | Scope 3 Disclosed  | Full Category | Partial | SR24 p.51| [TRANSI] | [TRANSI] | AUDITOR1| 10:14:02 | [EDIT] |
| 004  | Utilities | TSC-G01 | Biodiversity Mgmt  | IUCN Redlist  | None    | AR24 p.94| [TIDAK]  | [TRANSI] | AUDITOR1| 10:15:33 | [SAVED]|
+------+-----------+---------+--------------------+---------------+---------+----------+----------+----------+---------+----------+--------+
```

---

## 5. Anti-Slop Audit Checklist (Executive Precision Standard)

- [ ] **Type Spec Compliance**: Headlines use `Hanken Grotesk`, body uses `Inter`, all numbers/badges/tables use `JetBrains Mono`.
- [ ] **Palette Strictness**:
  - Primary `#047857` (light) / `#34D399` (dark)
  - Secondary `#1D4ED8` (light) / `#60A5FA` (dark)
  - Tertiary `#D97706` (light) / `#FBBF24` (dark)
  - Neutral `#0F172A` (light) / `#0B1120` & `#0F172A` (dark)
  - Destructive `#DC2626` (light) / `#F87171` (dark)
- [ ] **Zero Pill Cards & Zero Drop Shadows**: Panels use `rounded-none` or `rounded-[3px]`, hairline 1px borders, `shadow-none`.
- [ ] **Dark Mode Canvas Contrast**: Canvas `#070A11`, panel `#0F172A`, input `#162032`, hairline `#1E293B`.
- [ ] **Tabular Figures**: Every numeric comparison and currency value uses `tabular-nums font-mono text-right`.
