"""
Final Project Validation Script
CodeAlpha Data Analytics Internship Project
"""

import os
import pandas as pd

def validate_core_files():
    """Validate that all required files exist."""
    print("Checking Core Files...")
    
    required_files = [
        'dashboard/app.py',
        'src/scraper.py', 
        'src/data_cleaning.py',
        'notebooks/01_web_scraping.ipynb',
        'notebooks/02_exploratory_data_analysis.ipynb',
        'reports/Web_Scraping_Report.md',
        'reports/EDA_Report.md', 
        'reports/Visualization_Report.md',
        'README.md',
        'requirements.txt'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"FAIL - Missing files: {missing}")
        return False
    else:
        print("PASS - All required files present")
        return True

def validate_data():
    """Validate data files and UCI dataset usage."""
    print("Checking Data Files...")
    
    # Check UCI dataset
    uci_file = 'data/raw/Online Retail.xlsx'
    cleaned_file = 'data/cleaned/online_retail_cleaned.csv'
    scraped_file = 'data/scraped/books_scraped.csv'
    
    if not os.path.exists(uci_file):
        print("FAIL - UCI dataset missing (must be downloaded manually)")
        return False
        
    if not os.path.exists(cleaned_file):
        print("FAIL - Cleaned dataset missing")  
        return False
        
    if not os.path.exists(scraped_file):
        print("FAIL - Scraped dataset missing")
        return False
    
    # Check cleaned dataset size 
    try:
        df = pd.read_csv(cleaned_file)
        record_count = len(df)
        
        if record_count < 500000:
            print(f"WARN - Low record count: {record_count:,} (expected ~534k)")
        else:
            print(f"PASS - Real UCI dataset: {record_count:,} records")
            
    except Exception as e:
        print(f"FAIL - Error reading cleaned dataset: {e}")
        return False
    
    return True

def validate_no_synthetic():
    """Check for synthetic data remnants.""" 
    print("Checking for Synthetic Data...")
    
    # Check that synthetic generator is removed
    if os.path.exists('src/generate_sample_data.py'):
        print("FAIL - Synthetic data generator still present")
        return False
        
    # Check data archive
    if os.path.exists('data/archive/online_retail_sample.csv'):
        print("OK - Synthetic data properly archived")
    
    print("PASS - No synthetic data in production")
    return True

def main():
    """Run final validation."""
    print("CodeAlpha Project - Final Validation")
    print("=" * 50)
    
    tests = [
        ("Core Files", validate_core_files),
        ("Data Files", validate_data), 
        ("Synthetic Data Check", validate_no_synthetic)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("FINAL VALIDATION RESULTS")  
    print("=" * 50)
    
    if all(results):
        print("PASS - Project ready for submission!")
        return True
    else:
        print("FAIL - Issues found, see details above")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)