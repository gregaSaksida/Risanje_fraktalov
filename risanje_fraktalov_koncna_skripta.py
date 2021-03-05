import numpy as np
import matplotlib.pyplot as plt
barva = 'inferno'

with open('podatki_o_slikah.txt', 'a') as datoteka:
        datoteka.write(130 * '=' + '\n' + 130 * '=' + '\n')

def ustvari_fraktal(sirina_slike, visina_slike, iteracije, x_min, x_max, y_min, y_max):
    ix, iy = np.mgrid[0:sirina_slike, 0:visina_slike]
    x = np.linspace(x_min, x_max, sirina_slike)[ix]
    y = np.linspace(y_min, y_max, visina_slike)[iy]
    
    c = x + complex(0, 1)*y
    
    img = np.zeros(c.shape, dtype=int)
    
    velikost = sirina_slike*visina_slike
    ix.shape = velikost
    iy.shape = velikost
    c.shape = velikost
    
    z = np.copy(c)
    for i in range(iteracije):
        if i % 500 == 0:
            print(i)
        if not len(z):
            break
        #z = z*z + c
        np.multiply(z, z, z)
        np.add(z, c, z)
        rem = abs(z) > 2.0
        img[ix[rem], iy[rem]] = i+1
        rem = ~rem
        z = z[rem]
        ix, iy = ix[rem], iy[rem]
        c = c[rem]
    img[img == 0] = iteracije + 1
    sredina = np.median(img)
    img2 = img - sredina
    predznaki = np.sign(img2)
    #img = ((np.log(abs(img - sredina) + 1)) * predznaki)
    img = np.log(img)
    return img

#################################################
#################################################

import tkinter as tk
from PIL import Image, ImageTk
import time

def nova_velikost(slika):
    sirina_zaslona = okno.winfo_screenwidth()
    visina_zaslona = okno.winfo_screenheight()
    sirina_slike, visina_slike = slika.size
    razmerje_slike = sirina_slike / visina_slike
    popravek = 0.9
    if sirina_zaslona / sirina_slike > visina_zaslona / visina_slike:
        return (int(popravek*sirina_slike * visina_zaslona / visina_slike), int(popravek*visina_zaslona))
    else:
        return (int(popravek*sirina_zaslona), int(popravek*visina_slike * sirina_zaslona / sirina_slike))

def srediscne_koordinate(koordinate, dimenzije_slike, kompleksno_sredisce, razpon):
    abscisa, ordinata = koordinate
    sirina_slike, visina_slike = dimenzije_slike
    sirina_zaslona = okno.winfo_screenwidth()
    visina_zaslona = okno.winfo_screenheight()
    nova_abscisa = abscisa - sirina_zaslona / 2
    nova_ordinata = visina_slike / 2 - ordinata
    
    kompleksna_abscisa = kompleksno_sredisce[0] + (razpon[0] / sirina_slike) * nova_abscisa
    kompleksna_ordinata = kompleksno_sredisce[1] + (razpon[1] / visina_slike) * nova_ordinata
    
    return (kompleksna_abscisa, kompleksna_ordinata)


sirina_slike = 400
visina_slike = 400
iteracije = 400
x_min, x_max, y_min, y_max = -2, 1, -1.5, 1.5
sredisce = ((x_max + x_min)/2, (y_max + y_min)/2)
zaporedna_slika = 1

def zamenjaj_sliko():
    global razpon
    global iteracije
    global x_min
    global x_max
    global y_min
    global y_max
    global sirina_slike
    global visina_slike
    global nova_slika
    
    abscisa, ordinata = float(vhod_abscisa.get()), float(vhod_ordinata.get())
    razpon = float(vhod_razpon.get())
    iteracije = int(vhod_iteracije.get())
    sirina_slike, visina_slike = int(vhod_sirina_slike.get()), int(vhod_visina_slike.get())
    x_min, x_max, y_min, y_max = (abscisa - razpon/2, abscisa + razpon/2,
                                  ordinata - razpon/2, ordinata + razpon/2)
    nova_slika = ustvari_sliko(sirina_slike, visina_slike, iteracije, x_min, x_max, y_min, y_max)
    platno.itemconfig(slika_prikazana, image=nova_slika)

