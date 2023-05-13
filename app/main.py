from flask import Flask, redirect, render_template, url_for, request, send_from_directory
from app.invoice import invoicegen
import json
import os
import pymongo

with open('app/products.json') as f:
    data = json.load(f)

client = pymongo.MongoClient("mongodb+srv://admin:XyjNKns9G3Hyh7Tm@shopbackend.ocgcx.mongodb.net/rr_traders")
db = client.rr_traders
products = db.products


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


def createFile(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
    with open(uploads, 'a') as f:
        pass
    return uploads

@app.route('/files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

@app.route("/pdfgen", methods=['GET', 'POST'])
def pdfgen():
    print(request.url)
    _term = []
    name = request.form.get('name')
    houseName = request.form.get('hname')
    address = request.form.get('address')
    phone = request.form.get('phone')
    placeName = request.form.get('placeName')
    vehicleNo = request.form.get('vehicleNo')
    placeOfSupply = request.form.get('Pos')
    terms = request.form.get('terms')
    code1 = request.form.get('1code')
    code2 = request.form.get('2code')
    code3 = request.form.get('3code')

    qty1 = request.form.get('1qty')
    qty2 = request.form.get('2qty')
    qty3 = request.form.get('3qty')

    dis1 = request.form.get('1dis')
    dis2 = request.form.get('2dis')
    dis3 = request.form.get('3dis')
    if code1 != '':
        try:
            code = data[code1]
            print(code)
            if dis1 == '':
                dis1 = 0
            temp = {
                'name': code['name'],
                'item': int(code1),
                'qty':int(qty1),
                'discount': int(dis1),
                'rate':int(code['rate']),
                'gst': 0

            }
            _term.append(temp)
        except KeyError:
            print('not found')      
    if code2 != '':
        try:
            code = data[code2]
            print(code)
            temp = {
                'name': code['name'],
                'item': int(code2),
                'qty':int(qty2),
                'discount': int(dis2),
                'rate':int(code['rate']),
                'gst': 0

            }
            _term.append(temp)
        except KeyError:
            print('not found')      
    if code3 != '':
        try:
            code = data[code3]
            print(code)
            temp = {
                'name': code['name'],
                'item': int(code3),
                'qty':int(qty3),
                'discount': int(dis3),
                'rate':int(code['rate']),
                'gst': 0

            }
            _term.append(temp)
        except KeyError:
            print('not found')            
    # print(cname1, cname2,cname3, houseName, address, phone, placeName, vehicleNo, placeOfSupply, terms)
    file = invoicegen(app.root_path, app.config['UPLOAD_FOLDER'],
        _term, address=address, houseName=houseName, placeName=placeName, name=name, phone=phone,
               vechileNo=vehicleNo, placeOfSupply=placeOfSupply, terms=terms)
    return redirect(url_for('download', filename=file))
    

@app.route('/sales/', methods=['POST'])
def sales():
    data = request.get_json()
    return data
@app.before_first_request
def bef():
    app.config['UPLOAD_FOLDER'] = '/tmp'

if __name__ == '__main__':    
    app.run(debug=True)
