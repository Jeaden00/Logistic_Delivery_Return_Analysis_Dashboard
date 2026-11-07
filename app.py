
# 1. Import Libraries
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# 2. Dashboard Configuration
st.set_page_config(
    page_title="Logistics, Delivery & Returns Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}

h1 {
    margin-top: 0rem;
    padding-top: 0rem;
}

[data-testid="stPlotlyChart"] {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("Logistics, Delivery & Returns Insights")
st.caption("Delivery Performance | Shipment Analysis | Returns Insights")

# 3. Load Cleaned Datasets
data_path = Path(__file__).resolve().parent / "cleaned_data"

customers = pd.read_csv(data_path / "customers.csv")
products = pd.read_csv(data_path / "products.csv")
orders = pd.read_csv(data_path / "orders.csv")
order_items = pd.read_csv(data_path / "order_items.csv")
payments = pd.read_csv(data_path / "payments.csv")
shipments = pd.read_csv(data_path / "shipments.csv")
returns = pd.read_csv(data_path / "returns.csv")



# 4. Calculate Delivery and Returns KPIs

total_orders = orders["order_id"].nunique()
total_shipments = shipments["shipment_id"].nunique()
total_returns = returns["return_id"].nunique()

# Standardize shipment status for calculations
shipment_status = (
    shipments["shipment_status"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.lower()
)

delivered_count = (shipment_status == "delivered").sum()
in_transit_count = (shipment_status == "in transit").sum()
lost_count = (shipment_status == "lost").sum()

delivered_pct = delivered_count / total_shipments * 100
in_transit_pct = in_transit_count / total_shipments * 100
lost_pct = lost_count / total_shipments * 100

return_rate = (
    returns["order_id"].nunique() / total_orders * 100
)


# 5 Use valid delivery lead times only

lead_times = pd.to_numeric(
    shipments["valid_delivery_lead_time"],
    errors="coerce"
).dropna()

avg_lead_time = lead_times.mean()


#5 DISPLAY KPIs - STYLED KPI CARDS


st.subheader("Delivery & Returns KPI Summary")

col1, col2, col3, col4 = st.columns(4)

kpi_cards = [
    ("Total Orders", f"{total_orders:,}"),
    ("Delivery Success", f"{delivered_pct:.1f}%"),
    ("Avg. Lead Time", f"{avg_lead_time:.1f} days"),
    ("Return Rate", f"{return_rate:.1f}%")
]

for col, (label, value) in zip(
    [col1, col2, col3, col4], kpi_cards
):
    with col:
        st.markdown(
            f"""
            <div style="
                background-color: #E8F0F8;
                padding: 20px;
                border-radius: 10px;
                min-height: 105px;
                box-sizing: border-box;
            ">
                <div style="
                    color: #183B5B;
                    font-size: 15px;
                    font-weight: 600;
                    margin-bottom: 12px;
                ">
                    {label}
                </div>
                <div style="
                    color: #183B5B;
                    font-size: 30px;
                    font-weight: 700;
                    line-height: 1.2;
                ">
                    {value}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# 6. Chart 1 - Delivery Lead Time Distribution


lead_time_counts = (
    lead_times
    .value_counts()
    .sort_index()
    .rename_axis("Delivery Lead Time (Days)")
    .reset_index(name="Number of Shipments")
)

fig1 = px.bar(
    lead_time_counts,
    x="Delivery Lead Time (Days)",
    y="Number of Shipments",
    text="Number of Shipments"
)

fig1.update_layout(
    height=420,
    autosize=True,
    font=dict(size=16, color="#183B5B"),
    title=dict(font=dict(size=24)),
    xaxis=dict(
        title=dict(text="Delivery Lead Time (Days)", font=dict(size=18)),
        tickfont=dict(size=16),
        automargin=True
    ),
    yaxis=dict(
        title=dict(text="Number of Shipments", font=dict(size=18)),
        tickfont=dict(size=16),
        rangemode="tozero",
        automargin=True
    ),
    margin=dict(l=65, r=20, t=15, b=45),
    showlegend=False
)

fig1.update_traces(
    texttemplate="%{y:,}",
    textposition="outside",
    textfont=dict(size=14)
)


# 7. Chart 2 - Courier Delivery Success Rate

courier_summary = shipments.groupby("courier").agg(
    Total_Shipments=("shipment_id", "nunique"),
    Delivered_Shipments=(
        "shipment_status",
        lambda x: (
            x.astype(str).str.strip().str.lower() == "delivered"
        ).sum()
    )
).reset_index()

courier_summary["Delivery Success Rate (%)"] = (
    courier_summary["Delivered_Shipments"]
    / courier_summary["Total_Shipments"] * 100
)

courier_chart = courier_summary.sort_values(
    "Delivery Success Rate (%)",
    ascending=True
)


#  Chart 2 - Courier Delivery Success Rate

fig2 = px.bar(
    courier_chart,
    x="Delivery Success Rate (%)",
    y="courier",
    orientation="h",
    text="Delivery Success Rate (%)"
)


fig2.update_layout(
    height=420,
    font=dict(size=16, color="#183B5B"),
    xaxis=dict(
        title=dict(text="Delivery Success Rate (%)", font=dict(size=18)),
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        title=dict(text="Courier", font=dict(size=18)),
        tickfont=dict(size=16)
    ),
    margin=dict(l=80, r=40, t=20, b=55),
    showlegend=False
)


fig2.update_xaxes(
    range=[0, 100],
    ticksuffix="%"
)
fig2.update_traces(
    texttemplate="%{x:.1f}%",
    textposition="outside",
    textfont=dict(size=16)
)

# Display Charts 1 and 2 side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("Chart 1 - Delivery Lead Time Distribution")
    st.plotly_chart(
        fig1,
        use_container_width=True,
        height=240
    )

with col2:
    st.subheader("Chart 2 - Courier Delivery Success Rate")
    st.plotly_chart(
        fig2,
        use_container_width=True,
        height=240
    )



# 8. CHART 3 - MONTHLY SHIPMENT DELIVERY PERFORMANCE


# 8.1. Prepare shipment data
monthly_shipments = shipments.copy()

monthly_shipments["ship_date"] = pd.to_datetime(
    monthly_shipments["ship_date"],
    errors="coerce",
    dayfirst=True
)

monthly_shipments = monthly_shipments.dropna(
    subset=["ship_date"]
)

# 8.2. Standardize shipment status
monthly_shipments["shipment_status"] = (
    monthly_shipments["shipment_status"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# 8.3. Extract year and month
monthly_shipments["Year"] = (
    monthly_shipments["ship_date"].dt.year
)

monthly_shipments["Month"] = (
    monthly_shipments["ship_date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

# 8.4. Remove duplicate shipment records
monthly_shipments = monthly_shipments.drop_duplicates(
    subset=["shipment_id"]
)

# 8.5. Year filter
available_years = sorted(
    monthly_shipments["Year"].unique()
)

selected_year = st.selectbox(
    "Select Year",
    ["All Years"] + available_years,
    key="monthly_delivery_year"
)

# 8.6. Apply year filter
if selected_year != "All Years":
    filtered_shipments = monthly_shipments[
        monthly_shipments["Year"] == selected_year
    ].copy()
else:
    filtered_shipments = monthly_shipments.copy()

# 8.7. Identify delivered shipments
filtered_shipments["Delivered_Flag"] = (
    filtered_shipments["shipment_status"] == "delivered"
).astype(int)

# 8.8. Calculate monthly shipment performance
monthly_performance = (
    filtered_shipments.groupby("Month")
    .agg(
        Total_Shipments=("shipment_id", "nunique"),
        Delivered_Shipments=("Delivered_Flag", "sum")
    )
    .reset_index()
)

# 9. Calculate delivery success rate
monthly_performance["Delivery Success Rate (%)"] = (
    monthly_performance["Delivered_Shipments"]
    / monthly_performance["Total_Shipments"] * 100
)

# 8.10. Create readable month-year labels
monthly_performance["Month_Label"] = (
    monthly_performance["Month"].dt.strftime("%b %Y")
)

# 8.11. Create combo chart
fig6 = go.Figure()

# Blue bars - Number of delivered shipments

fig6.add_trace(
    go.Bar(
        x=monthly_performance["Month_Label"],
        y=monthly_performance["Delivered_Shipments"],
        name="Delivered Shipments",
        marker_color="#1976D2",
        text=monthly_performance["Delivered_Shipments"],
        textposition="outside",
        textfont=dict(size=16, color="#183B5B"),
        cliponaxis=False,
        yaxis="y"
    )
)

# Orange line - Delivery success rate
fig6.add_trace(
    go.Scatter(
        x=monthly_performance["Month_Label"],
        y=monthly_performance["Delivery Success Rate (%)"],
        name="Delivery Success Rate",
        mode="lines+markers",
        line=dict(
            color="#E67E22",
            width=2
        ),
        marker=dict(size=8),
        hovertemplate=(
            "Month: %{x}<br>"
            "Delivery Success Rate: %{y:.1f}%"
            "<extra></extra>"
        ),
        yaxis="y2"
    )
)

# 8.12. Select every second month label
visible_months = monthly_performance["Month_Label"].iloc[::2].tolist()

# 8.13. Chart layout
fig6.update_layout(
    height=420,
    font=dict(size=16, color="#183B5B"),

    xaxis=dict(
        title=dict(text="Month", font=dict(size=18)),
        type="category",
        tickmode="array",
        tickvals=visible_months,
        tickangle=-45,
        tickfont=dict(size=16),
        range=[-0.5, len(monthly_performance) - 0.5]
    ),

    yaxis=dict(
        title=dict(
            text="Number of Delivered Shipments",
            font=dict(size=18)
        ),
        tickfont=dict(size=16),
        rangemode="tozero"
    ),

    yaxis2=dict(
        title=dict(
            text="Delivery Success Rate (%)",
            font=dict(size=18)
        ),
        tickfont=dict(size=16),
        overlaying="y",
        side="right",
        range=[0, 100],
        dtick=25,
        ticksuffix="%"
    ),

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.0,
        xanchor="center",
        x=0.8,
        font=dict(size=16)
    ),

    margin=dict(l=65, r=65, t=50, b=75),
    hovermode="x unified"
)


# 9. Chart 4 - Shipment Status Breakdown

status_summary = (
    shipments["shipment_status"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
    .value_counts()
    .rename_axis("Shipment Status")
    .reset_index(name="Number of Shipments")
)

fig3 = px.bar(
    status_summary,
    x="Shipment Status",
    y="Number of Shipments",
    text="Number of Shipments"
)


fig3.update_layout(
    height=420,
    font=dict(size=18, color="#183B5B"),
    xaxis=dict(
        title=dict(text="Shipment Status", font=dict(size=18)),
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        title=dict(text="Number of Shipments", font=dict(size=18)),
        tickfont=dict(size=16),
        rangemode="tozero"
    ),
    margin=dict(l=60, r=30, t=30, b=50),
    showlegend=False
)



fig3.update_traces(
    textposition="outside",
    texttemplate="%{y:,}",
    textfont=dict(size=16, color="#183B5B")
)


# Display Charts 3 and 4 side by side
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Chart 3 - Monthly Shipment Delivery Performance")
    st.plotly_chart(
        fig6,
        use_container_width=True,
        height=260
    )

with chart_col2:
    st.subheader("Chart 4 - Shipment Status Breakdown")
    st.plotly_chart(
        fig3,
        use_container_width=True,
        height=240
    )


# 10. Chart 5 - Top Return Reasons

return_reasons = (
    returns["reason"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .value_counts()
    .head(10)
    .sort_values(ascending=False)
    .rename_axis("Return Reason")
    .reset_index(name="Number of Returns")
)

fig4 = px.bar(
    return_reasons,
    x="Return Reason",
    y="Number of Returns",
    text="Number of Returns"
)

fig4.update_layout(
    height=420,
    font=dict(size=16, color="#183B5B"),
    xaxis=dict(
        title=dict(text="Return Reason", font=dict(size=18)),
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        title=dict(text="Number of Returns", font=dict(size=18)),
        tickfont=dict(size=16),
        rangemode="tozero"
    ),
    margin=dict(l=60, r=30, t=30, b=100),
    showlegend=False
)



fig4.update_xaxes(tickangle=-30)

fig4.update_traces(
    textposition="outside",
    texttemplate="%{y:,}",
    textfont=dict(size=16, color="#183B5B")
)


# 11. Chart 6 - Return Rate by Category

# Get unique returned orders
returned_orders = returns[["order_id"]].drop_duplicates()

# Link returned orders to order items
returned_items = returned_orders.merge(
    order_items,
    on="order_id",
    how="inner"
)

# Link items to product categories
returned_items = returned_items.merge(
    products[["product_id", "category"]],
    on="product_id",
    how="left"
)

# Count unique returned orders per category
returned_by_category = (
    returned_items.groupby("category")["order_id"]
    .nunique()
)

# Count all unique orders per category
total_by_category = (
    order_items.merge(
        products[["product_id", "category"]],
        on="product_id",
        how="left"
    )
    .groupby("category")["order_id"]
    .nunique()
)

# Calculate return rate
category_return_rate = (
    returned_by_category / total_by_category * 100
).fillna(0).reset_index(name="Return Rate (%)")

category_return_rate = category_return_rate.sort_values(
    "Return Rate (%)",
    ascending=False
)

# Create chart
fig5 = px.bar(
    category_return_rate,
    x="category",
    y="Return Rate (%)",
    text="Return Rate (%)"
)

fig5.update_layout(
    height=420,
    font=dict(size=16, color="#183B5B"),
    xaxis=dict(
        title=dict(text="Product Category", font=dict(size=18)),
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        title=dict(text="Return Rate (%)", font=dict(size=18)),
        tickfont=dict(size=16),
        rangemode="tozero"
    ),
    margin=dict(l=60, r=30, t=30, b=50),
    showlegend=False
)



fig5.update_traces(
    texttemplate="%{y:.1f}%",
    textposition="outside",
    textfont=dict(size=16, color="#183B5B")
)


# 12. Display Charts 5 and 6 side by side
chart_col5, chart_col6 = st.columns(2)

with chart_col5:
    st.subheader("Chart 5 - Top Return Reasons")
    st.plotly_chart(
        fig4,
        use_container_width=True,
        height=240
    )

with chart_col6:
    st.subheader("Chart 6 - Return Rate by Product Category")
    st.plotly_chart(
        fig5,
        use_container_width=True,
        height=240
    )




# 13. Key Insights and Practical Recommendations

insights = [
    "Delivery success rate is 77.9%, indicating that approximately 22.1% of shipments were not recorded as delivered.",
    "Of 15,000 shipments, 18.0% are in transit, 3.1% are returned to sender, and 1.1% are lost.",
    "Average delivery lead time is 4 days, with valid delivery records ranging from 1 to 7 days.",
    "Courier delivery success rates are relatively close, at approximately 77–79%.",
    "Changed Mind (182), Defective (178), and Missing Parts (175) are the three most frequent return reasons.",
    "Home & Kitchen has the highest associated return rate at 8.6%, while Groceries has the lowest at 7.5%."
]

recommendations = [
    (
        "1. Improve Delivery Performance",
        "Investigate shipments that remain in transit, are returned to sender, "
        "or are classified as lost. Review courier performance and delivery "
        "exceptions to improve delivery success."
    ),
    (
        "2. Reduce Product Returns",
        "Investigate the leading return reasons and review product descriptions, "
        "packaging, quality checks, and completeness of shipped items. "
        "Prioritize monitoring of Home & Kitchen."
    )
]

insights_html = "".join(
    f'<li>{item}</li>' for item in insights
)

recommendations_html = "".join(
    f'<li><strong>{title}:</strong> {description}</li>'
    for title, description in recommendations
)

col_insights, col_recommendations = st.columns(2)

with col_insights:
    st.markdown(
        f"""
        <div style="
            background-color: #EAF2F8;
            padding: 16px 20px;
            border-radius: 12px;
            min-height: 0;
            color: #183B5B;
        ">
            <h3 style="font-size: 20px; margin: 0 0 3px 0; padding: 0;">
            Key Insights
            </h3>
            <ul style="
                font-size: 16px;
                line-height: 1.5;
                padding-left: 20px;
                margin: 0;
            ">
                {insights_html}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col_recommendations:
    st.markdown(
        f"""
        <div style="
            background-color: #EAF2F8;
            padding: 22px;
            border-radius: 12px;
            min-height: 0px;
            color: #183B5B;
        ">
            <h3 style="font-size: 20px; margin: 0 0 6px 0;">
                Practical Recommendations
            </h3>
            <ul style="
                font-size: 15px;
                line-height: 1.5;
                padding-left: 22px;
                margin: 0;
            ">
                {recommendations_html}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
