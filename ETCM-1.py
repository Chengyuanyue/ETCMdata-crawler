from time import sleep
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def each_row(cells, idx):
    # 从 cells 中根据索引读取某行的 6 个格子内的文本信息
    ChineseName = cells[idx].text.strip()
    Piyin = cells[idx + 1].text.strip()
    HerbType = cells[idx + 2].text.strip()
    HerbProperty = cells[idx + 3].text.strip()
    HerbMeridianTropism = cells[idx + 4].text.strip()
    HerbFlavor = cells[idx + 5].text.strip()

    # 获取中药的详情页（ href 属性值）
    btn_detailed = cells[idx].find_element(By.TAG_NAME, 'a')
    DetailedPage = btn_detailed.get_attribute('href').strip()
    arr = np.array([[ChineseName, Piyin,HerbType ,HerbProperty ,HerbMeridianTropism,HerbFlavor,DetailedPage]])
    return arr


def each_page():
    arr = np.empty([0, 7])
    cells = driver.find_elements(By.XPATH, '//td')

    # 每次循环收集一行加到 arr 中
    for i in range(0, 120, 6):
        # 先试着收集一下当前这行
        # 能收集到就存到 arr 中
        try:
            # 收集该行信息
            arr_temp = each_row(cells, i)
        # 不能收集到（无更多行比如末页、或网络延迟等原因）的话
        # 就返回一行 Error 方便以后检查
        except:
            arr_temp = np.array([['Error', 'Error', 'Error', 'Error','Error','Error','Error']])

        # 将刚收集的的信息合并到结果 arr 中
        arr = np.concatenate([arr, arr_temp])

    return arr


url = 'http://www.tcmip.cn/ETCM/index.php/Home/Index/Prescriptions_All.html?getType=yc'

# 新建一个 webdriver 对象
driver = webdriver.Edge('msedgedriver.exe')
# 访问 url
driver.get(url)

# 创建储存数据的空arr
arr = np.empty([0, 7])
for i in range(2):
    # 收集该页信息
    arr_temp = each_page()
    # 将刚收集的信息合并到结果 arr 中
    arr = np.concatenate([arr, arr_temp])
    # 等待 2 秒再翻页，防止操作频率过快引起注意
    sleep(2)
    # 找到下一页按钮并翻页
    #driver.find_element(By.LINK_TEXT,'›').click()
    btn_next_1 = driver.find_element(By.XPATH, "//a[text()='›']")
    btn_next_1.send_keys(Keys.ENTER)
    #btn_next_2 = driver.find_element(By.XPATH, '//a[›]')
    #btn_next_2.send_keys(Keys.ENTER)

col_names = ["ChineseName", "Piyin","HerbType","HerbProperty" ,"HerbMeridianTropism", "HerbFlavor","DetailedPage"]

# 以 pandas.DataFrame 输出爬到的信息
df_result = pd.DataFrame(data=arr, columns=col_names)
df_result.to_excel('ETCM中药.xlsx', index=False)
