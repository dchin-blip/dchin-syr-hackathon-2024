import pandas as pd
import streamlit as st

# Current Location = [43.038, -76.131]

st.title("FindAPark - Syracuse")

substitues = {
    "LITTLE LEAGUE" : "BASEBALL",
    "OLYMPIC RUNNING TRACK" : "TRACK",
    "SOCCER (PERM. POSTS)" : "SOCCER",
    "TURF FOOTBALL" : "FOOTBALL"
}

df = pd.read_csv("Syracuse_s_Athletic_Fields.csv")
for i in range(len(df.index.tolist())):
    purposes = (df.loc[i].at["FIELD_TYPE"]).split("/")
    purposes = [purpose.upper() for purpose in purposes]
    purposes_clean = []
    for purpose in purposes:
        if purpose.strip() in substitues.keys():
            purposes_clean.append(substitues[purpose.strip()])
        else:
            purposes_clean.append(purpose.strip())
    df.at[i, "_purpose"] = purposes_clean

step = 3

lat = st.number_input("Latitude", step = 1/(10**step), format = f"%0.{step}f", value = 43.038)
long = st.number_input("Longitude", step = 1/(10**step), format = f"%0.{step}f", value = -76.131)
selection = st.multiselect("Select Sport Type", options = ["Baseball", "Football", "Lacrosse", "Soccer", "Softball", "Track"])
selection.append("Multipurpose")
selection = [option.upper() for option in selection]
num = st.number_input("Number of Results", min_value = 1)

for i in range(len(df.index.tolist())):
    match = 0
    purpose = df.at[i, "_purpose"]
    for j in range(len(purpose)):
        if purpose[j] in selection:
            match = 1
            break
    df.at[i, "_match"] = match

df_match = df[df["_match"] == 1]
df_match["_distanceSqr"] = (df_match["LAT"] - lat)**2 + (df_match["LONG"] - long)**2
df_match["_miles"] = (df_match["_distanceSqr"]**(1/2) * 69)
df_match.rename(columns = {"PARK" : "Park", "_purpose" : "Sports", "_miles" : "Miles"}, inplace = True)
st.dataframe(df_match.sort_values(by = ["_distanceSqr"]).head(num), column_order = ["Park", "Sports", "Miles"], hide_index = True, width = 1200)