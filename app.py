# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import calendar
import re
import os

# ===== CONFIGURATION =====
MPESA_NUMBER = "+255 765 798 780"
DEVELOPER_NAME = "Chriss"
PREMIUM_PASSWORD = "pi2000"
BUSINESS_EMAIL = "xhakachris41@gmail.com"
COPYRIGHT_YEAR = "2025"
# =========================

# Set page config
st.set_page_config(
    page_title="BizTrack Pro - Tanzania",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown(f"""
<style>
.main-header {{font-size: 2.5rem; color: #2E86AB; text-align: center; margin-bottom: 1rem; font-weight: bold;}}
.feature-card {{background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; margin: 10px 0;}}
.premium-badge {{background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 8px 20px; border-radius: 25px; font-weight: bold;}}
.success-box {{background-color: #d4edda; border: 2px solid #c3e6cb; border-radius: 10px; padding: 20px; margin: 15px 0;}}
.stButton>button {{background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; padding: 12px 25px; font-weight: bold;}}
.stButton>button:hover {{background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); transform: scale(1.05);}}
.developer-info {{background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 15px; border-radius: 10px; margin: 10px 0;}}
.whatsapp-button {{background-color: #25D366 !important; color: white !important; border: none !important; padding: 10px 20px !important; border-radius: 5px !important; font-weight: bold !important;}}
.whatsapp-button:hover {{background-color: #128C7E !important; transform: scale(1.05);}}
.premium-feature {{border-left: 5px solid #667eea; padding-left: 15px; margin: 15px 0;}}
.copyright {{text-align: center; padding: 15px; margin-top: 20px; font-size: 0.9rem; color: #666; border-top: 1px solid #ddd;}}
.feature-explanation {{background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #2E86AB;}}
.premium-locked {{filter: blur(5px); pointer-events: none;}}
</style>
""", unsafe_allow_html=True)

# Professional Pricing
PREMIUM_PRICES = {
    "Monthly": "TZS 15,000",
    "Quarterly": "TZS 40,000",
    "Semi-Annual": "TZS 75,000",
    "Annual": "TZS 120,000"
}

# Translation dictionaries
ENGLISH_TEXTS = {
    "add_sale": "Add Sale",
    "view_reports": "View Reports",
    "inventory": "Inventory",
    "subscribe": "Subscribe",
    "business_name": "Enter Business Name",
    "date": "Date",
    "customer": "Customer Name",
    "product": "Product Name",
    "quantity": "Quantity",
    "price": "Price (TZS)",
    "add_button": "Add Sale",
    "total_sales": "Total Sales",
    "transactions": "Transactions",
    "avg_sale": "Average Sale",
    "premium_locked": "Premium features locked. Subscribe to unlock advanced analytics.",
    "premium_unlocked": "Premium Unlocked! Access all advanced features.",
    "sales_trend": "Sales Trend Analysis",
    "top_customers": "Customer Analytics",
    "product_performance": "Product Performance",
    "sales_distribution": "Sales Distribution",
    "export_data": "Export Data",
    "download_csv": "Download CSV",
    "inventory_management": "Inventory Management",
    "add_stock": "Add Stock",
    "current_stock": "Current Stock",
    "update_stock": "Update Stock",
    "subscribe_title": "Subscribe to Premium",
    "features_title": "15+ Premium Features Included",
    "choose_plan": "Choose Your Plan",
    "payment_instructions": "Payment Instructions",
    "contact_whatsapp": "Contact via WhatsApp",
    "developed_by": "Developed by",
    "contact": "Contact",
    "sales_forecast": "Sales Forecast",
    "customer_analytics": "Customer Insights",
    "financial_reports": "Financial Reports",
    "business_insights": "Business Insights",
    "performance_metrics": "Performance Metrics",
    "expense_tracking": "Expense Tracking",
    "profit_margin": "Profit Analysis",
    "cash_flow": "Cash Flow Analysis",
    "seasonal_trends": "Seasonal Trends",
    "customer_segmentation": "Customer Segmentation",
    "inventory_valuation": "Inventory Valuation",
    "business_health": "Business Health Score",
    "kpi_dashboard": "KPI Dashboard",
    "sales_comparison": "Sales Comparison",
    "feature_explanation": "What this means:",
    "premium_feature": "PREMIUM FEATURE",
    "staff_management": "Staff Performance",
    "supplier_analysis": "Supplier Analysis",
    "break_even": "Break-Even Analysis",
    "tax_calculator": "Tax Calculator",
    "business_goals": "Business Goals Tracker"
}

SWAHILI_TEXTS = {
    "add_sale": "Ongeza Mauzo",
    "view_reports": "Angalia Ripoti",
    "inventory": "Hesabu ya Bidhaa",
    "subscribe": "Jiunge Premium",
    "business_name": "Weka Jina la Biashara",
    "date": "Tarehe",
    "customer": "Jina la Mteja",
    "product": "Jina la Bidhaa",
    "quantity": "Idadi",
    "price": "Bei (TZS)",
    "add_button": "Ongeza Mauzo",
    "total_sales": "Jumla ya Mauzo",
    "transactions": "Idadi ya Mauzo",
    "avg_sale": "Wastani wa Mauzo",
    "premium_locked": "Vipengele vya premium vimefungwa. Jiunge kufungua uchambuzi wa hali ya juu.",
    "premium_unlocked": "Premium Imefunguliwa! Pata viungo vyote vya hali ya juu.",
    "sales_trend": "Uchambuzi wa Mwenendo wa Mauzo",
    "top_customers": "Uchambuzi wa Wateja",
    "product_performance": "Utendaji wa Bidhaa",
    "sales_distribution": "Mgawanyo wa Mauzo",
    "export_data": "Pakua Data",
    "download_csv": "Pakua CSV",
    "inventory_management": "Usimamizi wa Hesabu",
    "add_stock": "Ongeza Hesabu",
    "current_stock": "Hesabu ya Sasa",
    "update_stock": "Sasisha Hesabu",
    "subscribe_title": "Jiunge kwa Premium",
    "features_title": "Vipengele 15+ vya Premium",
    "choose_plan": "Chagua Mpango Wako",
    "payment_instructions": "Maelekezo ya Malipo",
    "contact_whatsapp": "Wasiliana kupitia WhatsApp",
    "developed_by": "Imetengenezwa na",
    "contact": "Wasiliana",
    "sales_forecast": "Utabiri wa Mauzo",
    "customer_analytics": "Ufahamu wa Wateja",
    "financial_reports": "Ripoti za Kifedha",
    "business_insights": "Ufahamu wa Biashara",
    "performance_metrics": "Vipimo vya Utendaji",
    "expense_tracking": "Ufuatiliaji wa Matumizi",
    "profit_margin": "Uchambuzi wa Faida",
    "cash_flow": "Uchambuzi wa Mfumuko wa Fedha",
    "seasonal_trends": "Mienendo ya Msimu",
    "customer_segmentation": "Mgawanyo wa Wateja",
    "inventory_valuation": "Thamani ya Hesabu",
    "business_health": "Hali ya Biashara",
    "kpi_dashboard": "Dashibodi ya Vipimo",
    "sales_comparison": "Kulinganisha kwa Mauzo",
    "feature_explanation": "Maana ya hii:",
    "premium_feature": "KIPENGEELE CHA PREMIUM",
    "staff_management": "Utendaji wa Wafanyikazi",
    "supplier_analysis": "Uchambuzi wa Wauzaji",
    "break_even": "Uchambuzi wa Bei ya Kuzidia",
    "tax_calculator": "Kikokotoo cha Kodi",
    "business_goals": "Kifuatiliaji Malengo ya Biashara"
}


def get_text(key):
    return SWAHILI_TEXTS[key] if st.session_state.get('language', 'English') == "Swahili" else ENGLISH_TEXTS[key]


# Initialize Session State
if 'current_business' not in st.session_state:
    st.session_state.current_business = ""
if 'premium_access' not in st.session_state:
    st.session_state.premium_access = False
if 'sales_df' not in st.session_state:
    st.session_state.sales_df = pd.DataFrame()
if 'inventory_df' not in st.session_state:
    st.session_state.inventory_df = pd.DataFrame()
if 'expenses_df' not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame()
if 'staff_df' not in st.session_state:
    st.session_state.staff_df = pd.DataFrame()
if 'suppliers_df' not in st.session_state:
    st.session_state.suppliers_df = pd.DataFrame()
if 'goals_df' not in st.session_state:
    st.session_state.goals_df = pd.DataFrame()
if 'premium_expiry' not in st.session_state:
    st.session_state.premium_expiry = None
if 'language' not in st.session_state:
    st.session_state.language = "English"
if 'selected_plan' not in st.session_state:
    st.session_state.selected_plan = None

# Data Functions


def get_business_filename(business_name, file_type="sales"):
    safe_name = "".join(c for c in business_name if c.isalnum()
                        or c in (' ', '-', '_')).rstrip()
    return f"{safe_name}_{file_type}.csv".replace(' ', '_')


def load_data(business_name, file_type="sales"):
    if not business_name:
        return pd.DataFrame()

    filename = get_business_filename(business_name, file_type)

    # If file doesn't exist, create an empty DataFrame with appropriate columns
    if not os.path.exists(filename):
        if file_type == "sales":
            df = pd.DataFrame(columns=['Date', 'Customer', 'Product',
                              'Quantity', 'Unit Price', 'Total', 'Cost Price', 'Profit'])
            df.to_csv(filename, index=False)
            return df
        elif file_type == "inventory":
            df = pd.DataFrame(columns=[
                              'Product', 'Current_Stock', 'Minimum_Stock', 'Cost_Price', 'Selling_Price', 'Last_Updated'])
            df.to_csv(filename, index=False)
            return df
        elif file_type == "expenses":
            df = pd.DataFrame(
                columns=['Date', 'Category', 'Description', 'Amount'])
            df.to_csv(filename, index=False)
            return df
        elif file_type == "staff":
            df = pd.DataFrame(
                columns=['Name', 'Position', 'Salary', 'Performance', 'Join_Date'])
            df.to_csv(filename, index=False)
            return df
        elif file_type == "suppliers":
            df = pd.DataFrame(
                columns=['Name', 'Product', 'Price', 'Rating', 'Delivery_Time'])
            df.to_csv(filename, index=False)
            return df
        elif file_type == "goals":
            df = pd.DataFrame(
                columns=['Goal', 'Target', 'Current', 'Deadline', 'Status'])
            df.to_csv(filename, index=False)
            return df

    # If file exists, load it
    try:
        df = pd.read_csv(filename)
        if file_type == "sales" and not df.empty and 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # If there's an error reading the file, create a new empty DataFrame
        if file_type == "sales":
            return pd.DataFrame(columns=['Date', 'Customer', 'Product', 'Quantity', 'Unit Price', 'Total', 'Cost Price', 'Profit'])
        elif file_type == "inventory":
            return pd.DataFrame(columns=['Product', 'Current_Stock', 'Minimum_Stock', 'Cost_Price', 'Selling_Price', 'Last_Updated'])
        elif file_type == "expenses":
            return pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])
        elif file_type == "staff":
            return pd.DataFrame(columns=['Name', 'Position', 'Salary', 'Performance', 'Join_Date'])
        elif file_type == "suppliers":
            return pd.DataFrame(columns=['Name', 'Product', 'Price', 'Rating', 'Delivery_Time'])
        elif file_type == "goals":
            return pd.DataFrame(columns=['Goal', 'Target', 'Current', 'Deadline', 'Status'])


