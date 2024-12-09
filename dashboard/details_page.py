from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
data = pd.read_csv("../data/crick_df_cleaned.csv")

def get_details_page_layout():
    return html.Div([
        # Header Section
        html.Div([
            html.Div([
                dcc.Link(html.Button("⬅️ Back", style={
                    "backgroundColor": "#007bff", 
                    "color": "white", 
                    "border": "none", 
                    "padding": "10px 20px", 
                    "borderRadius": "5px",
                    "cursor": "pointer"
                }), href="/", id="back-button"),
                html.H1("World Cup Details", id="page-header", style={
                    "textAlign": "center", 
                    "margin": "10px 0",
                    "color": "#333", 
                    "fontWeight": "bold",
                    "fontSize": "2.5em"
                }),
            ], className="header-container", style={
                "display": "flex", 
                "justifyContent": "space-between", 
                "alignItems": "center",
                "padding": "10px 30px",
                "backgroundColor": "#f8f9fa",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
            })
        ]),

        # Dropdown for Year Selection
        html.Div([
            html.Label("Select World Cup Year:", style={
                "fontWeight": "bold", 
                "marginTop": "20px", 
                "display": "block", 
                "fontSize": "1.2em"
            }),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": year, "value": year} for year in sorted(data["world_cup_year"].unique())],
                value=sorted(data["world_cup_year"].unique())[0],
                clearable=False,
                style={
                    "width": "100%", 
                    "padding": "10px", 
                    "marginTop": "10px", 
                    "borderRadius": "5px"
                }
            ),
        ], style={"padding": "20px"}),

        # Key Metrics Section
        html.Div([
            html.Div([
                html.H4("Winners:", id="winning-team", style={
                    "color": "#007bff", 
                    "fontWeight": "bold", 
                    "marginBottom": "10px"
                }),
            ], style={"marginBottom": "20px"}),

            html.Div([
                html.Div([
                    html.H4("Total Number of Matches:", id="total-matches", style={
                        "color": "#333", 
                        "fontWeight": "bold"
                    }),
                ], style={"flex": "1", "marginRight": "20px"}),

                html.Div([
                    html.H4("Played Matches:", id="played-matches", style={
                        "color": "#333", 
                        "fontWeight": "bold"
                    }),
                ], style={"flex": "1", "marginRight": "20px"}),

                html.Div([
                    html.H4("Abandoned:", id="abandoned", style={
                        "color": "#333", 
                        "fontWeight": "bold"
                    }),
                ], style={"flex": "1"}),
            ], style={
                "display": "flex", 
                "alignItems": "center", 
                "justifyContent": "space-between", 
                "margin": "20px 30px"
            }),
        ], style={"backgroundColor": "#f1f1f1", "padding": "20px", "borderRadius": "10px"}),

        # Graph Section 1
        html.Div([
            dcc.Graph(id="match-type-summary-chart", style={"marginTop": "20px", "marginBottom": "20px"}),
            dcc.Graph(id="team-performance-chart", style={"marginTop": "20px", "marginBottom": "20px"}),
        ], style={"display": "flex", "gap": "20px", "justifyContent": "space-around"}),

        # Dropdown for Team Selection
        html.Div([
            html.Label("Select a Team:", style={
                "fontWeight": "bold", 
                "display": "block", 
                "fontSize": "1.2em", 
                "marginTop": "20px"
            }),
            dcc.Dropdown(
                id="team-dropdown",
                options=[],
                clearable=False,
                style={
                    "width": "100%", 
                    "padding": "10px", 
                    "marginTop": "10px", 
                    "borderRadius": "5px"
                }
            ),
        ], style={"padding": "20px"}),

        # Graph Section 2
        html.Div([
            dcc.Graph(id="runs-vs-wickets-chart", style={"marginTop": "20px", "marginBottom": "20px", "flex": "1"}),
            dcc.Graph(id="venue-performance-chart", style={"marginTop": "20px", "marginBottom": "20px", "flex": "1"}),
        ], style={"display": "flex", "gap": "20px", "justifyContent": "space-around", "padding": "20px"}),
    ], style={
        "fontFamily": "'Arial', sans-serif", 
        "lineHeight": "1.6", 
        "maxWidth": "1200px", 
        "margin": "0 auto", 
        "backgroundColor": "#fff",
        "borderRadius": "10px", 
        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)"
    })


# Chart functions
def create_team_performance_chart(filtered_data):
    """Create a bar chart showing total runs and wickets by team."""
    team_runs = pd.concat([
        filtered_data[["team_1", "team_1_runs"]].rename(columns={"team_1": "team", "team_1_runs": "runs"}),
        filtered_data[["team_2", "team_2_runs"]].rename(columns={"team_2": "team", "team_2_runs": "runs"}),
    ])
    team_wickets = pd.concat([
        filtered_data[["team_1", "team_1_wickets"]].rename(columns={"team_1": "team", "team_1_wickets": "wickets"}),
        filtered_data[["team_2", "team_2_wickets"]].rename(columns={"team_2": "team", "team_2_wickets": "wickets"}),
    ])
    total_runs = team_runs.groupby("team")["runs"].sum().reset_index()
    total_wickets = team_wickets.groupby("team")["wickets"].sum().reset_index()
    team_stats = pd.merge(total_runs, total_wickets, on="team")

    return px.bar(
        team_stats,
        x="team",
        y=["runs", "wickets"],
        barmode="group",
        title=f"Total Runs and Wickets by Team",
        labels={"value": "Count", "variable": "Metric"},
        text_auto=True,
    )
    
def create_world_cup_match_type_summary_chart(filtered_data):
    """Create a pie chart showing distribution of winning teams."""
    return px.pie(
        filtered_data,
        names="match_category",
        title="Match Summary",
    )

