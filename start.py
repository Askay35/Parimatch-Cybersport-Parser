from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from os import system
import json
import time

opt = webdriver.ChromeOptions()
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_experimental_option("excludeSwitches", ["enable-automation"])
opt.add_experimental_option('useAutomationExtension', False)
opt.add_argument("--start-maximized")
opt.add_argument('--disable-extensions')
opt.add_argument('--profile-directory=Default')
opt.add_argument("--incognito")
opt.add_argument("--disable-plugins-discovery")
opt.add_experimental_option('excludeSwitches', ['enable-logging'])

opt.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

parimatch_url = "https://www.parimatch.ru/ru/e-sports/0-12"

driver = webdriver.Chrome(executable_path='chromedriver.exe', options=opt)
driver.delete_all_cookies()
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

event_class = 'b3_b5'

# event_title_class = 'gr_aj'
# cb_label_class = 'p5_p n7_n9'
# checkbox_class = 'p5_p7'


match_class = 'jr_jx'


# team_name_class = 'styles_name__2QIKf'

# out_container_class = 'styles_wrapper__ivXub'
# total_container_class = 'styles_wrapper__3d_dg'
# result_container_class = 'styles_row__1lIdZ'

# out_value_class = 'styles_title__303MO'
# out_coef_class = 'styles_value__1V_3B'

def waitToElem(to, elemclass):
    try:
        WebDriverWait(driver, to).until(ec.visibility_of_element_located((By.CLASS_NAME, elemclass)))
        return True
    except:
        return False


def clickByScript(elem):
    driver.execute_script("arguments[0].click();", elem)


def getUrls():
    driver.delete_all_cookies()
    driver.get(parimatch_url)

    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, event_class)))
    print("events found")

    last_y = driver.execute_script('return document.getElementById("line-holder").scrollTop')

    urls = []

    while (True):
        driver.execute_script(
            'let el = document.getElementById("line-holder");el.scroll({top:el.scrollTop+el.scrollHeight-el.scrollTop+1000,left:0,behavior:"smooth"});')

        time.sleep(1)

        y = driver.execute_script('return document.getElementById("line-holder").scrollTop')

        for m in driver.find_elements_by_xpath(
                '//div[@class="' + match_class + '"]/a[@data-id="event-card-container-event"]'):
            urls.append(m.get_attribute('href'))
            time.sleep(0.1)

        if y == last_y:
            break
        else:
            last_y = y

    out = []
    for i in urls:
        if i not in out:
            out.append(i)

    return out


def dictToJson(filename, array):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(array, file, ensure_ascii=False)


baseurl = 'https://parimatch.ru'

# def parseEvents(events):
#     matches_urls = []
#     WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, match_class)))
# ev = 0
# for event in events:
#     ev = ev + 1
#     print("event "+str(ev))
#     print(event)
#     event_matches = event.find_elements_by_class_name(match_class)
#     time.sleep(2)
#     if len(event_matches) > 0:
#         print("event matches count > 0")
#         for match in event_matches:
#             a = match.find_elements_by_xpath('.//a[@data-id="event-card-container-event"]')
#             if len(a) > 0:
#                 print('url added')
#                 matches_urls.append(a.getAttribute('href'))
#             else:
#                 print("a tag wasn't found")
#
# team_names = match.find_elements_by_class_name(team_name_class)
# if len(team_names) < 2:
#     print("team names count < 2")
#     continue
#
# print("team names count >= 2 ")
#
# m = {}

# m['event'] = event.find_elements_by_class_name(event_title_class)[0].text
#
# m['team1'] = team_names[0].text
# m['team2'] = team_names[1].text
#
# m['coefficients'] = {
#     "win":{},
#     "out":{
#         "p1":{},
#         "p2":{}
#     },
#     "total":{
#         "over":{},
#         "under": {},
#     }
# }
#
#
# result_container = match.find_elements_by_class_name(result_container_class)

