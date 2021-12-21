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
    else:
        return
    return result


ID = input("ID를 입력하세요: ") #인스타그램 ID
PW = input("비밀번호를 입력하세요: ") #인스타그램 PW

#화면 띄우기
instagram = "https://instagram.com"
driver = webdriver.Chrome('./chromedriver.exe')
driver.get(instagram)

#로딩하는 시간 기다리기
time.sleep(2)

#Login ID 속성값 찾고 입력하기
login_id = driver.find_element_by_name('username')
login_id.send_keys(ID)

#Login PW 속성값 찾기 입력하기
login_pw = driver.find_element_by_name('password')
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

# 게시글 dictionary 생성
article_dict = {}
# 게시글 키 변수 생성
key = 0
# 좋아요 횟수 변수 생성
like_cnt = 0

# 좋아요를 N번 하거나 게시글을 M개 조회할 때까지 반복
while True:

    # 현재 화면의 게시글 불러오기
    articles = wait_for(driver, "TAG_NAME", "article")

    # 좋아요 영역의 class명
    like_div_class = "fr66n"

    # 현재 화면의 게시글마다 반복
    for article in articles:

        # 게시글이 게시글 dictionary에 없는 경우
        if article not in article_dict.values():
            # 키 +1 및 dictionary에 추가
            key += 1
            article_dict[key] = article

            # 해당 게시글로 스크롤 이동
            driver.execute_script("arguments[0].scrollIntoView();", article_dict[key])
            print(f"{key}번째 게시글을 조회함")
            time.sleep(2)

            # 좋아요 버튼 element 불러오기
            like_div = wait_for(article_dict[key], "CLASS_NAME", like_div_class)
            like_btn = wait_for(like_div, "TAG_NAME", "button")

            # 좋아요 버튼이 눌려있지 않은 경우
            if len(like_btn.find_elements(By.TAG_NAME, "div")) > 1:
                like_btn.send_keys(Keys.ENTER)

                # 좋아요 횟수 +1
                like_cnt += 1
                print(f"{like_cnt}번째 좋아요: {key}번째 게시글")
                time.sleep(2)

                if like_cnt == 10:
                    break
    if key == 100:
        break