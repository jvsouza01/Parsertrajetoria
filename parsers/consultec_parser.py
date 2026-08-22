import re
import pypdf
from parsers.base_parser import BaseExamParser

class ConsultecParser(BaseExamParser):
    """
    Parser especializado para as bancas CONSULTEC e AIETEC (vestibulares e concursos como UESB, UNDB, UNESULBAHIA, etc.).
    Suporta:
    - Alternativas em formato de letra: A), B), C), D), E)
    - Alternativas em formato numérico baiano: 01), 02), 03), 04), 05) (com conversão A..E)
    - Textos-base por bloco: "Questões de X a Y", "Texto 1", "Texto A"
    - Detecção automática de disciplinas por cabeçalho de seção
    - Extração automática de gabarito embutido ou na última página
    """

    NUMERIC_TO_LETTER = {
        "01": "A", "1": "A",
        "02": "B", "2": "B",
        "03": "C", "3": "C",
        "04": "D", "4": "D",
        "05": "E", "5": "E"
    }

    DISCIPLINAS_CONHECIDAS = [
        ("Língua Portuguesa e Literatura Brasileira", ["LÍNGUA PORTUGUESA", "LITERATURA BRASILEIRA", "PORTUGUÊS"]),
        ("Língua Estrangeira - Inglês", ["LÍNGUA ESTRANGEIRA - INGLÊS", "LÍNGUA ESTRANGEIRA (INGLÊS)", "INGLÊS"]),
        ("Língua Estrangeira - Francês", ["LÍNGUA ESTRANGEIRA - FRANCÊS", "FRANCÊS"]),
        ("Língua Estrangeira - Espanhol", ["LÍNGUA ESTRANGEIRA - ESPANHOL", "ESPANHOL"]),
        ("Matemática / Raciocínio Lógico", ["MATEMÁTICA / RACIOCÍNIO LÓGICO", "MATEMÁTICA/RACIOCÍNIO LÓGICO", "MATEMÁTICA"]),
        ("Ciências Humanas", ["CIÊNCIAS HUMANAS", "HISTÓRIA", "GEOGRAFIA", "FILOSOFIA", "SOCIOLOGIA"]),
        ("Ciências da Natureza", ["CIÊNCIAS DA NATUREZA", "CIÊNCIAS NATUREZA", "FÍSICA", "QUÍMICA", "BIOLOGIA"])
    ]

    def parse_pdf(self, pdf_path_or_stream, gabarito_map=None, disciplina_map=None):
        gabarito_map = gabarito_map or {}
        disciplina_map = disciplina_map or {}

        reader = pypdf.PdfReader(pdf_path_or_stream)
        pages_text = []
        for p in reader.pages:
            t = p.extract_text() or ""
            pages_text.append(t)

        # Checa se a última página é uma folha de gabarito oficial Consultec/Aietec
        if len(pages_text) > 0 and not gabarito_map:
            last_text = pages_text[-1]
            if "GABARITO" in last_text.upper():
                auto_gab, auto_disc = self.extract_consultec_gabarito_page(last_text)
                if auto_gab:
                    gabarito_map.update(auto_gab)
                if auto_disc:
                    disciplina_map.update(auto_disc)
                pages_text = pages_text[:-1]

        # Mapeamento de seções de matérias
        full_doc_text = "\n".join(pages_text)
        secoes_materia = []
        pattern_secao = r'(?:^|\n)\s*([A-Za-zÀ-ÿ\s\/\(\)\-]+?)\s*(?:[\-\–\|]|–)\s*(?:Questões\s+)?(?:de\s+)?(\d{1,3})\s*(?:a|à)\s*(\d{1,3})'
        for m in re.finditer(pattern_secao, full_doc_text, re.IGNORECASE):
            nome_raw = m.group(1).strip()
            q_de = int(m.group(2))
            q_ate = int(m.group(3))
            nome_norm = self._normalizar_materia(nome_raw)
            if nome_norm:
                secoes_materia.append((q_de, q_ate, nome_norm))

        questoes = []
        current_pos = 1
        current_materia = "Língua Portuguesa e Literatura Brasileira"

        for p_idx, page_raw in enumerate(pages_text):
            p_text = self.clean_text(page_raw)

            # Ignora páginas exclusivas de instruções de redação ou tabela periódica vazias de questões
            if re.search(r'REDA[ÇC][ÃA]O\s*\n\s*INSTRU[ÇC][ÕO]ES', p_text, re.IGNORECASE) and "Questão" not in p_text:
                continue
            if "CLASSIFICAÇÃO PERIÓDICA DOS ELEMENTOS QUÍMICOS" in p_text and "Questão" not in p_text:
                continue
            if re.search(r'^\s*INSTRU[ÇC][ÕO]ES\s*\n', p_text, re.IGNORECASE) and p_idx <= 1:
                continue

            # Detecta alternativas na página
            alt_pattern = r'(?:^|\n|\s)([A-Ea-e])\s*[\)\.\-]\s+'
            is_num = False
            alts_found = list(re.finditer(alt_pattern, p_text))
            if len(alts_found) < 3:
                num_pattern = r'(?:^|\n|\s)0*([1-5])\s*[\)\.\-]\s+'
                num_alts = list(re.finditer(num_pattern, p_text))
                if len(num_alts) >= 3:
                    alts_found = num_alts
                    is_num = True

            if not alts_found:
                continue

            # Agrupa alternativas em questões (cada bloco inicia com 'A' ou '01')
            q_groups = []
            curr_group = []
            for am in alts_found:
                lbl = am.group(1).upper()
                letra = self.NUMERIC_TO_LETTER.get(lbl, lbl) if is_num else lbl
                if letra == 'A' and curr_group:
                    q_groups.append(curr_group)
                    curr_group = []
                curr_group.append((letra, am.start(), am.end()))
            if curr_group:
                q_groups.append(curr_group)

            for g_idx, g in enumerate(q_groups):
                if len(g) < 2:
                    continue

                prev_end = q_groups[g_idx-1][-1][2] if g_idx > 0 else 0
                enunc_chunk = p_text[prev_end:g[0][1]].strip()

                # Tenta achar número explícito da questão no enunciado
                m_qnum = re.search(r'(?:QUEST[ÃA]O|Quest[ãa]o)\s*0*(\d{1,3})\b', enunc_chunk, re.IGNORECASE)
                if not m_qnum:
                    m_qnum = re.search(r'(?:^|\n)\s*0*(\d{1,3})\s*QUEST[ÃA]O\b', enunc_chunk, re.IGNORECASE)

                if m_qnum:
                    q_num = int(m_qnum.group(1))
                else:
                    q_num = current_pos

                # Limpeza do enunciado
                enunc_clean = enunc_chunk
                enunc_clean = re.sub(r'^(?:UNDB|UESB|CONSULTEC|AIETEC|PROCESSO|L[ÍI]NGUA|MATEM[ÁA]TICA|CI[ÊE]NCIAS)[^\n]*\n', '', enunc_clean, flags=re.IGNORECASE)
                enunc_clean = re.sub(r'(?:QUEST[ÃA]O\s*\d+|\d+\s*QUEST[ÃA]O|QUEST[ÕO]ES\s+de\s+\d+\s+a\s+\d+)', '', enunc_clean, flags=re.IGNORECASE)
                enunc_clean = re.sub(r'^\s*[:\-\–\.]\s*', '', enunc_clean).strip()

                # Se o enunciado ficou muito curto ou vazio
                if len(enunc_clean) < 10 and "Questão" not in enunc_clean:
                    enunc_clean = f"Questão {q_num} - Prova {self.cargo or self.orgao}."

                # Extrai texto de cada alternativa
                alts_list = []
                for a_i, (letra, a_start, a_end) in enumerate(g):
                    alt_end = g[a_i+1][1] if a_i + 1 < len(g) else (q_groups[g_idx+1][0][1] if g_idx + 1 < len(q_groups) else len(p_text))
                    alt_text = p_text[a_end:alt_end].strip()
                    # Remove rodapés residuais do fim da última alternativa
                    alt_text = re.sub(r'\n(?:UNDB|UESB|AIETEC|L[íi]ngua|Matem[áa]tica|Ci[êe]ncias)[^\n]*$', '', alt_text, flags=re.IGNORECASE).strip()
                    alts_list.append({'letra': letra, 'texto': alt_text})

                # Determina matéria
                for (q_de, q_ate, mat) in secoes_materia:
                    if q_de <= q_num <= q_ate:
                        current_materia = mat
                        break
                if q_num in disciplina_map:
                    current_materia = disciplina_map[q_num]

                # Gabarito
                final_gab = str(gabarito_map.get(q_num, "")).strip().upper()
                is_anulada = (final_gab in ["*", "X", "T", "ANULADA"])
                if final_gab in self.NUMERIC_TO_LETTER:
                    final_gab = self.NUMERIC_TO_LETTER[final_gab]

                for alt in alts_list:
                    alt["correta"] = False if is_anulada else (alt["letra"] == final_gab)

                questoes.append({
                    "posicao": q_num,
                    "materia": current_materia,
                    "enunciado": enunc_clean,
                    "gabaritoOficial": final_gab,
                    "anulada": is_anulada,
                    "alternativas": alts_list
                })
                current_pos = max(current_pos + 1, q_num + 1)

        # Ordena e remove duplicadas se houver
        questoes_ordenadas = sorted(questoes, key=lambda x: x["posicao"])
        vistas = set()
        questoes_finais = []
        for q in questoes_ordenadas:
            if q["posicao"] not in vistas:
                vistas.add(q["posicao"])
                questoes_finais.append(q)

        return self.format_to_payload(questoes_finais)

    def extract_consultec_gabarito_page(self, text):
        """Extrai gabarito oficial formatado no padrão Consultec / Aietec."""
        gab_map = {}
        disc_map = {}
        
        matches = re.findall(r'(?:^|\s)0*(\d{1,3})\s*[\)\.]\s*(0[1-5]|[1-5]|[A-Ea-eXxTtNn\*]|Anulada\b)', text, re.IGNORECASE)
        for num_str, resp_raw in matches:
            num = int(num_str)
            resp = resp_raw.strip().upper()
            if resp in ["ANULADA", "*"]:
                gab_map[num] = "*"
            elif resp in self.NUMERIC_TO_LETTER:
                gab_map[num] = self.NUMERIC_TO_LETTER[resp]
            else:
                gab_map[num] = resp

        return gab_map, disc_map

    def _normalizar_materia(self, raw):
        raw_upper = raw.upper()
        for nome_padrao, keywords in self.DISCIPLINAS_CONHECIDAS:
            for kw in keywords:
                if kw in raw_upper:
                    return nome_padrao
        return raw.strip()
