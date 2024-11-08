# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Tytuł aplikacji
st.title("🥤Customize Your Smoothie!🥤")
st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Wprowadzenie nazwy
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

# Połączenie z Snowflake
session = get_active_session()

# Pobieranie dostępnych owoców
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Wybór składników
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    , max_selections=5
)

# Tworzenie zapytania do wstawienia
if ingredients_list:
        ingredients_string = ''
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '
            st.subheader(fruit_chosen + 'Nutrition Information')
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """
    
        # Zatwierdzenie zamówienia
        time_to_insert = st.button('Submit Order')
    
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

import requests

