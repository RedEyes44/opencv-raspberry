<?php
// Legge il JSON inviato dal Python (Raspberry Pi)
$dati = json_decode(file_get_contents("php://input"), true);

// Controlla che il campo "immagine" sia presente
if (empty($dati["immagine"])) {
    http_response_code(400);
    echo json_encode(["response" => false, "messaggio" => "Immagine mancante"]);
    exit;
}

// Estrae i parametri aggiuntivi
$flag_riconoscimento = isset($dati["flag_riconoscimento"]) ? $dati["flag_riconoscimento"] : false;
$api_key = isset($dati["api_key"]) ? $dati["api_key"] : "";

// Salva la foto decodificata su disco
$foto = base64_decode($dati["immagine"]);
$filename = "foto_" . time() . ".jpg";
// Assicurati che PHP abbia i permessi di scrittura in questa cartella
file_put_contents($filename, $foto);

header("Content-Type: application/json");

// Se il flag è TRUE, procediamo col riconoscimento
if ($flag_riconoscimento === true) {
    if (empty($api_key)) {
        echo json_encode(["error" => "API Key mancante. Impossibile eseguire il riconoscimento."]);
        exit;
    }

    // Prepara la chiamata cURL verso il motore di riconoscimento (CompreFace o simile)
    $url_api = 'http://127.0.0.1:8000/api/v1/recognition/recognize';
    
    // Crea un oggetto file da inviare in multipart/form-data
    $cfile = new CURLFile(realpath($filename), 'image/jpeg', 'file');
    $post_data = ['file' => $cfile];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url_api);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    // Passa l'API key negli header esattemente come faceva l'HTML
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "x-api-key: " . $api_key
    ]);

    $risultato_api = curl_exec($ch);
    $errore_curl = curl_error($ch);
    curl_close($ch);

    if ($risultato_api === false) {
        // Se l'API non risponde (es. container spento)
        echo json_encode([
            "error" => "Impossibile contattare l'API su localhost:8000",
            "dettaglio" => $errore_curl
        ]);
    } else {
        // Stampa esattamente il JSON grezzo restituito dall'API (verrà catturato da Python)
        echo $risultato_api;
    }

} else {
    // Se il flag è FALSE, rispondiamo solo con la conferma di salvataggio
    echo json_encode([
        "response" => true, 
        "messaggio" => "Foto salvata correttamente senza analisi.",
        "file_name" => $filename
    ]);
}
?>
