import pandas as pd
import requests
import json
import streamlit as st
import utils


def get_all_products():
    response = requests.get('http://127.0.0.1:5000/products')
    return json.loads(response.content)


def remove_product(barcode_id):
    res = requests.delete('http://127.0.0.1:5000/removeproduct', json={'barcode_id': barcode_id})
    st.text(res.content)
    st.experimental_singleton.clear()


def remove_products(product_frame, selected):
    to_remove = product_frame[product_frame['Title'].isin(selected)]
    to_remove_list = to_remove['Barcode id'].values

    for id in to_remove_list:
        remove_product(id)

st.markdown("Dashboard")
st.sidebar.markdown("Dashboard")

st.title("Whats in your fridge")
products = pd.DataFrame(get_all_products()['message'])

products_to_display = products[['title', 'purchase_date', 'price', 'barcode_id']]
products_to_display['price'] = products_to_display['price'].map(utils.format_price_for_gui)
products_to_display['days_in_fridge'] = products_to_display['purchase_date'].map(utils.calculate_num_days_in_fridge)
products_to_display['Date purchased'] = products_to_display['purchase_date'].map(utils.format_date_for_gui)
products_to_display.drop(['purchase_date'], axis=1, inplace=True)

products_to_display.columns = products_to_display.columns.map(utils.convert_to_display_text)

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.table(products_to_display)

st.subheader("Remove items")
options = st.multiselect(options=products_to_display['Title'], label='Select items to remove')
cap_button = st.button('Click here to remove selected elements from the list')

if cap_button:
    remove_products(products_to_display, options)
    options.clear()
