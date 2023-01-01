import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout='wide', page_title='startup Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['date']= pd.to_datetime(df['date'], errors = 'coerce')
df['month']= df['date'].dt.month
df['month']= df['month'].fillna(0)
df['month']= df['month'].astype(np.int64)
df['year'] = df['date'].dt.year
df['year']= df['year'].fillna(0)
df['year']= df['year'].astype(np.int64)
df['vertical']= df['vertical'].replace(['ECommerce'],'eCommerce')
df['vertical']= df['vertical'].replace(['E-Commerce'],'eCommerce')
df['vertical']= df['vertical'].replace(['ecommerce'],'eCommerce')

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
        st.header('Location of cities')
        sr_city = df.groupby('city')['round'].count().sort_values(ascending=False).head(15)
        df_city = sr_city.to_frame()
        df_city = df_city.assign(
            lat=[12.120000, 19.155001, 28.679079, 30.172716, 12.120000, 18.5204, 17.3850, 13.0827, 28.5355, 30.172716,
                 22.728392, 26.9124, 28.679079, 22.5726, 22.7196],
            lon=[76.680000, 72.849998, 77.069710, 77.299492, 76.680000, 73.8567, 78.4867, 80.2707, 77.3910, 77.299492,
                 71.637077, 75.7873, 77.069710, 88.3639, 75.8577])
        st.map(df_city)
    col10, col11 = st.columns(2)
    with col10:
        st.header('Top Investors')
        sr_investors = df.groupby('investors')['amount'].count().sort_values(ascending=False).head(10)
        st.area_chart(sr_investors)
    with col11:
        st.header('Top Startups')
        startup_series= df.groupby('startup')['amount'].sum().sort_values(ascending= False).head(10).index
        st.write(startup_series)
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
    st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('StartUp Analysis')
    
else:
    selected_investor = st.sidebar.selectbox('Select Startup', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)






