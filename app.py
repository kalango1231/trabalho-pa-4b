
from html import escape
from pathlib import Path
from flask import Flask, abort, Response, send_from_directory, redirect

app = Flask(__name__)
PASTA_FOTOS = Path(__file__).parent / "fotos"
PASTA_FOTOS.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# DADOS DA LOJA
# ---------------------------------------------------------------------------
GENEROS = {
    "masculino": {
        "nome": "Masculino",
        "categorias": {"calcas": "Calças", "camisas": "Camisas", "tenis": "Tênis"},
    },
    "feminino": {
        "nome": "Feminino",
        "categorias": {"vestidos": "Vestidos", "bolsas": "Bolsas", "calcas": "Calças"},
    },
}

# Título que aparece na faixa creme de cada categoria
TITULOS = {
    ("masculino", "calcas"): "Calças Masculinas",
    ("masculino", "camisas"): "Camisas Masculinas",
    ("masculino", "tenis"): "Tênis Masculinos",
    ("feminino", "vestidos"): "Vestidos Femininos",
    ("feminino", "bolsas"): "Bolsas Femininas",
    ("feminino", "calcas"): "Calças Femininas",
}

PRODUTOS = [
    # ----- MASCULINO · CALÇAS -----
    {"genero": "masculino", "cat": "calcas", "nome": "Calça Jeans Azul Reta", "cor": "#4a6f9c", "preco": 199, "promo": None, "tamanhos": "38 40 42 44", "foto": "masc-calca-jeans-azul.jpg"},
    {"genero": "masculino", "cat": "calcas", "nome": "Calça Jeans Preta Slim", "cor": "#1f1f22", "preco": 220, "promo": 169, "tamanhos": "38 40 42", "foto": "masc-calca-jeans-preta.jpg"},
    {"genero": "masculino", "cat": "calcas", "nome": "Calça Cargo Preta", "cor": "#2a2a2a", "preco": 260, "promo": None, "tamanhos": "38 40 42 44", "foto": "masc-calca-cargo-preta.jpg"},
    {"genero": "masculino", "cat": "calcas", "nome": "Calça Jogger Camuflada", "cor": "#7a6a58", "preco": 180, "promo": 139, "tamanhos": "P M G GG", "foto": "masc-calca-jogger-camuflada.jpg"},
    {"genero": "masculino", "cat": "calcas", "nome": "Calça Chino Bege", "cor": "#d6cfc0", "preco": 210, "promo": None, "tamanhos": "38 40 42 44 46", "foto": "masc-calca-chino-bege.jpg"},
    # ----- MASCULINO · CAMISAS -----
    {"genero": "masculino", "cat": "camisas", "nome": "Camisa Polo Preta Texturizada", "cor": "#1f1f22", "preco": 160, "promo": 119, "tamanhos": "P M G GG", "foto": "masc-camisa-polo-preta.jpg"},
    {"genero": "masculino", "cat": "camisas", "nome": "Camiseta Azul Claro", "cor": "#a9cbe8", "preco": 89, "promo": None, "tamanhos": "P M G GG", "foto": "masc-camiseta-azul-claro.jpg"},
    {"genero": "masculino", "cat": "camisas", "nome": "Camiseta Bege", "cor": "#d8c7a0", "preco": 89, "promo": None, "tamanhos": "P M G GG", "foto": "masc-camiseta-bege.jpg"},
    {"genero": "masculino", "cat": "camisas", "nome": "Camiseta Vinho", "cor": "#6b1a24", "preco": 89, "promo": 69, "tamanhos": "P M G GG", "foto": "masc-camiseta-vinho.jpg"},
    # ----- MASCULINO · TÊNIS -----
    {"genero": "masculino", "cat": "tenis", "nome": "Tênis Couro Preto", "cor": "#1f1f22", "preco": 250, "promo": None, "tamanhos": "39 40 41 42 43", "foto": "masc-tenis-couro-preto.jpg"},
    {"genero": "masculino", "cat": "tenis", "nome": "Tênis Camurça Bege", "cor": "#b9a68e", "preco": 380, "promo": 299, "tamanhos": "39 40 41 42 43 44", "foto": "masc-tenis-camurca-bege.jpg"},
    {"genero": "masculino", "cat": "tenis", "nome": "Tênis Couro Marrom", "cor": "#5a3a26", "preco": 280, "promo": None, "tamanhos": "40 41 42 43", "foto": "masc-tenis-couro-marrom.jpg"},
    # ----- FEMININO · VESTIDOS -----
    {"genero": "feminino", "cat": "vestidos", "nome": "Vestido Floral Azul", "cor": "#a9bde0", "preco": 220, "promo": 169, "tamanhos": "P M G", "foto": "fem-vestido-floral-azul.jpg"},
    {"genero": "feminino", "cat": "vestidos", "nome": "Vestido Midi Floral Rosa", "cor": "#e8b9c4", "preco": 260, "promo": None, "tamanhos": "PP P M G", "foto": "fem-vestido-midi-floral-rosa.jpg"},
    {"genero": "feminino", "cat": "vestidos", "nome": "Vestido Curto Caramelo", "cor": "#8a4a2e", "preco": 190, "promo": None, "tamanhos": "P M G GG", "foto": "fem-vestido-curto-caramelo.jpg"},
    # ----- FEMININO · BOLSAS -----
    {"genero": "feminino", "cat": "bolsas", "nome": "Bolsa Preta com Laço", "cor": "#1f1f22", "preco": 240, "promo": None, "tamanhos": "Único", "foto": "fem-bolsa-preta-laco.jpg"},
    {"genero": "feminino", "cat": "bolsas", "nome": "Bolsa Caramelo", "cor": "#8a5530", "preco": 230, "promo": 179, "tamanhos": "Único", "foto": "fem-bolsa-caramelo.jpg"},
    {"genero": "feminino", "cat": "bolsas", "nome": "Bolsa Off-White Laço Dourado", "cor": "#efe6d4", "preco": 250, "promo": None, "tamanhos": "Único", "foto": "fem-bolsa-off-white-laco.jpg"},
    # ----- FEMININO · CALÇAS -----
    {"genero": "feminino", "cat": "calcas", "nome": "Calça Alfaiataria Off-White", "cor": "#ece6da", "preco": 230, "promo": 179, "tamanhos": "36 38 40 42", "foto": "fem-calca-alfaiataria-off-white.jpg"},
]

