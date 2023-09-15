from IPython.display import HTML

def horizontal(dfs):
    html = '<div style="display:flex">'
    for df in dfs:
        html += '<div style="margin-right: 32px">'
        html += df.to_html()
        html += '</div>'
    html += '</div>'
    display(HTML(html))


lista_test = [1,2,3,5]

prueba = 3.4


texto = "hola que tal "