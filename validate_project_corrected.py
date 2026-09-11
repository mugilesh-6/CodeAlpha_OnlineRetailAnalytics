"""
CORRECTED Project Validation Script
CodeAlpha Data Analytics Internship Project

This script validates that the project uses the OFFICIAL UCI Online Retail dataset
and removes all synthetic/fake data from the submission.

CRITICAL CHECKS:
1. Official UCI dataset is present and valid
2. No synthetic data is used anywhere
3. All statistics are calculated from real data
4. Proper data source attribution
"""

import os
import sys
import pandas as pd
import json
from datetime import datetime

def check_uci_dataset():
    """Check if the official UCI Online Retail dataset is present and valid."""
    print("🔍 CRITICAL: Checking UCI Online Retail Dataset")
    print("-" * 50)
    
    uci_file = 'data/raw/Online Retail.xlsx'
    
    if not os.path.exists(uci_file):
        print(f"❌ CRITICAL FAILURE: Official UCI dataset not found")
        print(f"   Expected: {uci_file}")
        print(f"   Please download from: https://archive.ics.uci.edu/dataset/352/online+retail")
        return False
    
    try:
        # Check file size (real UCI file should be ~18-25MB)
        file_size = os.path.getsize(uci_file)
        print(f"📁 File size: {file_size/1024/1024:.1f} MB")
        
        if file_size < 15_000_000:
            print(f"❌ File size too small (expected >15MB)")
            print(f"   This may not be the official UCI dataset")
            return False
        
        # Load and validate dataset structure
        df = pd.read_excel(uci_file)
        record_count = len(df)
        
        print(f"📊 Records: {record_count:,}")
        print(f"📊 Columns: {list(df.columns)}")
        
        # Check record count (official UCI has ~541,909 records)
        if record_count < 500_000:
            print(f"❌ Record count too low (expected ~541,909)")
            return False
        
        # Check expected columns
        expected_columns = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 
                          'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
        
        missing_columns = set(expected_columns) - set(df.columns)
        if missing_columns:
            print(f"❌ Missing expected columns: {missing_columns}")
            return False
        
        # Check date range (should be 2010-2011)
        date_min = pd.to_datetime(df['InvoiceDate']).min()
        date_max = pd.to_datetime(df['InvoiceDate']).max()
        
        print(f"📅 Date range: {date_min.date()} to {date_max.date()}")
        
        if not (date_min.year == 2010 and date_max.year == 2011):
            print(f"❌ Invalid date range (expected 2010-2011)")
            return False
        
        print(f"✅ UCI dataset validation: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Error validating UCI dataset: {e}")
        return False

def check_synthetic_data_removed():
    """Check that synthetic/fake data has been removed from the project."""
    print("\n🚫 CRITICAL: Checking for Synthetic Data Removal")
    print("-" * 50)
    
    # Check for synthetic data files in main directories
    synthetic_files = [
        'data/raw/online_retail_sample.csv',
        'data/cleaned/online_retail_sample.csv'
    ]
    
    found_synthetic = []
    for file_path in synthetic_files:
        if os.path.exists(file_path):
            found_synthetic.append(file_path)
    
    if found_synthetic:
        print(f"❌ Synthetic data files still present:")
        for f in found_synthetic:
            print(f"   - {f}")
        print(f"   These must be moved to data/archive/ or removed")
        return False
    
    # Check if cleaned dataset exists and is realistic
    cleaned_file = 'data/cleaned/online_retail_cleaned.csv'
    
    if not os.path.exists(cleaned_file):
        print(f"❌ Cleaned dataset not found: {cleaned_file}")
        return False
    
    try:
        df_cleaned = pd.read_csv(cleaned_file, parse_dates=['InvoiceDate'])
        record_count = len(df_cleaned)
        
        print(f"📊 Cleaned dataset records: {record_count:,}")
        
        # Check for synthetic data indicators (known fake values)
        synthetic_indicators = {
            'total_records': [15000, 15_000],
            'unique_customers': [1500, 1_500], 
            'unique_orders': [750],
            'unique_products': [30]
        }
        
        actual_values = {
            'total_records': len(df_cleaned),
            'unique_customers': df_cleaned['CustomerID'].nunique(),
            'unique_orders': df_cleaned['InvoiceNo'].nunique(),
            'unique_products': df_cleaned['StockCode'].nunique()
        }
        
        print(f"📊 Actual metrics:")
        for key, value in actual_values.items():
            print(f"   {key}: {value:,}")
        
        # Check if any values match synthetic indicators
        for metric, indicators in synthetic_indicators.items():
            if actual_values[metric] in indicators:
                print(f"❌ Synthetic data indicator detected: {metric} = {actual_values[metric]}")
                return False
        
        # Record count should be realistic for UCI dataset (>400k after cleaning)
        if record_count < 400_000:
            print(f"❌ Record count too low for UCI dataset: {record_count:,}")
            print(f"   Expected >400,000 after cleaning")
            return False
        
        print(f"✅ Synthetic data removal: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Error checking cleaned dataset: {e}")
        return False

