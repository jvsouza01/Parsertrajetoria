import os
import re
import io
import json
import time
import base64
import requests
import pypdf
from concurrent.futures import ThreadPoolExecutor, as_completed

def _load_env_file():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip()

_load_env_file()

DEFAULT_GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")

DEFAULT_MODELS_CASCADE = [
    "gemini-2.5-flash",
    "gemini-3.5-flash",
    "gemini-3.7-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest"
]

# ==============================================================================
# SCHEMAS ESTRUTURADOS OFICIAIS (Structured Outputs - response_schema)
# ==============================================================================

QUESTION_EXTRACTION_SCHEMA = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "posicao": {"type": "INTEGER"},
            "materiaNome": {"type": "STRING", "nullable": True},
            "assunto": {"type": "STRING", "nullable": True},
            "textoBase": {"type": "STRING", "nullable": True},
            "enunciado": {"type": "STRING"},
            "temImagem": {"type": "BOOLEAN"},
            "descricaoImagem": {"type": "STRING", "nullable": True},
            "gabaritoOficial": {"type": "STRING"},
            "anulada": {"type": "BOOLEAN"},
            "alternativas": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "letra": {"type": "STRING"},
                        "texto": {"type": "STRING"},
                        "correta": {"type": "BOOLEAN"}
                    },
                    "required": ["letra", "texto", "correta"]
                }
            }
        },
        "required": ["posicao", "enunciado", "alternativas", "temImagem"]
    }
}

QUESTION_AUDIT_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "materiaNome": {"type": "STRING", "nullable": True},
        "assunto": {"type": "STRING", "nullable": True},
        "enunciado": {"type": "STRING"},
        "textoBase": {"type": "STRING", "nullable": True},
        "gabaritoOficial": {"type": "STRING"},
        "anulada": {"type": "BOOLEAN"},
        "alternativas": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "letra": {"type": "STRING"},
                    "texto": {"type": "STRING"},
                    "correta": {"type": "BOOLEAN"}
                },
                "required": ["letra", "texto", "correta"]
            }
        },
        "confianca": {"type": "NUMBER"},
        "statusRevisao": {"type": "STRING"},
        "motivosRevisao": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
        "melhoriasAplicadas": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        }
    },
    "required": ["enunciado", "alternativas", "confianca", "statusRevisao"]
}

