# Event Scraper: Biletix and Biletinial

This project is a Python-based scraping solution for extracting event details from two major ticketing platforms: **Biletix** and **Biletinial**. The scraped data includes event information such as names, descriptions, venues, dates, prices, and media links. The data is consolidated and saved into a single JSON file.

## Features
- Scrapes event details, including:
  - Event name and description
  - Event start and end dates
  - Venue details (latitude, longitude)
  - Ticket prices and categories
  - Media links (images)
- Combines results from **Biletix** and **Biletinial** into a unified JSON format.
- Supports different categories: `Music`, `Theatre`, `Sport`, `Stand-Up`, and more.
- Uses both **Playwright** and **BeautifulSoup** for dynamic and static scraping.
- Includes error handling for missing data and timeouts.

## Prerequisites
### Software
- Python 3.8+
- Chrome or Chromium browser for Playwright

### Libraries
Install dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Dependencies:
- `playwright`: for automated browser-based scraping
- `beautifulsoup4`: for static HTML parsing
- `requests`: for API requests
- `googlemaps`: for geocoding venue addresses
- `openai` and `google-cloud-vision`: for extended functionality

### Google Maps API Key
This project uses the Google Maps API for geolocation. You need to replace the placeholder in your code with a valid API key.

```python
gmaps = googlemaps.Client(key='YOUR_GOOGLE_MAPS_API_KEY')
```

## File Structure
```
project-root/
|
|-- /tests/
|   |-- biletix_scrape.py       # Scraper for Biletix using Playwright
|   |-- test2.py                # Biletix API test file
|   |-- coral-sonar-*.json      # Google Cloud service account credentials
|   |-- biletinial_scraper.py   # Scraper for Biletinial using Playwright
|
|-- biletinialBs4.py            # Static scraping of Biletinial events (BeautifulSoup)
|-- biletixvtwo.py              # Static scraping of Biletix events (Requests)
|-- json_template.json          # JSON output template structure
|-- event_merge.py              # Merges Biletix and Biletinial scraped data
|-- requirements.txt            # Project dependencies
|
|-- README.md                   # Project documentation
```

## Usage
1. **Set Up Playwright**
   Install browsers for Playwright:
   ```bash
   playwright install
   ```

2. **Run Scrapers**
   Run individual scrapers to collect data:

   - **Biletix Scraper**
     ```bash
     python biletixvtwo.py
     ```

   - **Biletinial Scraper**
     ```bash
     python biletinialBs4.py
     ```

3. **Merge Event Data**
   Combine the results from both scrapers:
   ```bash
   python event_merge.py
   ```

   The final consolidated data will be saved as `test4.json`.

## JSON Output Format
The final merged JSON file follows this structure:

```json
{
  "name": "Event Name",
  "description": "Event description",
  "links": ["link"],
  "media": ["img_link"],
  "category": "event_category",
  "places": [
    {
      "name": "Venue Name",
      "lat": 0,
      "long": 0,
      "start_time": "01-01-2024 19:00",
      "end_time": "01-01-2024 21:00",
      "vendors": [
        {
          "name": "biletix",
          "prices": [{ "type": "Regular", "price": 50 }]
        },
        {
          "name": "biletinial",
          "prices": [{ "type": "VIP", "price": 100 }]
        }
      ]
    }
  ]
}
```

## Notes
- **Performance**: The scrapers handle dynamic content and large result sets efficiently using Playwright.
- **Error Handling**: The scrapers account for missing data, geolocation errors, and network timeouts.
- **Dynamic Requests**: For Biletix, API calls fetch pricing and performance details.

## Contributions
Contributions are welcome! If you'd like to add features or fix bugs, please fork the repository and submit a pull request.
