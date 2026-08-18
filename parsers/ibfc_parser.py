import re
import pypdf
from parsers.base_parser import BaseExamParser

class IBFCParser(BaseExamParser):
    """Parser especializado para a banca Instituto Brasileiro de Formação e Capacitação (IBFC)."""

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

        # Remove cabeçalhos e rodapés de página do IBFC
        full_text = re.sub(r'IBFC_[A-Za-z0-9_\-\s]+', '', full_text)
        full_text = re.sub(r'RASCUNHO', '', full_text)

        # Mapeamento de textos-base ("Considere o texto a seguir para responder às questões de X a Y...")
        textos_base_map = {}
        tb_matches = list(re.finditer(
            r'(?:Considere o texto a seguir|Leia o texto a seguir|Com base no texto a seguir|Texto\s+[I|V|X\d]+)[^\n]*para responder às questões de\s*(\d{1,3})\s*(?:a|e)\s*(\d{1,3})[^\n]*\n(.*?)(?=\n\s*\d{1,3}\)\s+[A-ZÀ-ÿ\-\"\'\(\“\”\‘\’«»]|\Z)',
            full_text,
            re.DOTALL | re.IGNORECASE
        ))
        for m in tb_matches:
            q_start = int(m.group(1))
            q_end = int(m.group(2))
            tb_content = m.group(3).strip()
            for q_num in range(q_start, q_end + 1):
                textos_base_map[q_num] = tb_content

        # Padrão IBFC: Busca especificamente a sequência crescente 1, 2, 3... N
        # Evita capturar subitens internos como "COLUNA I \n 1) Decreto..."
        valid_splits = []
        expected_q = 1
        pos = 0

        while expected_q <= 120 and pos < len(full_text):
            # Procura pelo próximo número esperado: "\n 1) " ou "\n1) "
            pattern = re.compile(rf'(?:\n|^)\s*({expected_q})\)\s+(?=[A-ZÀ-ÿ\-\"\'\(\“\”\‘\’«»])')
            m = pattern.search(full_text, pos)
            if m:
                valid_splits.append((expected_q, m.start(), m.end()))
                pos = m.end()
                expected_q += 1
            else:
                # Tenta avançar se a prova pulou ou se não achou
                # Olha um pouco a frente para o próximo
                next_pat = re.compile(rf'(?:\n|^)\s*({expected_q + 1})\)\s+(?=[A-ZÀ-ÿ\-\"\'\(\“\”\‘\’«»])')
                m_next = next_pat.search(full_text, pos)
                if m_next:
                    valid_splits.append((expected_q + 1, m_next.start(), m_next.end()))
                    pos = m_next.end()
                    expected_q += 2
                else:
                    break

        questoes = []
        current_materia = "Língua Portuguesa"

        for i, (q_num, match_start, match_end) in enumerate(valid_splits):
            chunk_end = valid_splits[i+1][1] if i + 1 < len(valid_splits) else len(full_text)
            chunk = full_text[match_end:chunk_end].strip()

            if q_num in disciplina_map:
                current_materia = disciplina_map[q_num]

            # Separa alternativas no padrão "a) ", "b) ", "c) ", "d) ", "e) " ou "(a) ", "(b) "
            alt_matches = list(re.finditer(r'(?:\n|^|\s)(?:([a-eA-E])\)|\(([a-eA-E])\))\s+', chunk))
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
                        "correta": (letra == gabarito_map.get(q_num))
                    })
            else:
                enunciado = chunk

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
