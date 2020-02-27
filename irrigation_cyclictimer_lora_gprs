from time import sleep
from gprs import sim
from SX127x.LoRa import*
from SX127x.board_config import BOARD
import json
import requests
from datetime import datetime

BOARD.setup()

class LoRaRcvCont(LoRa):
   
    tx_counter=0
    b=0
    r=None
    grp=None
    group_read=None
    sep_group=None
    G=[]
    GP=[]
    start_time=[]
    end_time=[]
    group=[]
    d=[]
    ln=None


   
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
        self.d.clear()
        sim.send_sms("+919677534206","system starts")
        lora.receive_sms()
        self.b=1
        sleep(1)
       
    def receiver(self):
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
            elif(self.b==6):                
                lora.gprs()              
       
               
           
   
    def on_rx_done(self):
        self.set_mode(MODE.STDBY)
        print("Received: ")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print(bytes(payload).decode("utf-8",'ignore'))
        self.html=(bytes(payload).decode("utf-8",'ignore'))
        self.d.append(self.html)
        sleep(2)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

   
    def on_tx_done(self):
        #global args
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        sys.stdout.flush()
        print("Waitng to receive  the node...")
        sleep(2)
        print(self.node2)
        data =[int(hex(ord(c)), 0) for c in self.node2]
        self.write_payload(data)
        self.set_mode(MODE.TX)
        lora.receiver()
       
    def receive_sms(self):
        print("waiting...")        
        self.node2=sim.read_sms(1)
        if(self.node2==None):
            lora.receive_sms()
        elif(self.node2=="AUTO ON"):
            print("cyclic timer")
            sim.read_and_delete_all()
            lora.cyclic_timer()
           
           
        else:            
            lora.on_tx_done()

   
    def gprs(self):
        a=len(self.d)
        if(a==0):
            sim.send_sms("9677534206","Interrupt")
            lora.start()
       
        else:
           
            for i in self.d:
                print(i)
                if(len(i)>=15):
                    data=('GET /~mayagree/api.php?MSG='+i+'\r\n')
                    length=str(len(data))
                    print(data)
                    sim.gprs_gsm(length,data)                    
                    lora.start()
                    break
            print("Interrupt")
            lora.start()
           
   
    def cyclic_timer(self):
        print("waiting...")
        self.group_read=sim.read_sms(1)
        if(self.group_read==None):
            lora.cyclic_timer()
        else:
            lora.cyclic()
           
    def cyclic(self):
       
        a=self.group_read
        sim.read_and_delete_all()
        b=a.split(';')
        c=b[2:]        
        self.ln=len(c)
        print(self.ln)        
        for i in range(self.ln):
            d=c[i].split(':')            
            e=d[1].split(',')
            self.GP.append(d[0])            
            self.G.append(e)
            print(self.G)
            print(self.GP)
        lora.separate_grp_recevier()

    def separate_grp_recevier(self):
        print("waiting...")
        self.sep_group=sim.read_sms(1)
        if(self.sep_group==None):
            lora.separate_grp_recevier()
        else:
            lora.separate_grp()
           
    def separate_grp(self):      
       
        self.grp=self.sep_group
        print(self.grp)
        sim.read_and_delete_all()
        if(len(self.grp)>=20):
            lora.timer()
           
            def check():
                global i
                for i in range(self.ln):
                    CID={i:{self.GP[i]:self.G[i],self.start_time[i]:self.end_time[i]}}
                    qw=self.GP[i]
                    if(rn==self.start_time[i]):
                        for i in self.G[i]:
                            d=str(qw+":"+i+" ON")
                            self.set_mode(MODE.STDBY)
                            self.clear_irq_flags(TxDone=1)
                            sys.stdout.flush()
                            print("Waitng to receive  the node...")
                            sleep(12)
                            print(d)
                            data =[int(hex(ord(c)), 0) for c in d]
                            self.write_payload(data)
                            self.set_mode(MODE.TX)                

                           

                    elif(rn==self.end_time[i]):
                        for i in self.G[i]:
                            e=str(qw+":"+i+" OFF")
                            self.set_mode(MODE.STDBY)
                            self.clear_irq_flags(TxDone=1)
                            sys.stdout.flush()
                            print("Waitng to receive  the node...")
                            sleep(12)
                            print(e)
                            data =[int(hex(ord(c)), 0) for c in e]
                            self.write_payload(data)
                            self.set_mode(MODE.TX)                  

            while(1):
                rn = str(datetime.now().strftime("%H:%M"))
                print(rn)
                msg=sim.read_sms(1)
                if(msg=="AUTO OFF"):
                    lora.start()
                else:
                    check()
               
               
    def timer(self):
            a=self.grp
            b=a.split(';')
            c=b[1:]
            print(self.ln)
            for i in range(self.ln):
                q=c[i]
                d=q.split('|')
                self.group.append(d[0])
                e=d[1]
                f=e.split('~')                
                self.start_time.append(f[0])
                print(self.start_time)
                self.end_time.append(f[1])
                print(self.end_time)
                print(self.group)
            for i in range(self.ln):
                CID={self.group[i]:{self.start_time[i]:self.end_time[i]}}
                print(CID)    

       

lora=LoRaRcvCont()
print(lora.get_freq())
lora.set_coding_rate(4)
lora.set_bw(6)
lora.set_spreading_factor(12)
lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)
sim.read_and_delete_all()
sleep(5)
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
