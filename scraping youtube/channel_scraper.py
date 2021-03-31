from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape(url):
    print(url)

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    #https://medium.com/analytics-vidhya/using-python-and-selenium-to-scrape-infinite-scroll-web-pages-825d12c24ec7
    time.sleep(1)  # Allow 3 seconds for the web page to open
    scroll_pause_time = 0.3 # idk
    scrape_limit=500 #we dont need so many
    
    #long command but its just to access videos
    cmd="return ytInitialData.contents.twoColumnBrowseResultsRenderer.tabs[1].tabRenderer.content.sectionListRenderer.contents[0].itemSectionRenderer.contents[0].gridRenderer.items"
    
    while (True):
        # get scroll height
        scroll_height = driver.execute_script("return document.documentElement.scrollHeight;")  #document element bcas yt dumb
    
        # scroll to bottom
        driver.execute_script("window.scrollTo(0, {height})".format(height=scroll_height))  
        
        time.sleep(scroll_pause_time)
        length=driver.execute_script(cmd+".length") #length of videos
        
        if (length>scrape_limit): break
        if ("gridVideoRenderer" in driver.execute_script(cmd+"["+str(length-1)+"]")):
            time.sleep(3) #confirmation
            length=driver.execute_script(cmd+".length") #length of videos
            if ("gridVideoRenderer" in driver.execute_script(cmd+"["+str(length-1)+"]")):
                break
            

    #scrape video ids directly from console
    length=driver.execute_script(cmd+".length") #length of videos
    
    ids=[]
    for i in range(length):
        if (not "gridVideoRenderer" in driver.execute_script(cmd+"["+str(i)+"]")): continue
        ids.append(driver.execute_script(cmd+"["+str(i)+"].gridVideoRenderer.videoId"))
    
    driver.close()
    
    return ids
    
inp=open("channels_truth.txt","r").read()

f=open("ids.txt","w",encoding="utf-8")

for i in inp.split("\n"):
    i=i.split("\t")
    ids=scrape("https://www.youtube.com/channel/"+i[1]+"/videos")
    
    clickbait="1" if i[2]=="clickbait" else "0"
    
    print("added: "+str(len(ids)))
    for id in ids:
        f.write(id+"\t"+clickbait+"\n")
    
f.close()