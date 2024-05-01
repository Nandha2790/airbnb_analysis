import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import io
from scipy import stats

st.set_page_config(layout="wide")

col1,col2 = st.columns([1,2])

col1.image(image="Airbnb_logo.png",width=300)

col2.title("Airbnb Analysis")

df_with_outlier = pd.read_csv("airbnb.csv")
df= pd.read_csv("airbnb_without_outlier.csv")

selected = option_menu (
    menu_title=None,
    options= ['About Airbnb','Home','EDA','Descriptive Analysis'],
    icons= ['house','house','search','chart_with_upwards_trend'],
    orientation='horizontal'
                        )

if selected == 'About Airbnb':
    
    st.markdown("# What is Airbnb?")
    st.markdown(""" 
                
                - ### Airbnb (ABNB) is an online marketplace that connects people who want to rent out their homes with people looking for accommodations in specific locales. 
                - ### The company has come a long way since 2007, when its co-founders first came up with the idea to invite paying guests to sleep on an air mattress in their living room. 
                - ### According to Airbnb's latest data, it now has more than 7 million listings, covering some 100,000 cities and towns in 220-plus countries and regions worldwide.
                
                """)
    
    st.caption("Source-Investopedia")
    
    st.markdown(" # Project objective:")
    
    st.markdown(""" 
                
                - ### This project aims to collect sample data from MongoDB Atlas and preprocess it to create structured data.
                - ### This structured data undergoes an Exploratory Data Analysis (EDA) process to ensure it is free of missing values and outliers.
                - ### The data is then converted to a CSV file and imported into a Streamlit application to visualize the insights derived from it.
                
                """)
    
    st.markdown("# Steps Involved in This Project:")

    st.markdown(""" 
                - ### Obtain the connection string from MongoDB Atlas
                - ### Connect with MongoDB Compass on the local desktop to download the JSON file
                - ### Create a new database in MongoDB Compass and import the JSON file into a sample collection for efficient data retrieval
                - ### Preprocess the data in Jupyter Notebook to structure the data
                - ### Conduct Exploratory Data Analysis (EDA)
                - ### Treat missing values and outliers
                - ### Export the data without outliers and missing values for further analysis
                - ### Create a Streamlit web application using this CSV file and display the insights derived from it
                
                """)   


if selected == 'Home':
    
    col1,col2 = st.columns(2)

    country_list = col1.selectbox( "Country List", df['country'].unique())

    prop_list = col2.selectbox('Property Type',df['property_type'].unique())    

    df2 = df[ (df["country"] == country_list) & (df["property_type"] == prop_list)]
    
    df3 = df[ (df["country"] == country_list)]
        
    max_price = df2['price'].max()
    avg_price = round(df2['price'].mean(),0)
    min_price = df2['price'].min()
    max_price_diff = round(((max_price-avg_price)/avg_price) * 100,0)
    avg_price_diff = round(((avg_price-avg_price)/avg_price) * 100,0)
    min_price_diff = round(((min_price-avg_price)/avg_price) * 100,0)
    
    st.subheader("Price fluctuation")

    col1,col2,col3 = st.columns(3)
    col1.container(border=True).metric(f"Maximum Price - {prop_list}",max_price,f'{max_price_diff}%')
    col2.container(border=True).metric(f"Avgerage Price - {prop_list}",avg_price,f'{avg_price_diff}%')
    col3.container(border=True).metric(f"Minimun Price - {prop_list}",min_price,f'{min_price_diff}%')
    
    col1,col2 = st.columns([2,1])

    fig_rtype = px.pie( 
                df3,
                values='price',
                names='room_type',
                title=f"{country_list} - Price sharing by property types",
                height=700)
    
    fig_rtype.update_traces(textinfo='percent+label')
    
    col2.container(border=True).plotly_chart(fig_rtype,use_container_width=True)    
    
    fig_prop = px.bar( 
                df3,
                x='property_type',
                y='price',
                color='room_type',
                title=f" {country_list}- Room Type and Property Type",
                height=700)

    col1.container(border=True).plotly_chart(fig_prop,use_container_width=True)
    
    
    
    df5 = df2[ ['name','host_name','price','bedrooms','beds','cleaning_fee','guests_included','maximum_nights','minimum_nights','property_type','room_type','street']].reset_index(drop=True)
    
    st.subheader(f"{country_list} - List of {prop_list} Below Average Price")
    st.dataframe(df5[ ( df5['price'] <= df2['price'].mean())],use_container_width=True,hide_index=True)

    st.subheader(f"{country_list} - List of {prop_list} Above Average Price")
    st.dataframe(df5[ ( df5['price'] > df2['price'].mean())],use_container_width=True,hide_index=True)
    
    st.subheader("map")

    st.map(df2)
    
