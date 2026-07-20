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

1. Abre la app [https://udify.app/workflow/sk2ZaoOc6sN4Kfg7](#).
2. En el cuadro de entrada, pega el texto de una Orden de Compra.
3. Ejecuta el agente y observa el diagnóstico.

*Nota: En este repositorio se incluye el archivo `ProductsList.csv` que actúa como la base de datos oficial, así como el bloque de código Python (`validator_logic.py`) utilizado en el nodo de procesamiento.*

## ⚖️ Decisiones Clave y Tradeoffs (Arquitectura)

Al diseñar esta solución, prioricé el **sentido de producto y la confiabilidad operativa** sobre la creación de infraestructura desde cero:

* **Orquestación en Dify vs. Desarrollo Custom:** Opté por utilizar Dify como framework de agentes. Viniendo de entornos corporativos donde se utilizan plataformas visuales robustas para el manejo de automatizaciones, Dify me permitió acelerar el *time-to-market* y enfocarme en las reglas de negocio logísticas, en lugar de gastar horas del fin de semana configurando un backend en FastAPI y un frontend en React.
* **Separación de IA vs. Lógica Determinista:** Un gran tradeoff fue decidir *qué* hace el LLM. Decidí **no** usar IA (ni RAG) para comparar precios o existencias, ya que los LLMs pueden alucinar. El LLM (`gpt-4o-mini`, Temp 0) se usa *exclusivamente* como un motor de extracción de datos a JSON. La validación matemática de inventario y costos recae en un script de Python puro, garantizando un 100% de precisión.
* **Manejo de Stock Real:** Decidí expandir el reto original incluyendo no solo validación de precios, sino niveles de inventario reales en el diccionario de datos. Esto refleja un caso de uso logístico mucho más realista, permitiendo prever rupturas de la cadena de suministro antes de que la orden pase a almacén.
