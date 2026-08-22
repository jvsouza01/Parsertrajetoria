import os
import sys
import re
import json
import time
import base64
import tempfile
import shutil
import datetime
import threading
import subprocess
from flask import Flask, render_template, request, jsonify, Response
from parsers import ExamParserFactory, GabaritoExtractor
from services import GeminiService

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip()

load_env()

gemini_service = GeminiService()

base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
template_folder = os.path.join(base_dir, 'templates')
static_folder = os.path.join(base_dir, 'static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB max upload
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        res = Response()
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
        return res

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/favicon.ico')
def favicon():
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    if os.path.exists(icon_path):
        from flask import send_file
        return send_file(icon_path, mimetype='image/vnd.microsoft.icon')
    return Response(status=204)

@app.route('/')
def index():
    return render_template('index.html')

# =========================================================================
# ROTAS DE IMAGENS DE QUESTÕES (UPLOAD, PRINT / PASTE CTRL+V E SERVIÇO)
# =========================================================================

IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'output', 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

@app.route('/api/images/<filename>')
def serve_image(filename):
    from flask import send_from_directory
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/api/upload-image', methods=['POST'])
def upload_question_image():
    try:
        id_origem = request.form.get('idOrigem') or 'questao'
        id_clean = re.sub(r'[^A-Za-z0-9_]', '_', id_origem)
        
        # 1. Upload via arquivo multipart
        if 'image' in request.files:
            img_file = request.files['image']
            ext = os.path.splitext(img_file.filename)[1] or '.png'
            filename = f"{id_clean}_{int(time.time())}{ext}"
            file_path = os.path.join(IMAGES_DIR, filename)
            img_file.save(file_path)
            
            return jsonify({
                'success': True,
                'imagemUrl': f"images/{filename}",
                'previewUrl': f"/api/images/{filename}"
            })

        # 2. Upload via JSON Base64 (Ctrl+V / Printscreen)
        data = request.json or {}
        base64_data = data.get('image_base64', '')
        id_origem = data.get('idOrigem') or id_clean
        id_clean = re.sub(r'[^A-Za-z0-9_]', '_', id_origem)

        if base64_data:
            if ',' in base64_data:
                base64_data = base64_data.split(',')[1]
            img_bytes = base64.b64decode(base64_data)
            filename = f"{id_clean}_{int(time.time())}.png"
            file_path = os.path.join(IMAGES_DIR, filename)
            with open(file_path, 'wb') as f:
                f.write(img_bytes)

            return jsonify({
                'success': True,
                'imagemUrl': f"images/{filename}",
                'previewUrl': f"/api/images/{filename}"
            })

        return jsonify({'success': False, 'error': 'Nenhuma imagem enviada.'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



@app.route('/api/parse', methods=['POST'])
def parse_exam():
    try:
        if 'prova_pdf' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo de prova foi enviado.'}), 400

        prova_file = request.files['prova_pdf']
        gabarito_file = request.files.get('gabarito_pdf')
        gabarito_text = request.form.get('gabarito_text', '').strip()

        banca = request.form.get('banca', 'OUTRA')
        orgao = request.form.get('orgao', '')
        cargo = request.form.get('cargo', '')
        ano = request.form.get('ano', '2025')
        fonte = request.form.get('fonte', 'CONCURSO')

        metadata = {
            'banca': banca,
            'orgao': orgao,
            'cargo': cargo,
            'ano': ano,
            'fonte': fonte
        }

        # Salva prova temporariamente para leitura segura
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_prova:
            prova_file.save(tmp_prova.name)
            prova_tmp_path = tmp_prova.name

        gabarito_map = {}
        disciplina_map = {}

        # 1. Se foi enviado PDF de gabarito separado
        if gabarito_file and gabarito_file.filename:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_gab:
                gabarito_file.save(tmp_gab.name)
                gab_tmp_path = tmp_gab.name
            try:
                gabarito_map, disciplina_map = GabaritoExtractor.extract_from_pdf(gab_tmp_path)
            finally:
                if os.path.exists(gab_tmp_path):
                    try:
                        os.remove(gab_tmp_path)
                    except:
                        pass

        # 2. Se o usuário colou texto de gabarito
        if not gabarito_map and gabarito_text:
            gabarito_map, disc_text_map = GabaritoExtractor.extract_from_text(gabarito_text)
            if disc_text_map:
                disciplina_map.update(disc_text_map)

        try:
            parser = ExamParserFactory.get_parser(banca, metadata)
            questoes = parser.parse_pdf(prova_tmp_path, gabarito_map, disciplina_map)
        finally:
            if os.path.exists(prova_tmp_path):
                try:
                    os.remove(prova_tmp_path)
                except:
                    pass

        return jsonify({
            'success': True,
            'totalQuestoes': len(questoes),
            'banca': banca,
            'orgao': orgao,
            'cargo': cargo,
            'ano': ano,
            'gabaritosEncontrados': len(gabarito_map),
            'questoes': questoes
        })

    except Exception as e:
        print(f"[API Parse Error] {e}", file=sys.stderr)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/parse-gabarito', methods=['POST'])
def parse_gabarito_only():
    try:
        gabarito_file = request.files.get('gabarito_pdf')
        gabarito_text = request.form.get('gabarito_text', '').strip()

        gabarito_map = {}
        disciplina_map = {}

        if gabarito_file and gabarito_file.filename:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_gab:
                gabarito_file.save(tmp_gab.name)
                gab_tmp_path = tmp_gab.name
            try:
                gabarito_map, disciplina_map = GabaritoExtractor.extract_from_pdf(gab_tmp_path)
            finally:
                if os.path.exists(gab_tmp_path):
                    try:
                        os.remove(gab_tmp_path)
                    except:
                        pass
        elif gabarito_text:
            gabarito_map, disciplina_map = GabaritoExtractor.extract_from_text(gabarito_text)

        return jsonify({
            'success': True,
            'totalGabaritos': len(gabarito_map),
            'gabaritos': gabarito_map,
            'disciplinas': disciplina_map
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

import unicodedata

MATERIAS_CANONICAS_MAP = {
    # Português
    "portugues": "Língua Portuguesa",
    "lingua portuguesa": "Língua Portuguesa",
    "lingua portuguesa e literatura": "Língua Portuguesa",
    "gramatica": "Língua Portuguesa",
    "interpretacao de texto": "Língua Portuguesa",
    "literatura": "Língua Portuguesa",
    "literatura brasileira": "Língua Portuguesa",
    # Inglês
    "ingles": "Inglês",
    "lingua inglesa": "Inglês",
    "lingua estrangeira ingles": "Inglês",
    "lingua estrangeira - ingles": "Inglês",
    "lingua estrangeira (ingles)": "Inglês",
    "english": "Inglês",
    # Espanhol
    "espanhol": "Espanhol",
    "lingua espanhola": "Espanhol",
    "lingua estrangeira espanhol": "Espanhol",
    "lingua estrangeira - espanhol": "Espanhol",
    "lingua estrangeira (espanhol)": "Espanhol",
    "spanish": "Espanhol",
    # Matemática / RLM
    "matematica": "Matemática",
    "raciocinio logico": "Matemática",
    "raciocinio logico matematico": "Matemática",
    "matematica e rlm": "Matemática",
    "rlm": "Matemática",
    # História
    "historia": "História",
    "historia geral": "História",
    "historia do brasil": "História",
    "historia da bahia": "História",
    # Geografia
    "geografia": "Geografia",
    "geografia geral": "Geografia",
    "geografia do brasil": "Geografia",
    "geografia da bahia": "Geografia",
    # Ciências da Natureza
    "fisica": "Física",
    "quimica": "Química",
    "biologia": "Biologia",
    "ciencias biologicas": "Biologia",
    # Humanas
    "filosofia": "Filosofia",
    "sociologia": "Sociologia",
    # Direito
    "direito constitucional": "Direito Constitucional",
    "nocoes de direito constitucional": "Direito Constitucional",
    "direito administrativo": "Direito Administrativo",
    "nocoes de direito administrativo": "Direito Administrativo",
    "direito penal": "Direito Penal",
    "direito penal militar": "Direito Penal",
    "direito processual penal": "Direito Processual Penal",
    "processo penal": "Direito Processual Penal",
    "direito processual penal militar": "Direito Processual Penal",
    "legislacao institucional": "Legislação Institucional",
    "legislacao da pm-ba": "Legislação Institucional",
    "legislacao da pmba": "Legislação Institucional",
    "estatuto dos policiais militares": "Legislação Institucional",
    "direitos humanos": "Direito Constitucional",
    "nocoes de direito": "Direito Constitucional",
    "igualdade racial e de genero": "Legislação Institucional",
    # Informática
    "informatica": "Informática",
    "nocoes de informatica": "Informática",
    "tecnologia da informacao": "Informática",
    "ti": "Informática"
}

def normalize_text_key(s):
    if not s:
        return ""
    s = unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore').decode('utf-8')
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s.lower())
    return re.sub(r'\s+', ' ', s).strip()

_CANONICAL_LOOKUP = {
    normalize_text_key(k): v for k, v in MATERIAS_CANONICAS_MAP.items()
}

def normalize_canonical_materia(raw_name):
    if not raw_name:
        return None
    raw_str = str(raw_name).strip()
    if raw_str in ["", "null", "None", "undefined", "Geral", "GERAL", "[IA Automática (null)]"]:
        return None
    key = normalize_text_key(raw_str)
    if not key:
        return None
    return _CANONICAL_LOOKUP.get(key, raw_str)

def standardize_payload(questoes):
    """Garante que a lista de questões esteja 100% no padrão exato IngestaoQuestaoInput da API Trajetória."""
    clean_list = []
    for q in questoes:
        pos = int(q.get("posicao") or 1)
        banca = str(q.get("banca") or "OUTRA").strip()
        ano = int(q.get("ano") or 2025)
        cargo = str(q.get("cargo") or "").strip()
        orgao = str(q.get("orgao") or "").strip()
        fonte = str(q.get("fonte") or "CONCURSO").strip()
        
        banca_clean = re.sub(r'[^A-Z0-9]', '', banca.upper()) or "GEN"
        cargo_clean = re.sub(r'[^A-Z0-9]', '_', cargo.upper())[:15] if cargo else "PROVA"
        id_origem = q.get("idOrigem") or f"{banca_clean}_{ano}_{cargo_clean}_Q{pos:02d}"
        
        gabarito = str(q.get("gabaritoOficial") or "").strip().upper()
        is_anulada = bool(q.get("anulada", False) or gabarito in ["*", "X", "T", "ANULADA"])
        
        alternativas = []
        for alt in q.get("alternativas", []):
            if isinstance(alt, dict):
                letra = str(alt.get("letra", "")).strip().upper()
                texto = str(alt.get("texto", "")).strip()
                is_correta = False if is_anulada else (letra == gabarito)
                alternativas.append({
                    "letra": letra,
                    "texto": texto,
                    "correta": is_correta
                })
        
        enunciado = str(q.get("enunciado") or "").strip()
        texto_base = str(q.get("textoBase") or q.get("textoApoio") or "").strip()
        
        materia_norm = normalize_canonical_materia(q.get("materiaNome") or q.get("materia"))
        assunto_raw = str(q.get("assunto") or "").strip()
        
        clean_list.append({
            "idOrigem": id_origem,
            "posicao": pos,
            "fonte": fonte,
            "banca": banca,
            "orgao": orgao if orgao else None,
            "cargo": cargo if cargo else None,
            "ano": ano,
            "materiaNome": materia_norm,
            "assunto": assunto_raw if assunto_raw else None,
            "textoBase": texto_base if texto_base else None,
            "enunciado": enunciado,
            "imagemUrl": q.get("imagemUrl", None),
            "temImagem": bool(q.get("temImagem", False)),
            "descricaoImagem": q.get("descricaoImagem"),
            "gabaritoOficial": gabarito if not is_anulada else "*",
            "anulada": is_anulada,
            "alternativas": alternativas
        })
    return clean_list

@app.route('/api/export-json', methods=['POST'])
def export_json():
    try:
        data = request.json or {}
        raw_questoes = data.get('questoes', [])
        filename = data.get('filename', 'questoes_trajetoria_payload.json')
        
        questoes = standardize_payload(raw_questoes)
        json_bytes = json.dumps(questoes, ensure_ascii=False, indent=2).encode('utf-8')
        
        return Response(
            json_bytes,
            mimetype="application/json",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =========================================================================
# ROTAS DE INTELIGÊNCIA ARTIFICIAL (GOOGLE GEMINI COM RESILIÊNCIA & CASCATA)
# =========================================================================

@app.route('/api/ai/test-key', methods=['POST'])
def ai_test_key():
    try:
        data = request.json or {}
        api_key = data.get('api_key') or gemini_service.api_key
        svc = GeminiService(api_key=api_key)
        
        # Teste leve de conectividade
        payload = {
            "contents": [{"parts": [{"text": "Responda em JSON: {\"status\": \"ok\"}"}]}],
            "generationConfig": {"response_mime_type": "application/json", "temperature": 0.1}
        }
        raw_text, model_used = svc._call_gemini_with_fallback(payload)
        return jsonify({
            'success': True,
            'model': model_used,
            'message': f'Conexão com a API do Gemini estabelecida com sucesso via {model_used}!'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/ai/enhance-question', methods=['POST'])
def ai_enhance_question():
    try:
        data = request.json or {}
        questao = data.get('questao')
        if not questao:
            return jsonify({'success': False, 'error': 'Questão não fornecida.'}), 400

        metadata = data.get('metadata', {})
        api_key = data.get('api_key')
        svc = GeminiService(api_key=api_key) if api_key else gemini_service

        enhanced_q = svc.enhance_and_audit_question(questao, metadata)
        return jsonify({
            'success': True,
            'questao': enhanced_q
        })
    except Exception as e:
        print(f"[AI Enhance Error] {e}", file=sys.stderr)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ai/batch-enhance', methods=['POST'])
def ai_batch_enhance():
    try:
        data = request.json or {}
        questoes = data.get('questoes', [])
        if not questoes:
            return jsonify({'success': False, 'error': 'Lista de questões vazia.'}), 400

        metadata = data.get('metadata', {})
        api_key = data.get('api_key')
        svc = GeminiService(api_key=api_key) if api_key else gemini_service

        enhanced_list = svc.batch_enhance_questions(questoes, metadata, max_workers=10)
        return jsonify({
            'success': True,
            'total': len(enhanced_list),
            'questoes': enhanced_list
        })
    except Exception as e:
        print(f"[AI Batch Error] {e}", file=sys.stderr)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ai/parse-pdf', methods=['POST'])
def ai_parse_pdf():
    try:
        if 'prova_pdf' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo de prova foi enviado.'}), 400

        prova_file = request.files['prova_pdf']
        gabarito_file = request.files.get('gabarito_pdf')
        gabarito_text = request.form.get('gabarito_text', '').strip()

        banca = request.form.get('banca', 'OUTRA')
        orgao = request.form.get('orgao', '')
        cargo = request.form.get('cargo', '')
        ano = request.form.get('ano', '2025')
        fonte = request.form.get('fonte', 'CONCURSO')
        api_key = request.form.get('api_key')

        metadata = {
            'banca': banca,
            'orgao': orgao,
            'cargo': cargo,
            'ano': ano,
            'fonte': fonte
        }

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_prova:
            prova_file.save(tmp_prova.name)
            prova_tmp_path = tmp_prova.name

        gabarito_map = {}
        disciplina_map = {}

        if gabarito_file and gabarito_file.filename:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_gab:
                gabarito_file.save(tmp_gab.name)
                gab_tmp_path = tmp_gab.name
            try:
                gabarito_map, disciplina_map = GabaritoExtractor.extract_from_pdf(gab_tmp_path)
            finally:
                if os.path.exists(gab_tmp_path):
                    try:
                        os.remove(gab_tmp_path)
                    except:
                        pass
        elif gabarito_text:
            gabarito_map, disciplina_map = GabaritoExtractor.extract_from_text(gabarito_text)

        try:
            svc = GeminiService(api_key=api_key) if api_key else gemini_service
            questoes = svc.extract_pdf_with_gemini(prova_tmp_path, gabarito_map, metadata)
        finally:
            if os.path.exists(prova_tmp_path):
                try:
                    os.remove(prova_tmp_path)
                except:
                    pass

        return jsonify({
            'success': True,
            'totalQuestoes': len(questoes),
            'banca': banca,
            'orgao': orgao,
            'cargo': cargo,
            'ano': ano,
            'gabaritosEncontrados': len(gabarito_map),
            'questoes': questoes
        })
    except Exception as e:
        print(f"[AI Parse PDF Error] {e}", file=sys.stderr)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==============================================================================
# ESTEIRA DE PROCESSAMENTO CONTÍNUO (PILOTO AUTOMÁTICO / FOLDER WATCHER)
# ==============================================================================
class BatchWatcherWorker:
    def __init__(self):
        self.is_running = False
        self.watch_folder = ""
        self.output_folder = ""
        self.processed_folder = ""
        self.thread = None
        self.logs = []
        self.stats = {
            "provas_processadas": 0,
            "questoes_extraidas": 0,
            "erros": 0
        }
        self.active_file = None
        self.lock = threading.Lock()

    def add_log(self, msg, level="info"):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entry = {"time": timestamp, "msg": msg, "level": level}
        with self.lock:
            self.logs.append(entry)
            if len(self.logs) > 300:
                self.logs.pop(0)
        print(f"[{timestamp}] [Esteira] {msg}", flush=True)

    def start(self, watch_folder, output_folder=None, api_key=None):
        if self.is_running:
            return False, "A esteira já está em execução."
        
        self.watch_folder = os.path.abspath(watch_folder)
        if not os.path.exists(self.watch_folder):
            try:
                os.makedirs(self.watch_folder, exist_ok=True)
            except Exception as e:
                return False, f"Não foi possível acessar ou criar a pasta: {e}"

        self.output_folder = os.path.abspath(output_folder or os.path.join(self.watch_folder, "saida_json"))
        self.processed_folder = os.path.abspath(os.path.join(self.watch_folder, "processadas"))
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)

        self.api_key = api_key or gemini_service.api_key
        self.is_running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        self.add_log(f"Esteira iniciada com sucesso! Monitorando: {self.watch_folder}", "success")
        return True, "Esteira iniciada com sucesso!"

    def stop(self):
        if not self.is_running:
            return False, "A esteira já está parada."
        self.is_running = False
        self.active_file = None
        self.add_log("Comando de parada recebido. Encerrando ciclo da esteira...", "warning")
        return True, "Esteira parada com sucesso."

    @staticmethod
    def _find_matching_gabarito(prova_file, candidate_files):
        stop_words = {"prova", "provas", "pv", "caderno", "impresso", "gabarito", "gabaritos", "gb", "de", "da", "do", "das", "dos", "e", "em", "para", "pdf", "concurso"}
        def tokenize(filename):
            name = os.path.splitext(filename)[0].lower()
            raw_tokens = re.split(r'[-_\s\.]+', name)
            return {t for t in raw_tokens if len(t) > 1 and t not in stop_words}

        prova_tokens = tokenize(prova_file)
        if not prova_tokens:
            return None

        best_match = None
        best_score = 0.0

        for candidate in candidate_files:
            if candidate == prova_file:
                continue
            if not re.search(r'gabarito|gb|gabaritos', candidate, re.IGNORECASE):
                continue

            cand_tokens = tokenize(candidate)
            if not cand_tokens:
                continue

            intersection = prova_tokens.intersection(cand_tokens)
            union = prova_tokens.union(cand_tokens)
            score = len(intersection) / len(union) if union else 0.0

            if (len(intersection) >= 2 and score >= 0.35) or score >= 0.5:
                if score > best_score:
                    best_score = score
                    best_match = candidate

        return best_match

    @staticmethod
    def _detect_metadata_from_filename(filename):
        lower = filename.lower()
        bancas = [
            ("AOCP", r'aocp|instituto[-\s_]*aocp'),
            ("CEBRASPE", r'cebraspe|cespe'),
            ("FGV", r'fgv'),
            ("VUNESP", r'vunesp'),
            ("FCC", r'fcc|fundacao[-\s_]*carlos[-\s_]*chagas'),
            ("IBFC", r'ibfc'),
            ("UNEB", r'uneb'),
            ("IDECAN", r'idecan'),
            ("QUADRIX", r'quadrix'),
            ("CONSULPLAN", r'consulplan'),
            ("CONSULTEC", r'consultec|aietec'),
        ]
        banca = "OUTRA"
        for b_name, pattern in bancas:
            if re.search(pattern, lower):
                banca = b_name
                break

        ano_match = re.search(r'20\d{2}', filename)
        ano = int(ano_match.group(0)) if ano_match else 2025

        cargo = "PROVA"
        if "aluno_soldado" in lower or "aluno-soldado" in lower or "aluno soldado" in lower:
            cargo = "Aluno Soldado"
        elif "soldado" in lower:
            cargo = "Soldado"
        elif "oficial" in lower:
            cargo = "Oficial"
        elif "agente" in lower:
            cargo = "Agente de Polícia"
        elif "investigador" in lower:
            cargo = "Investigador"
        elif "escrivao" in lower or "escrivão" in lower:
            cargo = "Escrivão"
        elif "delegado" in lower:
            cargo = "Delegado"
        elif "perito" in lower:
            cargo = "Perito"

        orgao = None
        if "pm-ba" in lower or "pmba" in lower or "policia_militar_da_bahia" in lower or "policia militar da bahia" in lower:
            orgao = "PM-BA"
        elif "pc-ba" in lower or "pcba" in lower or "policia_civil_da_bahia" in lower:
            orgao = "PC-BA"
        elif "pc-go" in lower or "pcgo" in lower or "policia_civil_de_goias" in lower:
            orgao = "PC-GO"
        elif "pm-go" in lower or "pmgo" in lower:
            orgao = "PM-GO"

        return {
            "banca": banca,
            "ano": ano,
            "cargo": cargo,
            "orgao": orgao,
            "fonte": "CONCURSO"
        }

    def _auto_continue_extraction(self, svc, prova_path, questoes_iniciais, gabarito_map, metadata, max_passes=6):
        """
        Detecta gaps na extração inicial e dispara passes de auto-continuação
        até obter todas as questões esperadas ou esgotar o limite de tentativas.
        Python é responsável por detectar o que falta; a LLM é responsável
        pelo conteúdo completo de cada questão na continuação.
        """
        import pypdf

        questoes_by_pos = {q['posicao']: q for q in questoes_iniciais}
        total_esperado = len(gabarito_map) if gabarito_map else None

        try:
            reader = pypdf.PdfReader(prova_path)
            total_pages = len(reader.pages)
        except Exception:
            total_pages = 0

        for pass_num in range(1, max_passes + 1):
            extracted_positions = set(questoes_by_pos.keys())
            if not extracted_positions:
                break

            max_pos = max(extracted_positions)
            faltantes = []

            if total_esperado:
                # Com gabarito: sabemos exatamente quais posições devem existir
                faltantes = [p for p in range(1, total_esperado + 1) if p not in extracted_positions]
            else:
                # Sem gabarito separado (ex: vestibulares UESB, UNEC):
                # 1. Primeiro preenche qualquer gap interno em 1..max_pos
                gaps_internos = [p for p in range(1, max_pos + 1) if p not in extracted_positions]
                if gaps_internos:
                    faltantes = gaps_internos
                else:
                    # 2. Se não há gaps internos, sonda ativamente as próximas 30 questões além do max_pos
                    # O loop encerra naturalmente quando o modelo não encontrar mais questões novas (fim do caderno)
                    faltantes = list(range(max_pos + 1, max_pos + 31))

            if not faltantes:
                break

            # Limita cada pass a no máximo 30 questões para evitar timeout em provas pesadas
            MAX_BATCH_PER_PASS = 30
            batch_faltantes = faltantes[:MAX_BATCH_PER_PASS]

            if total_esperado:
                self.add_log(
                    f"⚠ Extração parcial: {len(extracted_positions)}/{total_esperado} questões. "
                    f"Faltam {len(faltantes)} posições. Continuação {pass_num}/{max_passes} (batch de {len(batch_faltantes)})...", "warning"
                )
            else:
                self.add_log(
                    f"⚠ Extração parcial: {len(extracted_positions)} questões / {total_pages} páginas. "
                    f"Buscando {len(batch_faltantes)} posições adicionais. Pass {pass_num}/{max_passes}...", "warning"
                )

            try:
                continuacao = svc.extract_missing_questions(
                    prova_path, batch_faltantes, gabarito_map, metadata, log_callback=self.add_log
                )
            except Exception as e:
                self.add_log(f"Erro no pass de continuação {pass_num}: {e}", "error")
                break

            if not continuacao:
                self.add_log(f"Pass {pass_num}: nenhuma questão adicional encontrada. Finalizando.", "info")
                break

            # Merge: posições da continuação têm prioridade (extração mais direcionada)
            novas_posicoes = set()
            for q in continuacao:
                pos = q['posicao']
                if pos not in questoes_by_pos:
                    novas_posicoes.add(pos)
                questoes_by_pos[pos] = q

            self.add_log(
                f"✓ Pass {pass_num}: {len(continuacao)} questões recuperadas "
                f"({len(novas_posicoes)} posições novas).", "success"
            )

            if not novas_posicoes:
                break  # Sem progresso real

            if self.is_running and pass_num < max_passes:
                time.sleep(4)  # Pausa entre passes para respeitar rate limit

        resultado = sorted(questoes_by_pos.values(), key=lambda x: x['posicao'])

        if total_esperado:
            if len(resultado) >= total_esperado:
                self.add_log(f"✓ Auto-continuação completa: {len(resultado)}/{total_esperado} questões!", "success")
            else:
                self.add_log(
                    f"⚠ Auto-continuação encerrada: {len(resultado)}/{total_esperado} questões obtidas.", "warning"
                )

        return resultado

    def _run_loop(self):
        while self.is_running:
            try:
                all_files = [f for f in os.listdir(self.watch_folder) if f.lower().endswith('.pdf') and os.path.isfile(os.path.join(self.watch_folder, f))]
                provas = [f for f in all_files if not re.search(r'gabarito|gb|gabaritos', f, re.IGNORECASE)]
                
                if not provas:
                    time.sleep(3)
                    continue

                for prova_file in provas:
                    if not self.is_running:
                        break

                    prova_path = os.path.join(self.watch_folder, prova_file)
                    if not os.path.exists(prova_path):
                        continue

                    self.active_file = prova_file
                    self.add_log(f"Iniciando processamento: {prova_file}", "info")

                    base_name = os.path.splitext(prova_file)[0]
                    gabarito_file = self._find_matching_gabarito(prova_file, all_files)

                    gabarito_map = {}
                    if gabarito_file:
                        gab_path = os.path.join(self.watch_folder, gabarito_file)
                        self.add_log(f"Gabarito oficial pareado: {gabarito_file}", "info")
                        try:
                            gabarito_map, _ = GabaritoExtractor.extract_from_pdf(gab_path)
                            self.add_log(f"{len(gabarito_map)} respostas extraídas da folha de gabarito.", "info")
                        except Exception as e:
                            self.add_log(f"Aviso ao ler folha de gabarito: {e}", "warning")
                    else:
                        self.add_log("Nenhum gabarito separado encontrado para esta prova. O Gemini buscará gabaritos embutidos no caderno.", "info")

                    try:
                        svc = GeminiService(api_key=self.api_key)
                        metadata = self._detect_metadata_from_filename(prova_file)

                        # PASS 1: Extração integral do caderno completo
                        questoes_raw = svc.extract_pdf_with_gemini(prova_path, gabarito_map, metadata, log_callback=self.add_log)

                        # AUTO-CONTINUAÇÃO: Detecta gaps e dispara passes direcionados até completar
                        questoes_raw = self._auto_continue_extraction(
                            svc, prova_path, questoes_raw, gabarito_map, metadata
                        )

                        questoes_standardized = standardize_payload(questoes_raw)

                        json_name = f"payload_{base_name}_{int(time.time())}.json"
                        json_path = os.path.join(self.output_folder, json_name)
                        with open(json_path, "w", encoding="utf-8") as jf:
                            json.dump(questoes_standardized, jf, ensure_ascii=False, indent=2)

                        with self.lock:
                            self.stats["provas_processadas"] += 1
                            self.stats["questoes_extraidas"] += len(questoes_standardized)

                        self.add_log(f"✓ SUCESSO! {len(questoes_standardized)} questões estruturadas em: {json_name}", "success")

                        try:
                            shutil.move(prova_path, os.path.join(self.processed_folder, prova_file))
                            if gabarito_file and os.path.exists(os.path.join(self.watch_folder, gabarito_file)):
                                shutil.move(os.path.join(self.watch_folder, gabarito_file), os.path.join(self.processed_folder, gabarito_file))
                        except Exception as mv_err:
                            self.add_log(f"Aviso ao mover arquivo processado: {mv_err}", "warning")

                    except Exception as parse_err:
                        with self.lock:
                            self.stats["erros"] += 1
                        self.add_log(f"✗ Erro ao processar {prova_file}: {parse_err}", "error")
                        try:
                            error_folder = os.path.join(self.watch_folder, "erros")
                            os.makedirs(error_folder, exist_ok=True)
                            shutil.move(prova_path, os.path.join(error_folder, prova_file))
                            if gabarito_file and os.path.exists(os.path.join(self.watch_folder, gabarito_file)):
                                shutil.move(os.path.join(self.watch_folder, gabarito_file), os.path.join(error_folder, gabarito_file))
                            self.add_log(f"Arquivo com falha movido para '{os.path.basename(error_folder)}/' para liberar a esteira.", "warning")
                        except Exception as mv_e:
                            pass

                    self.active_file = None
                    if self.is_running:
                        self.add_log("Pausa de 10s para respeitar limites da API...", "info")
                        time.sleep(10)

            except Exception as loop_err:
                self.add_log(f"Erro no loop da esteira: {loop_err}", "error")
                time.sleep(5)

        self.add_log("Esteira pausada / desligada.", "warning")

batch_watcher = BatchWatcherWorker()

@app.route('/api/batch/start', methods=['POST'])
def batch_start():
    data = request.get_json() or {}
    folder = data.get('folder', r'C:\Users\jao_v\Desktop\ProvasParser').strip()
    api_key = data.get('api_key')
    success, message = batch_watcher.start(folder, api_key=api_key)
    return jsonify({'success': success, 'message': message, 'running': batch_watcher.is_running})

@app.route('/api/batch/stop', methods=['POST'])
def batch_stop():
    success, message = batch_watcher.stop()
    return jsonify({'success': success, 'message': message, 'running': batch_watcher.is_running})

@app.route('/api/batch/status', methods=['GET'])
def batch_status():
    with batch_watcher.lock:
        return jsonify({
            'running': batch_watcher.is_running,
            'active_file': batch_watcher.active_file,
            'watch_folder': batch_watcher.watch_folder,
            'output_folder': batch_watcher.output_folder,
            'stats': dict(batch_watcher.stats),
            'logs': list(batch_watcher.logs)
        })

@app.route('/api/batch/open-folder', methods=['POST'])
def batch_open_folder():
    try:
        folder = batch_watcher.output_folder or os.path.abspath(r'C:\Users\jao_v\Desktop\ProvasParser\saida_json')
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        if sys.platform == 'win32':
            os.startfile(folder)
        else:
            subprocess.Popen(['xdg-open', folder])
        return jsonify({'success': True, 'folder': folder})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    port = int(os.environ.get('PORT', 5000))
    print(f"\n=======================================================")
    print(f"[*] Parser Trajetoria Studio Desktop!")
    print(f"-> Acesse no navegador: http://localhost:{port}")
    print(f"=======================================================\n")
    app.run(host='127.0.0.1', port=port, debug=False)