# ---------------------------------------------------------------------------
# ESTILO (CSS gerado pelo Python)
# ---------------------------------------------------------------------------
LARANJA, CREME, CINZA = "#fdc07d", "#fffde8", "#c8d0da"

CSS = f"""
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; font-family: Inter, system-ui, sans-serif; color: #1a1a1a; background: #faf8f4; }}

/* ---------- topo ---------- */
.topo {{ background: {LARANJA}; padding: 26px 16px 30px; border-radius: 0 0 36px 36px;
        box-shadow: 0 8px 24px rgba(181,110,40,.18); position: relative; }}
.topo-linha {{ display: flex; justify-content: center; max-width: 1200px; margin: 0 auto; }}
.logo {{ font-family: Oswald, Impact, sans-serif; font-size: clamp(32px, 6vw, 68px); letter-spacing: 3px; color: #111;
        text-decoration: none; text-align: center; line-height: 1; }}
.logo small {{ display: block; font-family: Inter, sans-serif; font-size: 12px; letter-spacing: 6px; font-weight: 600;
              color: #7a4a1e; margin-top: 8px; }}
.generos {{ display: flex; margin: 24px auto 0; background: {CREME}; border-radius: 999px; width: fit-content; padding: 5px;
           box-shadow: inset 0 1px 3px rgba(0,0,0,.08); }}
.generos a {{ padding: 10px 36px; border-radius: 999px; text-decoration: none; color: #555; font-weight: 700;
             letter-spacing: 1.5px; text-transform: uppercase; font-size: 13px; transition: all .2s; }}
.generos a.ativa {{ background: #222; color: {CREME}; box-shadow: 0 4px 10px rgba(0,0,0,.2); }}
.menu {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 14px; margin-top: 18px; }}
.pilula {{ min-width: 140px; padding: 11px 20px; border-radius: 999px; background: {CREME}; text-align: center;
          text-decoration: none; color: #333; font-size: 14px; font-weight: 600; transition: all .2s;
          box-shadow: 0 2px 6px rgba(0,0,0,.06); }}
.pilula:hover {{ transform: translateY(-2px); box-shadow: 0 6px 14px rgba(0,0,0,.12); }}
.pilula.ativa {{ background: #222; color: {CREME}; }}

/* ---------- título e banner ---------- */
main {{ max-width: 1240px; margin: 0 auto; padding: 0 16px; }}
.titulo {{ margin: 34px auto 22px; max-width: 760px; background: {CREME}; border-radius: 999px; padding: 14px 24px;
          text-align: center; font-weight: 400; font-size: clamp(22px, 3vw, 32px); box-shadow: 0 4px 14px rgba(0,0,0,.06); }}
.banner {{ height: 320px; overflow: hidden; display: flex; align-items: flex-end; justify-content: space-between;
          border-radius: 28px; box-shadow: 0 14px 34px rgba(120,70,30,.18);
          background: linear-gradient(120deg, #f8ead6 0%, #efd3ad 55%, #d6a473 100%); }}
.banner-texto {{ padding: 40px 52px; align-self: center; }}
.banner-chamada {{ margin: 0; font-family: Oswald, Impact, sans-serif; font-size: 18px; letter-spacing: 4px;
                  text-transform: uppercase; color: #8a5a32; }}
.banner-frase {{ margin: 10px 0 22px; font-size: clamp(24px, 3.4vw, 42px); font-weight: 700; line-height: 1.12; color: #3a2416; }}
.banner-botao {{ display: inline-block; background: #222; color: {CREME}; padding: 13px 28px; border-radius: 999px;
                text-decoration: none; font-weight: 600; transition: all .2s; }}
.banner-botao:hover {{ background: #000; transform: translateY(-2px); }}
.arara {{ height: 100%; max-width: 58%; }}

/* ---------- vantagens ---------- */
.vantagens {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 26px 0 40px; }}
.vantagem {{ display: flex; align-items: center; gap: 14px; background: #fff; border-radius: 18px; padding: 16px 20px;
            box-shadow: 0 4px 14px rgba(0,0,0,.05); }}
.vantagem span {{ font-size: 28px; }}
.vantagem b {{ display: block; font-size: 15px; }}
.vantagem small {{ color: #777; font-size: 13px; }}

/* ---------- produtos ---------- */
.grade {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 36px 32px; padding-bottom: 70px; }}
.card {{ display: flex; flex-direction: column; background: #fff; border-radius: 24px; overflow: hidden;
        box-shadow: 0 6px 20px rgba(0,0,0,.07); transition: transform .25s, box-shadow .25s; }}
.card:hover {{ transform: translateY(-6px); box-shadow: 0 18px 36px rgba(0,0,0,.13); }}
.foto {{ position: relative; aspect-ratio: 3/4; display: grid; place-items: center; overflow: hidden;
        background: radial-gradient(circle at 50% 40%, #fbfaf7, #e7e4de); }}
.foto:has(img) {{ background: #fff; }}
.foto img {{ width: 100%; height: 100%; object-fit: contain; padding: 10px; transition: transform .4s; }}
.card:hover .foto img {{ transform: scale(1.05); }}
.peca {{ width: 70%; height: 80%; filter: drop-shadow(0 10px 12px rgba(0,0,0,.15)); transition: transform .25s; }}
.card:hover .peca {{ transform: scale(1.05) rotate(-1deg); }}
.destaque {{ position: absolute; top: 18px; left: 0; background: #222; color: {LARANJA};
            font-family: Oswald, Impact, sans-serif; font-size: 20px; letter-spacing: 3px; text-transform: uppercase;
            padding: 6px 18px 6px 16px; border-radius: 0 999px 999px 0; box-shadow: 0 4px 10px rgba(0,0,0,.18); }}
.preco {{ margin: -26px 18px 0; z-index: 1; background: {LARANJA}; border-radius: 999px; padding: 14px; text-align: center;
         font-size: 20px; box-shadow: 0 6px 14px rgba(245,165,79,.35); }}
.preco s {{ color: #7a5a3a; font-size: 16px; margin-right: 4px; }}
.info {{ padding: 18px 22px 24px; flex: 1; display: flex; flex-direction: column; }}
.info h2 {{ margin: 0 0 10px; font-size: 18px; font-weight: 700; }}
.info p {{ margin: 0; font-size: 13px; color: #666; }}
.comprar {{ margin-top: auto; width: 100%; padding: 13px; border: none; border-radius: 999px; background: #222;
           color: {CREME}; font: inherit; font-weight: 600; cursor: pointer; transition: background .2s; }}
.info p + .comprar {{ margin-top: 16px; }}
.comprar:hover {{ background: #000; }}
.vazio {{ text-align: center; padding: 60px 16px; font-size: 18px; }}

/* ---------- rodapé ---------- */

.aviso {{ position: fixed; left: 50%; bottom: 24px; transform: translate(-50%, 140px); background: #222; color: {CREME};
         padding: 14px 24px; border-radius: 999px; transition: transform .3s; box-shadow: 0 10px 24px rgba(0,0,0,.25);
         max-width: calc(100% - 32px); z-index: 10; }}
.aviso.mostrar {{ transform: translate(-50%, 0); }}

@media (max-width: 760px) {{
  .generos a {{ padding: 10px 22px; }}
  .pilula {{ min-width: 0; flex: 1 1 40%; }}
  .banner {{ height: auto; flex-direction: column; align-items: stretch; }}
  .banner-texto {{ padding: 26px 22px 10px; }}
  .arara {{ max-width: 100%; height: 170px; }}
  .vantagens {{ grid-template-columns: 1fr; }}
}}
"""


