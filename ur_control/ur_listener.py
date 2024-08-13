import struct

class UrListener:
    def __init__(self,socket):
        self.s = socket
        
        self.remaining_data = b""
        
        self.stopped = True  
    
    def get_robot_state(self):
        self.stopped = self.get_status()
        return self.stopped
    
    def read_buffer(self):
        data = self.s.recv(100000)
        self.remaining_data += data

        while len(self.remaining_data) > 0:
            if len(self.remaining_data) < 4:
                break

            packlen = (struct.unpack('!i', self.remaining_data[0:4]))[0]
            
            if len(self.remaining_data) < packlen:
                break
            
            self.remaining_data = self.remaining_data[packlen:]
        return
        
    def get_status(self):
        data = self.s.recv(100000)
        self.remaining_data += data
        
        stopped = False
        while len(self.remaining_data) > 0:
            # make sure packet is bigger than 4 bytes to be able to read packlen & packtype
            if len(self.remaining_data) < 4:
                break

            packlen = (struct.unpack('!i', self.remaining_data[0:4]))[0]
            packtype = (struct.unpack('!b', self.remaining_data[4:5]))[0]
            
            # make sure remaining_data includes a full message
            if len(self.remaining_data) < packlen:
                break
            
            if packtype == 16:
                i = 0
                while i+5 < packlen:
                    msglen = (struct.unpack('!i', self.remaining_data[5+i:9+i]))[0] 
                    msgtype = (struct.unpack('!b', self.remaining_data[9+i:10+i]))[0] 
                    
                    if msgtype == 0:
                        isProgramRunning = (struct.unpack('!?', self.remaining_data[23+i:24+i]))[0]
                        stopped = isProgramRunning == False
                        
                    i = msglen + i

            self.remaining_data = self.remaining_data[packlen:]
        
        return stopped
        
