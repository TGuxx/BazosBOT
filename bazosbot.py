import requests
from bs4 import BeautifulSoup
import pandas as pd 
import time
import smtplib

counter = 0
tmp_list = []

#SPACER
def clear_line():
    for i in range(1,5):
        print('')
           
print('************************************************************')
print('* ____           __________   _____    ____   ____ _______ *')
print('*|  _ \   /\    |___  / __ \ / ____|  |  _ \ / __ \__   __|*')
print('*| |_) | /  \      / / |  | | (___    | |_) | |  | | | |   *')   
print('*|  _ < / /\ \    / /| |  | |\___ \   |  _ <| |  | | | |   *')   
print('*| |_) / ____ \  / /_| |__| |____) |  | |_) | |__| | | |   *')   
print('*|____/_/    \_\/_____\____/|_____/   |____/ \____/  |_|   *')  
print('*                                                          *')
print('*                    [For GPU SCOUTING]                    *')
print('************************************************************')
print('')
print('CTRL+C to terminate the script')
print('')

#SETUP 
refresh = input('REFRESH (secs/enter=60s): ')
if refresh == '':   
    refresh = 60
    
alert_opt = input("Do you wish to get email alerts?  (y/n): ")

if (alert_opt == 'y') or (alert_opt == 'Y'):
    email = input("Enter your E-mail (gmail only!): ")
    password = input("Enter password for your : ")
    
else:
    pass

component = 'graficka';
cena_od = input('CENA OD: ')
cena_do = input('CENA DO: ') 
baseurl = f"https://pc.bazos.sk/{component}/?hledat=&rubriky=pc&hlokalita=&humkreis=25&cenaod={cena_od}&cenado={cena_do}&Submit=H%C4%BEada%C5%A5&kitx=ano"    

baseurl_test = "https://pc.bazos.sk/"+component+"/?hledat=&rubriky=pc&hlokalita=&humkreis=25&cenaod="+cena_od+"&cenado="+cena_od+"&Submit=H%C4%BEada%C5%A5&kitx=ano"    

#EMAIL SENDING
def send_alert():
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(email,password)
    mail.sendmail(email,email,ALERT)
    mail.close()   
    print("******** EMAIL WAS SENT ********")
    
#HEADERS
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
        
        name =  item.find('h2',class_='nadpis').text.strip()
        price = item.find('div',class_='inzeratycena').text.strip()
        date =  item.find('span',class_='velikost10').text.strip()
        link = item.find('a').text.strip()
    
        GPU = {
                     
            'COMPONENT':name,
            'date':date,
            'CENA':price,       
            }
        
        GPU_list.append(GPU)
        
    if GPU_list != tmp_list: 
        if (alert_opt == 'y') or (alert_opt == 'Y'):
             if (alerts == 0):
      
                ALERT = "BAZOSBOT activated and WORKING!"    
                send_alert()                
             else:
                 ALERT = "Market change detected!"             
                 alerts += 1
                 send_alert()
      
    tmp_list = GPU_list
 
    df = pd.DataFrame(GPU_list)
    print(65*'*')
    print()
    print(df)
    print()
    print(65*'*')
    time.sleep(int(refresh))     