TRACO = 'stroke="rgba(0,0,0,.28)" stroke-width="2.5" stroke-linejoin="round"'
CLARO = 'fill="rgba(255,255,255,.35)"'
ESCURO = 'fill="rgba(0,0,0,.13)"'

FORMAS = {
    "camisas": f"""
        <path d="M62 44 L86 32 Q100 46 114 32 L138 44 L178 118 L158 128 L144 100 L144 196 L56 196 L56 100 L42 128 L22 118 Z"/>
        <path {CLARO} d="M86 32 L100 56 L92 62 L80 38 Z M114 32 L100 56 L108 62 L120 38 Z"/>
        <line x1="100" y1="56" x2="100" y2="196"/>
        <rect x="66" y="84" width="22" height="20" rx="2" fill="none"/>
        {''.join(f'<circle cx="104" cy="{y}" r="2.6" fill="rgba(0,0,0,.35)" stroke="none"/>' for y in (80, 108, 136, 164))}""",
    "calcas": f"""
        <path d="M58 18 L142 18 L154 228 L114 228 L100 82 L86 228 L46 228 Z"/>
        <rect {ESCURO} x="58" y="18" width="84" height="14"/>
        <path fill="none" d="M66 32 Q72 52 88 52 M134 32 Q128 52 112 52"/>
        <line x1="100" y1="32" x2="100" y2="74"/>""",
    "tenis": """
        <path d="M18 160 Q20 112 56 104 L86 98 Q104 124 140 128 Q182 132 186 160 Z"/>
        <rect x="14" y="158" width="176" height="18" rx="7" fill="#f7f5f0"/>
        <path fill="none" d="M86 98 Q96 118 112 124"/>
        <line x1="70" y1="110" x2="84" y2="118"/><line x1="76" y1="104" x2="92" y2="114"/><line x1="64" y1="118" x2="78" y2="124"/>""",
    "vestidos": f"""
        <path d="M78 20 L86 20 Q100 40 114 20 L122 20 L126 70 Q124 84 118 92 L168 222 L32 222 L82 92 Q76 84 74 70 Z"/>
        <path {ESCURO} d="M76 86 Q100 96 124 86 L120 98 Q100 106 80 98 Z"/>
        <path fill="none" d="M70 180 Q100 192 130 180" stroke="rgba(255,255,255,.4)"/>""",
    "bolsas": f"""
        <path fill="none" stroke-width="7" d="M70 100 Q70 40 100 40 Q130 40 130 100"/>
        <path d="M38 98 L162 98 L176 214 L24 214 Z"/>
        <rect {ESCURO} x="38" y="98" width="124" height="22"/>
        <rect x="90" y="112" width="20" height="16" rx="3" fill="#d9b25a"/>""",
}
# calça feminina usa o desenho de pantalona (perna larga)
FORMA_CALCA_FEM = f"""
    <path d="M62 18 L138 18 L170 228 L112 228 L100 84 L88 228 L30 228 Z"/>
    <rect {ESCURO} x="62" y="18" width="76" height="14"/>
    <line x1="100" y1="32" x2="100" y2="74"/>"""


