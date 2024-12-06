import pandas as pd

def dm_semifinal_stage(df: pd.DataFrame):
    # Ignorar a primeira linha
    df = df.iloc[1:]

    # Ignorar a última coluna
    df = df.iloc[:, :-1]

    # Renomear colunas para padronizar
    df.rename(columns={
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
    new_df = df.loc[:, [
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

    return clean_df
