from backend.data_collection.utils import get_season_year
from backend.utils import find_in_data_folder
from backend import CollectDraftData
from backend.draft import Draft
import pandas as pd
import plotly.express as px
import streamlit as st
import os

@st.cache
def get_data():
    year = get_season_year()
    path = find_in_data_folder(f"draft_order_{year}.csv")
    #collect data if not available
    if not os.path.exists(path):
        CollectDraftData().main()

    df = pd.read_csv(path)
    df = df.dropna(subset=["POS"])
    return df


# if args == None or len(args) < 3:
#     total_teams = int(input("Enter total number of teams: "))
#     pos = int(input("Enter draft position: "))
#     url = input("Enter draft url: ")
# else:
#     total_teams = args[0]
#     pos = args[1]
#     url = args[2]
# year = get_season_year()
# file_path = find_in_data_folder(f'draft_order_{year}.csv')
# drft = Draft(pd.read_csv(file_path), total_teams)
# current_round = 1

# wp = FantasyScraper()
# try:
#     wp.start(url)
# except WebDriverException:
#     update_chrome_driver()
#     wp.start(url)
# wp.check_login()
# if pos == 1:
#     drft.recommend()
#     time.sleep(30)
# while current_round < total_teams * 15:
#     if drft.current_team + drft.increment == pos:
#         drft.recommend()
#         time.sleep(30)
#     df = wp.collect('results-by-round')
#     if len(df.index) != 0:
#         df = bd.build_drafting_data(df)
#         drft.automated_draft(df, pos)
#         file_path = find_in_data_folder(f'league_draft_{year}.csv')
#         pd.DataFrame(drft.draft).to_csv(file_path, index = True, header=True)
#         current_round = drft.current_round
# wp.quit()


st.set_page_config(
    page_title = "Fantasy Drafter",
    page_icon = ":football:",
    layout = "wide",
)

df = get_data()

st.sidebar.header("Filter here: ")
position = st.sidebar.multiselect(
    label = "Select the Position Played:",
    options = df["POS"].unique(),
    default = df["POS"].unique(),
)

players_removed = st.sidebar.multiselect(
    label = "Select Player's Name to Remove:",
    options = df["PLAYER"].unique(),
    default = None,
)
players = [player for player in df["PLAYER"].unique() if player not in players_removed]

df_selection = df.query("POS == @position & PLAYER == @players")

quick_find = st.sidebar.multiselect(
    label = "Quickly Lookup a Player:",
    options = df["PLAYER"].unique(),
    default = None,
)
if quick_find:
    df_selection = df.query("PLAYER == @quick_find")

st.dataframe(df_selection)

new_selection = df_selection.dropna(subset=["VOR"]).reset_index()
vor_df = new_selection["VOR"]
if len(vor_df) > 24:
    vor_df = vor_df.iloc[:24]

vor_values = (
    vor_df
)
_x = new_selection["PLAYER"].iloc[vor_values.index]



next_24_vor = px.bar(
    vor_values,
    x = _x,
    y = "VOR",
    orientation = 'v'
)

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