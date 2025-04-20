import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.set_page_config(page_title="EV Dashboard", layout="wide")
st.title("Electric Vehicle Population Dashboard")

df = pd.read_csv("Electric_Vehicle_Population_Data.csv")


l,r=st.columns([1,1])
colors=['#1B4965','#62B6CB']

with l:
    # EV Type Distribution over all the years
    st.subheader("EV Type Distribution")
    vehicle_type_counts = df['Electric Vehicle Type'].value_counts().reset_index()
    vehicle_type_counts.columns = ['Vehicle Type', 'Count']
    
    fig = px.pie(
        vehicle_type_counts,
        names='Vehicle Type',
        values='Count',
        title='Battery Electric vs. Plug-in Hybrid Distribution',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    st.plotly_chart(fig, use_container_width=True)

with r:
    # Electric Utility Distribution by Make and Year
    st.subheader("Electric Utility Distribution")
    
    unique_makes = sorted(df['Make'].dropna().unique())
    selected_make = st.selectbox("Select Make", unique_makes)
   
    filtered_by_make = df[df['Make'] == selected_make]
    
    available_years = sorted(filtered_by_make['Model Year'].dropna().unique())
    selected_year = st.selectbox("Select Year", available_years)
    
    filtered_df = filtered_by_make[filtered_by_make['Model Year'] == selected_year]
    
    utility_counts = filtered_df['Electric Utility'].value_counts().reset_index()
    utility_counts.columns = ['Electric Utility', 'Count']
    
    fig_util = px.bar(
        utility_counts,
        x='Electric Utility',
        y='Count',
        title=f"Electric Utility Distribution for {selected_make} ({selected_year})",
        color_discrete_sequence=['#0077cc'],
        labels={'Count': 'Number of Vehicles'}
    )
    st.plotly_chart(fig_util, use_container_width=True)

with l:
    # Vehicle Production Distribution
    st.subheader("Vehicle Production by Make")
    
    all_years = sorted(df['Model Year'].dropna().unique())
    selected_year_prod = st.selectbox("Select Year for Make Distribution", all_years, key="prod_year_select")
   
    year_df = df[df['Model Year'] == selected_year_prod]
    make_counts=year_df['Make'].value_counts().reset_index()
    make_counts.columns=['Make','Count']
    
    fig_make_pie = px.pie(
        make_counts,
        names='Make',
        values='Count',
        title=f'Vehicle Production Distribution by Make in {selected_year_prod}',
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    fig_make_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')
    
    st.plotly_chart(fig_make_pie, use_container_width=True)
    
with l:
    #Electric Range of top N Makers
    st.subheader("Electric Range of top N Makes")
    
    df = df[df['Electric Range'].notnull()]
    df = df[df['Model Year'].notnull()]

    top_n = st.slider("Select number of top Makes", 2, 10, 5)
    top_makes = df['Make'].value_counts().head(top_n).index.tolist()
    
    filtered = df[df['Make'].isin(top_makes)]
    
    grouped = filtered.groupby(['Model Year', 'Make'], as_index=False)['Electric Range'].mean()
    
    chart = alt.Chart(grouped).mark_bar().encode(
        y=alt.Y('Model Year:O', title='Model Year'),
        x=alt.X('Electric Range:Q', title='Avg Electric Range'),
        color='Make:N',
        column='Make:N',  
        tooltip=['Model Year', 'Make', 'Electric Range']
    ).properties(
        title=f'avg electric range of top {top_n} makes',
        width=100,
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)
   
   