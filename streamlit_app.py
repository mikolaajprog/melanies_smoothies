# Import Python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

connection_parameters = {
    user = "mikolajlopatka"
    password = "FraHtMiki2024#"
    role = "SYSADMIN"
    warehouse = "COMPUTE_WH"
    database = "SMOOTHIES"
    schema = "PUBLIC"
}
# Inicjalizacja sesji Snowflake
session = Session.builder.configs(connection_parameters).create()

# Tytuł aplikacji
st.title("🥤Customize Your Smoothie!🥤")
st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Wprowadzenie nazwy
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

# Pobieranie dostępnych owoców z Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Wybór składników
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe.to_pandas()['FRUIT_NAME'].tolist(),  # Przekształcamy dane Snowflake do listy
    max_selections=5
)

# Tworzenie zapytania do wstawienia
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Zatwierdzenie zamówienia
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
