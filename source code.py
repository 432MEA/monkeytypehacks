import time
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from datetime import datetime, timedelta


# Opens MonkeyType in a Chromemium/Chrome window
# This can be modified to use different browsers/drivers
PATH = input("Path of the chrome driver: ")
browser = webdriver.Chrome(PATH)
browser.get('https://monkeytype.com/')


def type_text(words):
    for word in words:
        # Using selenium send_keys() to type the word if it contains single or double quotation marks
        if "'" in word.get_attribute('textContent') or '"' in word.get_attribute('textContent'):

            # Because 'word' isn't an HTML input element, an ActionChain is used to be able to send keys
            actions = ActionChains(browser)
            actions.send_keys(word.get_attribute('textContent') + ' ')
            actions.perform()

        # If the word doesn't contain quotation marks, the word is typed character by character
        # This is done to be able to make use of pyautogui.PAUSE
        else:
            for char in word.get_attribute('textContent'):
                pyautogui.typewrite(char)
            # Adds a space after every word typed
            pyautogui.typewrite(' ')


def given_word_count():
    # time.sleep() allows the user some time to select the desired test mode on monkeytype.com
    time.sleep(6)
    words = browser.find_elements_by_class_name('word')

    type_text(words)
    print("Done")
    choose()


def given_duration(test_time):
    # Performs a typing test with a given duration
    # Call this function with either 15, 30, 60 or 120 seconds as value for the test_time parameter
    # time.sleep() allows the user some time to select the desired test mode on monkeytype.com
    time.sleep(7)

    # Performs the function while the current time is less than the current time + the duration of the test
    end_time = datetime.now() + timedelta(seconds=test_time)
    while datetime.now() < end_time:
        # Stores the active word to type in a list in order to be used as a parameter for type_text()
        words = [browser.find_element_by_css_selector('div.word.active')]

        type_text(words)
    print("Done")
    choose()


def get_given_pause(pause_time):
    if pause_time < 0:
        print('Pause time cannot be less than 0')
        return
    # Sets the pause between each character to a given number of N/1000 seconds
    pyautogui.PAUSE = float(pause_time / 1000)


# This is an example of how to call the typing functions directly
# The function 'get_givin_pause()' is the time inbetween two letters
# Call `given_word_count()` to perform a words, custom or quote test 
# Call 'givin_duration()' to perform timed tests

#get_given_pause(75)
#given_word_count()

def choose():
    print("1.) Perform a words, custom or quote test")
    print("2.) Perform a timed test")
    choice = input(">>>")
    if choice == "1":
        pauseTime = float(input("Pause between each character in milliseconds: "))
        print("Starting in 6 seconds. Get your cursor ready.")
        get_given_pause(pauseTime)
        given_word_count()
    elif choice == "2":
        pauseTime = float(input("Pause between each character in milliseconds: "))
        length = int(input("Test time in seconds: "))
        print("Starting in 7 seconds. Get your cursor ready. ")
        get_given_pause(pauseTime)
        given_duration(length)
    else:
        print("That is not a valid choice. Choose one of the above choices.")
        choose()

choose()
