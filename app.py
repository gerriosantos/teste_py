
import dash
from dash import dcc, html, Input, Output, Dash
import pandas as pd
import plotly.express as px


# Carregar dados de avaliação de fluência (exemplo fictício)
df = pd.DataFrame({
    'Aluno': ['Ana', 'Bruno', 'Carlos', 'Diana', 'Eduardo'],
    'Fluência': [85, 70, 90, 60, 75],
    'Turma': ['A', 'B', 'A', 'B', 'A']
})


# Inicializar o app Dash
app = Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.Div([
        html.H1('📊 Dashboard de Avaliação de Fluência', style={
            'textAlign': 'center',
            'color': '#2c3e50',
            'marginBottom': '10px',
            'marginTop': '20px',
            'fontWeight': 'bold',
        }),
        html.P('Visualize e compare o desempenho de fluência dos alunos de forma interativa.', style={
            'textAlign': 'center',
            'color': '#34495e',
            'fontSize': '18px',
            'marginBottom': '30px',
        }),
        html.Div([
            html.Label('Selecione a turma:', style={
                'fontWeight': 'bold',
                'color': '#2980b9',
                'fontSize': '16px',
            }),
            dcc.Dropdown(
                id='turma-dropdown',
                options=[{'label': turma, 'value': turma} for turma in sorted(df['Turma'].unique())],
                value=None,
                placeholder='Todas as turmas',
                clearable=True,
                style={
                    'backgroundColor': '#ecf0f1',
                    'color': '#2c3e50',
                    'fontSize': '15px',
                }
            )
        ], style={
            'width': '300px',
            'margin': 'auto',
            'marginBottom': '30px',
            'padding': '20px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px #d0d7de',
        }),
        html.Div([
            dcc.Graph(id='grafico-fluencia'),
        ], style={
            'backgroundColor': '#fff',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px #d0d7de',
            'padding': '20px',
            'marginBottom': '20px',
        }),
        html.Div(id='media-fluencia', style={
            'textAlign': 'center',
            'marginTop': 20,
            'fontSize': '20px',
            'fontWeight': 'bold',
            'color': '#27ae60',
            'backgroundColor': '#eafaf1',
            'width': '300px',
            'margin': 'auto',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px #d0d7de',
            'padding': '15px',
        }),
        html.Div([
            html.P('ℹ️ Dica: Use o filtro acima para comparar turmas ou veja todos os alunos juntos!', style={
                'textAlign': 'center',
                'color': '#636e72',
                'fontSize': '15px',
                'marginTop': '30px',
            })
        ])
    ], style={
        'maxWidth': '700px',
        'margin': 'auto',
        'padding': '30px',
        'backgroundColor': '#f4f6fb',
        'borderRadius': '15px',
        'boxShadow': '0 4px 16px #d0d7de',
        'minHeight': '100vh',
    })
])


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
