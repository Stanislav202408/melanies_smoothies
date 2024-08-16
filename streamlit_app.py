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


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

import streamlit as st

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

#session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections = 5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
    my_insert_stmt = """insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
#    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        dwh = "USE WAREHOUSE COMPUTE_DWH;"
#        st.write(dwh)
        session.sql(dwh).collect()

#        st.write(my_insert_stmt)  
        session.sql(my_insert_stmt).collect()        
        st.success('Your Smoothie is ordered!', icon="✅")


st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)
