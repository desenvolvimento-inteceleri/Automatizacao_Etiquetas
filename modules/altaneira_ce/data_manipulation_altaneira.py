import pandas as pd

def dm_first_stage(df: pd.DataFrame):

    labels_df = pd.read_csv(df)

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
    
    return clean_df