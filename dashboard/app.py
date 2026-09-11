"""
Interactive Streamlit Dashboard
CodeAlpha Data Analytics Internship - Task 3

This dashboard provides interactive visualizations and insights for the online retail analytics project.
Features include KPI cards, filtering capabilities, and comprehensive business analytics.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import os
import sys

# Page configuration
st.set_page_config(
    page_title="Online Retail Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    .insight-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the cleaned dataset."""
    try:
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned', 'online_retail_cleaned.csv')
        df = pd.read_csv(data_path, parse_dates=['InvoiceDate'])
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found. Please ensure the data cleaning process has been completed.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()

@st.cache_data
def load_summary_stats():
    """Load summary statistics if available."""
    try:
        stats_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned', 'summary_stats.json')
        with open(stats_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def create_kpi_cards(df):
    """Create KPI metric cards."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Calculate KPIs
    total_revenue = df['Revenue'].sum()
    total_orders = df['InvoiceNo'].nunique()
    total_customers = df['CustomerID'].nunique()
    total_products = df['StockCode'].nunique()
    avg_order_value = df.groupby('InvoiceNo')['Revenue'].sum().mean()
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-value">£{total_revenue:,.0f}</div>
            <div class="metric-label">Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-value">{total_orders:,}</div>
            <div class="metric-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-value">{total_customers:,}</div>
            <div class="metric-label">Unique Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-value">{total_products:,}</div>
            <div class="metric-label">Products</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-value">£{avg_order_value:.0f}</div>
            <div class="metric-label">Avg Order Value</div>
        </div>
        """, unsafe_allow_html=True)

def create_filters(df):
    """Create sidebar filters."""
    st.sidebar.header("🔍 Data Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=[df['InvoiceDate'].min().date(), df['InvoiceDate'].max().date()],
        min_value=df['InvoiceDate'].min().date(),
        max_value=df['InvoiceDate'].max().date()
    )
    
    # Country filter
    countries = ['All'] + sorted(df['Country'].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        options=countries,
        default=['All']
    )
    
    # Customer type filter
    customer_types = st.sidebar.selectbox(
        "Customer Type",
        options=['All', 'Registered', 'Guest']
    )
    
    # Transaction type filter
    transaction_types = st.sidebar.selectbox(
        "Transaction Type",
        options=['All', 'Sale', 'Cancellation']
    )
    
    # Revenue range filter
    revenue_range = st.sidebar.slider(
        "Revenue Range (£)",
        min_value=float(df['Revenue'].min()),
        max_value=float(df['Revenue'].max()),
        value=(float(df['Revenue'].min()), float(df['Revenue'].max())),
        step=10.0
    )
    
    return {
        'date_range': date_range,
        'countries': selected_countries,
        'customer_type': customer_types,
        'transaction_type': transaction_types,
        'revenue_range': revenue_range
    }

def apply_filters(df, filters):
    """Apply selected filters to the dataframe."""
    filtered_df = df.copy()
    
    # Date filter
    if len(filters['date_range']) == 2:
        start_date, end_date = filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['InvoiceDate'].dt.date >= start_date) &
            (filtered_df['InvoiceDate'].dt.date <= end_date)
        ]
    
    # Country filter
    if 'All' not in filters['countries'] and filters['countries']:
        filtered_df = filtered_df[filtered_df['Country'].isin(filters['countries'])]
    
    # Customer type filter
    if filters['customer_type'] != 'All':
        filtered_df = filtered_df[filtered_df['CustomerType'] == filters['customer_type']]
    
    # Transaction type filter
    if filters['transaction_type'] != 'All':
        filtered_df = filtered_df[filtered_df['TransactionType'] == filters['transaction_type']]
    
    # Revenue range filter
    min_rev, max_rev = filters['revenue_range']
    filtered_df = filtered_df[
        (filtered_df['Revenue'] >= min_rev) &
        (filtered_df['Revenue'] <= max_rev)
    ]
    
    return filtered_df

