from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import chromedriver_binary
import time
import csv

my_url = "https://byebyegoodbyeworld.com/testing/"

#mobile_emulation = {
#
#	"deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
#
#	"userAgent": "Mozilla/5.0 (Linux; Android 10; Pixel) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Mobile Safari/537.36" }

chrome_options = Options()
#Uncomment next line to run in background
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=4")
chrome_options.add_argument('disable-infobars')
#chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options = chrome_options)

driver.implicitly_wait(5)

print("Loading User Info.")
try:
	input_file = open('C:/Path/To/login.txt')
	items = input_file.read().splitlines()

	#Set login info from login.txt
	usern = items[0]
	passw = items[1]

	length = len(items)
	for i in range(2, length, 1):
		item = items[i]

except Exception as e:
	print(e)
	raise

def GetTable():
	print("Getting Table.")

	tableName = driver.find_element_by_xpath('/html/body/h2')

	table = driver.find_element_by_xpath('/html/body/table/tbody')
	with open(('C:/Path/To/'+ tableName.text + '.csv'), 'w', newline='') as csvfile:
		wr = csv.writer(csvfile)
		#wr.writerow([''])  #Writes a blank row
		wr.writerow([d.text for d in table.find_elements_by_css_selector('th')])
		for row in table.find_elements_by_css_selector('tr'):
			wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
	print("Exported Data for:", tableName.text)
		
	driver.quit()

driver.get(my_url)
print("URL Loaded.")
print(driver.current_url)
print("Logging In.")
driver.find_element_by_xpath('//*[@id="Us"]').send_keys(usern)
driver.find_element_by_xpath('//*[@id="Pa"]').send_keys(passw)
driver.find_element_by_xpath('/html/body/form/input[3]').click()
print(driver.current_url)
#Check for element in page to verify successful login
hTag = driver.find_element_by_xpath('/html/body/h2')
if (hTag.text) == "Table":
	GetTable()
else:
	print("Error Logging In.")