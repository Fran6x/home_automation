import time
import struct
import board
import digitalio as dio
from circuitpython_nrf24l01 import RF24


# addresses needs to be in a buffer protocol object (bytearray)
# address = [b'1Node', b'2Node', b'3Node', b'4Node']

# change these (digital output) pins accordingly
ce = dio.DigitalInOut(board.D17)
csn = dio.DigitalInOut(board.D8)

# using board.SPI() automatically selects the MCU's
# available SPI pins, board.SCK, board.MOSI, board.MISO
spi = board.SPI()  # init spi bus object
 # initialize the nRF24L01 on the spi bus object





class Emitter:
    
    

    def __init__(self, address, location, id,  sensors_number, missed_req=0, pipe=1):
        self.listening_address = bytes(str(address*2) + "Node", 'utf8')
        self.writing_address = bytes(str(address*2-1) + "Node", 'utf8')
        self.pipe = pipe
        self.location = location
        self.id = id 
        self.sensors_number = sensors_number
        
        
        print(f"initializing object{self.listening_address, self.writing_address, self.sensors_number}")

        # nrf.payload_length = 8

        self.nrf = RF24(spi, csn, ce, ask_no_ack=False, payload_length=self.sensors_number*4)
        self.nrf.dynamic_payloads = False  # this is the default in the TMRh20 arduino library       
        
        


    # check les exeptions et remet le tuple
    def receive(self):
        
        default_val = "no data"
        start_time = time.monotonic()
        while time.monotonic() - start_time < 5:

            self.nrf.listen = True  # put radio in rx mode

            if self.nrf.any() > 0:  # data are comming

                buffer = self.nrf.recv()
                values = [struct.unpack('f', buffer[i*4:(i+1)*4])[0] for i in range(0, self.sensors_number)]
                for value in values:
                    print(f'VALUES = {value}')
               
                rounded_values = [round(value, 1) for value in values]
                
                return rounded_values
        
        
        return None

    def send(self):

        self.nrf.listen = False  # Put radio in tx mode
        buffer = struct.pack("i", 1)  # packed int = 1 in struct for C compatibility
        send_result = self.nrf.send(buffer)  # send data via nrf

        return send_result  # return true if sended

    def request(self):
        req_start_time = time.monotonic()
        print("preparing request 1")

        # set address of TX node into a RX pipe
        self.nrf.open_rx_pipe(self.pipe, self.listening_address)  # address[1]
        # set address of RX node into a TX pipe
        self.nrf.open_tx_pipe(self.writing_address)  # address[0]
        print("sending")

        print(self.send())

        data_received = self.receive()

        # if data_received is None:
        #     values = ["no data" for i in range(0, self.sensors_number)]
        #     return values
        if data_received is None:
            raise Exception ('No data received')
        else:

            for i, data in enumerate(data_received):
                print(f"data {i} = {data}")

            print(f"request took {time.monotonic() - req_start_time} seconde.")

            print(f"data_received = {data_received} !")

            

            # print(f"temperature = {data_received[0]}, humidity = {data_received[1]}")

            # return data_received[0], data_received[1]
            return data_received