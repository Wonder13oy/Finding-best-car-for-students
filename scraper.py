from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as req


# csv to save data to
filename = 'dataset/car_prices.csv'
file = open(filename, 'w')

headers = 'brand, model, year, mileage, price, fee per month\n'
file.write(headers)

for i in range(13):

    my_url = f'https://www.imperialauto.co.za/search?pricefrom=0&priceto=200000&page={i+1}&keywords=&used=true&new=true&demo=true&petrol=false&diesel=false&pricedtogo=false&manual=false&automatic=false&yearfrom=2002&yearto=2019&monthlyrepaymentfrom=0&monthlyrepaymentto=3500&mileagefrom=0&mileageto=0&showmakeslider=false&firstload=true&colour=&vehicle_value=r0+-+r200000&est_monthly_repayment=r0+-+r3500&vehicle_value=r0+-+r200000&est_monthly_repayment=r0+-+r3500&vehicle_value=r0+-+r200000&est_monthly_repayment=r0+-+r3500&vehicles_type_filter=used&vehicles_type_filter=demo&resultsperpage=60&sortby=pricelow'

    # connection
    client = req(my_url)
    page_html = client.read()
    client.close()

    # html parser
    page_soup = soup(page_html, 'html.parser')

    # getting each car
    containers = page_soup.findAll('div', {"class": "vehicle-container"})

    for container in containers:
        brand_name = container.h3.text.split(' ')
        brand = brand_name[0]
        model = brand_name[1]
        price = container.find('div', {"class": "now"}).text

        if container.span == None:
            continue
            
        mileage_year =  container.span.text.split('|')
        year = mileage_year[0]
        mileage = mileage_year[1]
        
        fee_pm =  container.find('div', {"class": "per-month-value"}).text

        file.write(f'{brand}, {year},{mileage}, {price},{fee_pm}\n')

    print(i+1)

file.close()