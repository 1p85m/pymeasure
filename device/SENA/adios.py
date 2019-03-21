#! /usr/bin/env python2.6
#-*- coding: utf-8 -*-

"""
AD,IOの入出力を行う

============================================
 Radio Telescope Observing System
--------------------------------------------
[Abstract]

 file-name:adios.py

 role: AD,IOの入出力

 main-author: H.Tsuji, H.Onoe

 directory-tree:

--------------------------------------------
[Detail Description]

・構成
　公開しているクラスは以下のとおり。
　(1)

--------------------------------------------
[History]

 2011/11/21 H.tsuji, H.Onoe 作成

--------------------------------------------
"""
import socket,time,numpy
import communicator

class adio(object):
    '''
    AD and IO
    '''
    
    def __init__(self, com):
        self.com = com
        pass
    
    def _set_att(self, no, value):
        self.com.open()
        self.com.send(att["att%d_%ddB" %(no, value)])
        self.com.close()
        return

    def get_att1(self):
        self.com.open()
        self.com.send(off['level_off'])
        while True:
            try:
                temp = self.com.recv()
                temp1 = temp.decode()
                if temp.find(b':')==0:
                    break
                else:
                    break
            except:
                print('(error) att1')
                break
        self.com.close()
        time.sleep(0.1)
        
        do1 = int(temp1[-16])*1
        do2 = int(temp1[-15])*2
        do3 = int(temp1[-14])*4
        do4 = int(temp1[-13])*8
        do5 = int(temp1[-11])*16
        att1 = do1+do2+do3+do4+do5
        return att1

    def get_att2(self):
        self.com.open()
        self.com.send(off['level_off'])
        while True:
            try:
                temp = self.com.recv()
                temp1 = temp.decode()
                if temp.find(b':')==0:
                    break
                else:
                    break
            except:
                print('(error) att2')
                break
        self.com.close()
        time.sleep(0.1)    

        do6 = int(temp1[-10])*1
        do7 = int(temp1[-9])*2
        do8 = int(temp1[-8])*4
        do9 = int(temp1[-6])*8
        do10 = int(temp1[-5])*16
        att2 = do6+do7+do8+do9+do10
        return att2

    
    def gen_lrc(code):
        c2d = lambda ascii:int(binsascii.b2a_hex(char),16)
        lrc = c2d(code[0])^c2d(code[1])  
        for c in code[2:]:lrc = lrc^c2d(c)
        return'%X'%lrc

    
    def get_level(self):
        self.com.open()
        self.com.send(off['level_off'])
        while True:
            try:
                temp = self.com.recv()
                if temp.find(':')==-1: continue
                else: pass
                #print temp
                break
            except communicator.CommunicatorTimeout:
                print('(error) if level')
                continue
            continue
        time.sleep(0.1)
        
        ch1 = float(temp[7:11])*(5./1024)
        ch2 = float(temp[13:17])*(5./1024)
        ch3 = float(temp[19:23])*(5./1024)
        ch4 = float(temp[25:29])*(5./1024)
        self.level = {'ch1':ch1, 'ch2':ch2, 'ch3':ch3, 'ch4':ch4}
        self.com.close()
        return self.level,temp
  
    def get_measure(self):
        self.com.open()
        
        # -- get_att1
        self.com.send(off['level_off'])
        while True:
            try:
                temp = self.com.recv()
                if temp.find(':')==-1: continue
                else: pass
                #print temp
                break
            except communicator.CommunicatorTimeout:
                print('(error) att1')
                continue
            continue
        do1 = int(temp[-16])*1
        do2 = int(temp[-15])*2
        do3 = int(temp[-14])*4
        do4 = int(temp[-13])*8
        do5 = int(temp[-11])*16
        att1 = do1+do2+do3+do4+do5
        
        
        # -- get_att2
        self.com.send(off['level_off'])
        while True:
            try:
                temp = self.com.recv()
                if temp.find(':')==-1: continue
                else: pass
                break
            except communicator.CommunicatorTimeout:
                print('(error) att2')
                continue
            continue
        do6 = int(temp[-10])*1
        do7 = int(temp[-9])*2
        do8 = int(temp[-8])*4
        do9 = int(temp[-6])*8
        do10 = int(temp[-5])*16
        att2 = do6+do7+do8+do9+do10
        
        
        # -- get_level
        self.com.send(off['level_off'])
        while True:
            try:
                temp = self.com.recv()
                temp1 = temp.decode()
                if temp.find(b':')==0:
                    break
                else:
                    break
            except:
                print('(error) if level')
                break
        ch1 = float(temp1[7:11])*(5./1024)
        ch2 = float(temp1[13:17])*(5./1024)
        ch3 = float(temp1[19:23])*(5./1024)
        ch4 = float(temp1[25:29])*(5./1024)
        self.level = {'ch1':ch1, 'ch2':ch2, 'ch3':ch3, 'ch4':ch4}
        
        self.com.close()
        
        return {'att1': att1, 'att2': att2, 'ifmonitor': self.level}
    
    def get_ad(self, integsec=1 ,repeat=1):
        ad1 = []
        ad2 = []
        ad3 = []
        ad4 = []
        
        self.com.open()
        for i in range(repeat):
            ret_ad1 = []
            ret_ad2 = []
            ret_ad3 = []
            ret_ad4 = []
            start_time = time.time()
            i=1
            while time.time()-start_time < integsec:
                a = time.time()-start_time
                i += 1
                self.com.send(off['level_off'])
                while True:
                    try:
                        temp = self.com.recv()
                        #print temp
                        if temp.find(':')==-1: continue
                        else: pass
                        break
                    except communicator.CommunicatorTimeout:
                        continue
                    continue

                ch1 = float(temp[7:11])*(5./1024)
                ch2 = float(temp[13:17])*(5./1024)
                ch3 = float(temp[19:23])*(5./1024)
                ch4 = float(temp[25:29])*(5./1024)
                ret_ad1.append(ch1)
                ret_ad2.append(ch2)
                ret_ad3.append(ch3)
                ret_ad4.append(ch4)
                continue
            ad1.append(numpy.average(ret_ad1))
            ad2.append(numpy.average(ret_ad2))
            ad3.append(numpy.average(ret_ad3))
            ad4.append(numpy.average(ret_ad4))
            continue
        self.com.close()
        ad = {"ad1":ad1, "ad2":ad2, "ad3":ad3, "ad4":ad4}
        return ad

    def get_pll(self):
        #refer to manual_rhio10-v1.4.3.pdf
        #pll = ':'+'03'+'030'+'\x30\x41'+'\r\n'  #chapter 5.3.3.1
        pll = ':030300A\r\n'  #chapter 5.3.3.1
        self.com.open()
        self.com.send(pll)
        while True:
            try:
                pll = self.com.recv() #chapter 5.3.2.2
                if pll.find(':')==-1: continue
                else: pass
                #print pll
                break
            except communicator.CommunicatorTimeout:
                print('(error) pll')
                continue
            continue
        self.com.close()
        return int(pll[30]) #,pll comennt out by K. Tokuda 2013/11/22



