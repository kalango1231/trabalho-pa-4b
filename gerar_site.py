"""Gera o site para o Live Server: index.html + styles.css.

Não precisa instalar nada (só o Python). Rode:
    python gerar_site.py
Depois abra o index.html com o Live Server.

Os produtos, preços e cores vêm do app.py. Mudou algo lá? Rode este arquivo de novo.
"""
import re
import sys
import types
import webbrowser
import importlib.util
from pathlib import Path

PASTA = Path(__file__).parent

# --- "Flask de mentira": deixa ler o app.py sem instalar o Flask ---------------
flask_falso = types.ModuleType("flask")


class Response:
    def __init__(self, html, mimetype=None):
        self.html = html


flask_falso.Flask = lambda nome: types.SimpleNamespace(route=lambda *a, **k: (lambda f: f), run=lambda **k: None)
flask_falso.Response = Response
flask_falso.abort = lambda codigo: (_ for _ in ()).throw(ValueError(codigo))
flask_falso.send_from_directory = flask_falso.redirect = lambda *a, **k: None
sys.modules["flask"] = flask_falso

spec = importlib.util.spec_from_file_location("loja", PASTA / "app.py")
loja = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loja)

# --- monta as páginas -----------------------------------------------------------
secoes, abas, menus = [], [], []
for genero, info in loja.GENEROS.items():
    primeira = next(iter(info["categorias"]))
    abas.append(f'<a href="#{genero}-{primeira}" data-g="{genero}">{info["nome"]}</a>')
    pills = []
    for slug in list(info["categorias"]) + ["promocoes"]:
        pag = f"{genero}-{slug}"
        r = loja.promocoes(genero) if slug == "promocoes" else loja.categoria(genero, slug)
        main = re.search(r"<main>(.*)</main>", r.html, re.S).group(1)
        main = main.replace('src="/fotos/', 'src="fotos/')
        main = main.replace('id="produtos"', f'id="produtos-{pag}"').replace('href="#produtos"', f'href="#produtos-{pag}"')
        secoes.append(f'<section class="pagina" data-pag="{pag}" hidden>{main}</section>')
        nome = "Promoções" if slug == "promocoes" else info["categorias"][slug]
        pills.append(f'<a href="#{pag}" class="pilula" data-pag="{pag}">{nome}</a>')
    menus.append(f'<nav class="menu" data-g="{genero}" hidden>{"".join(pills)}</nav>')

# o CSS do app.py tem chaves duplas {{ }} por causa do f-string; aqui já vem pronto
css = loja.CSS.strip() + "\n"

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Economia e Estilo</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="topo">
    <div class="topo-linha">
      <a href="#masculino-calcas" class="logo">ECONOMIA E ESTILO<small>MODA MASCULINA &amp; FEMININA</small></a>
    </div>
    <nav class="generos">{"".join(abas)}</nav>
    {"".join(menus)}
  </header>
  <main>
    {"".join(secoes)}
  </main>
  <div id="aviso" class="aviso" role="status"></div>
  <script>
    // troca de página sem sair do index.html
    function mostrar() {{
      let pag = location.hash.slice(1);
      if (!document.querySelector('.pagina[data-pag="' + pag + '"]')) pag = 'masculino-calcas';
      const genero = pag.split('-')[0];
      document.querySelectorAll('.pagina').forEach(s => s.hidden = s.dataset.pag !== pag);
      document.querySelectorAll('.menu').forEach(m => m.hidden = m.dataset.g !== genero);
      document.querySelectorAll('.generos a').forEach(a => a.classList.toggle('ativa', a.dataset.g === genero));
      document.querySelectorAll('.pilula').forEach(a => a.classList.toggle('ativa', a.dataset.pag === pag));
      document.title = 'Economia e Estilo · ' + document.querySelector('.pagina[data-pag="' + pag + '"] .titulo').textContent;
    }}
    addEventListener('hashchange', () => {{ if (!location.hash.startsWith('#produtos')) {{ mostrar(); scrollTo(0, 0); }} }});
    mostrar();

    // aviso da sacola
    let total = 0;
    document.querySelectorAll('.comprar').forEach(b => b.addEventListener('click', () => {{
      total++;
      const a = document.getElementById('aviso');
      a.textContent = '🛍️ ' + b.dataset.nome + ' adicionado à sacola (' + total + (total > 1 ? ' itens)' : ' item)');
      a.classList.add('mostrar');
      clearTimeout(a._t);
      a._t = setTimeout(() => a.classList.remove('mostrar'), 2400);
    }}));
  </script>
</body>
</html>
"""

(PASTA / "styles.css").write_text(css, encoding="utf-8")
(PASTA / "index.html").write_text(html, encoding="utf-8")
print("Pronto: index.html e styles.css gerados em", PASTA)

if "--abrir" in sys.argv:
    webbrowser.open((PASTA / "index.html").as_uri())
