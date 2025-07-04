from backend.data_collection.utils import get_season_year
from backend.events.simple_listener import write
from backend.utils import find_in_data_folder
from backend import CollectDraftData
import pandas as pd
import plotly.express as px
import streamlit as st
import asyncio
import os


#TODO find way to update data that works
# @st.cache_resource
# def get_data(path):
#     df = pd.read_csv(path).copy()
#     return df


st.set_page_config(
    page_title="Draft Data",
    page_icon=":football:",
    layout="wide",
)

year = get_season_year()
path = find_in_data_folder(f"draft_order_{year}_copy.csv")
df = pd.read_csv(path).copy()
df = df.dropna(subset=["POS"])

st.sidebar.header("Filter here: ")
position = st.sidebar.multiselect(
    label="Select the Position Played:",
    options=df["POS"].unique(),
    default=df["POS"].unique(),
)


players = df["PLAYER"].unique()

df_selection = df.query("POS == @position & PLAYER == @players")

quick_find = st.sidebar.multiselect(
    label="Quickly Lookup a Player:",
    options=df["PLAYER"].unique(),
    default=None,
)
if quick_find:
    df_selection = df.query("PLAYER == @quick_find")

st.sidebar.button("Update")

df_selection = pd.DataFrame(df_selection.values,columns=df_selection.columns)
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
