

class gps:
    import serial
    from time import sleep
    port = "/dev/ttyAMA0"
    ser =0
    data = 0
    def __init__(self):
        self.ser = self.serial.Serial(self.port,baudrate=9600,timeout=.5)
        self.ser.close()
    def getall(self):
        self.ser.open()
        self.sleep(.02)
        self.ser.reset_input_buffer()
        count = 0
        reply = [(0,0),0,'none']
        truths = [False,False,False]

        while count < 100 and not(truths[0] and truths[1] and truths[2]) :
            #print(count < 100)
            #print(not(truths[0] and truths[1] and truths[2]))
            #data = self.ser.readline()
            #print(reply,truths)

            try:
                #self.sleep(0.5)
                data =self.ser.readline()
                #print(str(data))
            except:
                data = ''
                print('failed parse')
                pass
            count +=1 
            if (str(data)[2:8] == "$GPVTG"):
                #print("Velocity data recieved")
                data=str(data).split(',')
                    #for i,b in enumerate(data):
                            #pass
                            #print(i,b)
                #print(data[7],type(data[7]))
                try:
                    a= (float(data[7])*0.621371)
                    reply[1]= a
                    truths[1] = True
                except:
                    pass
            elif (str(data)[2:8] == "$GPGLL"):
                    #print("location data recieved")
                data=str(data).split(',')
                    #for i,b in enumerate(data):
                            #print(i,b)
                try:
                    a = ((float(data[1][0:2])+(float(data[1][2:])/60)),-1*(float(data[3][0:3])+(float(data[3][3:])/60)))
                    reply[0] = a
                    truths[0]= True
                except:
                    pass
            elif (str(data)[2:8] == "$GPGSV"):
                    #print("location data recieved")
                data=str(data).split(',')
                #for i,b in enumerate(data):
                    #print(i,b)
                try:
                    reply[2] = data[3]
                    truths[2]= True
                except:
                    pass
        self.ser.close()

        return reply
##                try:
##                    a = ((float(data[1][0:2])+(float(data[1][2:])/60)),-1*(float(data[3][0:3])+(float(data[3][3:])/60)))
##                    reply[0] = a
##                    truths[0]= True
##                except:
##                    pass
    def getV(self):
        self.ser.open()
        #print('getting V')
        
        #self.ser.reset_input_buffer()
        #self.ser.reset_output_buffer()
        self.sleep(.02)
        count = 0
        while count <100:
            try:
                data =self.ser.readline()
            except:
                data = "blah"
            
            if (str(data)[2:8] == "$GPVTG"):
                #print("Velocity data recieved")
                data=str(data).split(',')
                #for i,b in enumerate(data):
                    #pass
                    #print(i,b)
                self.ser.close()
                print(data[7],type(data[7]))
                try:
                    a= (float(data[7])*0.621371)
                    return a 
                except:
                    pass
                 
            count+=1
       # print(count,data)

        self.ser.close()
        return 0
    def getll(self):
        #return (42.235946, -88.340130)
        self.ser.open()
        count=0
        #print('gettingloc')
        while count <100:
            try:
                data =self.ser.readline()
            except:
                data = "blah"  
            if (str(data)[2:8] == "$GPGLL"):
                #print("location data recieved")
                data=str(data).split(',')
                #for i,b in enumerate(data):
                    #print(i,b)
                self.ser.close()
                try:
                    a = ((float(data[1][0:2])+(float(data[1][2:])/60)),-1*(float(data[3][0:3])+(float(data[3][3:])/60)))
                    return a
                except:
                    pass
            count +=1
        self.ser.close()
        return 0,0