def save_data(df, business_name, file_type="sales"):
    if not business_name:
        return

    filename = get_business_filename(business_name, file_type)
    df.to_csv(filename, index=False)


def update_inventory(business_name, product_name, quantity_sold, cost_price, selling_price):
    inventory_df = load_data(business_name, "inventory")
    if not inventory_df.empty and product_name in inventory_df['Product'].values:
        current_stock = inventory_df.loc[inventory_df['Product']
                                         == product_name, 'Current_Stock'].values[0]
        new_stock = max(0, current_stock - quantity_sold)
        inventory_df.loc[inventory_df['Product'] ==
                         product_name, 'Current_Stock'] = new_stock
    else:
        new_product = pd.DataFrame({
            'Product': [product_name],
            'Current_Stock': [max(0, -quantity_sold)],
            'Minimum_Stock': [10],
            'Cost_Price': [cost_price],
            'Selling_Price': [selling_price],
            'Last_Updated': [datetime.now().strftime('%Y-%m-%d')]
        })
        inventory_df = pd.concat(
            [inventory_df, new_product], ignore_index=True)

    inventory_df.loc[inventory_df['Product'] == product_name,
                     'Last_Updated'] = datetime.now().strftime('%Y-%m-%d')
    save_data(inventory_df, business_name, "inventory")
    return inventory_df


def add_to_inventory(business_name, product_name, quantity_added, cost_price, selling_price):
    inventory_df = load_data(business_name, "inventory")
    if not inventory_df.empty and product_name in inventory_df['Product'].values:
        current_stock = inventory_df.loc[inventory_df['Product']
                                         == product_name, 'Current_Stock'].values[0]
        inventory_df.loc[inventory_df['Product'] == product_name,
                         'Current_Stock'] = current_stock + quantity_added
        inventory_df.loc[inventory_df['Product'] ==
                         product_name, 'Cost_Price'] = cost_price
        inventory_df.loc[inventory_df['Product'] ==
                         product_name, 'Selling_Price'] = selling_price
    else:
        new_product = pd.DataFrame({
            'Product': [product_name],
            'Current_Stock': [quantity_added],
            'Minimum_Stock': [10],
            'Cost_Price': [cost_price],
            'Selling_Price': [selling_price],
            'Last_Updated': [datetime.now().strftime('%Y-%m-%d')]
        })
        inventory_df = pd.concat(
            [inventory_df, new_product], ignore_index=True)

    inventory_df.loc[inventory_df['Product'] == product_name,
                     'Last_Updated'] = datetime.now().strftime('%Y-%m-%d')
    save_data(inventory_df, business_name, "inventory")
    return inventory_df


def add_expense(business_name, date, category, description, amount):
    expenses_df = load_data(business_name, "expenses")
    new_expense = pd.DataFrame({
        'Date': [date],
        'Category': [category],
        'Description': [description],
        'Amount': [amount]
    })
    expenses_df = pd.concat([expenses_df, new_expense], ignore_index=True)
    save_data(expenses_df, business_name, "expenses")
    return expenses_df


def add_staff(business_name, name, position, salary, performance, join_date):
    staff_df = load_data(business_name, "staff")
    new_staff = pd.DataFrame({
        'Name': [name],
        'Position': [position],
        'Salary': [salary],
        'Performance': [performance],
        'Join_Date': [join_date]
    })
    staff_df = pd.concat([staff_df, new_staff], ignore_index=True)
    save_data(staff_df, business_name, "staff")
    return staff_df


