import collections
import itertools

from bidict import bidict
import numpy as np

#mesa sthn analush exhgw analutika ti kanei to kathena kai se ti xrhsimeuei
EOB = (0, 0) #end of block
ZRL = (15, 0) #zero length length

#epeidh tha girname pisw dictionary gia th kwdikopoihsh twn DC kai AC prepei an exoyme ta kleidia 
DC = 'DC' 
AC = 'AC'

class Encoder:
    def __init__(self, data):
        '''
        tha kwdikopoihsoume thn eikona me bash to huffman table pou pairnoume ap to biblio
        pairnoume to DC pou apotelei to prwto stoixeio kathe block kai meta th diafora tous
        kai kwdikopoioume 
        Meta to AC pou einai ola ta upoloipa stoixeia kai kwdikopoioume me mhkos diadromhs
        '''
        #h eikona
        self.data = data

        #h lista pou perilambanei tis diafore me ta DC twn blocks
        self.dc_diff = None

        #h lista me ta length leght kwdikopoihseis twn AC.
        self.AC_lengthLength = None

    #ta properties tha mas bohthisoun kathws leitourgoun ws ena shortcut gia na gine set mia timh
    #dld kathe fora pou ftiaxnoume ena neo antikeimeno de xreiazetai na kalesoume ta setters giati me ta 
    #property ennoeitai kai etsi glitwnoume grammes
    @property
    def diff_dc(self):
        if self.dc_diff is None:
            self.GET_DC()
        return self.dc_diff

    @property
    def lengthLength_ac(self):
        if self.AC_lengthLength is None:
            self.GET_AC()
        return self.AC_lengthLength

    @diff_dc.setter #ta setters twn DC,AC
    def diff_dc(self, value):
        self.dc_diff = value

    @lengthLength_ac.setter
    def lengthLength_ac(self, value):
        self.AC_lengthLength = value

    #ta getters ta opoia kalountai mazi me ta setters kai etsi me to property pou analusame parapanw
    #kalountai ola auta molis ftiaxthei to antikeimeno kai etsi de xreiazetai na kaloume sunexeia oles aytes tis sunarthseis 
    def GET_DC(self):
        #upologizoume th diafora twn DC twn diaforwn blocks(to prwto stoixeio kathws einai auto me th megaluterh timh)
        #kai to kwdikopoioume (dld kanoume DPCM) 
        self.dc_diff = tuple(DC_enc(self.data[:, 0, 0]))

    def GET_AC(self):
        #upologizoume ta AC me length length kwdikopoihsh
        self.AC_lengthLength = []

        #gia kathe block trexoume zig zag algorithmo gia ola ta stoixeia tou AC 
        for block in self.data:
            self.AC_lengthLength.extend(
                AC_RunLength_enc(tuple(ZigZag_Algorithm(block))[1:])
            )
    def encode(self):
        '''
        h kwdikopoihsh twn DC kai AC opws eipame kai parapanw ginetai me bash to 
        jpeg huffmana pinaka. Edw gurname ena dictionary me to duadikh roh twn DC:01 kai AC:01
        '''        
        entropy_enc = {}
        '''pairnoume th duadikh roh twn DC,AC mesw huffman ap tis listes pou 
           proekupsan sthn arxikopoihsh'''
        #mas sumferei na einai string
        #edw afou exoume parei prwta ta prapanw kaloume th sunarthsh pou tha ta kwdikopoihsh kata huffman
        entropy_enc[DC] = ''.join(encode_huffman(v)
                          for v in self.diff_dc)
        entropy_enc[AC] = ''.join(encode_huffman(v)
                          for v in self.lengthLength_ac)
        return entropy_enc

#telos klashs

