# Import smtplib for the actual sending function
import smtplib
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import time
import re



login = "eumesmoallan"
senha = "ukkum2"
abas = 7


def doFarm():
    for farm in farm_table.find_elements_by_class_name("farm_icon_b"):
        attack = len(farm.find_elements_by_xpath("../../td[4]/img"))
        if(attack == 0):
            if ((re.search("disabled",farm.get_attribute("class"))) is None):
                cls=int(driver.find_element_by_id("light").text)
                if(cls < 5):
                    print "faltam tropas"
                    return False
                result = driver.execute_script(farm.get_attribute("onclick"))
                doFarm.count += 1
                print "enviando ataque ", doFarm.count, ", restou ", cls, " cls"
                time.sleep(1)
            else :
                print "sem tropas"
                return False
    return True
doFarm.count = 0

def wait():
    tmax = 10
    for i in range(0,tmax):
        print "farm em ",tmax-i," minutos."
        time.sleep(60)


driver = webdriver.Firefox()
driver.get("http://www.tribalwars.com.br")
print driver.title

user = driver.find_element_by_id("user")
user.send_keys(login)
password = driver.find_element_by_id("password")
password.send_keys(senha)
password.submit()


botao = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "server_select_list")))
driver.execute_script("return  Index.submit_login('server_br56');")
saque = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "manager_icon")))
saque.click()
farm_table =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "am_widget_Farm")))
uri = driver.current_url+"&Farm_page="

abas = len(farm_table.find_elements_by_class_name("paged-nav-item"))+1

inf=1
rec_farm=0
total_farm=0

while inf==1:
    doFarm.count = 0
    for i in range(0,abas):
        driver.get(uri+`i`)
        farm_table =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "am_widget_Farm")))
        if (len(farm_table.find_elements_by_id("bot_check_form"))>0) :
            exit()
        result = doFarm()
        if result is False:
            break
    print "Enviados ", doFarm.count, " ataques"
    #driver.get("http://br56.tribalwars.com.br/game.php?village=33110&screen=info_player")
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "stats")))
    #novo_farm = driver.execute_script("return StatsWidget.stats.looted_res")
    #print "Farm do dia ", novo_farm[0][1]
    #driver.get("http://br56.tribalwars.com.br/game.php?village=33110&screen=overview")
    wait()
