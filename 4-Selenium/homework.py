import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


def pchome(items):
    

    # 初始化瀏覽器
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=options)

    # 打開 PChome
    driver.get("https://24h.pchome.com.tw/")
    time.sleep(1)

    # 關閉跳窗
    try:
        driver.find_element(By.CSS_SELECTOR, ".c-popUp__endBtn > button").click()
    except:
        pass

    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".c-search__input").send_keys(items)
    driver.find_element(By.CSS_SELECTOR, ".c-search__btn.c-search__btn--search").click()
    try:
        no_result_text = driver.find_element(By.CSS_SELECTOR, ".c-tipsBox__text.c-tipsBox__text--regular500GrayDarkest").text
        if "找不到想要的商品" in no_result_text:
            print(f" PCHOME沒有這東東：{items}")
            return "找不到想要的商品"
    except NoSuchElementException:
                # 如果沒有找到商品列表，也沒有找到查無商品的提示，可能只是頁面載入問題，但我們在此處先返回。
                pass
    All_items = []
    page_count = 1
    
    while True:
        print(f"\n--- 正在爬取第 {page_count} 頁 ---")
        time.sleep(2)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        item_list = driver.find_elements(By.CSS_SELECTOR, ".c-listInfoGrid__item")
        for item in item_list:
            Product_name = item.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__title").text
            Product_price = item.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__price").text
            Product_img = item.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__img > img").get_attribute("src")
            Product_href = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            All_items.append({
                "name": Product_name,
                "price": Product_price,
                "img": Product_img,
                "href": Product_href
            })

        # 找下一頁按鈕
        try:
            next_page_button = driver.find_element(
                By.CSS_SELECTOR, 
                "div.c-pagination__button.is-next > button:not([disabled])"
            )
            next_page_button.click()
            page_count += 1
            time.sleep(2)
        except NoSuchElementException:
            print("已到達最後一頁，停止爬取")
            break
    print("總筆數：", len(All_items))
    driver.quit()
    

    #      輸出 JSON 檔案
    filename = f"{items}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(All_items, f, ensure_ascii=False, indent=2)

    print("\n======================================")
    print(f"已將資料輸出至： {filename}")
    print("總筆數：", len(All_items))

    return All_items
#-------------------------------------

if __name__ == "__main__":
    keyword = input("請輸入商品名稱：")
    pchome(keyword)
