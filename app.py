import json
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import requests
from streamlit_lottie import st_lottie

#reading the Dataset
data = pd.read_csv(r"matches1.csv")

# https://www.webfx.com/tools/emoji-cheat-sheet/

#Setting page header title and favicon icon
st.set_page_config(
    page_title="IPL Statistics",
    initial_sidebar_state="auto",
    page_icon="🏏",
    layout="wide"
)



# Sidebar
st.sidebar.header("Please Filter Here:")
year = st.sidebar.multiselect(
    "Select the Year:",
    #options will display all the options in the sidebar of following category
    options=data["season"].unique(),
    #default will show some of options selected and rest in drop down menu
    default=data["season"].unique()
)
toss_decision = st.sidebar.multiselect(
    "Select the Toss Decision:",
    #options will display all the options in the sidebar of following category
    options=data["toss_decision"].unique(),
    #default will show some of options selected and rest in drop down menu
    default=data["toss_decision"].unique()
)
homeTeam = st.sidebar.multiselect(
    "Select the Home Team:",
    #options will display all the options in the sidebar of following category
    options=data["team1"].unique(),
    #default will show some of options selected and rest in drop down menu
    # default = ["Mumbai Indians", "Sunrisers Hyderabad", "Rising Pune Supergiant", "Gujarat Lions", "Royal Challengers Bangalore", "Kolkata Knight Riders"],
    default=data["team1"].unique()
)
awayTeam = st.sidebar.multiselect(
    "Select the Away Team:",
    #options will display all the options in the sidebar of following category
    options=data["team2"].unique(),
    #default will show some of options selected and rest in drop down menu
    # default=["Kings XI Punjab", "Rajasthan Royals", "Chennai Super Kings", "Deccan Chargers", "Kochi Tuskers Kerala", "Pune Warriors", "Delhi Daredevils"]
    default=data["team2"].unique()
)
#It will update dataset after every filter applied
data_selection = data.query(
    "team1 == @homeTeam & team2 == @awayTeam & season == @year & toss_decision == @toss_decision"
)
# st.dataframe(data_selection)

#  For Animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Main Page
st.title(":bar_chart: IPL Statistics :trophy:")
st.markdown("##")

# Displaying Animations
# It will create 3 columns and can be accessed through left_column, middle_column and right_column respectively
left_column, middle_column, right_column = st.columns(3)
with left_column:
    dashboard1 = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_XCWz7k.json")
    st_lottie(dashboard1, key="Dashboard1", height=400)
with middle_column:
    dashboard2 = load_lottieurl("https://assets8.lottiefiles.com/private_files/lf30_g5gmkozp.json")
    st_lottie(dashboard2, key="Dashboard2", height=400)
with right_column:
    dashboard3 = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_lguqm6zh.json")
    st_lottie(dashboard3, key="Dashboard3", height=400)
# st.dataframe(data_selection)
st.markdown("""---""")

# Top KPI's
total_number_of_matches = len(data_selection)
df1=data_selection["win_by_runs"][data_selection["win_by_runs"]>0]
batting_first_wins = data_selection["win_by_runs"][data_selection["win_by_runs"]>0].mean()
fielding_first_wins = data_selection["win_by_wickets"][data_selection["win_by_wickets"]>0].mean()
dl_applied = data_selection["dl_applied"][data_selection["dl_applied"]>0]
batting_first = data_selection["toss_decision"][data_selection["toss_decision"] == "bat"]
fielding_first = data_selection["toss_decision"][data_selection["toss_decision"] == "field"]

# Displaying KPI's
left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Matches:")
    st.subheader(total_number_of_matches)
with right_column:
    st.subheader("Number of matches using DL:")
    st.subheader(len(dl_applied))   
st.markdown("""---""")

# Displaying KPI's
left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Team Batting first:")
    st.subheader(len(batting_first))
with right_column:
    st.subheader("Team Fielding first:")
    st.subheader(len(fielding_first))
st.markdown("""---""")

# Displaying KPI's
left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Batting first team wins by average runs:")
    st.subheader(round(batting_first_wins))
with right_column:
    st.subheader("Fielding first team wins by average wickets:")
    st.subheader(round(fielding_first_wins))
st.markdown("""---""")





#Bar_Graph1
data = data_selection["team1"]
data1 = data_selection["team2"]

# Calculating the data for graph
di = {}
key1 = []
value1 = []
for i in data:
    if i in di and i in key1:
        di[i] += 1
    else:
        di[i] = 1
        key1.append(i)
for i in data1:
    if i in di and i in key1:
        di[i] += 1
    else:
        di[i] = 1
        key1.append(i)
for i in range(len(key1)):
    value1.append(di[key1[i]])

# Creating pandas dataframe
chart_data = pd.DataFrame( 
    key1, 
    index=value1,
    columns=["Team Names"]
    )

