import json
import requests
import yfinance as yf
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('./config.json') as f:
    data = json.load(f)
    for c in data['config']:
        print('Webhook: ' + c['webhook'])

header= {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
url = "https://leolithium.com/investor-centre/asx-announcements/"

r = requests.get(url, headers=header, timeout=5)

#Predefine variables
link_text_old = ""
link_url_old = ""



# Initialize Webdrive
while r.status_code == 200:
    driver = webdriver.Chrome()
    driver.get(url)

# Wait for elements to load
    wait = WebDriverWait(driver, 10)
    announcement_date_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "investi-announcement-date")))
    announcement_link_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href^="https://www.investi.com.au/api/announcements/"]')))

# Get Data
    link_text = announcement_link_element.text
    link_url = announcement_link_element.get_attribute("href")
    announcement_date = announcement_date_element.text

#Close Webdriver
    driver.quit()
    
    if link_text == link_text_old:
        print("No Change")
    else:
        print("Link Text:", link_text)
        print("Link URL:", link_url)
        
        stock = yf.Ticker('LLL.AX')
        current_price = json.dumps(stock.info['currentPrice'])
        print(current_price + " AUD")
        
        
    #Initialize Webhook
        content=""
        webhook = DiscordWebhook(url=c['webhook'], username='LLL:ASX', content=content)
        embed = DiscordEmbed(title=link_text, color=242424, url=url)
        embed.set_footer(text="")
        embed.set_timestamp()
        embed.add_embed_field(name="Current Price", value=f'{current_price} AUD', inline=False)
        embed.add_embed_field(name="Attached document", value=link_url, inline=False)
        embed.add_embed_field(name="Date", value=announcement_date, inline=False)
        embed.set_image(url="https://leolithium.com/wp-content/uploads/LeoLithiumRegisteredLogoRetina.png")
        
        webhook.add_embed(embed)
        response = webhook.execute()
        
        link_text_old = link_text
        
    sleep(60)    
else:
    print("Data not available")

    
    