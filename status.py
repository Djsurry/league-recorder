import os, time, psutil
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# TODO redo this fucking shit and kill the devs of opgg :)
# blitz.gg is better anyway -ls



wait_for ="sc-gJTSre"

otherwise  = "sc-gzVnrw"

gametype = "StyledComponents__HeaderMainContentQueueType-e9atmj-19"
class Browser:
	def __init__(self):

		self.chrome_options = Options()  
		#self.chrome_options.add_argument("--headless")  
		self.driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),   chrome_options=self.chrome_options)  
		self.wait = WebDriverWait(self.driver, 10)
		setup_finished = False

	def start(self, region, ign):

		self.driver.get(f"https://blitz.gg/lol/live/{region}1/{ign}")

		try:
			self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, wait_for)))
		except:
			try:
				self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,otherwise)))
				self.driver.close()
				return False
			except:
				print('Error')
				self.driver.close()
				quit()

 
		gamemode = self.driver.find_element_by_class_name(gametype)
		self.driver.close()
		return gamemode.get_attribute('innerHTML')

def in_game(region, ign):
	b = Browser()
	mode = b.start(region, ign)
	if mode in ['Ranked Solo', 'Ranked Flex']:
		return True
	else:
		return False

def league_open():
	procs = []
	for p in list(psutil.process_iter()):
		try:
			procs.append(p.name())
		except psutil.AccessDenied:
			continue
	return "League of Legends.exe" in procs


if __name__ == "__main__":
	# b = Browser()
	# print(b.start('na', 'buzzlightyear99'))
	print(league_open())

