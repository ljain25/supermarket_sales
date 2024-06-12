import streamlit as st
import numpy as np
import pandas as pd
import statistics

st.set_page_config(layout='wide',page_title='Supermarket Sales Analysis')

def product_line_chart(data):
    st.write("Product line")
    st.bar_chart(data.groupby("Product line")["Total"].sum(), use_container_width = True, height = 420, color = "#F1C40F")

def city_chart(data):
    st.write("City")
    st.bar_chart(data.groupby("City")["Total"].sum(), use_container_width=True, height=380, color="#3498DB")

def rating_rate_chart(data):
    st.write("Rating_range")
    st.bar_chart(data["Rating_range"].value_counts(), use_container_width=True, height=350, color="#9B59B6")

def payment_mode_chart(data):
    st.write("Payment_mode")
    fig2 = px.pie(data["Payment_mode"].value_counts().reset_index(), values="count", names="Payment_mode", color = "Payment_mode", color_discrete_map={'Ewallet':"#F1C40F", 'Cash':"#3498DB", 'Credit card':"#9B59B6"})
    st.plotly_chart(fig2, use_container_width=True, theme="streamlit")

def gender_chart(data):
    st.write("Gender")
    fig1 = px.pie(data["Gender"].value_counts().reset_index(), values="count", names="Gender", color="Gender",
                  color_discrete_map={"Male": "#F1C40F", "Female": "#9B59B6"})
    st.plotly_chart(fig1, use_container_width=True, theme="streamlit")

def customer_type_chart(data):
    st.write("Customer type")
    fig = px.pie(data["Customer type"].value_counts().reset_index(), values="count", names="Customer type",
                 color="Customer type", color_discrete_map={"Member": "#F1C40F", "Normal": "#9B59B6"})
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def overall_analysis(data, opt1):
    st.title(f"{opt1} Overall Analysis")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        col1.container(border = True).metric("Total Sales", round(data["Total"].sum()))
    with col2:
        col2.container(border = True).metric("Total Gross Income", round(data["gross income"].sum()))
    with col3:
        col3.container(border = True).metric("City with Max. Sales", data.groupby("City")["Total"].sum().sort_values(ascending = False).index[0])
    with col4:
        col4.container(border = True).metric("Product Line with Max. Sales", data.groupby("Product line")["Total"].sum().sort_values(ascending = False).index[0])
    with col5:
        col5.container(border = True).metric("Average Rating", round(data["Rating"].mean(), 2))
    with col6:
        col6.container(border = True).metric("Avg Daily Sales", round(data.groupby("Date")["Total"].mean().mean()))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        product_line_chart(data)
    with c2:
        city_chart(data)
    with c3:
        rating_rate_chart(data)
    with c4:
        payment_mode_chart(data)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        gender_chart(data)
    with c2:
        customer_type_chart(data)
    with c3:
        if opt1 == "Combined":
            st.write("Month on Month Sales")
            st.line_chart(data.groupby("Month")["Total"].sum())

#  ****************************************************************

def city_analysis(data, opt, opt1):
    st.title(f"{opt} City Analysis ({opt1})")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        col1.container(border=True).metric("Total Sales", round(data["Total"].sum()))
    with col2:
        col2.container(border=True).metric("Total Gross Income", round(data["gross income"].sum()))
    with col3:
        col3.container(border = True).metric("Average Rating", round(data["Rating"].mean(), 2))
    with col4:
        col4.container(border = True).metric("Avg Daily Sales", round(data.groupby("Date")["Total"].mean().mean()))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        product_line_chart(data)
    with c2:
        rating_rate_chart(data)
    with c3:
        payment_mode_chart(data)
    with c4:
        gender_chart(data)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        customer_type_chart(data)
    with c2:
        if opt1 == "Combined":
            st.write("Month on Month Sales")
            st.line_chart(data.groupby("Month")["Total"].sum())

# ****************************************************************

def product_line_analysis(data, opt, opt1):
    st.title(f"{opt} - Product Line Analysis ({opt1})")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        col1.container(border=True).metric("Total Sales", round(data["Total"].sum()))
    with col2:
        col2.container(border=True).metric("Total Gross Income", round(data["gross income"].sum()))
    with col3:
        col3.container(border=True).metric("Average Rating", round(data["Rating"].mean(), 2))
    with col4:
        col4.container(border=True).metric("City with max products of this line sold", df["City"].value_counts().sort_values().index[0])
    with col5:
        col5.container(border = True).metric("Avg Daily Sales", round(data.groupby("Date")["Total"].mean().mean()))

    if opt1 == "Combined":
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            customer_type_chart(data)
        with c2:
            rating_rate_chart(data)
        with c3:
            gender_chart(data)
        with c4:
            st.write("Month on Month Sales")
            st.line_chart(data.groupby("Month")["Total"].sum())
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            customer_type_chart(data)
        with c2:
            rating_rate_chart(data)
        with c3:
            gender_chart(data)


# ****************************************************************

df = pd.read_csv("supermarket_sales_cleaned.csv")

st.sidebar.title("Supermarket Sales Analysis")

option1 = st.sidebar.selectbox("Select One", ["Overall", "City", "Product Line"])

if option1 == "Overall":
    opt1 = st.sidebar.selectbox("Select Month", ["Combined", "January", "February", "March"])
    if opt1 == "Combined":
        overall_analysis(df, opt1)
    else:
        overall_analysis(df[df["Month"] == opt1], opt1)


if option1 == "City":
    opt = st.sidebar.selectbox("Select City", list(df.City.unique()))
    city_df = df[df["City"] == opt]
    opt1 = st.sidebar.selectbox("Select Month", ["Combined", "January", "February", "March"])
    if opt1 == "Combined":
        city_analysis(city_df, opt, opt1)
    else:
        city_analysis(city_df[city_df["Month"] == opt1], opt, opt1)


if option1 == "Product Line":
    opt = st.sidebar.selectbox("Select Product line", list(df["Product line"].unique()))
    product_df = df[df["Product line"] == opt]
    opt1 = st.sidebar.selectbox("Select Month", ["Combined", "January", "February", "March"])
    if opt1 == "Combined":
        product_line_analysis(product_df, opt, opt1)
    else:
        product_line_analysis(product_df[product_df["Month"] == opt1], opt, opt1)
