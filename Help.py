import streamlit as st
from twilio.rest import Client
st.title("Need Some Help?")
st.write("IncomeGenie not working as expected? If you need any support fill out the field below to get answers to commonly asked questions or to contact IncomeGenie's Support team" )
with st.form("my_form"):
   phone_number = st.text_input('Enter your Phone Number Below:')
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
    twilio_number = "+18553056920"
    account_sid = "AC2c0f4154bcd696fb990741de353e09f6"
    auth_token = "f7fbbbd4d1f90d62310b151466f026e7"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
      body = """If you're having trouble uploading your file, there are a few things you can try:\n
      ✅ Check the file size: If your file is too large, the upload may fail. Try reducing the size of the file, or compressing it before uploading. \n
      ✅ Check the file type: Make sure you are uploading a file type that is allowed by the website or application. Some common file types include .csv  \n
      ✅ Check your internet connection: If your internet connection is weak or intermittent, the upload may fail. Try uploading the file from a different location or on a different device. \n
      ✅Try a different browser: Sometimes certain browsers have issues with file uploads. Try using a different browser, such as Chrome or Firefox, to see if the upload works. \n
      ✅Contact customer support at IncomeGenieSupport@gmail.com: If you've tried these steps and still can't upload your file, contact customer support for further assistance. Be sure to include details about the issue you're experiencing, including any error messages you may be seeing. """,
      from_ = twilio_number,
      to = phone_number
    )