def check_hardcoded_statistics():
    """Check for hardcoded synthetic statistics in reports and code."""
    print("\n📊 CRITICAL: Checking for Hardcoded Synthetic Statistics")
    print("-" * 50)
    
    # Known synthetic values to search for
    synthetic_values = [
        '15,000', '15000',
        '1,543,309', '1543309',
        '£1,543,309',
        '750 orders',
        '1,500 customers', '1500 customers',
        '78% of revenue',
        '40% retention',
        '£151K', '£151,520'
    ]
    
    # Files to check
    files_to_check = [
        'README.md',
        'reports/EDA_Report.md',
        'reports/Visualization_Report.md',
        'reports/Web_Scraping_Report.md',
        'dashboard/app.py'
    ]
    
    hardcoded_found = []
    
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found_in_file = []
            for synthetic_value in synthetic_values:
                if synthetic_value in content:
                    found_in_file.append(synthetic_value)
            
            if found_in_file:
                hardcoded_found.append({
                    'file': file_path,
                    'values': found_in_file
                })
                
        except Exception as e:
            print(f"⚠️  Warning: Could not check {file_path}: {e}")
    
    if hardcoded_found:
        print(f"❌ Hardcoded synthetic statistics found:")
        for item in hardcoded_found:
            print(f"   File: {item['file']}")
            for value in item['values']:
                print(f"     - '{value}'")
        print(f"\n   These must be removed and replaced with real calculated values")
        return False
    
    print(f"✅ No hardcoded synthetic statistics found")
    return True

def check_data_source_attribution():
    """Check that data sources are properly attributed."""
    print("\n📚 Checking Data Source Attribution")
    print("-" * 50)
    
    attribution_correct = True
    
    # Check README for proper attribution
    readme_path = 'README.md'
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            required_attributions = [
                'UCI Machine Learning Repository',
                'Online Retail',
                'books.toscrape.com'
            ]
            
            missing_attributions = []
            for attribution in required_attributions:
                if attribution not in readme_content:
                    missing_attributions.append(attribution)
            
            if missing_attributions:
                print(f"❌ Missing attributions in README: {missing_attributions}")
                attribution_correct = False
            else:
                print(f"✅ Data source attributions present in README")
                
        except Exception as e:
            print(f"❌ Error checking README: {e}")
            attribution_correct = False
    
    return attribution_correct

def check_task_completeness():
    """Check that all required task components exist."""
    print("\n📋 Checking Task Completeness")
    print("-" * 50)
    
    required_files = {
        'Task 1 - Web Scraping': [
            'src/scraper.py',
            'data/scraped/books_scraped.csv',
            'notebooks/01_web_scraping.ipynb',
            'reports/Web_Scraping_Report.md'
        ],
        'Task 2 - EDA': [
            'src/data_cleaning.py',
            'data/cleaned/online_retail_cleaned.csv',
            'notebooks/02_exploratory_data_analysis.ipynb',
            'reports/EDA_Report.md'
        ],
        'Task 3 - Visualization': [
            'dashboard/app.py',
            'reports/Visualization_Report.md'
        ],
        'Documentation': [
            'README.md',
            'requirements.txt'
        ]
    }
    
    all_complete = True
    
    for task, files in required_files.items():
        print(f"\n{task}:")
        task_complete = True
        
        for file_path in files:
            exists = os.path.exists(file_path)
            status_icon = "✅" if exists else "❌"
            print(f"   {status_icon} {file_path}")
            
            if not exists:
                task_complete = False
                all_complete = False
        
        task_status = "COMPLETE" if task_complete else "INCOMPLETE"
        print(f"   → {task}: {task_status}")
    
    return all_complete

