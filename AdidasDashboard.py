import streamlit as st
import plotly.express as px

import pandas as pd
import os
import numpy as np
import warnings
warnings.filterwarnings('ignore')

@st.cache_data
def get_data():
    df = pd.read_csv('Adidas.csv')
    return df
df = get_data()


#import sidebar
st.sidebar.header("Please Filter Here")
product = st.sidebar.multiselect(
    "Select the Product",
    options = df['Product'].unique(),
    default = df['Product'].unique())


# Retailer Sidebar
retailer = st.sidebar.radio(
    "Select the Retailer",
    options = df["Retailer"].unique()
)


# Region sidebar
region = st.sidebar.radio(
    "Select the Region",
    options = df['Region'].unique()
)

# SalesMethod sidebar
salesmethod = st.sidebar.radio(
    "Select the Sales Method",
    options = df['SalesMethod'].unique()
)





# Main Page
df_select = df.query(
    "Product ==@product & Retailer ==@retailer & Region ==@region & SalesMethod == @salesmethod "
)


if df_select.empty:
    st.warning("No data availabile based on the current Filter setting")
    st.stop()

st.title("Adidas Sales Dashboard")
st.markdown("##")



# Calculate KPIs
average_price = (df_select["PriceperUnit"].mean() * 100).astype(int)  # Calculate average price in INR
unitssold = df_select.shape[0]  # Get the number of units sold
totalsale = df_select["TotalSales"].sum()  # Calculate total sales
operatingmargin = df_select['OperatingMargin'].mean()  # Mean operating margin
OperatingExpenses = df_select['OperatingExpenses'].mean()

# Create columns for display
first_column, second_column, third_column, forth_column, fifth_column,  = st.columns(5)

with first_column:
    st.markdown("<div class='metric-card'><span class='header-icon'>💰</span> Average Price </div>", unsafe_allow_html=True)
    # st.markdown("<h3 style='font-size:15px;'>Average Price</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='font-size:15px;'>₹ {average_price:,}</h3>", unsafe_allow_html=True)

with second_column:
    st.markdown("<div class='metric-card'><span class='header-icon'>📦</span> No of Units Sold </div>", unsafe_allow_html=True)
    # st.markdown("<h3 style='font-size:15px;'>No of Units Sold</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='font-size:15px;'>{unitssold:,}</h3>", unsafe_allow_html=True)

with third_column:
    st.markdown("<div class='metric-card'><span class='header-icon'>🛒</span> Total Sales </div>", unsafe_allow_html=True)
    #st.markdown("<h3 style='font-size:15px;'>Total Sales</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='font-size:15px;'>₹ {totalsale:,}</h3>", unsafe_allow_html=True)

with forth_column:
    st.markdown("<div class='metric-card'><span class='header-icon'>💸</span> Sales Margin </div>", unsafe_allow_html=True)
    # st.markdown("<h3 style='font-size:15px;'>Sales Margin</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='font-size:15px;'>{operatingmargin:.2f} %</h3>", unsafe_allow_html=True)

with fifth_column:
    st.markdown("<div class='metric-card'><span class='header-icon'>🏦</span> Operating Expenses </div>", unsafe_allow_html=True)
    # st.markdown("<h3 style='font-size:15px;'>Operating Expenses</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='font-size:15px;'>₹ {OperatingExpenses:.2f}</h3>", unsafe_allow_html=True)

    


st.divider()

# Group by city and sum UnitsSold
units_sold_per_city = df_select.groupby(by=['City'])[['UnitsSold']].sum().sort_values(by='UnitsSold')

# Create bar plot
fig_units_sold = px.bar(
    units_sold_per_city,  # Data for the bar plot
    x='UnitsSold',  # Column for x-axis (Total Units Sold)
    y=units_sold_per_city.index,  # Use index for y-axis (Cities)
    orientation='h',  # Horizontal bar
    title="<b>Units Sold per City</b>",
    color_discrete_sequence=['#1f77b4'] * len(units_sold_per_city),
    template="plotly_white"
)

# Update layout
fig_units_sold.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False),
    yaxis_title='City',  # Add title for y-axis (City Names)
    xaxis_title='Total Units Sold',  # Title for x-axis
)

# Group by product and sum UnitsSold
units_sold_per_product = df_select.groupby(by=['Product'])[['UnitsSold']].sum().sort_values(by='UnitsSold')

# Create bar plot
fig_units_sold_product = px.bar(
    units_sold_per_product,  # Data for the bar plot
    x='UnitsSold',  # Column for x-axis (Total Units Sold)
    y=units_sold_per_product.index,  # Use index for y-axis (Products)
    orientation='h',  # Horizontal bar
    title="<b>Units Sold per Product</b>",
    color_discrete_sequence=['#ff7f0e'] * len(units_sold_per_product),  # Change color as needed
    template="plotly_white"
)

# Update layout
fig_units_sold_product.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False),
    yaxis_title='Product',  # Add title for y-axis (Product Names)
    xaxis_title='Total Units Sold',  # Title for x-axis
)


# Group by state and sum UnitsSold
units_sold_per_state = df_select.groupby(by=['State'])[['UnitsSold']].sum().reset_index()

# Create a pie chart for total units sold per state
fig_units_sold_state = px.pie(
    units_sold_per_state, 
    values='UnitsSold',  # Values to plot (Total Units Sold)
    names='State',  # Labels (States)
    title="<b>Total Units Sold per State</b>",  # Title of the chart
    template="plotly_white"
)

# Update layout for the pie chart
fig_units_sold_state.update_layout(
    showlegend=True,
    plot_bgcolor='rgba(0,0,0,0)',
    legend_title="States"
)

# Show the pie chart
# Display the plot in Streamlit

st.plotly_chart(fig_units_sold)
st.plotly_chart(fig_units_sold_product)
st.plotly_chart(fig_units_sold_state)

st.divider()

st.dataframe(df_select)



 




