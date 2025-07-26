import pandas as pd
import numpy as np
import os

def gerar_base_bruta(qtd_alunos=200, seed=42):
    np.random.seed(seed)
    nomes = [f"Aluno_{i+1}" for i in range(qtd_alunos)]
    turmas = np.random.choice(['A', 'B', 'C', 'D'], size=qtd_alunos)
    municipios = np.random.choice(['Município 1', 'Município 2', 'Município 3'], size=qtd_alunos)
    regionais = np.random.choice(['Regional Norte', 'Regional Sul'], size=qtd_alunos)
    estados = np.random.choice(['Estado X', 'Estado Y'], size=qtd_alunos)
    categorias = np.random.choice([
        'pré-leitor1', 'pré-leitor2', 'pré-leitor3', 'pré-leitor4', 'iniciante', 'fluente'
    ], size=qtd_alunos, p=[0.15, 0.15, 0.15, 0.15, 0.2, 0.2])
    datas = pd.date_range('2025-03-01', periods=5, freq='M')
    registros = []
    for i, nome in enumerate(nomes):
        for data in np.random.choice(datas, size=np.random.randint(1, 3)):
            cat = categorias[i]
            if cat == 'pré-leitor1':
                fluencia = np.random.normal(10, 3)
            elif cat == 'pré-leitor2':
                fluencia = np.random.normal(20, 4)
            elif cat == 'pré-leitor3':
                fluencia = np.random.normal(30, 5)
            elif cat == 'pré-leitor4':
                fluencia = np.random.normal(40, 6)
            elif cat == 'iniciante':
                fluencia = np.random.normal(60, 8)
            else:
                fluencia = np.random.normal(90, 10)
            registros.append({
                'aluno_nome': nome,
                'turma': turmas[i],
                'municipio': municipios[i],
                'regional': regionais[i],
                'estado': estados[i],
                'categoria_leitor': cat,
                'data_avaliacao': pd.Timestamp(data).strftime('%d/%m/%Y'),
                'fluencia': max(0, round(fluencia, 1))
            })
    return pd.DataFrame(registros)

def etl_fluencia(df_bruta):
    df = df_bruta.rename(columns={
        'aluno_nome': 'Aluno',
        'turma': 'Turma',
        'municipio': 'Município',
        'regional': 'Regional',
        'estado': 'Estado',
        'categoria_leitor': 'Categoria',
        'data_avaliacao': 'Data',
        'fluencia': 'Fluência'
    })
    df = df[(df['Fluência'] >= 0) & (df['Fluência'] <= 150)]
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
    df = df.sort_values('Data').groupby(['Aluno', 'Turma', 'Município', 'Regional', 'Estado'], as_index=False).last()
    return df

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    df_bruta = gerar_base_bruta()
    df_bruta.to_csv('data/fluencia_bruta.csv', index=False)
    df_tratada = etl_fluencia(df_bruta)
    df_tratada.to_csv('data/fluencia_tratada.csv', index=False)
    print('Bases salvas em data/fluencia_bruta.csv e data/fluencia_tratada.csv')