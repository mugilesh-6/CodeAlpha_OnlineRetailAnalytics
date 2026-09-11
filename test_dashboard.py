"""
Test script to verify dashboard components work correctly
"""

import pandas as pd
import os
import sys

def test_data_loading():
    """Test if data can be loaded successfully."""
    try:
        data_path = 'data/cleaned/online_retail_cleaned.csv'
        df = pd.read_csv(data_path, parse_dates=['InvoiceDate'])
        print(f"✅ Data loaded successfully: {df.shape}")
        print(f"   Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
        print(f"   Total revenue: £{df['TotalAmount'].sum():,.2f}")
        return True
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_basic_calculations():
    """Test basic dashboard calculations."""
    try:
        df = pd.read_csv('data/cleaned/online_retail_cleaned.csv', parse_dates=['InvoiceDate'])
        
        # Test KPI calculations
        total_revenue = df['TotalAmount'].sum()
        total_orders = df['InvoiceNo'].nunique()
        total_customers = df['CustomerID'].nunique()
        avg_order_value = df.groupby('InvoiceNo')['TotalAmount'].sum().mean()
        
        print(f"✅ KPI calculations work:")
        print(f"   Total Revenue: £{total_revenue:,.2f}")
        print(f"   Total Orders: {total_orders:,}")
        print(f"   Total Customers: {total_customers:,}")
        print(f"   Avg Order Value: £{avg_order_value:.2f}")
        
        return True
    except Exception as e:
        print(f"❌ Error in calculations: {e}")
        return False

def main():
    """Run all tests."""
    print("DASHBOARD TEST SUITE")
    print("=" * 30)
    
    # Change to project directory
    if not os.path.exists('data/cleaned/online_retail_cleaned.csv'):
        print("❌ Please run this from the project root directory")
        return
    
    # Run tests
    tests = [
        test_data_loading,
        test_basic_calculations
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append(False)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"TEST SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Dashboard is ready to run.")
        print("📊 To start the dashboard, run:")
        print("   streamlit run dashboard/app.py")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()