##### liblary1 #####code

# attenuator1 : 
# port1 = 1dB
# port2 = 2dB
# port3 = 4dB
# port4 = 8dB
# port5 = 16dB

# attenuator2 : 
# port6 = 1dB
# port7 = 2dB
# port8 = 4dB
# port9 = 8dB
# port10 = 16dB
 
# for get_status
# port9 = off

att = {\
'att1_0dB':":17011111100000,000000000010\r\n",\
'att1_1dB':":17011111100000,100000000011\r\n",\
'att1_2dB':":17011111100000,010000000011\r\n",\
'att1_3dB':":17011111100000,110000000010\r\n",\
'att1_4dB':":17011111100000,001000000011\r\n",\
'att1_5dB':":17011111100000,101000000010\r\n",\
'att1_6dB':":17011111100000,011000000010\r\n",\
'att1_7dB':":17011111100000,111000000011\r\n",\
'att1_8dB':":17011111100000,000100000011\r\n",\
'att1_9dB':":17011111100000,100100000010\r\n",\
'att1_10dB':":17011111100000,010100000010\r\n",\
'att1_11dB':":17011111100000,110100000011\r\n",\
'att1_12dB':":17011111100000,001100000010\r\n",\
'att1_13dB':":17011111100000,101100000011\r\n",\
'att1_14dB':":17011111100000,011100000011\r\n",\
'att1_15dB':":17011111100000,111100000010\r\n",\
'att1_16dB':":17011111100000,000010000011\r\n",\
'att1_17dB':":17011111100000,100010000010\r\n",\
'att1_18dB':":17011111100000,010010000010\r\n",\
'att1_19dB':":17011111100000,110010000011\r\n",\
'att1_20dB':":17011111100000,001010000010\r\n",\
'att1_21dB':":17011111100000,101010000011\r\n",\
'att1_22dB':":17011111100000,011010000011\r\n",\
'att1_23dB':":17011111100000,111010000010\r\n",\
'att1_24dB':":17011111100000,000110000010\r\n",\
'att1_25dB':":17011111100000,100110000011\r\n",\
'att1_26dB':":17011111100000,010110000011\r\n",\
'att1_27dB':":17011111100000,110110000010\r\n",\
'att1_28dB':":17011111100000,001110000011\r\n",\
'att1_29dB':":17011111100000,101110000010\r\n",\
'att1_30dB':":17011111100000,011110000010\r\n",\
'att1_31dB':":17011111100000,111110000011\r\n",\
'att2_0dB':":17010000011111,000000000010\r\n",\
'att2_1dB':":17010000011111,000001000011\r\n",\
'att2_2dB':":17010000011111,000000100011\r\n",\
'att2_3dB':":17010000011111,000001100010\r\n",\
'att2_4dB':":17010000011111,000000010011\r\n",\
'att2_5dB':":17010000011111,000001010010\r\n",\
'att2_6dB':":17010000011111,000000110010\r\n",\
'att2_7dB':":17010000011111,000001110011\r\n",\
'att2_8dB':":17010000011111,000000001011\r\n",\
'att2_9dB':":17010000011111,000001001010\r\n",\
'att2_10dB':":17010000011111,000000101010\r\n",\
'att2_11dB':":17010000011111,000001101011\r\n",\
'att2_12dB':":17010000011111,000000011010\r\n",\
'att2_13dB':":17010000011111,000001011011\r\n",\
'att2_14dB':":17010000011111,000000111011\r\n",\
'att2_15dB':":17010000011111,000001111010\r\n",\
'att2_16dB':":17010000011111,000000000111\r\n",\
'att2_17dB':":17010000011111,000001000110\r\n",\
'att2_18dB':":17010000011111,000000100110\r\n",\
'att2_19dB':":17010000011111,000001100111\r\n",\
'att2_20dB':":17010000011111,000000010110\r\n",\
'att2_21dB':":17010000011111,000001010111\r\n",\
'att2_22dB':":17010000011111,000000110111\r\n",\
'att2_23dB':":17010000011111,000001110110\r\n",\
'att2_24dB':":17010000011111,000000001110\r\n",\
'att2_25dB':":17010000011111,000001001111\r\n",\
'att2_26dB':":17010000011111,000000101111\r\n",\
'att2_27dB':":17010000011111,000001101110\r\n",\
'att2_28dB':":17010000011111,000000011111\r\n",\
'att2_29dB':":17010000011111,000001011110\r\n",\
'att2_30dB':":17010000011111,000000111110\r\n",\
'att2_31dB':":17010000011111,000001111111\r\n",\
}


