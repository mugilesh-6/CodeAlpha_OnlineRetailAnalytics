"""
Web Scraper for Books to Scrape Website
CodeAlpha Data Analytics Internship - Task 1

This module scrapes book data from books.toscrape.com for educational purposes.
The website is specifically designed for web scraping practice.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Optional

class BooksScraper:
    """
    A web scraper for books.toscrape.com - an educational scraping practice site.
    
    This scraper collects book information including titles, prices, ratings,
    availability, and other metadata from the demo bookstore.
    """
    
    def __init__(self, base_url: str = "https://books.toscrape.com", delay: float = 1.0):
        """
        Initialize the scraper.
        
        Args:
            base_url: The base URL of the website to scrape
            delay: Delay between requests to avoid overwhelming the server
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if request fails
        """
        try:
            self.logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Add delay to be respectful
            time.sleep(self.delay)
            
            return BeautifulSoup(response.content, 'html.parser')
            
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_rating(self, rating_element) -> int:
        """
        Extract numeric rating from rating element.
        
        Args:
            rating_element: BeautifulSoup element containing rating
            
        Returns:
            Rating as integer (1-5)
        """
        if not rating_element:
            return 0
            
        rating_classes = rating_element.get('class', [])
        rating_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        
        for class_name in rating_classes:
            if class_name in rating_map:
                return rating_map[class_name]
        
        return 0
    
    def extract_price(self, price_text: str) -> float:
        """
        Extract numeric price from price string.
        
        Args:
            price_text: Price string (e.g., "£51.77")
            
        Returns:
            Price as float
        """
        try:
            # Remove currency symbols and extract number
            price_clean = re.sub(r'[£$€]', '', price_text.strip())
            return float(price_clean)
        except (ValueError, AttributeError):
            return 0.0
    
    def scrape_book_details(self, book_url: str) -> Dict:
        """
        Scrape detailed information from a book's individual page.
        
        Args:
            book_url: URL of the book's detail page
            
        Returns:
            Dictionary containing book details
        """
        soup = self.get_page(book_url)
        if not soup:
            return {}
        
        details = {}
        
        try:
            # Extract product information table
            product_info = soup.find('table', class_='table table-striped')
            if product_info:
                rows = product_info.find_all('tr')
                for row in rows:
                    th = row.find('th')
                    td = row.find('td')
                    if th and td:
                        key = th.get_text(strip=True)
                        value = td.get_text(strip=True)
                        details[key] = value
            
            # Extract description if available
            description_div = soup.find('div', id='product_description')
            if description_div:
                description_p = description_div.find_next_sibling('p')
                if description_p:
                    details['Description'] = description_p.get_text(strip=True)
                    
        except Exception as e:
            self.logger.error(f"Error extracting details from {book_url}: {e}")
        
        return details
    
    def scrape_books_from_page(self, page_url: str) -> List[Dict]:
        """
        Scrape all books from a single page.
        
        Args:
            page_url: URL of the page to scrape
            
        Returns:
            List of dictionaries containing book data
        """
        soup = self.get_page(page_url)
        if not soup:
            return []
        
        books = []
        
        # Find all book articles
        book_articles = soup.find_all('article', class_='product_pod')
        
        for article in book_articles:
            try:
                book_data = {}
                
                # Extract title
                title_element = article.find('h3').find('a')
                book_data['Title'] = title_element.get('title', title_element.get_text(strip=True))
                
                # Extract book URL for detailed scraping
                book_url = urljoin(self.base_url, title_element.get('href'))
                book_data['URL'] = book_url
                
                # Extract price
                price_element = article.find('p', class_='price_color')
                if price_element:
                    price_text = price_element.get_text(strip=True)
                    book_data['Price_Text'] = price_text
                    book_data['Price'] = self.extract_price(price_text)
                
                # Extract rating
                rating_element = article.find('p', class_='star-rating')
                book_data['Rating'] = self.extract_rating(rating_element)
                
                # Extract availability
                availability_element = article.find('p', class_='instock availability')
                if availability_element:
                    book_data['Availability'] = availability_element.get_text(strip=True)
                
                # Extract image URL
                img_element = article.find('div', class_='image_container').find('img')
                if img_element:
                    book_data['Image_URL'] = urljoin(self.base_url, img_element.get('src'))
                
                books.append(book_data)
                
            except Exception as e:
                self.logger.error(f"Error extracting book data: {e}")
                continue
        
        return books
    
    def get_all_page_urls(self) -> List[str]:
        """
        Get URLs of all pages to scrape.
        
        Returns:
            List of page URLs
        """
        page_urls = []
        current_page = 1
        
        while True:
            if current_page == 1:
                page_url = self.base_url + '/index.html'
            else:
                page_url = f"{self.base_url}/catalogue/page-{current_page}.html"
            
            soup = self.get_page(page_url)
            if not soup:
                break
            
            # Check if page has books
            book_articles = soup.find_all('article', class_='product_pod')
            if not book_articles:
                break
            
            page_urls.append(page_url)
            
            # Check for next page
            next_button = soup.find('li', class_='next')
            if not next_button:
                break
            
            current_page += 1
            
            # Safety limit to avoid infinite loops
            if current_page > 100:
                self.logger.warning("Reached safety limit of 100 pages")
                break
        
        return page_urls
    
    def scrape_all_books(self, max_pages: int = 5) -> pd.DataFrame:
        """
        Scrape books from specified number of pages.
        
        Args:
            max_pages: Maximum number of pages to scrape (for testing purposes)
            
        Returns:
            DataFrame containing all scraped book data
        """
        self.logger.info("Starting to scrape books from books.toscrape.com")
        
        all_books = []
        
        # Generate page URLs directly instead of checking all pages
        page_urls = []
        for page_num in range(1, max_pages + 1):
            if page_num == 1:
                page_urls.append(f"{self.base_url}/index.html")
            else:
                page_urls.append(f"{self.base_url}/catalogue/page-{page_num}.html")
        
        self.logger.info(f"Will scrape {len(page_urls)} pages")
        
        for i, page_url in enumerate(page_urls, 1):
            self.logger.info(f"Scraping page {i}/{len(page_urls)}: {page_url}")
            
            books = self.scrape_books_from_page(page_url)
            if not books:  # If no books found, stop scraping
                self.logger.info(f"No books found on page {i}, stopping")
                break
                
            all_books.extend(books)
            self.logger.info(f"Extracted {len(books)} books from page {i}")
        
        # Create DataFrame
        df = pd.DataFrame(all_books)
        
        if not df.empty:
            # Add scraping metadata
            df['Scraped_Date'] = pd.Timestamp.now()
            df['Source'] = 'books.toscrape.com'
            
            # Reorder columns for better presentation
            column_order = ['Title', 'Price', 'Price_Text', 'Rating', 'Availability', 
                          'URL', 'Image_URL', 'Scraped_Date', 'Source']
            
            # Only include columns that exist
            available_columns = [col for col in column_order if col in df.columns]
            df = df[available_columns]
        
        self.logger.info(f"Scraping completed. Total books scraped: {len(df)}")
        
        return df
    
    def save_data(self, df: pd.DataFrame, filename: str) -> None:
        """
        Save scraped data to CSV file.
        
        Args:
            df: DataFrame to save
            filename: Output filename
        """
        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            self.logger.info(f"Data saved to {filename}")
            self.logger.info(f"Dataset shape: {df.shape}")
            
            # Print summary statistics
            if 'Price' in df.columns:
                self.logger.info(f"Price range: £{df['Price'].min():.2f} - £{df['Price'].max():.2f}")
            
            if 'Rating' in df.columns:
                self.logger.info(f"Average rating: {df['Rating'].mean():.2f}")
                
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")

def main():
    """
    Main function to run the web scraper.
    """
    # Initialize scraper
    scraper = BooksScraper()
    
    # Scrape books (limit to 5 pages for demo)
    books_df = scraper.scrape_all_books(max_pages=5)
    
    if not books_df.empty:
        # Save to CSV
        output_file = 'data/scraped/books_scraped.csv'
        scraper.save_data(books_df, output_file)
        
        # Display summary
        print("\n" + "="*50)
        print("SCRAPING SUMMARY")
        print("="*50)
        print(f"Website: books.toscrape.com")
        print(f"Total books scraped: {len(books_df)}")
        print(f"Data saved to: {output_file}")
        print(f"Average price: £{books_df['Price'].mean():.2f}")
        print(f"Price range: £{books_df['Price'].min():.2f} - £{books_df['Price'].max():.2f}")
        print(f"Average rating: {books_df['Rating'].mean():.2f}")
        print(f"Columns scraped: {list(books_df.columns)}")
        print("\nFirst 3 rows:")
        print(books_df.head(3).to_string())
        
    else:
        print("No data was scraped. Please check the website and try again.")

if __name__ == "__main__":
    main()