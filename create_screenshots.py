"""
Create Screenshots for Project Documentation
CodeAlpha Data Analytics Internship Project

This script provides instructions for taking dashboard screenshots
and validates the dashboard is ready for demonstration.
"""

import os
import webbrowser
import time
import subprocess
import sys

def create_screenshot_guide():
    """Create guide for taking dashboard screenshots."""
    
    guide = """
# Dashboard Screenshot Guide

## How to Take Screenshots

1. **Start the Dashboard:**
   ```bash
   cd CodeAlpha_OnlineRetailAnalytics
   streamlit run dashboard/app.py
   ```

2. **Wait for Dashboard to Load:**
   - Dashboard will open at http://localhost:8501
   - Wait for all data to load (about 3-5 seconds)

3. **Take the Following Screenshots:**

   **Screenshot 1: Dashboard Overview (dashboard_overview.png)**
   - Full page view showing KPI cards and main charts
   - Capture the header, KPIs, and top visualizations
   
   **Screenshot 2: Filtering in Action (dashboard_filters.png)**
   - Show the sidebar with filters applied
   - Select UK as country filter to demonstrate filtering
   - Capture the filtered results
   
   **Screenshot 3: Interactive Charts (dashboard_charts.png)**
   - Focus on the monthly revenue trend and top products
   - Show hover tooltips if possible
   
   **Screenshot 4: Business Insights (dashboard_insights.png)**
   - Scroll down to show the business insights section
   - Capture the insights cards and recommendations

4. **Save Screenshots:**
   - Save all screenshots in the `screenshots/` directory
   - Use PNG format for best quality
   - Name files descriptively as shown above

5. **Recommended Screenshot Settings:**
   - Browser zoom: 90% or 100%
   - Window size: Maximized or 1920x1080
   - Format: PNG
   - Quality: High resolution

## Alternative: Automated Screenshot Instructions

If you have screenshot tools available:
- **Windows:** Use Snipping Tool or Windows + Shift + S
- **Mac:** Use Command + Shift + 4
- **Linux:** Use gnome-screenshot or similar

## Validation Checklist

Before taking screenshots, verify:
- ✅ Dashboard loads without errors
- ✅ All KPI cards show correct values
- ✅ Charts render properly with data
- ✅ Filters work and update charts
- ✅ No console errors in browser
- ✅ Professional appearance with proper styling
"""
    
    with open('screenshots/SCREENSHOT_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("📸 Screenshot guide created: screenshots/SCREENSHOT_GUIDE.md")

def test_dashboard_launch():
    """Test if dashboard can be launched successfully."""
    print("🔧 Testing dashboard launch capability...")
    
    try:
        # Check if streamlit is available
        result = subprocess.run([sys.executable, '-c', 'import streamlit'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Streamlit is available")
        else:
            print("❌ Streamlit not available")
            return False
        
        # Check if dashboard file exists and is valid
        if not os.path.exists('dashboard/app.py'):
            print("❌ Dashboard file not found")
            return False
        
        print("✅ Dashboard file exists")
        
        # Provide launch instructions
        print("\n🚀 DASHBOARD LAUNCH INSTRUCTIONS:")
        print("1. Open a new terminal/command prompt")
        print("2. Navigate to project directory:")
        print("   cd CodeAlpha_OnlineRetailAnalytics")
        print("3. Launch dashboard:")
        print("   streamlit run dashboard/app.py")
        print("4. Dashboard will open at: http://localhost:8501")
        print("5. Take screenshots as per the guide above")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing dashboard: {e}")
        return False

def create_readme_screenshots_section():
    """Create screenshots section for README."""
    
    screenshots_section = """
## 📸 Dashboard Screenshots

### Overview Dashboard
![Dashboard Overview](screenshots/dashboard_overview.png)
*Main dashboard showing KPI cards, revenue trends, and product performance*

### Interactive Filtering
![Dashboard Filters](screenshots/dashboard_filters.png)
*Sidebar filters allowing real-time data exploration by date, country, and customer type*

### Business Analytics
![Dashboard Charts](screenshots/dashboard_charts.png)
*Interactive charts showing monthly trends, geographic analysis, and customer segments*

### Business Insights
![Dashboard Insights](screenshots/dashboard_insights.png)
*Automated business insights and strategic recommendations based on data analysis*

## 🎬 Dashboard Demo

To see the dashboard in action:

1. **Launch Dashboard:**
   ```bash
   cd CodeAlpha_OnlineRetailAnalytics
   streamlit run dashboard/app.py
   ```

2. **Explore Features:**
   - Adjust filters in the sidebar
   - Hover over charts for detailed information
   - Export filtered data as CSV
   - View real-time KPI updates

3. **Access URL:** http://localhost:8501
"""
    
    with open('screenshots/README_SCREENSHOTS_SECTION.txt', 'w', encoding='utf-8') as f:
        f.write(screenshots_section)
    
    print("📝 README screenshots section created: screenshots/README_SCREENSHOTS_SECTION.txt")

def main():
    """Main function to prepare screenshot documentation."""
    print("CodeAlpha Data Analytics Internship Project")
    print("SCREENSHOT PREPARATION")
    print("="*50)
    
    # Ensure screenshots directory exists
    os.makedirs('screenshots', exist_ok=True)
    
    # Create screenshot guide
    create_screenshot_guide()
    
    # Create README section
    create_readme_screenshots_section()
    
    # Test dashboard capability
    dashboard_ready = test_dashboard_launch()
    
    print("\n" + "="*50)
    print("SCREENSHOT PREPARATION COMPLETE")
    print("="*50)
    
    if dashboard_ready:
        print("✅ Dashboard is ready for screenshots")
        print("📋 Follow the guide in screenshots/SCREENSHOT_GUIDE.md")
        print("🚀 Launch dashboard with: streamlit run dashboard/app.py")
        print("📸 Take screenshots and save to screenshots/ directory")
    else:
        print("❌ Dashboard not ready - please fix issues first")
    
    print("\n📁 Files created:")
    print("   📋 screenshots/SCREENSHOT_GUIDE.md")
    print("   📝 screenshots/README_SCREENSHOTS_SECTION.txt")
    
    return 0 if dashboard_ready else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)