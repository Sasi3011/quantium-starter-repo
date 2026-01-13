import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("output.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

# Aggregate daily sales
daily_sales = df.groupby(["Date", "Region"], as_index=False).agg({"Sales": "sum"})
daily_sales = daily_sales.sort_values("Date")

app = dash.Dash(__name__)

# -------------------- Layout --------------------
app.layout = html.Div(
    style={
        "backgroundColor": "#0f172a",
        "minHeight": "100vh",
        "padding": "40px",
        "color": "white",
        "fontFamily": "Segoe UI, Arial",
    },
    children=[

        html.H1("Soul Foods – Pink Morsel Sales Visualiser",
                style={"textAlign": "center", "color": "#38bdf8"}),

        html.P(
            "Explore how Pink Morsel sales changed before and after the price increase on 15 January 2021.",
            style={"textAlign": "center", "color": "#cbd5e1"}
        ),

        html.Div(
            style={
                "marginTop": "30px",
                "marginBottom": "30px",
                "display": "flex",
                "justifyContent": "center",
                "gap": "20px"
            },
            children=[
                html.Label("Select Region:", style={"fontWeight": "bold"}),

                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={"color": "#38bdf8", "fontSize": "18px"}
                )
            ]
        ),

        dcc.Graph(id="sales-graph")
    ]
)

# -------------------- Callback --------------------
@app.callback(
    Output("sales-graph", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):

    if selected_region == "all":
        filtered = daily_sales
    else:
        filtered = daily_sales[daily_sales["Region"] == selected_region]

    fig = px.line(
        filtered,
        x="Date",
        y="Sales",
        color="Region",
        title="Pink Morsel Sales Over Time",
        labels={
            "Date": "Date",
            "Sales": "Total Sales",
            "Region": "Region"
        }
    )

    price_date = pd.to_datetime("2021-01-15")

    fig.add_shape(
        type="line",
        x0=price_date,
        x1=price_date,
        y0=0,
        y1=filtered["Sales"].max(),
        line=dict(color="red", dash="dash")
    )

    fig.add_annotation(
        x=price_date,
        y=filtered["Sales"].max(),
        text="Price Increase (15 Jan 2021)",
        showarrow=True,
        arrowhead=1
    )

    fig.update_layout(
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="white"),
        title_font_color="#38bdf8"
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
