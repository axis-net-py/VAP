"""Gera o deck 'Os 9 Passos da Venda Consultiva' no design system VAP.

Reconstroi o material (o modelo da Man Motors serviu so de referencia de conteudo)
com a linguagem visual do certificado: varredura em vortice, formas arredondadas,
Playfair Display + DM Sans e paleta ouro / preto / creme.

Saida: deck-vap.html  ->  PNG por slide  ->  deck-vap.pptx + deck-vap.pdf
"""
import html

W, H = 1920, 1080

# --------------------------------------------------------------------- conteudo
STEPS = [
    dict(n="01", t="Preparação", lead="Antes do contato, estude o cliente.",
         icon="clipboard",
         how=["Conheça a empresa, o mercado e os concorrentes.",
              "Defina o objetivo da visita.",
              "Tenha informações e materiais preparados."],
         focus="O que preciso saber para agregar valor antes mesmo de chegar?",
         note="Preparação reduz improviso. Saber tipo de carga, rota, frota atual, "
              "orçamento e urgência muda a conversa inteira."),
    dict(n="02", t="Conexão e Rapport", lead="As pessoas compram de quem gera confiança.",
         icon="handshake",
         how=["Cumprimente de forma genuína.",
              "Observe o perfil comportamental.",
              "Crie sintonia sem parecer artificial.",
              "Demonstre interesse verdadeiro."],
         focus="Criar um ambiente seguro para conversar.",
         note="Rapport não é bajulação. É respeito, atenção, escuta e postura "
              "profissional desde o primeiro contato."),
    dict(n="03", t="Diagnóstico", lead="Este é o coração da venda consultiva.",
         icon="search",
         how=["Pergunte antes de apresentar.",
              "Explore situação atual, dificuldades e objetivos.",
              "Entenda impactos financeiros e emocionais."],
         focus="Quem pergunta conduz a venda.",
         note="Como fazem hoje? Qual o maior desafio? O que acontece se continuar "
              "assim? Entender vem antes de oferecer."),
    dict(n="04", t="Escuta Ativa", lead="Escutar é diferente de esperar a vez de falar.",
         icon="listen",
         how=["Não interrompa.",
              "Faça anotações.",
              "Confirme o entendimento.",
              "Demonstre empatia."],
         focus="“Se entendi corretamente, o maior problema é…”",
         note="Escuta ativa transmite segurança. Repetir o que o cliente disse evita "
              "erro e aumenta a confiança."),
    dict(n="05", t="Apresentação da Solução", lead="Apresente apenas o que resolve as dores identificadas.",
         icon="truck",
         how=["Não venda características.",
              "Venda benefícios.",
              "Transforme produto em resultado."],
         focus="Produto → Benefício → Resultado",
         note="Não é só motor ou ano. É economia, produtividade, capacidade, menor "
              "risco e adequação à operação do cliente."),
    dict(n="06", t="Geração de Valor", lead="Mostre que o investimento gera retorno.",
         icon="diamond",
         how=["Economia e segurança.",
              "Praticidade e crescimento.",
              "Tranquilidade e lucro."],
         focus="Venda transformação. Não preço.",
         note="Preço sempre pesa quando o valor não está claro. Quando o cliente "
              "percebe retorno, a negociação fica madura."),
    dict(n="07", t="Tratamento das Objeções", lead="Objeção significa interesse.",
         icon="shield",
         how=["Nunca confronte. Primeiro compreenda.",
              "Ouvir, validar, esclarecer e confirmar.",
              "Responda com segurança e exemplos."],
         focus="“Entendo sua preocupação…”",
         note="Objeção não é rejeição. É dúvida, medo ou falta de informação. Acolha "
              "e esclareça."),
    dict(n="08", t="Fechamento", lead="Conduza naturalmente para a decisão.",
         icon="check",
         how=["“Faz sentido para você?”",
              "“Podemos iniciar?”",
              "“Qual a melhor data para começarmos?”"],
         focus="Não pressione. Conduza.",
         note="O fechamento é consequência do diagnóstico, do valor e da confiança. "
              "Pressionar demais quebra o que foi construído."),
    dict(n="09", t="Pós-venda e Fidelização", lead="A venda termina quando começa o relacionamento.",
         icon="star",
         how=["Acompanhe e confirme a satisfação.",
              "Ofereça suporte e novos contatos.",
              "Gere indicações."],
         focus="Cliente satisfeito compra de novo e indica.",
         note="Pós-venda é ativo comercial. Cliente bem acompanhado volta, indica e "
              "fortalece a marca."),
]

