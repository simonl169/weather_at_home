from machine import Pin, ADC
from time import sleep
from machine import deepsleep


def read_voltage(GPIO_PIN):
    pot = ADC(Pin(GPIO_PIN))
    pot.atten(ADC.ATTN_11DB)
    #ADC.ATTN_0DB — the full range voltage: 1.2V
    #ADC.ATTN_2_5DB — the full range voltage: 1.5V
    #ADC.ATTN_6DB — the full range voltage: 2.0V
    #ADC.ATTN_11DB Full range: 3.3v

    
    pot_value = pot.read()  
    volts = pot_value*3.3/4095
    
    return pot_value, volts

def main():
    print('Running main function')
    bit_value, volts = read_voltage(34)
    print(volts)
    sleep(2)
    print('Reading voltage done, going to deepsleep')
    deepsleep(5000)

    


if __name__ == '__main__':
    
    print('Running main function as main') 
    main()
        
  
  
  
  
