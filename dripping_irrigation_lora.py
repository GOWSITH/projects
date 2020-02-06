from time import sleep
from saran_gsm_1 import sim
from SX127x.LoRa import*
from SX127x.board_config import BOARD
from urllib import request
from urllib import parse
BOARD.setup()

class LoRaRcvCont(LoRa):
   
    tx_counter=0
    b=0
    sensor1=[]
    url="http://hicard.infinitesol.co/api/irriot"
    def __init__(self, verbose=False):
           
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)   
       
    def start(self):
        
        self.reset_ptr_rx()
        sys.stdout.write("\rstart")
        self.set_mode(MODE.TX)
        self.set_mode(MODE.RXCONT)
        self.write_payload([0x0f])
        sim.read_and_delete_all()
        lora.receive_sms()
        #lora.on_tx_done()
        self.b=1
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
        html=(bytes(payload).decode("utf-8",'ignore'))
        print(type(html))
        sleep(1.5)
        data=request.urlopen("http://hicard.infinitesol.co/api/irriot/poststatus?usr=14&msg=%s"%html)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    
    def on_tx_done(self):
        #global args
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        sys.stdout.flush()
        print("Waitng to receive  the node...")
        sleep(5)
        print(self.node2)     
        data =[int(hex(ord(c)), 0) for c in self.node2]
        self.write_payload(data)
        self.set_mode(MODE.TX)
        
    def receive_sms(self):
        print("waiting...")        
        self.node2=sim.read_sms(1)
        #print(self.node2)
        if(self.node2==None):
            lora.receive_sms()
        else:
            
            lora.on_tx_done()        
            
        
        
       

lora=LoRaRcvCont()
lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)
sim.read_and_delete_all()
print("Welcome")
sim.send_sms("+919677534206","system starts")
print("Waitng to receive...")
sleep(5)
def read_sms1():
    node=sim.read_sms(1)
    print(node)
    if(node=='1'):        
        lora.start()

    elif(node==None):
        read_sms1()

'''node=sim.read_sms(1)
print(node)
if(node=='1'):
    lora.start()

elif(node==None):
    read_sms1()'''


try:
    node=sim.read_sms(1)
    print(node)
    if(node=='1'):
        lora.start()

    elif(node==None):
        read_sms1()  
   


except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()'''
