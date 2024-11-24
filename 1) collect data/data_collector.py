from selenium import webdriver
from selenium.webdriver.common.by import By
import os

def get_valid_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit() and int(user_input) > 0:
            return int(user_input)
        else:
            print("Invalid input! Please enter a valid positive integer.")

product = input("Enter the product you want to search: ").strip()
max_pages = get_valid_input("Enter the number of pages to scrape (e.g., 20): ")
driver = webdriver.Chrome()

output_dir = os.path.join("data", "html_data")
os.makedirs(output_dir, exist_ok=True)

file = 0

try:
    for i in range(1, max_pages + 1):
        search_url = f"https://www.amazon.in/s?k={product.replace(' ', '+')}&page={i}"
        driver.get(search_url)

        elems = driver.find_elements(By.CLASS_NAME, "puis-card-container")

        print(f"{len(elems)} items found on page {i}")

        for elem in elems:
            file_path = os.path.join(output_dir, f"{product}_{file}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(elem.get_attribute("outerHTML"))
            print(f"Saved HTML to {file_path}")
            file += 1
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
    print("Scraping complete. Driver closed.")
