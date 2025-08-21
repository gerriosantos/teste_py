

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




# Inicializar o app Dash com suppress_callback_exceptions
app = Dash(__name__, suppress_callback_exceptions=True)

# Configurações das abas e colunas, com ícones e tooltips
tabs_config = [
    {'label': 'Aluno', 'value': 'aluno', 'col': 'Aluno', 'tipo': 'bar', 'icon': '👤', 'tooltip': 'Visualize dados por aluno individualmente.'},
    {'label': 'Turma', 'value': 'turma', 'col': 'Turma', 'tipo': 'box', 'icon': '👥', 'tooltip': 'Compare turmas e veja a distribuição de fluência.'},
    {'label': 'Regional', 'value': 'regional', 'col': 'Regional', 'tipo': 'violin', 'icon': '🗺️', 'tooltip': 'Veja a fluência por regionais de ensino.'},
    {'label': 'Estado', 'value': 'estado', 'col': 'Estado', 'tipo': 'bar', 'icon': '🏳️', 'tooltip': 'Compare estados.'},
    {'label': 'Escola', 'value': 'escola', 'col': 'Escola', 'tipo': 'bar', 'icon': '🏫', 'tooltip': 'Veja resultados por escola.'},
    {'label': 'Município', 'value': 'municipio', 'col': 'Município', 'tipo': 'bar', 'icon': '🏙️', 'tooltip': 'Compare municípios.'},
]

# Função para criar gráficos customizados
def criar_grafico(dff, x, tipo, color='Categoria'):
    if tipo == 'bar':
        fig = px.bar(
            dff, x=x, y='Fluência', color=color,
            title=f'Fluência por {x}', labels={'Fluência': 'Nota de Fluência'},
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
    elif tipo == 'box':
        fig = px.box(
            dff, x=x, y='Fluência', color=color,
            title=f'Distribuição de Fluência por {x}',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
    elif tipo == 'violin':
        fig = px.violin(
            dff, x=x, y='Fluência', color=color,
            box=True, points='all', title=f'Fluência por {x}',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
    else:
        fig = px.bar(dff, x=x, y='Fluência', color=color)
    fig.update_layout(
        plot_bgcolor='#f7f9fb',
        paper_bgcolor='#f7f9fb',
        font_color='#1a2639',
        title_font_color='#1a2639',
        legend_title_font_color='#1a2639',
        legend_bgcolor='#e8ecf4',
        legend_bordercolor='#bfc9d9',
        legend_borderwidth=1
    )
    return fig

# Layout com abas e tema customizado, com tooltips
app.layout = html.Div([
    html.H1('📊 Dashboard de Avaliação de Fluência', style={
        'textAlign': 'center',
        'color': '#1a2639',
        'marginBottom': '10px',
        'marginTop': '20px',
        'fontWeight': 'bold',
        'letterSpacing': '1px',
    }),
    html.P('Explore os dados de fluência por diferentes perspectivas usando as abas abaixo.', style={
        'textAlign': 'center',
        'color': '#3b4a5a',
        'fontSize': '18px',
        'marginBottom': '30px',
    }),
    dcc.Tabs(
        id='tabs', value='aluno',
        children=[
            dcc.Tab(
                label=f"{tab['icon']} {tab['label']}",
                value=tab['value'],
                style={
                    'background': '#e8ecf4',
                    'color': '#1a2639',
                    'fontWeight': 'bold',
                    'fontSize': '17px',
                    'padding': '10px 18px',
                    'borderRight': '1px solid #d0d7de',
                },
                selected_style={
                    'background': '#1a2639',
                    'color': '#fff',
                    'fontWeight': 'bold',
                    'fontSize': '17px',
                    'padding': '10px 18px',
                    'borderRight': '1px solid #d0d7de',
                    'boxShadow': '0 2px 8px #bfc9d9',
                }
            ) for tab in tabs_config
        ],
        style={
            'marginBottom': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px #d0d7de',
            'overflow': 'hidden',
        }
    ),
    html.Div(id='conteudo-aba')
], style={
    'maxWidth': '950px',
    'margin': 'auto',
    'padding': '32px',
    'backgroundColor': '#f7f9fb',
    'borderRadius': '18px',
    'boxShadow': '0 6px 24px #bfc9d9',
    'minHeight': '100vh',
    'border': '1px solid #e0e6ed',
})


# Callback para renderizar o conteúdo de cada aba
@app.callback(
    Output('conteudo-aba', 'children'),
    Input('tabs', 'value')
)
def renderizar_aba(aba):
    # Busca config da aba
    tab = next((t for t in tabs_config if t['value'] == aba), None)
    if not tab:
        return html.Div()
    col = tab['col']
    idx = aba
    return html.Div([
        html.H3(f'Visualização por {tab["label"]}'),
        dcc.Dropdown(
            id={'type': 'dropdown', 'index': idx},
            options=[{'label': v, 'value': v} for v in sorted(df[col].unique())],
            value=None,
            placeholder=f'Selecione um {tab["label"].lower()}',
            clearable=True
        ),
        dcc.Graph(id={'type': 'grafico', 'index': idx})
    ])



# Callbacks individuais para cada gráfico das abas
from dash import callback_context
for tab in tabs_config:
    aba = tab['value']
    col = tab['col']
    tipo = tab['tipo']
    dropdown_id = {'type': 'dropdown', 'index': aba}
    graph_id = {'type': 'grafico', 'index': aba}
    def make_callback(col=col, tipo=tipo, dropdown_id=dropdown_id, graph_id=graph_id):
        @app.callback(
            Output(graph_id, 'figure'),
            Input(dropdown_id, 'value'),
        )
        def update_graph(value):
            dff = df if not value else df[df[col] == value]
            return criar_grafico(dff, col, tipo)
    make_callback()


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
