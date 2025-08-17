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

df = df.fillna("N/A")

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

# Default sort settings
default_sort_col = "ECR"
default_sort_order = "Ascending"


# Sidebar: choose column to sort by
sort_values = ["ECR", "ADPRANK", "VALUERANK"]
sort_col = st.selectbox("Sort by column", sort_values, index=sort_values.index(default_sort_col))
sort_order = st.radio("Sort order", ["Ascending", "Descending"], index=0 if default_sort_order=="Ascending" else 1)

# Function to sort while keeping None at bottom
def sort_with_na_bottom(df, col, ascending=True):
    na_mask = df[col] == "N/A"
    df_non_na = df[~na_mask]
    df_na = df[na_mask]

    df_non_na_sorted = df_non_na.sort_values(by=col, ascending=ascending, key=lambda s: s.map(lambda x: float(x) if isinstance(x, (int,float)) else x))
    return pd.concat([df_non_na_sorted, df_na], ignore_index=True)

df_selection = sort_with_na_bottom(df_selection, sort_col, ascending=(sort_order=="Ascending"))


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
