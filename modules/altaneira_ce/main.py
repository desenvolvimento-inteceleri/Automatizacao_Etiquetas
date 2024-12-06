import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from .labels_altaneira import gerar_etiquetas
from .data_manipulation_altaneira import dm_first_stage
from .data_manipulation_semifinal import dm_semifinal_stage

@st.cache_data
def convert_df(df: pd.DataFrame):
    return df.to_csv(index=False).encode('utf-8')

def main():
    st.subheader("Criação de Etiquetas - Altaneira/Ce")
    pd.options.mode.chained_assignment = None

    opcao = st.selectbox(
        label= 'Selecione uma opção para criar etiquetas',
        options=('1ª Etapa - Classificatoria', '2 Etapa - Classificatoria', '3ª Semifinal - Semifinal'),
        index=None,
        placeholder='Selecione uma opção'
    )

    st.write('Você selecionou:', opcao)

    uploaded_file = st.file_uploader("Carregar planilha CSV", type="csv")

    if uploaded_file is not None:
        main_df = pd.read_csv(uploaded_file)
        df_tratado = pd.DataFrame
        if opcao == '1ª Etapa - Classificatoria':
            df_tratado = dm_first_stage(main_df)
        elif opcao == '3ª Semifinal - Semifinal':
            df_tratado = dm_semifinal_stage(main_df)
        # elif opcao == '2 Etapa - Classificatoria':
            #funcao de tratamento da segunda etapa

        AgGrid(df_tratado)

        # export_csv_file = convert_df(clean_df)

        # st.download_button(
        #     label="Baixar Planilha Tratada",
        #     data=export_csv_file,
        #     file_name="ETIQUETAS_TRATADA.csv",
        #     mime='Text/csv'
        # )

        # logo_file = st.file_uploader("Carregue a imagem da logo", type=["png", "jpg", "jpeg"])
        # championship = st.text_input("Nome do campeonato").upper()
        # stage = st.text_input("Etapa").upper()

        # if logo_file and championship and stage:
        #     st.download_button(
        #         label="Baixar PDF",
        #         data=gerar_etiquetas(tabela=clean_df, logo=logo_file, championship=championship, stage=stage),
        #         file_name='etiquetas_altaneira.pdf',
        #         mime='text/csv'
        #     )

if __name__ == "__main__":
    main()