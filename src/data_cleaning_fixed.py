"""
Data Cleaning Module for UCI Online Retail Dataset
CodeAlpha Data Analytics Internship Project

This module processes the official UCI Online Retail dataset (~541,909 records)
and creates a cleaned dataset for analysis.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import logging

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def find_dataset_path():
    """Find the UCI dataset path based on current working directory."""
    possible_paths = [
        'data/raw/Online Retail.xlsx',  # Running from root
        '../data/raw/Online Retail.xlsx'  # Running from src/
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    raise FileNotFoundError(
        "UCI Online Retail dataset not found. Please ensure it's at:\n"
        "- data/raw/Online Retail.xlsx (if running from root) OR\n"
        "- ../data/raw/Online Retail.xlsx (if running from src/)"
    )

def find_output_path():
    """Find the output path based on current working directory."""
    if os.path.exists('data/cleaned') or os.path.exists('data'):
        return 'data/cleaned/online_retail_cleaned.csv'
    else:
        return '../data/cleaned/online_retail_cleaned.csv'

def load_uci_dataset(file_path):
    """Load the UCI Online Retail dataset from Excel file."""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Loading UCI dataset from: {file_path}")
    
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)
        logger.info(f"Successfully loaded {len(df):,} records")
        logger.info(f"Columns: {list(df.columns)}")
        
        # Basic validation
        expected_columns = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 
                          'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
        
        missing_cols = set(expected_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing expected columns: {missing_cols}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        raise

def clean_dataset(df):
    """Comprehensive cleaning of the UCI Online Retail dataset."""
    logger = logging.getLogger(__name__)
    
    original_count = len(df)
    logger.info(f"Starting cleaning process with {original_count:,} records")
    
    # Create a copy for cleaning
    df_clean = df.copy()
    
    # 1. Handle missing values in CustomerID (convert to string to handle NaN)
    logger.info("Step 1: Handling missing CustomerID values")
    missing_customers_before = df_clean['CustomerID'].isnull().sum()
    logger.info(f"Missing CustomerID values: {missing_customers_before:,}")
    
    # For missing CustomerID, we'll keep them but mark as 'Unknown'
    df_clean['CustomerID'] = df_clean['CustomerID'].fillna('Unknown')
    
    # 2. Remove records with missing Description
    logger.info("Step 2: Removing records with missing Description")
    missing_desc_before = df_clean['Description'].isnull().sum()
    logger.info(f"Missing Description values: {missing_desc_before:,}")
    df_clean = df_clean.dropna(subset=['Description'])
    
    # 3. Handle invalid quantities (negative quantities indicate returns/cancellations)
    logger.info("Step 3: Processing quantity values")
    negative_qty = (df_clean['Quantity'] < 0).sum()
    zero_qty = (df_clean['Quantity'] == 0).sum()
    logger.info(f"Negative quantities (returns): {negative_qty:,}")
    logger.info(f"Zero quantities: {zero_qty:,}")
    
    # Remove zero quantities, keep negative (as they represent returns)
    df_clean = df_clean[df_clean['Quantity'] != 0]
    
    # 4. Handle invalid unit prices
    logger.info("Step 4: Processing unit prices")
    negative_price = (df_clean['UnitPrice'] < 0).sum()
    zero_price = (df_clean['UnitPrice'] == 0).sum()
    logger.info(f"Negative prices: {negative_price:,}")
    logger.info(f"Zero prices: {zero_price:,}")
    
    # Remove records with negative or zero unit prices
    df_clean = df_clean[df_clean['UnitPrice'] > 0]
    
    # 5. Parse and validate dates
    logger.info("Step 5: Processing dates")
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    
    # Check date range
    date_min = df_clean['InvoiceDate'].min()
    date_max = df_clean['InvoiceDate'].max()
    logger.info(f"Date range: {date_min.date()} to {date_max.date()}")
    
    # 6. Create calculated fields
    logger.info("Step 6: Creating calculated fields")
    df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['UnitPrice']
    
    # 7. Remove duplicates
    logger.info("Step 7: Removing duplicates")
    duplicates_before = df_clean.duplicated().sum()
    logger.info(f"Duplicate records: {duplicates_before:,}")
    df_clean = df_clean.drop_duplicates()
    
    # 8. Clean text fields
    logger.info("Step 8: Cleaning text fields")
    df_clean['Description'] = df_clean['Description'].str.strip().str.upper()
    df_clean['Country'] = df_clean['Country'].str.strip()
    
    # 9. Add data quality indicators
    df_clean['IsReturn'] = df_clean['Quantity'] < 0
    df_clean['IsCancellation'] = df_clean['InvoiceNo'].str.startswith('C', na=False)
    
    # Final statistics
    final_count = len(df_clean)
    removed_count = original_count - final_count
    retention_rate = (final_count / original_count) * 100
    
    logger.info("="*60)
    logger.info("CLEANING SUMMARY")
    logger.info("="*60)
    logger.info(f"Original records: {original_count:,}")
    logger.info(f"Final records: {final_count:,}")
    logger.info(f"Records removed: {removed_count:,}")
    logger.info(f"Retention rate: {retention_rate:.2f}%")
    logger.info(f"Unique customers: {df_clean['CustomerID'].nunique():,}")
    logger.info(f"Unique products: {df_clean['StockCode'].nunique():,}")
    logger.info(f"Unique invoices: {df_clean['InvoiceNo'].nunique():,}")
    logger.info(f"Countries: {df_clean['Country'].nunique()}")
    logger.info(f"Date range: {date_min.date()} to {date_max.date()}")
    
    return df_clean

def save_cleaned_dataset(df, output_path):
    """Save the cleaned dataset to CSV."""
    logger = logging.getLogger(__name__)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Cleaned dataset saved to: {output_path}")
    
    # Verify the saved file
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        logger.info(f"File size: {file_size/1024/1024:.2f} MB")
        return True
    else:
        logger.error("Failed to save cleaned dataset")
        return False

def main():
    """Main function to run the UCI data cleaning process."""
    # Setup logging
    logger = setup_logging()
    
    print("UCI Online Retail Dataset - Data Cleaning Pipeline")
    print("CodeAlpha Data Analytics Internship Project")
    print("="*60)
    
    try:
        # Find dataset path
        dataset_path = find_dataset_path()
        output_path = find_output_path()
        
        # Load dataset
        df_raw = load_uci_dataset(dataset_path)
        
        # Clean dataset
        df_cleaned = clean_dataset(df_raw)
        
        # Save cleaned dataset
        success = save_cleaned_dataset(df_cleaned, output_path)
        
        if success:
            print(f"\n✅ UCI dataset cleaning completed successfully!")
            print(f"📄 Input: {dataset_path}")
            print(f"📄 Output: {output_path}")
            print(f"📊 Final records: {len(df_cleaned):,}")
            print(f"📊 Features: {len(df_cleaned.columns)}")
            return True
        else:
            print(f"\n❌ Failed to save cleaned dataset")
            return False
            
    except FileNotFoundError as e:
        print(f"\n❌ Dataset not found:")
        print(f"   {e}")
        print(f"\n📋 Please download the official UCI Online Retail dataset:")
        print(f"   Source: https://archive.ics.uci.edu/dataset/352/online+retail")
        print(f"   Save as: data/raw/Online Retail.xlsx")
        return False
        
    except Exception as e:
        print(f"\n❌ Error in UCI data cleaning: {e}")
        logger.error(f"Cleaning failed: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)