"""OJK TKBI 2024/2026 Sector-Agnostic Decision Tree (SDT) Catalog for UMKM.

Governed by Peraturan Pemerintah Nomor 7 Tahun 2021 tentang Kemudahan, Pelindungan,
dan Pemberdayaan Koperasi dan Usaha Mikro, Kecil, dan Menengah.
Enables principle-based green assessment for MSMEs without burdensome heavy technical screening.
"""

from typing import Any

SDT_UMKM_CRITERIA: dict[str, dict[str, Any]] = {
    "EO1": {
        "code": "SDT-EO1",
        "name": "Mitigasi Perubahan Iklim (Climate Change Mitigation)",
        "description": "Upaya penurunan emisi gas rumah kaca dan transisi efisiensi energi operasional UMKM.",
        "questions": [
            {
                "id": "SDT-EO1-Q1",
                "question": "Apakah usaha menerapkan langkah efisiensi energi terukur (e.g. penggunaan lampu LED, inverter hemat energi, atau pemeliharaan mesin berkala)?",
                "guidance": "Bukti sederhana: Tagihan listrik bulanan yang stabil/menurun atau SOP hemat energi.",
                "type": "boolean",
                "threshold_score": 10,
            },
            {
                "id": "SDT-EO1-Q2",
                "question": "Apakah usaha memanfaatkan sumber energi terbarukan lokal (e.g. solar rooftop skala kecil, biomassa limbah pertanian, atau biogas)?",
                "guidance": "Bukti: Dokumentasi fisik instalasi atau sertifikat instalatur terdaftar.",
                "type": "boolean",
                "threshold_score": 20,
            },
            {
                "id": "SDT-EO1-Q3",
                "question": "Apakah usaha secara bertahap beralih dari bahan bakar fosil tinggi (batu bara / solar subsidi tanpa filter) ke alternatif rendah emisi?",
                "guidance": "Target transisi dalam rentang 1-3 tahun kalender.",
                "type": "boolean",
                "threshold_score": 15,
            },
        ],
    },
    "EO2": {
        "code": "SDT-EO2",
        "name": "Adaptasi Perubahan Iklim (Climate Change Adaptation)",
        "description": "Peningkatan ketahanan terhadap bencana hidrometeorologi (banjir, kekeringan, kenaikan muka laut).",
        "questions": [
            {
                "id": "SDT-EO2-Q1",
                "question": "Apakah lokasi usaha memiliki langkah perlindungan fisik dari risiko banjir, rob, atau tanah longsor?",
                "guidance": "Peninggian lantai, sumur resapan, drainase lancar, atau penghijauan penahan erosi.",
                "type": "boolean",
                "threshold_score": 15,
            },
            {
                "id": "SDT-EO2-Q2",
                "question": "Apakah usaha memiliki rencana kelangsungan usaha (business continuity) sederhana jika terjadi cuaca ekstrem?",
                "guidance": "Cadangan stok aman, alternatif pasokan bahan baku, atau polis asuransi mikro bencana.",
                "type": "boolean",
                "threshold_score": 15,
            },
        ],
    },
    "EO3": {
        "code": "SDT-EO3",
        "name": "Perlindungan Ekosistem dan Keanekaragaman Hayati",
        "description": "Menghindari degradasi habitat alami, kawasan lindung, dan kelestarian tanah/air.",
        "questions": [
            {
                "id": "SDT-EO3-Q1",
                "question": "Apakah operasional usaha berlokasi di luar kawasan hutan lindung, suaka alam, atau sempadan sungai?",
                "guidance": "Kesesuaian Tata Ruang (KKPR) atau surat keterangan domisili usaha dari kelurahan/desa.",
                "type": "boolean",
                "threshold_score": 20,
            },
            {
                "id": "SDT-EO3-Q2",
                "question": "Apakah bahan baku nabati/hewani tidak berasal dari perburuan liar atau deforestasi ilegal?",
                "guidance": "Sertifikat asal usul kayu (SVLK), sertifikasi organik, atau surat pernyataan komitmen non-deforestasi.",
                "type": "boolean",
                "threshold_score": 20,
            },
        ],
    },
    "EO4": {
        "code": "SDT-EO4",
        "name": "Ketahanan Sumber Daya & Ekonomi Sirkular",
        "description": "Pengurangan limbah, daur ulang material, dan efisiensi pemakaian air bersih.",
        "questions": [
            {
                "id": "SDT-EO4-Q1",
                "question": "Apakah usaha memilah sampah/limbah produksi dan menyalurkannya ke bank sampah atau mitra daur ulang?",
                "guidance": "Pemisahan sampah organik, anorganik, dan residu produksi.",
                "type": "boolean",
                "threshold_score": 15,
            },
            {
                "id": "SDT-EO4-Q2",
                "question": "Apakah kemasan produk menggunakan material ramah lingkungan atau dapat digunakan ulang (reusable)?",
                "guidance": "Kemasan kertas daur ulang, bio-plastik pati singkong, atau skema pengembalian kemasan (refill).",
                "type": "boolean",
                "threshold_score": 15,
            },
        ],
    },
}

