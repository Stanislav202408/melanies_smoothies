# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

from snowflake.connector import connect
from snowflake.snowpark import Session

cnx = st.connection("snowflake")
session = cnx.session()


# Define your Snowflake connection parameters
connection_parameters = {
    'account': 'QEHRVKM-DX67949',
    'user': 'STANISLAV',
    'password': '3B.iT9Fe1929',
    'warehouse': 'COMPUTE_DWH',
    'database': 'SMOOTHIES',
    'schema': 'PUBLIC',
}

# Establish the connection
#conn = connect(connection_parameters)
conn = connect(
    account=connection_parameters['account'],
    user=connection_parameters['user'],
    password=connection_parameters['password'],
    warehouse=connection_parameters['warehouse'],
    database=connection_parameters['database'],
    schema=connection_parameters['schema']
)

session = Session.builder.configs(connection_parameters).create()

# Select the warehouse
session.sql("USE WAREHOUSE COMPUTE_DWH").collect()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

#option = st.selectbox(
#    "What is your favourite fruit?",
#    ("Banana", "Strawberies", "Peaches"),
#)

#st.write("Your favourite fruit is:", option)

import streamlit as st

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

#session = get_active_session()


#my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections = 5)
#st.write("Your favourite fruit is:", ingredients_list)

if ingredients_list:
#    st.write(ingredients_list)
#    st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""


#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
#             values ('""" + ingredients_string + """')"""

    
    

 #   st.write(my_insert_stmt)
 #   st.stop()


# Define your Snowflake connection parameters
connection_parameters = {
    'account': 'QEHRVKM-DX67949',
    'user': 'STANISLAV',
    'password': '3B.iT9Fe1929',
    'warehouse': 'COMPUTE_DWH',
    'database': 'SMOOTHIES',
    'schema': 'PUBLIC',
}

# Establish the connection
#conn = connect(connection_parameters)
conn = connect(
    account=connection_parameters['account'],
    user=connection_parameters['user'],
    password=connection_parameters['password'],
    warehouse=connection_parameters['warehouse'],
    database=connection_parameters['database'],
    schema=connection_parameters['schema']
)

session = Session.builder.configs(connection_parameters).create()
session.sql("USE WAREHOUSE COMPUTE_DWH").collect()
    
time_to_insert = st.button('Submit Order')
    
   #if ingredients_string:
if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)
