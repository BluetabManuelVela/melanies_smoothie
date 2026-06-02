# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# To use a Snowpark column function named `col`, we need to import it into our app
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

# Add a Name Box for Smoothie Orders
name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name of your smoothie will be: ", name_on_order)

# Adding Interactive Elements
#option = st.selectbox(
#    'What is your favourite fruit?',
#    ('Banana', 'Strawberries', 'Peaches')
#)
#
#st.write('You favourite fruit is: ', option)


# Display the Fruit Options List
session = get_active_session()

#my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# Add a Multiselect
ingredients_list = st.multiselect('Choose up to 5 ingredients: '
                                  , my_dataframe 
                                  , max_selections = 5)

# Display the LIST
#st.write(ingredients_list)
#st.text(ingredients_list)

# Ocultar la lista cuando no hay ninguna selecion
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    # How a FOR LOOP Block Worksfor fruit_chosen in ingredients_list
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')

    #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
