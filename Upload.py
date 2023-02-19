import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import cohere
from PIL import Image
from authlib.integrations.requests_client import OAuth2Session

image = Image.open('logo-black.png')
st.image(image, use_column_width= True)
def income_statement_table(income_statement_csv):
    thisdict = {
      0 : "Total Revenue",
      1 : "Cost of Revenue",
      2 : "Gross Profit",
      3 : "Gross Profit Margin (%)",
      4 : "R&D Expense",
      5 : "SG&A Expense",
      6 : "Total Operating Expenses",
      7 : "Operating Income or Loss",
      8 : "Operating Margin (%)",
      9 : "Interest Expense",
      10 : "Total Other Income/Expenses",											
      11 : "Income Before Tax",											
      12 : "Income Tax Expense",											
      13 : "Income from Continuing Ops.",											
      14 : "Net Income",											
      15 : "Net Profit Margin (%)",											
      16 : "Net Income Available to Common Shareholders",										
      17 : "Basic EPS",				
      18 : "Diluted EPS",											
      19 : "Basic Average Shares",
      20 : "Diluted Average Shares",
    } 
    df = pd.read_csv(income_statement_csv)
    df = df.drop(df.columns[1], axis=1)
    df = df.round(2)
    #drop the first column from the dataframe
    st.table(df)
    df = df.drop(df.columns[0], axis=1)
    NUM = st.slider('Which Financial would like to analyze', 0, 20)
    # Get the first 2nd row
    row = df.iloc[NUM]
    #reverse the order of the data
    row = row[::-1]
    # Create a line chart of the data in the row
    fig2 = go.Figure(data=[go.Surface(x=df.columns[::-1], y=row)])
    fig2.update_layout(title= thisdict[NUM], xaxis_title='Year', yaxis_title= thisdict[NUM])
    fig = go.Figure(data=[go.Scatter(x=df.columns[::-1], y=row)])
    fig.update_layout(title= thisdict[NUM], xaxis_title='Year', yaxis_title= thisdict[NUM])
    # Perform polynomial linear regression on the data
    X = np.array([i for i in range(len(row))]).reshape(-1, 1)
    poly = PolynomialFeatures(3)
    poly.fit(X)
    X_poly = poly.transform(X)

    model = LinearRegression(fit_intercept=False)
    model.fit(X_poly, row)
    y_poly = model.predict(X_poly)

    # Add the polynomial regression line to the chart
    fig.add_trace(go.Scatter(x=df.columns[::-1], y=y_poly, name='Polynomial Regression', mode='lines'))
    
    # Predict values for Sep 2023, Sep 2024, Sep 2025
    x_pred = np.array([len(row), len(row)+1, len(row)+2]).reshape(-1, 1)
    X_pred_poly = poly.transform(x_pred)
    y_pred = model.predict(X_pred_poly)
    y_pred = y_pred * np.random.uniform(0.7, 1, len(y_pred))
    # Add the predictions to the chart
    fig.add_trace(go.Scatter(x=["Sep 2023", "Sep 2024", "Sep 2025"], y=y_pred, name='Predictions', mode='markers'))
    st.plotly_chart(fig)
    co = cohere.Client('tefrhj408xaRpjJvkr0GfQLRNKvnSJTfIdKE9g9J') #your cohere api key here 
    topic = str(thisdict[NUM])+ str(row)
    response = co.generate(
  model='command-xlarge-20221108',
  prompt="""Summarize the overall trend in the data. Analyze the forecast for the data, and Identify any outliers or unusual observations in the data"""+ str(topic),
  max_tokens=300,
  temperature=0.9,
  k=0,
  p=0.75,
  frequency_penalty=0,
  presence_penalty=0,
  stop_sequences=[],
  return_likelihoods='NONE')
    st.write(str(response.generations[0].text))

if __name__ == '__main__':
    st.header("Upload")
    income_statement_csv = st.file_uploader('Please Upload your Income Statement as a .csv file, Example: incomestatement.csv', type='csv')
    if income_statement_csv:
        st.success("Income Statement Uploaded Successfully")
        income_statement_table(income_statement_csv)
        questionBank = ["What are some ways to increase gross profit margin for our company based on our income statement?",
        "What steps can we take to reduce our R&D expenses while maintaining growth?",
        "How can we improve our operating margin and increase operating income?",
        "What strategies can we implement to lower our interest expenses?",
        "What actions can we take to increase our income before tax?",
        "What are some ways to reduce our income tax expenses?",
        "How can we increase our net profit margin?",
        "What measures can we take to improve our basic EPS?",
        "What strategies can we use to increase our net income available to common shareholders?",
        "What steps can we take to improve our diluted EPS?"]
        co = cohere.Client('tefrhj408xaRpjJvkr0GfQLRNKvnSJTfIdKE9g9J') #your cohere api key here 
        def write_post(topic):
          response = co.generate(
          model='command-xlarge-20221108',
          
          prompt=str(income_statement_csv) +"""
        Analyze the data above and take the role of a financial analyst and answer the prompt in two paragraphs:\"{topic}\"""",
          max_tokens=300,
          temperature=0.9,
          k=0,
          p=0.75,
          frequency_penalty=0,
          presence_penalty=0,
          stop_sequences=[],
          return_likelihoods='NONE')
          return(response.generations[0].text)
        st.header("Summary")
        
        for i in questionBank:
          st.subheader(i)
          st.write(write_post(i))        

      


