# Banner-isca — Workshop de Vendas de Alta Performance

**Data:** 2026-07-23
**Repo:** VAP (github.com/axis-net-py/VAP)

## Objetivo

Banner físico para ficar exposto durante a semana na Churrascaria Costelão (San Alberto — PY). Função de **isca**: despertar interesse do público do restaurante no workshop de vendas, sem data e sem valor. Quem se interessa escaneia o QR, cai no WhatsApp da Jocelaine (bot futuro sana dúvidas e encaminha ao formulário), e ela fecha na conversa.

Sem data/valor = peça reutilizável em todas as edições do workshop; nunca vence.

## Decisões (travadas no brainstorm)

- **Um banner só** (não dois). Isca reutilizável.
- **Formato:** banner 130 × 180 cm (largura × altura). Proporção ~3:4.
- **QR → WhatsApp** `wa.me/595987244284` com mensagem pronta.
- **Sem ACISA, sem data, sem valor.**
- **Foto** da Jocelaine de corpo inteiro (`jocelaine-3.png` — terno creme), recortada do fundo.
- **Tema claro** (creme/branco + dourado), estilo dos modelos de referência de workshop/webinar.
- **Estilo visual:** foto da Jocelaine **recortada do fundo** (rembg) sobreposta a formas curvas douradas; "Workshop" em destaque; pequena área de tópicos/benefícios.

## Conteúdo (texto exato)

- **Título:** Workshop de Vendas de Alta Performance!
- **Módulos do treinamento** (lista, marcadores dourados — emojis substituídos para não destoar da paleta na impressão):
  Perfil Comportamental · Técnicas de PNL · Comunicação Persuasiva · Negociação Estratégica · Quebra de Objeções · Fechamento de Vendas · Alta Performance Comercial
- **Frase de impacto:** "Vender não é dom. **É método.**"
- **Slogan:** O Código das Vendas Infalíveis
- **Assinatura:** com Jocelaine Rufatto
- **CTA:** Garanta sua vaga acessando o link no QR Code
- **QR:** `https://wa.me/595987244284?text=Oi%20Jocelaine!%20Vi%20o%20banner%20no%20Costel%C3%A3o%20e%20quero%20saber%20do%20Workshop%20de%20Vendas%20de%20Alta%20Performance`

## Layout — leitura em 3 distâncias

Banner 130×180 cm. Estrutura de cima para baixo (faixa central em duas colunas, aproveitando a largura):

1. **Barra dourada** no topo (assinatura visual).
2. **~4m / gancho:** título "Workshop de Vendas de Alta Performance!" grande (Anton), com "Performance!" em dourado.
3. **~2m / quem+o quê:** duas colunas — à esquerda a foto da Jocelaine recortada sobre disco dourado; à direita slogan (Fraunces itálico), "com Jocelaine Rufatto", filete dourado, lista dos módulos e a frase de impacto.
5. **~1m / ação:** QR grande (mín. 8×8 cm impresso) + "Garanta sua vaga acessando o link no QR Code" + ícone/label WhatsApp.
6. **Logo** Jocelaine Rufatto (versão branca `logo-jr.png`) no rodapé.

**Zona de segurança:** ~7,5 cm de margem interna em todos os lados — nada crítico nessa faixa.

## Design system

- Cores (tema claro): fundo creme `#faf7f2`, dourado `#c08a2a` / gradiente `#d9a84a→#a9741f`, tinta `#151210`, muted `#5f574e`. Mesmo dourado do flyer de parceria ACISA (contraste em fundo claro).
- Fontes: Anton (títulos/"Workshop"), Fraunces itálico (slogan/"Join our" style), Poppins (corpo).
- Formas curvas douradas atrás/ao redor da foto recortada (estilo dos modelos de referência).
- Foto recortada (`jocelaine-cut.png`) sobrepondo as curvas, saindo da moldura.

## Especificação técnica de saída

- **Fonte:** HTML único (`banner.html`) renderizado via Chrome headless (mesmo pipeline dos flyers).
- **Proporção de trabalho:** 1300×1800 px (10 px/cm) para preview/tela.
- **QR:** gerado como PNG (biblioteca `qrcode` Python ou API), embutido no HTML como `<img>`. Nível de correção de erro Q ou H (tolera desgaste do banner). Cor: escuro sobre módulo claro para garantir contraste de leitura — QR sobre placa clara arredondada, não sobre o preto.
- **Entregas:**
  - `banner.png` — preview 1300×1800 px.
  - `banner.pdf` — 130×180 cm, escala vetorial, cores forçadas (`print-color-adjust:exact`), gradientes dourados convertidos para cor sólida no PDF (evita artefato vetorial, como nos flyers).
- **Gráfica:** o PDF em cm é o arquivo final; a gráfica trata bleed/sangria. Incluir margem interna generosa já cobre a sangria.

## Fora de escopo

- **Bot de WhatsApp** — projeto separado. O QR aponta para um número; funciona com bot ou atendimento humano. Especificar depois (plataforma, fluxo, custo).
- Segundo banner / versão institucional atemporal.
- Versão para redes (já existem flyers).

## Arquivos no repo

- Novos: `banner.html`, `banner.png`, `banner.pdf`, `banner-qr.png`.
- Reutiliza: `jocelaine-3.png` (foto de corpo inteiro), `logo-jr-dark.png`.