MAP = [(s["n"], s["t"]) for s in STEPS]

# ------------------------------------------------------------------------ icones
ICONS = {
    "clipboard": '<rect x="14" y="10" width="20" height="30" rx="4"/>'
                 '<path d="M19 10V7h10v3"/><path d="M19 20h10M19 27h10M19 34h6"/>',
    "handshake": '<path d="M8 22l8-8 8 8-6 6z"/><path d="M40 22l-8-8-8 8 6 6z"/>'
                 '<path d="M18 28l6 6 6-6"/>',
    "search":    '<circle cx="21" cy="21" r="11"/><path d="M29 29l10 10"/>',
    "listen":    '<path d="M17 34c0-6-5-7-5-14a12 12 0 0 1 24 0c0 5-3 7-7 8"/>'
                 '<path d="M22 22a4 4 0 0 1 8 0c0 4-4 4-4 9"/><circle cx="26" cy="38" r="1.6"/>',
    "truck":     '<rect x="7" y="16" width="20" height="16" rx="2"/>'
                 '<path d="M27 21h7l6 6v5h-13z"/><circle cx="16" cy="36" r="3.4"/>'
                 '<circle cx="34" cy="36" r="3.4"/>',
    "diamond":   '<path d="M24 8l14 12-14 20L10 20z"/><path d="M10 20h28M24 8l-6 12 6 20 6-20z"/>',
    "shield":    '<path d="M24 8l14 5v11c0 9-6 14-14 17-8-3-14-8-14-17V13z"/>'
                 '<path d="M18 24l5 5 8-9"/>',
    "check":     '<rect x="12" y="8" width="24" height="32" rx="4"/>'
                 '<path d="M18 20l5 5 9-10"/><path d="M18 31h12"/>',
    "star":      '<path d="M24 8l5 11 12 1.5-9 8 2.5 12L24 34l-10.5 6.5L16 28.5l-9-8L19 19z"/>',
}


