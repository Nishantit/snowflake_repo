# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customized Your Smoothie! :cup_with_straw:")
st.write(
  """ Choose the fruits you want in custom Somoothie!
  """
)

#import streamlit as st
name_on_order = st.text_input('Name on Smoothie')
st.write('The Name of your Smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingradients_list = st.multiselect(
    'Choose Up to 5 ingradients:' , my_dataframe, max_selections=5
)

if ingradients_list:
     #st.write(ingradients_list)
     #st.text(ingradients_list)

     ingradients_string = ''

     for fruit_chosen in ingradients_list:
         ingradients_string += fruit_chosen + ' '
         search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
         #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')         
         st.subheader(fruit_chosen + ' Nutrition Information')
         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
         sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)       

     #st.write(ingradients_string)

     my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(ingredients,name_on_order)
            values ('""" + ingradients_string + """','""" + name_on_order + """')"""

     #st.write(my_insert_stmt)
    # st.stop()
     time_to_insert = st.button('Submit Order')

     if time_to_insert:
        session.sql(my_insert_stmt).collect()

     if ingradients_string:
         session.sql(my_insert_stmt).collect()
         st.success('Your Smoothie is ordered!', icon="✅")

