import os
import sys
import json
import tempfile
import requests
from flask import Flask, render_template, request, jsonify, send_file, Response
from parsers import ExamParserFactory, GabaritoExtractor

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
        dificuldade = request.form.get('dificuldade', 'FACIL')

        metadata = {
            'banca': banca,
            'orgao': orgao,
            'cargo': cargo,
            'ano': ano,
            'fonte': fonte,
            'dificuldade': dificuldade
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
                    os.remove(gab_tmp_path)

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
                os.remove(prova_tmp_path)

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
                    os.remove(gab_tmp_path)
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

@app.route('/api/send-backend', methods=['POST'])
def send_to_backend():
    try:
        data = request.json or {}
        questoes = data.get('questoes', [])
        api_url = data.get('apiUrl', 'http://localhost:8080/api/admin/ingestao/questoes').strip()
        token = data.get('token', '').strip()

        if not questoes:
            return jsonify({'success': False, 'error': 'Nenhuma questão para enviar.'}), 400

        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f"Bearer {token}" if not token.startswith('Bearer ') else token

        # Envia cada questão ou o lote completo
        success_count = 0
        failed_count = 0
        results = []

        # Tenta envio em lote primeiro
        try:
            resp = requests.post(api_url, json=questoes, headers=headers, timeout=15)
            if resp.status_code in [200, 201]:
                return jsonify({
                    'success': True,
                    'batch': True,
                    'message': f'Lote de {len(questoes)} questões enviado com sucesso!',
                    'status': resp.status_code,
                    'enviadas': len(questoes),
                    'falhas': 0
                })
        except Exception as e:
            print(f"[Batch Ingestion Failed, trying individual] {e}")

        # Se o backend não aceita array direto ou falhou, envia item por item
        for q in questoes:
            try:
                resp = requests.post(api_url, json=q, headers=headers, timeout=10)
                if resp.status_code in [200, 201]:
                    success_count += 1
                    results.append({'idOrigem': q.get('idOrigem'), 'status': 'OK', 'code': resp.status_code})
                else:
                    failed_count += 1
                    results.append({'idOrigem': q.get('idOrigem'), 'status': 'ERRO', 'code': resp.status_code, 'msg': resp.text[:200]})
            except Exception as ex:
                failed_count += 1
                results.append({'idOrigem': q.get('idOrigem'), 'status': 'ERRO', 'msg': str(ex)})

        return jsonify({
            'success': success_count > 0,
            'batch': False,
            'enviadas': success_count,
            'falhas': failed_count,
            'detalhes': results
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
    print(f"🚀 Parser Trajetória Studio iniciado!")
    print(f"👉 Acesse no navegador: http://localhost:{port}")
    print(f"=======================================================\n")
    app.run(host='0.0.0.0', port=port, debug=False)
