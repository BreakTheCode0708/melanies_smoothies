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

# import streamlit as st
# import requests
# from snowflake.snowpark.functions import col

# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
# st.write(
#     """Choose the fruits you want in your custom Smoothie!
#     """
# )

# name_on_order = st.text_input('Name on smoothie:')
# st.write('The name on your Smoothie will be:', name_on_order)

# # Get Snowflake session
# cnx = st.connection("snowflake")
# session = cnx.session()
# # Fetch the list of fruits from Snowflake
# fruit_options_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

# pd_df = fruit_options_df.to_pandas()
# #st.dataframe(pd_df)
# # Convert the Snowpark DataFrame to a list of fruit names
# fruit_options_list = [row['FRUIT_NAME'] for row in fruit_options_df]
# #st.stop()

# # Multiselect widget to choose fruits
# ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_options_list, max_selections=5)

# # Only proceed if ingredients are selected
# if ingredients_list:

#     # Create a comma-separated string of chosen ingredients
#     ingredients_string = ', '.join(ingredients_list)

#     # Display the button outside the loop
#     time_to_insert = st.button('Submit Order')

#     if time_to_insert:
#         # SQL Insert statement
#         my_insert_stmt = """
#             INSERT INTO smoothies.public.orders(ingredients,name_on_order)
#             VALUES ('""" + ingredients_string+ """','"""+name_on_order+"""')
#         """

#         st.write(my_insert_stmt)
#         #st.stop()

#         # Execute the SQL statement
#         session.sql(my_insert_stmt).collect()
        
#         # Display success message
#         st.success('Your Smoothie is ordered!, '+ name_on_order, icon="✅")

# if ingredients_list:
#      for fruit_chosen in ingredients_list:
         
#          ingredients_string += fruit_chosen + ' '
#          search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#          st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
#          st.subheader(fruit_chosen + ' Nutrition Infromation')
#          fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
#          fv_df = st.dataframe(data= fruityvice_response.json() , use_container_width=True)

import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# Input for the name on the smoothie order
name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch the list of fruits and their SEARCH_ON values from Snowflake
fruit_options_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')).to_pandas()

# Convert the DataFrame to a list of fruit names
fruit_options_list = fruit_options_df['FRUIT_NAME'].tolist()

# Multiselect widget to choose fruits (limit to 5 ingredients)
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_options_list, max_selections=5)

# Only proceed if ingredients are selected
if ingredients_list:

    # Create a comma-separated string of chosen ingredients
    ingredients_string = ', '.join(ingredients_list)

    # Display the button for submitting the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # Proper SQL Insert statement using f-string
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        # Display the insert statement for debugging
        st.write(my_insert_stmt)

        try:
            # Execute the SQL insert statement
            session.sql(my_insert_stmt).collect()

            # Display success message
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Loop through the selected fruits to fetch and display nutritional information
    for fruit_chosen in ingredients_list:
        # Fetch the corresponding 'SEARCH_ON' value from the DataFrame
        search_on = fruit_options_df.loc[fruit_options_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        st.write(f'The search value for {fruit_chosen} is {search_on}.')

        # Display the nutrition information using the search_on value
        st.subheader(f'{fruit_chosen} Nutrition Information')

        # Make API request to Fruityvice using the search_on value
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        
        # Check if the API call was successful
        if fruityvice_response.status_code == 200:
            # Convert the response JSON to a DataFrame and display it
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        else:
            st.error(f'Failed to retrieve data for {fruit_chosen}. Please try again.')


