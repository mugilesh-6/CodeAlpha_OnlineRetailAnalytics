"""
Optimized Data Cleaning Module for UCI Online Retail Dataset
CodeAlpha Data Analytics Internship Project

This module quickly processes the official UCI Online Retail dataset.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def main():
    """Main function to run the UCI data cleaning process."""
    print("UCI Online Retail Dataset - Data Cleaning Pipeline (Optimized)")
    print("CodeAlpha Data Analytics Internship Project")
    print("="*60)
    
    # Find dataset path
    if os.path.exists('data/raw/Online Retail.xlsx'):
        dataset_path = 'data/raw/Online Retail.xlsx'
        output_path = 'data/cleaned/online_retail_cleaned.csv'
    elif os.path.exists('../data/raw/Online Retail.xlsx'):
        dataset_path = '../data/raw/Online Retail.xlsx'
        output_path = '../data/cleaned/online_retail_cleaned.csv'
    else:
        print("❌ UCI dataset not found")
        return False
    
    try:
        print(f"Loading dataset from: {dataset_path}")
        
        # Load Excel file with optimizations
        df = pd.read_excel(dataset_path, engine='openpyxl')
        
        original_count = len(df)
        print(f"Original records: {original_count:,}")
        print(f"Columns: {list(df.columns)}")
        
        # Quick data cleaning
        print("Performing data cleaning...")
        
        # Remove records with missing Description
        df = df.dropna(subset=['Description'])
        
        # Remove zero quantities
        df = df[df['Quantity'] != 0]
        
        # Remove non-positive unit prices
        df = df[df['UnitPrice'] > 0]
        
        # Handle missing CustomerID
        df['CustomerID'] = df['CustomerID'].fillna('Unknown')
        
        # Parse dates
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        
        # Create calculated fields
        df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
        
        # Clean text fields
        df['Description'] = df['Description'].str.strip().str.upper()
        df['Country'] = df['Country'].str.strip()
        
        # Add indicators
        df['IsReturn'] = df['Quantity'] < 0
        df['IsCancellation'] = df['InvoiceNo'].astype(str).str.startswith('C')
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        final_count = len(df)
        retention_rate = (final_count / original_count) * 100
        
        # Create output directory
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save cleaned dataset
        print(f"Saving cleaned dataset...")
        df.to_csv(output_path, index=False)
        
        print("="*60)
        print("CLEANING SUMMARY")
        print("="*60)
        print(f"Original records: {original_count:,}")
        print(f"Final records: {final_count:,}")
        print(f"Records removed: {(original_count - final_count):,}")
        print(f"Retention rate: {retention_rate:.2f}%")
        print(f"Unique customers: {df['CustomerID'].nunique():,}")
        print(f"Unique products: {df['StockCode'].nunique():,}")
        print(f"Unique invoices: {df['InvoiceNo'].nunique():,}")
        print(f"Countries: {df['Country'].nunique()}")
        
        date_min = df['InvoiceDate'].min()
        date_max = df['InvoiceDate'].max()
        print(f"Date range: {date_min.date()} to {date_max.date()}")
        
        print(f"\nUCI dataset cleaning completed successfully!")
        print(f"Output: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error in UCI data cleaning: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)