# if len(result_container) > 0:
#     print("result container count > 0")
#     result_items = result_container[0].find_elements_by_class_name(out_coef_class)
#     if len(result_items) > 0:
#         print("result items count > 0")
#         m['coefficients']['win']['p1'] = float(result_items[0].text)
#         if len(result_items) > 1:
#             print("result items count > 1")
#             m['coefficients']['win']['p2'] = float(result_items[1].text)
#
# out_container = match.find_elements_by_class_name(out_container_class)
# if len(out_container) > 0:
#     print("out container count > 0")
#     out_values = out_container[0].find_elements_by_class_name(out_value_class)
#     out_coef = out_container[0].find_elements_by_class_name(out_coef_class)
#     if len(out_values) > 0:
#         print("out values count > 0")
#         m['coefficients']['out']['p1'][out_values[0].text] = float(out_coef[0].text)
#         if len(out_values) > 1:
#             m['coefficients']['out']['p2'][out_values[1].text] = float(out_coef[1].text)
#             if len(out_values) > 2:
#                 m['coefficients']['out']['p1'][out_values[2].text] = float(out_coef[2].text)
#                 if len(out_values) > 3:
#                     m['coefficients']['out']['p2'][out_values[3].text] = float(out_coef[3].text)
#
# total_container = match.find_elements_by_class_name(total_container_class)
# if len(total_container) > 0:
#     total_values = total_container[0].find_elements_by_class_name(out_value_class)
#     total_coef = total_container[0].find_elements_by_class_name(out_coef_class)
#     if len(total_values) > 0:
#         m['coefficients']['total']['over'][total_values[0].text] = float(total_coef[0].text)
#         if len(total_values) > 1:
#             m['coefficients']['total']['under'][total_values[1].text] = float(total_coef[1].text)
#             if len(total_values) > 2:
#                 m['coefficients']['total']['over'][total_values[2].text] = float(total_coef[2].text)
#                 if len(total_values) > 3:
#                     m['coefficients']['total']['under'][total_values[3].text] = float(total_coef[3].text)
#
# matches['games'].append(m)

# return matches_urls

result_container_xpath = '//div[contains(@class, "m7_p")]'

outcome_xpath = './/*[@data-id="outcome"]'

coef_xpath = './/span[@class="un_up"]'

result_title_xpath = './/div[@class="mz_p"]/span'

win_title = 'Победитель'

match_result_title = 'Результат матча'

total_title = 'Тотал'

out_title = 'Фора'


def parseUrl(url):
    print(f"parsing url {url}")
    driver.get(url)
    time.sleep(5)

    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, result_container_xpath)))

    result_containers = driver.find_elements_by_xpath(result_container_xpath)

    if len(result_containers) < 1:
        print("no result containers")
        return False

    match = {
        "coefficients": {
            "result": {
                "p1": 0,
                "draw": 0,
                "p2": 0
            },
            # "out": [],
            # "total": {
            #     "over": [],
            #     "under": []
            # }
        }
    }
    teams = driver.find_elements_by_xpath('//div[@data-id="prematch-infoboard-competitor"]')
    match['team1'] = teams[0].text
    match['team2'] = teams[1].text

    event_name = driver.find_element_by_xpath('//div[@data-id="heading-bar-title"]')
    match['event'] = event_name.text

    for rc in result_containers:
        r_title_el = rc.find_elements_by_xpath(result_title_xpath)
        if len(r_title_el) > 0:
            r_title = r_title_el[0].text
            if match['coefficients']['result']['p1'] == 0 and r_title == win_title:
                print("title = win")
                win_results = rc.find_elements_by_xpath(coef_xpath)
                if len(win_results) > 0:
                    print("win results found")
                    match['coefficients']['result']['p1'] = float(win_results[0].text)
                    match['coefficients']['result']['p2'] = float(win_results[1].text)
                else:
                    print("win results not found")
            # if len(match['coefficients']['out']) and r_title == out_title:
            elif match['coefficients']['result']['p1'] == 0 and r_title == match_result_title:
                print("title = result")
                match_results = rc.find_elements_by_xpath(coef_xpath)
                if len(match_results) > 0:
                    print("match results found")
                    match['coefficients']['result']['p1'] = float(match_results[0].text)
                    match['coefficients']['result']['draw'] = float(match_results[1].text)
                    match['coefficients']['result']['p2'] = float(match_results[2].text)
                else:
                    print("match results not found")
            else:
                print("title = " + r_title)
                match['coefficients'][r_title] = []
                total_res = rc.find_elements_by_xpath('.//div[@class="xp_tj xp_u9"]')
                if len(total_res) < 1:
                    out_results = rc.find_elements_by_xpath(outcome_xpath)
                    for out in out_results:
                        kv = t.text.replace('\n', ' ').split(' ')
                        match['coefficients'][r_title].append({'key':' '.join(kv),'value':kv[-1]})
                else:
                    for t in total_res:
                        total = t.text.replace('\n', ' ').split(' ')
                        match['coefficients'][r_title].append({'value':total[0],'over':total[1],'under':total[2]})

    print(match)

    return match


def parseUrls(urls):
    matches = []
    p = 0
    for url in urls:
        matches.append(parseUrl(url))
        p += 1
        if p > 0:
            break

    return matches


if __name__ == '__main__':
    urls = getUrls()
    matches = parseUrls(urls)
    dictToJson("res.json", matches)  # - вывод в json
    driver.close()
    system("taskkill /IM chromedriver.exe /f")
