from dash import html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import dash

from sentiment_prediction import entity_sentiment_analysis
from map_team import get_team_name

# Load the dataset
data = pd.read_csv("../data/crick_df_cleaned.csv")

# Extract unique team names
unique_teams = sorted(pd.concat([data["team_1"], data["team_2"]]).unique())

def get_main_page_layout():
    """Return the layout for the Main Page."""
    return html.Div([
        
        html.Div([
            html.Div([
                html.H1("Cricket World Cup Dashboard", id="page-header"),
                dcc.Link(html.Button("Details Page ➡️"), href="/details", id="back-button"),
            ], className="header-container")
        ]),

        html.Div([
            html.Button("League Match", id="League-Match", n_clicks=0, style={"margin": "5px"}),
            html.Button("Semi Finals", id="Semi-Final", n_clicks=0, style={"margin": "5px"}),
            html.Button("Finals", id="Final", n_clicks=0, style={"margin": "5px"}),
        ], style={"textAlign": "center", "margin": "20px"}),

        html.Div([
            html.Div([
                dcc.Graph(id="summary-chart-2"),
            ], style={"border": "2px solid black", "border-radius": "20px", "width": "48%", "padding": "10px"}),
            
            
            html.Div([
                html.H4("Try Our Sentiment Prediction", style={"textAlign": "center", "justifyContent": "left"}),
                
                html.Div([
                    html.Div([
                        html.Label("Select Team 1:"),
                        dcc.Dropdown(
                            id="team1-dropdown",
                            options=[{"label": team, "value": team} for team in unique_teams],
                            value=unique_teams[0],
                            clearable=False,
                        ),
                    ], style={"width": "30%", "display": "inline-block", "margin-left": "30px"}),

                    html.Div([
                        html.Label("Select Team 2:"),
                        dcc.Dropdown(
                            id="team2-dropdown",
                            options=[{"label": team, "value": team} for team in unique_teams],
                            value=unique_teams[1],
                            clearable=False,
                        ),
                    ], style={"width": "30%", "display": "inline-block", "margin-right": "10px"}),
                ], style={"display": "flex", "flexDirection": "row", "justifyContent": "space-between", "margin": "35px"}),
                
                html.Div([
                    html.Div([
                        html.Label("Enter your text here:"),
                        dcc.Input(
                            id="user-input",
                            type="text",
                            placeholder="Type your input here...",
                            style={"border": "1px solid gray", "border-radius": "10px", "padding": "15px", "fontSize": "12px"},
                        ),
                    ], style={"margin-left": "20px", "display": "flex", "flexDirection": "column", "gap":"10px"}),
            
                    html.Button(
                        "Submit",
                        id="submit-button",
                        n_clicks=0,
                        style={"margin-left": "20px", "padding": "10px", "border": "1px solid black", "border-radius": "10px", "width": "20%", "fontSize": "10px"},
                    ),
                ], style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "margin": "35px", "gap":"10px"}),
                
                html.Div([
                    html.Label("Prediction:", style={"margin-left": "20px"}),
                    html.Div(id="prediction-output", style={"margin-left": "20px", "fontWeight": "bold", "color": "blue", "fontSize": "15px", "border": "1px solid gray", "padding": "25px", "border-radius": "10px"}),
                ],style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "margin": "35px"}),                         
                            
            ], style={"border": "2px solid black", "border-radius": "20px", "width": "48%", "padding": "10px"}),
        ], style={"display": "flex", "flexDirection": "row", "justifyContent": "space-between", "margin": "20px"}),
        
        html.Div([
            dcc.Graph(id="summary-chart-1"),
        ]),
    ])

def sentiment_analysis(user_input, team1):
    """Predict the sentiment of the user input."""
    if not user_input:
        return "No input provided for analysis."
    prediction = entity_sentiment_analysis(user_input, team1)
    return prediction


def register_main_page_callbacks(app):
    """Register callbacks for the Main Page."""
    
    # Callback for Sentiment Prediction
    @app.callback(
        Output("prediction-output", "children"),
        [Input("submit-button", "n_clicks")],
        [State("team1-dropdown", "value"),
         State("user-input", "value")]
    )
    def update_prediction(submit_clicks, team1, user_input):
        if submit_clicks > 0:
            team1 = get_team_name(team1)
            user_input = user_input + " from " + team1
            return sentiment_analysis(user_input, team1)
        return ""

    # Callback for Charts
    @app.callback(
        [Output("summary-chart-1", "figure"),
         Output("summary-chart-2", "figure")],
        [Input("League-Match", "n_clicks"),
         Input("Semi-Final", "n_clicks"),
         Input("Final", "n_clicks")]
    )
    def update_charts(league_clicks, semi_final_clicks, final_clicks):
        # Determine the selected category
        ctx = dash.callback_context
        if not ctx.triggered:
            selected_category = "Final"
        else:
            selected_category = ctx.triggered[0]["prop_id"].split(".")[0]

        # Filter the dataset
        filtered_data = data[data["match_category"] == selected_category]

        # Create charts
        fig1 = px.bar(
            filtered_data, 
            x="team_1", 
            y="team_1_runs", 
            color="winning_team", 
            title="Team Performance in Selected Match Category",
            labels={"team_1": "Team", "team_1_runs": "Runs"}
        )

        fig2 = px.pie(
            filtered_data,
            names="winning_team",
            title="Winning Teams Distribution",
        )

        return fig1, fig2