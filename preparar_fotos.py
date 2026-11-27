
from pathlib import Path
from PIL import Image
from rembg import remove, new_session

PASTA = Path(__file__).parent
ORIGINAIS = PASTA / "fotos_originais"
PRONTAS = PASTA / "fotos"
LARGURA, ALTURA = 900, 1200   # formato 3:4, igual ao card do site
MARGEM = 0.08                 # espaço em volta da peça

PRONTAS.mkdir(exist_ok=True)
sessao = new_session("birefnet-general")   # modelo mais preciso para roupas e pessoas

for foto in sorted(ORIGINAIS.iterdir()):
    if foto.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        continue
    destino = PRONTAS / (foto.stem + ".jpg")
    if destino.exists() and destino.stat().st_mtime > foto.stat().st_mtime:
        print("já pronta:", destino.name)
        continue

    recorte = remove(Image.open(foto).convert("RGB"), session=sessao)   # imagem sem fundo (transparente)
    caixa = recorte.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
    if caixa:
        recorte = recorte.crop(caixa)

    # cabe a peça dentro do quadro com margem
    area_l, area_a = LARGURA * (1 - 2 * MARGEM), ALTURA * (1 - 2 * MARGEM)
    escala = min(area_l / recorte.width, area_a / recorte.height)
    recorte = recorte.resize((round(recorte.width * escala), round(recorte.height * escala)), Image.LANCZOS)

    fundo = Image.new("RGB", (LARGURA, ALTURA), "white")
    pos = ((LARGURA - recorte.width) // 2, (ALTURA - recorte.height) // 2)
    fundo.paste(recorte, pos, recorte)
    fundo.save(destino, quality=90)
    print("pronta:", destino.name)
