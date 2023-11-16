import pandas as pd
import plotly.express as px
import streamlit as st 


# emojiwebsite: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title='Sales Dashboard',
    page_icon=':bar_chart:',
    layout='wide'
)
@st.cache_data
def get_data_from_excel():
    data = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    data["hour"] = pd.to_datetime(data["Time"], format="%H:%M:%S").dt.hour
    return data
data = get_data_from_excel()
# st.dataframe(data)


# --- SIDEBAR ----
st.sidebar.header('Silahkan pilih disini: ')
city = st.sidebar.multiselect(
    "Pilih Kota: ",
    options=data['City'].unique(),
    default=data['City'].unique()
)

costumer_type = st.sidebar.multiselect(
    "Pilih Customer: ",
    options=data['Customer_type'].unique(),
    default=data['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    "Pilih Jenis kelamin: ",
    options=data['Gender'].unique(),
    default=data['Gender'].unique()
)

data_selection = data.query(
    "City == @city & Customer_type == @costumer_type & Gender == @gender"
)

st.dataframe(data_selection)

# --- MAINPAGE ---
st.title(':bar_chart: Sales Dashboard')
st.markdown('##')

#TOP KPI's
total_sales = int(data_selection['Total'].sum())
avarage_rating = round(data_selection['Rating'].mean(), 1)
star_rating = ":star:" * int(round(avarage_rating,0))
avarage_sale_by_transaction = round(data_selection['Total'].mean(),2)

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total Sales: ")
    st.subheader(f'IDR RP.{total_sales:,}')
with middle_column:
    st.subheader('Average Rating: ')
    st.subheader(f'{avarage_rating}{star_rating}')
with right_column:
    st.subheader('Avarage Sales Per Transaction: ')
    st.subheader(f'{avarage_sale_by_transaction}')
    
# st.markdown("---")
    
# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = data_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
# st.plotly_chart(fig_product_sales)


# SALES BY HOUR [BAR CHART]
sales_by_hour = data_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# st.plotly_chart(fig_hourly_sales)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)