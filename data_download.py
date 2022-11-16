from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
import os

PATH = 'C:\Program Files/ (x86)\Google\Chrome\Application\chrome.exe'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
wd = webdriver.Chrome(executable_path=PATH,options=options)


def get_images_from_google(wd, delay, max_images, url):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = url
	wd.get(url)

	image_urls = set()
	skips = 0
	while len(image_urls) + skips < max_images:
		scroll_down(wd)
		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))


	return image_urls


def download_image(down_path, url, file_name, image_type='JPEG',
                   verbose=True):
    try:
        
        img_content = requests.get(url).content
        img_file = io.BytesIO(img_content)
        image = Image.open(img_file)
        file_pth = down_path + file_name

        with open(file_pth, 'wb') as file:
            image.save(file, image_type)

        if verbose == True:
            print(f'The image: {file_pth} downloaded successfully.')
    except Exception as e:
        print(f'Unable to download image from Google Photos due to\n: {str(e)}')



if __name__ == '__main__':
    # Google search URLS
    google_urls = [
                   'https://www.google.com/search?q=sunset&tbm=isch&sxsrf=ALiCzsbVsCk50Jmw86j6eTm57eaAos943Q%3A1667687553621&source=hp&biw=1920&bih=1007&ei=geRmY7jKI5LA9APJ8YHoDA&iflsig=AJiK0e8AAAAAY2bykbBuPdBfBu-iMNqmll9bjUQHr-yV&ved=0ahUKEwj4jumhjJj7AhUSIH0KHcl4AM0Q4dUDCAc&uact=5&oq=sunset&gs_lp=EgNpbWeKAgtnd3Mtd2l6LWltZ7gBA_gBATIEECMYJzIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixA8ICBRAAGIAEwgIIEAAYsQMYgwFIyQlQAFiJCHAAeADIAQCQAQCYAW6gAckDqgEDNS4x&sclient=img',
                   'https://www.google.com/search?q=forest&tbm=isch&sxsrf=ALiCzsYmMVVoTdsp1JOxfWf_XNYkjW0L_A%3A1667687810993&source=hp&biw=1920&bih=1007&ei=guVmY_icOv7L0PEPy9KRuAU&iflsig=AJiK0e8AAAAAY2bzklBbguA-lvEKEwzK3VpTcbWkqMC2&ved=0ahUKEwj45cWcjZj7AhX-JTQIHUtpBFcQ4dUDCAc&uact=5&oq=forest&gs_lp=EgNpbWeKAgtnd3Mtd2l6LWltZ7gBA_gBATIEECMYJzIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixA8ICBRAAGIAESL4JUABYywZwAHgAyAEAkAEAmAFroAHAA6oBAzUuMQ&sclient=img'
                   
    ]
    
    labels = [
        'sunset','forest'
    ]

    cnt=0
    player_path = 'images/'
    # Make the directory if it doesn't exist
    if not os.path.exists(player_path):
            print(f'Making directory: {str(player_path)}')
            os.makedirs(player_path)

    for url_current, lbl in zip(google_urls, labels):
        urls = get_images_from_google(wd, 0, 250, url_current)
        for i, url in enumerate(urls):
            download_image(down_path=f'{player_path}', 
                        url=url, 
                        file_name=str(cnt)+ '.jpg',
                        verbose=True) 
            cnt+=1
    wd.quit()