off = {\
'level_off':":17010000000000,000000000011\r\n",\
}






def calc_LRC(field):
    import binascii
    a2b = lambda a: int(binascii.b2a_hex(a), 16)
    lrc = a2b(field[0]) ^ a2b(field[1])
    for _f in field[2:]: lrc = lrc ^ a2b(_f)
    lrc_hex = '%02X'%(lrc)
    lrc_dict = {'0':'\x30', '1':'\x31', '2':'\x32', '3':'\x33', '4':'\x34',
                '5':'\x35', '6':'\x36', '7':'\x37', '8':'\x38', '9':'\x39', 
                'A':'\x41', 'B':'\x42', 'C':'\x43', 'D':'\x44', 'E':'\x45',
                'F':'\x46'}
    lrc_code = [lrc_dict[_l] for _l in lrc_hex]
    return lrc_code


class adios(object):
    def __init__(self, communicator):
        self.com = communicator
        pass
    
    def _gen_command(self, length, function, data):
        start_flag = ':'
        end_flag = '\r\n'
        command = start_flag + length + function + data
        lrc = calc_LRC(command)
        command = command + lrc + end_flag
        return command
    
    def do_set(self, config='0000000000'):
        """
        Set a digital output conditions.
        
        Required arguments:
        
            *config*: [ str (10 of '1' or '0' characters) ]
                digital output configurations.
                -- (usage) ON ch1,ch2,ch5 :: config='1100100000'
        """
        self.com.send(self._gen_command('23', '01', '%s,%s'%('1'*10, config)))
        return
    
    def do_on(self, ch):
        """
        Set ON digital output channels.
        
        Required arguments:
        
            *ch*: [ int | list of int ]
                ch to be swhich ON.
                
        Return None.
        """
        config = self.do_status()
        for i in ch:
            config[i-1] = 1
            continue
        self.do_set(config)
        return
    
    def do_off(self, ch):
        """
        Set OFF digital output channels.
        
        Required arguments:
        
            *ch*: [ int | list of int ]
                ch to be swhich OFF.
        
        Return None.
        """
        config = self.do_status()
        for i in ch:
            config[i-1] = 0
            continue
        self.do_set(config)
        return
    
    def do_status(self):
        """
        Check current digital I/O status.
        
        No arguments requrired.
        
        Return ...
        """
        return
    
    def get_io(self):
        pass


