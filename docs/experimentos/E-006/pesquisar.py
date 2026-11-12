"""E-006: busca gratuita (DuckDuckGo HTML) + páginas baixadas + modelo gratuito que responde citando.
Uso: python pesquisar.py <modelo> <arquivo-perguntas.json>
"""
import html, json, re, subprocess, sys, time, unicodedata, urllib.parse, urllib.request

UA = "roteirista-pesquisa/0.1"
K = subprocess.run(["powershell", "-NoProfile", "-Command",
                    '[Environment]::GetEnvironmentVariable("NOVEROUTER_KEY","User")'],
                   capture_output=True, text=True).stdout.strip()


def get(url, t=25):
    r = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
    with urllib.request.urlopen(r, timeout=t) as f:
        return f.headers.get_content_type(), f.read()


def buscar(p):
    q = p["busca"]
    if p.get("fonte") == "wikipedia":
        _, b = get("https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srlimit=3&srsearch=" + urllib.parse.quote(q))
        return [("https://en.wikipedia.org/wiki/" + urllib.parse.quote(x["title"].replace(" ", "_")), None)
                for x in json.loads(b)["query"]["search"]]
    _, b = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=core&pageSize=3&query=" + urllib.parse.quote(q))
    out = []
    for x in json.loads(b)["resultList"]["result"]:
        u = "https://europepmc.org/article/" + x.get("source", "MED") + "/" + str(x.get("id"))
        t = f'{x.get("authorString","")} ({x.get("pubYear","")}). {x.get("title","")} {x.get("journalTitle","") or ""}. ABSTRACT: {re.sub("<[^>]+>"," ",x.get("abstractText",""))}'
        out.append((u, t))
    return out


def buscar_ddg(q):
    _, b = get("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q))
    s = b.decode("utf-8", "replace")
    out = []
    for m in re.findall(r'class="result__a" href="([^"]+)"', s):
        u = html.unescape(m)
        u = urllib.parse.parse_qs(urllib.parse.urlparse(u).query).get("uddg", [u])[0]
        if u not in out and "duckduckgo.com" not in u:
            out.append(u)
    return out


def texto(ct, b):
    if "pdf" in ct:
        return None
    s = b.decode("utf-8", "replace")
    s = re.sub(r"(?is)<(script|style|nav|footer|header|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("’", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


P = """Answer the QUESTION using only the PAGES below. For each fact you use, copy a short EXACT quote
(8 to 30 words, verbatim, from one page) that supports it.
Answer only with lines in this format:
<fact, in Portuguese> | "<exact quote>" | <page URL>
If the pages do not answer, answer only: sem resposta

QUESTION: {q}

{pages}"""


def perguntar(modelo, q, paginas):
    corpo = "\n\n".join(f"PAGE {u}\n{t}" for u, t in paginas)
    body = json.dumps({"model": "openrouter/" + modelo, "stream": False, "temperature": 0,
                       "max_tokens": 20000,
                       "messages": [{"role": "user", "content": P.format(q=q, pages=corpo)}]}).encode()
    r = urllib.request.Request("http://127.0.0.1:20128/v1/chat/completions", body,
                               {"Content-Type": "application/json", "Authorization": "Bearer " + K})
    raw = urllib.request.urlopen(r, timeout=400).read().decode("utf-8")
    try:
        j = json.loads(raw)
        return j["choices"][0]["message"].get("content") or "", j.get("usage")
    except json.JSONDecodeError:
        out, tk = "", None
        for l in raw.splitlines():
            l = l.strip().removeprefix("data:").strip()
            try:
                c = json.loads(l)
            except Exception:
                continue
            tk = c.get("usage") or tk
            for ch in c.get("choices", []):
                out += (ch.get("delta") or ch.get("message") or {}).get("content") or ""
        return out, tk


def main():
    modelo, arq = sys.argv[1], sys.argv[2]
    perguntas = json.load(open(arq, encoding="utf-8"))
    rel = []
    for p in perguntas:
        t0 = time.time()
        achados = buscar(p)
        urls = [u for u, _ in achados]
        paginas, falhas = [], []
        for u, pronto in achados:
            if len(paginas) == 3:
                break
            try:
                if pronto:
                    t = pronto
                elif "wikipedia.org" in u:
                    tit = urllib.parse.unquote(u.rsplit("/", 1)[1])
                    _, b = get("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&titles=" + urllib.parse.quote(tit))
                    t = next(iter(json.loads(b)["query"]["pages"].values())).get("extract", "")
                else:
                    ct, b = get(u)
                    t = texto(ct, b)
                if not t or len(t) < 300:
                    falhas.append(f"{u} (pdf ou vazio)")
                    continue
                paginas.append((u, t[:12000]))
            except Exception as e:
                falhas.append(f"{u} ({type(e).__name__} {getattr(e, 'code', '')})")
        try:
            resp, uso = perguntar(modelo, p["pergunta"], paginas) if paginas else ("sem páginas", None)
        except Exception as e:
            resp, uso = "ERRO " + str(e) + " " + (e.read().decode()[:300] if hasattr(e, "read") else ""), None
        pag = dict(paginas)
        linhas = []
        for l in resp.splitlines():
            m = re.match(r'\s*(.+?)\s*\|\s*"(.+?)"\s*\|\s*(\S+)', l)
            if not m:
                continue
            fato, cit, url = m.groups()
            ok = url in pag and norm(cit) in norm(pag[url])
            linhas.append({"fato": fato, "citacao": cit, "url": url, "confere": ok})
        rel.append({"id": p["id"], "pergunta": p["pergunta"], "esperado": p["esperado"],
                    "urls": urls[:6], "lidas": [u for u, _ in paginas], "falhas": falhas,
                    "resposta": resp, "linhas": linhas, "segundos": round(time.time() - t0),
                    "uso": uso})
        print(f"=== {p['id']} ({rel[-1]['segundos']}s) lidas {len(paginas)}, falhas {len(falhas)}")
        for x in linhas:
            print(("  OK  " if x["confere"] else "  XX  ") + f"{x['fato']}  <{x['url']}>")
        if not linhas:
            print("  " + resp[:400])
    nome = modelo.replace("/", "_").replace(":", "_")
    json.dump(rel, open(f"resultado--{nome}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


main()
