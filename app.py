#Importing libraries to work with the dataset
import pandas as pd
import streamlit as st
import plotly.express as px


#----------------------1---------------
#Read in the csv file and convert to a Pandas dataframe
df = pd.read_csv('clean_vehicles_us.csv') 

st.title('Choose your car')
st.subheader('Use this app to select the vehicle based on your preferences')

#----------------------2-------------------

from PIL import Image

# Open the JPEG image file
image = Image.open('image.jpg')

st.image(image)

#--------------------3----------------------------
st.caption(':red[Choose your parameters here]')

price_range = st.slider(
     "What is your price range?",
     value=(500, 375000))

actual_range=list(range(price_range[0],price_range[1]+1))

#-------------------------4---------------------------------------
st.header('Top 100 most popular models')
# Get the 100 most popular models
top_100_models = df['model'].value_counts().head(100)

# Create a checkbox to display the table of top 100 models
if st.checkbox('Show Top 100 Most Popular Models'):
    st.dataframe(top_100_models.reset_index().rename(columns={'index': 'Model', 'model': 'Count'}))
else:
    st.write("Check the box above to display the top 100 most popular models.")

#---------------------------------5---------------------------------

st.dataframe(df)
st.header('Vehicle types by manufacturer')
st.write(px.histogram(df, x='model', color='type',color_discrete_sequence=px.colors.qualitative.Bold))

#------------------------------------6-------------------------------
st.header('Histogram of condition vs mileage')

# Generate histogram using Plotly Express
histogram = px.histogram(df, x='odometer', color='condition',color_discrete_sequence=px.colors.qualitative.Bold)

# Update the y and x-axis range
histogram.update_xaxes(range=[0, 500000])
histogram.update_yaxes(range=[0, 800])
st.plotly_chart(histogram)


st.header('Distribution of Price by Model Year')

# Create a scatter plot for price by year
scatter_plot = px.scatter(df, x='model_year', y='price', color_discrete_sequence=px.colors.qualitative.Bold)
scatter_plot.update_yaxes(range=[0, 150000])
scatter_plot.update_xaxes(range=[1960, 2020])
# Display the scatter plot
st.plotly_chart(scatter_plot)

#-------------------------------7-------------------------

st.header('Average price for top 10 most frequent models')
# Get the top 10 most popular models
top_10_models = df['model'].value_counts().head(10).index.tolist()

df_top_10 = df[df['model'].isin(top_10_models)]
average_prices = df_top_10.groupby('model')['price'].mean()
st.write(px.bar(average_prices, x= 'price', color='price',color_discrete_sequence=px.colors.qualitative.Bold))




#--------------------------------8-----------------------------

st.header('Compare price distribution between manufacturers')
manufac_list = sorted(df['model'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('chevrolet silverado 1500'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('ford f-150'))
mask_filter = (df['model'] == manufacturer_1) | (df['model'] == manufacturer_2)
df_filtered = df[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='model',
                      histnorm=histnorm,
                      barmode='overlay',color_discrete_sequence=px.colors.qualitative.Bold))