def add_supplier(business_name, name, product, price, rating, delivery_time):
    suppliers_df = load_data(business_name, "suppliers")
    new_supplier = pd.DataFrame({
        'Name': [name],
        'Product': [product],
        'Price': [price],
        'Rating': [rating],
        'Delivery_Time': [delivery_time]
    })
    suppliers_df = pd.concat([suppliers_df, new_supplier], ignore_index=True)
    save_data(suppliers_df, business_name, "suppliers")
    return suppliers_df


def add_goal(business_name, goal, target, current, deadline, status):
    goals_df = load_data(business_name, "goals")
    new_goal = pd.DataFrame({
        'Goal': [goal],
        'Target': [target],
        'Current': [current],
        'Deadline': [deadline],
        'Status': [status]
    })
    goals_df = pd.concat([goals_df, new_goal], ignore_index=True)
    save_data(goals_df, business_name, "goals")
    return goals_df

# Premium Features Functions


def generate_sales_forecast(sales_df):
    if sales_df.empty or len(sales_df) < 10:
        return None, "Not enough data for accurate forecasting"

    # Simple forecasting using moving average
    daily_sales = sales_df.groupby('Date')['Total'].sum().reset_index()
    daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])
    daily_sales = daily_sales.set_index('Date').asfreq('D').fillna(0)

    # Calculate 7-day moving average
    forecast_values = daily_sales.rolling(7).mean().iloc[-30:]

    # Create forecast dates
    last_date = daily_sales.index.max()
    forecast_dates = pd.date_range(
        start=last_date + timedelta(days=1), periods=30)

    # Create forecast dataframe
    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        # Simple average of last 7 days
        'Forecast': forecast_values['Total'].mean()
    })

    return forecast_df, "Forecast generated successfully"


def calculate_profit_margins(sales_df, inventory_df):
    if sales_df.empty or inventory_df.empty:
        return pd.DataFrame()

    # Merge sales and inventory data
    profit_data = sales_df.merge(inventory_df, on='Product', how='left')

    # Calculate profit metrics
    if 'Cost_Price' in profit_data.columns and 'Selling_Price' in profit_data.columns:
        profit_data['Profit'] = (
            profit_data['Selling_Price'] - profit_data['Cost_Price']) * profit_data['Quantity']
        profit_data['Profit_Margin'] = (
            profit_data['Profit'] / (profit_data['Selling_Price'] * profit_data['Quantity'])) * 100

    return profit_data


def calculate_business_health(sales_df, expenses_df, inventory_df):
    if sales_df.empty:
        return 0, "Insufficient data"

    # Calculate basic health score (0-100)
    total_sales = sales_df['Total'].sum()
    total_expenses = expenses_df['Amount'].sum(
    ) if not expenses_df.empty else 0
    total_profit = sales_df['Profit'].sum(
    ) if 'Profit' in sales_df.columns else total_sales * 0.2  # Estimate if not available

    # Simple health score calculation
    if total_sales > 0:
        profit_margin = (total_profit / total_sales) * 100
        expense_ratio = (total_expenses / total_sales) * \
            100 if total_sales > 0 else 0

        # Health score based on profit margin and expense ratio
        health_score = max(0, min(100, profit_margin *
                           1.5 - expense_ratio * 0.5 + 50))

        status = "Excellent" if health_score >= 80 else "Good" if health_score >= 60 else "Fair" if health_score >= 40 else "Needs Improvement"

        return round(health_score, 1), status
    else:
        return 0, "No sales data"


def calculate_break_even(fixed_costs, variable_costs, selling_price):
    if selling_price - variable_costs <= 0:
        return 0, "Cannot calculate - selling price must be higher than variable costs"

    break_even_units = fixed_costs / (selling_price - variable_costs)
    break_even_sales = break_even_units * selling_price
    return break_even_units, break_even_sales


def calculate_tax(income, expenses, tax_rate=0.3):
    taxable_income = max(0, income - expenses)
    tax_amount = taxable_income * tax_rate
    return tax_amount


# Header
st.markdown('<h1 class="main-header">📊 BizTrack Pro Tanzania</h1>',
            unsafe_allow_html=True)

# Language Switcher
language = st.radio("", ["English", "Swahili"], horizontal=True,
                    index=0 if st.session_state.language == "English" else 1)
if language != st.session_state.language:
    st.session_state.language = language
    st.rerun()

# Sidebar
with st.sidebar:
    st.header(f"🏢 {get_text('business_name')}")
    business_name = st.text_input("", key="business_input")

    if business_name and business_name != st.session_state.current_business:
        st.session_state.current_business = business_name
        st.session_state.sales_df = load_data(business_name, "sales")
        st.session_state.inventory_df = load_data(business_name, "inventory")
        st.session_state.expenses_df = load_data(business_name, "expenses")
        st.session_state.staff_df = load_data(business_name, "staff")
        st.session_state.suppliers_df = load_data(business_name, "suppliers")
        st.session_state.goals_df = load_data(business_name, "goals")
        st.success(f"✅ {business_name} loaded!")

    if st.session_state.current_business:
        st.success(
            f"🔵 {get_text('business_name')}: {st.session_state.current_business}")

    # Premium Access
    st.header("💎 Premium Access")
    if st.session_state.premium_access:
        st.success("✅ Premium Active")
        if st.session_state.premium_expiry:
            st.info(
                f"Expiry: {st.session_state.premium_expiry.strftime('%Y-%m-%d')}")
        if st.button("🔓 Logout Premium"):
            st.session_state.premium_access = False
            st.rerun()
    else:
        password = st.text_input("Password", type="password")
        if st.button("🚀 Unlock Premium"):
            if password == PREMIUM_PASSWORD:
                st.session_state.premium_access = True
                st.session_state.premium_expiry = datetime.now().date() + timedelta(days=30)
                st.success("✅ Premium Unlocked!")
                st.rerun()
            else:
                st.error("❌ Incorrect Password")

# Main Content
if not st.session_state.current_business:
    st.info("👆 Please enter your business name to get started")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    get_text("add_sale"),
    get_text("view_reports"),
    get_text("inventory"),
    get_text("expense_tracking"),
    get_text("staff_management"),
    get_text("supplier_analysis"),
    get_text("subscribe")
])

