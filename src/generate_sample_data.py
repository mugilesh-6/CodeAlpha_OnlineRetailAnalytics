"""
Generate Sample Online Retail Dataset
CodeAlpha Data Analytics Internship Project

This module generates a realistic sample dataset with the structure of the UCI Online Retail dataset.
This is for demonstration purposes when the original dataset is not available.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

def generate_sample_retail_data(n_records: int = 10000) -> pd.DataFrame:
    """
    Generate a sample online retail dataset with realistic patterns.
    
    Args:
        n_records: Number of records to generate
        
    Returns:
        DataFrame with retail transaction data
    """
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Product catalog
    products = [
        ("85123A", "WHITE HANGING HEART T-LIGHT HOLDER", 2.55),
        ("71053", "WHITE METAL LANTERN", 3.39),
        ("84406B", "CREAM CUPID HEARTS COAT HANGER", 2.75),
        ("84029G", "KNITTED UNION FLAG HOT WATER BOTTLE", 3.39),
        ("84029E", "RED WOOLLY HOTTIE WHITE HEART", 3.39),
        ("22752", "SET 7 BABUSHKA NESTING BOXES", 7.65),
        ("21730", "GLASS STAR FROSTED T-LIGHT HOLDER", 4.25),
        ("22633", "HAND WARMER UNION JACK", 1.85),
        ("22632", "HAND WARMER RED POLKA DOT", 1.85),
        ("20725", "LUNCH BAG RED RETROSPOT", 4.25),
        ("22890", "NOVELTY BICYCLE BOTTLE OPENER", 1.25),
        ("84879", "ASSORTED COLOUR BIRD ORNAMENT", 1.69),
        ("22197", "SMALL POPCORN HOLDER", 0.85),
        ("22386", "JUMBO BAG APPLE DESIGN", 1.95),
        ("22375", "AIRLINE BAG VINTAGE WORLD CHAMPION", 4.95),
        ("22469", "HEART OF WICKER SMALL", 1.65),
        ("22423", "REGENCY CAKESTAND 3 TIER", 12.75),
        ("22720", "SET OF 3 CAKE TINS PANTRY DESIGN", 8.95),
        ("22816", "SET 6 RED SPOTTY PAPER CUPS", 2.95),
        ("22811", "SET 6 RED SPOTTY PAPER PLATES", 2.95),
        ("22457", "NATURAL SLATE HEART CHALKBOARD", 4.95),
        ("85014", "BLUE POLKADOT WRAP", 0.42),
        ("20713", "BAG 250g SWIRLY MARBLES", 0.42),
        ("23355", "HOT WATER BOTTLE KEEP CALM", 4.95),
        ("POST", "POSTAGE", 18.00),
        ("DOT", "DOTCOM POSTAGE", 18.00),
        ("22960", "JAM MAKING SET WITH JARS", 4.25),
        ("23084", "RABBIT NIGHT LIGHT", 1.79),
        ("20974", "PINK CHERRY LIGHTS", 4.95),
        ("22145", "CHRISTMAS CRAFT PAPER TAPE", 0.29),
    ]
    
    # Countries with weights (UK has highest probability)
    countries = [
        ("United Kingdom", 0.78),
        ("Germany", 0.05),
        ("France", 0.04),
        ("EIRE", 0.03),
        ("Spain", 0.025),
        ("Netherlands", 0.025),
        ("Belgium", 0.015),
        ("Italy", 0.015),
        ("Portugal", 0.01),
        ("Australia", 0.005),
        ("Norway", 0.005),
        ("Channel Islands", 0.0025),
        ("Japan", 0.0025),
    ]
    
    country_names = [c[0] for c in countries]
    country_weights = [c[1] for c in countries]
    
    # Normalize weights to sum to 1
    total_weight = sum(country_weights)
    country_weights = [w / total_weight for w in country_weights]
    
    # Generate data
    records = []
    
    # Generate customer IDs (some records will have missing CustomerID)
    n_customers = max(1000, n_records // 10)
    customer_ids = list(range(12346, 12346 + n_customers))
    
    # Date range: December 2010 to December 2011
    start_date = datetime(2010, 12, 1)
    end_date = datetime(2011, 12, 9)
    date_range = (end_date - start_date).days
    
    # Generate invoice numbers
    invoice_counter = 536365
    current_invoice = None
    items_in_current_invoice = 0
    max_items_per_invoice = 20
    
    for i in range(n_records):
        # Decide if we need a new invoice
        if current_invoice is None or items_in_current_invoice >= max_items_per_invoice:
            # 5% chance of cancellation invoice
            if random.random() < 0.05:
                current_invoice = f"C{invoice_counter}"
            else:
                current_invoice = str(invoice_counter)
            invoice_counter += 1
            items_in_current_invoice = 0
        
        items_in_current_invoice += 1
        
        # Select product
        stock_code, description, base_price = random.choice(products)
        
        # Add some price variation (±20%)
        price_multiplier = random.uniform(0.8, 1.2)
        unit_price = round(base_price * price_multiplier, 2)
        
        # Generate quantity (most orders are small, some are large wholesale)
        if random.random() < 0.8:  # 80% small quantities
            quantity = random.randint(1, 10)
        else:  # 20% larger quantities (wholesale)
            quantity = random.randint(20, 200)
        
        # For cancellation invoices, make quantity negative
        if current_invoice.startswith('C'):
            quantity = -abs(quantity)
        
        # Generate date
        days_from_start = random.randint(0, date_range)
        invoice_date = start_date + timedelta(days=days_from_start)
        
        # Add some time to the date
        hours = random.randint(8, 18)  # Business hours
        minutes = random.randint(0, 59)
        invoice_date = invoice_date.replace(hour=hours, minute=minutes)
        
        # Select country
        country = np.random.choice(country_names, p=country_weights)
        
        # Customer ID (90% have customer ID, 10% are missing)
        if random.random() < 0.9:
            customer_id = random.choice(customer_ids)
        else:
            customer_id = None
        
        # Create record
        record = {
            'InvoiceNo': current_invoice,
            'StockCode': stock_code,
            'Description': description,
            'Quantity': quantity,
            'InvoiceDate': invoice_date.strftime('%m/%d/%Y %H:%M'),
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Country': country
        }
        
        records.append(record)
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Sort by InvoiceDate to make it more realistic
    df = df.sort_values('InvoiceDate').reset_index(drop=True)
    
    return df

def main():
    """Generate and save sample data."""
    print("Generating sample online retail dataset...")
    
    # Generate 15,000 records for a good sample size
    df = generate_sample_retail_data(15000)
    
    # Save to CSV
    output_file = 'data/raw/online_retail_sample.csv'
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"Sample dataset generated and saved to: {output_file}")
    print(f"Dataset shape: {df.shape}")
    print(f"Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
    print(f"Number of unique customers: {df['CustomerID'].nunique()}")
    print(f"Number of unique products: {df['StockCode'].nunique()}")
    print(f"Number of countries: {df['Country'].nunique()}")
    
    # Show sample data
    print("\nSample records:")
    print(df.head(10).to_string())

if __name__ == "__main__":
    main()