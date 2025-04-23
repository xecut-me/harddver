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
