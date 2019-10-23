import network
 
def connect():
  ssid = "Tensor"
  password =  "87654321"
 
  station = network.WLAN(network.STA_IF)
 
  if station.isconnected() == True:
      tuple1 = station.ifconfig()
      #print(tuple1[0])
      ipold = tuple1[0]
      
      return ipold
 
  station.active(True)
  station.connect(ssid, password)
 
  while station.isconnected() == False:
      pass
 
  tuple1 = station.ifconfig()
  ipold = tuple1[0]
  return ipold