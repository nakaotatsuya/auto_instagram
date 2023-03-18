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
import argparse

likeCounter = 0
notLikeCounter = 0
alreadyLikeCounter = 0
continueLikeTooMuchCounter = 0
continuousLikeCounter = 0

def login(username, password):
	driver.get('https://www.instagram.com/')
	time.sleep(1)
	userNameTextBoxName = 'username'
	passTextBoxName = 'password'
	elementUserNameTextBox = waitElement((By.NAME, userNameTextBoxName), 2)
	elementUserNameTextBox.send_keys(username)
	time.sleep(1)
	driver.find_element(By.NAME, passTextBoxName).send_keys(password)
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

	#first_target_class_name = driver.find_elements_by_class_name('_aagw')[10]

	first_target_xpath = "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[1]/div/div/div[1]/div[2]/a/div[1]/div[2]"
	
	#/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[1]/div/div/div[2]/div[1]/a/div[1]/div[1]/img
	#/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[1]/div/div/div[1]/div[2]/a/div[1]/div[1]/img
	#target_xpath = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/section/div/div[3]/div/div/div[1]/div/article[' + str(article_number) + ']/div/div[3]/div/div/section[1]/span[1]/button'
	element_first_target = waitElementClickable((By.XPATH, first_target_xpath), 2)
	print(element_first_target)
	time.sleep(random.randint(2,3))
	print(element_first_target.location)
	#scroll
	# actions = ActionChains(driver)
	# actions.move_to_element(first_target_xpath)
	# actions.perform()
	# time.sleep(random.randint(2, 3))

	scroll_down(start=0, goal=element_first_target.location["y"])
	time.sleep(1)
	element_first_target.click()
	time.sleep(random.randint(2, 3))

def isAlreadyPressLike(element):
	likeButton = element.find_element(By.XPATH, "./div/span")
	print(likeButton)
	#time.sleep(random.randint(2,5))
	#likeButton1 = likeButton.find_element(By.CLASSNAME, "_aame")
	likeButton1 = likeButton.find_element(By.XPATH, "//*[name()='svg']")
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
	
def choose_article(article_number=1, continuousLikeCounter=0):
	
	target_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button"
	element_target = waitElementClickable((By.XPATH, target_xpath), 2)
	
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
	
	time.sleep(random.randint(1,2))
	right_arrow_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button"
	# /html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div/button
	right_arrow_element = waitElementClickable((By.XPATH, right_arrow_xpath), 2)
	right_arrow_element.click()
	time.sleep(random.randint(1,2))

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
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--tag_word", type=str, help="tag word")
	parser.add_argument("-u", "--username", type=str, help="login username")
	parser.add_argument("-p", "--password", type=str, help="login password")
	args = parser.parse_args()

	taglist = [args.tag_word]
	loopCount = 0
	errorCount = 0
	logging.info('Start!!!')
	options = webdriver.ChromeOptions()
	options.add_experimental_option('detach', True)
	driver = webdriver.Chrome(options=options)
	# driver.get('https://www.instagram.com/')
	login(username=args.username, password=args.password)
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

	searchByTag(tag=random.choice(taglist))
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
				choose_article(article_number=article_number)
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