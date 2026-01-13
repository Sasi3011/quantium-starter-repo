import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load processed data
df = pd.read_csv("output.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")


# Aggregate total sales per day per region
daily_sales = df.groupby(["Date", "Region"], as_index=False).agg({"Sales": "sum"})


# Sort by date
daily_sales = daily_sales.sort_values("Date")

# Create line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    color="Region",
    labels={
        "Date": "Date",
        "Sales": "Total Sales",
        "Region": "Region"
    },
    title="Pink Morsel Sales Over Time"
)

# Add price increase line
price_date = pd.to_datetime("2021-01-15")

fig.add_shape(
    type="line",
    x0=price_date,
    x1=price_date,
    y0=0,
    y1=daily_sales["Sales"].max(),
    line=dict(color="red", dash="dash")
)

fig.add_annotation(
    x=price_date,
    y=daily_sales["Sales"].max(),
    text="Price Increase (15 Jan 2021)",
    showarrow=True,
    arrowhead=1
)

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={"padding": "40px", "fontFamily": "Arial"},
    children=[
        html.H1("Soul Foods – Pink Morsel Sales Visualiser"),
        html.P(
            "This chart shows Pink Morsel sales before and after the price increase on 15 January 2021."
        ),
        dcc.Graph(figure=fig)
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
