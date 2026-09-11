"""
Data Cleaning Module for UCI Online Retail Dataset
CodeAlpha Data Analytics Internship Project

This module performs comprehensive data cleaning on the official UCI Online Retail dataset,
containing 541,909 transaction records from 01/12/2010 to 09/12/2011.
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime
import os
from typing import Tuple, Dict, Any

class UCIRetailDataCleaner:
    """
    A comprehensive data cleaning class for the official UCI Online Retail dataset.
    
    Dataset Information:
    - Source: UCI Machine Learning Repository
    - Original records: ~541,909 transactions
    - Period: 01/12/2010 to 09/12/2011
    - Columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
    """
    
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize the UCI data cleaner.
        
        Args:
            log_level: Logging level for the cleaner
        """
        # Setup logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize cleaning statistics
        self.cleaning_stats = {
            'original_shape': None,
            'final_shape': None,
            'records_removed': 0,
            'missing_values_handled': 0,
            'duplicates_removed': 0,
            'invalid_transactions_removed': 0,
            'cancellation_records': 0,
            'cleaning_timestamp': None
        }
    
    def load_uci_dataset(self, file_path: str = None) -> pd.DataFrame:
        """
        Load the official UCI Online Retail dataset.
        Auto-detects path based on current working directory.
        """
        if file_path is None:
            # Auto-detect path based on current directory
            if os.path.exists('data/raw/Online Retail.xlsx'):
                file_path = 'data/raw/Online Retail.xlsx'
            elif os.path.exists('../data/raw/Online Retail.xlsx'):
                file_path = '../data/raw/Online Retail.xlsx'
            else:
                raise FileNotFoundError("UCI Online Retail dataset not found. Please ensure it's at data/raw/Online Retail.xlsx")
        
        Args:
            file_path: Path to the UCI Excel file
            
        Returns:
            DataFrame containing the raw UCI data
        """
        try:
            self.logger.info(f"Loading UCI Online Retail dataset from: {file_path}")
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"UCI dataset not found: {file_path}")
            
            # Load the Excel file
            df = pd.read_excel(file_path, engine='openpyxl')
            self.cleaning_stats['original_shape'] = df.shape
            
            self.logger.info(f"✅ UCI dataset loaded successfully")
            self.logger.info(f"   Shape: {df.shape}")
            self.logger.info(f"   Columns: {list(df.columns)}")
            self.logger.info(f"   Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
            
            # Verify expected columns
            expected_columns = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 
                              'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
            
            missing_columns = set(expected_columns) - set(df.columns)
            if missing_columns:
                raise ValueError(f"Missing expected columns: {missing_columns}")
            
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Error loading UCI dataset: {e}")
            self.logger.info("📋 Please ensure you have downloaded the official UCI dataset")
            self.logger.info("   Instructions: data/MANUAL_DOWNLOAD_INSTRUCTIONS.md")
            raise
    
    def assess_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform initial data quality assessment on UCI dataset.
        
        Args:
            df: DataFrame to assess
            
        Returns:
            Dictionary containing data quality metrics
        """
        self.logger.info("Performing data quality assessment on UCI dataset...")
        
        quality_report = {
            'shape': df.shape,
            'columns': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'missing_percentages': (df.isnull().sum() / len(df) * 100).to_dict(),
            'duplicate_rows': df.duplicated().sum(),
            'unique_invoices': df['InvoiceNo'].nunique(),
            'unique_customers': df['CustomerID'].nunique(),
            'unique_products': df['StockCode'].nunique(),
            'unique_countries': df['Country'].nunique(),
            'date_range': {
                'start': df['InvoiceDate'].min(),
                'end': df['InvoiceDate'].max(),
                'days': (df['InvoiceDate'].max() - df['InvoiceDate'].min()).days
            }
        }
        
        # Check for cancellation invoices (InvoiceNo starting with 'C')
        cancellations = df['InvoiceNo'].astype(str).str.startswith('C').sum()
        quality_report['cancellation_invoices'] = cancellations
        
        # Check for negative quantities
        negative_quantities = (df['Quantity'] < 0).sum()
        quality_report['negative_quantities'] = negative_quantities
        
        # Check for zero/negative prices
        invalid_prices = (df['UnitPrice'] <= 0).sum()
        quality_report['invalid_prices'] = invalid_prices
        
        # Log key findings
        self.logger.info(f"📊 UCI Dataset Quality Assessment:")
        self.logger.info(f"   Records: {quality_report['shape'][0]:,}")
        self.logger.info(f"   Columns: {quality_report['shape'][1]}")
        self.logger.info(f"   Missing CustomerIDs: {quality_report['missing_values']['CustomerID']:,}")
        self.logger.info(f"   Duplicate rows: {quality_report['duplicate_rows']:,}")
        self.logger.info(f"   Cancellation invoices: {cancellations:,}")
        self.logger.info(f"   Unique customers: {quality_report['unique_customers']:,}")
        self.logger.info(f"   Unique products: {quality_report['unique_products']:,}")
        self.logger.info(f"   Countries: {quality_report['unique_countries']}")
        
        return quality_report
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the UCI dataset.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            DataFrame with missing values handled
        """
        self.logger.info("Handling missing values in UCI dataset...")
        
        df_clean = df.copy()
        original_missing = df_clean.isnull().sum().sum()
        
        # Handle missing CustomerID - these represent guest purchases
        missing_customers = df_clean['CustomerID'].isnull().sum()
        if missing_customers > 0:
            self.logger.info(f"   Found {missing_customers:,} records with missing CustomerID (guest purchases)")
            # Keep these records as they represent valid guest transactions
        
        # Handle missing Description
        missing_desc = df_clean['Description'].isnull().sum()
        if missing_desc > 0:
            self.logger.info(f"   Found {missing_desc:,} records with missing Description")
            # Remove records with missing descriptions as they cannot be analyzed
            df_clean = df_clean[df_clean['Description'].notnull()]
            self.logger.info(f"   Removed {missing_desc:,} records with missing descriptions")
            self.cleaning_stats['records_removed'] += missing_desc
        
        # Remove records with missing critical values
        critical_columns = ['InvoiceNo', 'StockCode', 'Quantity', 'InvoiceDate', 'UnitPrice']
        before_critical = len(df_clean)
        df_clean = df_clean.dropna(subset=critical_columns)
        after_critical = len(df_clean)
        
        if before_critical != after_critical:
            removed = before_critical - after_critical
            self.logger.info(f"   Removed {removed:,} records with missing critical values")
            self.cleaning_stats['records_removed'] += removed
        
        final_missing = df_clean.isnull().sum().sum()
        self.cleaning_stats['missing_values_handled'] = original_missing - final_missing
        
        return df_clean
    
    def handle_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle duplicate records in the UCI dataset.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            DataFrame with duplicates removed
        """
        self.logger.info("Handling duplicate records...")
        
        before_duplicates = len(df)
        duplicates = df.duplicated().sum()
        
        if duplicates > 0:
            self.logger.info(f"   Found {duplicates:,} exact duplicate records")
            df_clean = df.drop_duplicates()
            self.cleaning_stats['duplicates_removed'] = duplicates
        else:
            df_clean = df.copy()
            self.logger.info("   No exact duplicates found")
        
        after_duplicates = len(df_clean)
        removed = before_duplicates - after_duplicates
        if removed > 0:
            self.logger.info(f"   Removed {removed:,} duplicate records")
        
        return df_clean
    
    def handle_cancellations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify and handle cancellation transactions in UCI dataset.
        
        Args:
            df: DataFrame to process
            
        Returns:
            DataFrame with cancellation information added
        """
        self.logger.info("Processing cancellation transactions...")
        
        df_clean = df.copy()
        
        # Identify cancellations (InvoiceNo starting with 'C')
        is_cancellation = df_clean['InvoiceNo'].astype(str).str.startswith('C')
        num_cancellations = is_cancellation.sum()
        
        # Add cancellation flag
        df_clean['IsCancellation'] = is_cancellation
        df_clean['TransactionType'] = df_clean['IsCancellation'].map({True: 'Cancellation', False: 'Sale'})
        
        self.cleaning_stats['cancellation_records'] = num_cancellations
        
        self.logger.info(f"   Identified {num_cancellations:,} cancellation records ({num_cancellations/len(df_clean)*100:.2f}%)")
        
        return df_clean
    
    def handle_invalid_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle invalid transactions and outliers in UCI dataset.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            DataFrame with invalid transactions handled
        """
        self.logger.info("Handling invalid transactions and outliers...")
        
        df_clean = df.copy()
        original_len = len(df_clean)
        
        # Handle zero or negative unit prices
        invalid_prices = (df_clean['UnitPrice'] <= 0).sum()
        if invalid_prices > 0:
            self.logger.info(f"   Found {invalid_prices:,} records with zero/negative unit prices")
            
            # Keep cancellations even if they have zero prices
            mask_invalid_price = (df_clean['UnitPrice'] <= 0) & (~df_clean['IsCancellation'])
            
            df_clean = df_clean[~mask_invalid_price]
            removed = mask_invalid_price.sum()
            self.logger.info(f"   Removed {removed:,} non-cancellation records with invalid prices")
            self.cleaning_stats['invalid_transactions_removed'] += removed
        
        # Log extreme values but don't automatically remove them
        if 'Quantity' in df_clean.columns:
            q99 = df_clean['Quantity'].quantile(0.99)
            extreme_quantities = (df_clean['Quantity'] > q99 * 10).sum()
            if extreme_quantities > 0:
                self.logger.info(f"   Found {extreme_quantities:,} records with extremely high quantities (potential bulk orders)")
        
        return df_clean
    
    def create_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create derived features for UCI dataset analysis.
        
        Args:
            df: DataFrame to enhance
            
        Returns:
            DataFrame with additional features
        """
        self.logger.info("Creating derived features...")
        
        df_enhanced = df.copy()
        
        # Create Revenue column
        df_enhanced['Revenue'] = df_enhanced['Quantity'] * df_enhanced['UnitPrice']
        self.logger.info("   ✅ Created Revenue column (Quantity × UnitPrice)")
        
        # Convert InvoiceDate to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(df_enhanced['InvoiceDate']):
            df_enhanced['InvoiceDate'] = pd.to_datetime(df_enhanced['InvoiceDate'])
        
        # Extract date components
        df_enhanced['Year'] = df_enhanced['InvoiceDate'].dt.year
        df_enhanced['Month'] = df_enhanced['InvoiceDate'].dt.month
        df_enhanced['DayOfWeek'] = df_enhanced['InvoiceDate'].dt.dayofweek
        df_enhanced['Hour'] = df_enhanced['InvoiceDate'].dt.hour
        df_enhanced['MonthName'] = df_enhanced['InvoiceDate'].dt.month_name()
        df_enhanced['YearMonth'] = df_enhanced['InvoiceDate'].dt.to_period('M')
        self.logger.info("   ✅ Created date-based features")
        
        # Create customer type flag
        df_enhanced['IsGuestPurchase'] = df_enhanced['CustomerID'].isnull()
        df_enhanced['CustomerType'] = df_enhanced['IsGuestPurchase'].map({True: 'Guest', False: 'Registered'})
        self.logger.info("   ✅ Created customer type features")
        
        return df_enhanced
    
    def validate_cleaned_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate the cleaned UCI dataset.
        
        Args:
            df: Cleaned DataFrame to validate
            
        Returns:
            Dictionary containing validation results
        """
        self.logger.info("Validating cleaned UCI dataset...")
        
        validation_results = {
            'final_shape': df.shape,
            'remaining_missing_values': df.isnull().sum().to_dict(),
            'data_quality_checks': {}
        }
        
        checks = validation_results['data_quality_checks']
        
        # Business metrics
        total_revenue = df['Revenue'].sum()
        unique_customers = df['CustomerID'].nunique()
        unique_products = df['StockCode'].nunique()
        unique_countries = df['Country'].nunique()
        
        checks['business_metrics'] = {
            'total_revenue': float(total_revenue),
            'unique_customers': int(unique_customers),
            'unique_products': int(unique_products),
            'unique_countries': int(unique_countries),
            'date_range_days': (df['InvoiceDate'].max() - df['InvoiceDate'].min()).days
        }
        
        # Data quality metrics
        checks['revenue_stats'] = {
            'min': float(df['Revenue'].min()),
            'max': float(df['Revenue'].max()),
            'mean': float(df['Revenue'].mean()),
            'negative_revenue': int((df['Revenue'] < 0).sum())
        }
        
        self.logger.info(f"✅ Validation completed:")
        self.logger.info(f"   Final records: {validation_results['final_shape'][0]:,}")
        self.logger.info(f"   Total revenue: £{total_revenue:,.2f}")
        self.logger.info(f"   Unique customers: {unique_customers:,}")
        self.logger.info(f"   Unique products: {unique_products:,}")
        self.logger.info(f"   Countries: {unique_countries}")
        
        return validation_results
    
    def clean_uci_dataset(self, input_file: str = None, 
                         output_file: str = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Execute the complete UCI data cleaning pipeline.
        
        Args:
            input_file: Path to the raw UCI Excel file
            output_file: Path to save the cleaned data
            
        Returns:
            Tuple of (cleaned DataFrame, cleaning statistics)
        """
        self.logger.info("🚀 Starting UCI Online Retail data cleaning pipeline...")
        self.cleaning_stats['cleaning_timestamp'] = datetime.now()
        
        try:
            # Step 1: Load UCI dataset
            df = self.load_uci_dataset(input_file)
            
            # Step 2: Initial assessment
            quality_report = self.assess_data_quality(df)
            
            # Step 3: Handle missing values
            df = self.handle_missing_values(df)
            
            # Step 4: Handle duplicates
            df = self.handle_duplicates(df)
            
            # Step 5: Handle cancellations
            df = self.handle_cancellations(df)
            
            # Step 6: Handle invalid transactions
            df = self.handle_invalid_transactions(df)
            
            # Step 7: Create derived features
            df = self.create_derived_features(df)
            
            # Step 8: Final validation
            validation_results = self.validate_cleaned_data(df)
            
            # Update final statistics
            self.cleaning_stats['final_shape'] = df.shape
            total_removed = (self.cleaning_stats['original_shape'][0] - self.cleaning_stats['final_shape'][0])
            self.cleaning_stats['records_removed'] = total_removed
            
            # Save cleaned data
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            df.to_csv(output_file, index=False, encoding='utf-8')
            self.logger.info(f"💾 Cleaned data saved to: {output_file}")
            
            self.print_cleaning_summary()
            
            return df, {
                'cleaning_stats': self.cleaning_stats,
                'quality_report': quality_report,
                'validation_results': validation_results
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error in UCI cleaning pipeline: {e}")
            raise
    
    def print_cleaning_summary(self):
        """Print a summary of the UCI data cleaning process."""
        print("\n" + "="*70)
        print("UCI ONLINE RETAIL DATASET - CLEANING SUMMARY")
        print("="*70)
        print(f"📊 Original records: {self.cleaning_stats['original_shape'][0]:,}")
        print(f"📊 Final records: {self.cleaning_stats['final_shape'][0]:,}")
        print(f"📊 Records removed: {self.cleaning_stats['records_removed']:,}")
        print(f"📊 Cancellation records: {self.cleaning_stats['cancellation_records']:,}")
        print(f"📊 Duplicates removed: {self.cleaning_stats['duplicates_removed']:,}")
        
        if self.cleaning_stats['original_shape'] and self.cleaning_stats['final_shape']:
            retention_rate = (self.cleaning_stats['final_shape'][0] / self.cleaning_stats['original_shape'][0]) * 100
            print(f"📊 Data retention rate: {retention_rate:.2f}%")
        
        print(f"📊 Cleaning completed: {self.cleaning_stats['cleaning_timestamp']}")
        print("="*70)

def main():
    """
    Main function to run the UCI data cleaning process.
    """
    print("UCI Online Retail Dataset - Data Cleaning Pipeline")
    print("CodeAlpha Data Analytics Internship Project")
    print("="*60)
    
    # Initialize cleaner
    cleaner = UCIRetailDataCleaner()
    
    # Check if UCI dataset exists (handle running from different directories)
    if os.path.exists('data/raw/Online Retail.xlsx'):
        uci_file = 'data/raw/Online Retail.xlsx'
    elif os.path.exists('../data/raw/Online Retail.xlsx'):
        uci_file = '../data/raw/Online Retail.xlsx'
    else:
        print(f"❌ UCI dataset not found")
        print("📋 Please download the official UCI Online Retail dataset")
        print("   Expected locations:")
        print("   - data/raw/Online Retail.xlsx (if running from root)")
        print("   - ../data/raw/Online Retail.xlsx (if running from src/)")
        print("   Instructions: data/MANUAL_DOWNLOAD_INSTRUCTIONS.md")
        print("   Source: https://archive.ics.uci.edu/dataset/352/online+retail")
        return False
    
    try:
        # Run cleaning pipeline
        cleaned_df, cleaning_report = cleaner.clean_uci_dataset()
        
        print(f"\n✅ UCI dataset cleaning completed successfully!")
        print(f"📄 Cleaned dataset: data/cleaned/online_retail_cleaned.csv")
        print(f"📊 Records: {len(cleaned_df):,}")
        print(f"📊 Features: {len(cleaned_df.columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in UCI data cleaning: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)