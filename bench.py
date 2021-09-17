#!/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import numpy as np
import sys

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

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver.get("https://chromium.github.io/octane")
    assert "Octane 2.0" in driver.title
    driver.execute_script("Run()")

    try:
        element = WebDriverWait(driver, 1000).until(
            EC.text_to_be_present_in_element((By.ID, "main-banner"), "Octane Score:")
        )
    except TimeoutException:
        driver.quit()
        print("timeout", flush=True, file=sys.stderr)
        return measure(prefs)

    elem = driver.find_element_by_id("main-banner")
    text = elem.text
    driver.quit()
    return int(text[14:])

def measure_batch(prefs, n):
    values = []
    for j in range(n):
        v = measure(prefs)
        values.append(v)

    return "{:.0f} ({:.0f})".format(np.mean(values), np.std(values))

iterations = 100

disabled = {}
enabled = {}
for i in range(len(mitigations)):
    disabled[mitigations[i]] = False
    enabled[mitigations[i]] = True

print("n =", iterations, flush=True)
print("No mitigations:", measure_batch(disabled, iterations), flush=True)

prefs = dict(disabled)
prefs["javascript.options.spectre.index_masking"] = True
print("Just index_masking:", measure_batch(prefs, iterations), flush=True)

prefs = dict(disabled)
prefs["javascript.options.spectre.object_mitigations"] = True
print("Just object_mitigations:", measure_batch(prefs, iterations), flush=True)

prefs = dict(disabled)
prefs["javascript.options.spectre.index_masking"] = True
prefs["javascript.options.spectre.object_mitigations"] = True
print("index_masking + object_mitigations:", measure_batch(prefs, iterations), flush=True)

print("All mitigations:", measure_batch(enabled, iterations), flush=True)
