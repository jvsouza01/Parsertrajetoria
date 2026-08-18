import re
import pypdf
from parsers.base_parser import BaseExamParser

class CebraspeParser(BaseExamParser):
    """Parser especializado para a banca CEBRASPE / CESPE (estilo Certo/Errado ou múltipla escolha)."""

    def parse_pdf(self, pdf_path_or_stream, gabarito_map=None, disciplina_map=None):
        gabarito_map = gabarito_map or {}
        disciplina_map = disciplina_map or {}

        reader = pypdf.PdfReader(pdf_path_or_stream)
        raw_text_by_page = [p.extract_text() or "" for p in reader.pages]
        full_text = self.clean_text("\n".join(raw_text_by_page))

        # Detecta itens numerados: "101 ", "102 ", "1 ", "2 "
        # No Cebraspe, cada número é um item assertivo (Certo ou Errado) ou múltipla escolha (A-E)
        candidate_splits = list(re.finditer(r'(?:\n|^)\s*(\d{1,3})\s+(?=[A-ZÀ-ÿ\-\"\'\(\“\”\‘\’«»])', full_text))

        valid_splits = []
        for i, match in enumerate(candidate_splits):
            valid_splits.append((int(match.group(1)), match.start(), match.end()))

        questoes = []
        current_materia = "Conhecimentos Gerais"

        for i, (q_num, match_start, match_end) in enumerate(valid_splits):
            chunk_end = valid_splits[i+1][1] if i + 1 < len(valid_splits) else len(full_text)
            chunk = full_text[match_end:chunk_end].strip()

            if q_num in disciplina_map:
                current_materia = disciplina_map[q_num]

            # Checa se é múltipla escolha (A, B, C, D, E) ou Certo/Errado (C/E)
            alt_matches = list(re.finditer(r'(?:\n|^|\s)\(([A-Ea-e])\)\s+', chunk))
            alternativas = []

            gab_val = str(gabarito_map.get(q_num, "")).upper()
            is_anulada = gab_val in ["*", "X", "T", "ANULADA"]

            if len(alt_matches) >= 2:
                enunciado = chunk[:alt_matches[0].start()].strip()
                for j, alt_m in enumerate(alt_matches):
                    letra = alt_m.group(1).upper()
                    alt_start = alt_m.end()
                    alt_end = alt_matches[j+1].start() if j + 1 < len(alt_matches) else len(chunk)
                    alt_texto = chunk[alt_start:alt_end].strip()
                    alternativas.append({
                        "letra": letra,
                        "texto": alt_texto,
                        "correta": False if is_anulada else (letra == gab_val)
                    })
            else:
                # Formato Certo / Errado padrão Cebraspe
                enunciado = chunk
                alternativas = [
                    {"letra": "C", "texto": "Certo", "correta": False if is_anulada else (gab_val == "C")},
                    {"letra": "E", "texto": "Errado", "correta": False if is_anulada else (gab_val == "E")}
                ]

            questoes.append({
                "posicao": q_num,
                "materia": current_materia,
                "textoBase": "",
                "enunciado": enunciado,
                "gabaritoOficial": gab_val,
                "anulada": is_anulada,
                "alternativas": alternativas
            })

        return self.format_to_payload(questoes)
