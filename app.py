import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='startup Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['date']= pd.to_datetime(df['date'], errors = 'coerce')

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
    st.title('Overall Analysis')

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('StartUp Analysis')
    
else:
    selected_investor = st.sidebar.selectbox('Select Startup', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)






