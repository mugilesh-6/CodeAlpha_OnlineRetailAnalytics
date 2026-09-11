"""Quick validation of critical project corrections."""

import os
import re

def check_synthetic_statistics():
    """Check for remaining hardcoded synthetic statistics."""
    synthetic_patterns = [
        r'\b15,000\b',
        r'\b1,500\b(?=\s+customers)',
        r'\b750\b(?=\s+orders)', 
        r'£1,543,309',
        r'£151,520',
        r'78%.*UK',
        r'40%.*retention'
    ]
    
    files_to_check = [
        'README.md',
        'reports/EDA_Report.md', 
        'reports/Visualization_Report.md',
        'PROJECT_SUMMARY.md'
    ]
    
    print("🔍 Checking for hardcoded synthetic statistics...")
    issues_found = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for pattern in synthetic_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    issues_found.append(f"  {file_path}: {pattern} -> {matches}")
    
    if issues_found:
        print("❌ Hardcoded synthetic statistics found:")
        for issue in issues_found:
            print(issue)
        return False
    else:
        print("✅ No hardcoded synthetic statistics found!")
        return True

def check_uci_dataset():
    """Check UCI dataset presence."""
    uci_file = 'data/raw/Online Retail.xlsx'
    cleaned_file = 'data/cleaned/online_retail_cleaned.csv'
    
    print("🔍 Checking UCI dataset...")
    
    if not os.path.exists(uci_file):
        print(f"❌ UCI dataset missing: {uci_file}")
        return False
    
    if not os.path.exists(cleaned_file):
        print(f"❌ Cleaned dataset missing: {cleaned_file}")
        return False
        
    # Check cleaned dataset size
    import pandas as pd
    try:
        df = pd.read_csv(cleaned_file)
        record_count = len(df)
        print(f"✅ UCI dataset present: {record_count:,} cleaned records")
        
        # Validate it's not synthetic data
        if record_count == 15000:
            print("❌ Still using synthetic dataset (15,000 records)")
            return False
        elif record_count > 500000:
            print("✅ Using real UCI dataset!")
            return True
        else:
            print(f"⚠️ Unexpected record count: {record_count:,}")
            return True
            
    except Exception as e:
        print(f"❌ Error checking cleaned dataset: {e}")
        return False

def check_uci_attribution():
    """Check for UCI attribution in README."""
    print("🔍 Checking UCI attribution...")
    
    readme_file = 'README.md'
    if not os.path.exists(readme_file):
        print("❌ README.md not found")
        return False
        
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    uci_indicators = [
        'UCI Machine Learning Repository',
        'archive.ics.uci.edu',
        'online+retail'
    ]
    
    found_attributions = []
    for indicator in uci_indicators:
        if indicator.lower() in content.lower():
            found_attributions.append(indicator)
    
    if found_attributions:
        print(f"✅ UCI attribution found: {found_attributions}")
        return True
    else:
        print("❌ UCI attribution missing")
        return False

def main():
    """Run quick validation checks."""
    print("CodeAlpha Project - Quick Validation")
    print("=" * 50)
    
    checks = [
        ("UCI Dataset", check_uci_dataset),
        ("Synthetic Statistics Removal", check_synthetic_statistics), 
        ("UCI Attribution", check_uci_attribution)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("QUICK VALIDATION SUMMARY")
    print("=" * 50)
    
    all_passed = all(results)
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("🎉 Project ready for submission!")
    else:
        print("❌ Some checks failed")
        print("🔧 Please address issues above")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)