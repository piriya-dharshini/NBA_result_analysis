import plotly.express as px
from summary import GPA_count

def GPA_pie(semester, batch_year):

    Gpas_new = GPA_count(semester, batch_year)
    Gpas_new = Gpas_new.items()

    Gpas = []
    for i in Gpas_new:
        Gpas.append(list(i))
    #print("////",Gpas)

    Gpas[4][1] = Gpas[4][1] - Gpas[3][1]
    Gpas[3][1] = Gpas[3][1] - Gpas[2][1]
    Gpas[2][1] = Gpas[2][1] - Gpas[1][1]
    Gpas[1][1] = Gpas[1][1] - Gpas[0][1]

    Labels = ['Above 9', 'Above 8.5', 'Above 8', 'Above 7.5', 'Above 6']
    Values = [Gpas[0][1], Gpas[1][1], Gpas[2][1], Gpas[3][1], Gpas[4][1]]
    #print("\\\\",Values,Gpas)
    colors=['#7df9ff','#a020f0','#80ffaa','#aa80ff','#ff0090','#ff66b3','#fdfd96','#ff7f50','#ff355e','#faf0be','#aaf0d1']
    fig = px.pie(names = Labels, values = Values, color = Labels,
                                color_discrete_map={'Above 9':colors[0],
                                                        'Above 8.5':colors[3],
                                                        'Above 8':colors[5],
                                                        'Above 7.5':colors[10],
                                                        'Above 6':colors[6]})
    
    fig.update_layout(title = f'OVERALL SUMMARY FOR SEMESTER - {semester} OF THE BATCH {batch_year}')
    fig.update_traces(textinfo = 'label + percent', selector = dict(type = 'pie'))

    fig.write_html('RA_App/templates/Visualization_GPA.html')

GPA_pie(2, '2022-2026')