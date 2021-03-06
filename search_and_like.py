from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# element에서 method로 string을 찾을 때까지 대기하는 함수 생성
# element: 대상 element
# method: css_selector, xpath 등
# string: 각 method에 맞는 형태의 string
def wait_for(element, method, string):
    if method == "CSS_SELECTOR":

        # element에서 CSS_SELECTOR로 string을 찾을 때까지 10초 대기
        WebDriverWait(element, 10).until(
            EC.visibility_of_element_located((
            By.CSS_SELECTOR, string)))
        # 찾은 element가 복수 개인 경우
        if len(element.find_elements(By.CSS_SELECTOR, string)) > 1:
            result = element.find_elements(By.CSS_SELECTOR, string)
        # 찾은 element가 한 개 뿐인 경우
        else:
            result = element.find_elements(By.CSS_SELECTOR, string)[0]

    elif method == "XPATH":
        WebDriverWait(element, 10).until(
            EC.visibility_of_element_located((
            By.XPATH, string)))
        if len(element.find_elements(By.XPATH, string)) > 1:
            result = element.find_elements(By.XPATH, string)
        else:
            result = element.find_elements(By.XPATH, string)[0]
    elif method == "TAG_NAME":
        WebDriverWait(element, 10).until(
            EC.visibility_of_element_located((
            By.TAG_NAME, string)))
        if len(element.find_elements(By.TAG_NAME, string)) > 1:
            result = element.find_elements(By.TAG_NAME, string)
        else:
            result = element.find_elements(By.TAG_NAME, string)[0]
    elif method == "CLASS_NAME":
        WebDriverWait(element, 10).until(
            EC.visibility_of_element_located((
            By.CLASS_NAME, string)))
        if len(element.find_elements(By.CLASS_NAME, string)) > 1:
            result = element.find_elements(By.CLASS_NAME, string)
        else:
            result = element.find_elements(By.CLASS_NAME, string)[0]
    elif method == "NAME":
        WebDriverWait(element, 10).until(
            EC.visibility_of_element_located((
            By.NAME, string)))
        if len(element.find_elements(By.NAME, string)) > 1:
            result = element.find_elements(By.NAME, string)
        else:
            result = element.find_elements(By.NAME, string)[0]
    else:
        return
    return result


ID = str(input("ID를 입력하세요: "))
PW = str(input("비밀번호를 입력하세요: "))
SEARCING_KEYWORD = str(input("검색 키워드를 입력하세요: "))

#화면 띄우기
instagram = "https://instagram.com"
driver = webdriver.Chrome('./chromedriver.exe')
driver.get(instagram)
time.sleep(2)

#Login ID 입력하기
login_id = wait_for(driver, "NAME", "username")
login_id.send_keys(ID)

#Login PW 입력하기
login_pw = wait_for(driver, "NAME", "password")
login_pw.send_keys(PW)
login_pw.send_keys(Keys.RETURN)
time.sleep(3)

# 첫 번째 팝업 지우기
popup_css = "#react-root > section > main > div > div > div > div > button"
popup = wait_for(driver, "CSS_SELECTOR", popup_css)
popup.send_keys(Keys.ENTER)
time.sleep(1)

# 두 번째 팝업 지우기
popup_css = "body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm"
popup = wait_for(driver, "CSS_SELECTOR", popup_css)
popup.send_keys(Keys.ENTER)
time.sleep(1)

driver.get(f"{instagram}/explore/tags/{SEARCING_KEYWORD}")
current_articles_css = "#react-root > section > main > article > div:nth-child(3) > div > div > div"
like_subjects = list()
subject_css = "body > div._2dDPU.CkGkG > div.zZYga > div > article > div > div.UE9AK > div > header > div.o-MQd > div.PQo_0 > div.e1e1d > span > a"
x_btn_css = "body > div._2dDPU.CkGkG > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button"

current_articles = wait_for(driver, "CSS_SELECTOR", current_articles_css)
for article in current_articles:
    article = wait_for(article, "TAG_NAME", "a")
    article.send_keys(Keys.ENTER)
    subject = wait_for(driver, "CSS_SELECTOR", subject_css)
    like_subjects.append(subject.text)
    x_btn = wait_for(driver, "CSS_SELECTOR", x_btn_css)
    x_btn.send_keys(Keys.ENTER)
    print("subject added.")
    time.sleep(1)

articles_css = "#react-root > section > main > div > div._2z6nI > article > div > div > div > div > a"
like_btn_css = "body > div._2dDPU.CkGkG > div.zZYga > div > article > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm > div > div > section.ltpMr.Slqrh > span.fr66n > button"
x_btn_css = "body > div._2dDPU.CkGkG > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button"
subject_done_num = 0
for subject in like_subjects:
    driver.get(f"{instagram}/{subject}")
    articles = wait_for(driver, "CSS_SELECTOR", articles_css)
    like_num = 0
    for article in articles[:9]:
        article.send_keys(Keys.ENTER)
        like_btn = wait_for(driver, "CSS_SELECTOR", like_btn_css)
        if like_btn.find_elements(By.XPATH, "div/span/*[name()='svg'][@aria-label='좋아요']") != []:
            like_btn.send_keys(Keys.ENTER)
            like_num += 1
            print(f"좋아요 완료: {like_num}/{len(articles[:9])}")
        x_btn = wait_for(driver, "CSS_SELECTOR", x_btn_css)
        x_btn.send_keys(Keys.ENTER)
        time.sleep(1)
    subject_done_num += 1
    print(f"한 대상 좋아요 전체 완료: {subject_done_num}/{len(like_subjects)}")

