import requests #import library request
import json #import library json
from flask import Flask, render_template, url_for, request #hanya mengimport beberapa bagian = flask, render_template, url_for, request

app = Flask(__name__) #name dijadikan objek untuk app yang akan digunakan pada app.route
data = requests.get('https://dekontaminasi.com/api/id/covid19/hospitals').json() #sebagai tempat menuliskan url untuk mengambil data real dr api dengan menambahkan fungsi json agar dapat dikonversikan

prov = [] #parameter prov untuk menampung provinsi dari data yang sudah kita ambil diatas
for i in data:
    prov.append(i['province'])
   
@app.route('/') #app route dengan tanda slash yg akan menampilkan tampilan pertama kita
def home(): #fungsi home yang akan memanggil isi dari template home.html kita, dengan rs = data api yg akan mengirimkan data sehingga dpt ditampilkan dlm home.html
    return render_template('home.html', rs = data, judul='Home') 

@app.route('/cari/', methods = ['POST', 'GET']) #ketika kita mencari, maka akan tampil dari cari.html dgn 2 metode = post, get
def cari():
    if request.method == 'POST': #jika kita request metodenya dengan post, maka kita akan menginputkan provinsi yg kita inginkan akan masuk ke variable cari
        cari = request.form['cari']
        new_list = list(filter(lambda x: (x['province'] == cari), data)) #varibel newlist yang menggunakan list filter dan juga lambda, dimana jika variable cari yg kita inputkan misal papua dan lambda x = provinsi cari data dengan nama province papua akan difilter dan dimasukan kedalam list dengan variable new list
        return render_template('cari.html', rs = new_list, judul='Cari Data') #selanjutkan akan di return pada template file cari.html dimana rs = new list yg akan terlihat
        
    else:
        cari = request.args.get('cari') #akan mengembalikan nilai dari parameter "cari". Jika parameter "cari" tidak ditemukan, maka fungsi akan mengembalikan nilai None.

@app.route('/cari-data/')
def caridata():
    q = set(prov)
    p = list(map(lambda x: 'Provinsi ' + x, sorted(q)))
    #maka akan muncul data prov mana aja yg menyediakan untuk rs covid 19, karena ada data yg kembar disatu prov maka kita membuat variable q dengan set prov agar data prov tdk ada yg ngulang, selanjutnya variable p menampung list, pada list p data q dengan nama² prov tadi akan di sorted dengan ascending yaitu dari a-z yg akan masuk ke lambda, data yg sudah disorted akan masuk ke lambda akan masuk ke provinsi, misal x = kalimantan selatan, maka akan menjadi Provinsi Kalsel
    return render_template('cariutama.html', x = p, judul='Cari data') #untuk menampilkan difile cari utama

if __name__ == '__main__':
    app.run(debug=True, port="2123")

#high order function , Web Aplication