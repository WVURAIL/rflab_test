#!/Library/Frameworks/EPD64.framework/Versions/Current/bin/python
import time, socket
import matplotlib
matplotlib.use('Agg')
import pylab
import numpy as np

class GPIB:
    """A class to communicate with instruments over GPIB using a Prologix
       ethernet-GPIB converter.  """

#ip='192.168.0.37'
    def __init__(self, address=8, to=5, ip='10.10.10.137'):
      print "Initializing Connection..."
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 
                        socket.IPPROTO_TCP)
      self.sock.settimeout(to)
      self.sock.connect((ip, 1234))
      self.address = address
      self.sock.send("++mode 1\r") #switch prologix to controller mode
      self.sock.send("++auto 0\r") #set instrument to listen (1 is talk)
      self.sock.send("++eoi 1\r") #send EOI signal at end of command
      self.sock.send("++read_tmo_ms 3000\r") #read timeout in milliseconds
      self.change_address(self.address)
      print "Device Initialized"
  
    def change_address(self, address):
        self.address=address
        self.sock.send("++addr "+str(self.address)+"\r")
    
    
    def command(self, comstr):
        self.change_address(self.address)
        self.sock.send(comstr + "\r")
    
    def read(self):
      self.sock.send("++read eoi\r")
      data=[]
      while True:
         try:
            data1 = self.sock.recv(1024)
            data.append(data1)
         except socket.timeout:
            break
      return ''.join(data)

    def read_all(self):
      self.sock.send("++read\r")
      data=[]
      while True:
         try:
            data1 = self.sock.recv(1024)
            data.append(data1)
         except socket.timeout:
            break
      return ''.join(data)

    def query(self, comstr):
        self.command(comstr)
        value = self.read()
        return value
#rfroom - 192.168.1.137
def nfm_sweep(start=10e6, stop=1500e6, step=10e6, smoothing=2, address=8, ip='10.10.10.137'):
  nfm = GPIB(address, to=1, ip=ip)
  npts = int((stop-start)/step + 1)
  data = np.zeros((npts,3))
  nfm.command("F"+str(smoothing))
  freqs = np.arange(start,stop+1, step)
  for i,freq in enumerate(freqs):
    nfm.command("FR"+str(freq)+"HZ")
    result = nfm.query('H1')
    data[i] = np.fromstring(result, dtype=float, sep=',')
    print 'did freq {0}'.format(freq)
  return data 


    

if __name__ == "__main__":
   import sys
   filename = sys.argv[1]
   data = nfm_sweep()
   np.save(filename, data)
   
   
