# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched 

 
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your smoothie!
    """
)
cnx=st.connection("snowflake") 
session=cnx.session()
my_dataframe=session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
 
 
from snowflake.snowpark import types as T
 
if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
 
    if submitted:
        # st.success("Someone clicked the button.", icon='👍')
        og_dataset = session.table("smoothies.public.orders")
        # Manually define the schema for the dataframe
        schema = T.StructType([
            T.StructField("ORDER_UID", T.LongType()),  # Equivalent to NUMBER(38,0)
            T.StructField("ORDER_FILLED", T.BooleanType()),
            T.StructField("NAME_ON_ORDER", T.StringType()),
            T.StructField("INGREDIENTS", T.StringType()),
            T.StructField("ORDER_TS", T.TimestampType()),  # Equivalent to TIMESTAMP_LTZ(9)
        ])
        edited_dataset = session.create_dataframe(editable_df, schema=schema)
        try:
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success("Orders updated: ", icon='👍')
        except Exception as e:
            st.write(f"Something went wrong: {e}")
 
else:
    st.success("There are no pending orders right now",icon = '👍')

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
