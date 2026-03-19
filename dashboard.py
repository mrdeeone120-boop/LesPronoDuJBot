import streamlit as st
import pandas as pd

st.set_page_config(page_title="LesPronoDuJBot Dashboard", layout="wide")
st.title("📊 LesPronoDuJBot Dashboard")

try:
    df = pd.read_csv("valuebets.csv")
    st.dataframe(df)

    if "stake" in df.columns:
        st.line_chart(df["stake"])
except FileNotFoundError:
    st.warning("CSV non trouvé. Le bot doit envoyer au moins un prono.")