SYSTEM_INSTRUCTION_EXTRACTOR = """Você é um especialista sênior em transcrição e extração de provas de concursos públicos e vestibulares.
Sua missão é transcrever integralmente o texto das questões a partir do PDF visual com 100% de fidelidade.

DIRETRIZES FUNDAMENTAIS DE TRANSCRIÇÃO:
1. TRANSCRIÇÃO COMPLETA DE TODAS AS QUESTÕES NUMERADAS:
   - Toda e qualquer questão numerada (Questão 01, Questão 02, etc.) DEVE ser extraída na íntegra.
   - Em cadernos que começam com seções de Redação, temas ou instruções e depois iniciam as questões da prova objetiva (ex: "Questão 01", "Questão 02"...), NUNCA ignore a primeira página com questões! Extraia rigorosamente desde a Questão 01.

2. TEXTOS DE APOIO / TEXTOS-BASE (REGRA DE OURO):
   - Qualquer texto, fragmento literário, conto, citação, crônica, poema, artigo de lei, reportagem ou caixa de leitura que anteceda uma ou mais questões (ex: "O texto seguinte servirá de base para responder às questões de 1 a 7", "Considere o fragmento...") NUNCA DEVE SER PERDIDO.
   - Extraia o texto base completo no campo 'textoBase'.
   - O campo 'enunciado' deve conter a pergunta/comando específico da questão.

3. DESTAQUES TIPOGRÁFICOS (SUBLINHADOS E NEGRITOS COM TAGS HTML):
   - Se no PDF visual houver palavras, orações ou expressões sublinhadas (com traço embaixo), você DEVE envolvê-las com a tag <u>...</u> (ex: <u>jogam</u>, <u>Alugamos</u>, <u>A família do morto</u>, <u>precisam</u>) tanto no textoBase, quanto no enunciado e nas alternativas.
   - Se houver termos em negrito no original, use **...** ou <b>...</b>.

4. CLASSIFICAÇÃO CANÔNICA DE MATÉRIAS:
   - Utilize a grade canônica oficial para 'materiaNome':
     * "Língua Portuguesa"
     * "Inglês" (para questões ou textos em inglês)
     * "Espanhol" (para questões ou textos em espanhol)
     * "Matemática" (ou Raciocínio Lógico)
     * "História"
     * "Geografia"
     * "Física"
     * "Química"
     * "Biologia"
     * "Filosofia"
     * "Sociologia"
     * "Direito Constitucional"
     * "Direito Administrativo"
     * "Direito Penal"
     * "Direito Processual Penal"
     * "Legislação Institucional"
     * "Informática"
   - REGRA CRÍTICA PARA 'materiaNome':
     * Se o texto da questão/texto-base for em INGLÊS, defina 'materiaNome': "Inglês".
     * Se for em ESPANHOL, defina 'materiaNome': "Espanhol".
     * Se houver cabeçalho de seção explícito na página (ex: "PROVA DE HISTÓRIA"), utilize a matéria correspondente.
     * Se NÃO houver cabeçalho explícito ou se houver dúvida sobre a matéria, defina 'materiaNome': null (a IA da plataforma fará a classificação global com 100% de acerto). NUNCA invente nem atribua uma matéria do bloco anterior se o conteúdo não for dela!

5. TRANSCRIÇÃO LITERAL E INTEGRAL:
   - NUNCA resuma, abrevie ou omita opções de resposta ou trechos de enunciado. Preserve pontuação, itálicos, aspas e referências bibliográficas (autor/obra) na íntegra.

6. ELEMENTOS VISUAIS (IMAGENS/FIGURAS):
   - Se a questão contiver imagens, charges, tirinhas, mapas, gráficos, esquemas ou diagramas, defina 'temImagem': true e descreva detalhadamente em 'descricaoImagem'.

7. GABARITO OFICIAL E ANULAÇÕES:
   - Se a alternativa correta estiver anotada na prova (ex: '(Correta: X)', gabarito ao lado ou ao final), preencha 'gabaritoOficial' e marque 'correta': true na alternativa certa.
   - Se a questão estiver anulada, marque 'anulada': true.

8. ALTERNATIVAS NUMÉRICAS (FORMATO VESTIBULAR - UESB, UNIFACS, UNEC, UESB, etc.):
   - Algumas provas usam alternativas numeradas como 01) 02) 03) 04) 05) em vez de A) B) C) D) E).
   - REGRA CRÍTICA DE DISTINÇÃO:
     * Uma QUESTÃO é identificada por um cabeçalho explícito como "QUESTÃO 7", "QUESTÃO 8", "7.", "8." no início de um bloco.
     * Uma ALTERNATIVA NUMÉRICA é um item indentado e sequencial (01, 02, 03, 04, 05) que aparece dentro do corpo de uma questão já iniciada, logo abaixo do enunciado.
   - Quando as alternativas forem numéricas (01 a 05), mapeie-as para letras da seguinte forma:
     * 01 → letra "A"
     * 02 → letra "B"
     * 03 → letra "C"
     * 04 → letra "D"
     * 05 → letra "E"
   - NUNCA confunda itens 01/02/03/04/05 de alternativas com o número da questão. O número da questão vem sempre de um cabeçalho explícito como "QUESTÃO N"."""

SYSTEM_INSTRUCTION_AUDITOR = """Você é um auditor técnico especialista em questões de concursos e vestibulares.
Sua missão é realizar denoising (limpeza de quebras de linha e hifenização indevida de colunas duplas), auditar integridade de enunciados/alternativas e validar conformidade com o gabarito oficial e classificação canônica de matéria."""