def icon(name, size=48):
    return (f'<svg class="ico" viewBox="0 0 48 48" width="{size}" height="{size}" '
            f'fill="none" stroke="currentColor" stroke-width="2.4" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


# ------------------------------------------------------------------- ornamentos
def vortex(op=1.0, ink="#151210", cream="#F4ECDC"):
    """Varredura em vortice: canto inferior-esquerdo + copia girada 180."""
    return f'''
<svg class="orn" viewBox="0 0 {W} {H}" preserveAspectRatio="none" style="opacity:{op}">
  <defs>
    <linearGradient id="gv" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E8C268"/><stop offset="52%" stop-color="#C08A2A"/>
      <stop offset="100%" stop-color="#9C6A1C"/>
    </linearGradient>
  </defs>
  <g id="sw">
    <path d="M0,600 Q20,930 470,1080 L0,1080 Z" fill="url(#gv)"/>
    <path d="M0,548 Q24,900 372,1080 L420,1080 Q22,912 0,572 Z" fill="{ink}"/>
    <path d="M0,496 Q28,868 282,1080 L322,1080 Q26,880 0,518 Z" fill="{cream}"/>
  </g>
  <use href="#sw" transform="rotate(180 {W/2} {H/2})"/>
</svg>'''


def corner():
    """Slides claros ficam limpos: trilho dourado a esquerda e um brilho creme
    nos cantos opostos, sem nada cruzar a area de texto."""
    return f'''
<svg class="orn" viewBox="0 0 {W} {H}" preserveAspectRatio="none">
  <defs>
    <linearGradient id="gr" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E8C268"/><stop offset="55%" stop-color="#C08A2A"/>
      <stop offset="100%" stop-color="#A9741F"/>
    </linearGradient>
    <radialGradient id="gw">
      <stop offset="0%" stop-color="#EEDFBC" stop-opacity=".85"/>
      <stop offset="100%" stop-color="#EEDFBC" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <circle cx="{W}" cy="0" r="560" fill="url(#gw)"/>
  <circle cx="0" cy="{H}" r="560" fill="url(#gw)"/>
  <rect x="0" y="0" width="13" height="{H}" fill="url(#gr)"/>
</svg>'''


def head(title, tag):
    return (f'<header class="hd"><img class="mark" src="logo-jr-dark.png" alt="">'
            f'<h2>{html.escape(title)}</h2><span class="tag">{html.escape(tag)}</span></header>')


FOOT = ('<footer class="ft"><span>Vendas de Alta Performance · O Código das Vendas '
        'Infalíveis</span><span>Disciplina · Organização · Foco · Ação · Resultados</span></footer>')


# --------------------------------------------------------------------- slides
def slide_cover():
    return f'''
<section class="slide dark cover">
  {vortex()}
  <div class="cv-txt">
    <div class="eyebrow">Material de estudo · Equipe comercial</div>
    <div class="gold-rule"></div>
    <h1>Os 9 Passos da<br><em>Venda Consultiva</em></h1>
    <p class="cv-sub">Quanto melhor o diagnóstico, mais natural será o fechamento.</p>
    <div class="cv-badge">80% escutar · 20% falar</div>
  </div>
  <img class="cv-photo" src="jocelaine-branco.png" alt="Jocelaine Rufatto">
  <img class="cv-logo" src="logo-jr.png" alt="Jocelaine Rufatto">
</section>'''


def slide_quote():
    return f'''
<section class="slide dark quote">
  {vortex(0.9)}
  <figure class="q-photo"><img src="cena-consultiva.png" alt=""></figure>
  <div class="q-txt">
    <div class="q-mark">“</div>
    <h1>A venda consultiva não é <em>empurrar produto</em>.</h1>
    <p>É entender a necessidade, gerar confiança e conduzir o cliente
       para uma decisão segura.</p>
  </div>
</section>'''


def slide_map():
    cards = "".join(
        f'<div class="mc"><span class="mc-n">{n}</span><span class="mc-t">{html.escape(t)}</span></div>'
        for n, t in MAP)
    return f'''
<section class="slide light">
  {corner()}
  {head("Mapa do treinamento", "Visão geral")}
  <div class="body map">
    <p class="lead">Nove passos, uma sequência. Cada etapa prepara a seguinte —
       pular uma etapa cobra o preço na frente.</p>
    <div class="mgrid">{cards}</div>
    <div class="rule-strip">Regra de ouro — quanto melhor o diagnóstico,
       menos pressão será necessária no fechamento.</div>
  </div>
  {FOOT}
</section>'''


def slide_step(s, i):
    hows = "".join(f'<li>{html.escape(h)}</li>' for h in s["how"])
    return f'''
<section class="slide light">
  {corner()}
  {head(s["t"], f"Passo {i}/9")}
  <div class="body step">
    <div class="st-head">
      <div class="medal">{icon(s["icon"], 54)}<span class="medal-n">{s["n"]}</span></div>
      <div>
        <h1>{html.escape(s["t"])}</h1>
        <p class="st-lead">{html.escape(s["lead"])}</p>
      </div>
    </div>
    <div class="cols">
      <div class="card">
        <div class="card-k">Como aplicar na prática</div>
        <ul>{hows}</ul>
      </div>
      <div class="card gold">
        <div class="card-k">Ponto de atenção</div>
        <p class="focus">{html.escape(s["focus"])}</p>
      </div>
    </div>
    <div class="note"><span class="note-k">Para estudar e falar</span>
      <p>{html.escape(s["note"])}</p></div>
  </div>
  {FOOT}
</section>'''


def slide_summary():
    steps = "".join(f'<li><span>{n}</span>{html.escape(t)}</li>' for n, t in MAP)
    return f'''
<section class="slide light">
  {corner()}
  {head("Resumo e plano de ação", "Encerramento")}
  <div class="body sum">
    <p class="lead">A excelência comercial nasce da disciplina no básico: perguntar bem,
       registrar corretamente e acompanhar até o cliente ficar satisfeito.</p>
    <div class="cols sum-cols">
      <div class="card">
        <div class="card-k">Os 9 passos</div>
        <ol class="nine">{steps}</ol>
      </div>
      <div class="card gold">
        <div class="card-k">Plano de ação</div>
        <p class="ask">Responda individualmente:</p>
        <ol class="ask-list">
          <li>Qual comportamento vou mudar a partir de segunda-feira?</li>
          <li>Qual ação terá o maior impacto no meu desempenho?</li>
          <li>Como posso contribuir para a equipe alcançar melhores resultados?</li>
        </ol>
      </div>
    </div>
    <div class="rule-strip">80% escutar · 20% falar · diagnosticar antes de apresentar</div>
  </div>
  {FOOT}
</section>'''


def slide_end():
    return f'''
<section class="slide dark end">
  {vortex()}
  <div class="end-txt">
    <img class="end-logo" src="logo-jr.png" alt="Jocelaine Rufatto">
    <div class="gold-rule center"></div>
    <p>Vendas de Alta Performance</p>
    <span>O Código das Vendas Infalíveis</span>
  </div>
</section>'''


CSS = f'''
:root{{
  --ink:#151210; --ink-2:#221c17; --ink-soft:#5F574E;
  --paper:#FDFAF4; --paper-2:#F4ECDC; --card:#FFFFFF;
  --gold:#C08A2A; --gold-deep:#96651A; --gold-lt:#E8C268;
  --line:#E3D3B0;
  --grad:linear-gradient(120deg,#E8C268 0%,#C08A2A 55%,#A9741F 100%);
  --pad:96px;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#6f6f6f}}
.slide{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
  font-family:'DM Sans',sans-serif;color:var(--ink);background:var(--paper)}}
.slide+.slide{{margin-top:28px}}
.slide.dark{{background:var(--ink);color:#fff}}
.orn{{position:absolute;inset:0;width:100%;height:100%;z-index:1}}

h1,h2,.medal-n,.mc-n,.q-mark,.nine span{{font-family:'Playfair Display',serif;font-weight:500}}

/* ---------------- cabecalho e rodape ---------------- */
.hd{{position:absolute;top:0;left:0;right:0;height:118px;z-index:6;
  display:flex;align-items:center;gap:28px;padding:0 var(--pad);
  border-bottom:1px solid var(--line)}}
.hd .mark{{height:40px}}
.hd h2{{flex:1;font-size:38px;letter-spacing:.004em}}
.hd .tag{{font-size:19px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold-deep);
  font-weight:500}}
.ft{{position:absolute;left:var(--pad);right:var(--pad);bottom:46px;z-index:6;
  display:flex;justify-content:space-between;font-size:17px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink-soft);opacity:.8;
  padding-top:20px;border-top:1px solid var(--line)}}

.body{{position:absolute;left:var(--pad);right:var(--pad);top:170px;bottom:150px;z-index:5}}
.lead{{font-size:30px;line-height:1.42;color:var(--ink-soft);max-width:1500px}}

.gold-rule{{width:132px;height:5px;border-radius:3px;background:var(--grad)}}
.gold-rule.center{{margin:0 auto}}

/* ---------------- capa ---------------- */
.cover .cv-txt{{position:absolute;left:var(--pad);top:264px;z-index:5;width:1000px}}
.eyebrow{{font-size:19px;letter-spacing:.34em;text-transform:uppercase;color:var(--gold-lt);
  margin-bottom:26px}}
.cover h1{{margin-top:34px;font-size:104px;line-height:1.03;color:#fff}}
.cover h1 em{{font-style:italic;background:var(--grad);-webkit-background-clip:text;
  background-clip:text;color:transparent}}
.cv-sub{{margin-top:30px;font-size:29px;line-height:1.45;color:#D9D2C7;max-width:820px}}
.cv-badge{{margin-top:40px;display:inline-block;padding:16px 34px;border-radius:999px;
  border:1px solid rgba(232,194,104,.55);color:var(--gold-lt);font-size:20px;
  letter-spacing:.2em;text-transform:uppercase}}
.cv-photo{{position:absolute;right:96px;bottom:0;height:1005px;z-index:4;
  filter:drop-shadow(-30px 20px 60px rgba(0,0,0,.55))}}
.cv-logo{{position:absolute;left:var(--pad);top:84px;z-index:6;height:62px}}

/* ---------------- citacao ---------------- */
.q-photo{{position:absolute;right:var(--pad);top:120px;width:620px;height:840px;z-index:4;
  border-radius:46px;overflow:hidden;border:1px solid rgba(232,194,104,.4);
  box-shadow:0 30px 70px rgba(0,0,0,.5)}}
.q-photo img{{width:100%;height:100%;object-fit:cover;object-position:50% 22%}}
.q-txt{{position:absolute;left:var(--pad);top:250px;width:980px;z-index:5}}
.q-mark{{font-size:150px;line-height:.6;color:var(--gold);opacity:.85}}
.quote h1{{margin-top:34px;font-size:64px;line-height:1.16;color:#fff}}
.quote h1 em{{font-style:italic;color:var(--gold-lt)}}
.quote p{{margin-top:32px;font-size:29px;line-height:1.5;color:#CDC5B8;max-width:880px}}

/* ---------------- mapa ---------------- */
.map{{display:flex;flex-direction:column}}
.mgrid{{margin-top:40px;display:grid;
  grid-template-columns:repeat(3,1fr);gap:26px;flex:1;align-content:center}}
.mc{{display:flex;align-items:center;gap:26px;background:var(--card);
  border:1px solid var(--line);border-radius:26px;padding:30px 34px;
  box-shadow:0 10px 26px rgba(21,18,16,.05)}}
.mc-n{{font-size:44px;color:var(--gold);min-width:66px}}
.mc-t{{font-size:29px;font-weight:500}}
.rule-strip{{margin-top:34px;background:var(--ink);color:#F0E7D6;
  border-radius:22px;padding:26px 40px;font-size:23px;text-align:center;letter-spacing:.01em}}

/* ---------------- passo ---------------- */
.st-head{{display:flex;align-items:center;gap:38px}}
.medal{{position:relative;width:150px;height:150px;flex:none;border-radius:44px;
  background:var(--grad);color:var(--ink);display:flex;align-items:center;
  justify-content:center;box-shadow:0 16px 34px rgba(192,138,42,.32)}}
.medal-n{{position:absolute;right:-12px;bottom:-14px;width:66px;height:66px;
  border-radius:22px;background:var(--ink);color:var(--gold-lt);font-size:29px;
  display:flex;align-items:center;justify-content:center}}
.step h1{{font-size:60px;line-height:1.06}}
.st-lead{{margin-top:12px;font-size:29px;color:var(--ink-soft)}}

/* passo: cabeca, cartoes que esticam e a faixa escura no rodape */
.step{{display:flex;flex-direction:column}}
.cols{{margin-top:46px;display:grid;grid-template-columns:1.18fr 1fr;gap:34px;flex:1}}
.card{{display:flex;flex-direction:column}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:32px;
  padding:38px 42px;box-shadow:0 12px 30px rgba(21,18,16,.05)}}
.card.gold{{background:var(--paper-2);border-color:#DFC894}}
.card-k{{font-size:17px;letter-spacing:.24em;text-transform:uppercase;
  color:var(--gold-deep);font-weight:500;margin-bottom:24px}}
.card ul{{list-style:none}}
.card ul li{{position:relative;padding-left:34px;font-size:27px;line-height:1.5;
  margin-bottom:16px}}
.card ul li:last-child{{margin-bottom:0}}
.card ul{{margin:auto 0}}
.card ul li::before{{content:"";position:absolute;left:0;top:14px;width:11px;height:11px;
  transform:rotate(45deg);background:var(--grad)}}
.focus{{font-size:31px;line-height:1.42;color:var(--gold-deep);font-weight:500;
  margin:auto 0}}

.note{{margin-top:34px;background:var(--ink);border-radius:26px;padding:30px 40px}}
.note-k{{display:block;font-size:16px;letter-spacing:.24em;text-transform:uppercase;
  color:var(--gold-lt);margin-bottom:12px}}
.note p{{font-size:24px;line-height:1.45;color:#EDE5D8}}

/* ---------------- resumo ---------------- */
.sum{{display:flex;flex-direction:column}}
.sum-cols{{margin-top:40px;grid-template-columns:1fr 1fr}}
.nine{{list-style:none;columns:2;column-gap:44px}}
.nine li{{display:flex;gap:16px;font-size:25px;line-height:1.4;margin-bottom:15px;
  break-inside:avoid}}
.nine li span{{color:var(--gold);min-width:42px}}
.ask{{font-size:22px;color:var(--ink-soft);margin-bottom:20px}}
.ask-list{{padding-left:26px}}
.ask-list li{{font-size:25px;line-height:1.42;margin-bottom:16px}}
.ask-list li::marker{{color:var(--gold);font-weight:600}}

/* ---------------- encerramento ---------------- */
.end-txt{{position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:26px;text-align:center}}
.end-logo{{height:120px}}
.end-txt p{{font-size:40px;font-family:'Playfair Display',serif}}
.end-txt span{{font-size:24px;letter-spacing:.26em;text-transform:uppercase;
  color:var(--gold-lt)}}

@page{{size:{W}px {H}px;margin:0}}
'''


def build_html(path="deck-vap.html"):
    slides = [slide_cover(), slide_quote(), slide_map()]
    slides += [slide_step(s, i) for i, s in enumerate(STEPS, 1)]
    slides += [slide_summary(), slide_end()]
    doc = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{"".join(slides)}</body></html>'''
    open(path, "w", encoding="utf-8").write(doc)
    return path, len(slides)


if __name__ == "__main__":
    p, n = build_html()
    print(f"{p}: {n} slides")
