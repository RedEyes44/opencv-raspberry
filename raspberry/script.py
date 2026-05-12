import cv2, base64, time, requests
 
# --- 1) SCATTA FOTO ---
cam = cv2.VideoCapture(0) # apre la webcam USB
time.sleep(0.5) # aspetta che si stabilizzi
_, frame = cam.read() # cattura un frame
cam.release() # chiude la webcam
 
# --- 2) CODIFICA BASE64 ---
cv2.imwrite('foto.jpg', frame)
_, buffer = cv2.imencode(".jpg", frame) # converte in JPEG
foto_b64 = base64.b64encode(buffer).decode() # codifica in Base64
 
print(foto_b64)
 
URL = "http://192.168.134.32/opencv/script.php"
 
risposta = requests.post(URL, json={"immagine": foto_b64}, timeout=10)
 
# --- 3) INVIA AL SERVER ---
# ---  risposta = requests.post(URL, json={&quot;immagine&quot;: foto_b64}, timeout=10)
 
# --- 4) ACCENDI IL LED SE RISPOSTA OK ---
# --- if risposta.status_code == 200 and risposta.json().get(&quot;response&quot;) ==
# --- True:
# --- print(&quot;Riconosciuto! LED acceso.&quot;)
# --- GPIO.output(PIN_LED, GPIO.HIGH)
# --- time.sleep(3)
# --- GPIO.output(PIN_LED, GPIO.LOW)
# --- GPIO.cleanup()
# --- print(&quot;Fine.&quot;)
 
 
