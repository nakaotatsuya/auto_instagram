from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from datetime import datetime 
import os
import time
import random
import logging.config

likeCounter = 0
notLikeCounter = 0
alreadyLikeCounter = 0
continueLikeTooMuchCounter = 0
continuousLikeCounter = 0

def login():
	driver.get('https://www.instagram.com/')
	time.sleep(1)
	userNameTextBoxName = 'username'
	passTextBoxName = 'password'
	elementUserNameTextBox = waitElement((By.NAME, userNameTextBoxName), 2)
	elementUserNameTextBox.send_keys('dokechi_2023')
	time.sleep(1)
	driver.find_element(By.NAME, passTextBoxName).send_keys('zaqbaran')
	time.sleep(1)

	loginButtonXPathName = '//*[@id="loginForm"]/div/div[3]/button'
	elementLoginButton = waitElementClickable((By.XPATH, loginButtonXPathName), 2)
	elementLoginButton.click()
	time.sleep(random.randint(2, 5))

def searchByTag(tag):
	# logger.info('search by {}'.format(tag))
	instaurl = 'https://www.instagram.com/explore/tags/'
	driver.get(instaurl + tag)
	time.sleep(random.randint(2, 5))

def isAlreadyPressLike(element):
	likeButton = element.find_element(By.XPATH, "./div/span")
	print(likeButton)
	likeButton1 = likeButton.find_element(By.CLASS_NAME, "_ab6-")
	label = likeButton1.get_attribute('aria-label')
	print("label is ...", label)
	if label == '「いいね！」を取り消す':
		return True
	else:
		return False

def scroll_down(start, goal):
	#ページの高さを取得
    #height = driver.execute_script("return document.body.scrollHeight")
    #最後までスクロールすると長いので、半分の長さに割る。
    #height = height // 16
	
	#ループ処理で少しづつ移動
	for x in range(start ,goal, 30):
		driver.execute_script("window.scrollTo(0, "+str(x)+");")
	return goal
	
def choose_article(article_number=1, continuousLikeCounter=0, old_height=0):
	# targetImages = "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/section/div/div[3]/div/div/div[1]/div"
	# elementtargetImages = waitElements((By.XPATH, targetImages), 2)
	# print(elementtargetImages)
	# time.sleep(random.randint(5,8))

	target_xpath = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/section/div/div[3]/div/div/div[1]/div/article[' + str(article_number) + ']/div/div[3]/div/div/section[1]/span[1]/button'
	element_target = waitElementClickable((By.XPATH, target_xpath), 2)
	print(element_target)
	#element_target.click()
	time.sleep(random.randint(2,3))
	print(element_target.location)
	#scroll
	# offset = 20
	new_height = scroll_down(start=old_height, goal=element_target.location["y"])
	# time.sleep(2)
	# element_target.click()
	# driver.execute_script("arguments[0].scrollIntoView();", element_target)
	# if offset != 0:
	# 	script = "window.scrollTo(0, window.pageYOffset + " + str(offset) + ");"
	# 	driver.execute_script(script)
	# 	time.sleep(random.randint(5,10))

	if random.randint(1,5) % 5 == 0:
		print("through")
		time.sleep(1)
		continuousLikeCounter = 0
	elif isAlreadyPressLike(element=element_target):
		print("'good' is already pushed.")
		time.sleep(1)
		continuousLikeCounter = 0
	else:
		time.sleep(random.randint(2,3))
		element_target.click()
		print("clicked!!! article number is {}.".format(article_number))
		continuousLikeCounter+= 1
	return new_height

def convertMinutesToSeconds(minutes):
    return (minutes * 60)

def waitElement(elementLocator, seconds):
	wait = WebDriverWait(driver, 30)
	element = wait.until(expected_conditions.presence_of_element_located(elementLocator))
	time.sleep(seconds)
	return element
	
def waitElements(elementLocator, seconds):
	wait = WebDriverWait(driver, 30)
	elements = wait.until(expected_conditions.presence_of_all_elements_located(elementLocator))
	time.sleep(seconds)
	return elements

def waitElementClickable(elementLocator, seconds):
	wait = WebDriverWait(driver, 30)
	element = wait.until(expected_conditions.element_to_be_clickable(elementLocator))
	time.sleep(seconds)
	return element

if __name__ == '__main__':
	# taglist = ["music"]

	loopCount = 0
	errorCount = 0
	logging.info('Start!!!')
	options = webdriver.ChromeOptions()
	options.add_experimental_option('detach', True)
	driver = webdriver.Chrome(options=options)
	# driver.get('https://www.instagram.com/')
	login()
	time.sleep(random.randint(2, 3))
	
	#laterButtonXpath = "//button[@class='sqdOP yWX7d    y3zKF     ']"
	laterButtonXpath = "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button"
	elementLaterButton = waitElementClickable((By.XPATH, laterButtonXpath), 2)
	elementLaterButton.click()
	time.sleep(random.randint(2, 3))
	
	laterButtonXpath2 = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]"
	elementLaterButton2 = waitElementClickable((By.XPATH, laterButtonXpath2), 2)
	elementLaterButton2.click()
	time.sleep(random.randint(2, 3))
	#driver.service.stop()
	n_article = 6
	new_height = 0

	while True:
		try:
			loopCount += 1
			logging.info('Loop Count_{}'.format(loopCount))
			# startAutomation()
			for article_number in range(n_article):
				article_number += 1
				print("height:", new_height)
				new_height = choose_article(article_number=article_number, old_height=new_height)
				print(article_number)
		except Exception as e:
			errorCount += 1
			import traceback
			logging.error(traceback.format_exc())
			
			if errorCount == 10:
				logging.error('Error. End system.')
				driver.close()
				break
			logging.error('error {} times'.format(errorCount))
			driver.close()
			waitTime = random.randint(convertMinutesToSeconds(60), convertMinutesToSeconds(65))
			logging.info('wait for {} secs'.format(waitTime))
			time.sleep(waitTime)
		else:
			print("this is else.")			
			if loopCount % 10 == 0:
				# waitTime = random.randint(convertMinutesToSeconds(30), convertMinutesToSeconds(32))
				waitTime = random.randint(60, 90)
				logging.info('wait for {} secs'.format(waitTime))
				driver.close()
				time.sleep(waitTime)
			else:			 
				# waitTime = random.randint(convertMinutesToSeconds(10), convertMinutesToSeconds(12))
				waitTime = random.randint(60, 90)
				logging.info('wait for {} secs'.format(waitTime))
				driver.close()
				time.sleep(waitTime)

	print("this is outside of whlie.")
	driver.service.stop()