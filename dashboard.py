import streamlit as st
import pandas as pd

st.title("LesPronoDuJBot Dashboard")

df = pd.read_csv("valuebets.csv")

st.dataframe(df)
st.line_chart(df["bankroll"])