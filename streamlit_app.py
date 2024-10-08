import requests


# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

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

cnx = st.connection("snowflake")
session = cnx.session()
#my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)  #this lists the content of the dataframe
# st.stop()

# Convert the Snowpark Dataframe to a Pandas Dataframe so that we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections = 5)
#st.write("Your favourite fruit is:", ingredients_list)

if ingredients_list:
#    st.write(ingredients_list)
#    st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)       
        fv_df = st.dataframe(fruityvice_response.json(), use_container_width=True)   #Put the JSON into a Dataframe
        
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""


    time_to_insert = st.button('Submit Order')
    
    #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")





