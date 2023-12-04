import streamlit as st
import pandas as pd
import math as math
from handcalcs.decorator import handcalc
import forallpeople as si
 
si.environment("structural")

st.write("##### DESIGN AND DETAILING OF REINFORCED CONCRETE WALLS TO AS 3600:2018")

uploaded_file = st.file_uploader("ETABS Pier forces:", type=["xlsx"])
if uploaded_file is not None:
    df_forces = pd.read_excel(uploaded_file)

uploaded_file = st.file_uploader("ETABS Pier properties:", type=["xlsx"])
if uploaded_file is not None:
    df_pier_props = pd.read_excel(uploaded_file)

uploaded_file = st.file_uploader("ETABS storey heights:", type=["xlsx"])
if uploaded_file is not None:
    df_storey_heights = pd.read_excel(uploaded_file)
    #df = df.set_index(['Story','Pier'])
    #df = df.drop('Unnamed: 0', axis=1)
    #pd.set_option('display.max_columns',None)
    #pd.set_option('display.max_rows',None)
    #st.dataframe(df)

df_forces2 = df_forces.drop([0], axis=0)
st.dataframe(df_forces2)
mask=df_forces2['Case Type'] == 'Combination'
df_combos = df_forces2.loc[mask]
st.dataframe(df_combos)

#MAX TENSION IN PIERS CHECK
mask = df_combos['P'] > 0
p_tens = df_combos.loc[mask]
p_tens['P'] = pd.to_numeric(p_tens['P'], errors='coerce')
p_tens_loc = p_tens.groupby(["Story","Pier"])["P"].groups
p_tens_idxmax = p_tens.groupby(["Story","Pier"])["P"].idxmax()
p_tens_max = p_tens.loc[p_tens_idxmax]
st.dataframe(p_tens_max)
p_tens_max = p_tens_max.set_index("Story")

st.dataframe(df_storey_heights)
df_story_height = df_storey_heights.drop([0], axis=0)
df_story_height2 = df_story_height.drop(['Master Story','Similar To','Splice Story','Splice Height','Color','GUID'], axis=1)
st.dataframe(df_story_height2)

df_story=df_story_height2
Story_list = df_story['Name'].tolist()
stories = Story_list[:-1]

story_categorical = pd.CategoricalDtype(stories, ordered=True)
p_tens_max.index = p_tens_max.index.astype(story_categorical)
p_tens_dtype = p_tens_max.sort_index()
st.dataframe(p_tens_dtype)

#MIN COMPRESSION IN PIERS CHECK
mask = df_combos['P'] < 0
p_tens_min_compr = df_combos.loc[mask]
p_tens_min_compr['P'] = pd.to_numeric(p_tens_min_compr['P'], errors='coerce')
min_compr_tens = p_tens_min_compr.groupby(["Story","Pier"])["P"].max().reset_index()
min_compr_tens_idxmax = p_tens_min_compr.groupby(["Story","Pier"])["P"].idxmax()
p_tens_max2 = p_tens_min_compr.loc[min_compr_tens_idxmax]

#df_story=df_story_height2
#Story_list = df_story['Name'].tolist()
#stories = Story_list[:-1]

story_categorical = pd.CategoricalDtype(stories, ordered=True)
p_tens_max2.index = p_tens_max2.index.astype(story_categorical)
p_tens2_dtype = p_tens_max2.sort_index()
st.dataframe(p_tens2_dtype)

#MAX COMPRESSION IN PIERS CHECK
mask = df_combos['P'] < 0
p_compr = df_combos.loc[mask]
p_compr['P'] = pd.to_numeric(p_compr['P'], errors='coerce')
p_compr_loc = p_compr.groupby(["Story","Pier"])["P"].groups
p_compr_idxmax = p_compr.groupby(["Story","Pier"])["P"].idxmin()
p_compr_max = p_compr.loc[p_compr_idxmax]
st.dataframe(p_compr_max)
p_compr_max = p_compr_max.set_index("Story")

st.dataframe(df_storey_heights)
df_story_height = df_storey_heights.drop([0], axis=0)
df_story_height2 = df_story_height.drop(['Master Story','Similar To','Splice Story','Splice Height','Color','GUID'], axis=1)
st.dataframe(df_story_height2)

df_story=df_story_height2
Story_list = df_story['Name'].tolist()
stories = Story_list[:-1]

story_categorical = pd.CategoricalDtype(stories, ordered=True)
p_compr_max.index = p_compr_max.index.astype(story_categorical)
p_compr_dtype = p_compr_max.sort_index()
st.dataframe(p_compr_dtype)

#MAX M3 IN PIERS CHECK
df_combos['M3'] = pd.to_numeric(df_combos['M3'], errors='coerce')
m3_loc = df_combos.groupby(["Story","Pier"])["M3"].groups
m3_idxmax = df_combos.groupby(["Story","Pier"])["M3"].apply(lambda x: x.abs().idxmax())
m3_max = df_combos.loc[m3_idxmax]
m3_max = m3_max.set_index("Story")
m3_max.index = m3_max.index.astype(story_categorical)
m3_dtype = m3_max.sort_index()
st.dataframe(m3_dtype)

#MAX V2 IN PIERS CHECK
df_combos['V2'] = pd.to_numeric(df_combos['V2'], errors='coerce')
v2_loc = df_combos.groupby(["Story","Pier"])["V2"].groups
v2_idxmax = df_combos.groupby(["Story","Pier"])["V2"].apply(lambda x: x.abs().idxmax())
v2_max = df_combos.loc[v2_idxmax]
v2_max = v2_max.set_index("Story")
v2_max.index = v2_max.index.astype(story_categorical)
v2_dtype = v2_max.sort_index()
st.dataframe(v2_dtype)

#MERGE DATAFRAMES
p_tens_ = p_tens_dtype.drop(["Case Type","Step Type","Location"], axis=1)
p_compr_ = p_compr_dtype.drop(["Case Type","Step Type","Location"], axis=1)
m3_ = m3_dtype.drop(["Case Type","Step Type","Location"], axis=1)
v2_ = v2_dtype.drop(["Case Type","Step Type","Location"], axis=1)
tens_compr_merge = p_compr_.merge(p_tens_,on=["Story","Pier"],how='outer')
tens_compr_merge.index = tens_compr_merge.index.astype(story_categorical)
p_t_merged = tens_compr_merge.sort_index()

p_t_m3 = p_t_merged.merge(m3_,on=["Story","Pier"],how='outer')
st.dataframe(p_t_merged)

p_t_m3_v2 = p_t_m3.merge(v2_,on=["Story","Pier"],how='outer', suffixes=('_x1','_y1'))
df_combined = p_t_m3_v2
st.dataframe(df_combined)

##Story heights
story_prop=df_story_height2
story_properties = story_prop.iloc[:-1]
story_prop3=story_properties.rename(columns={"Name":"Story"})
story_prop4=story_prop3.set_index("Story")
st.dataframe(story_prop4)
df_combined2 = df_combined.merge(story_prop4,on=["Story"],how='outer')
st.dataframe(df_combined2)

##Sort index
st.dataframe(df_pier_props)
df_pier_prop = df_pier_props.drop([0], axis=0)
pier_props = df_pier_prop.drop(['AxisAngle','# Area Objects','# Line Objects','Width Top','Thickness Top','Material','CG Bottom X','CG Bottom Y','CG Bottom Z','CG Top X','CG Top Y','CG Top Z'], axis=1)
pier_props1=pier_props.set_index("Story")
df_combined3 = df_combined2.merge(pier_props,on=["Story","Pier"],how='outer')
st.dataframe(df_combined3)

