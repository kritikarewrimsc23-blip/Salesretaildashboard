import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(
    page_title="Retail Sales Analysis Dashboard",
    page_icon="🛒",
    layout="wide"
)

# --- Load Data ---
sales = pd.read_csv("cleaned_sales.csv")  # <-- use your actual file name
sales['Date'] = pd.to_datetime(sales['Date'])

# --- Custom Header ---
st.markdown("""
    <h1 style='text-align: center; color: #6002EE; font-size: 2.8em;'>
        🛍️ Retail Sales Analysis Dashboard
    </h1>
    <hr style='border:1px solid #6002EE'>
    """, unsafe_allow_html=True)

# --- Metrics Row ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${sales['Total Amount'].sum():,.0f}")
col2.metric("Transactions", f"{sales.shape[0]:,}")
col3.metric("Unique Customers", f"{sales['Customer ID'].nunique()}")
top_cat = sales.groupby('Category')['Total Amount'].sum().idxmax()
col4.metric("Top Category", top_cat)

# --- Sidebar Filter ---
st.sidebar.header("📂 Filter Data")
category_filter = st.sidebar.multiselect(
    "Select Category:", 
    sales["Category"].unique(), 
    default=sales["Category"].unique()
)
filtered_sales = sales[sales["Category"].isin(category_filter)]

# --- Sales by Category (Interactive) ---
st.subheader("Sales by Category")
category_revenue = filtered_sales.groupby('Category')['Total Amount'].sum().reset_index().sort_values('Total Amount', ascending=False)
fig_cat = px.bar(
    category_revenue, x='Category', y='Total Amount', color='Total Amount',
    color_continuous_scale='blues',
    title='Sales by Category'
)
st.plotly_chart(fig_cat, use_container_width=True)

# --- Monthly Sales Trend ---
st.subheader("Monthly Sales Trend")
monthly_sales = filtered_sales.set_index('Date').resample('M')['Total Amount'].sum().reset_index()
fig_month = px.line(
    monthly_sales, x='Date', y='Total Amount', markers=True,
    line_shape='spline', title='Monthly Sales Trend'
)
st.plotly_chart(fig_month, use_container_width=True)

# --- Age Group Analysis ---
st.subheader("Average Purchase Amount per Age Group")
age_labels = ['<20', '21-30', '31-40', '41-50', '51-60', '60+']
filtered_sales['Age Group'] = pd.cut(
    filtered_sales['Age'], bins=[0,20,30,40,50,60,100], labels=age_labels)
age_group_revenue = filtered_sales.groupby('Age Group', observed=False)['Total Amount'].mean().reset_index()
fig_age = px.bar(
    age_group_revenue, x='Age Group', y='Total Amount', color='Age Group',
    color_discrete_sequence=px.colors.sequential.Purp_r, title='Avg Purchase per Age Group'
)
st.plotly_chart(fig_age, use_container_width=True)

# --- Top Customers ---
st.subheader("Top 10 Customers by Revenue")
top_customers = filtered_sales.groupby('Customer ID')['Total Amount'].sum().sort_values(ascending=False).head(10).reset_index()
st.dataframe(top_customers, use_container_width=True, hide_index=True)

# --- Dynamic Category-wise Sales Trend ---
st.subheader("Category-wise Sales Trend")
selected_category = st.selectbox("Pick a Category:", filtered_sales['Category'].unique())
cat_trend = filtered_sales[filtered_sales['Category']==selected_category].set_index('Date').resample('M')['Total Amount'].sum().reset_index()
fig_cat_trend = px.line(
    cat_trend, x='Date', y='Total Amount', markers=True,
    title=f"{selected_category} Sales Trend"
)
st.plotly_chart(fig_cat_trend, use_container_width=True)

# --- Key Insights ---
with st.expander("💡 Key Insights"):
    st.write("- **{}** is the top-performing category.".format(top_cat))
    st.write("- **{}** unique customers contribute to revenue.".format(sales['Customer ID'].nunique()))
    st.write("- Most purchases come from customers aged **{}**.".format(age_group_revenue.loc[age_group_revenue['Total Amount'].idxmax(), 'Age Group']))

# --- Footer ---
st.markdown("""
<hr>
<p style='text-align:center;'> <i> Tip: Update your CSV and reload for fresh results.<br>Built with Streamlit & Plotly | Author: Your Name </i></p>
""", unsafe_allow_html=True)
