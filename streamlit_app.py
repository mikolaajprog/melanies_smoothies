# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from snowflake.snowpark.exceptions import SnowparkSessionException

# Tytuł aplikacji
st.title("🥤Customize Your Smoothie!🥤")
st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Wprowadzenie nazwy
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

# Konfiguracja połączenia z Snowflake
connection_parameters = {
    "account": "<your_account>",        # np. 'xyz12345'
    "user": "<your_user>",              # np. 'user_name'
    "password": "<your_password>",      # np. 'your_password'
    "role": "<your_role>",              # opcjonalnie, jeśli masz przypisaną rolę
    "warehouse": "<your_warehouse>",    # np. 'compute_wh'
    "database": "<your_database>",      # np. 'smoothies'
    "schema": "<your_schema>"           # np. 'public'
}

# Inicjalizacja sesji
try:
    session = Session.builder.configs(connection_parameters).create()
except SnowparkSessionException as e:
    st.error(f"Problem with Snowflake session: {e}")
    session = None

# Jeśli sesja jest poprawnie utworzona, kontynuuj
if session:
    # Pobieranie dostępnych owoców
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

    # Wybór składników
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients: '
        , my_dataframe.to_pandas()['FRUIT_NAME'].tolist()  # konwersja do listy
        , max_selections=5
    )

    # Tworzenie zapytania do wstawienia
    if ingredients_list:
        ingredients_string = ''
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '

        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """

        # Zatwierdzenie zamówienia
        time_to_insert = st.button('Submit Order')

        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
else:
    st.error("Unable to establish a connection with Snowflake. Please check your credentials.")
