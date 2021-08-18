#!/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np

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
    values = []
    for j in range(n):
        v = measure(prefs)
        values.append(v)

    return "{:.0f} ({:.1f})".format(np.mean(values), np.std(values))

iterations = 20

disabled = {}
for m in mitigations:
    disabled[m] = False

print("n =", iterations)
print("No mitigations:", measure_batch(disabled, iterations))
print("Just index_masking:", measure_batch(dict(filter(lambda x: x[0] != "javascript.options.spectre.index_masking", disabled.items())), iterations))
print("Just object_mitigations:", measure_batch(dict(filter(lambda x: x[0] != "javascript.options.spectre.object_mitigations", disabled.items())), iterations))
print("index_masking + object_mitigations:", measure_batch(dict(filter(lambda x: x[0] != "javascript.options.spectre.index_masking" and x[0] != "javascript.options.spectre.object_mitigations", disabled.items())), iterations))
print("All mitigations:", measure_batch({}, iterations))
