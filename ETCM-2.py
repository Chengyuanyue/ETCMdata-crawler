import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# 创建空列表，后面储存数据
herb = []
compounds = []
detaileds = []

# 循环读入数据
df = pd.read_excel('ETCM中药.xlsx')
for k in range(254,402):
    url = df['DetailedPage'][k]
    name = df['ChineseName'][k]

    # 新建一个 webdriver 对象
    driver = webdriver.Edge("msedgedriver.exe")
    # 访问 url
    driver.get(url)

    # 解析中药成分及 url
    compoundcell = driver.find_elements(By.XPATH, '//table[@id="table"]//tr[@data-index="11"]//a[@class="tdcolor"]')

    #计数
    print(k)
    
    # 以列表的形式保存数据
    for i in range(0,len(compoundcell)):
        compound = compoundcell[i].text
        detailed = compoundcell[i].get_attribute('href').strip()
        #print(compound)
        #print(detailed)
        compounds.append(compound)
        detaileds.append(detailed)
        herb.append(name)
 
        # 保存数据
        dataframe=pd.DataFrame({'herb':herb,'compound':compounds,'detailed':detaileds})
        dataframe.to_excel ("C:/Users/yuechengyuan/Desktop/ETCM_10421.xlsx", encoding='utf-8-sig', index=False)
