from requests import get
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#-----------------------------------------

def buy(api_key):
    url = 'https://sms-activate.ru/stubs/handler_api.php'
    country = '2'
    service = 'ig'
    payload = {
        'api_key':api_key,
        'action':'getNumber',
        'service':service,
        'country':country
    }
    res = get(url, params=payload)
    id = res.text.split(':')[1]
    phone = res.text.split(':')[2]
    set_status(api_key, id, '1')

    return id, phone

def set_status(api_key, id, status):
    url = 'https://sms-activate.ru/stubs/handler_api.php'
    payload = {
        'api_key':api_key,
        'action':'setStatus',
        'id':id,
        'status':status,
    }
    get(url, params=payload)

def get_code(api_key, id):
    url = 'https://sms-activate.ru/stubs/handler_api.php'
    payload = {
        'api_key':api_key,
        'action':'getStatus',
        'id':id,
    }
    res = get(url, params=payload).text.split(':')
    while(res[0] == 'STATUS_WAIT_CODE'):
        res = get(url, params=payload).text.split(':')
    if(res[0] == 'STATUS_OK'):
        set_status(api_key, id, '6')
        return res[1]

#-----------------------------------------

api_key = '' #api ключ для sms-activate

#технические данные
url = 'https://www.instagram.com/accounts/emailsignup' #адрес сайта
t = 2 #время задержки загрузки

#данные для регистрации
names = [''] #список имён
nicks = [''] #список ников
passwords = [''] #список паролей
years = [''] #список годов рождения
months = [''] #список месяцев рождения
days = [''] #список дней рождения

#код
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r'G:\Programming\Python\chromedriver.exe', options=chrome_options)
driver.get(url)

#----------------------------------------- 1 страница
sleep(t)
id, phone = buy(api_key)
driver.find_element_by_xpath("//input[@type='text'][@name='emailOrPhone']").send_keys(phone) # ввод номера телефона
driver.find_element_by_xpath("//input[@type='text'][@name='fullName']").send_keys(names[randint(0, len(names)-1)]) #ввод имени
driver.find_element_by_xpath("//input[@type='text'][@name='username']").send_keys(nicks[randint(0, len(nicks)-1)]) #ввод ника
driver.find_element_by_xpath("//input[@type='password'][@name='password']").send_keys(passwords[randint(0, len(passwords)-1)]) #ввод пароля
driver.find_element_by_xpath("//button[@type='submit'][@class='sqdOP  L3NKy   y3zKF     ']").click() #нажатие кнопки 'Далее'

#----------------------------------------- 2 страница

sleep(t)
year = driver.find_element_by_xpath("//select[@class='h144Z  '][@title='Год:']")
for option in year.find_elements_by_tag_name("option"):
    if(option.get_attribute("value") == years[randint(0, len(years)-1)]):
        option.click()
        break

month = driver.find_element_by_xpath("//select[@class='h144Z  '][@title='Год:']")
for option in month.find_elements_by_tag_name("option"):
    if(option.get_attribute("value") == months[randint(0, len(months)-1)]):
        option.click()
        break

day = driver.find_element_by_xpath("//select[@class='h144Z  '][@title='Год:']")
for option in day.find_elements_by_tag_name("option"):
    if(option.get_attribute("value") == days[randint(0, len(days)-1)]):
        option.click()
        break

driver.find_element_by_xpath("//button[@type='button'][@class='sqdOP  L3NKy _4pI4F  y3zKF     ']").click() #нажатие кнопки 'Далее'

#----------------------------------------- 3 страница

sleep(t)
code = get_code(api_key, id)
driver.find_element_by_xpath("//input[@type='tel'][@name='confirmationCode']").send_keys(code) #ввод кода верификации номера телефона
driver.find_element_by_xpath("//button[@type='button'][@class='sqdOP  L3NKy   y3zKF     ']").click() #нажатие кнопки 'Подтвердить'

#----------------------------------------- конец

driver.close()
driver.quit()