import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, send_file
from flask_cors import CORS
from reports.saida_report import generate_saida_pdf
from reports.pendencia_faturamento_report import generate_pendencia_faturamento_pdf
from reports.historico_report import generate_historico_pdf

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/report/saida', methods=['POST'])
def generate_saida_report():
    data = request.json
    buffer = generate_saida_pdf(data)
    return send_file(buffer, as_attachment=True, attachment_filename='saida_report.pdf', mimetype='application/pdf')

@app.route('/report/pendencia_faturamento', methods=['POST'])
def generate_pendencia_faturamento_report():
    data = request.json
    buffer = generate_pendencia_faturamento_pdf(data)
    return send_file(buffer, as_attachment=True, attachment_filename='pendencia_faturamento_report.pdf', mimetype='application/pdf')

@app.route('/report/historico', methods=['POST'])
def generate_historico_report():
    data = request.json
    buffer = generate_historico_pdf(data)
    return send_file(buffer, as_attachment=True, attachment_filename='historico_report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
