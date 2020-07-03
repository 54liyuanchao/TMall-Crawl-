from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
from time import sleep
from selenium.webdriver import ActionChains

class tabao:

    def __init__(self):
        self.url = 'https://login.taobao.com/member/login.jhtml'

        options = webdriver.ChromeOptions()
        prefs = {}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        prefs["profile.managed_default_content_settings.images"] = 2
        options.add_experimental_option("prefs", prefs)
        #options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s


    def login(self):

        self.browser.get(self.url)

        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[5]/a[1]').click()

        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@id="pl_login_logged"]/div/div[2]/div/input').send_keys(weibo_username)
        self.browser.find_element_by_xpath('//*[@id="pl_login_logged"]/div/div[3]/div/input').send_keys(
            weibo_password)
        self.browser.find_element_by_xpath('//*[@class="btn_tip"]/a/span').click()

        taobao_name = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="J_SiteNavLogin"]/div[1]/div[2]/a')))
        print(taobao_name.text)

    def swipe_down(self, second):
        for i in range(int(second / 0.1)):
            js = "var q=document.documentElement.scrollTop=" + str(300 + 200 * i)
            self.browser.execute_script(js)
            sleep(0.1)
        js = "var q=document.documentElement.scrollTop=100000"
        self.browser.execute_script(js)
        sleep(0.2)


    def get_track(dist):  # distance为传入的总距离
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = dist* 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 200

        while current < dist:
            if current < mid:
                # 加速度为2
                a = 200
            else:
                # 加速度为-2
                a = -3
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def get_data(self,name):


        self.browser.get("https://list.tmall.com/search_product.htm?q="+name)
        err = self.browser.find_element_by_xpath("//*[@id='content']/div/div[2]").text
        err = err[:5]
        if(err == "喵~没找到"):
            print("没有找到搜索结果")
            return

        total_page = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[8]/div/b[2]/form')))
        total_page = total_page.text.replace("共", "").replace("页，到第页 确定", "").replace("，", "")
        print("总页数："+total_page)

        for page in range(2,int(total_page)):

            total_good = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="J_ItemList"]')))
            html = self.browser.page_source
            doc = pq(html)
            items = doc('#J_ItemList .product').items()

            for item in items:
                item_title = item.find('.productTitle').text().replace('\n', "").replace('\r', "")
                item_price = item.find('.productPrice').text().replace('\n', "").replace('\r', "")
                item_status = item.find('.productStatus').text().replace('\n', "").replace('\r', "")
                item_url = item.find('.productImg').attr('href')

                print(item_title+"  "+item_price+"  "+item_status+"  "+item_url+'\n')

            self.swipe_down(2)
            confirm_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page > div.ui-page-wrap > b.ui-page-skip > form > input.ui-page-skipTo')))
            submit_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page > div.ui-page-wrap > b.ui-page-skip > form > button.ui-btn-s')))
            confirm_button.clear()
            confirm_button.send_keys(page)
            sleep(1)
            submit_button.click()


            try:
                WebDriverWait(self.browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.ID, "nc_1_n1z")))  # 等待滑动拖动控件出现
                swipe_button = self.browser.find_element_by_id('nc_1_n1z')  # 获取滑动拖动控件

                # 模拟拽托
                action = ActionChains(self.browser)  # 实例化一个action对象
                action.click_and_hold(swipe_button).perform()  # perform()用来执行ActionChains中存储的行为
                action.reset_actions()
                tracks = self.get_track(500)
                for track in tracks:
                    action.move_by_offset(track, 0).perform()  # 移动滑块

            except Exception as e:
                print('get button failed: ', e)







if __name__ == "__main__":
    # 使用之前请先查看当前目录下的使用说明文件README.MD
    # 使用之前请先查看当前目录下的使用说明文件README.MD
    # 使用之前请先查看当前目录下的使用说明文件README.MD

    chromedriver_path = "/Users/yuanchaoli/Downloads/chromedriver"  # 改成你的chromedriver的完整路径地址
    weibo_username = "15222471238"  # 改成你的微博账号
    weibo_password = "0ooo00ooo0"  # 改成你的微博密码

    a = tabao()
    a.login()  # 登录
    a.get_data("足球")  # 登录
    print('done')