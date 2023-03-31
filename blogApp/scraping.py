import requests
from bs4 import BeautifulSoup


def get_panels():
    html_text_ebay=requests.get('https://www.ebay.com/sch/i.html?_fsrp=1&_from=R40&_nkw=solar%20panel&_sacat=0&Wattage=200%252D299%2520W%7C300%252D399%2520W%7C500%252D599%2520W%7C600%252D699%2520W%7C700%252D799%2520W%7C800%252D899%2520W%7C900%252D999%2520W%7C1000%252D1499%2520W&_sop=15&Type=Solar%2520Panel&_dcat=41981&LH_ItemCondition=1000&rt=nc&_udlo=10').text
    soup_ebay = BeautifulSoup(html_text_ebay,'lxml')
    panels_ebay = soup_ebay.find_all('li',class_='s-item s-item__pl-on-bottom s-item--watch-at-corner')
    
    panel_titles=[]
    panel_prices=[]
    panel_links=[]
    data={}
    for panel in panels_ebay:
        panel_title= panel.find('h3',class_='s-item__title').text
        panel_titles.append(panel_title)

        panel_price=panel.find('span','s-item__price').text.replace('$','').replace(',','')
        panel_prices.append(float(panel_price))

        post_link=panel.a['href']
        panel_links.append(post_link)
        
    html_text_walmart=requests.get('https://www.europe-solarstore.com/solar-panels.html?dir=asc&limit=all&order=price').text
    soup_walmart = BeautifulSoup(html_text_walmart,'lxml')

    panels_walmart = soup_walmart.find_all('li','item')

    for panel in panels_walmart:
        panel_title= panel.find('h2',class_='product-name').text
        panel_titles.append(panel_title)

        panel_price=panel.find('span','regular-price').text.replace("€",'').strip('\n').replace(',','')
        panel_prices.append(float(panel_price))

        post_link=panel.a['href']
        panel_links.append(post_link)
        
        
    data['panel_titles']=panel_titles
    data['panel_prices']=panel_prices
    data['panel_links']=panel_links
    
    return data
