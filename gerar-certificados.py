"""Gera os certificados do treinamento para uma lista de participantes.

Usa certificado-1pagina.html como molde, escreve o nome de cada aluno na linha
e exporta um PDF por participante mais um PDF unico com todos.

Uso:
    python gerar-certificados.py participantes.txt
    python gerar-certificados.py participantes.txt --saida certificados

O arquivo de participantes e um nome por linha. Linhas vazias e as que comecam
com # sao ignoradas. Aceita tambem .csv (usa a primeira coluna).
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import unicodedata

import fitz
from PIL import Image

MOLDE = "certificado-1pagina.html"
W, H = 1123, 794          # A4 paisagem @96dpi
ESCALA = 3                # 288 dpi no PDF final
GAP = 24                  # respiro entre paginas na renderizacao em lote

CSS_NOME = """
  /* nome do participante escrito sobre a linha */
  .nameline{position:relative}
  .nameline .nome{position:absolute;left:0;right:0;bottom:10px;text-align:center;
    font-family:'Playfair Display',serif;font-size:42px;line-height:1.1;
    color:var(--ink);white-space:nowrap}
  .nameline .nome.longo{font-size:34px}
  .nameline .nome.muito-longo{font-size:28px}
"""

FONTE_NOME = ('<link href="https://fonts.googleapis.com/css2?'
              'family=Playfair+Display:wght@500;600&display=swap" rel="stylesheet">')


def achar_chrome():
    for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              shutil.which("chrome"), shutil.which("google-chrome")):
        if p and os.path.exists(p):
            return p
    sys.exit("Chrome nao encontrado. Instale o Google Chrome para gerar os PDFs.")


def ler_nomes(caminho):
    nomes = []
    with open(caminho, encoding="utf-8-sig") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            if "," in linha or ";" in linha:          # csv: primeira coluna
                linha = re.split("[,;]", linha)[0].strip()
            if linha:
                nomes.append(" ".join(linha.split()))
    return nomes


def slug(nome):
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s or "participante"


def classe_por_tamanho(nome):
    if len(nome) > 42:
        return " muito-longo"
    if len(nome) > 30:
        return " longo"
    return ""


def montar_html(nomes, destino="_lote.html"):
    molde = open(MOLDE, encoding="utf-8").read()

    if "Playfair+Display" not in molde:
        molde = molde.replace("</head>", FONTE_NOME + "\n</head>")
    molde = molde.replace("</style>", CSS_NOME + "</style>")

    # a pagina do molde vira o bloco repetido, um por participante
    ini = molde.index("<section class=\"page\">")
    fim = molde.index("</section>") + len("</section>")
    cabeca, pagina, rodape = molde[:ini], molde[ini:fim], molde[fim:]

    if "<div class=\"slot\"></div>" not in pagina:
        sys.exit("O molde nao tem a linha do nome (div.slot). Verifique o "
                 f"{MOLDE}.")

    paginas = []
    for nome in nomes:
        alvo = ('<div class="slot"></div>'
                f'<div class="nome{classe_por_tamanho(nome)}">'
                f'{html.escape(nome)}</div>')
        paginas.append(pagina.replace('<div class="slot"></div>', alvo))

    # separa visualmente as paginas so na renderizacao
    estilo = f"<style>.page + .page{{margin-top:{GAP}px}} html,body{{background:#8a8a8a}}</style>"
    open(destino, "w", encoding="utf-8").write(
        cabeca + estilo + "".join(paginas) + rodape)
    return destino


def renderizar(caminho_html, n):
    total = H * n + GAP * (n - 1)
    saida = os.path.abspath("_lote.png")
    subprocess.run([achar_chrome(), "--headless", "--disable-gpu",
                    f"--window-size={W},{total}", "--hide-scrollbars",
                    f"--force-device-scale-factor={ESCALA}",
                    "--virtual-time-budget=40000",
                    f"--screenshot={saida}",
                    "file:///" + os.path.abspath(caminho_html).replace("\\", "/")],
                   capture_output=True)
    if not os.path.exists(saida):
        sys.exit("O Chrome nao gerou a imagem do lote.")
    return saida


def exportar(png_lote, nomes, pasta):
    Image.MAX_IMAGE_PIXELS = None
    os.makedirs(pasta, exist_ok=True)
    folha = Image.open(png_lote)
    pw, ph, pgap = W * ESCALA, H * ESCALA, GAP * ESCALA
    pt_w, pt_h = 841.89, 595.28

    juntos = fitz.open()
    gerados = []
    for i, nome in enumerate(nomes):
        y = i * (ph + pgap)
        recorte = folha.crop((0, y, pw, y + ph))
        tmp = os.path.join(pasta, f"_{i}.png")
        recorte.save(tmp)

        doc = fitz.open()
        doc.new_page(width=pt_w, height=pt_h).insert_image(
            fitz.Rect(0, 0, pt_w, pt_h), filename=tmp)
        destino = os.path.join(pasta, f"{i+1:02d}-{slug(nome)}.pdf")
        doc.save(destino, deflate=True)
        gerados.append(destino)

        juntos.new_page(width=pt_w, height=pt_h).insert_image(
            fitz.Rect(0, 0, pt_w, pt_h), filename=tmp)
        os.remove(tmp)

    todos = os.path.join(pasta, "TODOS-os-certificados.pdf")
    juntos.save(todos, deflate=True)
    return gerados, todos


def main():
    ap = argparse.ArgumentParser(description="Gera certificados em lote.")
    ap.add_argument("lista", help="arquivo .txt ou .csv com um nome por linha")
    ap.add_argument("--saida", default="certificados", help="pasta de destino")
    args = ap.parse_args()

    nomes = ler_nomes(args.lista)
    if not nomes:
        sys.exit("Nenhum nome encontrado na lista.")
    print(f"{len(nomes)} participantes")

    caminho = montar_html(nomes)
    png = renderizar(caminho, len(nomes))
    gerados, todos = exportar(png, nomes, args.saida)

    for f in (caminho, png):
        if os.path.exists(f):
            os.remove(f)

    print(f"\n{len(gerados)} certificados em {args.saida}/")
    for g in gerados[:5]:
        print("  ", os.path.basename(g))
    if len(gerados) > 5:
        print(f"   ... e mais {len(gerados)-5}")
    print("  ", os.path.basename(todos), "(todos juntos, para imprimir de uma vez)")


if __name__ == "__main__":
    main()
