from secret import BACKDOOR_AUTH, BACKDOOR_URL
import subprocess
import requests
import asyncio
import re


def get_co2_emitted():
    J_total = 0
    J_current = 0

    with open("/home/kiosk/logs/power.log", "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            J = int(line) / 1_000_000

            if J < J_current:
                J_total += J_current
            
            J_current = J
    
    J_total += J_current

    kWh_CO2_kg = 0.8 # Belgrade with fossil fuel dominated electricity
    J_CO2_kg = kWh_CO2_kg / 60 / 60 / 1000

    CO2_kg_so_far = J_CO2_kg * J_total

    return f"{CO2_kg_so_far:.3f} kg of CO₂ emitted so far"


def get_temp():
    result = subprocess.run("sensors", capture_output=True, text=True)
    exp = re.search(r"\+[^ ]+", result.stdout)
    text_result = ""

    if exp:
        text_result = exp.group()

    return text_result


async def data_pusher(driver):
    while True:
        data = {}

        try:
            data["backdoor"] = requests.get(BACKDOOR_URL, headers={"Authorization": BACKDOOR_AUTH}).json()
        except Exception as e:
            print(e)
        
        try:
            data["co2"] = get_co2_emitted()
        except Exception as e:
            print(e)

        try:
            data["temp"] = get_temp()
        except Exception as e:
            print(e)

        driver.execute_script("onData(arguments[0]);", data)

        await asyncio.sleep(10)
