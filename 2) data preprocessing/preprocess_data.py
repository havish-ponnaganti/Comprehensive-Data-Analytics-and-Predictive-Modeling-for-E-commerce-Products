from bs4 import BeautifulSoup
import os
import pandas as pd

d = {
    'title': [], 'price': [], 'link': [], 'rating': [], 'number_of_ratings': [],
    'items_bought_in_past_month': [], 'original_price': [], 'discounted_price': [],
    'discount_percentage': []
}

html_data_folder = "data/html_data"

for file in os.listdir(html_data_folder):
    try:
        with open(f"{html_data_folder}/{file}", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

            t = soup.find("h2")
            title = t.get_text(strip=True) if t else "Title Not Found"
            a = t.find("a") if t else None
            link = "https://amazon.in/" + a['href'] if a and 'href' in a.attrs else "Link Not Found"
            price_span = soup.find("span", class_="a-price-whole")
            price = price_span.get_text(strip=True) if price_span else "Price Not Found"
            rating_span = soup.find("span", class_="a-icon-alt")
            rating = rating_span.get_text(strip=True) if rating_span else "Rating Not Found"
            num_ratings_span = soup.find("span", class_="a-size-base")
            number_of_ratings = num_ratings_span.get_text(strip=True) if num_ratings_span else "Not Available"
            bought_info = soup.find("span", string=lambda text: text and "bought in past month" in text)
            items_bought_in_past_month = bought_info.get_text(strip=True) if bought_info else "Not Available"
            original_price_span = soup.find("span", class_="a-text-price")
            original_price = original_price_span.get_text(strip=True) if original_price_span else "Not Available"
            offer_price_span = soup.find("span", class_="a-price-whole")
            discounted_price = offer_price_span.get_text(strip=True) if offer_price_span else "Not Available"
            discount_span = soup.find("span", class_="a-letter-space")
            discount_percentage = discount_span.get_text(strip=True) if discount_span else "Not Available"

            d['title'].append(title)
            d['price'].append(price)
            d['link'].append(link)
            d['rating'].append(rating)
            d['number_of_ratings'].append(number_of_ratings)
            d['items_bought_in_past_month'].append(items_bought_in_past_month)
            d['original_price'].append(original_price)
            d['discounted_price'].append(discounted_price)
            d['discount_percentage'].append(discount_percentage)

    except Exception as e:
        print(f"Error processing file {file}: {e}")

df = pd.DataFrame(data=d)
df.to_csv("data/data.csv", index=False)
print("CSV file saved to data/data.csv")
