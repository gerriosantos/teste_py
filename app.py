

import dash
from dash import dcc, html, Input, Output, Dash
import pandas as pd
import plotly.express as px
import os

# Carregar base tratada do ETL
df = pd.read_csv('data/fluencia_tratada.csv')

# Simular coluna Escola (caso não exista)
if 'Escola' not in df.columns:
    escolas = ['Escola Alfa', 'Escola Beta', 'Escola Gama', 'Escola Delta']
    df['Escola'] = df['Município'].apply(lambda x: escolas[hash(x) % len(escolas)])


# Inicializar o app Dash
app = Dash(__name__)

# Layout com abas
app.layout = html.Div([
    html.H1('📊 Dashboard de Avaliação de Fluência', style={
        'textAlign': 'center',
        'color': '#2c3e50',
        'marginBottom': '10px',
        'marginTop': '20px',
        'fontWeight': 'bold',
    }),
    html.P('Explore os dados de fluência por diferentes perspectivas usando as abas abaixo.', style={
        'textAlign': 'center',
        'color': '#34495e',
        'fontSize': '18px',
        'marginBottom': '30px',
    }),
    dcc.Tabs(id='tabs', value='aluno', children=[
        dcc.Tab(label='Aluno', value='aluno'),
        dcc.Tab(label='Turma', value='turma'),
        dcc.Tab(label='Regional', value='regional'),
        dcc.Tab(label='Estado', value='estado'),
        dcc.Tab(label='Escola', value='escola'),
        dcc.Tab(label='Município', value='municipio'),
    ]),
    html.Div(id='conteudo-aba')
], style={
    'maxWidth': '900px',
    'margin': 'auto',
    'padding': '30px',
    'backgroundColor': '#f4f6fb',
    'borderRadius': '15px',
    'boxShadow': '0 4px 16px #d0d7de',
    'minHeight': '100vh',
})


# Callback para renderizar o conteúdo de cada aba
@app.callback(
    Output('conteudo-aba', 'children'),
    Input('tabs', 'value')
)
def renderizar_aba(aba):
    if aba == 'aluno':
        return html.Div([
            html.H3('Visualização por Aluno'),
            dcc.Dropdown(
                id='aluno-dropdown',
                options=[{'label': a, 'value': a} for a in sorted(df['Aluno'].unique())],
                value=None,
                placeholder='Selecione um aluno',
                clearable=True
            ),
            dcc.Graph(id='grafico-aluno')
        ])
    elif aba == 'turma':
        return html.Div([
            html.H3('Visualização por Turma'),
            dcc.Dropdown(
                id='turma-dropdown',
                options=[{'label': t, 'value': t} for t in sorted(df['Turma'].unique())],
                value=None,
                placeholder='Selecione uma turma',
                clearable=True
            ),
            dcc.Graph(id='grafico-turma')
        ])
    elif aba == 'regional':
        return html.Div([
            html.H3('Visualização por Regional'),
            dcc.Dropdown(
                id='regional-dropdown',
                options=[{'label': r, 'value': r} for r in sorted(df['Regional'].unique())],
                value=None,
                placeholder='Selecione uma regional',
                clearable=True
            ),
            dcc.Graph(id='grafico-regional')
        ])
    elif aba == 'estado':
        return html.Div([
            html.H3('Visualização por Estado'),
            dcc.Dropdown(
                id='estado-dropdown',
                options=[{'label': e, 'value': e} for e in sorted(df['Estado'].unique())],
                value=None,
                placeholder='Selecione um estado',
                clearable=True
            ),
            dcc.Graph(id='grafico-estado')
        ])
    elif aba == 'escola':
        return html.Div([
            html.H3('Visualização por Escola'),
            dcc.Dropdown(
                id='escola-dropdown',
                options=[{'label': e, 'value': e} for e in sorted(df['Escola'].unique())],
                value=None,
                placeholder='Selecione uma escola',
                clearable=True
            ),
            dcc.Graph(id='grafico-escola')
        ])
    elif aba == 'municipio':
        return html.Div([
            html.H3('Visualização por Município'),
            dcc.Dropdown(
                id='municipio-dropdown',
                options=[{'label': m, 'value': m} for m in sorted(df['Município'].unique())],
                value=None,
                placeholder='Selecione um município',
                clearable=True
            ),
            dcc.Graph(id='grafico-municipio')
        ])
    return html.Div()

# Callbacks para gráficos de cada aba
@app.callback(
    Output('grafico-aluno', 'figure'),
    Input('aluno-dropdown', 'value')
)
def grafico_aluno(aluno):
    dff = df if not aluno else df[df['Aluno'] == aluno]
    fig = px.bar(dff, x='Aluno', y='Fluência', color='Categoria',
                 title='Fluência por Aluno', labels={'Fluência': 'Nota de Fluência'})
    return fig

@app.callback(
    Output('grafico-turma', 'figure'),
    Input('turma-dropdown', 'value')
)
def grafico_turma(turma):
    dff = df if not turma else df[df['Turma'] == turma]
    fig = px.box(dff, x='Turma', y='Fluência', color='Categoria',
                 title='Distribuição de Fluência por Turma')
    return fig

@app.callback(
    Output('grafico-regional', 'figure'),
    Input('regional-dropdown', 'value')
)
def grafico_regional(regional):
    dff = df if not regional else df[df['Regional'] == regional]
    fig = px.violin(dff, x='Regional', y='Fluência', color='Categoria',
                   box=True, points='all', title='Fluência por Regional')
    return fig

@app.callback(
    Output('grafico-estado', 'figure'),
    Input('estado-dropdown', 'value')
)
def grafico_estado(estado):
    dff = df if not estado else df[df['Estado'] == estado]
    fig = px.bar(dff, x='Estado', y='Fluência', color='Categoria',
                 title='Fluência por Estado')
    return fig

@app.callback(
    Output('grafico-escola', 'figure'),
    Input('escola-dropdown', 'value')
)
def grafico_escola(escola):
    dff = df if not escola else df[df['Escola'] == escola]
    fig = px.bar(dff, x='Escola', y='Fluência', color='Categoria',
                 title='Fluência por Escola')
    return fig

@app.callback(
    Output('grafico-municipio', 'figure'),
    Input('municipio-dropdown', 'value')
)
def grafico_municipio(municipio):
    dff = df if not municipio else df[df['Município'] == municipio]
    fig = px.bar(dff, x='Município', y='Fluência', color='Categoria',
                 title='Fluência por Município')
    return fig


# Callback para atualizar o gráfico e a média
@app.callback(
    Output('grafico-fluencia', 'figure'),
    Output('media-fluencia', 'children'),
    Input('turma-dropdown', 'value')
)
def atualizar_dashboard(turma):
    if turma:
        df_filtrado = df[df['Turma'] == turma]
    else:
        df_filtrado = df
    fig = px.bar(df_filtrado, x='Aluno', y='Fluência', color='Aluno',
                 labels={'Fluência': 'Nota de Fluência'},
                 title='Notas de Fluência por Aluno')
    media = df_filtrado['Fluência'].mean()
    texto_media = f"Média de Fluência: {media:.2f}"
    return fig, texto_media

if __name__ == '__main__':
    app.run(debug=True)
