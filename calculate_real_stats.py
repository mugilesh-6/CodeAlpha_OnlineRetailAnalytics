"""
Calculate Real Statistics from UCI Dataset
This script calculates the actual statistics to replace hardcoded synthetic values.
"""

import pandas as pd
import numpy as np

def calculate_uci_statistics():
    """Calculate real statistics from the cleaned UCI dataset."""
    
    # Load the cleaned UCI dataset
    df = pd.read_csv('data/cleaned/online_retail_cleaned.csv', parse_dates=['InvoiceDate'])
    
    print("REAL UCI DATASET STATISTICS")
    print("="*50)
    
    # Basic counts
    total_records = len(df)
    unique_customers = df['CustomerID'].nunique()
    unique_orders = df['InvoiceNo'].nunique()
    unique_products = df['StockCode'].nunique()
    unique_countries = df['Country'].nunique()
    
    print(f"📊 Total Records: {total_records:,}")
    print(f"👥 Unique Customers: {unique_customers:,}")
    print(f"📋 Unique Orders: {unique_orders:,}")
    print(f"📦 Unique Products: {unique_products:,}")
    print(f"🌍 Countries: {unique_countries}")
    
    # Financial metrics
    total_revenue = df['TotalAmount'].sum()
    average_order_value = df.groupby('InvoiceNo')['TotalAmount'].sum().mean()
    
    print(f"\n💰 FINANCIAL METRICS:")
    print(f"📈 Total Revenue: £{total_revenue:,.2f}")
    print(f"📊 Average Order Value: £{average_order_value:,.2f}")
    
    # Date range
    date_min = df['InvoiceDate'].min()
    date_max = df['InvoiceDate'].max()
    days_span = (date_max - date_min).days
    
    print(f"\n📅 DATE RANGE:")
    print(f"Start: {date_min.date()}")
    print(f"End: {date_max.date()}")
    print(f"Days: {days_span}")
    
    # Geographic analysis
    revenue_by_country = df.groupby('Country')['TotalAmount'].sum().sort_values(ascending=False)
    uk_revenue = revenue_by_country['United Kingdom'] if 'United Kingdom' in revenue_by_country else 0
    uk_percentage = (uk_revenue / total_revenue) * 100
    
    print(f"\n🌍 GEOGRAPHIC ANALYSIS:")
    print(f"UK Revenue: £{uk_revenue:,.2f}")
    print(f"UK Percentage: {uk_percentage:.1f}%")
    
    # Customer analysis
    customer_orders = df[df['CustomerID'] != 'Unknown'].groupby('CustomerID')['InvoiceNo'].nunique()
    repeat_customers = (customer_orders > 1).sum()
    total_known_customers = len(customer_orders)
    retention_rate = (repeat_customers / total_known_customers) * 100
    
    print(f"\n👥 CUSTOMER ANALYSIS:")
    print(f"Known Customers: {total_known_customers:,}")
    print(f"Repeat Customers: {repeat_customers:,}")
    print(f"Retention Rate: {retention_rate:.1f}%")
    
    # Return actual values for replacement
    return {
        'total_records': f"{total_records:,}",
        'unique_customers': f"{unique_customers:,}",
        'unique_orders': f"{unique_orders:,}",
        'unique_products': f"{unique_products:,}",
        'total_revenue': f"£{total_revenue:,.0f}",
        'uk_percentage': f"{uk_percentage:.0f}%",
        'retention_rate': f"{retention_rate:.0f}%",
        'average_order_value': f"£{average_order_value:,.0f}",
        'date_range': f"{date_min.strftime('%B %Y')} to {date_max.strftime('%B %Y')}"
    }

if __name__ == "__main__":
    stats = calculate_uci_statistics()
    
    print(f"\n🔄 REPLACEMENT VALUES:")
    print("="*50)
    print("Replace synthetic values with these real values:")
    print(f"• 15,000 → {stats['total_records']}")
    print(f"• 1,500 customers → {stats['unique_customers']} customers") 
    print(f"• 750 orders → {stats['unique_orders']} orders")
    print(f"• £1,543,309 → {stats['total_revenue']}")
    print(f"• 78% (UK) → {stats['uk_percentage']} (UK)")
    print(f"• 40% retention → {stats['retention_rate']} retention")