if selected == 'EDA':
    
    st.dataframe(df_with_outlier.head())
    
    buffer = io.StringIO()
    df_with_outlier.info(buf=buffer)
    info = buffer.getvalue()    
    st.subheader("Dataframe info")  
    st.text(info) 
    
    st.markdown( "## Missing Value")
    st.text(df.isnull().sum())
    
    st.markdown( "## Finding the ouliers for each property types on the listed conuntry")
    
    col1,col2 = st.columns(2)
    with col1.container(border=True):
        st.subheader("Dataframe Shape-With outlier")
        st.text(df_with_outlier.shape)   
    
    with col2.container(border=True):
        st.subheader("Dataframe Shape-Without outlier")
        st.text(df.shape)  

    country_list = list(df_with_outlier['country'].unique())
    
    
    
    st.header("Checking the Price with Each Property for outlier")

    prop = list(df_with_outlier['property_type'].unique())
    
    for country in country_list:
        with st.expander(f"{country}"):
            df1_prop = df_with_outlier[ (df_with_outlier['country'] == country)]
            df1_prop_without_outlier = df[ (df['country'] == country)]
            prop = list(df1_prop['property_type'].unique())            
            for p in prop:
                col1,col2= st.columns(2)
                col3,col4= st.columns(2)
                df2_prop = df1_prop[ (df1_prop['property_type'] == p)]
                df2_prop_without_outlier = df1_prop_without_outlier[ (df1_prop_without_outlier['property_type'] == p)]
                fig_box = px.box(df2_prop,y='price',title= f"{p}" )
                fig_box_without_outlier = px.box(df2_prop_without_outlier,y='price',title= f"{p} after removing outlier manualy" )
                col1.plotly_chart(fig_box)
                col2.subheader("Property Details")
                col2.dataframe(df2_prop['price'].describe())
                col3.plotly_chart(fig_box_without_outlier)
                col4.subheader("Property Details after removing outlier")
                col4.dataframe(df2_prop_without_outlier['price'].describe())
                

if selected == 'Descriptive Analysis':
    
    tab1,tab2,tab3 = st.tabs(["Average Price of Properties","Price analysis based on Review score","Average Price of Properties for each country"])
    
    df_price = df.groupby(['country','property_type'])['price'].mean().reset_index()
    
    country_list = list(df_price['country'].unique())
    
    country_price = tab1.selectbox("Country List",country_list)
    df1_price = df_price [ ( df_price['country'] == country_price)].sort_values('price', ascending=False)
    df1_price = df1_price.rename(columns= {'price':'Average Price'})
    tab1.table(df1_price.reset_index(drop=True))
    
    for i in country_list:
        
        df2_price = df_price [ ( df_price['country'] == i)].sort_values('price', ascending=False)
        df2_price = df2_price.rename(columns= {'price':'Average Price'})
        
        fig_price = px.bar( 
                        df2_price,
                        x='property_type',
                        y='Average Price',
                        color='Average Price',
                        text_auto='.2s',
                        title=f'Average property price of {i}',
                        color_continuous_scale='Portland'
                        )
        fig_price.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        tab1.plotly_chart(fig_price,use_container_width=True)
    
    
    
    with tab2:
        col1,col2 = st.columns(2)       
        
        col1.subheader("Review score with More than 80%")
        col2.subheader("Review score with Less than 80%")
    
        for i in country_list:
        
            df3_price = df [ ( df['country'] == i) & (df['review_scores'] >= 80)]
            df4_price = df3_price.groupby(['property_type'])['price'].mean().reset_index()            
            df4_price = df4_price.rename(columns= {'price':'Average Price'})
            
            fig_price = px.bar( 
                            df4_price,
                            x='property_type',
                            y='Average Price',
                            color='Average Price',
                            text_auto='.2s',
                            title=f'Average property price of {i} with have review score of More than 80%',
                            color_continuous_scale='Portland'
                            )
            fig_price.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
            col1.container(border=True).plotly_chart(fig_price,use_container_width=True)

        for i in country_list:
        
            df5_price = df_price [ ( df['country'] == i) & (df['review_scores'] < 80) ]
            df6_price = df5_price.groupby(['property_type'])['price'].mean().reset_index()
            df6_price = df6_price.rename(columns= {'price':'Average Price'})
            
            fig_price = px.bar( 
                            df6_price,
                            x='property_type',
                            y='Average Price',
                            color='Average Price',
                            text_auto='.2s',
                            title=f'Average property price of {i} with have review score of Less than 80%',
                            color_continuous_scale='Portland'
                            )
            fig_price.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
            col2.container(border=True).plotly_chart(fig_price,use_container_width=True)    
    
    property_list = tab3.selectbox("Property List",list(df_price['property_type'].unique()))
    df7_price = df_price[ ( df_price['property_type'] == property_list)].reset_index(drop=True)
    df7_price = df7_price.rename(columns= {'price': 'Average Price'})
    tab3.table(df7_price.sort_values('Average Price', ascending = False).reset_index(drop = True))
    
    property_list1 = list(df_price['property_type'].unique())
    for i in property_list1:
        df8_price = df_price[ ( df_price['property_type'] == i)].reset_index(drop=True)
        df8_price = df8_price.rename(columns= {'price': 'Average Price'})
        fig_price = px.bar( 
                        df8_price,
                        x='country',
                        y='Average Price',
                        color='Average Price',
                        text_auto='.2s',
                        title=f'Average property price of {i}',
                        color_continuous_scale='Portland'
                        )
        fig_price.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        tab3.plotly_chart(fig_price,use_container_width=True)   