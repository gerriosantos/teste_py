import pandas as pd
import numpy as np

def gerar_base_bruta(qtd_alunos=30, seed=42):
    np.random.seed(seed)
    nomes = [f"Aluno_{i+1}" for i in range(qtd_alunos)]
    turmas = np.random.choice(['A', 'B', 'C'], size=qtd_alunos)
    # Simula avaliações em diferentes datas e com possíveis erros de digitação
    datas = pd.date_range('2025-03-01', periods=5, freq='M')
    registros = []
    for nome, turma in zip(nomes, turmas):
        for data in np.random.choice(datas, size=np.random.randint(2, 6)):
            fluencia = np.random.normal(75, 15)
            # Simula erros de digitação e valores extremos
            if np.random.rand() < 0.05:
                fluencia = np.random.choice([0, 200, -10, 999])
            registros.append({
                'aluno_nome': nome,
                'turma': turma,
                'data_avaliacao': data.strftime('%d/%m/%Y'),
                'fluencia': round(fluencia, 1)
            })
    return pd.DataFrame(registros)

def etl_fluencia(df_bruta):
    # Corrige nomes das colunas
    df = df_bruta.rename(columns={
        'aluno_nome': 'Aluno',
        'turma': 'Turma',
        'data_avaliacao': 'Data',
        'fluencia': 'Fluência'
    })
    # Remove valores extremos e negativos
    df = df[(df['Fluência'] >= 0) & (df['Fluência'] <= 150)]
    # Converte datas
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
    # Mantém apenas a última avaliação de cada aluno
    df = df.sort_values('Data').groupby(['Aluno', 'Turma'], as_index=False).last()
    return df

if __name__ == "__main__":
    # Gera base bruta e salva para inspeção
    df_bruta = gerar_base_bruta()
    df_bruta.to_csv('data/fluencia_bruta.csv', index=False)
    # Executa ETL e salva base tratada
    df_tratada = etl_fluencia(df_bruta)
    df_tratada.to_csv('data/fluencia_tratada.csv', index=False)
    print('Bases salvas em data/fluencia_bruta.csv e data/fluencia_tratada.csv')
