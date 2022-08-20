from machine import Pin, ADC
from time import sleep


def read_volatage(GPIO_PIN):
    pot = ADC(Pin(GPIO_PIN))
    pot.atten(ADC.ATTN_11DB)
    #ADC.ATTN_0DB — the full range voltage: 1.2V
    #ADC.ATTN_2_5DB — the full range voltage: 1.5V
    #ADC.ATTN_6DB — the full range voltage: 2.0V
    #ADC.ATTN_11DB Full range: 3.3v

    
    pot_value = pot.read()  
    volts = pot_value*3.3/4095
    
    return pot_value, volts




if __name__ == '__main__':
      
    while True:
        bit_value, volts = read_volatage(34)
        print(volts)
        sleep(0.1)
  
  
  
  
