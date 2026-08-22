import re
import pypdf
from parsers.base_parser import BaseExamParser

class FGVParser(BaseExamParser):
    """
    Parser especializado para provas da Fundação Getulio Vargas (FGV).
    Padrão:
    - Questão 01 ou 1 (isolado no início de linha)
    - Alternativas: (A), (B), (C), (D), (E) ou A, B, C, D, E seguidos de texto.
    """

    def parse_pdf(self, pdf_path_or_stream, gabarito_map=None, disciplina_map=None):
        gabarito_map = gabarito_map or {}
        disciplina_map = disciplina_map or {}

        reader = pypdf.PdfReader(pdf_path_or_stream)
        pages_text = [p.extract_text() or "" for p in reader.pages]
        full_text = "\n".join(pages_text)
        full_text = self.clean_text(full_text)

        # Remove cabeçalhos e rodapés comuns FGV
        full_text = re.sub(r'FGV\s+CONHECIMENTO[^\n]*', '', full_text, flags=re.IGNORECASE)
        full_text = re.sub(r'TIPO\s+\d+\s+[\-\–]\s+COR[^\n]*', '', full_text, flags=re.IGNORECASE)

        # Localização de questões
        splits = list(re.finditer(r'(?:^|\n)\s*(?:QUEST[ÃA]O\s+)?0*(\d{1,3})\s*(?:\n|[\.\-\:]\s+)', full_text, re.IGNORECASE))
        valid_splits = []
        for match in splits:
            num = int(match.group(1))
            valid_splits.append((num, match.start(), match.end()))

        questoes = []
        current_materia = "Conhecimentos Gerais"

        for i, (q_num, match_start, match_end) in enumerate(valid_splits):
            chunk_end = valid_splits[i+1][1] if i + 1 < len(valid_splits) else len(full_text)
            chunk = full_text[match_end:chunk_end].strip()

            if q_num in disciplina_map:
                current_materia = disciplina_map[q_num]

            final_gab = str(gabarito_map.get(q_num, "")).strip().upper()
            is_anulada = (final_gab in ["*", "X", "T", "ANULADA"])

            # Alternativas (A), (B), (C), (D), (E) ou A), B), C), D), E)
            alt_matches = list(re.finditer(r'(?:^|\n|\s)(?:\(?([A-Ea-e])\)|([A-Ea-e])\))\s+', chunk))
            alternativas = []

            if len(alt_matches) >= 2:
                enunciado = chunk[:alt_matches[0].start()].strip()
                for j, alt_m in enumerate(alt_matches):
                    letra = (alt_m.group(1) or alt_m.group(2)).upper()
                    alt_start = alt_m.end()
                    alt_end = alt_matches[j+1].start() if j + 1 < len(alt_matches) else len(chunk)
                    alt_texto = chunk[alt_start:alt_end].strip()

                    alternativas.append({
                        "letra": letra,
                        "texto": alt_texto,
                        "correta": False if is_anulada else (letra == final_gab)
                    })
            else:
                enunciado = chunk

            questoes.append({
                "posicao": q_num,
                "materia": current_materia,
                "enunciado": enunciado,
                "gabaritoOficial": final_gab,
                "anulada": is_anulada,
                "alternativas": alternativas
            })

        return self.format_to_payload(questoes)
