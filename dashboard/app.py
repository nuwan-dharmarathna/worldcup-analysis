from dash import Dash, dcc, html, Input, Output
from main_page import get_main_page_layout, register_main_page_callbacks
from details_page import get_details_page_layout, register_details_page_callbacks

# Initialize the app
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Cricket World Cup Dashboard"

# App layout with routing
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content"),
])

# Callbacks for routing
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/details":
        return get_details_page_layout()
    return get_main_page_layout()

# Register callbacks for individual pages
register_main_page_callbacks(app)
register_details_page_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
