# The mark checker uses selenium webdriver to poll upnet.up.ac.za and fetch newly released exam marks.

# LIBRARIES
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import warnings
import sys
import subprocess

# VARIABLES
USERNAME = str(sys.argv[1])
PASSWORD = str(sys.argv[2])
ALERT_EMAILS = [str(sys.argv[1])]
prevMarks = []
marks = []

# Polling Function
def poll():
	warnings.filterwarnings('ignore')
	op = webdriver.ChromeOptions()
	op.add_argument('--headless')
	driver = webdriver.Chrome(options=op)
	driver.get("https://upnet.up.ac.za")

	time.sleep(1)

	userField = driver.find_element_by_id("userid_placeholder")
	userField.clear()
	userField.send_keys(USERNAME)

	passField = driver.find_element_by_id("password")
	passField.clear()
	passField.send_keys(PASSWORD)
	passField.send_keys(Keys.RETURN)

	if "PROCEED WITHOUT PASSWORD CHANGE" in driver.page_source:
		try:
			driver.find_element_by_partial_link_text('PROCEED').click()
		except:
			time.sleep(3)
			driver.find_element_by_partial_link_text('PROCEED').click()

	oldTab = driver.current_window_handle

	time.sleep(3)

	try:
		driver.find_element_by_link_text('Student Centre').click()
	except:
		time.sleep(5)
		driver.find_element_by_link_text('Student Centre').click()


	time.sleep(3)

	for handle in driver.window_handles:
		if handle != oldTab:
			driver.switch_to_window(handle)

	try:
		driver.find_element_by_id("win0divPTNUI_LAND_REC_GROUPLET$2").click()
	except:
		try:
			time.sleep(5)
			driver.find_element_by_id("win0divPTNUI_LAND_REC_GROUPLET$2").click()
		except:
			time.sleep(10)
			driver.find_element_by_id("win0divPTNUI_LAND_REC_GROUPLET$2").click()

	time.sleep(3)

	marks = []

	for i in range(0,20):
		try:
			className = str(driver.find_element_by_id("CLASS_NAME$"+str(i)).get_attribute('innerHTML'))
			mark = str(driver.find_element_by_id("DERIVED_SSS_SCL_UP_GRADE1$"+str(i)).get_attribute('innerHTML'))
			marks.append([className, mark])
		except Exception as e:
			break

	driver.close()
	res = subprocess.check_call("pkill chrome", shell=True)
	return marks

def alert():
	# RUN SENDMAIL SCRIPT
	for email in ALERT_EMAILS:
		res = subprocess.check_call("./sendMail %s" % str(email), shell=True)

while(True):
	try:
		marks = poll()
		if marks != prevMarks and prevMarks != []:
			alert()
		prevMarks = marks
		time.sleep(60)
	except:
		pass