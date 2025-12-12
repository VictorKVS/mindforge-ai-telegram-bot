from uag.gateway import handle as uag_handle

def run_scenario(scenario):
    # упрощённо: имитируем агент → UAG
    response = uag_handle(scenario["request"])
    return response