# Tab 1: Add Sale
with tab1:
    st.header(f"➕ {get_text('add_sale')}")

    with st.form("sale_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input(get_text("date"), datetime.today())
            customer = st.text_input(get_text("customer"))
            product = st.text_input(get_text("product"))
        with col2:
            quantity = st.number_input(
                get_text("quantity"), min_value=1, value=1)
            unit_price = st.number_input(
                get_text("price"), min_value=0.0, value=0.0)
            cost_price = st.number_input(
                "Cost Price (TZS)", min_value=0.0, value=0.0)

        if st.form_submit_button(f"🚀 {get_text('add_button')}"):
            total = quantity * unit_price
            profit = (unit_price - cost_price) * quantity

            new_sale = pd.DataFrame({
                'Date': [date], 'Customer': [customer], 'Product': [product],
                'Quantity': [quantity], 'Unit Price': [unit_price], 'Total': [total],
                'Cost Price': [cost_price], 'Profit': [profit]
            })

            updated_df = pd.concat(
                [st.session_state.sales_df, new_sale], ignore_index=True)
            st.session_state.sales_df = updated_df
            save_data(updated_df, st.session_state.current_business, "sales")

            st.session_state.inventory_df = update_inventory(
                st.session_state.current_business, product, quantity, cost_price, unit_price
            )

            st.success(
                f"✅ Added! Total: TZS {total:,.2f}, Profit: TZS {profit:,.2f}")

# Tab 2: View Reports
with tab2:
    st.header(f"📈 {get_text('view_reports')}")

    if st.session_state.sales_df.empty:
        st.info("No sales data yet. Add your first sale!")
    else:
        total_sales = st.session_state.sales_df['Total'].sum()
        total_transactions = len(st.session_state.sales_df)
        avg_sale = total_sales / total_transactions if total_transactions > 0 else 0
        total_profit = st.session_state.sales_df['Profit'].sum(
        ) if 'Profit' in st.session_state.sales_df.columns else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric(get_text("total_sales"), f"TZS {total_sales:,.2f}")
        col2.metric(get_text("transactions"), total_transactions)
        col3.metric(get_text("avg_sale"), f"TZS {avg_sale:,.2f}")
        col4.metric(get_text("profit_margin"), f"TZS {total_profit:,.2f}")

        st.dataframe(st.session_state.sales_df, use_container_width=True)

        if not st.session_state.premium_access:
            st.warning(f"🔒 {get_text('premium_locked')}")
            # Show blurred preview of premium features
            st.markdown('<div class="premium-locked">', unsafe_allow_html=True)
            st.subheader("📈 Sales Trend Analysis (Premium)")
            st.info("Unlock premium to view detailed analytics")
            st.subheader("🏆 Customer Analytics (Premium)")
            st.info("Unlock premium to view customer insights")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success(f"🎉 {get_text('premium_unlocked')}")

            # Premium Features Section - 15+ Analytics Tools
            st.markdown("## 🎯 15+ Premium Analytics Features")

            # 1. Sales Trend Chart
            st.subheader(f"📈 {get_text('sales_trend')}")
            daily_sales = st.session_state.sales_df.groupby(
                'Date')['Total'].sum().reset_index()
            fig = px.line(daily_sales, x='Date', y='Total', title='Daily Sales Trend',
                          labels={'Total': 'Sales (TZS)', 'Date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Sales Trend Analysis** shows how your sales are performing over time. 
                - **Upward trends** indicate growing business
                - **Downward trends** may need attention
                - **Consistent patterns** help with inventory planning
                - Use this to forecast future sales and plan resources
                """)

            # 2. Top Customers
            st.subheader(f"🏆 {get_text('top_customers')}")
            customer_sales = st.session_state.sales_df.groupby(
                'Customer')['Total'].sum().sort_values(ascending=False).head(10)
            fig = px.bar(customer_sales, x=customer_sales.values, y=customer_sales.index,
                         orientation='h', title='Top 10 Customers by Sales',
                         labels={'x': 'Total Sales (TZS)', 'y': 'Customer'})
            st.plotly_chart(fig, use_container_width=True)
            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Customer Analytics** identifies your most valuable customers. 
                - **Focus marketing efforts** on top customers
                - **Identify potential** loyalty program candidates
                - **Understand customer** buying patterns
                - **Personalize offers** for high-value customers
                """)
                st.dataframe(customer_sales.reset_index().rename(
                    columns={'Customer': 'Customer Name', 'Total': 'Total Sales (TZS)'}))

            # 3. Product Performance
            st.subheader(f"📦 {get_text('product_performance')}")
            product_performance = st.session_state.sales_df.groupby(
                'Product').agg({'Quantity': 'sum', 'Total': 'sum'}).reset_index()
            fig = px.scatter(product_performance, x='Quantity', y='Total', size='Total', hover_name='Product',
                             title='Product Performance: Quantity Sold vs Revenue',
                             labels={'Quantity': 'Units Sold', 'Total': 'Total Revenue (TZS)'})
            st.plotly_chart(fig, use_container_width=True)
            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Product Performance** shows which items are your best sellers and revenue generators.
                - **Large circles** = high revenue products
                - **Right position** = high quantity sold
                - **Top-left** = high value, low volume items
                - **Bottom-right** = low value, high volume items
                """)
                st.dataframe(product_performance.sort_values(
                    'Total', ascending=False))

            # 4. Sales Distribution
            st.subheader(f"🥧 {get_text('sales_distribution')}")
            sales_by_product = st.session_state.sales_df.groupby('Product')[
                'Total'].sum()
            fig = px.pie(values=sales_by_product.values, names=sales_by_product.index,
                         title='Sales Distribution by Product', hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Sales Distribution** shows what percentage of your revenue comes from each product.
                - **Identify your most important** products
                - **Balance your product** portfolio
                - **Focus on high-performing** categories
                - **Identify underperforming** products that may need promotion
                """)

            # 5. Sales Forecast
            st.subheader(f"🔮 {get_text('sales_forecast')}")
            forecast_df, forecast_msg = generate_sales_forecast(
                st.session_state.sales_df)

            if forecast_df is not None:
                fig = px.line(forecast_df, x='Date', y='Forecast', title='30-Day Sales Forecast',
                              labels={'Forecast': 'Expected Sales (TZS)', 'Date': 'Date'})
                st.plotly_chart(fig, use_container_width=True)
                with st.expander(f"💡 {get_text('feature_explanation')}"):
                    st.markdown("""
                    **Sales Forecasting** predicts future sales based on historical data.
                    - **Plan inventory** and staffing needs
                    - **Set realistic revenue** targets
                    - **Prepare for seasonal** fluctuations
                    - **Make informed decisions** about business expansion
                    """)
                    st.dataframe(forecast_df)
            else:
                st.info(forecast_msg)

            # 6. Customer Analytics
            st.subheader(f"👥 {get_text('customer_analytics')}")
            customer_analysis = st.session_state.sales_df.groupby('Customer').agg({
                'Total': ['sum', 'count'],
                'Quantity': 'sum'
            }).round(2)
            customer_analysis.columns = [
                'Total Spent', 'Visit Count', 'Items Purchased']
            customer_analysis['Average Spend'] = (
                customer_analysis['Total Spent'] / customer_analysis['Visit Count']).round(2)
            customer_analysis = customer_analysis.sort_values(
                'Total Spent', ascending=False)

            fig = px.bar(customer_analysis.head(10), x='Total Spent', y=customer_analysis.head(10).index,
                         orientation='h', title='Top 10 Customers by Total Spending',
                         labels={'Total Spent': 'Total Amount Spent (TZS)', 'y': 'Customer'})
            st.plotly_chart(fig, use_container_width=True)
            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Customer Insights** provides detailed analysis of your customer base.
                - **Identify your most loyal** customers
                - **Understand purchasing** frequency
                - **Target marketing campaigns** effectively
                - **Develop customer retention** strategies
                """)
                st.dataframe(customer_analysis)

            # 7. Profit Margin Analysis
            st.subheader(f"💰 {get_text('profit_margin')}")
            profit_data = calculate_profit_margins(
                st.session_state.sales_df, st.session_state.inventory_df)

            if not profit_data.empty and 'Profit_Margin' in profit_data.columns:
                product_profit = profit_data.groupby(
                    'Product')['Profit_Margin'].mean().reset_index()
                fig = px.bar(product_profit.sort_values('Profit_Margin', ascending=False).head(10),
                             x='Product', y='Profit_Margin',
                             title='Top 10 Products by Profit Margin (%)',
                             labels={'Profit_Margin': 'Profit Margin %'})
                st.plotly_chart(fig, use_container_width=True)
                with st.expander(f"💡 {get_text('feature_explanation')}"):
                    st.markdown("""
                    **Profit Analysis** shows which products generate the highest profit margins.
                    - **Focus on high-margin** products
                    - **Review pricing strategy** for low-margin items
                    - **Optimize product mix** for maximum profitability
                    - **Identify opportunities** for cost reduction
                    """)
                    st.dataframe(product_profit.sort_values(
                        'Profit_Margin', ascending=False))
            else:
                st.info(
                    "Add cost prices to inventory to enable profit margin analysis")

            # 8. Monthly Performance
            st.subheader(f"📅 {get_text('performance_metrics')}")
            monthly_sales = st.session_state.sales_df.copy()
            monthly_sales['Date'] = pd.to_datetime(monthly_sales['Date'])
            monthly_sales['Month'] = monthly_sales['Date'].dt.to_period('M')
            monthly_performance = monthly_sales.groupby('Month').agg({
                'Total': 'sum',
                'Profit': 'sum',
                'Quantity': 'sum'
            }).reset_index()
            monthly_performance['Month'] = monthly_performance['Month'].astype(
                str)

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=monthly_performance['Month'], y=monthly_performance['Total'],
                                 name="Revenue", marker_color='#636EFA'))
            fig.add_trace(go.Scatter(x=monthly_performance['Month'], y=monthly_performance['Profit'],
                                     name="Profit", line=dict(color='#FFA15A')), secondary_y=True)
            fig.update_layout(title_text="Monthly Revenue and Profit",
                              xaxis_title="Month", yaxis_title="Revenue (TZS)", yaxis2_title="Profit (TZS)")
            st.plotly_chart(fig, use_container_width=True)
            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Monthly Performance** tracks your business growth over time.
                - **Compare revenue and profit** trends
                - **Identify seasonal patterns** in your business
                - **Measure business growth** month-over-month
                - **Set benchmarks** for future performance
                """)
                st.dataframe(monthly_performance)

            # 9. Inventory Valuation
            st.subheader("📊 Inventory Valuation")
            if not st.session_state.inventory_df.empty and 'Cost_Price' in st.session_state.inventory_df.columns:
                inventory_value = st.session_state.inventory_df.copy()
                inventory_value['Total Value'] = inventory_value['Current_Stock'] * \
                    inventory_value['Cost_Price']
                inventory_value = inventory_value[['Product', 'Current_Stock', 'Cost_Price', 'Total Value']].sort_values(
                    'Total Value', ascending=False)

                fig = px.treemap(inventory_value, path=['Product'], values='Total Value',
                                 title='Inventory Value by Product (TreeMap)',
                                 color='Total Value', color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)

                total_inv_value = inventory_value['Total Value'].sum()
                st.metric("Total Inventory Value",
                          f"TZS {total_inv_value:,.2f}")

                with st.expander(f"💡 {get_text('feature_explanation')}"):
                    st.markdown("""
                    **Inventory Valuation** shows the total value of your current stock.
                    - **Understand how much capital** is tied in inventory
                    - **Identify overstocked or understocked** items
                    - **Make informed purchasing** decisions
                    - **Optimize inventory management** for better cash flow
                    """)
                    st.dataframe(inventory_value)
            else:
                st.info("Add cost prices to inventory to enable value analysis")

            # 10. Business Health Score
            st.subheader(f"❤️ {get_text('business_health')}")
            health_score, health_status = calculate_business_health(
                st.session_state.sales_df, st.session_state.expenses_df, st.session_state.inventory_df)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=health_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Business Health Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "red"},
                        {'range': [40, 60], 'color': "orange"},
                        {'range': [60, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': health_score}}))

            st.plotly_chart(fig, use_container_width=True)
            st.metric("Business Health Status", health_status)

            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Business Health Score** provides an overall assessment of your business performance.
                - **80-100: Excellent** - Your business is thriving and profitable
                - **60-79: Good** - Solid performance with room for improvement
                - **40-59: Fair** - Needs attention to key areas like costs or pricing
                - **0-39: Needs Improvement** - Immediate action required to avoid losses
                """)

            # 11. Cash Flow Analysis
            st.subheader(f"💵 {get_text('cash_flow')}")
            if not st.session_state.expenses_df.empty:
                cash_flow_data = pd.concat([
                    st.session_state.sales_df[['Date', 'Total']].rename(
                        columns={'Total': 'Amount'}).assign(Type='Income'),
                    st.session_state.expenses_df[[
                        'Date', 'Amount']].assign(Type='Expense')
                ])
                cash_flow_data['Date'] = pd.to_datetime(cash_flow_data['Date'])
                cash_flow_monthly = cash_flow_data.groupby([cash_flow_data['Date'].dt.to_period(
                    'M'), 'Type'])['Amount'].sum().unstack().fillna(0)
                cash_flow_monthly['Net Cash Flow'] = cash_flow_monthly.get(
                    'Income', 0) - cash_flow_monthly.get('Expense', 0)
                cash_flow_monthly = cash_flow_monthly.reset_index()
                cash_flow_monthly['Date'] = cash_flow_monthly['Date'].astype(
                    str)

                fig = px.line(cash_flow_monthly, x='Date', y='Net Cash Flow',
                              title='Monthly Net Cash Flow', markers=True,
                              labels={'Net Cash Flow': 'Net Cash Flow (TZS)', 'Date': 'Month'})
                st.plotly_chart(fig, use_container_width=True)

                with st.expander(f"💡 {get_text('feature_explanation')}"):
                    st.markdown("""
                    **Cash Flow Analysis** tracks the movement of money in and out of your business.
                    - **Positive values**: More money coming in than going out (Healthy)
                    - **Negative values**: More expenses than income (Concerning)
                    - **Essential for financial planning** and sustainability
                    - **Helps anticipate cash shortages** before they happen
                    """)
                    st.dataframe(cash_flow_monthly)
            else:
                st.info("Add expense data to enable cash flow analysis")

            # 12. Seasonal Trends
            st.subheader(f"🌦️ {get_text('seasonal_trends')}")
            sales_seasonal = st.session_state.sales_df.copy()
            sales_seasonal['Date'] = pd.to_datetime(sales_seasonal['Date'])
            sales_seasonal['Month'] = sales_seasonal['Date'].dt.month
            sales_seasonal['Month_Name'] = sales_seasonal['Date'].dt.month_name()
            monthly_trends = sales_seasonal.groupby(['Month', 'Month_Name'])[
                'Total'].sum().reset_index()

            fig = px.line(monthly_trends, x='Month_Name', y='Total', title='Monthly Sales Trends',
                          category_orders={'Month_Name': ['January', 'February', 'March', 'April', 'May', 'June',
                                                          'July', 'August', 'September', 'October', 'November', 'December']},
                          labels={'Total': 'Total Sales (TZS)', 'Month_Name': 'Month'})
            st.plotly_chart(fig, use_container_width=True)

            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Seasonal Trends** shows how your sales vary by month throughout the year.
                - **Identify peak seasons** for your business
                - **Plan inventory and staffing** for busy periods
                - **Develop targeted marketing** for slow seasons
                - **Optimize business operations** based on seasonal patterns
                """)
                st.dataframe(monthly_trends.sort_values('Month'))

            # 13. Customer Segmentation
            st.subheader(f"👥 {get_text('customer_segmentation')}")
            customer_segments = st.session_state.sales_df.groupby('Customer').agg({
                'Total': 'sum',
                'Date': 'count'
            }).rename(columns={'Total': 'Total_Spent', 'Date': 'Visit_Count'})
            customer_segments['Customer_Type'] = pd.cut(customer_segments['Total_Spent'],
                                                        bins=[
                                                            0, 10000, 50000, float('inf')],
                                                        labels=['Small', 'Medium', 'Large'])

            segment_summary = customer_segments.groupby('Customer_Type').agg({
                'Total_Spent': ['count', 'sum'],
                'Visit_Count': 'mean'
            }).round(2)
            segment_summary.columns = [
                'Number_of_Customers', 'Total_Revenue', 'Average_Visits']

            fig = px.pie(segment_summary, values='Number_of_Customers', names=segment_summary.index,
                         title='Customer Segmentation by Spending Level')
            st.plotly_chart(fig, use_container_width=True)

            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Customer Segmentation** categorizes your customers based on their spending behavior.
                - **Large Spenders**: Your most valuable customers (focus on retention)
                - **Medium Spenders**: Potential for growth (offer premium products)
                - **Small Spenders**: New or occasional customers (focus on conversion)
                - **Helps tailor marketing strategies** to each segment
                """)
                st.dataframe(segment_summary)

            # 14. KPI Dashboard
            st.subheader(f"📊 {get_text('kpi_dashboard')}")
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

            # Calculate KPIs
            avg_daily_sales = daily_sales['Total'].mean(
            ) if not daily_sales.empty else 0
            best_sales_day = daily_sales.loc[daily_sales['Total'].idxmax(
            )] if not daily_sales.empty else None
            customer_count = len(
                st.session_state.sales_df['Customer'].unique())
            avg_transaction_value = total_sales / \
                total_transactions if total_transactions > 0 else 0

            with kpi_col1:
                st.metric("Average Daily Sales", f"TZS {avg_daily_sales:,.2f}")
            with kpi_col2:
                if best_sales_day is not None:
                    st.metric("Best Sales Day",
                              f"TZS {best_sales_day['Total']:,.2f}")
                else:
                    st.metric("Best Sales Day", "N/A")
            with kpi_col3:
                st.metric("Unique Customers", customer_count)
            with kpi_col4:
                st.metric("Avg Transaction Value",
                          f"TZS {avg_transaction_value:,.2f}")

            # Additional KPIs
            kpi_col5, kpi_col6, kpi_col7, kpi_col8 = st.columns(4)
            with kpi_col5:
                st.metric("Total Profit", f"TZS {total_profit:,.2f}")
            with kpi_col6:
                profit_margin = (total_profit / total_sales *
                                 100) if total_sales > 0 else 0
                st.metric("Profit Margin", f"{profit_margin:.1f}%")
            with kpi_col7:
                inventory_value = st.session_state.inventory_df['Current_Stock'].sum(
                ) if not st.session_state.inventory_df.empty else 0
                st.metric("Total Inventory Items", f"{inventory_value:,.0f}")
            with kpi_col8:
                expenses_total = st.session_state.expenses_df['Amount'].sum(
                ) if not st.session_state.expenses_df.empty else 0
                st.metric("Total Expenses", f"TZS {expenses_total:,.2f}")

            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **KPI Dashboard** provides key performance indicators for your business at a glance.
                - **Monitor essential business metrics** in one place
                - **Track progress toward business goals**
                - **Make data-driven decisions quickly**
                - **Identify areas needing immediate attention**
                """)

            # 15. Sales Comparison
            st.subheader(f"📋 {get_text('sales_comparison')}")
            if len(st.session_state.sales_df) >= 2:
                sales_comparison = st.session_state.sales_df.copy()
                sales_comparison['Date'] = pd.to_datetime(
                    sales_comparison['Date'])
                sales_comparison['Period'] = sales_comparison['Date'].dt.to_period(
                    'M')

                period_stats = sales_comparison.groupby('Period').agg({
                    'Total': ['sum', 'count', 'mean'],
                    'Profit': 'sum'
                }).round(2)
                period_stats.columns = [
                    'Total_Sales', 'Transaction_Count', 'Average_Sale', 'Total_Profit']
                period_stats['Sales_Growth'] = period_stats['Total_Sales'].pct_change(
                ) * 100

                fig = go.Figure()
                fig.add_trace(go.Bar(x=period_stats.index.astype(str), y=period_stats['Total_Sales'],
                                     name='Total Sales', marker_color='#636EFA'))
                fig.add_trace(go.Scatter(x=period_stats.index.astype(str), y=period_stats['Sales_Growth'],
                                         name='Growth %', yaxis='y2', line=dict(color='#FFA15A')))

                fig.update_layout(
                    title='Sales Comparison with Growth Rate',
                    xaxis_title='Period',
                    yaxis_title='Total Sales (TZS)',
                    yaxis2=dict(title='Growth %', overlaying='y', side='right')
                )

                st.plotly_chart(fig, use_container_width=True)

                with st.expander(f"💡 {get_text('feature_explanation')}"):
                    st.markdown("""
                    **Sales Comparison** shows your business performance across different time periods.
                    - **Track month-over-month growth**
                    - **Identify trends and patterns**
                    - **Compare performance across periods**
                    - **Set realistic growth targets** based on historical data
                    """)
                    st.dataframe(period_stats)
            else:
                st.info("Need at least 2 months of data for comparison analysis")

            # 16. Break-Even Analysis
            st.subheader(f"⚖️ {get_text('break_even')}")
            col1, col2, col3 = st.columns(3)
            with col1:
                fixed_costs = st.number_input(
                    "Fixed Costs (TZS)", min_value=0.0, value=100000.0)
            with col2:
                variable_costs = st.number_input(
                    "Variable Costs per Unit (TZS)", min_value=0.0, value=5000.0)
            with col3:
                selling_price = st.number_input(
                    "Selling Price per Unit (TZS)", min_value=0.0, value=10000.0)

            break_even_units, break_even_sales = calculate_break_even(
                fixed_costs, variable_costs, selling_price)

            if isinstance(break_even_units, str):
                st.error(break_even_units)
            else:
                st.metric("Break-Even Point (Units)",
                          f"{break_even_units:,.0f}")
                st.metric("Break-Even Sales (TZS)",
                          f"TZS {break_even_sales:,.2f}")

                # Visualization
                units_range = np.linspace(0, break_even_units * 2, 100)
                total_costs = fixed_costs + variable_costs * units_range
                total_revenue = selling_price * units_range

                break_even_df = pd.DataFrame({
                    'Units': units_range,
                    'Total_Costs': total_costs,
                    'Total_Revenue': total_revenue
                })

                fig = px.line(break_even_df, x='Units', y=['Total_Costs', 'Total_Revenue'],
                              title='Break-Even Analysis', labels={'value': 'Amount (TZS)', 'variable': 'Type'})
                fig.add_vline(x=break_even_units, line_dash="dash", line_color="red",
                              annotation_text=f"Break-Even: {break_even_units:,.0f} units")
                st.plotly_chart(fig, use_container_width=True)

                with st.expander(f"💡 {get_text('feature_explanation')}"):
                    st.markdown("""
                    **Break-Even Analysis** shows when your business will start making a profit.
                    - **Fixed Costs**: Expenses that don't change with sales volume (rent, salaries)
                    - **Variable Costs**: Expenses that increase with each unit sold (materials, packaging)
                    - **Break-Even Point**: Where total revenue equals total costs
                    - **Essential for pricing decisions** and financial planning
                    """)

            # 17. Tax Calculator
            st.subheader(f"🧮 {get_text('tax_calculator')}")
            col1, col2 = st.columns(2)
            with col1:
                annual_income = st.number_input(
                    "Annual Income (TZS)", min_value=0.0, value=5000000.0)
            with col2:
                annual_expenses = st.number_input(
                    "Annual Expenses (TZS)", min_value=0.0, value=2000000.0)

            tax_amount = calculate_tax(annual_income, annual_expenses)
            net_profit = annual_income - annual_expenses - tax_amount

            st.metric("Taxable Income",
                      f"TZS {max(0, annual_income - annual_expenses):,.2f}")
            st.metric("Estimated Tax (30%)", f"TZS {tax_amount:,.2f}")
            st.metric("Net Profit After Tax", f"TZS {net_profit:,.2f}")

            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Tax Calculator** helps estimate your business tax obligations.
                - **Based on Tanzanian corporate tax rate** of 30%
                - **Taxable Income** = Annual Income - Annual Expenses
                - **Plan for tax payments** throughout the year
                - **Understand your net profit** after taxes
                """)

            # Export Data
            st.subheader(f"💾 {get_text('export_data')}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                sales_csv = st.session_state.sales_df.to_csv(index=False)
                st.download_button(f"📥 Sales {get_text('download_csv')}", data=sales_csv,
                                   file_name="sales_data.csv", mime="text/csv")
            with col2:
                inventory_csv = st.session_state.inventory_df.to_csv(
                    index=False)
                st.download_button(f"📥 Inventory {get_text('download_csv')}", data=inventory_csv,
                                   file_name="inventory_data.csv", mime="text/csv")
            with col3:
                expenses_csv = st.session_state.expenses_df.to_csv(index=False)
                st.download_button(f"📥 Expenses {get_text('download_csv')}", data=expenses_csv,
                                   file_name="expenses_data.csv", mime="text/csv")
            with col4:
                # Create a summary report
                summary_data = {
                    'Metric': ['Total Sales', 'Total Profit', 'Number of Transactions', 'Unique Customers'],
                    'Value': [total_sales, total_profit, total_transactions, customer_count]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_csv = summary_df.to_csv(index=False)
                st.download_button("📥 Summary Report", data=summary_csv,
                                   file_name="business_summary.csv", mime="text/csv")

# Tab 3: Inventory Management
with tab3:
    st.header(f"📦 {get_text('inventory_management')}")

    # Add Stock Form
    st.subheader(f"➕ {get_text('add_stock')}")
    with st.form("add_stock_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            product_name = st.text_input(get_text("product"))
        with col2:
            quantity = st.number_input(
                get_text("quantity"), min_value=1, value=1)
        with col3:
            cost_price = st.number_input(
                "Cost Price (TZS)", min_value=0.0, value=0.0)
            selling_price = st.number_input(
                "Selling Price (TZS)", min_value=0.0, value=0.0)

        if st.form_submit_button(f"✅ {get_text('add_stock')}"):
            if product_name:
                st.session_state.inventory_df = add_to_inventory(
                    st.session_state.current_business, product_name, quantity, cost_price, selling_price
                )
                st.success(
                    f"Added {quantity} units of {product_name} to inventory!")

    # Current Inventory
    st.subheader(f"📊 {get_text('current_stock')}")
    if st.session_state.inventory_df.empty:
        st.info("No inventory data yet. Add stock using the form above.")
    else:
        st.dataframe(st.session_state.inventory_df, use_container_width=True)

        # Low stock alerts
        if 'Current_Stock' in st.session_state.inventory_df.columns and 'Minimum_Stock' in st.session_state.inventory_df.columns:
            low_stock = st.session_state.inventory_df[st.session_state.inventory_df['Current_Stock'] <
                                                      st.session_state.inventory_df['Minimum_Stock']]
            if not low_stock.empty:
                st.warning(
                    "⚠️ Low Stock Alert! These products need restocking:")
                st.dataframe(
                    low_stock[['Product', 'Current_Stock', 'Minimum_Stock']])

# Tab 4: Expense Tracking
with tab4:
    st.header(f"💸 {get_text('expense_tracking')}")

    if not st.session_state.premium_access:
        st.warning(f"🔒 {get_text('premium_locked')}")
        st.info("Subscribe to Premium to unlock Expense Tracking features")
    else:
        with st.form("expense_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                exp_date = st.date_input(
                    get_text("date"), datetime.today(), key="expense_date")
                category = st.selectbox(
                    "Category", ["Rent", "Utilities", "Salaries", "Supplies", "Marketing", "Other"])
            with col2:
                description = st.text_input("Description")
                amount = st.number_input(
                    "Amount (TZS)", min_value=0.0, value=0.0)

            if st.form_submit_button("➕ Add Expense"):
                st.session_state.expenses_df = add_expense(
                    st.session_state.current_business, exp_date, category, description, amount
                )
                st.success(f"Added expense: {description} - TZS {amount:,.2f}")

        # Display Expenses
        if not st.session_state.expenses_df.empty:
            st.subheader("Expense Summary")
            total_expenses = st.session_state.expenses_df['Amount'].sum()
            st.metric("Total Expenses", f"TZS {total_expenses:,.2f}")

            # Expense by category
            expense_by_category = st.session_state.expenses_df.groupby(
                'Category')['Amount'].sum().reset_index()
            fig = px.pie(expense_by_category, values='Amount',
                         names='Category', title='Expenses by Category')
            st.plotly_chart(fig, use_container_width=True)

            # Monthly expenses trend
            expenses_monthly = st.session_state.expenses_df.copy()
            expenses_monthly['Date'] = pd.to_datetime(expenses_monthly['Date'])
            expenses_monthly['Month'] = expenses_monthly['Date'].dt.to_period(
                'M')
            monthly_expenses = expenses_monthly.groupby(
                'Month')['Amount'].sum().reset_index()
            monthly_expenses['Month'] = monthly_expenses['Month'].astype(str)

            fig = px.line(monthly_expenses, x='Month', y='Amount',
                          title='Monthly Expenses Trend', markers=True)
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(st.session_state.expenses_df,
                         use_container_width=True)

            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Expense Tracking** helps you monitor and control your business costs.
                - **Identify major expense categories** and find savings opportunities
                - **Track spending patterns** over time to budget effectively
                - **Compare expenses to revenue** to maintain profitability
                - **Plan for future expenses** and avoid cash flow problems
                """)

