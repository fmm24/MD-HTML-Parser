#import sys
import re 

"""
mogli smo i da unosimo iz komandne linije
f = open(sys.argv[1],"r"), postupak ostaje isti
"""


try:
    f = open("input.md","r")
except IOError:
    print("Greska")
    exit(1)

fajl = f.read()
i=0

#patterni za celine koje treba prepoznati
#izmedju () ce nam se nalaziti odgovarajuce grupe koje cemo kasnije koristiti zbog neophodnog ispisa

boldovano = re.compile("(\*{2}|_{2})(.+?)(\*{2}|_{2})")         #ovako cemo prepoznati sve boldovane celine
precrtana = re.compile("~~(.*)~~")                             
italic = re.compile("(\*{1}|_{1})([^\*_\s]+)(\*{1}|_{1})")
BoldItalic = re.compile(r'(\*)\1{2}(.+?)\1(.*?)\1{2}')          # ovo je za slucaj ***rec***, tj kada celinu treba i boldovati i "iskositi", slicno se mogu odraditi i ostale kombinacije
horizontalno = re.compile(r'[-\*_]{3}\n')                 # tri uzastopna - * _ daju horizonatlni brejk, ali samo na pocetku linije, u sredini ne
mono = re.compile("`([^`]+)`")
linkovi = re.compile("\[(.*)\]\((.*)\)")
naslovi = re.compile(r"\A(#{1,6})\s([a-zA-Z0-9]+)\n")                      # headings imaju velicine od 1 do 6, sto se izrazava odg brojem taraba, samo na pocetku reda
linebreak = re.compile("\s\s\n")                                # dve beline na kraju linije proizvode line break
PLinija = re.compile("\n\n")                 # prazne linije ce nam sluziti za zatvaranje jednog i otvaranje drugog paragrafa
                                
UlazakUl =re.compile(r'(\w|\s)*:\n\s\*')    #ovo ce oznacavati pocetak bucket liste
elementUL = re.compile(r'\s\*\s(\w|\s)+\n')

UlazakOl = re.compile(r'(\w|\s)*:\n\s\d\.')
elementOL = re.compile(r'\s\d\.\s(\w|\s)+\n')

citiranje = re.compile(r'>(\w|\s)+\n')


