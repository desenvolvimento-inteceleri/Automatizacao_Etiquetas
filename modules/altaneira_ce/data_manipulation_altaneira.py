import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from .labels_altaneira import gerar_etiquetas

@st.cache_data
def convert_df(df: pd.DataFrame):
    return df.to_csv(index=False).encode('utf-8')

def main():
    st.subheader("Criação de Etiquetas - Altaneira/Ce")
    pd.options.mode.chained_assignment = None

    opcao = st.selectbox(
        label= 'Selecione uma opção para criar etiquetas',
        options=('1ª Etapa - Classificatoria', 'Paralimpiada', '3ª Semifinal - Semifinal'),
        index=None,
        placeholder='Selecione uma opção'
    )

    st.write('Você selecionou:', opcao)

    uploaded_file = st.file_uploader("Carregar planilha CSV", type="csv")

    if uploaded_file is not None:
        labels_df = pd.read_csv(uploaded_file)

        labels_df.rename(columns={
            'Nome da Escola': 'NOME ESCOLA',
            'Total de alunos do 1º ano': '1º ANO',
            'Total de alunos do 2º  ano': '2º ANO',
            'Total de alunos do 3º  ano ': '3º ANO',
            'Total de alunos do 4º  ano': '4º ANO',
            'Total de alunos do 5º  ano': '5º ANO',
            'Total de alunos do 6º ano': '6º ANO',
            'Total de alunos do 7º  ano': '7º ANO',
            'Total de alunos do 8º ': '8º ANO',
            'Total de alunos do 9º  ano': '9º ANO',
            'Total de alunos da  EJA 1ª seguimento': '1º ANO EJA',
            'Total de alunos da  EJAI 2ª seguimento': '2º ANO EJA'
        }, inplace=True)                        
        
        new_df =labels_df.loc[:, [
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

        newnew_df = new_df.melt(id_vars=['NOME ESCOLA'], var_name='ANO ESCOLAR', value_name='TOTAL')
        clean_df = newnew_df.dropna()
        clean_df["TOTAL"] = pd.to_numeric(clean_df['TOTAL'], errors='coerce').astype(int)
        clean_df = clean_df[clean_df['TOTAL'] !=0]

        clean_df['NOME ESCOLA'] = clean_df['NOME ESCOLA'].apply(lambda escola: ' '.join(escola.split(' ')[1:]))

        clean_df['NOME ESCOLA'] = clean_df['NOME ESCOLA'].str.upper()
        clean_df = clean_df.sort_values(by='NOME ESCOLA')

        AgGrid(clean_df)

        export_csv_file = convert_df(clean_df)

        st.download_button(
            label="Baixar Planilha Tratada",
            data=export_csv_file,
            file_name="ETIQUETAS_TRATADA.csv",
            mime='Text/csv'
        )

        logo_file = st.file_uploader("Carregue a imagem da logo", type=["png", "jpg", "jpeg"])
        championship = st.text_input("Nome do campeonato").upper()
        stage = st.text_input("Etapa").upper()

        if logo_file and championship and stage:
            st.download_button(
                label="Baixar PDF",
                data=gerar_etiquetas(tabela=clean_df, logo=logo_file, championship=championship, stage=stage),
                file_name='etiquetas_altaneira.pdf',
                mime='text/csv'
            )

if __name__ == "__main__":
    main()