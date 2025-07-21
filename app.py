import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os

# Carregar dados de avaliação de fluência (exemplo fictício)
data = {
    'Aluno': ['Ana', 'Bruno', 'Carlos', 'Diana', 'Eduardo'],
    'Fluência': [85, 70, 90, 60, 75],
    'Turma': ['A', 'B', 'A', 'B', 'A']
}
df = pd.DataFrame(data)

# Inicializar o app Dash
dashboard = dash.Dash(__name__)

# Layout do dashboard
dashboard.layout = html.Div([
    html.H1('Dashboard de Avaliação de Fluência', style={'textAlign': 'center'}),
    html.Div([
        html.Label('Selecione a turma:'),
        dcc.Dropdown(
            id='turma-dropdown',
            options=[{'label': turma, 'value': turma} for turma in sorted(df['Turma'].unique())],
            value=None,
            placeholder='Todas as turmas',
            clearable=True
        )
    ], style={'width': '30%', 'margin': 'auto'}),
    dcc.Graph(id='grafico-fluencia'),
    html.Div(id='media-fluencia', style={'textAlign': 'center', 'marginTop': 20})
])

# Callback para atualizar o gráfico e a média
def filtrar_df(turma):
    if turma:
        return df[df['Turma'] == turma]
    return df

@dashboard.callback(
    Output('grafico-fluencia', 'figure'),
    Output('media-fluencia', 'children'),
    Input('turma-dropdown', 'value')
)
def atualizar_dashboard(turma):
    df_filtrado = filtrar_df(turma)
    fig = px.bar(df_filtrado, x='Aluno', y='Fluência', color='Aluno',
                 labels={'Fluência': 'Nota de Fluência'},
                 title='Notas de Fluência por Aluno')
    media = df_filtrado['Fluência'].mean()
    texto_media = f"Média de Fluência: {media:.2f}"
    return fig, texto_media

if __name__ == '__main__':
    dashboard.run_server(debug=True)