# Tab 5: Staff Management
with tab5:
    st.header(f"👥 {get_text('staff_management')}")

    if not st.session_state.premium_access:
        st.warning(f"🔒 {get_text('premium_locked')}")
        st.info("Subscribe to Premium to unlock Staff Management features")
    else:
        with st.form("staff_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Staff Name")
                position = st.selectbox(
                    "Position", ["Manager", "Sales", "Cashier", "Cleaner", "Other"])
            with col2:
                salary = st.number_input(
                    "Monthly Salary (TZS)", min_value=0.0, value=0.0)
                performance = st.slider("Performance Rating", 1, 10, 7)
            with col3:
                join_date = st.date_input("Join Date", datetime.today())

            if st.form_submit_button("➕ Add Staff"):
                st.session_state.staff_df = add_staff(
                    st.session_state.current_business, name, position, salary, performance, join_date
                )
                st.success(f"Added staff: {name}")

        # Display Staff
        if not st.session_state.staff_df.empty:
            st.subheader("Staff Performance Summary")
            total_salary = st.session_state.staff_df['Salary'].sum()
            avg_performance = st.session_state.staff_df['Performance'].mean()

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Monthly Salary", f"TZS {total_salary:,.2f}")
            with col2:
                st.metric("Average Performance", f"{avg_performance:.1f}/10")

            # Staff performance chart
            fig = px.bar(st.session_state.staff_df, x='Name', y='Performance',
                         title='Staff Performance Ratings', color='Performance',
                         color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(st.session_state.staff_df, use_container_width=True)

            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Staff Management** helps you track employee performance and costs.
                - **Monitor salary expenses** and optimize staffing costs
                - **Track performance ratings** to identify top performers
                - **Plan training and development** based on performance data
                - **Make informed decisions** about promotions and bonuses
                """)

# Tab 6: Supplier Analysis
with tab6:
    st.header(f"📦 {get_text('supplier_analysis')}")

    if not st.session_state.premium_access:
        st.warning(f"🔒 {get_text('premium_locked')}")
        st.info("Subscribe to Premium to unlock Supplier Analysis features")
    else:
        with st.form("supplier_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Supplier Name")
                product = st.text_input("Product Supplied")
            with col2:
                price = st.number_input(
                    "Price (TZS)", min_value=0.0, value=0.0)
                rating = st.slider("Supplier Rating", 1, 10, 7)
            with col3:
                delivery_time = st.number_input(
                    "Delivery Time (Days)", min_value=1, value=3)

            if st.form_submit_button("➕ Add Supplier"):
                st.session_state.suppliers_df = add_supplier(
                    st.session_state.current_business, name, product, price, rating, delivery_time
                )
                st.success(f"Added supplier: {name}")

        # Display Suppliers
        if not st.session_state.suppliers_df.empty:
            st.subheader("Supplier Performance Summary")
            avg_rating = st.session_state.suppliers_df['Rating'].mean()
            avg_delivery = st.session_state.suppliers_df['Delivery_Time'].mean(
            )

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Average Supplier Rating", f"{avg_rating:.1f}/10")
            with col2:
                st.metric("Average Delivery Time", f"{avg_delivery:.1f} days")

            # Supplier comparison chart
            fig = px.scatter(st.session_state.suppliers_df, x='Price', y='Rating', size='Delivery_Time',
                             hover_name='Name', title='Supplier Comparison: Price vs Rating',
                             labels={'Price': 'Price (TZS)', 'Rating': 'Rating (1-10)'})
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(st.session_state.suppliers_df,
                         use_container_width=True)

            with st.expander(f"💡 {get_text('feature_explanation')}"):
                st.markdown("""
                **Supplier Analysis** helps you evaluate and compare your suppliers.
                - **Compare prices** across different suppliers
                - **Evaluate supplier reliability** through ratings and delivery times
                - **Identify best value suppliers** (good quality at reasonable price)
                - **Negotiate better terms** with performance data
                """)

# Tab 7: Subscription
with tab7:
    st.header(f"💳 {get_text('subscribe_title')}")

    if st.session_state.premium_access:
        st.success("✅ You already have premium access!")
        if st.session_state.premium_expiry:
            days_remaining = (st.session_state.premium_expiry -
                              datetime.now().date()).days
            st.info(f"Your premium access expires in {days_remaining} days")
    else:
        st.markdown(f"""
        <div class="feature-card">
            <h3>🎯 {get_text('features_title')}:</h3>
            <ul>
                <li>📈 Interactive Sales Charts & Graphs</li>
                <li>🏆 Customer Analytics & Insights</li>
                <li>📦 Product Performance Dashboard</li>
                <li>🥧 Sales Distribution Analysis</li>
                <li>🔮 30-Day Sales Forecasting</li>
                <li>💰 Profit Margin Analysis</li>
                <li>📅 Monthly Performance Reports</li>
                <li>📊 Inventory Valuation Analysis</li>
                <li>💸 Expense Tracking & Categorization</li>
                <li>❤️ Business Health Scoring</li>
                <li>💵 Cash Flow Analysis</li>
                <li>🌦️ Seasonal Trends Identification</li>
                <li>👥 Customer Segmentation</li>
                <li>📋 KPI Dashboard</li>
                <li>📊 Sales Comparison Tools</li>
                <li>👥 Staff Performance Management</li>
                <li>📦 Supplier Analysis & Comparison</li>
                <li>⚖️ Break-Even Analysis</li>
                <li>🧮 Tax Calculator</li>
                <li>💾 Advanced Data Export Options</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.subheader(f"💰 {get_text('choose_plan')}")
        col1, col2, col3, col4 = st.columns(4)
        plans = list(PREMIUM_PRICES.keys())

        for i, plan in enumerate(plans):
            with [col1, col2, col3, col4][i]:
                st.markdown("<div class='feature-card'>",
                            unsafe_allow_html=True)
                st.subheader(f"📅 {plan}")
                st.metric("Price", PREMIUM_PRICES[plan])
                if st.button(f"Choose {plan}", key=plan.lower()):
                    st.session_state.selected_plan = plan
                st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.selected_plan:
            st.markdown("---")
            plan_price = PREMIUM_PRICES[st.session_state.selected_plan]
            st.success(
                f"Selected: {st.session_state.selected_plan} Plan ({plan_price})")

            st.markdown(f"""
            <div class="success-box">
                <h4>📋 {get_text('payment_instructions')}:</h4>
                <ol>
                    <li><strong>Send {plan_price}</strong> to <strong>{MPESA_NUMBER}</strong></li>
                    <li>Use <strong>{st.session_state.current_business}</strong> as reference</li>
                    <li>Click the WhatsApp button below to send confirmation</li>
                    <li>You will receive the Premium Password immediately</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

            # Create WhatsApp message
            whatsapp_message = f"Hello! I want to subscribe to {st.session_state.selected_plan} plan. My business is {st.session_state.current_business}. I have sent {plan_price} to {MPESA_NUMBER}."
            whatsapp_url = f"https://wa.me/{MPESA_NUMBER.replace('+', '').replace(' ', '')}?text={whatsapp_message}"

            # WhatsApp button
            st.markdown(f"""
            <a href="{whatsapp_url}" target="_blank">
                <button class="whatsapp-button">
                    💬 {get_text('contact_whatsapp')}
                </button>
            </a>
            """, unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown(f'<div class="developer-info">', unsafe_allow_html=True)
st.sidebar.markdown(f"### 👨‍💻 {get_text('developed_by')}: {DEVELOPER_NAME}")
st.sidebar.markdown(f"**📞 {get_text('contact')}:** {MPESA_NUMBER}")
st.sidebar.markdown(f"**📧 Email:** {BUSINESS_EMAIL}")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Copyright notice
st.markdown(f"""
<div class="copyright">
    <p>© {COPYRIGHT_YEAR} BizTrack Pro Tanzania. All rights reserved.</p>
    <p>Developed by {DEVELOPER_NAME}. Unauthorized copying, distribution, or use of this software is prohibited.</p>
    <p>Contact: {MPESA_NUMBER} | {BUSINESS_EMAIL}</p>
</div>
""", unsafe_allow_html=True)
