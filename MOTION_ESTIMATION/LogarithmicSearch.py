import sys
import numpy as np

'''
    Algorithmos logarithmikis anazhthshs
        diairoume thn eikona se 16*16 makroblock
        Briskoume ta dianusmata gia kathe makroblock:
            se kathe macroblock:
                briskoume to kalutero tairiasma metaxu twn duo frames 
                me bash th metrikh SAD kai th logarithmikh anazhthsh:
                    1)me bash ena step k psaxnoume th mikroterh diafora 
                    2)an to mikrotero den einai sto kentro tote phgainoume s auto to 
                    eikonostoixeio kai to k paramenei stathero
                    3)an einai sto kentro tote k=k/2 kai sugkrinoume eikonostoixeia pio konta sto kentro 
                    4)an k=1 telos
                apothikeusai to dianusma pou dhlwnei se poia thesh exei metakinithei to makroblock ap 
                to prohgoumeno plaisio 
'''
class LogSearch:
    def __init__(self,target_picture, referenced_picture,n=16,step=8):
        self.target_picture = target_picture #plaisio stoxos
        self.referenced_picture = referenced_picture #prohgoumeno plasio
        self.n = n #to megethos kathe makroblock
        self.x = 0 #suntetagmenes pou tha mas bohthisoun sto poitioning
        self.y = 0
        self.step=step
        
    def position(self, i, j): #gia na briskoume th thesh tou eikonostoixeio me bash to makroblock pou exetazoume
        y = self.y + i
        x = self.x + j
        return y, x

    def _macroblock(self, i, j,isTarget=True): #gia na mporoume na pairnoume to macroblock pou brisketai eite 
        y, x = self.position(i, j)              #eite sto prohgoumeno plaisio eite sto trexon
        if isTarget: #an einai plaisio stoxou
            return list(reversed(self.target_picture))[y][x]
        else: #an prohgoumeno
            return list(reversed(self.referenced_picture))[y][x]

    def SAD(self,n,m): #sum absolute value
        sum=0.0
        target_picture=None
        target_picture=self.target_picture

        y, x = self.position(n,m) #briskoume tis suntetagmenes tou
        
        #epeidh to padding einai problhma, exoume ena exupno tropo na elegxoume ta oria
        #an xefugei tote prosthetoume th pio megalh timh wste na sigoureutoume oti de tha einai to pio mikro athroisma
        if x>=len(target_picture[0]) or x<0 or y>=len(target_picture) or  y<0:
            sum =sum + sys.float_info.max/10
        else: #an einai entos oriwn prosthetoume apla thn apoluth diafora tous
            sum = sum + np.abs(self._macroblock(n,m,isTarget=False)-self._macroblock(n,m))
        return sum

    #briskoume ta dianusmata
    def motionVector(self):
        n_start = 0
        m_start = 0
        min_value = sys.float_info.max 

        stop=0
        n = n_start
        m = m_start
        step = self.step

        while(stop==0):

            min_value = self.SAD(n,m)
            
            #logarithmikh anazhthsh, sugkriseis twn 9 eikonostoixeiwn
            #   #   #

            #   #   # 

            #   #   #
            for i in range(n-step,n+step+1,step):   
                if(i==n): #sugkrinoume prwta auta pou einai panw katw aristera kai dexia tou kentrou
                    for j in range(m-step,m+step+1,step):
                        value = self.SAD(i,j)
                        [n,m,value,min_value]=self.findMinLocation(n,m,i,j,value,min_value)
                else: #gia ta plagia
                    value = self.SAD(i,m)
                    temp=m
                    [n,m,value,min_value]=self.findMinLocation(n,m,i,temp,value,min_value)
            #exoume brei tis nees suntetagmenes

            if([n,m] == [n_start,m_start]): #an einai to kentro tote pairnoume to miso toy step
                step=int(step/2)
            if([n,m]!=[n_start,m_start]): #an den einai to kentro sunexizoume
                n_start=n
                m_start=m
            if(step ==1): #an to step ginei 1 stamatame
                 stop=1
        
        #teleutaia logarithmikh anazhthsh gia ta pleon 8 pio kontina stoixeia tou kentrou
        ###
        ###
        ###
        min_value = self.SAD(n,m)
        
        for i in range(n-step,n+step+1,step):
            for j in range(m-step,m+step+1,step):
                value = self.SAD(i,j)
                [n,m,value,min_value]=self.findMinLocation(n,m,i,j,value,min_value)
        
        return [n,m]

    #gia na brisoume th sugkrish me th mikroterh timh
    def findMinLocation(self,n,m,i,j,value,min_value): 
        if value<min_value:
            min_value=value
            n=i
            m=j
        return [n,m,value,min_value]

    #gia kathe macroblock apothikeuoume to dianusma tou
    def motionEstimation(self):

        target_picture=None
        target_picture=self.target_picture

        y_macroblocks = int(len(target_picture)/ self.n)
        x_macroblocks = int(len(target_picture[0])/ self.n)
        
        result = []
        for y in range(y_macroblocks):
            row = []
            for x in range(x_macroblocks):
                self.x = x * self.n
                self.y = y * self.n
                vector=self.motionVector()
                row.append(vector)
            result.append(row)
        return result

    #anakataskeuazoume thn eikona n+1
    def ReconstructImage(self, remove=False): #to remove xrhsimeuei gia na afairesoume to antikeimeno
        background=None

        target_picture=None 
        target_picture=self.target_picture
        helper=target_picture.shape[0]-1
        
        referenced_picture=None 
        referenced_picture=self.referenced_picture
        
        y_macroblocs = int(len(target_picture) / self.n)
        x_macroblocs = int(len(target_picture[0]) / self.n)
        
        makblocks_Vectors = self.motionEstimation() #briskoume ta dianusmata
        
        for y_ in range(y_macroblocs):
            for x_ in range(x_macroblocs):
                x = x_ * self.n
                y = y_ * self.n
                offset_y = makblocks_Vectors[y_][x_][1] #ta dianusmata
                offset_x = makblocks_Vectors[y_][x_][0]
                if((offset_y!=0 or offset_x!=0) and remove==False): #gia na elaxistopoihsoume to xrono, elegxoume poia den einai 0 kathws den exei nohma 
                    for n1 in range(self.n):    #na asxolhthoume me ta mhdenika kathws shmainei oti den allaxan thesh 
                        for m1 in range(self.n):
                            ey = y + n1 #oi nees suntetagmenes 
                            ex = x + m1 
                            
                            #se periptwsh pou bgei ektos oriwn
                            if ey < 0 or len(referenced_picture) <= ey or ex < 0 or len(referenced_picture[0]) <= ex:
                                continue
                            cy = y - offset_y #oi suntetagmenes sto prohgoumeno plaisio
                            cx = x - offset_x

                            #se periptwsh pou bgei ektos oriwn
                            if cy < 0 or len(referenced_picture) <= cy or cx < 0 or len(referenced_picture[0]) <= cx:
                                continue
                            #anakataskeuasoume to plaisio
                            target_picture[helper-ey][ex] =referenced_picture[helper-cy][cx]
                else:#an theloume na afairesoume to stoixeio
                    for n1 in range(self.n):    
                        for m1 in range(self.n):
                            ey = y + n1 #oi nees suntetagmenes 
                            ex = x + m1 
                            
                            #se periptwsh pou bgei ektos oriwn
                            if ey < 0 or len(referenced_picture) <= ey or ex < 0 or len(referenced_picture[0]) <= ex:
                                continue
                            cy = y - offset_y #oi suntetagmenes sto prohgoumeno plaisio
                            cx = x - offset_x

                            #se periptwsh pou bgei ektos oriwn
                            if cy < 0 or len(referenced_picture) <= cy or cx < 0 or len(referenced_picture[0]) <= cx:
                                continue
                            
                            #anakataskeuasoume to plaisio
                            if (offset_y==0 or offset_x==0):#pairnoume to plaisio me to mhdeniko dianusma
                                background=referenced_picture[helper-cy][cx]
                            else: #kai to prosthetoume ekei pou uparxei kinhsh
                                target_picture[helper-ey][ex]=background
        return target_picture