import re
from typing import Dict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_REGEX = re.compile(r"(?:\+\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?[\d\s-]{6,15}\d")


def infer_company_name(url: str, soup: BeautifulSoup) -> str:
    if soup.title and soup.title.text.strip():
        title = soup.title.text.strip()
        return title.split("|")[0].split("-")[0].strip()

    domain = urlparse(url).netloc.replace("www.", "")
    return domain.split(".")[0].replace("-", " ").title()


def scrape_company_data(url: str, timeout: int = 12) -> Dict[str, str]:
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