def create_team1_vs_others_chart(filtered_data, selected_team):
    """Create a bar chart showing performance of selected team vs others."""
    return px.bar(
        filtered_data,
        x="team_2",
        y="team_2_runs",
        color="team_1",
        title=f"Performance of {selected_team} vs Others" if selected_team else "Team 1 vs Others",
        labels={"team_2": "Opponent Team", "team_2_runs": "Runs Scored by Opponent"},
    )

def create_runs_vs_wickets_chart(filtered_data, selected_team, winning_team):
    
    """Create a scatter plot showing runs vs wickets."""
    
    def team_performance_df(filtered_data, selected_team):
        # Filter data for the selected team
        team_data = filtered_data[(filtered_data["team_1"] == selected_team) | (filtered_data["team_2"] == selected_team)]
        
        # Initialize lists to store runs and wickets
        runs_list = []
        wickets_list = []

        # Loop through the filtered data to calculate runs and wickets
        for _, row in team_data.iterrows():
            if row["team_1"] == selected_team:
                runs_list.append(row["team_1_runs"])
                wickets_list.append(row["team_1_wickets"])
            elif row["team_2"] == selected_team:
                runs_list.append(row["team_2_runs"])
                wickets_list.append(row["team_2_wickets"])

        # Create the DataFrame
        return pd.DataFrame({
            "runs": runs_list,
            "wickets": wickets_list
        })
        
    
    if not selected_team:
        data = team_performance_df(filtered_data, winning_team)
    else:
        data = team_performance_df(filtered_data, selected_team)
    
    
    return px.scatter(
        data,
        x="runs",
        y="wickets",
        title=f"Runs vs Wickets of {selected_team}" if selected_team else f"Runs vs Wickets of {winning_team}",
        labels={"runs": "Runs Scored", "wickets": "Wickets Loss"},
    )

def create_venue_performance_chart(filtered_data, selected_team, winning_team):
    
    """Create a bar-plot showing venue-wise performance."""
    
    def venue_performance_df(filtered_data, selected_team):
        # Filter data for the selected team
        team_data = filtered_data[(filtered_data["team_1"] == selected_team) | (filtered_data["team_2"] == selected_team)]
        
        # Initialize lists to store venue-wise data
        venue_list = []
        runs_list = []
        wickets_list = []

        # Loop through the filtered data to calculate runs and wickets by venue
        for venue in team_data["venue"].unique():
            venue_data = team_data[team_data["venue"] == venue]

            # Calculate runs and wickets for the selected team in the current venue
            runs = 0
            wickets = 0

            for _, row in venue_data.iterrows():
                if row["team_1"] == selected_team:
                    runs += row["team_1_runs"]
                    wickets += row["team_2_wickets"]
                elif row["team_2"] == selected_team:
                    runs += row["team_2_runs"]
                    wickets += row["team_1_wickets"]

            # Append data to the lists
            venue_list.append(venue)
            runs_list.append(runs)
            wickets_list.append(wickets)

        # Create the DataFrame
        return pd.DataFrame({
            "Venue": venue_list,
            "Runs": runs_list,
            "Wickets": wickets_list
        })
    
    if not selected_team:
        venue_df = venue_performance_df(filtered_data, winning_team)
        
    else:
        venue_df = venue_performance_df(filtered_data, selected_team)
         
    fig = px.bar(
        venue_df,
        x="Venue",
        y=["Runs", "Wickets"],
        barmode="group",
        title=f"Venue Performance of {selected_team}" if selected_team else f"Venue Performance of {winning_team}",
        labels={"value": "Count", "variable": "Metric"},
        text_auto=True,
    )
    return fig

def register_details_page_callbacks(app):
    """Register callbacks for the Details Page."""
    @app.callback(
        [
            Output("winning-team", "children"),
            Output("total-matches", "children"),
            Output("played-matches", "children"),
            Output("abandoned", "children"),
            Output("match-type-summary-chart", "figure"),
            Output("team-performance-chart", "figure"),
            Output("runs-vs-wickets-chart", "figure"),
            Output("venue-performance-chart", "figure"),
            Output("team-dropdown", "options"),
        ],
        [
            Input("year-dropdown", "value"),
            Input("team-dropdown", "value"),
        ],
    )
    def update_details_page(selected_year, selected_team):
        # Filter the dataset by year
        filtered_data = data[data["world_cup_year"] == selected_year]

        # Get the winning team
        winning_team = (filtered_data[filtered_data["match_category"] == "Final"]["winning_team"].values[0])
        
        played_matches = filtered_data[filtered_data["match_status"] == "played"].shape[0]
        abandoned_matches = filtered_data[filtered_data["match_status"] == "abandoned"].shape[0]
        
        # Total number of matches
        total_matches = filtered_data.shape[0]

        # Populate the team dropdown with unique teams
        unique_teams = pd.concat([filtered_data["team_1"], filtered_data["team_2"]]).unique()
        
        # Generate the charts
        team_performance_chart = create_team_performance_chart(filtered_data)
        category_summary_chart = create_world_cup_match_type_summary_chart(filtered_data)
        runs_vs_wickets_chart = create_runs_vs_wickets_chart(filtered_data, selected_team, winning_team)
        venue_performance_chart = create_venue_performance_chart(filtered_data, selected_team, winning_team)

        return (
            f"Winning Team: {winning_team}",
            f"Total Matches: {total_matches}",
            f"Played Matches: {played_matches}",
            f"Abandoned Matches: {abandoned_matches}",
            category_summary_chart,
            team_performance_chart,
            runs_vs_wickets_chart,
            venue_performance_chart,
            unique_teams,
        )