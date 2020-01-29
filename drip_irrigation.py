from time import sleep
from SX127x.LoRa import*
from SX127x.board_config import BOARD
from urllib import request
from urllib import parse
BOARD.setup()

class LoRaRcvCont(LoRa):
   
    tx_counter=0
    b=0
   
    def __init__(self, verbose=False):
           
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)   
       
    def start(self):
        self.reset_ptr_rx()
        sys.stdout.write("\rstart")
        self.set_mode(MODE.TX)
        self.set_mode(MODE.RXCONT)
        self.write_payload([0x0f])
        
        lora.on_tx_done()
        self.b=0
        sleep(1)
        while(1):
            if(self.b<=5):
                sleep(1)
                self.b=self.b+1
                rssi_value = self.get_rssi_value()
                status = self.get_modem_status()
                print(self.b)                
                lora.on_rx_done()
                sleep(1)                
                sys.stdout.flush()
            elif(self.b>5):
                lora.start()
                
                
           
   
           
    def on_rx_done(self):
        self.set_mode(MODE.STDBY)
        print("Received: ")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print(bytes(payload).decode("utf-8",'ignore'))
        html=bytes(payload).decode("utf-8",'ignore')
        data=request.urlopen("https://api.thingspeak.com/update?api_key=G11K5Q42ZJWO3R26&field1=%s"%html)
        sleep(0.5)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
       
   
   
   
    def on_tx_done(self):
    
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        sys.stdout.flush()
        rawinput = str(input("Enterthenode:"))        
        data =[int(hex(ord(c)), 0) for c in rawinput]
        self.write_payload(data)
        self.set_mode(MODE.TX)          
       

lora=LoRaRcvCont()
lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)
try:
   
    lora.start()


except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
