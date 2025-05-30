import json
import uuid
from deep_translator import GoogleTranslator


# Cargamos el JSON original
with open("Prueba_Junior.json", "r", encoding="utf-8") as original:
    
    datos = json.load(original)


# Mapeo para las ids repetidas
mapeo_id = {}


# Función para generar el ID único más la categoría
def generar_id(categoria):
    
    uid = uuid.uuid4().hex[:30]
    return f"{categoria:<20}"[:20] + uid


# Función para clasificar el texto o actor
def clasificar(texto, actor):
    if actor == "Des. Usuario":
        
        return "RESPUESTA_USUARIO"
    
    elif actor == "Instrucción":
        
        if texto.lower().startswith("pregunta") or texto.lower().startswith("solicita"):
            
            return "CONSULTA_DATOS"
        
        else:
            
            return "INDICACION"
        
    else:
        
        return "OTROS"


# Función de traducción
traduccion = GoogleTranslator(source="auto", target="en")
def traducir(texto):
    
    try:
        
        return traduccion.translate(texto)
    
    except Exception:
        
        return texto


# Función para transformar los nodos del JSON
def transformar_nodos(nodo):
        
    id_original = nodo.get("id", "")
    
    texto = nodo.get("texto", "")
    actor = nodo.get("actor", "")
    tipo = nodo.get("tipo", "")
    equipo = nodo.get("equipo", "")
    herramienta = nodo.get("herramienta", "")
    
    
    # Asignar ID nuevo si no se ha asignado antes
    if id_original not in mapeo_id:
        
        categoria = clasificar(texto, actor)
        mapeo_id[id_original] = generar_id(categoria)


    # Reemplazo y traduzco
    nodo["id"] = mapeo_id[id_original]
    nodo["texto"] = traducir(texto)
    nodo["actor"] = traducir(actor)
    nodo["tipo"] = traducir(tipo)
    nodo["equipo"] = traducir(equipo)
    nodo["herramienta"] = traducir(herramienta)


    # Procesar recursivamente las interacciones
    if "interacciones" in nodo:
        for subnodo in nodo["interacciones"]:
            transformar_nodos(subnodo)


# Ejecutamos la funcion de transformación
for bloque in datos:
    transformar_nodos(bloque)


# Guardamos el nuevo archivo JSON
with open("Prueba_Transformada.json", "w", encoding="utf-8") as f:
    
    json.dump(datos, f, ensure_ascii=False, indent=2)
    
print("Transformación completada. Archivo guardado como 'Prueba_Transformada.json'")
