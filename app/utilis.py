import qrcode

def qrgen(text):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(text)        
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

# url = "mongodb+srv://cyberhoax:fAB5eb8SS75TWAm@cluster0.b6bqs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
import pymongo


# client = pymongo.MongoClient(url)

products.insert_one(
    {
        "productId": 1106, 
        "name": "6ft 8mm plain asbestos sheet",
        "rate": 600,
        "type": 'asbestos sheet',
        "currentStock": 0
    }
)

{
    "orderId": 1,
    "customername": "arjun Manjunath",
    "housename": None,
    "address": None,
    "phone": 7025062976,
    'vechicle': 55
}


print(db.list_collection_names())