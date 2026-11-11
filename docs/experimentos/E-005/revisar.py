import json,os,sys,subprocess,urllib.request,time
K=subprocess.run(['powershell','-NoProfile','-Command','[Environment]::GetEnvironmentVariable("NOVEROUTER_KEY","User")'],capture_output=True,text=True).stdout.strip()
mat=open('../ensaio/cap-1-material.md',encoding='utf-8').read()
P="""Você revisa a fidelidade de um texto em português escrito a partir de trechos de um livro em inglês.
Compare o TEXTO com o MATERIAL. Liste cada afirmação do TEXTO que o MATERIAL não sustenta: fato inventado, detalhe acrescentado, ordem dos acontecimentos trocada, contraste ou comparação que o livro não faz, generalização maior que o livro. Ignore estilo, cortes e a apresentação do narrador ("Eu sou o Alderick").
Responda só com linhas no formato:
<frase do TEXTO, copiada> | <motivo curto> | <id do MATERIAL que contradiz ou "sem apoio">
Se não houver nenhuma, responda só: nada

MATERIAL:
{m}

TEXTO:
{t}"""
modelos=sys.argv[1:]
for arq in ['rascunho.md','final.md']:
  t=open(arq,encoding='utf-8').read()
  for m in modelos:
    body=json.dumps({"model":"openrouter/"+m,"messages":[{"role":"user","content":P.format(m=mat,t=t)}],"temperature":0,"max_tokens":20000,"stream":False}).encode()
    r=urllib.request.Request("http://127.0.0.1:20128/v1/chat/completions",body,{"Content-Type":"application/json","Authorization":"Bearer "+K})
    t0=time.time()
    try:
      raw=urllib.request.urlopen(r,timeout=300).read().decode('utf-8')
      open('ultimo-bruto.txt','w',encoding='utf-8').write(raw)
      try:
        j=json.loads(raw); out=j['choices'][0]['message'].get('content') or '(vazio)'; real=j.get('model'); tk=j.get('usage')
      except json.JSONDecodeError:
        out='';real='';tk=''
        for l in raw.splitlines():
          l=l.strip()
          if not l: continue
          if l.startswith('data:'): l=l[5:].strip()
          if l=='[DONE]': continue
          try: c=json.loads(l)
          except Exception: continue
          real=c.get('model',real); tk=c.get('usage') or tk
          for ch in c.get('choices',[]):
            out+=(ch.get('delta') or ch.get('message') or {}).get('content') or ''
        out=out or '(vazio)'
    except Exception as e:
      out='ERRO '+str(e)+' '+(e.read().decode()[:300] if hasattr(e,'read') else ''); real='';tk=''
    nome=m.replace('/','_').replace(':','_')
    open(f'{arq[:-3]}--{nome}.txt','w',encoding='utf-8').write(out)
    print(f'=== {arq} | {m} -> {real} | {time.time()-t0:.0f}s | {tk}\n{out}\n',flush=True)