def run_data_cleaning_test():
    """Test if the data cleaning pipeline works with UCI data."""
    print("\n🧹 Testing Data Cleaning Pipeline")
    print("-" * 50)
    
    # Check if UCI dataset exists
    if not os.path.exists('data/raw/Online Retail.xlsx'):
        print(f"❌ Cannot test cleaning: UCI dataset not found")
        return False
    
    try:
        # Try to run data cleaning
        print(f"🔧 Running data cleaning pipeline...")
        import subprocess
        result = subprocess.run([sys.executable, 'src/data_cleaning.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ Data cleaning pipeline: SUCCESS")
            
            # Check output
            if os.path.exists('data/cleaned/online_retail_cleaned.csv'):
                df_cleaned = pd.read_csv('data/cleaned/online_retail_cleaned.csv')
                print(f"   Generated {len(df_cleaned):,} cleaned records")
                return True
            else:
                print(f"❌ Cleaned dataset not generated")
                return False
        else:
            print(f"❌ Data cleaning failed:")
            print(f"   {result.stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Data cleaning timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing data cleaning: {e}")
        return False

def generate_validation_report():
    """Generate the final validation report."""
    print("\n" + "="*80)
    print("FINAL VALIDATION REPORT - CORRECTED VERSION")
    print("="*80)
    
    # Run all critical checks
    checks = {
        'UCI Dataset Valid': check_uci_dataset(),
        'Synthetic Data Removed': check_synthetic_data_removed(),
        'No Hardcoded Statistics': check_hardcoded_statistics(),
        'Data Source Attribution': check_data_source_attribution(),
        'Task Completeness': check_task_completeness(),
        'Data Cleaning Works': run_data_cleaning_test()
    }
    
    # Calculate overall status
    all_passed = all(checks.values())
    critical_passed = all([
        checks['UCI Dataset Valid'],
        checks['Synthetic Data Removed'],
        checks['No Hardcoded Statistics']
    ])
    
    print(f"\n🎯 OVERALL STATUS: {'PASS' if all_passed else 'FAIL'}")
    print(f"🔍 CRITICAL CHECKS: {'PASS' if critical_passed else 'FAIL'}")
    
    print(f"\n📊 VALIDATION RESULTS:")
    for check_name, result in checks.items():
        status_icon = "✅" if result else "❌"
        print(f"   {status_icon} {check_name}")
    
    # Manual steps if needed
    if not critical_passed:
        print(f"\n⚠️  MANUAL STEPS REQUIRED:")
        
        if not checks['UCI Dataset Valid']:
            print(f"   1. Download official UCI Online Retail dataset:")
            print(f"      Source: https://archive.ics.uci.edu/dataset/352/online+retail")
            print(f"      Save as: data/raw/Online Retail.xlsx")
            print(f"      Instructions: data/MANUAL_DOWNLOAD_INSTRUCTIONS.md")
        
        if not checks['Synthetic Data Removed']:
            print(f"   2. Remove synthetic data files:")
            print(f"      Move data/raw/online_retail_sample.csv to data/archive/")
            print(f"      Run: python src/data_cleaning.py (with UCI data)")
        
        if not checks['No Hardcoded Statistics']:
            print(f"   3. Update reports to remove hardcoded synthetic numbers")
            print(f"      Replace all statistics with calculations from real UCI data")
    
    # Ready for submission status
    if all_passed:
        print(f"\n🎉 PROJECT READY FOR CODEALPHA SUBMISSION!")
        print(f"✅ All requirements met")
        print(f"✅ Official UCI dataset validated")
        print(f"✅ No synthetic data present")
        print(f"✅ All statistics calculated from real data")
    else:
        print(f"\n❌ PROJECT NOT READY FOR SUBMISSION")
        print(f"🔧 Please address the issues above before submission")
    
    # Save report
    validation_result = {
        'timestamp': datetime.now().isoformat(),
        'overall_status': 'PASS' if all_passed else 'FAIL',
        'critical_status': 'PASS' if critical_passed else 'FAIL',
        'checks': {k: 'PASS' if v else 'FAIL' for k, v in checks.items()},
        'ready_for_submission': all_passed
    }
    
    with open('validation_report_corrected.json', 'w') as f:
        json.dump(validation_result, f, indent=2)
    
    print(f"\n📄 Detailed report saved: validation_report_corrected.json")
    
    return all_passed

def main():
    """Run the corrected project validation."""
    print("CodeAlpha Data Analytics Internship Project")
    print("CORRECTED PROJECT VALIDATION")
    print("="*80)
    print("🎯 Focus: Official UCI dataset validation and synthetic data removal")
    print("")
    
    success = generate_validation_report()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)