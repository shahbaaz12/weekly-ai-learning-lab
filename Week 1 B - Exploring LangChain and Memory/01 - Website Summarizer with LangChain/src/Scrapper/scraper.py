import requests
from bs4 import BeautifulSoup

# Mimic a normal browser so websites are more likely to allow the request.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Remove page elements that usually add noise to the summary.
TAGS_TO_REMOVE = (
    "script",
    "style",
    "nav",
    "footer",
    "header",
    "img",
    "input",
)

# Prevent huge webpages from sending excessive text to the LLM.
MAX_CONTENT_CHARACTERS = 20_000


def fetch_website_contents(url: str) -> str:
    """Fetch a webpage and return its cleaned text content."""
    # Remove accidental spaces before validating the URL.
    url = url.strip()

    if not url:
        raise ValueError("Enter a website URL.")

    # Add HTTPS when the user enters only a domain name.
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(f"Could not fetch the website: {error}") from error

    # Parse the returned HTML into a searchable document.
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else "No title found"

    # Delete non-content elements before extracting readable text.
    for tag in soup(TAGS_TO_REMOVE):
        tag.decompose()

    # Extract the remaining visible text after noisy elements were removed.
    text = soup.get_text(separator="\n", strip=True)

    if not text:
        raise RuntimeError("No readable text was found on this page.")

    # Keep the prompt within a sensible size.
    if len(text) > MAX_CONTENT_CHARACTERS:
        text = text[:MAX_CONTENT_CHARACTERS] + "\n\n[Content truncated]"

    return f"Title: {title}\n\nPage contents:\n{text}"
