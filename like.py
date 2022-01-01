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
            EC.presence_of_element_located((
            By.CSS_SELECTOR, string)))
        # 찾은 element가 복수 개인 경우
        if len(element.find_elements(By.CSS_SELECTOR, string)) > 1:
            result = element.find_elements(By.CSS_SELECTOR, string)
        # 찾은 element가 한 개 뿐인 경우
        else:
            result = element.find_elements(By.CSS_SELECTOR, string)[0]

    elif method == "XPATH":
        WebDriverWait(element, 10).until(
            EC.presence_of_element_located((
            By.XPATH, string)))
        if len(element.find_elements(By.XPATH, string)) > 1:
            result = element.find_elements(By.XPATH, string)
        else:
            result = element.find_elements(By.XPATH, string)[0]
    elif method == "TAG_NAME":
        WebDriverWait(element, 10).until(
            EC.presence_of_element_located((
            By.TAG_NAME, string)))
        if len(element.find_elements(By.TAG_NAME, string)) > 1:
            result = element.find_elements(By.TAG_NAME, string)
        else:
            result = element.find_elements(By.TAG_NAME, string)[0]
    elif method == "CLASS_NAME":
        WebDriverWait(element, 10).until(
            EC.presence_of_element_located((
            By.CLASS_NAME, string)))
        if len(element.find_elements(By.CLASS_NAME, string)) > 1:
            result = element.find_elements(By.CLASS_NAME, string)
        else:
            result = element.find_elements(By.CLASS_NAME, string)[0]
    elif method == "NAME":
        WebDriverWait(element, 10).until(
            EC.presence_of_element_located((
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

#화면 띄우기
instagram = "https://instagram.com"
driver = webdriver.Chrome('./chromedriver.exe')
driver.get(instagram)

#Login ID 입력하기
login_id = wait_for(driver, "NAME", "username")
login_id.send_keys(ID)

#Login PW 입력하기
login_pw = wait_for(driver, "NAME", "password")
login_pw.send_keys(PW)
login_pw.send_keys(Keys.RETURN)

# 첫 번째 팝업 지우기
popup_css = "#react-root > section > main > div > div > div > div > button"
popup = wait_for(driver, "CSS_SELECTOR", popup_css)
popup.send_keys(Keys.ENTER)

# 두 번째 팝업 지우기
popup_css = "body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm"
popup = wait_for(driver, "CSS_SELECTOR", popup_css)
popup.send_keys(Keys.ENTER)


# 게시글 dictionary 생성
article_dict = {}

# 좋아요 영역의 class명
like_div_class = "fr66n"

# 게시글 키 변수 생성
key = 0
# 현재 조회하는 게시글의 key
now = 0
# 좋아요 횟수 변수 생성
like_cnt = 0
# 좋아요 스킵한 게시글 변수 생성 (10개 이상 스킵 시 작업 종료)
pass_cnt = 0
# 조회할 게시글의 수
m = 200
# 좋아요할 게시글의 수
n = 100


# 좋아요를 n번 하거나 게시글을 m개 조회할 때까지 반복
while True:

    # 현시점 화면의 전체 게시글 불러오기
    # 인스타그램은 스크롤을 조금만 움직여도 article이 동적으로 변하므로
    # 한 게시글의 탐색을 마칠 때마다 articles를 업데이트 하도록 함
    articles = wait_for(driver, "TAG_NAME", "article")

    # 업데이트된 articles를 dictionary에 넣어두는 과정
    for article in articles:

        # 게시글이 게시글 dictionary에 없는 경우
        if article not in article_dict.values():
            # 키 +1 및 dictionary에 추가
            key += 1
            article_dict[key] = article

    
    # 게시글 탐색 시작
    now += 1

    try:
        # 해당 게시글로 스크롤 이동
        driver.execute_script("arguments[0].scrollIntoView();", article_dict[now])
        print(f"{now}번째 게시글을 조회함")
        time.sleep(1)
    except:
        # 어떤 이유에선지 불러온 article이 조회되지 않는 경우가 있음 -> 다음 게시글로 넘어감
        print(f"{now}번째 게시글은 불러올 수 없음")
        continue


    # 좋아요 버튼 element 불러오기
    like_div = wait_for(article_dict[now], "CLASS_NAME", like_div_class)
    like_btn = wait_for(like_div, "TAG_NAME", "button")

    # 좋아요 버튼이 눌려있지 않은 경우
    if like_btn.find_elements(By.XPATH, "div/span/*[name()='svg'][@aria-label='좋아요']") != []:
        like_btn.send_keys(Keys.ENTER)

        # 좋아요 횟수 +1
        like_cnt += 1
        # 좋아요 스킵한 게시글 수 리셋
        pass_cnt = 0
        print(f"{like_cnt}번째 좋아요: {now}번째 게시글")
        time.sleep(1)

        if like_cnt == n:
            break
        elif like_cnt%10 == 0:
            print(f"{like_cnt}건을 좋아요했습니다. 10초 대기 후에 작업 재개합니다.")
            time.sleep(10)

    else:
        # 좋아요 스킵 시 +1
        pass_cnt += 1
        if pass_cnt == 10:
            print("연속된 10개의 게시글의 좋아요를 스킵하여 아래 게시글은 모두 좋아요를 누른 것으로 판단, 작업 종료합니다.")
            break

    if now == m:
        break