def encode_huffman(value):
    """Kwdikopoihsh huffman

    pairnoume ta DC, AC ws bit kai ta kwdikopoioume sumfwna me tous pinakes huffman
    """
    #briskoume th thesh tou value sto pinaka me ta ranges 
    def get_HuffmanRange(table, target):
        for i, row in enumerate(table):
            for j, element in enumerate(row):
                if target == element:
                    return (i, j)
        raise ValueError('error:de mporei na brei to range')
    '''
        gia na xehwrisoume an h timh pou pairnoume antistoixei se DC h AC
        prepei na doume an milame gia lista h akeraia timh.
        Xeroume oti to DC tha einai kapoio int enw to AC tha einai mia lista 
        me to mhkos tou poses fores emfanistike enas arithmos
    '''
    #elegxoume an einai lista, dld tupou collection.iterable
    if not isinstance(value, collections.Iterable):  # afou den einai ara einai DC
        if value <= -2048 or value >= 2048:
            raise ValueError(
                'uparxei error giati to DC einai para polu megalo'
            )
        #briskoume th thesh tou value mesa sto pinaka
        size, code = get_HuffmanRange(HUFFMAN_CATEGORIES, value)

        #me bash th thesh gurname thn antistoixh kwdikopoihsh
        if size == 0:#an einai to prwto dld value=0
            return HUFFMAN_CATEGORY_CODEWORD[DC][size]

        return (HUFFMAN_CATEGORY_CODEWORD[DC][size]
                + '{:0{padding}b}'.format(code, padding=size))
    else:   # afou einai lista einai AC 
        value = tuple(value)
        if value == EOB or value == ZRL: #an to AC einai kapoio ap ta duo special sumbola gurname amesws th kwdikopoihsh 
            return HUFFMAN_CATEGORY_CODEWORD[AC][value]

        length, key = value
        if key == 0 or key <= -1024 or key >= 1024:
            raise ValueError(
                'error: to AC anhkei mono sto diasthma (-1024,0)u(0,1024)'
            )
        #antistoixa me DC
        size, code = get_HuffmanRange(HUFFMAN_CATEGORIES, key)
        return (HUFFMAN_CATEGORY_CODEWORD[AC][(length, size)]
                + '{:0{padding}b}'.format(code, padding=size))

def DC_enc(block):
    #upologizoume th diafora twn DC me ta prohgoumena block kai gurname to pinaka pou dhmiourgoume 
    return (
        (item - block[i - 1]) if i else item
        for i, item in enumerate(block)
    )

#o algorithmos mhkous diadromhs
#tha mas bohthisei na diagrapsoume ta peritta stoixeia dld to 0
def AC_RunLength_enc(block):
    #pairname to block to opoio omws  prwta exoume anatrexei me zig zag 
    #epita h metablhth group krata poses fores emfnisthke autos o arithmos px (63,0) dld to 0 emfanisthke 63 fores
    #den einai 64 gt to prwto stoixeio panta einai to DC
    groups = [(len(tuple(group)), key)
              for key, group in itertools.groupby(block)]
    
    ret = []
    helper = False  #tha th xrhsimopoihsoume gia ta zeugaria tou epomenou group pou to kleidi tous den einai mhden.
    
    #epeidh h metablhth einai tuple kai mporoumee xwris na xeroume to mhkos ths listas na exetasoume 
    #to teleutaio stoixeio
    if groups[-1][1] == 0:#an einai to 0 to teleutaio stoixeio oses fores kai na emfanizetai, sbhsto gt einai peritto 
        del groups[-1]
    #gia ta upoloipa, to length edw xrhsimopoieitai gia na metrame ton arithmo twn stoixeiwn pou den exoun kwdikopoihthei akomh 
    for i, (length, key) in enumerate(groups):
        if  helper== True:#an brethei tetoio zeugari pou to kleidi toy den einai to 0
            length -= 1   
            helper = False
        if length == 0:#an to mhkos ginei 0 paei sto epomeno group 
            continue
        if key == 0:#an o arithmos autos einai to 0
            #an to mhkos einai megalutero apo 16 tote xrhsimopoieitai h kwdikopoish zrl
            #exhgw toys logous sthn analush 
            while length >= 16:
                ret.append(ZRL)
                length -= 16
            ret.append((length, groups[i + 1][1]))#an einai mikrotero apo 16 tha kwdikopoihthoume meta me tous non zero suntelestes AC
            helper = True #sigoura to epomeno de tha einai 0 opote kai to thetoume true
        else: #an den einai 0 tote thetoume mhkos 0 gt mas endiaferoun ta axrhsta mhdenika
            ret.extend(((0, key), ) * length)
    return ret + [EOB] #prosthetoume sto telos to special sumbolo EOB(end of block)

#o zig zag algorithmos
def ZigZag_Algorithm(data):
    if data.shape[0] != data.shape[1]:#o algorithmos de mporei na doulepsei an to block den einai tetragwno
        raise ValueError('den einai tetragwnh h mhtra')
    x, y = 0, 0 #arxikopoihsh
    for i in np.nditer(data): #anti na exoume duo epanalhpshs pairnoume ta stoixeia tou block kai ta bazoume se mia grammh
        yield data[y][x] #fwrtonoume sth sunarthsh th timh tou array, to yield de tha kanei amesws return
        '''
        o algorithmos:
            1)allaxe kateuthinsh molis bretheis sta oria tou block px [i,0]
            2)proxwra diagwnia oso briskeis peritto h zugo athroisma suntetagmenwn
            3)an einai peritto kai ftaseis sta oria tote prosthese +1 sta x 
            alliws +1 sta y
            4)epanelabe
        '''
        if (x + y) % 2 == 1:
            x, y = move_zig_zag(x, y, data.shape[0])
        else:
            y, x = move_zig_zag(y, x, data.shape[0])

