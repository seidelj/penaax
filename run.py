import calendar
from selenium import webdriver
from models import Session, Game, LookupDate
from pyvirtualdisplay import Display
from sqlutils import get_or_create
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

display = Display(visible=0, size=(800,600))
display.start()


session = Session()
_URL = "http://www.milb.com/scoreboard/index.jsp?cid=&lid=111&org=&sc=&sid=milb&t=league&ymd="

# p.errmsg "There are no games scheduled for this league on July 19, 2016. Please select another date."

def find_game_tables(browser):
    tables = browser.find_elements_by_tag_name("table")
    tIds = []
    for table in tables:
        if "_penaax_" in table.get_attribute("id"): tIds.append(table.get_attribute("id"))
    return tIds

def parse_row(row):
    location = row.get_attribute('class')
    team = row.find_element_by_class_name('team_info').find_element_by_class_name('a').text
    runs = row.find_element_by_class_name('runs').text

    return dict(location=location, team=team, runs=runs)

def main():
    browser = webdriver.Firefox()
    wait = WebDriverWait(browser, 10)
#This will iterate over yyyymmdd
    for date in session.query(LookupDate).filter(LookupDate.finished == 1):
        print date.yyyymmdd
        browser.get(_URL + date.yyyymmdd)
	try:
            contentDiv = wait.until(EC.presence_of_element_located((By.ID, 'sbContent')))
	except TimeoutException:
            if "There are no games scheduled" in browser.find_element_by_id('scoreboard').text: continue
        gameTableIds = find_game_tables(browser)
        for gameId in gameTableIds:
            table = browser.find_element_by_id(gameId)
            tbody = table.find_element_by_tag_name('tbody')
            tableRows = tbody.find_elements_by_tag_name('tr')
            gameInfo = []
            for tableRow in tableRows:
                gameInfo.append(parse_row(tableRow))
            game, created = get_or_create(session, Game, gameid=gameId)
            game.parse_info(gameInfo, date.yyyymmdd)
            session.commit()
        date.finished = 1
        session.commit()





if __name__ == "__main__":
    main()

display.stop()
