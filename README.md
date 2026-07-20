# 📦 AI Supply Chain Agent: Purchase Order Validator

**Autor:** Marco Antonio Gómez-Morales  
**Demo en vivo:** https://udify.app/workflow/sk2ZaoOc6sN4Kfg7  
**Video de demostración:** [Inserta aquí el enlace a tu video de 3-5 min]

## 🎯 ¿Qué hace este proyecto?
Este workflow automatiza la recepción y validación de Órdenes de Compra (POs) entrantes. En la operación logística real, la revisión manual de POs es un proceso lento y propenso a errores (aprobar precios incorrectos o solicitar productos sin stock). 

Este agente resuelve el problema de extremo a extremo:
1. **Recibe** el texto libre de una orden de compra (puede venir de un correo o PDF extraído).
2. **Extrae** los datos usando `gpt-4o-mini` con salidas estructuradas estrictas (JSON) para obtener: Nombre, SKU, Cantidad y Precio.
3. **Verifica** deterministamente mediante un backend en Python cada partida contra una base de datos/catálogo oficial de 25 componentes.
4. **Genera** un reporte ejecutivo resaltando anomalías operativas:
   - ⚠️ Discrepancias de precio.
   - ❌ SKUs inexistentes o inválidos.
   - ⚠️ Quiebres de stock (parciales o producto agotado).

## 🚀 Cómo correrlo y probarlo
Dado que el proyecto fue construido y desplegado mediante orquestación visual en Dify, no es necesario levantar un servidor local para probar la funcionalidad principal.

1. Abre la app https://udify.app/workflow/sk2ZaoOc6sN4Kfg7.
2. En el cuadro de entrada, pega el texto de una Orden de Compra que se encuentran en los ejemplos de abajo.
3. Ejecuta el agente y observa el diagnóstico.

## **Ejemplos de Ordenes de Compra:**

**Ejemplo #1 (cumple con todas las condicones y no muestra errores en la salida):**

*ORDEN DE COMPRA: ROBOTICS INTEGRATION MX*
*PO Número: 2026-A1020*
*Fecha: 20 de Julio de 2026*

*Por medio de la presente, solicitamos el material para nuestro nuevo lote de tableros de control. Aceptamos los precios de su catálogo vigente:*
*- 50 unidades de Pantalla OLED 0.96 I2C (SKU-OLED1) a $3.10 cada una.*
*- 20 piezas de Protoboard de 830 Puntos (SKU-BREAD) con precio de $2.90 por unidad.*
*- 10 Kits de Resistencias de 600pcs (SKU-RESI0) a $5.50 el kit.*
*- 40 Sensores Infrarrojos de Presencia (SKU-INTR0) a un costo de $1.50 c/u.*
*- 15 Cautines Eléctricos Lápiz 60W (SKU-KA220) listados a $12.00.*

*Favor de confirmar la fecha de entrega a nuestra planta.*
## 

**Ejemplo #2 (Tiene SKUs inventados, precios bajísimos que el cliente intentó "colar" y peticiones masivas de artículos que están a punto de agotarse o ya están en cero):**

*ORDEN DE COMPRA: AUTOMATIZACIÓN GLOBAL S.A. DE C.V.*
*PO Número: 2026-F9933*
*Fecha: 21 de Julio de 2026*

*Requerimos los siguientes componentes para la línea de ensamblaje principal. Notarán que hemos aplicado un descuento especial por volumen en algunos artículos:*
*- 25 Arduino Nano CH340 (SKU-NANO3) a un precio rebajado de $3.50. (Trampa: Stock 0 y precio incorrecto).*
*- 50 Servomotores MG996R (SKU-MOT02) a $6.80 cada uno. (Trampa: Pide 50, solo hay 45).*
*- 10 Módulos Bluetooth HC-05 (SKU-BLU05) a $4.80 por pieza. (Sin error).*
*- 200 Motores a Pasos NEMA 17 marcados con su código SKU-STPP9 a $10.00. (Trampa: SKU falso y precio muy por debajo de los $14.20).*
*- 10 Raspberry Pi 4 4GB (SKU-RPI4) a $45.00 la unidad. (Trampa: Pide 10, solo hay 8 en stock).*
## 

**Ejemplo #3 (Este escenario prueba la precisión del LLM. El cliente redactó el texto de forma más coloquial e informal, escondiendo los datos clave, y tiene errores de centavos que a un humano se le pasarían por alto):**

*ORDEN DE COMPRA RÁPIDA - TECH SOLUTIONS*
*Referencia: URG-881*

*Hola equipo, necesitamos que nos manden de urgencia los siguientes materiales para mañana en la mañana.*
*Mándenme 30 ventiladores de 5V para gabinete, los que tienen el código SKU-FAN05. Vi que están a $1.50 en la cotización pasada, así que los cerramos a ese precio. También ocupamos 5 Multímetros digitales básicos (SKU-MULT0) a $15.50 y para terminar, agrégame 100 sensores de temperatura DHT22 (SKU-DHT22), creo que estaban a $3.80 cada uno. Ah, y por favor metan 15 Carcasas de Acrílico para RPi4, el código es SKU-CASE4 y el precio es de $3.90.*

*Facturen todo junto y me avisan.*
## 

***Nota: En este repositorio se incluye el archivo `ProductsList.csv` que actúa como la base de datos oficial, así como el bloque de código Python (`codigoPO.py`) utilizado en el nodo de procesamiento.***

## ⚖️ Decisiones Clave y Tradeoffs (Arquitectura)

Al diseñar esta solución, prioricé el **sentido de producto y la confiabilidad operativa** sobre la creación de infraestructura desde cero:

* **Orquestación en Dify vs. Desarrollo Custom:** Opté por utilizar Dify como framework de agentes. Viniendo de entornos corporativos donde se utilizan plataformas visuales robustas para el manejo de automatizaciones, Dify me permitió acelerar el *time-to-market* y enfocarme en las reglas de negocio logísticas, en lugar de gastar horas del fin de semana configurando un backend en FastAPI y un frontend en React.
* **Separación de IA vs. Lógica Determinista:** Un gran tradeoff fue decidir *qué* hace el LLM. Decidí **no** usar IA (ni RAG) para comparar precios o existencias, ya que los LLMs pueden alucinar. El LLM (`gpt-4o-mini`, Temp 0.5) se usa *exclusivamente* como un motor de extracción de datos a JSON. La validación matemática de inventario y costos recae en un script de Python puro, garantizando un 100% de precisión.
* **Manejo de Stock Real:** Decidí expandir el reto original incluyendo no solo validación de precios, sino niveles de inventario reales en el diccionario de datos. Esto refleja un caso de uso logístico mucho más realista (Stock variable y precios reales), permitiendo prever rupturas de la cadena de suministro antes de que la orden pase a almacén.
