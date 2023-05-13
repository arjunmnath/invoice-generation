from logging import root
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import json
import os
import uuid
from app.utilis import qrgen
from datetime import datetime
from num2words import num2words
from flask import url_for

with open('app/info.json') as f:
    data = json.load(f)


# border x left start = 20
# border x right start = 575
# border y bottom start = 20
# border y top start = 820

# c = canvas.Canvas(f"hello.pdf", pagesize=A4)
current = data["invoiceNo"]


def invoicegen(
    rootpath,
    conf,
    items,
    name,
    phone,
    houseName='',
    address='',
    placeName='',
    vechileNo='',
    placeOfSupply='',
    terms="CASH"
               ):

    
    FILENAME = f"{str(datetime.now())}.pdf"
    uploads = os.path.join(rootpath, conf, FILENAME)
    c = canvas.Canvas(uploads, pagesize=A4)
    date = str(datetime.now().date())
    time = str(datetime.now().strftime("%H:%M:%S"))
    current[1] = str(int(current[1])+1)
    invoiceNo = "/".join(current)
    c.setAuthor("R.R Traders")
    c.setTitle("R. R Traders Gst Invoice")
    c.setSubject("Gst Invoice")
    # invoice border outline
    c.line(20, 20, 20, 820)
    c.line(20, 820, 575, 820)
    c.line(575, 820, 575, 20)
    c.line(575, 20, 20, 20)

    # invoice top section division
    c.line(20, 700, 575, 700)
    c.line(370, 820, 370, 700)

    # invoice top sub section division
    c.line(20, 620, 575, 620)
    c.line(20, 660, 575, 660)
    c.line(125, 700, 125, 620)
    c.line(227, 700, 227, 620)
    c.line(323, 700, 323, 175)
    c.line(450, 700, 450, 620)

    # invoice items section division
    c.line(20, 502, 575, 502)
    c.line(20, 458, 575, 458)
    c.line(20, 175, 575, 175)
    c.line(42, 502, 42, 175)
    c.line(230, 502, 230, 175)
    c.line(270, 502, 270, 175)
    c.line(374, 502, 374, 175)
    c.line(418, 502, 418, 175)
    c.line(470, 502, 470, 175)
    c.line(516, 502, 516, 175)

    # invoice total gst cal divison
    c.line(20, 155, 575, 155)
    c.line(20, 68, 575, 68)
    c.line(366, 155, 366, 68)

    # invoice static content
    c.setFont("Helvetica-Bold", 28)
    c.drawString(30, 780, data['shopName'])
    c.setFont("Helvetica", 12)
    c.drawString(30, 767, data['subShopInfo'])
    c.drawString(30, 745, data['shopAddress'][0])
    c.drawString(30, 730, data['shopAddress'][1])
    c.drawString(30, 715, data['shopAddress'][2])
    c.setFont("Helvetica-Bold", 13)
    c.drawString(395, 790, f"GSTIN: ")
    c.drawString(395, 745, f"Mobile: ")
    c.drawString(395, 730, f"Ph: ")
    c.setFont("Helvetica", 13)
    c.drawString(37, 680, "Invoice No &")
    c.drawString(55, 667, "Date")
    c.drawString(145, 675, "Vehicle No.")
    c.drawString(252, 680, "Time Of")
    c.drawString(254, 667, "Supply")
    c.drawString(363, 680, "Place Of")
    c.drawString(367, 667, "Supply")
    c.drawString(493, 675, "Terms")
    c.drawString(442, 790, data["gstIn"])
    c.drawString(442, 745, data["mobileNo"])
    c.drawString(420, 730, data["phoneNo"])
    c.drawString(28, 590, "Name And Address Of Purchaser:")
    c.drawString(333, 600, "GSTIN NO:")
    c.drawString(333, 560, "Phone:")
    c.drawString(333, 540, "Fax:")
    c.drawString(333, 520, "Email:")
    c.drawString(25, 485, "SI")
    c.drawString(27, 470, "#")
    c.drawString(82, 477, "Commodity Name")
    c.drawString(237, 483, "Item")
    c.drawString(235, 470, "Code")
    c.drawString(285, 477, "QTY")
    c.drawString(335, 477, "Rate")
    c.drawString(382, 477, "Total")
    c.drawString(433, 477, "Disc")
    c.drawString(480, 485, "GST")
    c.drawString(487, 470, "%")
    c.drawString(520, 485, "Taxable")
    c.drawString(530, 470, "Value")
    c.drawString(60, 160, "Total:")
    c.drawString(30, 120, "Amount In Words:")
    c.drawString(350, 50, "For RR Traders")
    c.setFont("Helvetica", 10)
    c.drawString(500, 35, "Signature")
    c.setFont("Helvetica-Bold", 13)
    c.drawString(420, 130, "CGST:")
    c.drawString(420, 115, "SGST:")
    c.drawString(380, 100, "ADD: Kfc 1%: ")
    c.drawString(427, 80, "Total: ")

    # qr content
    c.drawInlineImage(qrgen(data["qrContent"]),
                      250, 715, height=100, width=100)

    # dynamic contents
    c.setFont("Helvetica", 12)
    c.drawString(30, 565, name.upper())
    c.drawString(30, 550, houseName.upper())
    c.drawString(30, 520, address.upper())
    c.drawString(30, 535, placeName.upper())
    c.drawString(30, 505, phone)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, 645, invoiceNo)
    c.setFont("Helvetica", 13)
    c.drawString(40, 630, date)
    c.drawString(135, 635, vechileNo)
    c.drawString(250, 635, time)
    c.drawCentredString(385, 635, placeOfSupply)
    c.drawString(490, 635, terms)
    if items:
        finTotal = 0
        finQty = 0
        term = 440
        finGst = 0
        for _, x in enumerate(items):
            _total = x['rate'] * x['qty']
            if x['discount'] != 0:
                __total = _total - (_total * (x['discount']/100))

            else:
                __total = _total
            c.drawString(27, term, str(_+1))  # SI no
            c.drawString(55, term, x['name'].upper())
            c.setFont("Helvetica", 10)
            c.drawString(235, term, str(x['item']))
            c.drawString(275, term, str(x['qty'])+' Nos')
            c.drawString(335, term, str(x['rate']))
            c.drawString(378, term, str(_total))
            c.drawString(433, term, str(x['discount'])+" %")
            c.drawString(480, term, str(x['gst'])+" %")
            c.drawString(520, term, str(__total))

            c.setFont("Helvetica", 13)

            finTotal += __total
            finQty += x['qty']
            term -= 20
            finGst += __total * ((x['gst']/2)/100)
        if finGst != 0:            
            kfc = int(finTotal * 0.01)
        else:
            kfc = 0         
        sumTotal = finTotal + (finGst * 2) + kfc
        c.drawString(275, 160, str(finQty)+" Nos")
        c.drawRightString(570, 160, str(finTotal))
        c.setFont("Helvetica-Bold", 13)
        c.drawRightString(570, 130, str(int(finGst)))
        c.drawRightString(570, 115, str(int(finGst)))
        c.drawRightString(570, 100, str(kfc))
        c.setFont("Helvetica-Bold", 16)
        _sumTotal = str(round(sumTotal))
        if len(_sumTotal) <= 3:
            pass
        elif len(_sumTotal) <= 5:
            _sumTotal = _sumTotal[::-1]
            _ = _sumTotal[:3] + ',' + _sumTotal[3:]
            _sumTotal = _[::-1]
        elif len(_sumTotal) <= 7:
            _sumTotal = _sumTotal[::-1]
            _ = _sumTotal[:3] + ',' + _sumTotal[3:5]+','+_sumTotal[5:]
            _sumTotal = _[::-1]

        c.drawRightString(570, 80, "Rs: " + _sumTotal)
        c.setFont("Helvetica", 13)
        var = num2words(round(sumTotal))
        if len(var) > 52:
            Atvar = var[52]
            if Atvar == ' ':
                fvar = [var[:52], var[53:]]
                _term = 100
                for x in fvar:
                    c.drawString(30, _term, x)
                    _term -= 20
            elif Atvar != ' ':
                i = 51
                while True:
                    _atVar = var[i]
                    if _atVar == ' ':
                        break
                    else:
                        i -= 1
                fvar = [var[:i], var[i+1:]]
                _term = 100
                for x in fvar:
                    c.drawString(30, _term, x)
                    _term -= 20
        else:
            c.drawString(30, 100, var)                    
    c.showPage()
    c.save()
    with open('info.json', 'w') as fp:
        json.dump(data, fp, indent=4)
    return FILENAME

