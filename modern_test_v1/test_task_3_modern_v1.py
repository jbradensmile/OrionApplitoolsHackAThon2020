from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from applitools.selenium import (
    logger,
    VisualGridRunner,
    Eyes,
    Target,
    BatchInfo,
    BrowserType,
    DeviceName,
)

import os

api_key = "41aE6zclkZw5vvvU98XUOrCn9RftiKdfTUamMosLTNOY110"
batch_name = "UFG Hackathon"
concurrency = 10
desktop_viewport = {"width": 1200, "height": 700}
eyes_viewport = {"width": 800, "height": 600}
tablet_viewport = {"width":768, "height": 700}
test_name = "Task 3"
v1_url = "https://demo.applitools.com/gridHackathonV1.html"
v2_url = "https://demo.applitools.com/gridHackathonV2.html"

def set_up(eyes):

    # You can get your api key from the Applitools dashboard
    eyes.configure.set_api_key(api_key)

    # create a new batch info instance and set it to the configuration
    eyes.configure.set_batch(BatchInfo(batch_name))

    # Add browsers with different viewports
    # Add mobile emulation devices in Portrait mode
    (
        eyes.configure.add_browser(desktop_viewport.get("width"), desktop_viewport.get("height"), BrowserType.CHROME)
        .add_browser(desktop_viewport.get("width"), desktop_viewport.get("height"), BrowserType.FIREFOX)
        .add_browser(desktop_viewport.get("width"), desktop_viewport.get("height"), BrowserType.EDGE) # Edge will be depricated, but EDGE_CHROMIUM isn't valid yet.
        .add_browser(tablet_viewport.get("width"), tablet_viewport.get("height"), BrowserType.CHROME)
        .add_browser(tablet_viewport.get("width"), tablet_viewport.get("height"), BrowserType.FIREFOX)
        .add_browser(tablet_viewport.get("width"), tablet_viewport.get("height"), BrowserType.EDGE)
        .add_device_emulation(DeviceName.iPhone_X) # Viewport doesn't match rules.
    )


def ultra_fast_test(web_driver, eyes):
    try:
        # Navigate to the url we want to test
        print("Navigating to the site.")
        web_driver.get(v1_url)

        # Task 3 specific elements
        open_filter = web_driver.find_element_by_id('A__openfilter__206')
        black_filter_checkbox = web_driver.find_element_by_id('SPAN__checkmark__107')
        filter_button = web_driver.find_element_by_id('filterBtn') 

        # Filtering for Black shoe products
        print("Clicking open filter button.")
        open_filter.click()

        print("Clicking the Black checkbox.")
        if black_filter_checkbox:
            web_driver.execute_script("arguments[0].click();", black_filter_checkbox)

        print("Executing the filter.")
        if filter_button:
            web_driver.execute_script("arguments[0].click();", filter_button)

        #Click on black shoe image
        print("Clicking on the first black shoe product.")
        product_image = web_driver.find_element_by_id('IMG__imgfluid__215') # Defining here to get passed a 'stale element' issue.
        product_image.click()

        # Call Open on eyes to initialize a test session
        print("Initializing window for session.")
        eyes.open(
            web_driver, "Demo App", test_name, eyes_viewport
        )

        # Check the app page
        print("Building the HTML to send to UFG.")
        eyes.check("Product Details test", Target.window().fully().with_name(v1_url))

        # Call Close on eyes to let the server know it should display the results
        eyes.close_async()
    except Exception as e:
        eyes.abort_async()
        print(e)


def tear_down(web_driver, runner):
    # Close the browser
    print("Closing the browser.")
    web_driver.close()

    print("Running UFG and creating Batch in Dashboard")
    # we pass false to this method to suppress the exception that is thrown if we
    # find visual differences
    all_test_results = runner.get_all_test_results(False)
    print(all_test_results)

# Create a new chrome web driver
web_driver = Chrome(ChromeDriverManager().install())

# Create a runner with concurrency of 1
runner = VisualGridRunner(concurrency)

# Create Eyes object with the runner, meaning it'll be a Visual Grid eyes.
eyes = Eyes(runner)

set_up(eyes)

try:
    # ⭐️ Note to see visual bugs, run the test using the above URL for the 1st run.
    # but then change the above URL to https://demo.applitools.com/index_v2.html
    # (for the 2nd run)
    ultra_fast_test(web_driver, eyes)
finally:
    tear_down(web_driver, runner)
