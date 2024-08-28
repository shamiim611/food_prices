
import streamlit as st
import pandas as pd
import plotly.express as px

file_path ='C:/Users/HP/Documents/Python Scripts/global_food_prices.zip'
data = pd.read_csv(file_path, compression ='zip', encoding ='latin1' )

# Rename 'adm0_name' to 'country'
data.rename(columns={'adm0_name': 'country'}, inplace=True)

# Streamlit app
st.title("Global Food Prices Exploratory Data Analysis")
st.markdown("This app allows you to interactively explore the global food prices dataset.")

# Sidebar options for filtering
st.sidebar.header("Filter Options")

# Filter by country
countries = sorted(data['country'].unique())
selected_countries = st.sidebar.multiselect('Select countries', countries, default=countries)

# Filter by commodity
commodities = sorted(data['cm_name'].unique())
selected_commodities = st.sidebar.multiselect('Select commodities', commodities, default=commodities)

# Filter by year range
years = sorted(data['mp_year'].unique())
selected_years = st.sidebar.slider('Select year range', min_value=min(years), max_value=max(years), value=(min(years), max(years)))

# Filter the dataset based on the selected filters
filtered_data = data[
    (data['country'].isin(selected_countries)) &
    (data['cm_name'].isin(selected_commodities)) &
    (data['mp_year'] >= selected_years[0]) &
    (data['mp_year'] <= selected_years[1])
]

# Show a summary of the filtered dataset
st.write(f"### Summary of Filtered Data ({len(filtered_data)} rows)")
st.dataframe(filtered_data.head())

# Visualize the count of price types for the selected countries and commodities
st.write("### Count of Price Types by Country and Commodity")
pt_counts = filtered_data.groupby(['country', 'pt_name']).size().reset_index(name='count')
fig1 = px.bar(pt_counts, 
              x='country', 
              y='count', 
              color='pt_name', 
              title='Count of Price Types by Country and Commodity',
              labels={'country': 'Country', 'count': 'Count', 'pt_name': 'Price Type'},
              barmode='group')
st.plotly_chart(fig1)

# Visualize average price of commodities over time
st.write("### Average Price of Commodities Over Time")
avg_price = filtered_data.groupby(['mp_year', 'cm_name'])['mp_price'].mean().reset_index()
fig2 = px.line(avg_price, 
               x='mp_year', 
               y='mp_price', 
               color='cm_name', 
               title='Average Price of Commodities Over Time',
               labels={'mp_year': 'Year', 'mp_price': 'Average Price', 'cm_name': 'Commodity'})
st.plotly_chart(fig2)

# Visualize price distribution
st.write("### Price Distribution by Country and Commodity")
fig3 = px.box(filtered_data, 
              x='country', 
              y='mp_price', 
              color='cm_name', 
              title='Price Distribution by Country and Commodity',
              labels={'country': 'Country', 'mp_price': 'Price', 'cm_name': 'Commodity'})
st.plotly_chart(fig3)

# Additional statistics
st.write("### Descriptive Statistics")
st.write(filtered_data.describe())
