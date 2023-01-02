import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout='wide', page_title='Startup Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['date']= pd.to_datetime(df['date'], errors = 'coerce')
df['month']= df['date'].dt.month
df['month']= df['month'].fillna(0)
df['month']= df['month'].astype(np.int64)
df['year'] = df['date'].dt.year
df['year']= df['year'].fillna(0)
df['year']= df['year'].astype(np.int64)


def load_startup_analysis(startup):
    col1, col2, col3 = st.columns([1,2,2])
    with col1:
        st.metric("Name of Startup", startup)
    with col2:
        startup_verti = str(df[df['startup'].str.contains(startup)].head()[
            ['date', 'vertical', 'subvertical', 'city', 'round', 'amount']]['vertical'].values[0])
        st.metric("Type of Industry", startup_verti)
    with col3:
        startup_subverti = str(df[df['startup'].str.contains(startup)].head()[
                                ['date', 'vertical', 'subvertical', 'city', 'round', 'amount']]['subvertical'].values[0])
        st.metric("Type of Subindustry", startup_subverti)

    col4, col5, col6 = st.columns([1,2,2])
    with col4:
        startup_city = str(df[df['startup'].str.contains(startup)].head()[
                                ['date', 'vertical', 'subvertical', 'city', 'round', 'amount']]['city'].values[0])
        st.metric("Location of Startup", startup_city)

    with col5:
        startup_investor =str(df[df['startup'].str.contains(startup)].head()[['investors']]['investors'].values[0])
        st.metric("Name of Investor", startup_investor)
    with col6:
        startup_round = str(df[df['startup'].str.contains(startup)].head()[['round']]['round'].values[0])
        st.metric("Type of Investment", startup_round)



def load_overall_analysis():
    st.title("Overall Analysis")
#TOTAL OVER ANALYSIS
    total = round(df['amount'].sum())
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    average_funding = round(df.groupby('startup')['amount'].sum().mean())
    num_startups = df['startup'].nunique()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric("total investment", str(total) + 'Cr')
    with col2:
        st.metric("Maximum investment", str(max_funding) + 'Cr')
    with col3:
        st.metric("Average Investment", str(average_funding) + 'Cr')
    with col4:
        st.metric("Total Startups invested in", num_startups)

    col5,col6 = st.columns(2)
    with col5:
        st.header('MoM Graph')
        selected_option = st.selectbox('Select Type',['Total','Count'])
        if selected_option== 'Total':
            temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        else:
            temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

        temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        fig5, ax5 = plt.subplots()
        ax5.plot(temp_df['x-axis'], temp_df['amount'])
        st.pyplot(fig5)

    with col6:
        st.header('Top Sector having Max Investment')
        selected_option1 = st.selectbox('Select Type1', ['Total1', 'Count1'])
        if selected_option1 == 'Total1':
            temp1_df = df.groupby('vertical')['amount'].sum().sort_values(ascending= False).head(10)
        else:
            temp1_df = df.groupby('vertical')['amount'].count().sort_values(ascending= False).head(10)
        fig6, ax6 = plt.subplots()
        ax6.pie(temp1_df, labels= temp1_df.index)
        st.pyplot(fig6)
    col7, col8,col9 = st.columns(3)
    with col7:
        st.header('Funding in Top 20 Cities')
        df_city= df.groupby('city')['round'].count().sort_values(ascending=False).head(20)
        st.bar_chart(df_city)
    with col8:
        st.header('Type Of Funding')
        df_funding =df.groupby('round')['startup'].count().sort_values(ascending= False).head(15)
        st.line_chart(df_funding)
    with col9:
        st.header('Top Startups')
        startup_series = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10).index
        st.write(startup_series)

    col10, col11 = st.columns(2)
    with col10:
        st.header('Top Investors')
        sr_investors = df.groupby('investors')['amount'].count().sort_values(ascending=False).head(10)
        st.area_chart(sr_investors)

def load_investor_details(investor):
    st.title(investor)
#load the recent five investment
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1,col2, col3 = st.columns(3)
    with col1:
     #big investements
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending= False).head()
        st.subheader('Top Five Biggest Investments')
        fig,ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('sector invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index)


        st.pyplot(fig1)

    with col3:

        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()

        st.subheader('stage')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels= round_series.index)


        st.pyplot(fig2)

    col4, col5 = st.columns(2)

    with col4:

        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()

        st.subheader('city invested in')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index)


        st.pyplot(fig3)

    with col5:
        df['year'] = df['date'].dt.year
        year_series= df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('YoY investments')
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)

        st.pyplot(fig4)

st.title('Startup Dashboard')


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])
if option == 'Overall Analysis':
    load_overall_analysis()


elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('StartUp Analysis')
    if btn1:
        load_startup_analysis(selected_startup)
    
else:
    selected_investor = st.sidebar.selectbox('Select Startup', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)






