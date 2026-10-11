import os, time, requests, threading, re
from http.server import BaseHTTPRequestHandler, HTTPServer
import discord
from discord.ext import commands

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# TUS 7 TIENDAS BASE + TUS 4 FEEDS DE INSTAGRAM CONVERTIDOS POR RSS.APP
RutaMerch_1 = "https://redbubble.com"
RutaMerch_2 = "https://etsy.com"
RutaMerch_3 = "https://ethaicd.com"
RutaMerch_4 = "https://teepublic.com"
RutaMerch_5 = "https://creativelifestyle.store"
RutaMerch_6 = "https://aliexpress.com"
RutaMerch_7 = "https://velvetmoon.cl"
RutaMerch_8 = "https://rss.app"
RutaMerch_9 = "https://rss.app"
RutaMerch_10 = "https://rss.app"
RutaMerch_11 = "https://rss.app"

FUENTES_MERCH = {
    "Redbubble Posters": RutaMerch_1,
    "Etsy Fan Merch": RutaMerch_2,
    "eThaiCD (Cajas Oficiales Thai)": RutaMerch_3,
    "Teepublic Camisetas": RutaMerch_4,
    "Creative Lifestyle Store": RutaMerch_5,
    "AliExpress Baratijas": RutaMerch_6,
    "VelvetMoon Papelería": RutaMerch_7,
    "Babii Store Latam (Instagram)": RutaMerch_8,
    "Raikantopini Shop (Instagram)": RutaMerch_9,
    "Daina Shop Custom Funkos (Instagram)": RutaMerch_10,
    "Mixup Store Peru (Instagram)": RutaMerch_11
}

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot de LingLing Coleccionista Compulsiva Activo")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(("0.0.0.0", port), Servidor).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

def enviar_a_discord(link, titulo, resumen, fuente, imagen_url=None):
    # FRASE FINAL CON EL NOMBRE COMPLETADO CON ÉXITO
    saludo_lingling = (
        "🛍️✨ **¡Sawasdee kha! Soy LingLing Kwong, su coleccionista de confianza, y les traigo "
        "estos hermosos tesoros jochis que seguramente quieren adquirir. ¡Prepárense para dejar sus quincenas! 🖼️🎁**"
    )
    payload = {
        "content": saludo_lingling,
        "embeds": [{
            "title": titulo if titulo else "Coleccionable Exclusivo Detectado",
            "description": resumen if resumen else "Haz clic en el enlace para revisar las fotos, precios y detalles de este artículo de colección.",
            "url": link,
            "color": 16744319,
            "fields": [
                {"name": "🏪 Catálogo / Tienda de Origen", "value": fuente, "inline": True}
            ]
        }]
    }
    if imagen_url and imagen_url.startswith("http"):
        payload["embeds"]["image"] = {"url": imagen_url}
        
    try:
        requests.post(WEBHOOK_URL, json=payload, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except:
        pass

def extraer_datos_tienda(html_puro, url_base):
    try:
        foto = None
        img_match = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html_puro)
        if not img_match:
            img_match = re.search(r'<img[^>]+src="([^"]+)"', html_puro)
        if not img_match:
            img_match = re.search(r'<media:content[^>]+url="([^"]+)"', html_puro)
            
        if img_match:
            foto = img_match.group(1).strip()
            if foto.startswith("//"): foto = "https:" + foto
            if not foto.startswith("http"): foto = url_base.rstrip('/') + "/" + foto.lstrip('/')

        tit_match = re.search(r'<title>([^<]+)</title>', html_puro)
        if not tit_match:
            tit_match = re.search(r'<title><!\[CDATA\[([^\]]+)\]\]></title>', html_puro)
            
        titulo = tit_match.group(1).strip() if tit_match else "Nuevo artículo de merch disponible"
        titulo = re.sub(r'(| Etsy| | Redbubble| AliExpress| RSS\.app)', '', titulo, flags=re.IGNORECASE).strip()
        
        resumen = "¡Cuadros, photobooks oficiales, llaveros, ropa o artículos custom detectados en el catálogo! Revisa las fotografías completas en el enlace oficial."
        return [(url_base, titulo, resumen, foto)]
    except:
        pass
    return None

def bucle_monitoreo_merch():
    ultimos_productos = {}
    print("Iniciando rastreador antibloqueo de LingLing Coleccionista (11 Fuentes)...")
    while True:
        for nombre_tienda, url in FUENTES_MERCH.items():
            try:
                cabeceras_humanas = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Cache-Control": "max-age=0"
                }
                res = requests.get(url, headers=cabeceras_humanas, timeout=20)
                if res.status_code != 200: continue
                
                datos = extraer_datos_tienda(res.text, url)
                if datos:
                    for link, titulo, resumen, foto in datos:
                        if nombre_tienda not in ultimos_productos or titulo != ultimos_productos[nombre_tienda]:
                            ultimos_productos[nombre_tienda] = titulo
                            enviar_a_discord(link, titulo, resumen, nombre_tienda, foto)
                            time.sleep(3)
            except:
                pass
        time.sleep(900)

if __name__ == "__main__":
    bucle_monitoreo_merch()
          
