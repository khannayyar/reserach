# get_publications.py
import scholarly
import json
import os

# --- Configuration ---
# Replace with your Google Scholar user ID
AUTHOR_ID = 'A0nTCiwAAAAJ' 
# Define the output file path for your website
OUTPUT_FILE = 'publications.json'

def fetch_scholar_data():
    """Fetches and saves publication data from Google Scholar."""
    print(f"Starting to fetch publications for author ID: {AUTHOR_ID}")

    try:
        # Search for the author by their ID and retrieve their publications
        author = scholarly.scholarly.search_author_id(AUTHOR_ID)
        # The 'fill' method is crucial to get all the details
        author = scholarly.scholarly.fill(author, sections=['publications'])

        publications_list = []
        for pub in author['publications']:
            # Fetch detailed data for each publication
            pub_filled = scholarly.scholarly.fill(pub)

            # Extract the data you need
            publications_list.append({
                'title': pub_filled['bib'].get('title', 'N/A'),
                # --- FIX APPLIED HERE ---
                # Use 0 as a default for the year if it's missing, ensuring it's always a number.
                'year': int(pub_filled['bib'].get('pub_year', 0)),
                'citations': pub_filled.get('num_citations', 0),
                'link': pub_filled.get('pub_url', '#')
            })

        # Sort publications by year, with the most recent first
        publications_list.sort(key=lambda x: x.get('year', 0), reverse=True)

        # Save the list to a JSON file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(publications_list, f, indent=4, ensure_ascii=False)

        print(f"✅ Success! Saved {len(publications_list)} publications to {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    fetch_scholar_data()