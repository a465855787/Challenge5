# ?? json ??????
import json

# ?? selenium ????
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ???????
results = []

# ?? xpath ??????
def parse(response):
    for comment in response.css('div.comment-list-item'):
        result = {
            'username':comment.css('div.user-username a::text').extract_first().strip(),
            'content':comment.css('div.comment-item-content.markdown-box p::text').extract_first().strip()
        }
        
        results.append(result)

# ????????
def has_next_page(response,page):
    # ?? xpath ??????????????
    # ?? True ?? False
    next = response.css('div#comments div.pagination-container ul li.disabled.next-page').extract_first()
    print(page,next)
    if next==None:
        return True
    else:
        return False
# ??????
def goto_next_page(driver):
    # ?? driver.find_element_by_xpath ????????
    # ??????? click() ???????? 
    next_btn = driver.find_element_by_xpath('//*[@id="comments"]/div/div[4]/ul/li[6]/a')
    next_btn.click()

# ????????
def wait_page_return(driver, page):
 
    WebDriverWait(driver, 30).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//ul[@class="pagination"]/li[@class="active"]'),
            str(page)
        )
    )

# ???
def spider():
    # ?? PhantomJS ? webdriver
    driver = webdriver.PhantomJS()
    # ???????
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1
    while True:
        # ????????

        wait_page_return(driver, page)
        # ??????
        html = driver.page_source
        # ?? HtmlResponse ??
        response = HtmlResponse(url=url, body=html.encode('utf8'))
        # ?? HtmlResponse ????????
        parse(response)
        # ????????????
        if not has_next_page(response,page):
            break
        # ??????
        page += 1
        goto_next_page(driver)
    # ? results ?? json ????????
    with open('/home/shiyanlou/comments.json', 'w') as f:
        f.write(json.dumps(results))


if __name__ == '__main__':
    spider()