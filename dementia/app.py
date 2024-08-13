import pandas as pd
from shiny import App, Inputs, Outputs, Session, render, ui
from shinywidgets import output_widget, render_widget
import plotly.graph_objs as go
import plotly.io as pio
pio.templates

# data sets
from africa_list import african_countries 
data = pd.read_csv('combined_df')


app_ui = ui.page_fluid(
    ui.input_select("select_country","select",choices= african_countries,selected=None),
    ui.output_text("value"),
    output_widget("plot")
)


def server(input: Inputs, output: Outputs, session: Session):
    @render.text()
    def value():
        return "Your country: " + str(input.select_country())
    

    @render_widget()
    def plot():

        df = data[data['Entity'] == str(input.select_country())]

        fig = go.Figure()

        for variable in ['alcohol_consumption', 'Cases_100,000_people']:
            fig.add_trace(go.Scatter(x=df['Year'], 
                                     y=df[variable], 
                                     mode='lines', 
                                     name=f"{variable}"))
            fig.update_layout(template='simple_white',
                               font=dict(size=14),
                               title_font=dict(size=20))
        return fig

        

app = App(app_ui, server)