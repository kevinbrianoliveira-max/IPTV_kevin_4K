import requests
import os

TMDB_KEY = "f5437da3eb453c46d801cd56b42046dc"

def get_poster(nome, tipo="movie"):
    url = f"https://api.themoviedb.org{tipo}?api_key={TMDB_KEY}&query={nome}&language=pt-BR"
    try:
        res = requests.get(url).json()
        if res.get('results'):
            return f"https://image.tmdb.org{res['results'][0]['poster_path']}"
    except: pass
    return ""

with open("playlist.m3u", "w", encoding="utf-8") as f_out:
    f_out.write("#EXTM3U\n")
    if os.path.exists("links.txt"):
        with open("links.txt", "r", encoding="utf-8") as f_in:
            for linha in f_in:
                if "|" in linha:
                    partes = [p.strip() for p in linha.split("|")]
                    nome, url = partes[0], partes[1]
                    if "S0" in nome.upper() or "E0" in nome.upper():
                        capa = get_poster(nome.split("S0")[0].strip(), "tv")
                        f_out.write(f'#EXTINF:-1 tvg-logo="{capa}" group-title="SÉRIES", {nome}\n{url}\n')
                    elif "fazoeli" in url or "m3u8" in url:
                        f_out.write(f'#EXTINF:-1 group-title="CANAIS AO VIVO", {nome}\n{url}\n')
                    else:
                        capa = get_poster(nome, "movie")
                        f_out.write(f'#EXTINF:-1 tvg-logo="{capa}" group-title="FILMES", {nome}\n{url}\n')