SDT_DNSH_QUESTIONS = [
    {
        "id": "SDT-DNSH-1",
        "criterion": "Pencegahan Pencemaran Air & Tanah",
        "question": "Apakah limbah cair sisa proses produksi tidak langsung dibuang ke saluran air umum/sungai tanpa pengendapan atau penyaringan?",
        "required_answer": True,
    },
    {
        "id": "SDT-DNSH-2",
        "criterion": "Pengelolaan B3 Skala Kecil",
        "question": "Jika menggunakan bahan berbahaya/beracun (e.g. oli bekas, pelarut, pestisida), apakah disimpan dalam wadah tertutup aman?",
        "required_answer": True,
    },
]

SDT_SOCIAL_ASPECTS_QUESTIONS = [
    {
        "id": "SDT-SA-1",
        "criterion": "Keselamatan & Kesehatan Kerja (K3 Sederhana)",
        "question": "Apakah pekerja dibekali alat pelindung diri (APD) yang memadai sesuai risiko pekerjaan (e.g. sarung tangan, masker, sepatu)?",
        "required_answer": True,
    },
    {
        "id": "SDT-SA-2",
        "criterion": "Pencegahan Pekerja Anak & Hak Pekerja",
        "question": "Apakah usaha bebas dari mempekerjakan anak di bawah umur yang mengganggu pendidikan dan memastikan pembayaran upah yang disepakati secara adil?",
        "required_answer": True,
    },
]


def evaluate_sdt_submission(
    primary_eo: str,
    eo_answers: dict[str, bool],
    dnsh_answers: dict[str, bool],
    social_answers: dict[str, bool],
    has_rmt_commitment: bool = False,
) -> dict[str, Any]:
    """Evaluate SDT submission for UMKM following OJK principle-based framework."""
    eo_config = SDT_UMKM_CRITERIA.get(primary_eo, SDT_UMKM_CRITERIA["EO1"])
    questions = eo_config["questions"]

    # 1. Primary EO Score
    total_score = 0
    max_score = sum(q["threshold_score"] for q in questions)
    for q in questions:
        if eo_answers.get(q["id"], False):
            total_score += q["threshold_score"]

    score_pct = (total_score / max_score) * 100 if max_score > 0 else 0

    # 2. DNSH Gate
    dnsh_passed = all(dnsh_answers.get(q["id"], False) for q in SDT_DNSH_QUESTIONS)

    # 3. Social Aspects Gate
    social_passed = all(social_answers.get(q["id"], False) for q in SDT_SOCIAL_ASPECTS_QUESTIONS)

    # 4. Classification determination
    if not social_passed:
        classification = "TIDAK MEMENUHI KLASIFIKASI"
        notes = "Gagal memenuhi Essential Criteria Aspek Sosial (hak dasar tenaga kerja & keselamatan kerja)."
    elif dnsh_passed and score_pct >= 70:
        classification = "HIJAU"
        notes = f"Memenuhi ambang batas utama {eo_config['name']} ({score_pct:.0f}%) serta seluruh prinsip DNSH dan Aspek Sosial."
    elif dnsh_passed and score_pct >= 40:
        classification = "TRANSISI"
        notes = f"Memenuhi kriteria transisi {eo_config['name']} ({score_pct:.0f}%) dengan kepatuhan penuh DNSH & Aspek Sosial."
    elif not dnsh_passed and has_rmt_commitment and score_pct >= 40:
        classification = "TRANSISI INTERIM"
        notes = "Terdapat isu DNSH namun didukung komitmen Remedial Measures to Transition (RMT) maksimal 3 tahun."
    else:
        classification = "TIDAK MEMENUHI KLASIFIKASI"
        notes = f"Skor pemenuhan ({score_pct:.0f}%) belum mencapai batas minimum atau melanggar prinsip DNSH tanpa rencana RMT terikat."

    return {
        "primary_eo": primary_eo,
        "eo_name": eo_config["name"],
        "eo_score_pct": round(score_pct, 1),
        "dnsh_passed": dnsh_passed,
        "social_passed": social_passed,
        "has_rmt_commitment": has_rmt_commitment,
        "classification": classification,
        "notes": notes,
    }
