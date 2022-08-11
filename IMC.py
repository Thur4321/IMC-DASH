import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
    
app = dash.Dash(__name__)

peso = []
altura = []

for i in range(46, 111):
    if i%2 == 0:
        peso.append(i)
        
for i in range(146, 211):
    if i%2 == 0:
        altura.append(i)

app.layout = html.Div([
    html.H1('Cálculo de IMC', style = {'text-align':'center'}),
    dcc.Input(id="name", type="text", placeholder="", style={'marginRight':'10px'}),
    dcc.Dropdown(id = 'slct_pes',
                options = peso,
                multi = False,
                value = 46,
                style = {'width':'40%'}
                ),
    dcc.Dropdown(id = 'slct_alt',
                options = altura,
                multi = False,
                value = 146,
                style = {'width':'40%'}
                ),
    html.Div(id = 'output_container', children = []),
    html.Br(),
    dcc.Graph(id = 'IMC', figure = {})
    
])

@app.callback(
    [Output(component_id = 'output_container', component_property = 'children'),
    Output(component_id = 'IMC', component_property = 'figure')],
    [Input(component_id = 'name', component_property = 'value'),
     Input(component_id = 'slct_pes', component_property = 'value'),
     Input(component_id = 'slct_alt', component_property = 'value')]
)
def update_graph(name, pes_slctd, alt_slctd):
     
    imc = pes_slctd/((alt_slctd/100)**2)
     
    imc_array = np.empty((len(altura), len(peso)), dtype=int)
    for i in range(0, len(altura)):
        for j in range(0, len(peso)):
            imc_array[i][j] = (peso[j]/((altura[i]/100)**2))
     
    fig = px.imshow(imc_array, labels=dict(x="Peso", y="Altura", color="IMC"), x = peso, y = altura, text_auto=False, color_continuous_scale='Turbo')
    
    fig.add_scatter(x = [pes_slctd], y = [alt_slctd]) 
    
    
    if imc < 18.5:
      resultado = 'Abaixo do peso'
    elif 18.5 <= imc < 25:
      resultado = 'Peso normal'
    elif 25 <= imc < 30: 
      resultado = 'Sobrepeso'
    elif 30 <= imc < 40:
      resultado = 'Obesidade'
    else:
      resultado = 'Obesidade mórbida'
    
    if name != None:
        container = 'O '+name+' está em: {}'.format(resultado)
    else:
        container = 'O usuário está em: {}'.format(resultado)
    
    return container, fig

if __name__ == '__main__':
    app.run_server(port = 9000, debug=True, use_reloader=True)