def create_monthly_revenue_chart(df):
    """Create monthly revenue trend chart."""
    monthly_data = df.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()
    monthly_data['Date'] = pd.to_datetime(monthly_data[['Year', 'Month']].assign(day=1))
    monthly_data = monthly_data.sort_values('Date')
    
    fig = px.line(
        monthly_data, 
        x='Date', 
        y='Revenue',
        title='📈 Monthly Revenue Trend',
        labels={'Revenue': 'Revenue (£)', 'Date': 'Date'},
        markers=True
    )
    
    fig.update_traces(line_color='#1f77b4', line_width=3, marker_size=8)
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=18,
        title_x=0.5
    )
    
    return fig

def create_top_products_chart(df):
    """Create top products chart."""
    # Filter positive revenues only for top products
    sales_df = df[df['Revenue'] > 0]
    top_products = sales_df.groupby(['StockCode', 'Description'])['Revenue'].sum().sort_values(ascending=True).tail(10)
    
    # Clean product names for display
    product_names = [desc[:40] + '...' if len(desc) > 40 else desc 
                    for desc in top_products.index.get_level_values('Description')]
    
    fig = px.bar(
        x=top_products.values,
        y=product_names,
        orientation='h',
        title='🏆 Top 10 Products by Revenue',
        labels={'x': 'Revenue (£)', 'y': 'Product'},
        color=top_products.values,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=18,
        title_x=0.5
    )
    
    return fig

def create_country_revenue_chart(df):
    """Create revenue by country chart."""
    country_revenue = df.groupby('Country')['Revenue'].sum().sort_values(ascending=True).tail(10)
    
    fig = px.bar(
        x=country_revenue.values,
        y=country_revenue.index,
        orientation='h',
        title='🌍 Top 10 Countries by Revenue',
        labels={'x': 'Revenue (£)', 'y': 'Country'},
        color=country_revenue.values,
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=18,
        title_x=0.5
    )
    
    return fig

def create_revenue_distribution_chart(df):
    """Create revenue distribution histogram."""
    # Filter out extreme outliers for better visualization
    q99 = df['Revenue'].quantile(0.99)
    q1 = df['Revenue'].quantile(0.01)
    filtered_revenue = df[(df['Revenue'] >= q1) & (df['Revenue'] <= q99)]['Revenue']
    
    fig = px.histogram(
        x=filtered_revenue,
        nbins=50,
        title='💰 Revenue Distribution',
        labels={'x': 'Revenue (£)', 'y': 'Frequency'},
        color_discrete_sequence=['#ff7f0e']
    )
    
    fig.add_vline(x=filtered_revenue.mean(), line_dash="dash", line_color="red", 
                  annotation_text=f"Mean: £{filtered_revenue.mean():.0f}")
    fig.add_vline(x=filtered_revenue.median(), line_dash="dash", line_color="green",
                  annotation_text=f"Median: £{filtered_revenue.median():.0f}")
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=18,
        title_x=0.5
    )
    
    return fig

def create_scatter_plot(df):
    """Create quantity vs revenue scatter plot."""
    # Sample data for better performance
    sample_df = df.sample(min(2000, len(df))) if len(df) > 2000 else df
    
    fig = px.scatter(
        sample_df,
        x='Quantity',
        y='UnitPrice',
        size='Revenue',
        color='TransactionType',
        title='📦 Quantity vs Unit Price (bubble size = Revenue)',
        labels={'Quantity': 'Quantity', 'UnitPrice': 'Unit Price (£)'},
        hover_data=['Revenue', 'Description']
    )
    
    fig.update_layout(
        height=400,
        title_font_size=18,
        title_x=0.5
    )
    
    return fig

