import asyncio
import pwinput
from os import path
from pathlib import Path
import time

from pyppeteer import launch
from pyppeteer.errors import TimeoutError as TO

PASSWORD = pwinput.pwinput(prompt='Please Enter WordPress Password: ', mask='')
BASE_DIR = p = Path('.')

#Enter the path to your Chrome or Chromium executable here
CHROMIUM_EXECUTABLE_PATH = "/Applications/Chromium.app/Contents/MacOS/Chromium"
#Enter where your WordPress instance is running here
WORDPRESS_SITE_URL = 'http://localhost:8080'
WORDPRESS_ADMIN_URL = f'{WORDPRESS_SITE_URL}/wp-admin/'

# Enter your WordPress username here
ADMIN_USER = 'jo'
ADMIN_PASSWORD = PASSWORD

async def create_post(page, title, content, first_run):        
    await page.waitForSelector('#wp-admin-bar-new-content')
    await page.click('#wp-admin-bar-new-content')

    if first_run:
        await page.waitForSelector('button[aria-label="Close dialogue"]')
        await page.click('button[aria-label="Close dialogue"]')

    await page.waitForSelector('.wp-block-post-title')
    await page.click('.wp-block-post-title')
    await page.keyboard.type(title)
    await page.click('.block-editor-inserter__toggle')
    # THERE IS AN ANIMATION HERE THAT PREVENTS A GOOD CLICK.
    time.sleep(0.5)
    await page.waitForSelector('.block-editor-inserter__quick-inserter-expand')
    await page.click('.block-editor-inserter__quick-inserter-expand')
    await page.waitForSelector('.editor-block-list-item-html')
    await page.click('.editor-block-list-item-html')
    await page.waitForSelector('.block-editor-plain-text')
    await page.click('.block-editor-plain-text')
    await page.keyboard.type(content)
    await page.click('.editor-post-publish-button__button')
    time.sleep(0.5)
    await page.click('.editor-post-publish-panel__header .components-button')
    await page.waitForSelector('.post-publish-panel__postpublish-buttons')
    await page.click('.edit-post-fullscreen-mode-close')    

async def main():
    browser = await launch(executablePath=CHROMIUM_EXECUTABLE_PATH, headless=False, autoClose=False)
    page = await browser.newPage()
    
    await page.goto(WORDPRESS_ADMIN_URL)
    await page.waitForSelector('#user_login');
    await page.focus('#user_login')
    await page.keyboard.type(ADMIN_USER)
    await page.focus('#user_pass')
    await page.keyboard.type(ADMIN_PASSWORD)
    await page.click('#wp-submit')

    try:
        await page.waitForSelector('#login_error', timeout=1000)
        await browser.close()
        print("\n\nYou have entered the wrong username or password. Please try again.\n\n")
    except TO:
        pass    

    first_run = True
        
    for x in (BASE_DIR / 'Posts').iterdir():
        title = x

        with open(x) as f:
            content = f.read()
            
            await create_post(page, path.basename(title), content, first_run)

        first_run = False
    
    await browser.close()



    

asyncio.get_event_loop().run_until_complete(main())
