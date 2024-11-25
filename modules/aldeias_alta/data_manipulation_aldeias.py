import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from .labels_aldeias import gerar_etiquetas

@st.cache_data
def convert_df(df: pd.DataFrame):
    return df.to_csv(index=False).encode('utf-8')

def main():
    st.subheader("Criação de Etiquetas - Aldeias Altas")
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
            'Nome da escola':'NOME ESCOLA',
            'Total de alunos do 1º ano da MANHÃ':'1º ANO MANHÃ',
            'Total de alunos do 1º ano  da TARDE':'1º ANO TARDE',
            'Total de alunos do 2º  ano da MANHÃ':'2º ANO MANHÃ',
            'Total de alunos do 2º  ano da TARDE':'2º ANO TARDE',
            'Total de alunos do 3º  ano da MANHÃ':'3º ANO MANHÃ',
            'Total de alunos do 3º  ano da TARDE':'3º ANO TARDE',
            'Total de alunos do 4º  ano da MANHÃ':'4º ANO MANHÃ',
            'Total de alunos do 4º  ano da TARDE':'4º ANO TARDE',
            'Total de alunos do 5º  ano da MANHÃ':'5º ANO MANHÃ',
            'Total de alunos do 5º  ano  da TARDE':'5º ANO TARDE'
        }, inplace=True)

        new_df = labels_df.loc[:, [
            'NOME ESCOLA',
            '1º ANO MANHÃ',
            '1º ANO TARDE',
            '2º ANO MANHÃ',
            '2º ANO TARDE',
            '3º ANO MANHÃ',
            '3º ANO TARDE',
            '4º ANO MANHÃ',
            '4º ANO TARDE',
            '5º ANO MANHÃ',
            '5º ANO TARDE'
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