def create_customer_analysis_chart(df):
    """Create customer analysis chart."""
    # Customer segments analysis
    customer_data = df[df['CustomerID'].notnull()].groupby('CustomerID')['Revenue'].sum()
    
    # Create segments
    segments = pd.cut(customer_data, 
                     bins=[-np.inf, 0, 100, 500, 1000, np.inf], 
                     labels=['Negative', 'Low (£0-100)', 'Medium (£100-500)', 'High (£500-1000)', 'VIP (£1000+)'])
    
    segment_counts = segments.value_counts()
    
    fig = px.pie(
        values=segment_counts.values,
        names=segment_counts.index,
        title='👥 Customer Revenue Segments',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        height=400,
        title_font_size=18,
        title_x=0.5
    )
    
    return fig

def display_insights(df):
    """Display key business insights."""
    st.markdown("## 💡 Key Business Insights")
    
    # Calculate insights
    total_revenue = df['Revenue'].sum()
    uk_revenue = df[df['Country'] == 'United Kingdom']['Revenue'].sum()
    uk_percentage = (uk_revenue / total_revenue * 100) if total_revenue > 0 else 0
    
    avg_order_value = df.groupby('InvoiceNo')['Revenue'].sum().mean()
    
    cancellation_rate = (df['IsCancellation'].sum() / len(df) * 100) if len(df) > 0 else 0
    
    guest_purchases = (df['CustomerID'].isnull().sum() / len(df) * 100) if len(df) > 0 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
            <h4>🏆 Market Dominance</h4>
            <p>UK accounts for <strong>{uk_percentage:.1f}%</strong> of total revenue (£{uk_revenue:,.0f})</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="insight-box">
            <h4>💰 Order Value</h4>
            <p>Average order value is <strong>£{avg_order_value:.2f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box">
            <h4>👥 Customer Behavior</h4>
            <p><strong>{guest_purchases:.1f}%</strong> of purchases are from guest users</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="insight-box">
            <h4>↩️ Return Rate</h4>
            <p><strong>{cancellation_rate:.1f}%</strong> of transactions are cancellations</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main dashboard application."""
    # Header
    st.markdown('<h1 class="main-header">📊 Online Retail Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; color: #666;">
        <p>CodeAlpha Data Analytics Internship - Interactive Business Intelligence Dashboard</p>
        <p>🔍 Explore sales trends, customer behavior, and product performance with interactive filters</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
        st.success(f"✅ Data loaded successfully! {len(df):,} transactions from {df['InvoiceDate'].dt.date.min()} to {df['InvoiceDate'].dt.date.max()}")
    
    # Create filters
    filters = create_filters(df)
    
    # Apply filters
    filtered_df = apply_filters(df, filters)
    
    if len(filtered_df) == 0:
        st.warning("⚠️ No data matches the selected filters. Please adjust your filter criteria.")
        return
    
    st.markdown(f"**Showing {len(filtered_df):,} transactions** (filtered from {len(df):,} total)")
    
    # KPI Cards
    st.markdown("## 📊 Key Performance Indicators")
    create_kpi_cards(filtered_df)
    
    # Main visualizations
    st.markdown("## 📈 Revenue Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_monthly_revenue_chart(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_revenue_distribution_chart(filtered_df), use_container_width=True)
    
    # Product and Geographic Analysis
    st.markdown("## 🛍️ Product & Geographic Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_top_products_chart(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_country_revenue_chart(filtered_df), use_container_width=True)
    
    # Advanced Analytics
    st.markdown("## 🔬 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_scatter_plot(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_customer_analysis_chart(filtered_df), use_container_width=True)
    
    # Business Insights
    display_insights(filtered_df)
    
    # Data export section
    st.markdown("## 📥 Data Export")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Download Filtered Data (CSV)"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"online_retail_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 View Data Sample"):
            st.dataframe(filtered_df.head(100))
    
    with col3:
        st.metric("Data Quality", f"{(1 - filtered_df.isnull().sum().sum() / (len(filtered_df) * len(filtered_df.columns))):.1%}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🎯 <strong>CodeAlpha Data Analytics Internship Project</strong></p>
        <p>Built with Streamlit • Data from Online Retail Dataset • Interactive Analytics Dashboard</p>
        <p>Tasks Completed: ✅ Web Scraping • ✅ EDA • ✅ Interactive Visualization</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()