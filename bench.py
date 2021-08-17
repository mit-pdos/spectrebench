#!/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

mitigations = [
    "javascript.options.spectre.index_masking",
    "javascript.options.spectre.jit_to_cxx_calls",
    "javascript.options.spectre.object_mitigations",
    "javascript.options.spectre.string_mitigations",
    "javascript.options.spectre.value_masking",
]

def measure(prefs):
    profile = webdriver.FirefoxProfile()
    for pref, value in prefs.items():
        profile.DEFAULT_PREFERENCES['frozen'][pref] = value

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get("https://chromium.github.io/octane")
    assert "Octane 2.0" in driver.title
    driver.execute_script("Run()")

    try:
        element = WebDriverWait(driver, 100).until(
            EC.text_to_be_present_in_element((By.ID, "main-banner"), "Octane Score:")
        )
    finally:
        elem = driver.find_element_by_id("main-banner")
        text = elem.text
        driver.quit()
        return int(text[14:])

def measure_batch(prefs, n):
    v = 0
    for j in range(n):
        v = max(v, measure(prefs))
    return v

disabled = {}
print("Default:", measure_batch({}, 5))
for i in reversed(range(len(mitigations))):
    disabled[mitigations[i]] = False
    print("{}=False: {}".format(mitigations[i], measure_batch(disabled, 5)))



