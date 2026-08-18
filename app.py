import os
import sys
import json
import tempfile
from flask import Flask, render_template, request, jsonify, Response
from parsers import ExamParserFactory, GabaritoExtractor

# Suporte a empacotamento PyInstaller (sys._MEIPASS)
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    template_folder = os.path.join(base_dir, 'templates')
    static_folder = os.path.join(base_dir, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB max upload

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/api/export-json', methods=['POST'])
def export_json():
    try:
        data = request.json or {}
        questoes = data.get('questoes', [])
        filename = data.get('filename', 'questoes_trajetoria_payload.json')
        
        json_bytes = json.dumps(questoes, ensure_ascii=False, indent=2).encode('utf-8')
        
        return Response(
            json_bytes,
            mimetype="application/json",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n=======================================================")
    print(f"🚀 Parser Trajetória Studio Desktop!")
    print(f"👉 Acesse no navegador: http://localhost:{port}")
    print(f"=======================================================\n")
    app.run(host='127.0.0.1', port=port, debug=False)
