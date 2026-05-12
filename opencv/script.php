<?php
// Legge il JSON inviato dal Raspberry Pi
$dati = json_decode(file_get_contents("php://input"), true);

// Controlla che il campo "immagine" sia presente
if (empty($dati["immagine"])) {
    http_response_code(400);
    echo json_encode(["response" => false, "messaggio" => "Immagine mancante"]);
    exit;
}

// Salva la foto decodificata su disco
$foto = base64_decode($dati["immagine"]);
file_put_contents("foto_" . time() . ".jpg", $foto);

// --- QUI metti la tua logica di riconoscimento ---
// Per ora risponde sempre true come esempio
$riconosciuto = true;

// Risponde al Raspberry Pi
header("Content-Type: application/json");
echo json_encode(["response" => $riconosciuto]);
