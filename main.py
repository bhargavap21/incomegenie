import streamlit as st
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.app_logo import add_logo

show_pages(
    [
        Page("main.py", "Incomegenie Information", "🏠"),
        Page("pages/Upload.py", "Analyze", "🧐"),
        Page("pages/Help.py", "Help", "🏥"),
    ]
)
from PIL import Image

image = Image.open('logo-black.png')
st.image(image, use_column_width= True )
st.title("Incomegenie Information")
st.header("How it Works")
st.write("Our app is a tool for small businesses and investors to analyze the income statements of a business. The user can upload a .csv file containing the income statement data, and the app will display the data in a table format. The user can then select a specific row from the table to analyze. The app will then display a line chart showing the income data for the selected row, and it will also perform a polynomial linear regression on the data to generate a trendline. Additionally, the app will make predictions for the next three years based on the trendline, and these predictions are plotted on the chart as points.  Overall, our app provides a way to visually explore and make predictions about a company's financial performance.")

st.header("How we built it")
st.write("""
1) Python programming language \n
2) Streamlit library for creating interactive web apps \n
3) Pandas library for data manipulation and analysis \n
4) Plotly library for creating interactive charts and graphs \n
5) Numpy library for mathematical operations \n
6) Scikit-learn library for machine learning and predictive modeling \n
7) Cohere artificial intelligence to analyze and summarize data
8) Twilio Api to send support messages to users \n
""" )