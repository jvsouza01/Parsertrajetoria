import re
import pypdf
from parsers.base_parser import BaseExamParser

class UNEBParser(BaseExamParser):
    """
    Parser especializado e resiliente para a banca Universidade do Estado da Bahia (UNEB).
    Trata gabarito embutido (ex: "(Correta: D)"), dedup de números de questão,
    textos de apoio compartilhados e isolamento correto de matérias.
    """

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

        # Remove rodapés e cabeçalhos fixos da UNEB
        full_text = re.sub(r'Polícia Militar da Bahia[^\n]*', '', full_text, flags=re.IGNORECASE)
        full_text = re.sub(r'Processo Seletivo[^\n]*', '', full_text, flags=re.IGNORECASE)
        full_text = re.sub(r'RASCUNHO[^\n]*', '', full_text, flags=re.IGNORECASE)

        # Mapeamento de textos-base ("O texto seguinte servirá de base para responder às questões de X a Y...")
        textos_base_map = {}
        tb_matches = list(re.finditer(
            r'(?:O texto seguinte servirá de base|Leia o texto|Com base no texto|Para responder às questões)[^\n]*?(?:de|das questões)\s*0*(\d{1,3})\s*(?:a|à|e|-)\s*0*(\d{1,3})[^\n]*\n(.*?)(?=\n\s*Questão\s+\d{1,3}|\Z)',
            full_text,
            re.DOTALL | re.IGNORECASE
        ))
        for m in tb_matches:
            try:
                q_start = int(m.group(1))
                q_end = int(m.group(2))
                tb_content = m.group(3).strip()
                for q_num in range(q_start, q_end + 1):
                    textos_base_map[q_num] = tb_content
            except Exception:
                pass

        # Mapeamento de disciplinas com nomes canônicos oficiais
        disciplines_patterns = [
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?L[ÍI]NGUA\s+PORTUGUESA\b', "Língua Portuguesa"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?LITERATURA(?:\s+BRASILEIRA)?\b', "Língua Portuguesa"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?(?:L[ÍI]NGUA\s+ESTRANGEIRA\s*[-–—]?\s*)?INGL[ÊE]S\b', "Inglês"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?(?:L[ÍI]NGUA\s+ESTRANGEIRA\s*[-–—]?\s*)?ESPANHOL\b', "Espanhol"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?MATEM[ÁA]TICA(?:\s+E\s+RLM)?\b', "Matemática"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?HIST[ÓO]RIA(?:\s+DO\s+BRASIL|\s+GERAL|\s+DA\s+BAHIA)?\b', "História"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?GEOGRAFIA(?:\s+DO\s+BRASIL|\s+GERAL|\s+DA\s+BAHIA)?\b', "Geografia"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?ATUALIDADES\b', "História"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?F[ÍI]SICA\b', "Física"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?QU[ÍI]MICA\b', "Química"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?BIOLOGIA\b', "Biologia"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?FILOSOFIA\b', "Filosofia"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?SOCIOLOGIA\b', "Sociologia"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?NO[ÇC][ÕO]ES\s+DE\s+DIREITO\b', "Direito Constitucional"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?DIREITO\s+CONSTITUCIONAL\b', "Direito Constitucional"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?DIREITOS\s+HUMANOS\b', "Direito Constitucional"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?DIREITO\s+ADMINISTRATIVO\b', "Direito Administrativo"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?DIREITO\s+PENAL(?:\s+MILITAR)?\b', "Direito Penal"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?(?:DIREITO\s+)?PROCESSUAL\s+PENAL(?:\s+MILITAR)?\b', "Direito Processual Penal"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?LEGISLA[ÇC][ÃA]O\s+INSTITUCIONAL\b', "Legislação Institucional"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?IGUALDADE\s+RACIAL\s+E\s+DE\s+G[ÊE]NERO\b', "Legislação Institucional"),
            (r'(?:\n|^)\s*(?:PROVA\s+DE\s+)?INFORM[ÁA]TICA\b', "Informática")
        ]

        # 1. Encontra todas as ocorrências de "Questão XX"
        candidate_splits = list(re.finditer(r'(?:\n|^)\s*Quest[aã]o\s+0*(\d{1,3})\b', full_text, re.IGNORECASE))
        if not candidate_splits:
            return []

        # 2. Agrupa por número de questão para resolver duplicações (ex: URLs de imagens antes do enunciado real)
        splits_by_qnum = {}
        for i, match in enumerate(candidate_splits):
            q_num = int(match.group(1))
            chunk_start = match.end()
            chunk_end = candidate_splits[i+1].start() if i + 1 < len(candidate_splits) else len(full_text)
            chunk_text = full_text[chunk_start:chunk_end].strip()

            # Conta alternativas válidas (A), (B), (C)...
            alts_found = len(re.findall(r'(?:\n|^|\s)\(([A-Ea-e])\)\s+', chunk_text))
            has_embedded_gab = bool(re.search(r'\((?:Correta|Gabarito):\s*([A-Ea-eXxTtNn\*])\)', chunk_text, re.IGNORECASE))
            
            # Score de qualidade do bloco
            score = (alts_found * 100) + (50 if has_embedded_gab else 0) + min(len(chunk_text), 200)
            
            # Se a questão só tem link/URL curta, reduz score
            if chunk_text.startswith("http") or len(chunk_text) < 30:
                score -= 200

            candidate_obj = {
                "q_num": q_num,
                "match_start": match.start(),
                "match_end": match.end(),
                "chunk_end": chunk_end,
                "chunk": chunk_text,
                "score": score,
                "alts_found": alts_found
            }

            if q_num not in splits_by_qnum:
                splits_by_qnum[q_num] = []
            splits_by_qnum[q_num].append(candidate_obj)

        # 3. Seleciona o melhor chunk para cada número de questão (garante 100% sem duplicatas)
        ordered_qnums = sorted(splits_by_qnum.keys())
        questoes = []
        current_materia = "Língua Portuguesa"

        for q_num in ordered_qnums:
            candidates = splits_by_qnum[q_num]
            # Escolhe o candidato com maior pontuação (que tem alternativas e gabarito)
            best = max(candidates, key=lambda c: c["score"])
            chunk = best["chunk"]

            # Checa se antes da questão havia mudança de disciplina por cabeçalho real
            between_text = full_text[max(0, best["match_start"] - 300):best["match_start"]]
            for pat, disc_name in disciplines_patterns:
                if re.search(pat, between_text, re.IGNORECASE):
                    current_materia = disc_name

            if q_num in disciplina_map:
                current_materia = disciplina_map[q_num]

            # Anti-leakage / Detecção de língua estrangeira no bloco da questão
            bloco_texto = f" {textos_base_map.get(q_num, '')} {chunk} ".lower()
            english_markers = [" the ", " and ", " of ", " to ", " in ", " with ", " which ", " according to ", " is ", " that ", " for "]
            spanish_markers = [" el ", " la ", " los ", " las ", " de ", " en ", " y ", " que ", " por ", " según ", " con "]
            
            eng_hits = sum(1 for m in english_markers if m in bloco_texto)
            spa_hits = sum(1 for m in spanish_markers if m in bloco_texto)
            
            materia_questao = current_materia
            if eng_hits >= 3:
                materia_questao = "Inglês"
            elif spa_hits >= 3:
                materia_questao = "Espanhol"

            # Detecta se há gabarito embutido: "(Correta: C)", "(Gabarito: C)", "(Anulada)"
            gab_embedded = None
            is_anulada = False
            m_gab = re.search(r'\((?:Correta|Gabarito):\s*([A-Ea-eXxTtNn\*])\)', chunk, re.IGNORECASE)
            if m_gab:
                raw_letra = m_gab.group(1).upper()
                if raw_letra in ["A", "B", "C", "D", "E"]:
                    gab_embedded = raw_letra
                elif raw_letra in ["*", "X", "T", "N"]:
                    is_anulada = True
                chunk = re.sub(r'\((?:Correta|Gabarito):\s*[A-Ea-eXxTtNn\*]\)', '', chunk).strip()
            elif re.search(r'\(Anulada\)', chunk, re.IGNORECASE):
                is_anulada = True
                chunk = re.sub(r'\(Anulada\)', '', chunk).strip()

            final_gab = gab_embedded or str(gabarito_map.get(q_num, "")).upper()
            if final_gab in ["*", "X", "T", "ANULADA"]:
                is_anulada = True

            # Limpa ruídos de links de imagens ou cabeçalhos espúrios no início do enunciado
            chunk = re.sub(r'^https?://[^\s]+\s*', '', chunk)
            chunk = re.sub(r'^[0-9&_=\.\-a-zA-Z]+\b\s*\n', '', chunk)

            # Separa alternativas (A), (B), (C), (D), (E)
            alt_patterns = [
                r'(?:\n|^|\s)\(([A-Ea-e])\)\s+',
                r'(?:\n|^|\s)([A-Ea-e])\)\s+'
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
                        
                        # Limpa aspas ou pontuação estranha no início/fim da alternativa
                        alternativas.append({
                            "letra": letra,
                            "texto": alt_texto,
                            "correta": False if is_anulada else (letra == final_gab)
                        })
                    break

            questoes.append({
                "posicao": q_num,
                "materia": materia_questao,
                "textoBase": textos_base_map.get(q_num, ""),
                "enunciado": enunciado,
                "gabaritoOficial": final_gab if not is_anulada else "*",
                "anulada": is_anulada,
                "alternativas": alternativas
            })

        return self.format_to_payload(questoes)
