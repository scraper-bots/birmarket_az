import requests
import pandas as pd
import json
from typing import List, Dict
import time

class UmicoScraper:
    def __init__(self):
        self.base_url = "https://search.umico.az/v2/marketing_names"
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "az",
            "content-language": "az",
            "origin": "https://birmarket.az",
            "referer": "https://birmarket.az/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }
        self.all_data = []

    def fetch_page(self, page: int, per_page: int = 60) -> Dict:
        """Fetch a single page of data from the API"""
        params = {
            "page": page,
            "per_page": per_page,
            "country_id": 1,
            "city_id": 1,
            "sort_by": "popular",
            "coordinates": "40.372508,49.842474"
        }

        try:
            response = requests.get(self.base_url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            return None

    def extract_useful_data(self, item: Dict) -> Dict:
        """Extract useful fields from a single item"""
        # Extract phone numbers
        phones = []
        if item.get('partner_contacts'):
            phones = [contact['contact_value'] for contact in item['partner_contacts']
                     if contact.get('contact_type') == 'work']

        # Extract social media
        social_media = {}
        if item.get('partner_social_accounts'):
            for account in item['partner_social_accounts']:
                social_media[account['social_network']] = account['link']

        # Extract categories
        categories = []
        if item.get('categories'):
            categories = [cat['name_az'] for cat in item['categories']]

        # Extract point of sales (addresses)
        addresses = []
        if item.get('point_of_sales'):
            for pos in item['point_of_sales']:
                address_info = {
                    'city': pos.get('city', {}).get('name_az', ''),
                    'district': pos.get('district', {}).get('name_az', ''),
                    'street': pos.get('street_az', ''),
                    'house': pos.get('house', ''),
                    'address_notes': pos.get('address_notes_az', ''),
                    'location': pos.get('location', ''),
                }

                # Extract operating hours
                hours = []
                if pos.get('pos_operating_hours'):
                    for hour in pos['pos_operating_hours']:
                        if not hour.get('non_working_day'):
                            hours.append(f"{hour['day_of_week']}: {hour['from']}-{hour['to']}")
                address_info['operating_hours'] = '; '.join(hours)

                addresses.append(address_info)

        # Extract rating
        rating = None
        if item.get('ratings') and item['ratings'].get('marketing_name_rating_value'):
            rating = item['ratings']['marketing_name_rating_value']

        # Build the result
        result = {
            'store_name': item.get('name', ''),
            'phone_numbers': ', '.join(phones),
            'website': item.get('website', ''),
            'cashback_percentage': item.get('cashback_percentage', ''),
            'rating': rating,
            'rating_count': item.get('ratings', {}).get('marketing_name_session_count', ''),
            'categories': ' | '.join(categories),
            'main_category': item.get('main_category', {}).get('name_az', ''),
            'active': item.get('active', False),
            'instagram': social_media.get('instagram', ''),
            'facebook': social_media.get('facebook', ''),
            'notes': item.get('notes_az', ''),
        }

        # Add address information (first location if multiple exist)
        if addresses:
            first_address = addresses[0]
            result.update({
                'city': first_address['city'],
                'district': first_address['district'],
                'street': first_address['street'],
                'house': first_address['house'],
                'address_notes': first_address['address_notes'],
                'coordinates': first_address['location'],
                'operating_hours': first_address['operating_hours'],
            })

            # If multiple locations, add a count
            result['total_locations'] = len(addresses)
        else:
            result.update({
                'city': '',
                'district': '',
                'street': '',
                'house': '',
                'address_notes': '',
                'coordinates': '',
                'operating_hours': '',
                'total_locations': 0
            })

        return result

    def scrape_all_pages(self, max_pages: int = 100):
        """Scrape all pages until no more data is returned"""
        print("Starting to scrape data from Umico API...")
        page = 1

        while page <= max_pages:
            print(f"Fetching page {page}...")
            data = self.fetch_page(page)

            if not data or 'data' not in data or len(data['data']) == 0:
                print(f"No more data found at page {page}. Stopping.")
                break

            # Extract useful data from each item
            for item in data['data']:
                useful_data = self.extract_useful_data(item)
                self.all_data.append(useful_data)

            print(f"Extracted {len(data['data'])} items from page {page}")

            # Check if we've reached the last page
            if len(data['data']) < 60:  # Less than per_page means last page
                print("Reached the last page.")
                break

            page += 1
            time.sleep(1)  # Be respectful to the API

        print(f"\nTotal items scraped: {len(self.all_data)}")
        return self.all_data

    def save_to_csv(self, filename: str = 'umico_stores.csv'):
        """Save the scraped data to CSV"""
        if not self.all_data:
            print("No data to save!")
            return

        df = pd.DataFrame(self.all_data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data saved to {filename}")

    def save_to_xlsx(self, filename: str = 'umico_stores.xlsx'):
        """Save the scraped data to XLSX"""
        if not self.all_data:
            print("No data to save!")
            return

        df = pd.DataFrame(self.all_data)

        # Create Excel writer with openpyxl engine
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Stores')

            # Auto-adjust column widths
            worksheet = writer.sheets['Stores']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)

        print(f"Data saved to {filename}")


if __name__ == "__main__":
    scraper = UmicoScraper()

    # Scrape all pages
    scraper.scrape_all_pages()

    # Save to both formats
    scraper.save_to_csv('umico_stores.csv')
    scraper.save_to_xlsx('umico_stores.xlsx')

    print("\nScraping completed successfully!")
    print(f"Files created: umico_stores.csv and umico_stores.xlsx")
