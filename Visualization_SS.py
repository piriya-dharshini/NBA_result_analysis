import plotly.express as px
import plotly.graph_objects as go
from analysis import semester_data, Reappear, Grade_Count

def RA_bar(semester, batch_year):
    x = semester_data(semester, batch_year)
    #print(x)
    y1 = [Grade_Count('AB', item, semester, batch_year) for item in x]
    y2 = [Reappear(item, semester, batch_year) for item in x]
    #print(y1)
    #print(y2)

    # Define your custom colors
    absent_color = '#138D75' 
    reappear_color = '#F0159A'
    bar_width = 0.5

    fig = go.Figure(go.Bar(x=x, y=y1, name='ABSENT', marker=dict(color=absent_color),width=bar_width))
    fig.add_trace(go.Bar(x=x, y=y2, name='REAPPEAR', marker=dict(color=reappear_color),width=bar_width))
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    fig.update_layout(title = f'SUBJECT-WISE SUMMARY FOR SEMESTER - {semester} OF THE BATCH {batch_year}')
    #fig.show()
    
    fig.write_html('RA_App/templates/Visualization_RA.html')


#RA_pie(2, '2022-2026')