def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.connect('<Tensor>', '<87654321>')
        while not sta_if.isconnected():
            pass
   print('network config:', sta_if.ifconfig())