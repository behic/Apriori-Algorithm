import itertools
import sys
import os.path
from sys import exit

#verileri oku
##return data[]: dosyadan gelen itemlar
def readfile(DosyaAdi):
    data = []
    with open(DosyaAdi) as dp:
        next(dp)
        for line in dp:
            count = 0
            trans = line[:-1].split(' ',1)
            items = trans[1].split(', ')
            data.append(items)
        dp.close()
    return data


## verileri tara, support değeri küçük olan  itemleri filtrele
def filtrele(itemKumeleri, Sup, data):
    filt_itemKumesi = []
    n = len(data)
    for itemKumesi in itemKumeleri:
        var = 0
        for line in data:
            if set(itemKumesi) <= set(line): 		# itemKumesi trasansaction'da varsa:
                var += 1
        if var >= Sup: 		#Sup koşulunu sağlıyorsa itemKumesini filtrelenlere ekle
            filt_itemKumesi.append(itemKumesi)
    return filt_itemKumesi


##item kümelerini bir sonraki adım için kendileriyle joinle 
def joinle(itemKumeleri):    
    joinKumesi = []
    
    for i in itemKumeleri[:len(itemKumeleri)-1]: #i'ye ilk kümeyi ata,sondan bir önceki kümeye kadar git
        
        index_j = itemKumeleri.index(i) + 1 	#index_j'ye (i+1). kümenin indexini ata. 
        while index_j < len(itemKumeleri): 		#index_j'den son kümeye kadar git
            j = itemKumeleri[index_j]  			

            #i ve j kümelerinin sadece son elemanları farklıysa
            if i[:len(i)-1] == j[:len(j)-1]: 
                #iki kümeyi joinle		
                tmp = i + j[len(j)-1:]			#i kümesini ve j'nin son elemanını al
                if joinKumesi.count(tmp) == 0: 	                    				
                    joinKumesi.append(tmp)
            index_j += 1
    return joinKumesi

## çok geçen item kümelerinden kurallar üret
def kural_uret(ItemKumeleri, data, Conf):
    for itemKumesi in ItemKumeleri:
        i = 1
        if len(itemKumesi) < 2: #item kümesi tek elemandan oluşuyorsa return
            return -1
        while i < len(itemKumesi): #i eleman oluşan itemKumesi üret
            uret = itertools.combinations(itemKumesi, i)# i itemden oluşan kümeler üret
            for j in uret:
                # kümeyi ikiye ayır
                sag = j
                sol = set(itemKumesi) - set(sag)

                solvar, sagvar = 0, 0 #sol kümenin olduğu durumlarda sağ küme var mı				
                for line in data:
                    if sol <= set(line):
                        solvar += 1
                        if set(sag) <= set(line):
                            sagvar += 1
                conf = sagvar/solvar
                if conf >= Conf:
                    print(list(sol), '->', list(sag), ' Confidence Değeri:', "{0:.1f}%".format(conf*100))
            i += 1


if __name__ == "__main__":
    
    # girdi verilerini kontrol et
    if len(sys.argv) != 4:
        print('girdi hatası')
        print('girdi formatı şu şekilde olmalı: python aprior.py DosyaAdi MinimumSup MinumumConf')
        exit()
    if os.path.isfile(sys.argv[1]):
        DosyaAdi = sys.argv[1]
    else:
        print('veri dosyası bulunumadı, tekrar deneyin')
        print('girdi formatı şu şekilde olmalı: DosyaAdi MinimumSup MinumumConf')
        exit()
    if int(sys.argv[2]) > 0:
            Sup = int(sys.argv[2])
    else:
        print('Sup değeri = ', sys.argv[2])
        print('minsup pozitif tamsayı olmalı')
        print('girdi formatı şu şekilde olmalı: DosyaAdi MinimumSup MinumumConf')
        exit()
    if 0 <= float(sys.argv[3]) <= 1:
        Conf = float(sys.argv[3])
    else:
        print('minumun confidence değeri 0 ila 1 arasında olmalı')
        print('girdi formatı şu şekilde olmalı: DosyaAdi MinimumSup MinumumConf')
        exit()
	
	#BASLA
        data = []
	
    data = readfile(DosyaAdi)  # DosyaAdi = 'deneme.txt'
    # kaç farklı item kümesi olduğunu bul
    itemKumeleri = []
    for T in data:
        for I in T:
            if itemKumeleri.count([I]) == 0:
                itemKumeleri.append([I])

    #Tekrar eden elemanları support'a göre filtrele	
    filt_itemKumesi = filtrele(itemKumeleri, Sup, data)
	
    #Yeni item kümesi oluşturamayıncaya kadar
    while filt_itemKumesi != []:
        # kurallar üret
        kural_uret(filt_itemKumesi, data, Conf)           

        # bir sonraki adımdaki adaylar için itemleri joinle, 
        aday_items = joinle(filt_itemKumesi)

        # bir sonraki adım için oluşturulmuş adayları supportlarına göre filtrele
        filt_itemKumesi = filtrele(aday_items, Sup, data)