def ustvari_sliko(sirina_slike, visina_slike, iteracije, x_min, x_max, y_min, y_max):
    global zaporedna_slika
    
    with open('podatki_o_slikah.txt', 'a') as datoteka:
        datoteka.write('{0}, {1}, {2}, {3}, {4}, {5}, {6} '.format(
            sirina_slike, visina_slike, iteracije, x_min, x_max, y_min, y_max))
    
    zacetek = time.time()
    fraktal = ustvari_fraktal(sirina_slike, visina_slike, iteracije, x_min, x_max, y_min, y_max)
    fraktal_prikaz = plt.imshow(fraktal.T, origin='lower', extent=[x_min, x_max, y_min, y_max], cmap=barva, interpolation='bicubic')
    fraktal_prikaz.write_png('fraktal{0}.png'.format(zaporedna_slika))
    slika = Image.open('fraktal{0}.png'.format(zaporedna_slika))
    zaporedna_slika += 1
    slika = slika.resize(nova_velikost(slika))
    slika = ImageTk.PhotoImage(slika)
    
    preteceni_cas = time.time() - zacetek
    with open('podatki_o_slikah.txt', 'a') as datoteka:
        datoteka.write('{0}\n'.format(preteceni_cas))
    print(preteceni_cas)
    
    return slika

def posodobi_gumbe(posodobi_vse=True):
    vhod_abscisa.delete(0, 'end')
    vhod_ordinata.delete(0, 'end')
    vhod_abscisa.insert(0, str(sredisce[0]))
    vhod_ordinata.insert(0, str(sredisce[1]))
    if posodobi_vse:
        vhod_razpon.delete(0, 'end')
        vhod_iteracije.delete(0, 'end')
        vhod_sirina_slike.delete(0, 'end')
        vhod_visina_slike.delete(0, 'end')
        vhod_razpon.insert(0, str(x_max - x_min))
        vhod_iteracije.insert(0, str(iteracije))
        vhod_sirina_slike.insert(0, str(sirina_slike))
        vhod_visina_slike.insert(0, str(visina_slike))
    return None

def ponastavi():
    global sredisce
    sredisce = ((x_max + x_min)/2, (y_max + y_min)/2)
    posodobi_gumbe()
    return None

okno = tk.Tk()
slika = ustvari_sliko(sirina_slike, visina_slike, iteracije, x_min, x_max, y_min, y_max)
sirina_zaslona = okno.winfo_screenwidth()
visina_zaslona = okno.winfo_screenheight()

platno = tk.Canvas(width=0.95*sirina_zaslona, height=0.95*visina_zaslona)
platno.pack(expand='yes', fill='both')

slika_prikazana = platno.create_image(sirina_zaslona/2, 0, image=slika, anchor="n")

ukazni_stolpec = tk.Frame(platno)
ukazni_stolpec.pack(side='right')
tk.Label(ukazni_stolpec, text='abscisa sredisca').grid(row=0, column=0)
tk.Label(ukazni_stolpec, text='ordinata sredisca').grid(row=1, column=0)
tk.Label(ukazni_stolpec, text='razpon sredisca').grid(row=2, column=0)
tk.Label(ukazni_stolpec, text='stevilo iteracij').grid(row=3, column=0)
tk.Label(ukazni_stolpec, text='sirina_slike').grid(row=4, column=0)
tk.Label(ukazni_stolpec, text='visina_slike').grid(row=5, column=0)

vhod_abscisa = tk.Entry(ukazni_stolpec)
vhod_ordinata = tk.Entry(ukazni_stolpec)
vhod_razpon = tk.Entry(ukazni_stolpec)
vhod_iteracije = tk.Entry(ukazni_stolpec)
vhod_sirina_slike = tk.Entry(ukazni_stolpec)
vhod_visina_slike = tk.Entry(ukazni_stolpec)

vhod_abscisa.grid(row=0, column=1)
vhod_ordinata.grid(row=1, column=1)
vhod_razpon.grid(row=2, column=1)
vhod_iteracije.grid(row=3, column=1)
vhod_sirina_slike.grid(row=4, column=1)
vhod_visina_slike.grid(row=5, column=1)

posodobi_gumbe()

def vrni_koordinate(event):
    #outputting x and y coords to console
    koordinate = (event.x, event.y)
    dimenzije_slike = (slika.width(), slika.height())
    kompleksno_sredisce = ((x_max + x_min)/2, (y_max + y_min)/2)
    razpon = (x_max - x_min, y_max - y_min)
    global sredisce
    sredisce = srediscne_koordinate(koordinate, dimenzije_slike, kompleksno_sredisce, razpon)
    posodobi_gumbe(posodobi_vse=False)
    return None

platno.bind("<Button 1>", vrni_koordinate)
gumb = tk.Button(ukazni_stolpec, text='Narisi!', command=zamenjaj_sliko).grid(row=6, column=1)
gumb = tk.Button(ukazni_stolpec, text='Ponastavi na trenutno sliko.',
                 command=ponastavi).grid(row=7, column=1)

okno.mainloop()