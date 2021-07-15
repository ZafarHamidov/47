import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
from security import YOUR_SMTP_ADDRESS, YOUR_EMAIL, YOUR_PASSWORD


# URL1 = "https://www.amazon.com/AmazonBasics-Security-Safe-0-5-Cubic-Feet/dp/B00UG9HB1Q/ref=sr_1_1?dchild=1&keywords=amazonbasics&pd_rd_r=e115afac-3a61-4214-804f-f796ff621e2a&pd_rd_w=CWThp&pd_rd_wg=79tXY&pf_rd_p=9349ffb9-3aaa-476f-8532-6a4a5c3da3e7&pf_rd_r=W7FN6E65J2BER5HE4NJJ&qid=1626341048&sr=8-1"
URL = "https://www.citilink.ru/product/klaviatura-a4-bloody-b930-usb-chernyi-1010866/"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(URL, headers=header)

soup = BeautifulSoup(response.content, "lxml")
# print(soup.prettify())

price = soup.find(class_="ProductHeader__price-default_current-price").getText().strip()
price_without_currency = price.split("₽")[0]
price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.find(name="h1", class_="Heading Heading_level_1 ProductHeader__title").getText().strip()
print(title)

BUY_PRICE = 17000
if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"
    
    with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
        connection.sendmail(
            from_addr=YOUR_EMAIL,
            to_addrs=YOUR_EMAIL,
            msg=f"Цена подешевела!\n\n{message}\n{URL}".encode('utf-8').strip()
        )




