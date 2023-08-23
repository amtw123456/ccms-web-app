import requests
import json
from bs4 import BeautifulSoup

# URL of the API call
url = "https://steamcommunity.com/market/search/render/?query=case&start=0&count=3&search_descriptions=0&sort_column=default&sort_dir=desc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase"

# Make the HTTP GET request
response = requests.get(url)
parsed_response = json.loads(response.content)
formatted_response = json.dumps(parsed_response, indent=2)

# print(parsed_response)

soup = BeautifulSoup(parsed_response["results_html"], 'html.parser')

for tag in soup.find_all(class_='sale_price'):
    print(tag.text)
    print("----------------------")


for tag in soup.find_all(class_='market_listing_item_name'):
    print(tag.text)
    print("----------------------")
