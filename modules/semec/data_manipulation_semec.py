import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

from .labels_semec import gerar_etiquetas

@st.cache_data
def convert_df(df: pd.DataFrame):
	return df.to_csv(index=False).encode('utf-8')

def main():
	st.subheader("Criação de Etiquetas - SEMEC")
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

		# Selecionando apenas as siglas dos dados na coluna de Distrito
		labels_df["Selecione abaixo a área administrativa da sua escola:"] = labels_df['Selecione abaixo a área administrativa da sua escola:'].apply(lambda polo: polo.split(' ')[-1].upper() if isinstance(polo, str) else polo)

		# Renomeando os indices da tabela 
		labels_df.rename(columns={
				'Qual é o nome da sua escola?': 'NOME ESCOLA',
				'Selecione abaixo a área administrativa da sua escola:': 'DISTRITO',
				'Total de alunos do 1º ano da MANHÃ': '1º ANO MANHÃ',
				'Total de alunos do 1º ano da INTERMEDIÁRIO': '1º ANO INTERMEDIÁRIO',
				'Total de alunos do 1º ano  da TARDE': '1º ANO TARDE',
				'Total de alunos do 2º  ano da MANHÃ': '2º ANO MANHÃ',
				'Total de alunos do 2º ano da INTERMEDIÁRIO': '2º ANO INTERMEDIÁRIO',
				'Total de alunos do 2º  ano da TARDE': '2º ANO TARDE',
				'Total de alunos do 3º  ano da MANHÃ': '3º ANO MANHÃ',
				'Total de alunos do 3º  ano da  INTERMEDIÁRIO': '3º ANO INTERMEDIÁRIO',
				'Total de alunos do 3º  ano da TARDE': '3º ANO TARDE',
				'Total de alunos do 4º  ano da MANHÃ': '4º ANO MANHÃ',
				'Total de alunos do 4º  ano da  INTERMEDIÁRIO': '4º ANO INTERMEDIÁRIO',
				'Total de alunos do 4º  ano da TARDE': '4º ANO TARDE',
				'Total de alunos do 5º  ano da MANHÃ': '5º ANO MANHÃ',
				'Total de alunos do 5º  ano da  INTERMEDIÁRIO': '5º ANO INTERMEDIÁRIO',
				'Total de alunos do 5º  ano  da TARDE': '5º ANO TARDE',
				'Total de alunos do 6º ano  da MANHÃ': '6º ANO MANHÃ',
				'Total de alunos do 6º ano  da  INTERMEDIÁRIO': '6º ANO INTERMEDIÁRIO',
				'Total de alunos do 6º ano  da TARDE': '6º ANO TARDE',
				'Total de alunos do 7º  ano da MANHÃ': '7º ANO MANHÃ',
				'Total de alunos do 7º  ano da  INTERMEDIÁRIO': '7º ANO INTERMEDIÁRIO',
				'Total de alunos do 7º  ano da TARDE': '7º ANO TARDE',
				'Total de alunos do 8º  ano da MANHÃ': '8º ANO MANHÃ',
				'Total de alunos do 8º  ano da  INTERMEDIÁRIO': '8º ANO INTERMEDIÁRIO',
				'Total de alunos do 8º  ano da TARDE': '8º ANO TARDE',
				'Total de alunos do 9º  ano da MANHÃ': '9º ANO MANHÃ',
				'Total de alunos do 9º  ano da  INTERMEDIÁRIO': '9º ANO INTERMEDIÁRIO',
				'Total de alunos do 9º  ano da TARDE': '9º ANO TARDE',
				'Total de alunos da  EJAI 1ª TOTALIDADE': 'EJAI 1º ANO',
				'Total de alunos da  EJAI 2ª TOTALIDADE': 'EJAI 2º ANO',
				'Total de alunos da EJAI 3ª TOTALIDADE': 'EJAI 3º ANO',
				'Total de alunos da EJAI 4ª TOTALIDADE': 'EJAI 4º ANO'
		}, inplace=True)

		# Seleção e transformação dos dados
		new_df = labels_df.loc[:, [
				'NOME ESCOLA', 'DISTRITO',
				'1º ANO MANHÃ', '1º ANO INTERMEDIÁRIO', '1º ANO TARDE',
				'2º ANO MANHÃ', '2º ANO INTERMEDIÁRIO', '2º ANO TARDE',
				'3º ANO MANHÃ', '3º ANO INTERMEDIÁRIO', '3º ANO TARDE',
				'4º ANO MANHÃ', '4º ANO INTERMEDIÁRIO', '4º ANO TARDE',
				'5º ANO MANHÃ', '5º ANO INTERMEDIÁRIO', '5º ANO TARDE',
				'6º ANO MANHÃ', '6º ANO INTERMEDIÁRIO', '6º ANO TARDE',
				'7º ANO MANHÃ', '7º ANO INTERMEDIÁRIO', '7º ANO TARDE',
				'8º ANO MANHÃ', '8º ANO INTERMEDIÁRIO', '8º ANO TARDE',
				'9º ANO MANHÃ', '9º ANO INTERMEDIÁRIO', '9º ANO TARDE',
				'EJAI 1º ANO', 'EJAI 2º ANO', 'EJAI 3º ANO', 'EJAI 4º ANO'
		]]
		
		# Tratamento dos dados da nova tabela 
		newnew_df = new_df.melt(id_vars=['NOME ESCOLA', 'DISTRITO'], var_name='ATRIBUTO', value_name="TOTAL")
		clean_df = newnew_df.dropna()
		clean_df["TOTAL"] = pd.to_numeric(clean_df["TOTAL"], errors='coerce').astype(int)
		clean_df = clean_df[clean_df["TOTAL"] != 0]

		# Formatando o nome das Escolasde de forma que fiquem sem as siglas  
		clean_df["NOME ESCOLA"] = clean_df['NOME ESCOLA'].apply(lambda escola: ' '.join(escola.split(' ')[1:]) if escola.split(' ')[0].upper() not in ['UP', 'ANEXO'] else escola)

		# Formatanto todos os nomes das Escolas para caixa alta e deixando em ordem alfabetica
		clean_df["NOME ESCOLA"] = clean_df["NOME ESCOLA"].str.upper()
		clean_df = clean_df.sort_values(by='NOME ESCOLA')

		# Exibição dos dados com o AgGrid
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
				file_name='etiquetas_semec.pdf',
				mime='text/csv'
			)		    

if __name__ == "__main__":
	main()