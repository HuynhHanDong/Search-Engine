import requests
import re
from urllib.parse import urljoin
import html

# Global Variables
visited_urls = set()
collected_products = []
MAX_PRODUCTS = 100
MAX_PRODUCTS_PER_PAGE = 5
MAX_DEPTH = 3

# Regular expressions
product_block_pattern = re.compile(r'<article class="product_pod">(.*?)</article>', re.S)
title_pattern = re.compile(r'<h3>.*?title="(.*?)".*?</h3>', re.S)
price_pattern = re.compile(r'<p class="price_color">Â£([0-9]+\.?[0-9]*)</p>')
href_pattern = re.compile(r'href="(.*?)"')

def extract_products(raw_html, depth):
    """ Extract up to 5 product details from HTML using regex """
    blocks = product_block_pattern.findall(raw_html)
    results = []

    for block in blocks[:MAX_PRODUCTS_PER_PAGE]:
        title_match = title_pattern.search(block)
        price_match = price_pattern.search(block)

        if title_match and price_match:
            title = html.unescape(title_match.group(1).strip()) if title_match else "N/A"  # Handles HTML entities in title: ', ", &, <, >
            price = price_match.group(1).strip() if price_match else "N/A"
            results.append((title, price, depth))

    return results

def crawl(url, depth):
    """ Recursive crawler """
    if depth > MAX_DEPTH or len(collected_products) >= MAX_PRODUCTS or url in visited_urls:
        return

    try:
        response = requests.get(url, timeout=5)
        visited_urls.add(url)
        raw_html = response.text

        # Extract and save products
        new_products = extract_products(raw_html, depth)
        for product in new_products:
            if len(collected_products) < MAX_PRODUCTS:
                collected_products.append(product)

        # Extract next links to follow (category/product pages)
        for href in href_pattern.findall(raw_html):
            full_url = urljoin(url, href)
            if 'catalogue' in full_url and full_url not in visited_urls:
                crawl(full_url, depth + 1)

    except Exception as e:
        print(f"Error accessing {url}: {e}")

def main():
    # Start crawling
    start_url = "https://books.toscrape.com/"
    crawl(start_url, 1)

    # Print results
    print("\nCollected Products:\n")
    for i, (title, price, depth) in enumerate(collected_products, start=1):
        print(f"{i}. {title} - £{price} - Depth: {depth}")

if __name__ == "__main__":
    main()