novifajl = "<!DOCTYPE html>\n<html>\n<body>\n<p>"          #upisujemo u pocetak html fajla
while i<len(fajl):                        #citamo redom iz ulazne datoteke i pokusavamo da uparimo sa odgovarajucim patterinma                 
        
    if BoldItalic.match(fajl[i:]):
        m=BoldItalic.match(fajl[i:])
        novifajl = novifajl + "<strong><em>" + m.group(2)+"</em></strong>"
        i=i+len(m.group())

    elif boldovano.match(fajl[i:]):
        m = boldovano.match(fajl[i:])
        novifajl = novifajl + "<strong>"+m.group(2)+"</strong>"
        i = i +len(m.group())

    elif precrtana.match(fajl[i:]):
        m = precrtana.match(fajl[i:])
        novifajl = novifajl + "<strike>"+m.group(1)+"</strike>"
        i = i +len(m.group())

    elif italic.match(fajl[i:]):
        m = italic.match(fajl[i:])
        novifajl = novifajl + "<em>"+m.group(2)+"</em>"
        i = i +len(m.group())

    elif mono.match(fajl[i:]):
        m = mono.match(fajl[i:])
        novifajl = novifajl + "<code>"+m.group(1)+"</code>"
        i = i +len(m.group())

    elif linkovi.match(fajl[i:]):
        m=linkovi.match(fajl[i:])
        ime = str(m.group(1))
        link = str(m.group(2))
        novifajl = novifajl + "<a href="+link+">"+ime+"</a>" 
        i = i+len(m.group())

    elif PLinija.match(fajl[i:]):
        m=PLinija.match(fajl[i:])
        novifajl = novifajl + "</p>\n<p>"
        i = i+len(m.group())

    elif naslovi.match(fajl[i:]):                           #naslove/headings mozemo klasifikovati po broj # koje se pojavljuju i prevesti u odg html naslove
        m = naslovi.match(fajl[i:])
        j=0
        j=len(m.group(1))
        novifajl = novifajl + "<h"+str(j)+">"+m.group(2)+"</h"+str(j)+">"
        i = i+len(m.group())

    
    elif UlazakUl.match(fajl[i:]):                       # citacemo prvo liniju koja ce nam oznaciti ulaz u ul, zatim ulazimo u petlju sve dok se regex slaze sa sledecim redom, stampamo odgova-
        m=UlazakUl.match(fajl[i:])                       # rajuci ispisi, koristeci ono sto smo matchovali
        i = i+len(m.group())-2
        novifajl = novifajl+str(m.group())[0:len(str(m.group()))-1]+"\n<ul>\n"
        while elementUL.match(fajl[i:]):
            k=elementUL.match(fajl[i:])
            novifajl = novifajl + "<li>"+str(k.group())[2:len(k.group())-1]+"</li>\n"
            i=i+len(k.group())
            
        novifajl = novifajl + "</ul>"

    elif UlazakOl.match(fajl[i:]):                       # analogan postupak UL
        m=UlazakOl.match(fajl[i:])
        i = i+len(m.group())-3
        novifajl = novifajl+str(m.group())[0:len(str(m.group()))-2]+"\n<ol>\n"
        while elementOL.match(fajl[i:]):
            k=elementOL.match(fajl[i:])
            novifajl = novifajl + "<li>"+str(k.group())[3:len(k.group())-1]+"</li>\n"
            i=i+len(k.group())

        novifajl = novifajl + "</ol>"
    
    elif citiranje.match(fajl[i:]):                     #slican koncept kao za ul/ol, samo sada koristimo sam reg izraz za ulazak u petlju
        m=citiranje.match(fajl[i:])
        i = i+len(m.group())
        novifajl = novifajl + "<blockquote><p>"+str(m.group())[1:]
        while citiranje.match(fajl[i:]):
            k = citiranje.match(fajl[i:])
            novifajl = novifajl + str(k.group())[1:]
            i = i +len(k.group())
        novifajl = novifajl + "</p></blockquote>"

    elif horizontalno.match(fajl[i:]):
        novifajl = novifajl + "<hr />"
        i=i+3

    elif linebreak.match(fajl[i:]):
        m=linebreak.match(fajl[i:])
        novifajl = novifajl + "<br />"
        i=i+len(m.group())
   
    else:
        novifajl = novifajl + fajl[i]                           # ako ne pripada nijednom patternu, onda znaci da je deo obicnog teksta, samo ga prepisujemo 
        i=i+1
    


novifajl +="</p>\n</body>\n</html>"                             # kompletiramo odgovarajuci html fajl
try:
    f = open("output.html","w")                                  # otvaramo fajl u koji treba upisati novi sadrzaj
except IOError:                                                 # hvatamo izuzetke
    exit(1)

f.write(novifajl)
f.close()



"""
Komentari:
-Ovakav nacin je jedna od ideja, pored ovoga sam jos imao ideju da mozda prvo ucitam sve iz ulazne datoteke
kao jedan veliki string, i onda odatle da "vadim" pomocu odgovarajucih regularnih izraza, takodje samo imao
neke ideje i preko ugradjenih re.sub(), medjutim ipak samo se odlucio da pustim brojac kroz ceo fajl i tako 
koriscenjem regexa matchujem odgovarajuce stvari

-Pretpostavio sam da pre ucitavanja same organizovane/neorganizovane liste moraju
stajati :, bar je tako uvek bilo na ulaznim primerima, procedura je slicna ukoliko
ne moraju, samo bi ucitavali prvu liniju na koju naletimo koja zadovoljava elementUL
ili elementOL i onda ponovo ulazili u while petlju, prakticno identicno procestu za blockquoting
, dodatno napravio sam pretpostavku da su odredjene tj neodredjene liste formata 
belina/(broj ili zvezdica)/belina/element liste , tako sam bar zakljucio iz primera ulaza

-Postojalo je dosta stvari na koje sam trebao da obratim paznju, i dosta drugacijih nacina da se u markdownu
prave iste stvari, na primer nisu u celosti odradjene sve kombinacije modova bold,italic i strikethorugh, ali
se svi rade analogno primeru kada u isto vreme i boldujemo i italikujemo celinu, samo bi bilo potrtebno jos 
par regularnih izraza, izvinjavam se ukoliko sam napravio jos neki previd ili nesto nisam implementirao,a trebao
sam,uglavnom sam se vodio primerima ulaznih fajlova koji ste mi slali na mejl.

"""



