from backend.data_collection.utils import get_season_year
from backend.utils import find_in_data_folder
from backend import CollectDraftData
import pandas as pd
import plotly.express as px
import streamlit as st
import os


@st.cache
def get_data():
    path = find_in_data_folder(f"draft_order_{year}.csv")
    df = pd.read_csv(path)
    df = df.dropna(subset=["POS"])
    return df


st.set_page_config(
    page_title="Draft Data",
    page_icon=":football:",
    layout="wide",
)

try:
    df = get_data()
except FileNotFoundError:
    # collect data if not available
    year = get_season_year()
    CollectDraftData.main(year)
    df = get_data()


st.sidebar.header("Filter here: ")
position = st.sidebar.multiselect(
    label="Select the Position Played:",
    options=df["POS"].unique(),
    default=df["POS"].unique(),
)

players_removed = st.sidebar.multiselect(
    label="Select Player's Name to Remove:",
    options=df["PLAYER"].unique(),
    default=None,
)
players = [player for player in df["PLAYER"].unique() if player not in players_removed]

df_selection = df.query("POS == @position & PLAYER == @players")

quick_find = st.sidebar.multiselect(
    label="Quickly Lookup a Player:",
    options=df["PLAYER"].unique(),
    default=None,
)
if quick_find:
    df_selection = df.query("PLAYER == @quick_find")

st.dataframe(df_selection)

new_selection = df_selection.dropna(subset=["VOR"]).reset_index()
vor_df = new_selection["VOR"]
if len(vor_df) > 24:
    vor_df = vor_df.iloc[:24]

vor_values = vor_df
_x = new_selection["PLAYER"].iloc[vor_values.index]


next_24_vor = px.bar(vor_values, x=_x, y="VOR", orientation="v")

st.plotly_chart(next_24_vor)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
