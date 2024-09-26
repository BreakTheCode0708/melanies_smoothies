# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col, when_matched 

 
# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
# st.write(
#     """Choose the fruits you want in your smoothie!
#     """
# )
# cnx=st.connection("snowflake") 
# session=cnx.session()
# my_dataframe=session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
 
 
# from snowflake.snowpark import types as T
 
# if my_dataframe:
#     editable_df = st.data_editor(my_dataframe)
#     submitted = st.button('Submit')
 
#     if submitted:
#         # st.success("Someone clicked the button.", icon='👍')
#         og_dataset = session.table("smoothies.public.orders")
#         # Manually define the schema for the dataframe
#         schema = T.StructType([
#             T.StructField("ORDER_UID", T.LongType()),  # Equivalent to NUMBER(38,0)
#             T.StructField("ORDER_FILLED", T.BooleanType()),
#             T.StructField("NAME_ON_ORDER", T.StringType()),
#             T.StructField("INGREDIENTS", T.StringType()),
#             T.StructField("ORDER_TS", T.TimestampType()),  # Equivalent to TIMESTAMP_LTZ(9)
#         ])
#         edited_dataset = session.create_dataframe(editable_df, schema=schema)
#         try:
#             og_dataset.merge(edited_dataset
#                              , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
#                              , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
#                             )
#             st.success("Orders updated: ", icon='👍')
#         except Exception as e:
#             st.write(f"Something went wrong: {e}")
 
# else:
#     st.success("There are no pending orders right now",icon = '👍')

import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()
# Fetch the list of fruits from Snowflake
fruit_options_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()

# Convert the Snowpark DataFrame to a list of fruit names
fruit_options_list = [row['FRUIT_NAME'] for row in fruit_options_df]

# Multiselect widget to choose fruits
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_options_list, max_selections=5)

# Only proceed if ingredients are selected
if ingredients_list:

    # Create a comma-separated string of chosen ingredients
    ingredients_string = ', '.join(ingredients_list)

    # Display the button outside the loop
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # SQL Insert statement
        my_insert_stmt = """
            INSERT INTO smoothies.public.orders(ingredients,name_on_order)
            VALUES ('""" + ingredients_string+ """','"""+name_on_order+"""')
        """

        st.write(my_insert_stmt)
        #st.stop()

        # Execute the SQL statement
        session.sql(my_insert_stmt).collect()
        
        # Display success message
        st.success('Your Smoothie is ordered!, '+ name_on_order, icon="✅")

if ingredients_list:
     for fruit_chosen in ingredients_list:
         ingredients_string += fruit_chosen + ' '
         st.subheader(fruit_chosen + ' Nutrition Infromation')
         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
         fv_df = st.dataframe(data= fruityvice_response.json() , use_container_width=True)