def desenho_peca(genero, cat, cor):
    forma = FORMA_CALCA_FEM if (genero == "feminino" and cat == "calcas") else FORMAS[cat]
    return (f'<svg viewBox="0 0 200 240" class="peca" aria-hidden="true">'
            f'<g fill="{cor}" {TRACO}>{forma}</g></svg>')


def desenho_arara(genero):
    if genero == "feminino":
        cores = ["#e3c8b4", "#d98c8c", "#5f7d5a", "#f4f1ea", "#b5603c", "#232326", "#8fb3d9"]
        roupa = "M28 16 L34 16 Q40 26 46 16 L52 16 L54 40 L50 50 L76 150 L4 150 L30 50 L26 40 Z"
    else:
        cores = ["#f4f1ea", "#8fb3d9", "#22324f", "#b5603c", "#5f6b45", "#d8c3a0", "#7a2e3a"]
        roupa = "M16 20 L32 12 Q40 22 48 12 L64 20 L80 74 L68 80 L60 56 L60 140 L20 140 L20 56 L12 80 L0 74 Z"
    cabides = "".join(f"""
        <g transform="translate({40 + i * 78},30)">
          <path d="M40 0 Q40 -10 48 -10" fill="none" stroke="#6b4a33" stroke-width="3"/>
          <path d="M40 0 L10 18 L70 18 Z" fill="none" stroke="#6b4a33" stroke-width="3"/>
          <path d="{roupa}" fill="{cor}" stroke="rgba(0,0,0,.25)" stroke-width="2"/>
        </g>""" for i, cor in enumerate(cores))
    return (f'<svg class="arara" viewBox="0 0 600 260" aria-hidden="true">'
            f'<line x1="20" y1="30" x2="580" y2="30" stroke="#6b4a33" stroke-width="6" stroke-linecap="round"/>'
            f'{cabides}</svg>')