class GeminiService:
    """
    Serviço resiliente para integração com a API Google Gemini e Google Cloud Vertex AI.
    Suporta:
    - Google Cloud Vertex AI oficial (Pós-pago via Service Account JSON)
    - Pool de Múltiplas Chaves de API com chaveamento instantâneo em 429
    - Structured Outputs nativo (response_schema)
    - Transcrição determinística (temperature 0.0)
    - Cascata automática de modelos e retries com backoff exponencial
    """

    def __init__(self, api_key=None, models_cascade=None):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Detecção automática de Service Account do Vertex AI
        self.is_vertex = False
        self.vertex_creds = None
        self.vertex_project_id = None
        self.vertex_location = "us-central1"
        
        sa_files = [f for f in os.listdir(project_root) if f.endswith('.json') and ('overview' in f.lower() or 'service' in f.lower() or 'gemini' in f.lower() or 'groovy' in f.lower())]
        if sa_files:
            try:
                from google.oauth2 import service_account
                sa_path = os.path.join(project_root, sa_files[0])
                self.vertex_creds = service_account.Credentials.from_service_account_file(
                    sa_path,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                self.vertex_project_id = self.vertex_creds.project_id
                self.is_vertex = True
                print(f"[OK] [GeminiService] Vertex AI Pós-Pago CONECTADA com sucesso! Projeto: {self.vertex_project_id}")
            except Exception as e:
                print(f"[!] [GeminiService] Aviso ao carregar credenciais Vertex AI: {e}")

        if isinstance(api_key, list):
            self.api_keys = [str(k).strip() for k in api_key if k and str(k).strip()]
        elif isinstance(api_key, str) and (',' in api_key or ';' in api_key or '\n' in api_key):
            self.api_keys = [k.strip() for k in re.split(r'[,;\n]+', api_key) if k.strip()]
        elif api_key:
            self.api_keys = [api_key.strip()]
        else:
            default_env = os.environ.get("GEMINI_API_KEY", "") or DEFAULT_GEMINI_KEY
            self.api_keys = [k.strip() for k in re.split(r'[,;\n]+', default_env) if k.strip()]

        self.api_key = self.api_keys[0] if self.api_keys else ""
        self.models_cascade = models_cascade or DEFAULT_MODELS_CASCADE
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def _convert_payload_for_vertex(self, payload):
        """Converte o payload do padrão AI Studio para a especificação oficial Vertex AI REST."""
        import copy
        p = copy.deepcopy(payload)
        
        # 1. system_instruction -> systemInstruction
        if "system_instruction" in p:
            p["systemInstruction"] = p.pop("system_instruction")
            
        # 2. contents -> garantir role 'user' e inlineData camelCase
        if "contents" in p:
            for item in p["contents"]:
                if "role" not in item:
                    item["role"] = "user"
                if "parts" in item:
                    for part in item["parts"]:
                        if "inline_data" in part:
                            data_obj = part.pop("inline_data")
                            part["inlineData"] = {
                                "mimeType": data_obj.get("mime_type", "application/pdf"),
                                "data": data_obj.get("data", "")
                            }
                            
        # 3. generationConfig -> camelCase
        if "generationConfig" in p:
            gc = p["generationConfig"]
            if "response_mime_type" in gc:
                gc["responseMimeType"] = gc.pop("response_mime_type")
            if "response_schema" in gc:
                gc["responseSchema"] = gc.pop("response_schema")
                
        return p

    def _call_gemini_with_fallback(self, payload, custom_models=None, timeout=240, log_callback=None):
        """
        Executa a requisição com cascata transparente de modelos via Vertex AI (Pós-pago) ou AI Studio.
        """
        last_error = None

        # -------------------------------------------------------------
        # CAMINHO 1: VERTEX AI OFICIAL (GOOGLE CLOUD PÓS-PAGO)
        # -------------------------------------------------------------
        if self.is_vertex and self.vertex_creds:
            import google.auth.transport.requests
            try:
                self.vertex_creds.refresh(google.auth.transport.requests.Request())
                token = self.vertex_creds.token
            except Exception as auth_err:
                token = None
                last_error = f"Erro de autenticação Vertex: {auth_err}"

            if token:
                vertex_payload = self._convert_payload_for_vertex(payload)
                # Modelo principal: gemini-2.5-flash (ultra veloz e sem limites)
                vertex_models = custom_models or ["gemini-2.5-flash", "gemini-2.5-pro"]
                for model in vertex_models:
                    url = f"https://{self.vertex_location}-aiplatform.googleapis.com/v1/projects/{self.vertex_project_id}/locations/{self.vertex_location}/publishers/google/models/{model}:generateContent"
                    headers = {
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }

                    if log_callback:
                        log_callback(f"Extraindo via Vertex AI ({model}) [Pós-Pago]...", "info")

                    for attempt in range(2):
                        try:
                            res = requests.post(url, headers=headers, json=vertex_payload, timeout=timeout)
                            if res.status_code == 200:
                                data = res.json()
                                candidates = data.get("candidates", [])
                                if candidates and "content" in candidates[0]:
                                    parts = candidates[0]["content"].get("parts", [])
                                    if parts and "text" in parts[0]:
                                        return parts[0]["text"], f"vertex-{model}"
                                raise ValueError(f"Resposta sem conteúdo de texto ({model})")
                            elif res.status_code in [500, 503]:
                                time.sleep(3.0)
                                continue
                            elif res.status_code == 429:
                                time.sleep(5.0)
                                continue
                            else:
                                last_error = f"HTTP {res.status_code} Vertex: {res.text[:140]}"
                                break
                        except requests.exceptions.Timeout:
                            last_error = f"Timeout ({timeout}s) em Vertex {model}"
                            break
                        except Exception as req_err:
                            last_error = str(req_err)
                            time.sleep(1.0)

                # Se a Vertex AI está configurada, não cai para o AI Studio (evita erro de pré-pago)
                raise RuntimeError(f"Vertex AI falhou. Último erro: {last_error}")

        # -------------------------------------------------------------
        # CAMINHO 2: GOOGLE AI STUDIO (FALLBACK / CHAVE DE API)
        # -------------------------------------------------------------
        models = custom_models or self.models_cascade
        keys_pool = list(self.api_keys) if self.api_keys else [self.api_key]

        for model in models:
            for key_idx, current_key in enumerate(keys_pool):
                key_masked = f"{current_key[:6]}...{current_key[-4:]}" if len(current_key) > 10 else f"Chave {key_idx+1}"
                url = f"{self.base_url}/{model}:generateContent?key={current_key}"
                headers = {"Content-Type": "application/json"}

                if log_callback and len(keys_pool) > 1:
                    log_callback(f"Tentando {model} via Chave #{key_idx + 1} ({key_masked})...", "info")
                elif log_callback:
                    log_callback(f"Tentando extração com o modelo {model}...", "info")

                for attempt in range(2):
                    try:
                        res = requests.post(url, headers=headers, json=payload, timeout=timeout)
                        
                        if res.status_code == 200:
                            data = res.json()
                            candidates = data.get("candidates", [])
                            if candidates and "content" in candidates[0]:
                                parts = candidates[0]["content"].get("parts", [])
                                if parts and "text" in parts[0]:
                                    return parts[0]["text"], model
                            raise ValueError(f"Resposta sem conteúdo de texto ({model})")
                        
                        elif res.status_code == 429:
                            if len(keys_pool) > 1 and key_idx < len(keys_pool) - 1:
                                if log_callback:
                                    log_callback(f"Chave #{key_idx + 1} atingiu cota (429). Alternando imediatamente para Chave #{key_idx + 2}...", "warning")
                                break

                            wait_time = 10.0 + (attempt * 12.0)
                            if log_callback:
                                log_callback(f"Rate limit 429 em {model}. Aguardando {wait_time:.1f}s para liberar cota...", "warning")
                            time.sleep(wait_time)
                            last_error = f"Rate limit 429 em {model}"
                            continue
                        
                        elif res.status_code in [500, 503]:
                            if attempt == 0:
                                time.sleep(2.5)
                                continue
                            last_error = f"HTTP {res.status_code} em {model}"
                            break
                        
                        elif res.status_code == 404:
                            last_error = f"Modelo {model} indisponível (404)"
                            break
                        
                        else:
                            last_error = f"HTTP {res.status_code}: {res.text[:140]}"
                            time.sleep(0.5)
                    
                    except requests.exceptions.Timeout:
                        last_error = f"Timeout ({timeout}s) em {model}"
                        break
                    except Exception as e:
                        last_error = str(e)
                        time.sleep(0.5)

        raise RuntimeError(f"Todos os modelos da cascata falharam. Último erro: {last_error}")

    def _clean_json_text(self, text):
        """Extrai a estrutura JSON (objeto ou array) de forma robusta."""
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
        text = text.strip()
        
        # Se contiver delimitadores no meio ou texto explicativo extra, busca o bloco JSON
        if not (text.startswith("{") or text.startswith("[")):
            match = re.search(r"(\[.*\]|\{.*\})", text, re.DOTALL)
            if match:
                text = match.group(1).strip()
        return text

    def enhance_and_audit_question(self, questao, metadata=None):
        """
        Trata, limpa, valida e audita a integridade estrutural de uma questão individual
        usando Structured Outputs (response_schema) e system_instruction.
        """
        metadata = metadata or {}
        banca = metadata.get("banca", questao.get("banca", "GERAL"))
        cargo = metadata.get("cargo", questao.get("cargo", ""))
        ano = metadata.get("ano", questao.get("ano", 2025))

        questao_input = {
            "posicao": questao.get("posicao", 1),
            "materiaNome": questao.get("materiaNome"),
            "assunto": questao.get("assunto"),
            "gabaritoOficial": questao.get("gabaritoOficial", ""),
            "textoBaseOriginal": questao.get("textoBase") or questao.get("textoApoio", ""),
            "enunciadoOriginal": questao.get("enunciado", ""),
            "alternativasOriginais": questao.get("alternativas", []),
            "contextoProva": f"Banca: {banca} | Cargo: {cargo} | Ano: {ano}"
        }

        payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_INSTRUCTION_AUDITOR}]
            },
            "contents": [
                {
                    "parts": [
                        {"text": f"DADOS DA QUESTÃO PARA AUDITORIA:\n{json.dumps(questao_input, ensure_ascii=False, indent=2)}"}
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "response_schema": QUESTION_AUDIT_SCHEMA,
                "temperature": 0.0
            }
        }

        raw_text, model_used = self._call_gemini_with_fallback(payload)
        cleaned_json = self._clean_json_text(raw_text)
        result = json.loads(cleaned_json)

        enhanced = dict(questao)
        enhanced["enunciado"] = result.get("enunciado", questao.get("enunciado"))
        
        # Preserva ou atualiza textoBase
        tb_result = result.get("textoBase") or questao.get("textoBase") or questao.get("textoApoio")
        enhanced["textoBase"] = tb_result if tb_result else None
        enhanced["textoApoio"] = enhanced["textoBase"]
        
        # Preserva ou atualiza materiaNome
        if "materiaNome" in result:
            enhanced["materiaNome"] = result.get("materiaNome")
            
        if "assunto" in result:
            enhanced["assunto"] = result.get("assunto")
        
        gab_result = result.get("gabaritoOficial") or questao.get("gabaritoOficial", "")
        enhanced["gabaritoOficial"] = str(gab_result).upper()
        enhanced["anulada"] = result.get("anulada", questao.get("anulada", False))

        if "alternativas" in result and isinstance(result["alternativas"], list) and len(result["alternativas"]) > 0:
            alts_cleaned = []
            for alt in result["alternativas"]:
                letra = str(alt.get("letra", "")).upper()
                is_corr = alt.get("correta", False)
                if not is_corr and not enhanced["anulada"]:
                    is_corr = (letra == enhanced["gabaritoOficial"])
                alts_cleaned.append({
                    "letra": letra,
                    "texto": alt.get("texto", "").strip(),
                    "correta": is_corr
                })
            enhanced["alternativas"] = alts_cleaned

        enhanced["aiAudit"] = {
            "modelUsed": model_used,
            "confianca": float(result.get("confianca", 0.98)),
            "statusRevisao": result.get("statusRevisao", "APROVADO_AUTO"),
            "motivosRevisao": result.get("motivosRevisao", []),
            "melhoriasAplicadas": result.get("melhoriasAplicadas", []),
            "timestamp": int(time.time())
        }

        return enhanced

    def batch_enhance_questions(self, questoes, metadata=None, max_workers=2):
        """
        Processa uma lista de questões em paralelo com controle de concorrência.
        """
        if not questoes:
            return []

        total = len(questoes)
        results = [None] * total

        def _process_single(idx, q):
            pos = q.get("posicao", idx + 1)
            time.sleep((idx % 2) * 0.5)
            try:
                res = self.enhance_and_audit_question(q, metadata)
                return idx, res
            except Exception as exc:
                fallback_q = dict(q)
                fallback_q["aiAudit"] = {
                    "modelUsed": "fallback",
                    "confianca": 0.0,
                    "statusRevisao": "PENDENTE_REVISAO",
                    "motivosRevisao": [f"Erro na IA: {str(exc)}"],
                    "melhoriasAplicadas": []
                }
                return idx, fallback_q

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(_process_single, idx, q)
                for idx, q in enumerate(questoes)
            ]
            for future in as_completed(futures):
                idx, q_res = future.result()
                results[idx] = q_res

        return results

    def _create_pdf_slice_b64(self, reader, start_page, end_page):
        """Gera um mini PDF em Base64 para o intervalo de páginas selecionado."""
        writer = pypdf.PdfWriter()
        for p in range(start_page, min(end_page + 1, len(reader.pages))):
            writer.add_page(reader.pages[p])
        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")

    def extract_pdf_with_gemini(self, pdf_path, gabarito_map=None, metadata=None, log_callback=None):
        """
        Extrai todas as questões do caderno de prova em PDF utilizando Ingestão Integral Direta
        (Visão Global do documento completo), preservando integralmente textos de apoio compartilhados
        e enunciados que cruzam páginas, sem nenhum corte ou perda de contexto.
        """
        gabarito_map = gabarito_map or {}
        metadata = metadata or {}
        banca = metadata.get("banca", "OUTRA")
        cargo = metadata.get("cargo", "PROVA")
        ano = int(metadata.get("ano", 2025)) if str(metadata.get("ano", "")).isdigit() else 2025
        fonte = metadata.get("fonte", "CONCURSO")

        reader = pypdf.PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"\n=======================================================", flush=True)
        print(f"[*] [Gemini PDF Extractor] Ingestão Integral Direta de {total_pages} páginas (Visão Global)...", flush=True)
        print(f"=======================================================", flush=True)

        if log_callback:
            log_callback(f"Enviando caderno integral ({total_pages} páginas) para IA (Visão Global)...", "info")

        with open(pdf_path, "rb") as f:
            pdf_full_b64 = base64.b64encode(f.read()).decode("utf-8")

        prompt_full = f"""Extraia com precisão máxima TODAS as questões objetivas de concurso/vestibular presentes neste caderno de prova integral ({total_pages} páginas).
Banca: {banca} | Cargo: {cargo} | Ano: {ano}

DIRETRIZES FUNDAMENTAIS DE EXTRAÇÃO COMPLETA:
1. EXTRAIA 100% DAS QUESTÕES DO CADERNO INTEIRO (DA QUESTÃO 01 ATÉ A ÚLTIMA QUESTÃO):
   - Percorra TODAS as {total_pages} páginas da primeira à última.
   - NUNCA pare na primeira matéria nem após as primeiras páginas.
   - Extraia as questões de TODAS as disciplinas presentes na prova (Língua Portuguesa, Matemática/RLM, História, Geografia, Legislação, Noções de Direito, Conhecimentos Gerais e Específicos).
   - Se as páginas iniciais contiverem capa, instruções ou proposta de redação, ignore a redação e inicie a extração na primeira questão objetiva (Questão 01) e prossiga continuamente até o fim da prova.

2. TEXTOS DE APOIO / TEXTOS-BASE (REGRA DE OURO - NÃO PERDER):
   - Qualquer texto literário, artigo, fragmento ou crônica que sirva de base para um grupo de questões (ex: 'Considere o texto para responder às questões de 1 a 5') DEVE ser copiado integralmente no campo 'textoBase' de CADA UMA das questões correspondentes.
   - ATENÇÃO: Cada questão é exibida de forma independente na plataforma — o aluno pode acessar qualquer questão diretamente. Por isso, o textoBase NUNCA pode estar ausente em uma questão que depende dele.

3. DESTAQUES TIPOGRÁFICOS:
   - Termos sublinhados DEVEM usar <u>...</u>.
   - Termos em negrito DEVEM usar **...**.

4. CLASSIFICAÇÃO CANÔNICA DE MATÉRIAS:
   - Se o texto/questão for em inglês ➔ 'materiaNome': "Inglês".
   - Se for em espanhol ➔ 'materiaNome': "Espanhol".
   - Se for Língua Portuguesa ou Literatura ➔ 'materiaNome': "Língua Portuguesa".
   - Se não houver cabeçalho explícito de matéria ou se houver dúvida ➔ 'materiaNome': null (a IA da plataforma fará a classificação global).

5. IMAGENS E FIGURAS:
   - Se a questão contiver imagem, gráfico, mapa ou tirinha, marque 'temImagem': true e descreva em 'descricaoImagem'.

6. GABARITO OFICIAL:
   - Se a alternativa correta estiver anotada/visível no caderno, preencha 'gabaritoOficial' e marque 'correta': true."""

        payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_INSTRUCTION_EXTRACTOR}]
            },
            "contents": [
                {
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": "application/pdf",
                                "data": pdf_full_b64
                            }
                        },
                        {
                            "text": prompt_full
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "response_schema": QUESTION_EXTRACTION_SCHEMA,
                "temperature": 0.0,
                "maxOutputTokens": 65536
            }
        }

        t0 = time.time()
        print(f"[*] [Gemini Extractor] Enviando caderno completo ({total_pages} páginas) para o Gemini...", flush=True)
        raw_text, model_used = self._call_gemini_with_fallback(payload, timeout=240, log_callback=log_callback)
        duration = time.time() - t0
        print(f"[OK] [Gemini Extractor] Resposta global recebida em {duration:.2f}s via {model_used}!", flush=True)
        if log_callback:
            log_callback(f"✓ Resposta global recebida em {duration:.1f}s via {model_used}!", "success")

        cleaned = self._clean_json_text(raw_text)
        questoes_raw = json.loads(cleaned)

        if not isinstance(questoes_raw, list):
            questoes_raw = [questoes_raw]

        payload_final = []
        banca_clean = re.sub(r'[^A-Z0-9]', '', banca.upper()) or "GEN"
        cargo_clean = re.sub(r'[^A-Z0-9]', '_', cargo.upper())[:15] if cargo else "PROVA"

        for q in questoes_raw:
            pos = int(q.get("posicao", len(payload_final) + 1))
            pos_str = f"{pos:02d}"
            id_origem = f"{banca_clean}_{ano}_{cargo_clean}_Q{pos_str}"

            gab_oficial = gabarito_map.get(pos) or q.get("gabaritoOficial")
            if gab_oficial:
                gab_oficial = str(gab_oficial).strip().upper()

            alternativas = []
            for alt in q.get("alternativas", []):
                letra = str(alt.get("letra", "")).strip().upper()
                is_correta = bool(alt.get("correta", False))
                if gab_oficial and letra == gab_oficial:
                    is_correta = True
                alternativas.append({
                    "letra": letra,
                    "texto": str(alt.get("texto", "")).strip(),
                    "correta": is_correta
                })

            payload_final.append({
                "idOrigem": id_origem,
                "posicao": pos,
                "fonte": fonte,
                "banca": banca,
                "orgao": metadata.get("orgao"),
                "cargo": cargo,
                "ano": ano,
                "materiaNome": q.get("materiaNome"),
                "assunto": q.get("assunto"),
                "textoBase": q.get("textoBase"),
                "textoApoio": q.get("textoBase"),
                "enunciado": q.get("enunciado", ""),
                "imagemUrl": None,
                "temImagem": bool(q.get("temImagem", False)),
                "descricaoImagem": q.get("descricaoImagem"),
                "gabaritoOficial": gab_oficial,
                "anulada": bool(q.get("anulada", False) or gab_oficial in ["*", "X", "T", "ANULADA"]),
                "alternativas": alternativas,
                "aiAudit": {
                    "modelUsed": f"{model_used}-full-document",
                    "confianca": 1.0,
                    "statusRevisao": "APROVADO_AUTO",
                    "motivosRevisao": [],
                    "melhoriasAplicadas": ["Ingestão Integral Direta em PDF com Visão Global e Structured Outputs"]
                }
            })

        payload_final.sort(key=lambda x: x["posicao"])
        print(f"\n[✓] [Gemini PDF Extractor] Processamento finalizado com sucesso! Total: {len(payload_final)} questões consolidadas de 1 a {len(payload_final)}.\n", flush=True)
        return payload_final

    def extract_missing_questions(self, pdf_path, missing_positions, gabarito_map=None, metadata=None, log_callback=None):
        """
        Extrai especificamente as questões cujas posições estão faltando em uma extração prévia.
        Usado pela esteira de auto-continuação para preencher gaps detectados pelo Python.
        A LLM recebe o PDF completo + lista exata de questões a extrair, sendo totalmente
        responsável pelo conteúdo (enunciado, alternativas, textoBase) de cada questão.
        """
        gabarito_map = gabarito_map or {}
        metadata = metadata or {}
        banca = metadata.get("banca", "OUTRA")
        cargo = metadata.get("cargo", "PROVA")
        ano = int(metadata.get("ano", 2025)) if str(metadata.get("ano", "")).isdigit() else 2025
        fonte = metadata.get("fonte", "CONCURSO")

        if not missing_positions:
            return []

        reader = pypdf.PdfReader(pdf_path)
        total_pages = len(reader.pages)

        faltantes_sorted = sorted(missing_positions)
        faltantes_str = ", ".join(str(p) for p in faltantes_sorted)
        preview = faltantes_str[:100] + ("..." if len(faltantes_str) > 100 else "")

        if log_callback:
            log_callback(f"Auto-continuação: buscando {len(faltantes_sorted)} questões faltantes [{preview}]...", "warning")

        with open(pdf_path, "rb") as f:
            pdf_full_b64 = base64.b64encode(f.read()).decode("utf-8")

        prompt_continuacao = f"""CONTINUAÇÃO DE EXTRAÇÃO — Questões Específicas Faltantes
Banca: {banca} | Cargo: {cargo} | Ano: {ano} | Caderno: {total_pages} páginas

Este caderno já foi parcialmente processado. Extraia SOMENTE as questões com os seguintes números:

QUESTÕES A EXTRAIR AGORA: {faltantes_str}

REGRAS OBRIGATÓRIAS DESTA CONTINUAÇÃO:
1. Localize cada número da lista acima no caderno pelo cabeçalho de questão (ex: "QUESTÃO 6", "6.", etc.).
2. Extraia integralmente: enunciado, todas as alternativas, e textoBase completo se a questão depender de texto de apoio.
3. NÃO extraia questões com números que não estejam na lista acima. Apenas as listadas.
4. Se um número da lista não existir no PDF, simplesmente ignore-o — não invente questões.
5. Alternativas numeradas 01/02/03/04/05 devem ser mapeadas para A/B/C/D/E respectivamente.
6. O campo 'posicao' deve conter o número exato da questão conforme aparece no caderno."""

        payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_INSTRUCTION_EXTRACTOR}]
            },
            "contents": [
                {
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": "application/pdf",
                                "data": pdf_full_b64
                            }
                        },
                        {
                            "text": prompt_continuacao
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "response_schema": QUESTION_EXTRACTION_SCHEMA,
                "temperature": 0.0,
                "maxOutputTokens": 65536
            }
        }

        t0 = time.time()
        print(f"[*] [Auto-Continuação] Buscando questões: {faltantes_str[:80]}...", flush=True)
        raw_text, model_used = self._call_gemini_with_fallback(payload, timeout=240, log_callback=log_callback)
        duration = time.time() - t0
        print(f"[OK] [Auto-Continuação] Resposta recebida em {duration:.2f}s via {model_used}!", flush=True)
        if log_callback:
            log_callback(f"✓ Resposta de continuação em {duration:.1f}s via {model_used}!", "success")

        cleaned = self._clean_json_text(raw_text)
        questoes_raw = json.loads(cleaned)

        if not isinstance(questoes_raw, list):
            questoes_raw = [questoes_raw]

        payload_final = []
        banca_clean = re.sub(r'[^A-Z0-9]', '', banca.upper()) or "GEN"
        cargo_clean = re.sub(r'[^A-Z0-9]', '_', cargo.upper())[:15] if cargo else "PROVA"

        for q in questoes_raw:
            pos = int(q.get("posicao", 0))
            if pos == 0:
                continue

            pos_str = f"{pos:02d}"
            id_origem = f"{banca_clean}_{ano}_{cargo_clean}_Q{pos_str}"

            gab_oficial = gabarito_map.get(pos) or q.get("gabaritoOficial")
            if gab_oficial:
                gab_oficial = str(gab_oficial).strip().upper()

            alternativas = []
            for alt in q.get("alternativas", []):
                letra = str(alt.get("letra", "")).strip().upper()
                is_correta = bool(alt.get("correta", False))
                if gab_oficial and letra == gab_oficial:
                    is_correta = True
                alternativas.append({
                    "letra": letra,
                    "texto": str(alt.get("texto", "")).strip(),
                    "correta": is_correta
                })

            payload_final.append({
                "idOrigem": id_origem,
                "posicao": pos,
                "fonte": fonte,
                "banca": banca,
                "orgao": metadata.get("orgao"),
                "cargo": cargo,
                "ano": ano,
                "materiaNome": q.get("materiaNome"),
                "assunto": q.get("assunto"),
                "textoBase": q.get("textoBase"),
                "textoApoio": q.get("textoBase"),
                "enunciado": q.get("enunciado", ""),
                "imagemUrl": None,
                "temImagem": bool(q.get("temImagem", False)),
                "descricaoImagem": q.get("descricaoImagem"),
                "gabaritoOficial": gab_oficial,
                "anulada": bool(q.get("anulada", False) or gab_oficial in ["*", "X", "T", "ANULADA"]),
                "alternativas": alternativas,
                "aiAudit": {
                    "modelUsed": f"{model_used}-continuation",
                    "confianca": 1.0,
                    "statusRevisao": "APROVADO_AUTO",
                    "motivosRevisao": [],
                    "melhoriasAplicadas": ["Auto-Continuação por detecção de gaps"]
                }
            })

        print(f"[✓] [Auto-Continuação] {len(payload_final)} questões recuperadas neste pass.", flush=True)
        return payload_final

