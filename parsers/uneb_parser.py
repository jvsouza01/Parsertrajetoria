import re
import pypdf
from parsers.base_parser import BaseExamParser

class UNEBParser(BaseExamParser):
    """Parser especializado para a banca Universidade do Estado da Bahia (UNEB)."""

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

        # Remove rodapés da UNEB
        full_text = re.sub(r'Polícia Militar da Bahia[^\n]+', '', full_text)
        full_text = re.sub(r'RASCUNHO', '', full_text)

        # Mapeamento de textos-base ("O texto seguinte servirá de base para responder às questões de X a Y...")
        textos_base_map = {}
        tb_matches = list(re.finditer(
            r'(?:O texto seguinte servirá de base|Leia o texto|Com base no texto)[^\n]*para responder às questões de\s*(\d{1,3})\s*(?:a|e)\s*(\d{1,3})[^\n]*\n(.*?)(?=\n\s*Questão\s+\d{1,3}|\Z)',
            full_text,
            re.DOTALL | re.IGNORECASE
        ))
        for m in tb_matches:
            q_start = int(m.group(1))
            q_end = int(m.group(2))
            tb_content = m.group(3).strip()
            for q_num in range(q_start, q_end + 1):
                textos_base_map[q_num] = tb_content

        disciplines_keywords = [
            "Língua Portuguesa", "Língua Estrangeira", "Inglês", "Espanhol",
            "Matemática", "História", "Geografia", "Atualidades", "Física",
            "Química", "Biologia", "Noções de Direito", "Direito Constitucional",
            "Direitos Humanos", "Direito Administrativo", "Direito Penal",
            "Igualdade Racial e de Gênero", "Informática"
        ]

        # Padrão UNEB de início de questão: "Questão 01" ou "Questão 1"
        candidate_splits = list(re.finditer(r'(?:\n|^)\s*Questão\s+0*(\d{1,3})\b', full_text, re.IGNORECASE))

        valid_splits = []
        for i, match in enumerate(candidate_splits):
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

            # Detecta se há gabarito embutido: "(Correta: C)", "(Gabarito: C)", "(Anulada)"
            gab_embedded = None
            is_anulada = False
            m_gab = re.search(r'\((?:Correta|Gabarito):\s*([A-Ea-eXxTtNn\*])\)', chunk, re.IGNORECASE)
            if m_gab:
                gab_embedded = m_gab.group(1).upper()
                chunk = re.sub(r'\((?:Correta|Gabarito):\s*[A-Ea-eXxTtNn\*]\)', '', chunk).strip()
            elif re.search(r'\(Anulada\)', chunk, re.IGNORECASE):
                is_anulada = True
                chunk = re.sub(r'\(Anulada\)', '', chunk).strip()

            final_gab = gab_embedded or gabarito_map.get(q_num, "")
            if final_gab in ["*", "X", "T", "ANULADA"]:
                is_anulada = True

            # Separa alternativas (A), (B), (C), (D), (E)
            alt_matches = list(re.finditer(r'(?:\n|^|\s)\(([A-Ea-e])\)\s+', chunk))
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
                        "correta": False if is_anulada else (letra == final_gab)
                    })
            else:
                enunciado = chunk

            questoes.append({
                "posicao": q_num,
                "materia": current_materia,
                "textoBase": textos_base_map.get(q_num, ""),
                "enunciado": enunciado,
                "gabaritoOficial": final_gab,
                "anulada": is_anulada,
                "alternativas": alternativas
            })

        return self.format_to_payload(questoes)
