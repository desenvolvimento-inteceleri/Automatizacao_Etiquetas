import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from .labels_peixe_boi import gerar_etiquetas

@st.cache_data
def convert_df(df: pd.DataFrame):
	return df.to_csv(index=False).encode('utf-8')

def main():
	st.subheader("Criação de Etiquetas - Peixe Boi")
	pd.options.mode.chained_assignment = None  
   
   # Caixa de seleção para criação de etiquetas para cada etapa do campeonato 
	opcao = st.selectbox(
     	label= 'Selecione uma opção para criar etiquetas', 
     	options=('1ª Etapa - Classificatoria', 'Paralimpiada', '3ª Semifinal - Semifinal'),
        index=None,
        placeholder='Selecione uma opção'
    )
 
	st.write('Você selecionou:', opcao)
 
	# Botão de upload do arquivo CSV
	uploaded_file = st.file_uploader("Carregar planilha CSV", type="csv")
	
	if uploaded_file is not None:
		labels_df = pd.read_csv(uploaded_file)		
		
		labels_df.rename(columns={
    	'Nome da escola': 'NOME ESCOLA',
      'EJA 1ªTOTALIDADE': 'EJA 1º ANO',
      'EJA 2ªTOTALIDADE': 'EJA 2º ANO',
      'EJA 3ªTOTALIDADE': 'EJA 3º ANO',
      'EJA 4ªTOTALIDADE': 'EJA 4º ANO',
	  '1ºano': '1º ANO',
	  '2ºano': '2º ANO',
	  '3ºano': '3º ANO',
	  '4ºano': '4º ANO',
	  '5ºano': '5º ANO',
	  '6ºano': '6º ANO',
	  '7ºano': '7º ANO',
	  '8ºano': '8º ANO',
      '9ºano': '9º ANO'
	  }, inplace=True)

		new_df = labels_df.loc[:, [
			'NOME ESCOLA',
			'1º ANO',
	        '2º ANO',
	        '3º ANO',
	        '4º ANO',
	        '5º ANO',
	        '6º ANO',
	        '7º ANO',
	        '8º ANO',
            '9º ANO',
			'EJA 1º ANO',
			'EJA 2º ANO',
			'EJA 3º ANO',
			'EJA 4º ANO',
		]]
		
		newnew_df = new_df.melt(id_vars=['NOME ESCOLA'], var_name='ANO ESCOLAR', value_name="TOTAL") # TRANSFORMA COLUNAS EM LINHAS
		clean_df = newnew_df.dropna() # RETIRA OS VALORES NULOS DA TABELA
		clean_df["TOTAL"] = pd.to_numeric(clean_df["TOTAL"], errors='coerce').astype(int) # TRANSFORMA OS VALORES DA COLUNA "TOTAL" EM INTEIROS
		clean_df = clean_df[clean_df["TOTAL"] != 0] # FILTRA A TABELA PARA MOSTRAR NA COLUNA TOTAL SOMENTE OS VALORES DIFERENTES DE 0
		
		# 	# Formatando o nome das Escolasde de forma que fiquem sem as siglas  
		clean_df["NOME ESCOLA"] = clean_df['NOME ESCOLA'].apply(lambda escola: ' '.join(escola.split(' ')[1:]))

		# # Formatanto todos os nomes das Escolas para caixa alta e deixando em ordem alfabetica
		clean_df["NOME ESCOLA"] = clean_df["NOME ESCOLA"].str.upper()
		clean_df = clean_df.sort_values(by='NOME ESCOLA')

		AgGrid(clean_df)
        
        # Função de download
		export_csv_file = convert_df(clean_df)

		# Botão de download após o tratamento da planilha
		st.download_button(
				label="Baixar Planilha Tratada",
				data=export_csv_file,
				file_name='ETIQUETAS_tratada.csv',
				mime='text/csv'
		)

		logo_file = st.file_uploader("Carregue a imagem da logo", type=["png", "jpg", "jpeg"])
		championship = st.text_input("Nome do Campeonato").upper()
		stage = st.text_input("Etapa").upper()
	
		if logo_file and championship and stage:
			st.download_button(
				label="Baixar PDF",
				data=gerar_etiquetas(tabela=clean_df, logo=logo_file, championship=championship, stage=stage),
				file_name='etiquetas_peixe_boi.pdf',
				mime='text/csv'
			)		    

if __name__ == "__main__":
	main()