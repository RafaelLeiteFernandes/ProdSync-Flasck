from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
import io

def generate_solicitation_pdf(solicitation_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20,
        rightMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,  # Center
        spaceAfter=12
    )
    subtitle_style = ParagraphStyle(
        name='SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=1,  # Center
        spaceAfter=12
    )
    h2_style = ParagraphStyle(
        name='H2Style',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12
    )
    normal_style = styles['Normal']
    normal_bold_style = ParagraphStyle(
        name='NormalBold',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    footer_style = ParagraphStyle(
        name='Footer',
        fontSize=10,
        leading=12,
        alignment=1,  # Center
        spaceBefore=20,
    )

    def add_solicitation_section(elements):
        # Cabeçalho com logo e título em um quadrado
        header_data = [
            [
                Image("reports/static/werner.png", width=80, height=30),
                Paragraph("Requisição de Retirada", title_style)
            ]
        ]
        header_table = Table(header_data, colWidths=[60, 440])
        header_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 12))

        # Dados da Solicitação
        elements.append(Paragraph("Dados da Solicitação", subtitle_style))
        
        data_elements = [
            Paragraph(f"Código: {solicitation_data.get('codigo', '')}", h2_style),
            Paragraph(f"Solicitante: {solicitation_data.get('usuario_nome', '')}", normal_style),
            Paragraph(f"Tipo de Retirada: {solicitation_data.get('tipo_retirada_nome', '')}", normal_style),
            Paragraph(f"Destino: {solicitation_data.get('destino_nome', '')}", normal_style),
            Paragraph(f"Observação: {solicitation_data.get('observacao', '')}", normal_style),
            Paragraph(f"Status: {solicitation_data.get('status', '')}", normal_style),
            Paragraph(f"Data da Solicitação: {solicitation_data.get('data_solicitacao', '')}", normal_style),
        ]
        
        data_table = Table([
            [data_elements[0], data_elements[1]],
            [data_elements[2], data_elements[3]],
            [data_elements[4], data_elements[5]],
            [data_elements[6]]
        ], colWidths=[250, 250])
        data_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        elements.append(data_table)
        elements.append(Spacer(1, 12))

        # Tabela para os itens da solicitação
        elements.append(Paragraph("Lista de Produtos", subtitle_style))
        elements.append(Spacer(1, 12))
        table_data = [["Código", "Produto / Descrição", "Quantidade"]]

        for item in solicitation_data['items']:
            row = [
                item['codpro'],
                item['produto_descricao'],
                item['quantidade']
            ]
            table_data.append(row)

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table = Table(table_data, style=table_style, colWidths=[100, 300, 100])
        elements.append(table)

        # Espaçamento para a próxima seção
        elements.append(Spacer(1, 48))

    # Adicionar apenas uma seção
    add_solicitation_section(elements)

    doc.build(elements)
    buffer.seek(0)
    return buffer