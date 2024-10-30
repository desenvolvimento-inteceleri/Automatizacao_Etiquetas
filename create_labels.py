from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER
import tempfile

paragraph_label_style = ParagraphStyle('paragraph labels style', 
  fontSize=10,
  borderPadding=5,
  alignment=TA_CENTER
)

# Função para desenhar uma etiqueta
def desenhar_etiqueta(c, x, y, largura, altura, tabela, logo, champioship, stage):
  c.rect(x, y, largura, altura) # DESENHA UM RETANGULO
  c.drawImage(logo, x + (largura - (85.9 * mm)) / 2, y + altura - 45, width=(85.9 * mm), height=(14.49 * mm))  # Ajuste o tamanho e a posição do logo conforme necessário
  p = Paragraph(f"""
    {champioship} <br/>\
    <b>{stage}</b> <br/>\
    DISTRITO: {tabela['DISTRITO']} <br/>\
    <b>ESCOLA: {tabela['NOME ESCOLA']}</b> <br/>\
    <b>{tabela['ATRIBUTO']} PROVAS: {tabela['TOTAL']}</b>
  """, paragraph_label_style)
  p.wrapOn(c, largura, altura - 60) # CALCULO PARA O TAMANHO DO QUADRADO PARA QUEBRAR LINHA
  p.drawOn(c, x, y + altura - 120)

def gerar_etiquetas(tabela, logo, championship, stage):
  # Configurações do PDF
  largura_pagina, altura_pagina = A4
  largura_etiqueta = 97 * mm
  altura_etiqueta = 55 * mm
  margem_horizontal = (largura_pagina - 2 * largura_etiqueta) / 3
  margem_vertical = (altura_pagina - 5 * altura_etiqueta) / 6

  # Criar o PDF
  c = canvas.Canvas("etiquetas.pdf", pagesize=A4)

  # Salvar o arquivo carregado em um arquivo temporário
  with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
    tmpfile.write(logo.getbuffer())
    logo_path = tmpfile.name

  # Desenhar etiquetas na página
  x = margem_horizontal
  y = altura_pagina - margem_vertical - altura_etiqueta

  for index, row in tabela.iterrows():
    desenhar_etiqueta(c, x, y, largura_etiqueta, altura_etiqueta, row, logo_path, championship, stage)
    x += largura_etiqueta + (3 * mm)
    if x + largura_etiqueta > largura_pagina:
      x = margem_horizontal
      y -= altura_etiqueta
      if y < margem_vertical:
        c.showPage()
        y = altura_pagina - margem_vertical - altura_etiqueta
  return c
  #c.save() # ISSO AQUI CRIA O ARQUIVO E SALVA NA TUA PASTA, MAS TU NÃO QUER SALVAR E SIM RETORNAR O "C" PARA QUE ELE SEJA ARMAZENADO LÁ NO OUTRO ARQUIVO, DENTRO DE UMA VARIAVEL, ENTÃO TU VAI RETORNAR USANDO O "RETURN C", OU SEJA "C" É A TUA VARIAVEL QUE É UM PDF E TU TA RETORNANDO ELA
  
