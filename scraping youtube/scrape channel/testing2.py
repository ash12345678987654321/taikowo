from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.youtube.com/channel/UCoSrY_IQQVpmIRZ9Xf-y93g/videos")

#html=driver.page_source
#open("gawrgura.html","w",encoding="utf-8").write(html)

#https://medium.com/analytics-vidhya/using-python-and-selenium-to-scrape-infinite-scroll-web-pages-825d12c24ec7
time.sleep(1)  # Allow 1 seconds for the web page to open
scroll_pause_time = 1 # shitty internet moment
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.documentElement.scrollHeight;")  #document element bcas yt dumb
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    
    #print(screen_height*i,scroll_height)
    if (screen_height) * i > scroll_height:
        break

#scrape video ids directly from console
cmd="return ytInitialData.contents.twoColumnBrowseResultsRenderer.tabs[1].tabRenderer.content.sectionListRenderer.contents[0].itemSectionRenderer.contents[0].gridRenderer.items"

length=driver.execute_script(cmd+".length;") #length of videos

for i in range(length):
    print(driver.execute_script(cmd+"["+str(i)+"].gridVideoRenderer.videoId"))

driver.close()