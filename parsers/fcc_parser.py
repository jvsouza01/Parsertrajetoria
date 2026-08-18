import re
import pypdf
from parsers.base_parser import BaseExamParser

class FCCParser(BaseExamParser):
    """Parser especializado para a banca Fundação Carlos Chagas (FCC)."""

    def parse_pdf(self, pdf_path_or_stream, gabarito_map=None, disciplina_map=None):
        gabarito_map = gabarito_map or {}
        disciplina_map = disciplina_map or {}
        
        reader = pypdf.PdfReader(pdf_path_or_stream)
        raw_text_by_page = []
        for page in reader.pages:
            t = page.extract_text() or ""
            raw_text_by_page.append(t)

        full_text = "\n".join(raw_text_by_page)
        full_text = self.clean_text(full_text)

        # Remove rodapés e cabeçalhos FCC
        full_text = re.sub(r'Caderno de Prova[^\n]+', '', full_text)
        full_text = re.sub(r'\d+\s+GOVBA[^\n]+', '', full_text)
        full_text = re.sub(r'GOVBA[^\n]+\d+', '', full_text)

        # Mapeamento de textos-base ("Atenção: Para responder às questões de números X a Y...")
        textos_base_map = {}
        tb_patterns = [
            r'Atenção:\s*Para responder às questões de números?\s*(\d{1,3})\s*(?:a|e)\s*(\d{1,3})[^\n]*\n(.*?)(?=\n\s*\d{1,3}\.\s+[A-ZÀ-ÿ\-\"\'\(]|\Z)',
            r'Para responder às questões de números?\s*(\d{1,3})\s*(?:a|e)\s*(\d{1,3})[^\n]*\n(.*?)(?=\n\s*\d{1,3}\.\s+[A-ZÀ-ÿ\-\"\'\(]|\Z)'
        ]
        for pat in tb_patterns:
            for m in re.finditer(pat, full_text, re.DOTALL | re.IGNORECASE):
                q_start = int(m.group(1))
                q_end = int(m.group(2))
                tb_content = m.group(3).strip()
                for q_num in range(q_start, q_end + 1):
                    textos_base_map[q_num] = tb_content

        disciplines_keywords = [
            "Língua Portuguesa", "Raciocínio Lógico-Matemático", "Raciocínio Lógico",
            "Matemática", "História do Brasil", "Geografia do Brasil", "Atualidades",
            "Noções de Direito Constitucional", "Noções de Direitos Humanos",
            "Noções de Direito Administrativo", "Noções de Direito Penal",
            "Noções de Igualdade Racial e de Gênero", "Noções de Direito Penal Militar",
            "Informática", "Direito Constitucional", "Direito Administrativo",
            "Direito Penal", "Direito Processual Penal", "Direito Civil"
        ]

        # Busca questões reais da FCC que possuem numeração e alternativas (A) ... (B) ...
        # Padrão: "\n 1. " até a próxima questão
        candidate_splits = list(re.finditer(r'(?:\n|^)\s*(\d{1,3})\.\s+(?=[A-ZÀ-ÿ\-\"\'\(•])', full_text))
        
        valid_splits = []
        for i, match in enumerate(candidate_splits):
            start_pos = match.end()
            end_pos = candidate_splits[i+1].start() if i + 1 < len(candidate_splits) else len(full_text)
            chunk = full_text[start_pos:end_pos]
            
            # Só é uma questão real se contiver alternativas (A) e (B) ou se estiver na sequência
            has_alts = bool(re.search(r'\([A-E]\)', chunk))
            if has_alts:
                valid_splits.append((int(match.group(1)), match.start(), match.end()))

        questoes = []
        current_materia = "Língua Portuguesa"

        for i, (q_num, match_start, match_end) in enumerate(valid_splits):
            chunk_end = valid_splits[i+1][1] if i + 1 < len(valid_splits) else len(full_text)
            chunk = full_text[match_end:chunk_end].strip()

            # Checa se antes da questão havia mudança de disciplina
            pre_start = valid_splits[i-1][1] if i > 0 else 0
            between_text = full_text[pre_start:match_start]
            for disc in disciplines_keywords:
                if disc.lower() in between_text.lower():
                    current_materia = disc

            if q_num in disciplina_map:
                current_materia = disciplina_map[q_num]

            # Separa enunciado e alternativas
            alt_matches = list(re.finditer(r'\(([A-Ea-e])\)\s+', chunk))
            alternativas = []

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
                        "correta": (letra == gabarito_map.get(q_num))
                    })
            else:
                enunciado = chunk

            # Limpa ruídos do enunciado
            enunciado = re.sub(r'Caderno de Prova[^\n]+', '', enunciado).strip()

            questoes.append({
                "posicao": q_num,
                "materia": current_materia,
                "textoBase": textos_base_map.get(q_num, ""),
                "enunciado": enunciado,
                "gabaritoOficial": gabarito_map.get(q_num, ""),
                "anulada": gabarito_map.get(q_num) in ["*", "X", "T", "ANULADA"],
                "alternativas": alternativas
            })

        return self.format_to_payload(questoes)
