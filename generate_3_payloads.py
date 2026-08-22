import json
import os
import re
from parsers import ExamParserFactory, GabaritoExtractor

def generate_payloads():
    os.makedirs("output", exist_ok=True)

    # ----------------------------------------------------
    # 1. UNESULBAHIA / CONSULTEC Medicina 2021.2
    # ----------------------------------------------------
    pdf_unesul = r"C:\Users\jao_v\Downloads\unesulbahia202121-omline-medicina-01082021.pdf"
    if os.path.exists(pdf_unesul):
        print("Parsing UNESULBAHIA / CONSULTEC Medicina 2021.2...")
        meta1 = {
            "banca": "CONSULTEC",
            "orgao": "UNESULBAHIA",
            "cargo": "Medicina",
            "ano": 2021,
            "fonte": "VESTIBULAR"
        }
        parser1 = ExamParserFactory.get_parser("CONSULTEC", meta1)
        questoes1 = parser1.parse_pdf(pdf_unesul)
        
        out1 = os.path.join("output", "payload_consultec_unesulbahia_2021.json")
        with open(out1, "w", encoding="utf-8") as f:
            json.dump(questoes1, f, ensure_ascii=False, indent=2)
        print(f"Salvo {len(questoes1)} questoes em {out1}")
    else:
        print(f"Arquivo {pdf_unesul} nao encontrado.")

    # ----------------------------------------------------
    # 2. UESB 2020 (AIETEC / CONSULTEC)
    # ----------------------------------------------------
    pdf_uesb = r"C:\Users\jao_v\Downloads\uesb2020_cad1_modelo1.pdf"
    if os.path.exists(pdf_uesb):
        print("\nParsing UESB 2020 (AIETEC / CONSULTEC)...")
        meta2 = {
            "banca": "CONSULTEC",
            "orgao": "UESB",
            "cargo": "Vestibular 2020 - Caderno 1",
            "ano": 2020,
            "fonte": "VESTIBULAR"
        }
        parser2 = ExamParserFactory.get_parser("CONSULTEC", meta2)
        questoes2 = parser2.parse_pdf(pdf_uesb)
        
        out2 = os.path.join("output", "payload_consultec_uesb_2020.json")
        with open(out2, "w", encoding="utf-8") as f:
            json.dump(questoes2, f, ensure_ascii=False, indent=2)
        print(f"Salvo {len(questoes2)} questoes em {out2}")
    else:
        print(f"Arquivo {pdf_uesb} nao encontrado.")

    # ----------------------------------------------------
    # 3. UNDB 2024.1 (AIETEC / CONSULTEC)
    # ----------------------------------------------------
    pdf_undb = r"C:\Users\jao_v\Downloads\2023.11.28-10.45.5353undb20241-med-final_ING_COM_GABARITO.pdf"
    if os.path.exists(pdf_undb):
        print("\nParsing UNDB Medicina 2024.1 (AIETEC / CONSULTEC)...")
        meta3 = {
            "banca": "CONSULTEC",
            "orgao": "Centro Universitário UNDB",
            "cargo": "Medicina 2024.1",
            "ano": 2024,
            "fonte": "VESTIBULAR"
        }
        parser3 = ExamParserFactory.get_parser("CONSULTEC", meta3)
        questoes3 = parser3.parse_pdf(pdf_undb)
        
        out3 = os.path.join("output", "payload_consultec_undb_2024.json")
        with open(out3, "w", encoding="utf-8") as f:
            json.dump(questoes3, f, ensure_ascii=False, indent=2)
        print(f"Salvo {len(questoes3)} questoes em {out3}")
    else:
        print(f"Arquivo {pdf_undb} nao encontrado.")

generate_payloads()

