import requests
from bs4 import BeautifulSoup
import pandas as pd 
import time
import smtplib

counter = 0
tmp_list = []


#EMAIL LOGIN (gmail)
email =  'insert sender email here'
password = 'insert sender email password here'
receiver = 'insert receiver email address here'

#SPACER
def clear_line():
    for i in range(1,5):
        print('')

print('************************************************************')
print('* ____           __________   _____    ____   ____ _______ *')
print('*|  _ \   /\    |___  / __ \ / ____|  |  _ \ / __ \__   __|*')
print('*| |_) | /  \      / / |  | | (___    | |_) | |  | | | |   *'   )   
print('*|  _ < / /\ \    / /| |  | |\___ \   |  _ <| |  | | | |   *')   
print('*| |_) / ____ \  / /_| |__| |____) |  | |_) | |__| | | |   *')   
print('*|____/_/    \_\/_____\____/|_____/   |____/ \____/  |_|   *')  
print('*                                                          *')
print('************************************************************')
print('')


#REFRESHING
refresh = input('REFRESH (secs/enter=60s): ')
if refresh == '':   
    refresh = 60
    
      
#CATEGORY
print("PC / MOBILE / CAR: ")
cat = input(': ')


if (cat == 'PC') or (cat =='pc'):

    print("cpu / gpu / ram / mobo")
    component = input(': ')
    
    if component == 'cpu':
        component = 'procesor'
        
    if component == 'gpu':
        component = 'graficka'
        
    if component == 'ram':
       component = 'pamet'    
   
    if component == 'mobo':
        component = 'motherboard' 
        
    cena_od = input('CENA OD: ')
    cena_do = input('CENA DO: ') 
    baseurl = f"https://pc.bazos.sk/{component}/?hledat=&rubriky=pc&hlokalita=&humkreis=25&cenaod={cena_od}&cenado={cena_do}&Submit=H%C4%BEada%C5%A5&kitx=ano"    
        
     
        
if   (cat =='mobile') or (cat =='MOBILE'):
    
    print("ALL / APPLE / SAMSUNG / xx")
    component = input(': ')
    
    if (component == 'ALL') or (component == 'all'):
        component = ''
        
    if (component == 'APPLE') or (component == 'apple'):
        component = 'apple/'
        
    if (component == 'SAMSUNG') or (component == 'samsung'):
        component = 'samsung/'   
     
        
    cena_od = input('CENA OD: ')
    cena_do = input('CENA DO: ') 
    baseurl = f"https://mobil.bazos.sk/{component}?hledat=&rubriky=mobil&hlokalita=&humkreis=25&cenaod={cena_od}&cenado={cena_do}&Submit=H%C4%BEada%C5%A5&kitx=ano"
   
    
if   (cat =='car') or (cat =='CAR'):
    
    print("ALL / x / x / x")
    component = input(': ')
    
    if component == ('ALL' or 'all'):
        component = ''
        
 
    cena_od = input('CENA OD: ')
    cena_do = input('CENA DO: ') 
    baseurl = f'https://auto.bazos.sk/?hledat=&rubriky=auto&hlokalita=&humkreis=25&cenaod={cena_od}&cenado={cena_do}&Submit=H%C4%BEada%C5%A5&kitx=ano'
    
  
ALERT = f'MARKET CHANGE DETECTED/n {baseurl} '     

#EMAIL SENDING
def send_alert():
    
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(email,password)
    mail.sendmail(email,receiver,ALERT)
    mail.close()   
    print("******** EMAIL WAS SENT ********")
    

headers = {   
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

alerts = 0


while True:
    
    clear_line()
    
    GPU_list = []
    counter += 1
    
    print(f"[Updating every {refresh} seconds..]")
    print(f'[Refreshed {counter} times]')
    print(f'Alerts sent: {alerts-1}')
    print('')
    
    r = requests.get(baseurl)
    soup = BeautifulSoup(r.content, 'lxml')
 
    product_list  = soup.find_all('div',class_='inzeraty inzeratyflex')
    
    for item in product_list:
        
        name = item.find('span',class_='nadpis').text.strip()
        price = item.find('div',class_='inzeratycena').text.strip()
        date = item.find('span',class_='velikost10').text.strip()
    
        GPU = {
                     
            'COMPONENT':name,
            'date':date,
            'CENA':price,
                     
            }
        
        GPU_list.append(GPU)
        
    if GPU_list != tmp_list: 
        alerts += 1 
       
        
    tmp_list = GPU_list
 
    df = pd.DataFrame(GPU_list)
    print(65*'*')
    print()
    print(df)
    print()
    print(65*'*')
    
    time.sleep(int(refresh))     