def move_zig_zag(i, j, size):
    if j < (size - 1): #otan den einai sta ora tou block
        return (max(0, i - 1), j + 1)
    #otan ftasei sta oria
    return (i + 1, j)

#parakatw einai oloi oi pinakes kwdikopoihshs gia huffman me bash to biblio
#tha anaptuxthoun kai sthn analush
HUFFMAN_CATEGORIES = (
    (0, ),
    (-1, 1),
    (-3, -2, 2, 3),
    (*range(-7, -4 + 1), *range(4, 7 + 1)),
    (*range(-15, -8 + 1), *range(8, 15 + 1)),
    (*range(-31, -16 + 1), *range(16, 31 + 1)),
    (*range(-63, -32 + 1), *range(32, 63 + 1)),
    (*range(-127, -64 + 1), *range(64, 127 + 1)),
    (*range(-255, -128 + 1), *range(128, 255 + 1)),
    (*range(-511, -256 + 1), *range(256, 511 + 1)),
    (*range(-1023, -512 + 1), *range(512, 1023 + 1)),
    (*range(-2047, -1024 + 1), *range(1024, 2047 + 1)),
    (*range(-4095, -2048 + 1), *range(2048, 4095 + 1)),
    (*range(-8191, -4096 + 1), *range(4096, 8191 + 1)),
    (*range(-16383, -8192 + 1), *range(8192, 16383 + 1)),
    (*range(-32767, -16384 + 1), *range(16384, 32767 + 1))
)

