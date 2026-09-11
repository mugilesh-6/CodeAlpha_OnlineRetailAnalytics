
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