# Creating Bar Graph
total_matches_each_team = px.bar(
    chart_data,
    x="Team Names",
    y=chart_data.index,
    orientation="v",
    title="<b>Number of Matches Played by Each Team:</b>",
    color_discrete_sequence=["cyan"] * len(chart_data),
    template="plotly_dark"
)
# Making the background transparent
total_matches_each_team.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Pie_Chart
data4 = data_selection["result"]
# Calculating the data for pie chart
cou = {}
key = []
value = []
for i in data4:
    if i in cou and i in key:
        cou[i] += 1
    else:
        cou[i] = 1
        key.append(i)
for i in range(len(key)):
    value.append(cou[key[i]])
fig_pie1 = px.pie(
    hole=0.4,
    values=value,
    names=key,
    title="<b>Match Result</b>",
)

# Displaying bar graph and pie chart
left_column, right_column = st.columns(2)
left_column.plotly_chart(total_matches_each_team, use_container_width=True)
right_column.plotly_chart(fig_pie1, use_container_width=True)
st.markdown("##")


# Bar_Chart2
data2 = data_selection["toss_winner"]
# Calculating the data for graph
di = {}
key1 = []
value1 = []
for i in data2:
    if i in di and i in key1:
        di[i] += 1
    else:
        di[i] = 1
        key1.append(i)
for i in range(len(key1)):
    value1.append(di[key1[i]])

#Creating pandas Dataframe
chart_data1 = pd.DataFrame( 
    key1, 
    index=value1,
    columns=["Toss Winner"]
    )
#Creating Bar Graph
toss_wins = px.bar(
    chart_data1,
    x="Toss Winner",
    y=chart_data1.index,
    orientation="v",
    title="<b>Number of Tosses Won by Each Team:</b>",
    color_discrete_sequence=["green"] * len(chart_data),
    template="plotly_dark"
)
# Making the background transparent
toss_wins.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Pie_Chart2
data3 = data_selection["toss_decision"]
# Calculating the data for pie chart
cou = {}
key = []
value = []
for i in data3:
    if i in cou and i in key:
        cou[i] += 1
    else:
        cou[i] = 1
        key.append(i)
for i in range(len(key)):
    value.append(cou[key[i]])
fig_pie = px.pie(
    hole=0.4,
    values=value,
    names=key,
    title="<b>Toss Result</b>",
)

# Displaying Bar Chart and Pie CHart
left_column, right_column = st.columns(2)
left_column.plotly_chart(toss_wins, use_container_width=True)
right_column.plotly_chart(fig_pie, use_container_width=True)
st.markdown("##")


# Line_Chart
data5 = data_selection["winner"]
# Calculating the data for line chart
cou = {}
key = []
value = []
for i in data5:
    if i in cou and i in key:
        cou[i] += 1
    else:
        cou[i] = 1
        key.append(i)
for i in range(len(key)):
    value.append(cou[key[i]])

# Creating Pandas Dataframe
line_data = pd.DataFrame( 
    key, 
    index=value,
    columns=["Team Names"],
    )
fig_line = px.line(
    line_data,
    x="Team Names",
    y=line_data.index,
    orientation="v",
    title="<b>Wins by Each Team </b>",
    markers=True
)
# Making the background transparent
fig_line.update_layout(
    plot_bgcolor="rgba(0,0,0,0)"
)

# Displaying Line Chart
st.plotly_chart(fig_line, use_container_width=True)
st.markdown("##")


################################################################

# Filtering Dataset
df2=data_selection[["winner", "win_by_runs", "win_by_wickets"]]
df3 = df2[df2["win_by_runs"]>0]
df3 = round(df3.groupby(by=["winner"]).mean()).sort_values(by="win_by_runs")

# Bar_chart3
average_win_by_runs = px.bar(
    df3,
    x=df3.index,
    y="win_by_runs",
    orientation="v",
    title="<b>Win by Runs(average):</b>",
    color_discrete_sequence=["brown"] * len(df3),
    template="plotly_dark"
)
# Making the background transparent
average_win_by_runs.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=True))
)

# Bar_Chart4
df4 = df2[df2["win_by_wickets"]>0]
df4 = round(df4.groupby(by=["winner"]).mean()).sort_values(by="win_by_wickets")


average_win_by_wickets = px.bar(
    df4,
    x=df4.index,
    y="win_by_wickets",
    orientation="v",
    title="<b>Win by Wickets(average):</b>",
    color_discrete_sequence=["yellow"] * len(df4),
    template="plotly_dark"
)
# Making the background transparent
average_win_by_wickets.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=True))
)

# Displaying both  Bar Charts
left_column, right_column = st.columns(2)
left_column.plotly_chart(average_win_by_runs, use_container_width=True)
right_column.plotly_chart(average_win_by_wickets, use_container_width=True)
st.markdown("##")

# CSS for removing header, footer and main menu
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)