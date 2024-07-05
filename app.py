from flask import Flask, request, send_file
from flask_cors import CORS
from reports.production_report import generate_pdf

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todos os domínios

@app.route('/report/pdf', methods=['POST'])
def generate_report():
    data = request.json  # Dados enviados na requisição
    buffer = generate_pdf(data)
    return send_file(buffer, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
