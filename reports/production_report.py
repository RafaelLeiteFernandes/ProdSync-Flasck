from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
import io
import pandas as pd

def create_bar_chart(data, categories):
    drawing = Drawing(500, 200)
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = data
    bc.categoryAxis.categoryNames = categories
    bc.bars[0].fillColor = colors.green
    bc.bars[1].fillColor = colors.red

    legend = Legend()
    legend.x = 350
    legend.y = 150
    legend.colorNamePairs = [(colors.green, "Produção"), (colors.red, "Média de Peso")]
    legend.fontName = "Helvetica"
    legend.fontSize = 12

    drawing.add(bc)
    drawing.add(legend)

    return drawing

def generate_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    elements = []

    # Cabeçalho
    logo_path = "reports/static/logo.png"  # Caminho para o logo
    logo = Image(logo_path, width=50, height=50)
    elements.append(logo)
    elements.append(Spacer(1, 12))
    
    header_style = ParagraphStyle(
        name='Header',
        fontSize=14,
        leading=16,
        alignment=1,  # Center
        spaceAfter=10,
    )
    header = Paragraph("Relatório de Produções", header_style)
    elements.append(header)

    # Data
    date_style = ParagraphStyle(
        name='Date',
        fontSize=10,
        leading=12,
        alignment=2,  # Right
    )
    date = Paragraph(f"Data: {data.get('date', 'N/A')}", date_style)
    elements.append(date)
    elements.append(Spacer(1, 12))  # Adicionar espaço

    # Agrupar dados por produto e calcular totais e médias
    df = pd.DataFrame(data['productions'])
    grouped = df.groupby('produto').agg({
        'produção': 'sum',
        'peso': 'mean',
        'cor': 'mean'
    }).reset_index()

    # Dados para o gráfico
    chart_data = [grouped['produção'].tolist(), grouped['peso'].tolist()]
    chart_categories = grouped['produto'].tolist()
    bar_chart = create_bar_chart(chart_data, chart_categories)
    elements.append(bar_chart)

    elements.append(Spacer(1, 24))  # Adicionar espaço

    # Tabela de Produções
    table_data = [["Produto", "Total Produção", "Média de Cor", "Média de Peso"]]
    for index, row in grouped.iterrows():
        table_data.append([
            row['produto'],
            row['produção'],
            f"{row['cor']:.2f}",  # Formatar média de cor com 2 casas decimais
            f"{row['peso']:.2f}"  # Formatar média de peso com 2 casas decimais
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
