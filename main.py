import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

url: str = ("https://www.time.ir/")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get(url=url)

driver.find_element(By.XPATH,
                    '//*[@id="ctl00_cphTop_Sampa_Web_View_EventUI_EventCalendarSimple30cphTop_3732_ecEventCalendar_lblHeaderDates"]/span[2]').click()
driver.find_element(By.XPATH,
                    '//*[@id="ctl00_cphTop_Sampa_Web_View_EventUI_EventCalendarSimple30cphTop_3732_ecEventCalendar_txtYearSelected"]').send_keys(
    '1395')
driver.find_element(By.XPATH,
                    '//*[@id="ctl00_cphTop_Sampa_Web_View_EventUI_EventCalendarSimple30cphTop_3732_ecEventCalendar_btnOk"]').click()
time.sleep(5)

shamsi_list = []
miladi_list = []
ghamari_list = []
is_holiday_list = []
monasebat_list = []
year_shamsi_list = []
month_shamsi_list = []
year_month_miladi_list = []
year_month_ghamari_list = []

while True:
    monasebat_list_temp = []
    monasebat_day_temp = []
    for i in driver.find_elements(By.XPATH, '//li[@class="eventHoliday "]'):
        monasebat_day_temp.append(i.text.split(' ')[0])
        monasebat_list_temp.append(' '.join(i.text.split(' ')[1:]))

    for i in driver.find_elements(By.XPATH,
                                  '//div[@class="mainCalendar"]/div[@class="dayList"]/div[@class=(" " or "today") and @class!= "spacer disabled"]'):
        child_class = i.find_element(By.XPATH, './/div').get_attribute('class')
        if child_class == ' holiday' or child_class == 'holiday':
            is_holiday_list.append(1)
        else:
            is_holiday_list.append(0)
        shamsi_list.append(i.text.split('\n')[0])
        try:
            monasebat_list.append(monasebat_list_temp[monasebat_day_temp.index(i.text.split('\n')[0])])
        except:
            monasebat_list.append(None)

        miladi_list.append(i.text.split('\n')[1])
        ghamari_list.append(i.text.split('\n')[2])
        year_month_shamsi_miladi_ghamari = driver.find_element(By.XPATH,'//*[@id="ctl00_cphTop_Sampa_Web_View_EventUI_EventCalendarSimple30cphTop_3732_ecEventCalendar_lblHeaderDates"]').text.split('\n')
        month_shamsi_list.append(year_month_shamsi_miladi_ghamari[0].split(' ')[0])
        year_shamsi_list.append(year_month_shamsi_miladi_ghamari[0].split(' ')[1])
        year_month_miladi_list.append(year_month_shamsi_miladi_ghamari[1])
        year_month_ghamari_list.append(year_month_shamsi_miladi_ghamari[3])

    driver.find_element(By.XPATH,'//*[@id="ctl00_cphTop_Sampa_Web_View_EventUI_EventCalendarSimple30cphTop_3732_ecEventCalendar_pnlNext"]').click()
    time.sleep(3)

df = pd.DataFrame({
    'year_shamsi':year_shamsi_list,
    'month_shamsi':month_shamsi_list,
    'day_shamsi':shamsi_list,
    'is_holiday':is_holiday_list,
    'monasebat':monasebat_list,
    'day_miladi':miladi_list,
    'year_month_miladi':year_month_miladi_list,
    'day_ghamari': ghamari_list,
    'year_month_ghamari': year_month_ghamari_list,
})

df.to_excel('time_ir.xlsx')