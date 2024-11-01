from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER
import tempfile
import io

# Estilo do texto nas etiquetas
paragraph_label_style = ParagraphStyle(
    'paragraph labels style', 
    fontSize=10,
    borderPadding=5,
    alignment=TA_CENTER
)

# Função para desenhar uma única etiqueta
def desenhar_etiqueta(c, x, y, largura, altura, tabela, logo, championship, stage):
    # Definir a cor da borda para branco
    c.setStrokeColorRGB(1, 1, 1)  # Branco
    
    # Desenho do retângulo da etiqueta
    c.rect(x, y, largura, altura)
    
    # Inserção do logo
    c.drawImage(logo, x + (largura - (85.9 * mm)) / 2, y + altura - 45, width=(85.9 * mm), height=(14.49 * mm))
    
    # Texto da etiqueta
    p = Paragraph(f"""
        {championship} <br/>
        <b>{stage}</b> <br/>
        DISTRITO: {tabela['DISTRITO']} <br/>
        <b>ESCOLA: {tabela['NOME ESCOLA']}</b> <br/>
        <b>{tabela['ATRIBUTO']} PROVAS: {tabela['TOTAL']}</b>
    """, paragraph_label_style)
    
    # Ajuste do parágrafo dentro da etiqueta
    p.wrapOn(c, largura, altura - 60)
    p.drawOn(c, x, y + altura - 120)

# Função principal para gerar o PDF com as etiquetas
def gerar_etiquetas(tabela, logo, championship, stage):
    buffer = io.BytesIO()
    largura_pagina, altura_pagina = A4
    largura_etiqueta = 99 * mm
    altura_etiqueta = 55 * mm  # Ajuste para altura exata
    margem_topo = 9 * mm
    margem_lateral = 5 * mm
    espaco_vertical = 3 * mm  # Espaço vertical entre as colunas
    
    # Configuração do PDF
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Salvamento do logo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        tmpfile.write(logo.getbuffer())
        logo_path = tmpfile.name
    
    # Posições das colunas
    x_positions = [margem_lateral, largura_pagina / 2 + espaco_vertical / 2]
    y_position = altura_pagina - margem_topo - altura_etiqueta

    etiquetas_na_pagina = 0
    linha = 0
    
    for index, row in tabela.iterrows():
        for x in x_positions:
            desenhar_etiqueta(c, x, y_position, largura_etiqueta, altura_etiqueta, row, logo_path, championship, stage)
            etiquetas_na_pagina += 1
            
            # Verificar se alcançou 10 etiquetas e mudar para uma nova página
            if etiquetas_na_pagina >= 10:
                c.showPage()
                y_position = altura_pagina - margem_topo - altura_etiqueta
                etiquetas_na_pagina = 0
                linha = 0
                break
        
        # Ajuste de posição vertical após desenhar ambas as etiquetas da linha
        linha += 1
        if linha < 5:
            y_position -= altura_etiqueta
        else:
            linha = 0
            y_position = altura_pagina - margem_topo - altura_etiqueta

    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data
