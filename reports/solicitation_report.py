from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
import io

def generate_solicitation_pdf(solicitation_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    elements = []

    # Cabeçalho
    logo_path = "reports/static/logo.png"  # Caminho para o logo
    try:
        logo = Image(logo_path, width=50, height=50)
        elements.append(logo)
        elements.append(Spacer(1, 12))
    except IOError:
        print(f"Warning: Logo at {logo_path} not found, skipping logo.")
    
    header_style = ParagraphStyle(
        name='Header',
        fontSize=14,
        leading=16,
        alignment=1,  # Center
        spaceAfter=10,
    )
    header = Paragraph("Relatório de Solicitação", header_style)
    elements.append(header)

    # Data
    date_style = ParagraphStyle(
        name='Date',
        fontSize=10,
        leading=12,
        alignment=2,  # Right
    )
    date = Paragraph(f"Data: {solicitation_data.get('data_solicitacao', 'N/A')}", date_style)
    elements.append(date)
    elements.append(Spacer(1, 12))  # Adicionar espaço

    # Dados da Solicitação
    elements.append(Paragraph(f"Código: {solicitation_data.get('codigo', '')}", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f"Solicitante: {solicitation_data.get('usuario_nome', '')}", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f"Tipo de Retirada: {solicitation_data.get('tipo_retirada_nome', '')}", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f"Destino: {solicitation_data.get('destino_nome', '')}", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f"Observação: {solicitation_data.get('observacao', '')}", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f"Status: {solicitation_data.get('status', '')}", getSampleStyleSheet()['Normal']))
    elements.append(Spacer(1, 12))  # Adicionar espaço

    # Tabela de Itens da Solicitação
    table_data = [["Produto", "Quantidade", "Quantidade Separada", "Lote", "Data Fabricação", "Data Validade"]]
    for item in solicitation_data['items']:
        table_data.append([
            item['produto_descricao'],
            item['quantidade'],
            item['quantidade_separada'],
            item.get('lote', '-'),
            item.get('data_fab', '-'),
            item.get('data_vlt', '-')
        ])

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table = Table(table_data, style=table_style)
    elements.append(table)

    # Verificar se a tabela cabe na página, senão adicionar uma quebra de página
    if len(table_data) > 10:  # Ajustar esse valor conforme necessário
        elements.append(PageBreak())

    # Rodapé
    footer_style = ParagraphStyle(
        name='Footer',
        fontSize=10,
        leading=12,
        alignment=1,  # Center
        spaceBefore=20,
    )
    footer = Paragraph("Relatório gerado por [Nome da Empresa]", footer_style)
    elements.append(footer)

    doc.build(elements)
    buffer.seek(0)
    return buffer
