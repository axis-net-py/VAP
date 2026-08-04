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
POR_LOTE = 6              # paginas por captura (o Chrome nao passa de ~16k px)

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


def exportar_lote(png_lote, nomes, pasta, offset, juntos):
    Image.MAX_IMAGE_PIXELS = None
    folha = Image.open(png_lote)
    pw, ph, pgap = W * ESCALA, H * ESCALA, GAP * ESCALA
    pt_w, pt_h = 841.89, 595.28

    gerados = []
    for i, nome in enumerate(nomes):
        y = i * (ph + pgap)
        tmp = os.path.join(pasta, f"_{offset+i}.png")
        folha.crop((0, y, pw, y + ph)).save(tmp)

        doc = fitz.open()
        doc.new_page(width=pt_w, height=pt_h).insert_image(
            fitz.Rect(0, 0, pt_w, pt_h), filename=tmp)
        destino = os.path.join(pasta, f"{offset+i+1:03d}-{slug(nome)}.pdf")
        doc.save(destino, deflate=True)
        gerados.append(destino)

        juntos.new_page(width=pt_w, height=pt_h).insert_image(
            fitz.Rect(0, 0, pt_w, pt_h), filename=tmp)
        os.remove(tmp)
    folha.close()
    return gerados


def main():
    ap = argparse.ArgumentParser(description="Gera certificados em lote.")
    ap.add_argument("lista", help="arquivo .txt ou .csv com um nome por linha")
    ap.add_argument("--saida", default="certificados", help="pasta de destino")
    args = ap.parse_args()

    nomes = ler_nomes(args.lista)
    if not nomes:
        sys.exit("Nenhum nome encontrado na lista.")
    os.makedirs(args.saida, exist_ok=True)
    lotes = [nomes[i:i + POR_LOTE] for i in range(0, len(nomes), POR_LOTE)]
    print(f"{len(nomes)} participantes em {len(lotes)} lotes de ate {POR_LOTE}")

    juntos = fitz.open()
    gerados = []
    for n, lote in enumerate(lotes, 1):
        caminho = montar_html(lote)
        png = renderizar(caminho, len(lote))
        gerados += exportar_lote(png, lote, args.saida, len(gerados), juntos)
        for f in (caminho, png):
            if os.path.exists(f):
                os.remove(f)
        print(f"  lote {n}/{len(lotes)} - {len(gerados)} prontos")

    todos = os.path.join(args.saida, "TODOS-os-certificados.pdf")
    juntos.save(todos, deflate=True)

    print(f"\n{len(gerados)} certificados em {args.saida}/")
    print("  ", os.path.basename(gerados[0]), "...", os.path.basename(gerados[-1]))
    print("  ", os.path.basename(todos), "(todos juntos, para imprimir de uma vez)")


if __name__ == "__main__":
    main()