def reais(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def imagem(p):
    if p["foto"] and (PASTA_FOTOS / p["foto"]).exists():
        return f'<img src="/fotos/{escape(p["foto"])}" alt="{escape(p["nome"])}">'
    return desenho_peca(p["genero"], p["cat"], p["cor"])


def card(p):
    preco, promo = p["preco"], p["promo"]
    if promo:
        destaque = '<span class="destaque">Oferta</span>'
        etiqueta = f"R$ <s>{preco}</s> <strong>{promo}!</strong>"
    else:
        destaque, etiqueta = "", f"R$ {preco}"
    nome = escape(p["nome"])
    return f"""
    <article class="card">
      <div class="foto">{imagem(p)}{destaque}</div>
      <div class="preco">{etiqueta}</div>
      <div class="info">
        <h2>{nome}</h2>
        <p>ou 3x de R$ {reais((promo or preco) / 3)} sem juros</p>
        <button class="comprar" data-nome="{nome}">Adicionar à sacola</button>
      </div>
    </article>"""


def pagina(titulo, produtos, genero="masculino", ativa=None):
    abas = "".join(
        f'<a href="/{g}" class="{"ativa" if g == genero else ""}">{info["nome"]}</a>'
        for g, info in GENEROS.items()
    )
    menu = "".join(
        f'<a href="/{genero}/{slug}" class="pilula{" ativa" if slug == ativa else ""}">{nome}</a>'
        for slug, nome in GENEROS[genero]["categorias"].items()
    )
    menu += f'<a href="/{genero}/promocoes" class="pilula{" ativa" if ativa == "promocoes" else ""}">Promoções</a>'

    if produtos:
        conteudo = '<section class="grade" id="produtos">' + "".join(card(p) for p in produtos) + "</section>"
    else:
        conteudo = '<p class="vazio">Nenhum produto nesta seção ainda.</p>'

    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Economia e Estilo · {escape(titulo)}</title>
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>
  <header class="topo">
    <div class="topo-linha">
      <a href="/" class="logo">ECONOMIA E ESTILO<small>MODA MASCULINA &amp; FEMININA</small></a>
    </div>
    <nav class="generos">{abas}</nav>
    <nav class="menu">{menu}</nav>
  </header>
  <main>
    <h1 class="titulo">{escape(titulo)}</h1>
    <section class="banner">
      <div class="banner-texto">
        <p class="banner-chamada">Moda {"feminina" if genero == "feminino" else "masculina"}</p>
        <p class="banner-frase">Estilo de verdade,<br>preço que cabe no bolso.</p>
        <a href="#produtos" class="banner-botao">Ver coleção</a>
      </div>
      {desenho_arara(genero)}
    </section>
    <section class="vantagens">
      <div class="vantagem"><span>🚚</span><div><b>Frete grátis</b><small>em compras acima de R$ 199</small></div></div>
      <div class="vantagem"><span>💳</span><div><b>3x sem juros</b><small>no cartão de crédito</small></div></div>
      <div class="vantagem"><span>🔄</span><div><b>Troca fácil</b><small>até 30 dias após a compra</small></div></div>
    </section>
    {conteudo}
  </main>
  <div id="aviso" class="aviso" role="status"></div>
  <script>
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
</html>"""
    return Response(html, mimetype="text/html")



@app.route("/")
def inicio():
    return redirect("/masculino")


@app.route("/fotos/<path:arquivo>")
def fotos(arquivo):
    return send_from_directory(PASTA_FOTOS, arquivo)


@app.route("/<genero>")
def secao(genero):
    if genero not in GENEROS:
        abort(404)
    primeira = next(iter(GENEROS[genero]["categorias"]))
    return categoria(genero, primeira)


@app.route("/<genero>/promocoes")
def promocoes(genero):
    if genero not in GENEROS:
        abort(404)
    itens = [p for p in PRODUTOS if p["genero"] == genero and p["promo"]]
    return pagina(f"Promoções {GENEROS[genero]['nome']}", itens, genero, "promocoes")


@app.route("/<genero>/<slug>")
def categoria(genero, slug):
    if genero not in GENEROS or slug not in GENEROS[genero]["categorias"]:
        abort(404)
    itens = [p for p in PRODUTOS if p["genero"] == genero and p["cat"] == slug]
    titulo = TITULOS.get((genero, slug), GENEROS[genero]["categorias"][slug])
    return pagina(titulo, itens, genero, slug)


if __name__ == "__main__":
    app.run(debug=True)
