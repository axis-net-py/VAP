"""Extrai uma rubrica de uma foto/scan e atualiza a assinatura do certificado.

Funciona com caneta escura sobre papel claro. O fundo do papel e estimado e
subtraido, entao sombra, textura e iluminacao irregular somem sozinhas.
Para papel pautado (caderno), use --azul: ai a tinta e separada pela cor, e as
linhas cinza da pauta ficam de fora.

Uso:
    python atualizar-rubrica.py rubrica.jpg
    python atualizar-rubrica.py rubrica.jpeg --azul
    python atualizar-rubrica.py rubrica.jpg --cor 1a1848 --saida assinatura-jocelaine.png
"""
import argparse
import sys

import numpy as np
from PIL import Image, ImageFilter

try:
    from scipy import ndimage
except ImportError:
    ndimage = None

PADRAO = "assinatura-jocelaine.png"


def alpha_por_fundo(im, forca=1.0):
    """Tinta escura sobre papel claro: subtrai o fundo estimado do papel."""
    cinza = np.array(im.convert("L")).astype(float)
    # o papel e o que sobra depois de um desfoque forte; o traco e fino e some
    fundo = np.array(im.convert("L").filter(ImageFilter.MedianFilter(size=15))
                     .filter(ImageFilter.GaussianBlur(18))).astype(float)
    escuro = np.clip(fundo - cinza, 0, 255)
    lim = max(12.0, np.percentile(escuro, 99.5) * 0.10)
    return np.clip((escuro - lim) / (lim * 3.0) * forca, 0, 1)


def alpha_por_cor(im):
    """Papel pautado: separa a tinta azul da pauta cinza pela dominancia do azul."""
    a = np.array(im.convert("RGB")).astype(float)
    R, B = a[:, :, 0], a[:, :, 2]
    mx, mn = a.max(axis=2), a.min(axis=2)
    azul = np.clip((B - R) / 40.0, 0, 1)
    sat = np.clip((mx - mn) / 45.0, 0, 1)
    esc = np.clip((235 - mx) / 120.0, 0, 1)
    al = azul * sat * 0.55 + azul * esc * 0.8
    al[(B - R) < 10] = 0
    return np.clip((al - 0.12) / 0.62, 0, 1)


def limpar(alpha, minimo=120):
    """Tira respingos e marcas soltas do papel."""
    if ndimage is None:
        return alpha
    rot, n = ndimage.label(alpha > 0.2)
    if n == 0:
        return alpha
    tam = ndimage.sum(alpha > 0.2, rot, range(1, n + 1))
    manter = np.isin(rot, [i + 1 for i, s in enumerate(tam) if s >= minimo])
    saida = alpha.copy()
    saida[~manter] = 0
    print(f"   {n} manchas detectadas, {int((tam >= minimo).sum())} mantidas")
    return saida


def main():
    ap = argparse.ArgumentParser(description="Extrai a rubrica para PNG transparente.")
    ap.add_argument("origem", help="foto ou scan da assinatura")
    ap.add_argument("--saida", default=PADRAO)
    ap.add_argument("--azul", action="store_true",
                    help="papel pautado com caneta azul (separa pela cor)")
    ap.add_argument("--cor", default="1a1848",
                    help="cor final do traco em hex (padrao: azul-tinta escuro)")
    ap.add_argument("--forca", type=float, default=1.35, help="reforco do traco")
    args = ap.parse_args()

    im = Image.open(args.origem)
    if getattr(im, "n_frames", 1) > 1:
        im.seek(0)
    im = im.convert("RGB")
    print(f"origem: {args.origem} {im.size}")

    alpha = alpha_por_cor(im) if args.azul else alpha_por_fundo(im, args.forca)
    alpha = limpar(alpha)
    alpha = np.clip(alpha * args.forca, 0, 1)

    if alpha.max() < 0.2:
        sys.exit("Nao encontrei traco na imagem. Tente outra foto ou use --azul.")

    r, g, b = (int(args.cor[i:i + 2], 16) for i in (0, 2, 4))
    rgba = np.dstack([np.full(alpha.shape, r), np.full(alpha.shape, g),
                      np.full(alpha.shape, b), alpha * 255]).astype("uint8")
    out = Image.fromarray(rgba, "RGBA").filter(ImageFilter.MedianFilter(3))
    caixa = out.getchannel("A").point(lambda v: 255 if v > 45 else 0).getbbox()
    if not caixa:
        sys.exit("Traco fraco demais depois da limpeza.")
    out = out.crop(caixa)

    # largura util de ~1400px ja e suficiente para 288 dpi no certificado
    if out.width > 1400:
        out = out.resize((1400, round(out.height * 1400 / out.width)), Image.LANCZOS)

    out.save(args.saida)
    print(f"gravado: {args.saida} {out.size}")

    prova = Image.new("RGBA", out.size, (253, 250, 244, 255))
    prova.alpha_composite(out)
    prova.convert("RGB").save("_rubrica-prova.png")
    print("prova sobre o creme do certificado: _rubrica-prova.png")


if __name__ == "__main__":
    main()
