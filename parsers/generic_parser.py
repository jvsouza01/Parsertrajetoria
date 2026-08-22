import re
import pypdf
from parsers.base_parser import BaseExamParser

class GenericExamParser(BaseExamParser):
    """
    Parser adaptativo universal para qualquer banca ou formato não catalogado (FGV, VUNESP, ENEM, etc).
    Testa dinamicamente múltiplos padrões de numeração e múltiplos estilos de alternativas.
    """

    def parse_pdf(self, pdf_path_or_stream, gabarito_map=None, disciplina_map=None):
        gabarito_map = gabarito_map or {}
        disciplina_map = disciplina_map or {}

        reader = pypdf.PdfReader(pdf_path_or_stream)
        raw_text_by_page = [p.extract_text() or "" for p in reader.pages]
        full_text = self.clean_text("\n".join(raw_text_by_page))

        # Tenta múltiplos padrões de início de questão
        patterns = [
            # Padrão 1: "Questão 01", "QUESTÃO 1"
            (r'(?:\n|^)\s*QUEST[ÃA]O\s+0*(\d{1,3})\b', False),
            # Padrão 2: "1. ", "01. "
            (r'(?:\n|^)\s*0*(\d{1,3})\.\s+(?=[A-ZÀ-ÿ\-\"\'\(\“\”\‘\’«»•])', True),
            # Padrão 3: "1) ", "01) "
            (r'(?:\n|^)\s*0*(\d{1,3})\)\s+(?=[A-ZÀ-ÿ\-\"\'\(\“\”\‘\’«»•])', True),
            # Padrão 4: "1 - ", "01 - "
            (r'(?:\n|^)\s*0*(\d{1,3})\s*-\s+(?=[A-ZÀ-ÿ\-\"\'\(\“\”\‘\’«»•])', True)
        ]

        best_splits = []
        for pat, require_alts in patterns:
            candidate_splits = list(re.finditer(pat, full_text, re.IGNORECASE))
            if len(candidate_splits) >= 5:
                # Valida se as questões possuem alternativas ou conteúdo substancial
                valid = []
                for i, match in enumerate(candidate_splits):
                    start_pos = match.end()
                    end_pos = candidate_splits[i+1].start() if i + 1 < len(candidate_splits) else len(full_text)
                    chunk = full_text[start_pos:end_pos]
                    if not require_alts or re.search(r'(?:\n|^|\s)(?:\([A-Ea-e]\)|[A-Ea-e]\))\s+', chunk):
                        valid.append((int(match.group(1)), match.start(), match.end()))
                
                if len(valid) > len(best_splits):
                    best_splits = valid

        if not best_splits:
            # Fallback extremo: divide por páginas se não encontrar números
            return []

        questoes = []
        current_materia = None

        for i, (q_num, match_start, match_end) in enumerate(best_splits):
            chunk_end = best_splits[i+1][1] if i + 1 < len(best_splits) else len(full_text)
            chunk = full_text[match_end:chunk_end].strip()

            if q_num in disciplina_map:
                current_materia = disciplina_map[q_num]

            # Anti-leakage / Detecção de língua estrangeira no bloco da questão
            bloco_texto = f" {chunk} ".lower()
            english_markers = [" the ", " and ", " of ", " to ", " in ", " with ", " which ", " according to ", " is "]
            spanish_markers = [" el ", " la ", " los ", " las ", " de ", " en ", " y ", " que ", " por ", " según "]
            
            eng_hits = sum(1 for m in english_markers if m in bloco_texto)
            spa_hits = sum(1 for m in spanish_markers if m in bloco_texto)
            
            materia_questao = current_materia
            if eng_hits >= 3:
                materia_questao = "Inglês"
            elif spa_hits >= 3:
                materia_questao = "Espanhol"

            # Detecta gabarito embutido
            gab_embedded = None
            is_anulada = False
            m_gab = re.search(r'\((?:Correta|Gabarito):\s*([A-Ea-eXxTtNn\*])\)', chunk, re.IGNORECASE)
            if m_gab:
                gab_embedded = m_gab.group(1).upper()
                chunk = re.sub(r'\((?:Correta|Gabarito):\s*[A-Ea-eXxTtNn\*]\)', '', chunk).strip()

            final_gab = gab_embedded or str(gabarito_map.get(q_num, "")).upper()
            if final_gab in ["*", "X", "T", "ANULADA"]:
                is_anulada = True

            # Tenta encontrar alternativas em múltiplos formatos: (A) ou a) ou A) ou A -
            alt_patterns = [
                r'(?:\n|^|\s)\(([A-Ea-e])\)\s+',
                r'(?:\n|^|\s)([A-Ea-e])\)\s+',
                r'(?:\n|^|\s)([A-Ea-e])\s*-\s+'
            ]

            alternativas = []
            enunciado = chunk

            for alt_pat in alt_patterns:
                alt_matches = list(re.finditer(alt_pat, chunk))
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
                            "correta": False if is_anulada else (letra == final_gab)
                        })
                    break

            questoes.append({
                "posicao": q_num,
                "materia": materia_questao,
                "textoBase": None,
                "enunciado": enunciado,
                "gabaritoOficial": final_gab,
                "anulada": is_anulada,
                "alternativas": alternativas
            })

        return self.format_to_payload(questoes)
