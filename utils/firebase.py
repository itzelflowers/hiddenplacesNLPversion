import pyrebase

class Firebase:
    def __init__(self):
        # Configuración actualizada con tus nuevos datos
        self._firebaseConfig = {
            'apiKey': "AIzaSyB2Q3IbCkMcpVm-7Aj6UTkv6FLFQzL3udI",
            'authDomain': "hiddenplacesnlp.firebaseapp.com",
            # Nota: La databaseURL suele ser https://[PROJECT_ID]-default-rtdb.firebaseio.com/
            'databaseURL': "https://hiddenplacesnlp-default-rtdb.firebaseio.com",
            'projectId': "hiddenplacesnlp",
            'storageBucket': "hiddenplacesnlp.firebasestorage.app",
            'messagingSenderId': "185162167479",
            'appId': "1:185162167479:web:9143c09904a344f2390932"
        }
        # Inicialización de Firebase
        self._firebase = pyrebase.initialize_app(self._firebaseConfig)
    
    def getFirebase(self):
        return self._firebase
    
    def getdb(self):
        return self._firebase.database()
    
    def getauth(self):
        return self._firebase.auth()
    
    def getstorage(self):
        return self._firebase.storage()