"""
UCI Online Retail Dataset Download Utility
CodeAlpha Data Analytics Internship Project

This module handles downloading the official UCI Online Retail dataset.
The dataset contains 541,909 transaction records from 01/12/2010 to 09/12/2011.
"""

import requests
import os
import pandas as pd
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_uci_online_retail():
    """
    Download the official UCI Online Retail dataset.
    
    Dataset Information:
    - Source: UCI Machine Learning Repository
    - URL: https://archive.ics.uci.edu/dataset/352/online+retail
    - Records: 541,909 transactions
    - Period: 01/12/2010 to 09/12/2011
    - Format: Excel (.xlsx)
    """
    
    # UCI dataset direct download URL
    dataset_url = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
    
    # Alternative direct Excel file URL (if available)
    excel_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
    
    raw_data_dir = Path("data/raw")
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = raw_data_dir / "Online Retail.xlsx"
    
    logger.info("Attempting to download UCI Online Retail dataset...")
    
    # Try direct Excel file download first
    try:
        logger.info(f"Downloading from: {excel_url}")
        response = requests.get(excel_url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"✅ Dataset downloaded successfully: {output_path}")
        
        # Verify the file
        try:
            df = pd.read_excel(output_path)
            logger.info(f"✅ Dataset verified: {len(df):,} records, {len(df.columns)} columns")
            logger.info(f"Columns: {list(df.columns)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error verifying downloaded file: {e}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Download failed: {e}")
        logger.info("Please download manually from: https://archive.ics.uci.edu/dataset/352/online+retail")
        return False

def verify_uci_dataset():
    """
    Verify that the UCI dataset exists and has expected structure.
    
    Returns:
        bool: True if dataset is valid, False otherwise
    """
    
    dataset_path = Path("data/raw/Online Retail.xlsx")
    
    if not dataset_path.exists():
        logger.error(f"❌ UCI dataset not found: {dataset_path}")
        return False
    
    try:
        df = pd.read_excel(dataset_path)
        
        expected_columns = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
        
        # Check columns
        missing_columns = set(expected_columns) - set(df.columns)
        if missing_columns:
            logger.error(f"❌ Missing expected columns: {missing_columns}")
            return False
        
        # Check record count (should be around 541,909)
        if len(df) < 500000:
            logger.warning(f"⚠️ Dataset has {len(df):,} records. Expected ~541,909")
        
        logger.info(f"✅ Dataset verified: {len(df):,} records")
        logger.info(f"✅ Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
        logger.info(f"✅ Countries: {df['Country'].nunique()}")
        logger.info(f"✅ Products: {df['StockCode'].nunique()}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error verifying dataset: {e}")
        return False

def create_manual_download_instructions():
    """
    Create instructions for manual dataset download if automatic download fails.
    """
    
    instructions = """
# Manual UCI Dataset Download Instructions

If the automatic download fails, please follow these steps:

## Step 1: Visit UCI Repository
Go to: https://archive.ics.uci.edu/dataset/352/online+retail

## Step 2: Download Dataset
1. Click on "Download" button
2. Download the "Online Retail.xlsx" file
3. The file should be approximately 18-25 MB

## Step 3: Place in Project
1. Save the file as: `data/raw/Online Retail.xlsx`
2. Ensure the filename matches exactly (including the space)
3. Do not rename or modify the file

## Step 4: Verify Dataset
Run the verification:
```bash
python src/download_dataset.py
```

## Expected Dataset Properties
- Records: ~541,909 transactions  
- Period: 01/12/2010 to 09/12/2011
- Columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
- File size: ~18-25 MB
- Format: Excel (.xlsx)

## Alternative Sources
If UCI is unavailable, the dataset is also available on:
- Kaggle: https://www.kaggle.com/datasets/hellbuoy/online-retail-customer-clustering
- GitHub repositories (search for "UCI Online Retail")

**IMPORTANT:** Ensure you download the ORIGINAL UCI dataset, not a pre-processed or cleaned version.
"""
    
    instructions_path = Path("data/MANUAL_DOWNLOAD_INSTRUCTIONS.md")
    with open(instructions_path, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    logger.info(f"📋 Manual download instructions created: {instructions_path}")

def main():
    """
    Main function to handle UCI dataset acquisition.
    """
    print("UCI Online Retail Dataset Download Utility")
    print("=" * 50)
    
    # Check if dataset already exists
    if verify_uci_dataset():
        print("✅ UCI dataset is already available and verified!")
        return True
    
    # Try automatic download
    success = download_uci_online_retail()
    
    if not success:
        print("\n❌ Automatic download failed")
        print("📋 Creating manual download instructions...")
        create_manual_download_instructions()
        print("\n🔍 Please follow the manual download instructions in:")
        print("   data/MANUAL_DOWNLOAD_INSTRUCTIONS.md")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n⚠️ Dataset download incomplete. Manual download required.")
        exit(1)
    else:
        print("\n🎉 UCI dataset ready for analysis!")
        exit(0)