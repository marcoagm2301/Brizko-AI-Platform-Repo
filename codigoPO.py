import json

def main(lista_llm: str) -> dict:
    try:
        datos_llm = json.loads(lista_llm)
    except Exception:
        datos_llm = {"items_extraidos": []}
    # 'catalogo' contiene la lista de todos los elementos que se encuentran en el archivo "productslist.csv"
    catalogo = {
        'SKU-ARDU0': {'nombre': 'Arduino Uno R3 Compatible', 'precio': 8.5, 'stock': 65},
        'SKU-BLU05': {'nombre': 'Módulo Bluetooth HC-05', 'precio': 4.8, 'stock': 14},
        'SKU-BREAD': {'nombre': 'Protoboard de 830 Puntos', 'precio': 2.9, 'stock': 180},
        'SKU-CAB10': {'nombre': 'Kit de Cables Jumper (100pcs)', 'precio': 2.5, 'stock': 150},
        'SKU-CASE4': {'nombre': 'Carcasa de Acrílico para RPi4', 'precio': 3.9, 'stock': 19},
        'SKU-DHT22': {'nombre': 'Sensor Temperatura y Humedad', 'precio': 3.8, 'stock': 110},
        'SKU-DRV88': {'nombre': 'Driver A4988 para Motor', 'precio': 1.8, 'stock': 500},
        'SKU-ESP32': {'nombre': 'ESP32 Development Board', 'precio': 12.5, 'stock': 120},
        'SKU-FAN05': {'nombre': 'Ventilador 5V para Gabinete', 'precio': 1.75, 'stock': 75},
        'SKU-INTR0': {'nombre': 'Sensor Infrarrojo de Presencia', 'precio': 1.5, 'stock': 80},
        'SKU-KA220': {'nombre': 'Cautín Eléctrico Lápiz 60W', 'precio': 12.0, 'stock': 22},
        'SKU-KEY44': {'nombre': 'Teclado Matricial 4x4 Membrana', 'precio': 1.2, 'stock': 300},
        'SKU-LCD16': {'nombre': 'Pantalla LCD 16x2 con I2C', 'precio': 5.2, 'stock': 40},
        'SKU-MOT02': {'nombre': 'Servomotor MG996R', 'precio': 6.8, 'stock': 45},
        'SKU-MULT0': {'nombre': 'Multímetro Digital Básico', 'precio': 15.5, 'stock': 12},
        'SKU-NANO3': {'nombre': 'Arduino Nano CH340', 'precio': 4.2, 'stock': 0},
        'SKU-OLED1': {'nombre': 'Pantalla OLED 0.96 I2C', 'precio': 3.1, 'stock': 200},
        'SKU-PSU12': {'nombre': 'Fuente de Poder 12V 5A', 'precio': 18.9, 'stock': 15},
        'SKU-REL04': {'nombre': 'Módulo Relé de 4 Canales', 'precio': 4.5, 'stock': 90},
        'SKU-RESI0': {'nombre': 'Kit de Resistencias (600pcs)', 'precio': 5.5, 'stock': 400},
        'SKU-RFID0': {'nombre': 'Módulo Lector RFID RC522', 'precio': 4.0, 'stock': 25},
        'SKU-RPI4': {'nombre': 'Raspberry Pi 4 4GB', 'precio': 45.0, 'stock': 8},
        'SKU-SEN01': {'nombre': 'Sensor Ultrasónico HC-SR04', 'precio': 2.2, 'stock': 350},
        'SKU-STEP0': {'nombre': 'Motor a Pasos NEMA 17', 'precio': 14.2, 'stock': 30},
        'SKU-WIFI0': {'nombre': 'Módulo WiFi ESP8266 ESP-01', 'precio': 2.1, 'stock': 95}
    }

    # Se crea la lista para almacenar los productos
    orden_validada = []
    
    # Elementos disponibles en 'catalogo'
    items = datos_llm.get("items_extraidos", [])
    
    # Ciclo for que permite identificar con excepciones los productos/elementos que se encuentran en nuestro catalogo.
    # Las condiciones if/else de este ciclo nos permiten identificar y comparar los elementos del archivo 'ProductsList.csv' con lo que el usuario ingresa en la herramienta de IA (prompt)
    for item in items:
        nombre = item.get("Nombre", "Desconocido")
        sku = item.get("SKU", "MISSING").strip()
        
        try:
            cantidad = int(item.get("Cantidad", 0))
        except:
            cantidad = 0
            
        try:
            precio_solicitado = float(item.get("Precio Solicitado", 0.0))
        except:
            precio_solicitado = 0.0
        
        estado_item = "APROBADO"
        comentario = "Coincide plenamente con catálogo oficial."
        
        if sku not in catalogo:
            estado_item = "ERROR_SKU"
            comentario = f"El SKU '{sku}' no existe en nuestro catálogo."
        else:
            datos_oficiales = catalogo[sku]
            precio_oficial = datos_oficiales["precio"]
            stock_actual = datos_oficiales["stock"]
            
            if precio_solicitado != precio_oficial:
                estado_item = "DISCREPANCIA_PRECIO"
                comentario = f"Error en precio. Solicitado: ${precio_solicitado:.2f} USD | Oficial: ${precio_oficial:.2f} USD."
            elif stock_actual == 0:
                estado_item = "SIN_STOCK"
                comentario = f"El artículo se encuentra AGOTADO (Stock: 0)."
            elif cantidad > stock_actual:
                estado_item = "STOCK_INSUFICIENTE"
                comentario = f"Quiebre parcial. Solicitado: {cantidad} | Disponible: {stock_actual} uds."
        
        # Estructura final del texto que se visualiza en formato JSON
        item_procesado = {
            "Nombre": nombre,
            "SKU": sku,
            "Cantidad": cantidad,
            "Precio Solicitado": precio_solicitado,
            "Estado": estado_item,
            "Detalle": comentario
        }
        orden_validada.append(item_procesado)

    # Devolvemos un diccionario con una única llave llamada "result" y convertimos la lista a un string legible
    return {
        "result": json.dumps(orden_validada, indent=2, ensure_ascii=False)
    }