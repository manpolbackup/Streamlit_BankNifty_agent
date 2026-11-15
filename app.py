# app.py

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from agent import banknifty_agent

st.set_page_config(
    page_title="BANKNIFTY PCR Agent",
    layout="wide"
)

st.title("BANKNIFTY PCR Agent")

query = st.text_input(
    "Enter Query",
    value="Analyze BANKNIFTY"
)

if st.button("Analyze"):

    with st.spinner("Running Analysis..."):

        response = banknifty_agent.invoke(
            {
                "messages":[
                    ("user", query)
                ]
            }
        )

        result = response["messages"][-1].content

    st.markdown(result)