import pyrebase

def get_token():
    config = {
        "apiKey": "AIzaSyC--anxL74t3h78q7ZSVPMPipv2m244kBg",
        "authDomain": "kitetoken-ca4cb.firebaseapp.com",
        "databaseURL": "https://kitetoken-ca4cb-default-rtdb.firebaseio.com",
        "projectId": "kitetoken-ca4cb",
        "storageBucket": "kitetoken-ca4cb.appspot.com",
        "messagingSenderId": "369939516780",
        "appId": "1:369939516780:web:17b2f6a31a6a802a453749",
        "measurementId": "G-DCVB5QCJ1Q"
    }
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password('kamble.s@sabertoothtech.in','Somy@1234')
    user = auth.refresh(user['refreshToken'])

    db = firebase.database()
    #
    tok=db.child("tokens").get().val()['token']
    print(tok)
    return tok