HUFFMAN_CATEGORY_CODEWORD = {
    DC: bidict({
            0:  '00',
            1:  '010',
            2:  '011',
            3:  '100',
            4:  '101',
            5:  '110',
            6:  '1110',
            7:  '11110',
            8:  '111110',
            9:  '1111110',
            10: '11111110',
            11: '111111110'
        }),
    AC: bidict({
            EOB: '1010',  #(0, 0)
            ZRL: '11111111001',  #(15, 0)

            (0, 1):  '00',
            (0, 2):  '01',
            (0, 3):  '100',
            (0, 4):  '1011',
            (0, 5):  '11010',
            (0, 6):  '1111000',
            (0, 7):  '11111000',
            (0, 8):  '1111110110',
            (0, 9):  '1111111110000010',
            (0, 10): '1111111110000011',

            (1, 1):  '1100',
            (1, 2):  '11011',
            (1, 3):  '1111001',
            (1, 4):  '111110110',
            (1, 5):  '11111110110',
            (1, 6):  '1111111110000100',
            (1, 7):  '1111111110000101',
            (1, 8):  '1111111110000110',
            (1, 9):  '1111111110000111',
            (1, 10): '1111111110001000',

            (2, 1):  '11100',
            (2, 2):  '11111001',
            (2, 3):  '1111110111',
            (2, 4):  '111111110100',
            (2, 5):  '1111111110001001',
            (2, 6):  '1111111110001010',
            (2, 7):  '1111111110001011',
            (2, 8):  '1111111110001100',
            (2, 9):  '1111111110001101',
            (2, 10): '1111111110001110',

            (3, 1):  '111010',
            (3, 2):  '111110111',
            (3, 3):  '111111110101',
            (3, 4):  '1111111110001111',
            (3, 5):  '1111111110010000',
            (3, 6):  '1111111110010001',
            (3, 7):  '1111111110010010',
            (3, 8):  '1111111110010011',
            (3, 9):  '1111111110010100',
            (3, 10): '1111111110010101',

            (4, 1):  '111011',
            (4, 2):  '1111111000',
            (4, 3):  '1111111110010110',
            (4, 4):  '1111111110010111',
            (4, 5):  '1111111110011000',
            (4, 6):  '1111111110011001',
            (4, 7):  '1111111110011010',
            (4, 8):  '1111111110011011',
            (4, 9):  '1111111110011100',
            (4, 10): '1111111110011101',

            (5, 1):  '1111010',
            (5, 2):  '11111110111',
            (5, 3):  '1111111110011110',
            (5, 4):  '1111111110011111',
            (5, 5):  '1111111110100000',
            (5, 6):  '1111111110100001',
            (5, 7):  '1111111110100010',
            (5, 8):  '1111111110100011',
            (5, 9):  '1111111110100100',
            (5, 10): '1111111110100101',

            (6, 1):  '1111011',
            (6, 2):  '111111110110',
            (6, 3):  '1111111110100110',
            (6, 4):  '1111111110100111',
            (6, 5):  '1111111110101000',
            (6, 6):  '1111111110101001',
            (6, 7):  '1111111110101010',
            (6, 8):  '1111111110101011',
            (6, 9):  '1111111110101100',
            (6, 10): '1111111110101101',

            (7, 1):  '11111010',
            (7, 2):  '111111110111',
            (7, 3):  '1111111110101110',
            (7, 4):  '1111111110101111',
            (7, 5):  '1111111110110000',
            (7, 6):  '1111111110110001',
            (7, 7):  '1111111110110010',
            (7, 8):  '1111111110110011',
            (7, 9):  '1111111110110100',
            (7, 10): '1111111110110101',

            (8, 1):  '111111000',
            (8, 2):  '111111111000000',
            (8, 3):  '1111111110110110',
            (8, 4):  '1111111110110111',
            (8, 5):  '1111111110111000',
            (8, 6):  '1111111110111001',
            (8, 7):  '1111111110111010',
            (8, 8):  '1111111110111011',
            (8, 9):  '1111111110111100',
            (8, 10): '1111111110111101',

            (9, 1):  '111111001',
            (9, 2):  '1111111110111110',
            (9, 3):  '1111111110111111',
            (9, 4):  '1111111111000000',
            (9, 5):  '1111111111000001',
            (9, 6):  '1111111111000010',
            (9, 7):  '1111111111000011',
            (9, 8):  '1111111111000100',
            (9, 9):  '1111111111000101',
            (9, 10): '1111111111000110',
            # A
            (10, 1):  '111111010',
            (10, 2):  '1111111111000111',
            (10, 3):  '1111111111001000',
            (10, 4):  '1111111111001001',
            (10, 5):  '1111111111001010',
            (10, 6):  '1111111111001011',
            (10, 7):  '1111111111001100',
            (10, 8):  '1111111111001101',
            (10, 9):  '1111111111001110',
            (10, 10): '1111111111001111',
            # B
            (11, 1):  '1111111001',
            (11, 2):  '1111111111010000',
            (11, 3):  '1111111111010001',
            (11, 4):  '1111111111010010',
            (11, 5):  '1111111111010011',
            (11, 6):  '1111111111010100',
            (11, 7):  '1111111111010101',
            (11, 8):  '1111111111010110',
            (11, 9):  '1111111111010111',
            (11, 10): '1111111111011000',
            # C
            (12, 1):  '1111111010',
            (12, 2):  '1111111111011001',
            (12, 3):  '1111111111011010',
            (12, 4):  '1111111111011011',
            (12, 5):  '1111111111011100',
            (12, 6):  '1111111111011101',
            (12, 7):  '1111111111011110',
            (12, 8):  '1111111111011111',
            (12, 9):  '1111111111100000',
            (12, 10): '1111111111100001',
            # D
            (13, 1):  '11111111000',
            (13, 2):  '1111111111100010',
            (13, 3):  '1111111111100011',
            (13, 4):  '1111111111100100',
            (13, 5):  '1111111111100101',
            (13, 6):  '1111111111100110',
            (13, 7):  '1111111111100111',
            (13, 8):  '1111111111101000',
            (13, 9):  '1111111111101001',
            (13, 10): '1111111111101010',
            # E
            (14, 1):  '1111111111101011',
            (14, 2):  '1111111111101100',
            (14, 3):  '1111111111101101',
            (14, 4):  '1111111111101110',
            (14, 5):  '1111111111101111',
            (14, 6):  '1111111111110000',
            (14, 7):  '1111111111110001',
            (14, 8):  '1111111111110010',
            (14, 9):  '1111111111110011',
            (14, 10): '1111111111110100',
            # F
            (15, 1):  '1111111111110101',
            (15, 2):  '1111111111110110',
            (15, 3):  '1111111111110111',
            (15, 4):  '1111111111111000',
            (15, 5):  '1111111111111001',
            (15, 6):  '1111111111111010',
            (15, 7):  '1111111111111011',
            (15, 8):  '1111111111111100',
            (15, 9):  '1111111111111101',
            (15, 10): '1111111111111110'
        }),
}
