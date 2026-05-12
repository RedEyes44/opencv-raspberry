import cv2, base64, time, requests
import json

# --- CONFIGURAZIONE ---
FLAG_RICONOSCIMENTO = True  # Metti 'False' se vuoi solo salvare la foto senza riconoscere
API_KEY = "INSERISCI_QUI_LA_TUA_API_KEY"  # La stessa che inserisci nella pagina web
URL_PHP = "http://192.168.134.32/opencv/script.php"

# --- 1) SCATTA FOTO ---
cam = cv2.VideoCapture(0) # apre la webcam USB
time.sleep(0.5) # aspetta che si stabilizzi
ret, frame = cam.read() # cattura un frame
cam.release() # chiude la webcam

if not ret:
    print("❌ Errore: Impossibile catturare l'immagine dalla webcam.")
    exit()

# --- 2) CODIFICA BASE64 ---
# Salva anche in locale per debug
cv2.imwrite('foto.jpg', frame)
_, buffer = cv2.imencode(".jpg", frame) # converte in JPEG
foto_b64 = base64.b64encode(buffer).decode() # codifica in Base64

# --- 3) INVIA AL SERVER PHP ---
payload = {
    "immagine": foto_b64,
    "flag_riconoscimento": FLAG_RICONOSCIMENTO,
    "api_key": API_KEY
}

print("📤 Invio al server in corso...")
try:
    risposta = requests.post(URL_PHP, json=payload, timeout=15)
    
    # --- 4) GESTISCI LA RISPOSTA ---
    if risposta.status_code == 200:
        dati_json = risposta.json()
        
        if FLAG_RICONOSCIMENTO:
            print("\n🔍 JSON DI RICONOSCIMENTO RICEVUTO:")
            print(json.dumps(dati_json, indent=2))
            
            # Qui puoi aggiungere la logica per accendere il LED
            # Esempio: se c'è un risultato valido nel JSON
            # if "result" in dati_json and len(dati_json["result"]) > 0:
            #     print("Persona riconosciuta! Accendo il LED.")
        else:
            print("\n✅ Immagine salvata con successo sul server (Nessun riconoscimento richiesto).")
            print(json.dumps(dati_json, indent=2))
            
    else:
        print(f"❌ Errore dal server. Status Code: {risposta.status_code}")
        print(risposta.text)
        
except Exception as e:
    print(f"❌ Errore di connessione: {e}")
