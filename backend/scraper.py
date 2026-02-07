import re
from typing import Dict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_REGEX = re.compile(r"(?:\+\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?[\d\s-]{6,15}\d")


def infer_company_name(url: str, soup: BeautifulSoup) -> str:
    """
    Derives a company name from a web page by using the page title when available or falling back to the URL's domain.
    
    If the page title contains separators like "|" or "-", the portion before the first separator is used. If no usable title exists, the leftmost label of the domain (with hyphens replaced by spaces) is converted to title case and returned.
    
    Parameters:
        url (str): The page URL used as a fallback when no title is present.
        soup (BeautifulSoup): Parsed HTML of the page.
    
    Returns:
        str: The inferred company name.
    """
    if soup.title and soup.title.text.strip():
        title = soup.title.text.strip()
        return title.split("|")[0].split("-")[0].strip()

    domain = urlparse(url).netloc.replace("www.", "")
    return domain.split(".")[0].replace("-", " ").title()


def scrape_company_data(url: str, timeout: int = 12) -> Dict[str, str]:
    """
    Fetch a web page and extract basic company contact information.
    
    Parses and normalizes the provided URL, performs an HTTP GET request, and scans the page text for an inferred company name, the first email address, and the first phone number.
    
    Parameters:
        url (str): The page URL to fetch; if the scheme is missing "https://" will be prepended.
        timeout (int): Request timeout in seconds (default 12).
    
    Returns:
        Dict[str, str]: A mapping with keys:
            - "company_name": inferred company name from the page title or domain,
            - "email": first matched email address or None if none found,
            - "phone": first matched phone number or None if none found,
            - "website": the (possibly normalized) URL that was fetched.
    
    Raises:
        ValueError: If the URL has an invalid scheme or missing network location.
        requests.HTTPError: If the HTTP response status indicates an error (raised by response.raise_for_status()).
    """
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Invalid URL format")

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; EUBuyerAutomationBot/1.0)",
    }

    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    emails = EMAIL_REGEX.findall(text)
    phones = PHONE_REGEX.findall(text)

    return {
        "company_name": infer_company_name(url, soup),
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "website": url,
    }