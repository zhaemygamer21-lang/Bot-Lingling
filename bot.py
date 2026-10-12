import os, time, requests, threading, re
from http.server import BaseHTTPRequestHandler, HTTPServer

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# PEGA TUS ENLACES REALES DENTRO DE LAS COMILLAS CORRESPONDIENTES:
RutaMerch_1 = "https://www.redbubble.com/shop?"

query=Gl&ref=search_box"
RutaMerch_2 = "https://www.etsy.com/es/search?"

q=gl&ref=search_bar"
RutaMerch_3 = "https://www.teepublic.com/t-shirts?"

query=gl"
RutaMerch_4 = "https://creativelifestyle.store/?"

s=Gl&post_type=product"
RutaMerch_5 = "https://es.aliexpress.com/w/wholesale-gl-

thai-series.html?"

osf=auto_suggest&spm=a2g0n.productli st.header.O"
RutaMerch_6 = "https://www.velvetmoon.cl/search?q=Gl"
RutaMerch_7 = "https://www.ethaicd.com/"
RutaMerch_8 = "https://rss.app/feeds/XFteWTncJ495pct3.

xmI"
RutaMerch_9 = "https://rss.app/feeds/mQzu3TPHk2 VgufR 6.xml"
RutaMerch_10 = "https://rss.app/feeds/Ao5SN5Fn9cw9IKa O.xmI"
RutaMerch_11 = "https://rss.app/feeds/LSg24vu1F3JnpR9P.

xml"

FUENTES_MERCH = {
    "Redbubble Posters": RutaMerch_1,
    "Etsy Fan Merch": RutaMerch_2,
    "Teepublic Camisetas": RutaMerch_3,
    "Creative Lifestyle Store": RutaMerch_4,
    "AliExpress Baratijas": RutaMerch_5,
    "VelvetMoon Papelería": RutaMerch_6,
    "eThaiCD portal de entretenimiento tailandés": RutaMerch_7,
    "Babii Store Latam (Instagram)": RutaMerch_8,
    "Raikantopini Shop (Instagram)": RutaMerch_9,
    "Daina Shop Custom Funkos (Instagram)": RutaMerch_10,
    "Mixup Store Peru (Instagram)": RutaMerch_11
}

# FILTROS DE PALABRAS CLAVE QUE ME PEDISTE
KEYWORDS_MERCH = ["Freen", "Becky", "Lingling", "Orm", "Lena Lalina", "Miu", "Faye", "Atom", "Lookmhee", "Sonya", 
    "LMSY", "Namtan", "Film", "NamtanFilm", "Milk", "Love", "MilkLove", "View", "Mim", "ViewMim", 
    "Ginny", "Jayna", "GinnyJayna", "Engfa", "Charlotte", "EngLot", "Apple", "Mim", "AppleMim", "Nile", 
    "Namwan", "NileNamwan", "Lilly Ladapa", "Belle", "LillyBelle", "Namneung", "Noey", "NamneungNoey", 
    "Atom Kamnoetsirikun", "Mersedes Kanyawee", "AtomMersedes", "Bam", "Baipor", "BamBamBaipor", "Tan", 
    "Yada", "TanYada", "June", "Enjoy", "JuneEnjoy", "Fah", "Bell", "FahBell", "Ormsin", "Folk", 
    "OrmsinFolk", "Anda", "Lookkaew", "AndaLookkaew", "Noon", "Praewa", "NoonPraewa", "Tungpang", "Jessie", 
    "TungpangJessie", "Tangkwa", "Nur", "TangkwaNur", "Shelly", "Pundao", "ShellyPundao", "Garn", "Mimie", 
    "GarnMimie", "May Yada", "MayNita", "Nita", "Minnie", "Pannie", "MinniePannie", "Bommy", "Ning", 
    "BommyNing", "Meena", "Aoom", "MeenaAoom", "Yuyee Alisa", "Mint Mintita", "Care", "Prigkhing", "Nuttacha", 
    "Bhapat Ahchariyasripong", "Charada Imraporn", "Chutimon Prasanwan", "Evarin Atichaichaowakit", 
    "Plaifa Waraha", "Fay Apisara", "Jeanie Ornlin", "BamBam Thitaree", "Ciize Rutricha", "Emi Thasorn", 
    "Bonnie Pattraphus Borattasuwan", "Jan Ployshompoo", "JingJing Yu", "Kapook Ploynira Hiruntaveesin", 
    "Jaoying Chawalitporn Pusomjit", "Mewnich Nannaphas Lertvilai", "Pahn Pathitta", 
    "Fond Nattanicha Chantaravareelekha", "Oom", "Bint Sireethorn", "Puinoon Warangsiri Tanajarusworaphat", 
    "FayMay", "Nita Aniphan Chalermburanawong", "Neko", "Mie Phattaranan", "Aya Orapan", "Kao Supassara", 
    "Jane Methika", "Natt Pitcha", "Meo-Meow", "Jennis", "Tarwaan", "Kaew", "Spy", "Yipun",
    "GL", "serie GL", "wlw", "thai", "gl series"]

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

def coincide_con_filtros(texto):
    t = texto.lower()
    return any(kw in t for kw in KEYWORDS_MERCH)

def enviar_a_discord(link, titulo, resumen, fuente, imagen_url=None):
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
        
        resumen = "¡Cuadros, papelería, ropa o artículos custom detectados en el catálogo sáfico! Revisa las fotografías en el enlace oficial."
        return [(url_base, titulo, resumen, foto)]
    except:
        pass
    return None

def bucle_monitoreo_merch():
    ultimos_productos = {}
    print("Iniciando rastreador masivo de tesoros jochis...")
    
    # FORZAR ENVIAR LO DE LA ÚLTIMA SEMANA DESDE EL INICIO
    primera_carga = True
    
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
                        if primera_carga or (nombre_tienda not in ultimos_productos or titulo != ultimos_productos[nombre_tienda]):
                            ultimos_productos[nombre_tienda] = titulo
                            
                            if coincide_con_filtros(titulo) or coincide_con_filtros(resumen) or "rss.app" in url:
                                enviar_a_discord(link, titulo, resumen, nombre_tienda, foto)
                                time.sleep(4)
            except:
                pass
        
        primera_carga = False
        time.sleep(900)

if __name__ == "__main__":
    bucle_monitoreo_merch()
    
