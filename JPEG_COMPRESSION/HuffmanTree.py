import numpy as np
from scipy.misc import imread,imresize
import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter
import queue

'''
    algorithmos huffman tree
    briskoume tis pithanothtes kathe noumerou (h logikh einai oti auto pou emfanizetai suxnotera prepei na apotuponetai ligoteres fores)
    ftiaxnoume to dentro:
        pairnoumee kathe fora tis duo mikroteres pithanothtes kai tis prosthetoume
        se kathe prosthesh dhmiourgeitai enas neos desmos
        molis ftasoume sth riza stamatame
    anatrexoume to dentro
        ston aristero desmo bazoume 1 kai sto dexi 0

'''

class Node:
    def __init__(self):
        self.prob=None 
        self.code=None
        self.data=None
        self.left=None
        self.right=None
    #einai special methods pou kalountai molis ginei dhmioyrgia fyllou
    #kai exoyn ws skopo na deixoun to pws prepei kapoia antikeimena na sumperiferontai
    def __lt__(self,other): #edw deixnoume pws prepei na sumperiferetai otan einai mikrotero apo
        #h methodos einai polu xrhsimei wste h lista sto telos na einai se auxousa seira 
        #dld kathe fora elegxoume ta fylla kai blepoume pio einai to mikrotero
        if(self.prob < other.prob):
            return 1
        else:
            return 0

#ftiaxnoume to dentro
def tree(probabilities):
    prq=queue.PriorityQueue() #apotelei mia lista pou kathe fora pou tha zhtame(get) tha fernei to stoixeio
    #me thn upshloterh proteraiothta dld to fullo me to mikrotero probability
    #einai mia FIFO (first-in-first-out) 
    for i,probabilities in enumerate(probabilities):
        leaf=Node() #ftiaxnoume to fyllo
        leaf.data=i
        leaf.prob=probabilities
        prq.put(leaf) #pairname to fullo sth parapanw lista
        
    while(prq.qsize()>1): #otan exoume brei ta duo fulla ayta ta opoia einai apo prin 
        n_node=Node()   #ayta me tis mikroteres pithanothtes. ftiaxnoume to kainourgio fullo
        l=prq.get()     #aristero fullo
        r=prq.get()     #dexi fullo

        n_node.left=l  
        n_node.right=r
        n_prob=l.prob+r.prob #prosthetoume tis pithanothtes tous 
        n_node.prob=n_prob  #kai etsi bazoume sto kainourgio fullo mas to athroisma twn pithanothtwn
        prq.put(n_node) #to prosthetoume sth lista
    #h diadikasia epanalambanetai mexri na ftasoume sth riza
    return prq.get() #gurname pisw th lista pou ftiaxame wste na anatrexoume to dentro

#anatrexoume to dentro
def huffman_traversal(root_node): 
    if(root_node.left is not None): #an exei aristero desmo
        huffman_traversal.count+=1 #+1 mia thesh bit
        huffman_traversal(root_node.left) #metakinhsou sta aristera
        huffman_traversal.count-=1 #an den uparxei afairese ena kathws to exoume pprosthesei sthn arxh
    if (root_node.right is not None): #an exei dexi desmo
        huffman_traversal.count+=1 #+1 bit
        huffman_traversal(root_node.right) #metakinhsou dexia
        huffman_traversal.count-=1
    else: #an ftasame se fullo
        #apothikeuoume to mexri twra apotelesma
        huffman_traversal.output_bits[root_node.data]=huffman_traversal.count
        
    return

huffman_traversal.output_bits = np.empty(256,dtype=int) #o pinakas me ta bits pou tha gurisoume
huffman_traversal.count=0