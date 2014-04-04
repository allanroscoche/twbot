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
aldeias = ["33110","23255"]
tropa_farm = 5


muralhas = []
url_base = "http://br56.tribalwars.com.br/game.php?village="


def doMuralhas(driver):
    url_p1 = "http://br56.tribalwars.com.br/game.php?village="+aldeia[0]+"&target="
    url_p2 = "&screen=place"
    for aldeia in muralhas:
        url = aldeia.strip()
        driver.get(url_p1+url+url_p2)
        barbaros = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "unit_input_axe")))
        barbaros.send_keys("30")
        arietes = driver.find_element_by_id("unit_input_ram")
        arietes.send_keys("5")
        explorador = driver.find_element_by_id("unit_input_spy")
        explorador.send_keys("1")
        submit = driver.find_element_by_id("target_attack")
        submit.click()
        ataque = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "troop_confirm_go")))
        ataque.click()


def nivel_muralha(farm):
    id_aldeia = farm.find_element_by_xpath("../../td[4]").text
    nivel_muralha = int(farm.find_element_by_xpath("../../td[7]").text)
    if (nivel_muralha > 1):
        muralhas.append(farm.get_attribute("onclick").split(",")[1])
        print id_aldeia, "muralha nivel", nivel_muralha
        muralhas.append(id_aldeia)
    return nivel_muralha



def doFarm(driver):
        muralhas = []
        url_farm = url_base + aldeia + "&screen=am_farm"
        driver.get(url_farm)
        uri = driver.current_url+"&Farm_page="
        abas = len(driver.find_elements_by_class_name("paged-nav-item"))+1
        nome_aldeia = driver.find_element_by_id("menu_row2_village").text
        for i in range(0,abas):
            print "Farmando aba",i+1, "na aldeia", nome_aldeia
            driver.get(uri+`i`)
            farm_table =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "am_widget_Farm")))
            # Verificacao do Capcha
            if (len(farm_table.find_elements_by_id("bot_check_image"))>0) :
                print "Bot Checker!"
                exit()
            for farm in farm_table.find_elements_by_class_name("farm_icon_b"):
                attack = len(farm.find_elements_by_xpath("../../td[4]/img"))
                if(attack == 0):
                    if ((re.search("disabled",farm.get_attribute("class"))) is None):
                        if (nivel_muralha(farm) < 3) :
                            cls=int(driver.find_element_by_id("light").text)
                            if(cls < tropa_farm):
                                print "faltam tropas"
                                return False
                            result = driver.execute_script(farm.get_attribute("onclick"))
                            doFarm.count += 1
                            time.sleep(1)
                    else :
                        print "sem tropas"
                        return False
        #print len(muralhas)," aldeias com muralha elevada"
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

if (len(driver.find_elements_by_id("bot_check_image"))>0) :
    print "Bot! Fudeu!"
    exit()

inf=1
while inf==1:
    doFarm.count = 0
    for aldeia in aldeias:
        doFarm(driver)
        #doMuralhas(driver)
    print "Enviados ", doFarm.count, " ataques"
    driver.get("http://br56.tribalwars.com.br/game.php?village=33110&screen=info_player")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "stats")))
    novo_farm = driver.execute_script("return StatsWidget.stats.looted_res")
    print "Farm do dia ", novo_farm[0][1]
    wait()
