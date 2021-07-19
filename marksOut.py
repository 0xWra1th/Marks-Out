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
LOGIN_EMAIL = str(sys.argv[1])+"@tuks.co.za"
ALERT_EMAILS = [LOGIN_EMAIL]
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

def alert(mark):
	# RUN SENDMAIL SCRIPT
	for i,email in enumerate(ALERT_EMAILS):
		if email == LOGIN_EMAIL:
			res = subprocess.check_call("touch mail.txt", shell=True)
			res = subprocess.check_call("echo \"%s\" > mail.txt" % str("Subject: "+str(mark[0]+": "+str(mark[1]))+"\r\nFrom: Mark Alert<"+str(SENDER)+">\r\n\r\nYou have a new mark available on the UPnet Portal!!"), shell=True)
			res = subprocess.check_call("./sendMail %s" % str(email), shell=True)
			res = subprocess.check_call("rm mail.txt", shell=True)
		else:
			res = subprocess.check_call("touch mail.txt", shell=True)
			res = subprocess.check_call("echo \"%s\" > mail.txt" % str("Subject: "+str(mark[0])+" Mark Released!\r\nFrom: Mark Alert<"+str(SENDER)+">\r\n\r\nYou have a new mark available on the UPnet Portal!!\r\n"), shell=True)
			res = subprocess.check_call("./sendMail %s" % str(email), shell=True)
			res = subprocess.check_call("rm mail.txt", shell=True)

while(True):
	try:
		marks = poll()
		for mark in marks:
			if mark not in prevMarks and prevMarks != []:
				alert(mark)
		prevMarks = marks
		time.sleep(60)
	except:
		pass