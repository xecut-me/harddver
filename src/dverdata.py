from secret import BACKDOOR_AUTH, BACKDOOR_URL
from time import sleep
import subprocess
import requests
import json
import re


def get_power_stat():
    J_total = 0
    J_current = 0
    dJ_60sec = None

    with open("/home/kiosk/logs/power.log", "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            J = int(line) / 1_000_000

            if J < J_current:
                J_total += J_current
            else:
                dJ_60sec = J - J_current
            
            J_current = J
    
    J_total += J_current

    kWh_CO2_kg = 0.8 # Belgrade with fossil fuel dominated electricity
    J_CO2_kg = kWh_CO2_kg / 60 / 60 / 1000

    CO2_kg_so_far = J_CO2_kg * J_total

    co2_msg = f"{CO2_kg_so_far:.3f} kg of CO₂ emitted so far"
    w_msg = f"{dJ_60sec / 60:.2f}W" if dJ_60sec else ""

    return (co2_msg, w_msg)


def get_temp():
    result = subprocess.run("sensors", capture_output=True, text=True)
    exp = re.search(r"\+[^ ]+", result.stdout)
    text_result = ""

    if exp:
        text_result = exp.group()

    return text_result


def get_data():
    data = {}

    try:
        data["backdoor"] = requests.get(BACKDOOR_URL, headers={"Authorization": BACKDOOR_AUTH}).json()
    except Exception as e:
        print(e)
    
    try:
        data["co2"], data["w"] = get_power_stat()
    except Exception as e:
        print(e)

    try:
        data["temp"] = get_temp()
    except Exception as e:
        print(e)

    return json.dumps(data, ensure_ascii=False, indent=2)


def data_pusher(driver):
    with open("./chat.json.log", "r") as file:
        for line in file:
            driver.execute_script("addMessage(arguments[0]);", line)

    while True:
        driver.execute_script("onData(arguments[0]);", get_data())

        sleep(10)
