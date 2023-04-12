import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

def read_kpi_data():
    kpi_data = pd.read_excel('kpis.xlsx', engine='openpyxl')
    kpi_data['Date'] = pd.to_datetime(kpi_data['Date'], errors='coerce')
    return kpi_data

kpi_data = read_kpi_data()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('KPI Dashboard'),
    html.H3('Created by Joas Antonio'),
    dcc.Dropdown(
        id='kpi_selector',
        options=[{'label': kpi, 'value': kpi} for kpi in kpi_data['KPI'].dropna().unique()],
        value='MTTD',
        clearable=False
    ),
    dcc.DatePickerRange(
        id='date_range_selector',
        min_date_allowed=kpi_data['Date'].dropna().min(),
        max_date_allowed=kpi_data['Date'].dropna().max(),
        start_date=kpi_data['Date'].dropna().min(),
        end_date=kpi_data['Date'].dropna().max(),
    ),
    dcc.Graph(id='kpi_pie_chart'),
    dcc.Interval(
        id='interval-component',
        interval=10*1000, # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('kpi_pie_chart', 'figure'),
    [Input('kpi_selector', 'value'), Input('date_range_selector', 'start_date'), Input('date_range_selector', 'end_date'), Input('interval-component', 'n_intervals')]
)
def update_kpi_pie_chart(selected_kpi, start_date, end_date, n):
    kpi_data = read_kpi_data()
    kpi_df = kpi_data[(kpi_data['KPI'] == selected_kpi) & (kpi_data['Date'] >= start_date) & (kpi_data['Date'] <= end_date)]

    if kpi_df.empty:
        return go.Figure(
            data=[],
            layout=go.Layout(
                title=f'No data available for {selected_kpi} between {start_date} and {end_date}'
            )
        )

    # Substitua 'Value1', 'Value2', 'Value3' pelas colunas que representam os diferentes valores do KPI
    values = ['Value1', 'Value2', 'Value3']
    pie_values = [kpi_df[value].sum() for value in values]

    return go.Figure(
        data=[go.Pie(
            labels=values,
            values=pie_values,
            hole=.4,
            textinfo='label+percent'
        )],
        layout=go.Layout(
            title=f'{selected_kpi} Distribution (Date Range: {start_date} - {end_date})'
        )
    )

if __name__ == '__main__':
    app.run_server(debug=True)
