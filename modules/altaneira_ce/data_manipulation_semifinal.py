import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from .labels_altaneira import gerar_etiquetas

@st.cache_data
def convert_df(df: pd.DataFrame):
    return df.to_csv(index=False).encode('utf-8')

def main():
    st.subheader("Criação de Etiquetas - Altaneira/CE")
    pd.options.mode.chained_assignment = None 
    # Botão de upload do arquivo CSV
    uploaded_file = st.file_uploader("Carregar planilha CSV", type="csv")
    
    if uploaded_file is not None:
        labels_df = pd.read_csv(uploaded_file)

        # Ignorar a primeira linha
        labels_df = labels_df.iloc[1:]

        # Ignorar a última coluna
        labels_df = labels_df.iloc[:, :-1]

        # Renomear colunas para padronizar
        labels_df.rename(columns={
            'Qual o nome da sua escola': 'NOME ESCOLA',
            '1ª ano': '1º ANO',
            '2ª ano': '2º ANO',
            '3º ano': '3º ANO',
            '4º ano': '4º ANO',
            '5º ano': '5º ANO',
            '6º ano': '6º ANO',
            '7º ano': '7º ANO',
            '8º ano': '8º ANO',
            '9º ano': '9º ANO',
            'EJA 1ª etapa': '1º ANO EJA',
            'EJA 2ª etapa': '2º ANO EJA',
        }, inplace=True)

        # Selecionar colunas de interesse
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
            '1º ANO EJA',
            '2º ANO EJA',
        ]]
        
        newnew_df = new_df.melt(id_vars=['NOME ESCOLA'], var_name='ANO ESCOLAR', value_name="TOTAL")
        clean_df = newnew_df.dropna()
        clean_df["TOTAL"] = pd.to_numeric(clean_df["TOTAL"], errors='coerce').astype(int)
        clean_df = clean_df[clean_df["TOTAL"] != 0]

        # Ignorar última linha se "Total geral" estiver na coluna "NOME ESCOLA"
        if clean_df.iloc[-1]['NOME ESCOLA'].strip().lower() == "Total geral":
            clean_df = clean_df.iloc[:-1]

        # Limpar e formatar nomes das escolas
        clean_df["NOME ESCOLA"] = clean_df['NOME ESCOLA'].apply(lambda escola: ' '.join(escola.split(' ')[1:]))
        clean_df["NOME ESCOLA"] = clean_df["NOME ESCOLA"].str.upper()
        clean_df = clean_df.sort_values(by='NOME ESCOLA')

        # Exibir tabela tratada
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
                mime='application/pdf'
            )            

if __name__ == "__main__":
    main()
