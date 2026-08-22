import re
import pypdf

class GabaritoExtractor:
    """
    Extrator unificado e inteligente de gabaritos:
    - Suporta FCC ("001 - B 002 - D ...")
    - Suporta IBFC / FGV / VUNESP em tabelas (linhas de números seguidas de linhas de letras, incluindo '*' para anuladas)
    - Suporta ENEM e listas simples ("1 A 2 B ...")
    - Suporta gabaritos colados manualmente em texto ("1-A, 2-B, 3: C, 4. D")
    - Extrai também mapeamento de disciplinas caso estejam presentes no gabarito (como no IBFC)
    """

    @staticmethod
    def extract_from_pdf(pdf_path_or_stream):
        """Lê o texto completo de um PDF de gabarito e extrai {numero: resposta} e {numero: disciplina}."""
        try:
            reader = pypdf.PdfReader(pdf_path_or_stream)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text() or ""
                full_text += text + "\n"
            return GabaritoExtractor.extract_from_text(full_text)
        except Exception as e:
            print(f"[GabaritoExtractor] Erro ao ler PDF de gabarito: {e}")
            return {}, {}

    @staticmethod
    def extract_from_text(text):
        """
        Retorna uma tupla (gabarito_map, disciplina_map).
        gabarito_map: dict {int(num): 'A'|'B'|'C'|'D'|'E'|'*'}
        disciplina_map: dict {int(num): str(disciplina)}
        """
        if not text or not text.strip():
            return {}, {}

        text = text.strip()
        gabarito_map = {}
        disciplina_map = {}

        # 1. Padrão FCC: "001 - B", "01 - B", "1 - B", "001-B", "001 - *"
        fcc_matches = re.findall(r'(?:^|\s)0*(\d{1,3})\s*-\s*([A-Ea-eXxTtNn\*])', text)
        if len(fcc_matches) >= 5:
            for num_str, letra in fcc_matches:
                gabarito_map[int(num_str)] = letra.upper()
            return gabarito_map, disciplina_map

        # 2. Padrão Tabelar IBFC / Multidisciplinar
        # Varre linha por linha procurando pares de linhas:
        # Linha A: "1 2 3 4 5 6 7 8"
        # Linha B: "D C D E A B C B"
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        current_discipline = None

        for idx, line in enumerate(lines):
            # Se for um título provável de disciplina (sem números no início, letras maiúsculas)
            if not re.match(r'^\d+', line) and not re.match(r'^[A-E\*\s]+$', line, re.IGNORECASE):
                # Ignora cabeçalhos genéricos
                if not any(k in line.upper() for k in ["GOVERNO", "ESTADO", "SECRETARIA", "CONCURSO", "GABARITO", "OFICIAL", "VERSÃO", "POLÍCIA", "CARGO"]):
                    current_discipline = line.title()

            tokens = line.split()
            # Se todos os tokens forem números inteiros (ex: 1 2 3 4 ou 41 42 43)
            if len(tokens) >= 2 and all(t.isdigit() for t in tokens):
                # Olha a próxima linha para ver se são as respostas
                if idx + 1 < len(lines):
                    resp_tokens = lines[idx + 1].split()
                    if len(resp_tokens) == len(tokens) and all(re.match(r'^[A-Ea-eXxTtNn\*]$', r) for r in resp_tokens):
                        for num_str, resp in zip(tokens, resp_tokens):
                            num = int(num_str)
                            gabarito_map[num] = resp.upper()
                            if current_discipline:
                                disciplina_map[num] = current_discipline

        if len(gabarito_map) >= 5:
            return gabarito_map, disciplina_map

        # 3. Padrão Consultec / Aietec / Vestibulares com '1) 05', '1. C', '10. Anulada', '25) 01*'
        num_map = {"01": "A", "1": "A", "02": "B", "2": "B", "03": "C", "3": "C", "04": "D", "4": "D", "05": "E", "5": "E"}
        consultec_matches = re.findall(r'(?:^|\s)0*(\d{1,3})\s*[\)\.\:]\s*(0[1-5]|[1-5]|[A-Ea-eXxTtNn\*]|Anulada\b)', text, re.IGNORECASE)
        if len(consultec_matches) >= 5:
            for num_str, val_raw in consultec_matches:
                num = int(num_str)
                v = val_raw.strip().upper()
                if v in ["ANULADA", "*", "X", "T"]:
                    gabarito_map[num] = "*"
                elif v in num_map:
                    gabarito_map[num] = num_map[v]
                elif v in ["A", "B", "C", "D", "E"]:
                    gabarito_map[num] = v
            if len(gabarito_map) >= 5:
                return gabarito_map, disciplina_map

        # 4. Padrão ENEM / Padrão direto: "1 A", "01 B", "10 C", "1 - A", "1: A", "1. A", "1) A"
        direct_matches = re.findall(r'(?:^|\s)0*(\d{1,3})\s*[\.\:\)\-]?\s*([A-Ea-eXxTtNn\*])(?=\s|$|[,\;\.\)])', text)
        if len(direct_matches) >= 5:
            for num_str, letra in direct_matches:
                gabarito_map[int(num_str)] = letra.upper()
            return gabarito_map, disciplina_map

        # 5. Fallback: pares isolados de número e letra
        fallback_matches = re.findall(r'(\d{1,3})\s*[\s\-\:\.\)]\s*([A-Ea-eXxTtNn\*])', text)
        if fallback_matches:
            for num_str, letra in fallback_matches:
                gabarito_map[int(num_str)] = letra.upper()

        return gabarito_map, disciplina_map

