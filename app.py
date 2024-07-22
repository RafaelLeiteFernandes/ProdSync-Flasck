from flask import Flask, request, send_file
from flask_cors import CORS
from reports.production_report import generate_pdf
from reports.solicitation_report import generate_solicitation_pdf

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Permitir CORS para todas as origens

@app.route('/report/pdf', methods=['POST'])
def generate_report():
    data = request.json  # Dados enviados na requisição
    buffer = generate_pdf(data)
    return send_file(buffer, as_attachment=True, attachment_filename='report.pdf', mimetype='application/pdf')

@app.route('/report/solicitation', methods=['POST'])
def generate_solicitation_report():
    data = request.json  # Dados enviados na requisição
    buffer = generate_solicitation_pdf(data)
    return send_file(buffer, as_attachment=True, attachment_filename='solicitation_report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)