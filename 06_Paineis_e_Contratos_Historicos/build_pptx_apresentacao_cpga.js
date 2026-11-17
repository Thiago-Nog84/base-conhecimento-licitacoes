const pptxgen = require("pptxgenjs");

// ===== Paleta oficial MPPI (Manual de Identidade Visual 2025) =====
const RED = "A60225";
const RED_DARK = "7A011C";
const BLACK = "000000";
const GREY = "5A5A5A";
const LIGHTGREY = "E2E2E5";
const CARDGREY = "AFAFB4";
const WHITE = "FFFFFF";

const TITLE_FONT = "Piximisa"; // fonte oficial de títulos do manual — se não instalada, PowerPoint substitui
const BODY_FONT = "Calibri"; // fonte oficial de corpo de texto do manual

const ASSETS = "/sessions/quirky-zen-bardeen/mnt/outputs/assets/";
const BG_CONTENT = ASSETS + "bg_content.png";
const BG_RED = ASSETS + "bg_red_diagonal.png";
const LOGO = ASSETS + "logo_preferencial.png";

const SLIDE_W = 13.333;
const SLIDE_H = 7.5;
const MARGIN = 0.6;

const pres = new pptxgen();
pres.defineLayout({ name: "MPPI_WIDE", width: SLIDE_W, height: SLIDE_H });
pres.layout = "MPPI_WIDE";

// ===================== Helpers =====================

function addBgLight(slide) {
  slide.background = { color: WHITE };
  slide.addImage({ path: BG_CONTENT, x: 0, y: 0, w: SLIDE_W, h: SLIDE_H, sizing: { type: "cover", w: SLIDE_W, h: SLIDE_H } });
}

function addBgRed(slide) {
  slide.background = { color: RED };
  slide.addImage({ path: BG_RED, x: 0, y: 0, w: SLIDE_W, h: SLIDE_H, sizing: { type: "cover", w: SLIDE_W, h: SLIDE_H } });
}

function addLogoCorner(slide, opts = {}) {
  const w = opts.w || 1.3;
  const h = w * (575 / 1949);
  const x = opts.x != null ? opts.x : SLIDE_W - w - 0.4;
  const y = opts.y != null ? opts.y : SLIDE_H - h - 0.35;
  slide.addImage({ path: LOGO, x, y, w, h });
}

function addLogoOnRed(slide, opts = {}) {
  // Sobre fundo vermelho: caixa branca com opacidade, seguindo a regra do manual (p.12) para fundos inconstantes
  const w = opts.w || 3.6;
  const h = w * (575 / 1949);
  const x = opts.x != null ? opts.x : (SLIDE_W - w) / 2;
  const y = opts.y != null ? opts.y : 0.55;
  slide.addShape("rect", { x: x - 0.25, y: y - 0.18, w: w + 0.5, h: h + 0.36, fill: { color: WHITE, transparency: 15 }, line: { type: "none" } });
  slide.addImage({ path: LOGO, x, y, w, h });
}

function addKicker(slide, text, opts = {}) {
  const x = opts.x != null ? opts.x : MARGIN;
  const y = opts.y != null ? opts.y : 0.45;
  const w = opts.w || 5.3;
  const h = 0.46;
  slide.addShape("roundRect", { x, y, w, h, rectRadius: 0.08, fill: { color: RED }, line: { type: "none" } });
  slide.addText(text.toUpperCase(), {
    x, y, w, h, align: "center", valign: "middle",
    fontFace: BODY_FONT, fontSize: 13, bold: true, color: WHITE, charSpacing: 1, margin: 0,
  });
}

function addTitle(slide, text, opts = {}) {
  const y = opts.y != null ? opts.y : 0.95;
  const color = opts.color || BLACK;
  const fontSize = opts.fontSize || 32;
  slide.addText(text.toUpperCase(), {
    x: MARGIN, y, w: SLIDE_W - MARGIN * 2, h: opts.h || 0.95,
    fontFace: TITLE_FONT, fontSize, bold: true, color, align: opts.align || "left",
    valign: "top", margin: 0, lineSpacingMultiple: 1.0,
  });
}

function addFooterNum(slide, n) {
  slide.addText(String(n).padStart(2, "0"), {
    x: 0.35, y: SLIDE_H - 0.55, w: 0.8, h: 0.35, fontFace: BODY_FONT, fontSize: 12, color: GREY, margin: 0,
  });
}

function card(slide, x, y, w, h, opts = {}) {
  slide.addShape("roundRect", {
    x, y, w, h, rectRadius: 0.09,
    fill: { color: opts.fill || LIGHTGREY },
    line: opts.line === false ? { type: "none" } : { color: opts.lineColor || CARDGREY, width: 1.5 },
    shadow: { type: "outer", color: "000000", opacity: 0.22, blur: 5, offset: 2, angle: 90 },
  });
}

function bulletList(slide, items, opts = {}) {
  const x = opts.x != null ? opts.x : MARGIN;
  const y = opts.y != null ? opts.y : 2.1;
  const w = opts.w || SLIDE_W - MARGIN * 2;
  const fontSize = opts.fontSize || 17;
  const color = opts.color || BLACK;
  const paras = items.map((t, i) => ({
    text: t,
    options: { bullet: { code: "25A0", indent: 18 }, color: opts.bulletColor || RED, breakLine: i < items.length - 1 },
  }));
  slide.addText(
    items.map((t, i) => ({ text: t, options: { bullet: { code: "25A0", indent: 18 }, color, breakLine: i < items.length - 1 } })),
    { x, y, w, h: opts.h || 3.2, fontFace: BODY_FONT, fontSize, color, valign: "top", margin: 0, paraSpaceAfter: opts.spaceAfter || 10, lineSpacingMultiple: 1.05 }
  );
}

function statBox(slide, x, y, w, h, number, label, opts = {}) {
  card(slide, x, y, w, h);
  slide.addText(number, {
    x: x + 0.15, y: y + 0.18, w: w - 0.3, h: h * 0.55, align: "center", valign: "bottom",
    fontFace: TITLE_FONT, fontSize: opts.fontSize || 34, bold: true, color: RED, margin: 0,
  });
  slide.addText(label, {
    x: x + 0.15, y: y + h * 0.62, w: w - 0.3, h: h * 0.34, align: "center", valign: "top",
    fontFace: BODY_FONT, fontSize: 14, color: GREY, margin: 0,
  });
}

function flowRow(slide, items, x, y, w, h, opts = {}) {
  const n = items.length;
  const gap = opts.gap != null ? opts.gap : 0.18;
  const boxW = (w - gap * (n - 1)) / n;
  items.forEach((label, i) => {
    const bx = x + i * (boxW + gap);
    slide.addShape("roundRect", {
      x: bx, y, w: boxW, h, rectRadius: 0.08,
      fill: { color: i % 2 === 0 ? RED : GREY },
      line: { type: "none" },
    });
    slide.addText(String(i + 1 + (opts.startIndex || 0)), {
      x: bx + 0.08, y: y + 0.08, w: 0.4, h: 0.32, fontFace: BODY_FONT, fontSize: 13, bold: true, color: WHITE, margin: 0,
    });
    slide.addText(label, {
      x: bx + 0.12, y: y + 0.4, w: boxW - 0.24, h: h - 0.5, fontFace: BODY_FONT, fontSize: opts.labelSize || 14, color: WHITE,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.02, bold: true,
    });
    if (i < n - 1) {
      slide.addText("▶", {
        x: bx + boxW, y: y + h / 2 - 0.15, w: gap, h: 0.3, align: "center", valign: "middle",
        fontFace: BODY_FONT, fontSize: 15, bold: true, color: GREY, margin: 0,
      });
    }
  });
}

function placeholderFrame(slide, x, y, w, h, label) {
  slide.addShape("roundRect", { x, y, w, h, rectRadius: 0.06, fill: { color: "FBFBFB" }, line: { color: CARDGREY, width: 1.5, dashType: "dash" } });
  // barra de "navegador" no topo, para simular print de tela
  slide.addShape("roundRect", { x, y, w, h: 0.35, rectRadius: 0.06, fill: { color: "E4E4E4" }, line: { type: "none" } });
  ["A60225", "5A5A5A", "5A5A5A"].forEach((c, i) => {
    slide.addShape("ellipse", { x: x + 0.15 + i * 0.22, y: y + 0.11, w: 0.13, h: 0.13, fill: { color: c }, line: { type: "none" } });
  });
  slide.addText("SUBSTITUIR POR PRINT REAL DO SISTEMA", {
    x, y: y + h / 2 - 0.6, w, h: 0.45, align: "center", fontFace: BODY_FONT, fontSize: 14, bold: true, color: GREY, margin: 0,
  });
  slide.addText(label, {
    x, y: y + h / 2 - 0.05, w, h: 0.55, align: "center", fontFace: TITLE_FONT, fontSize: 22, bold: true, color: RED, margin: 0,
  });
}

function chip(slide, x, y, w, text) {
  const h = 0.58;
  slide.addShape("roundRect", { x, y, w, h, rectRadius: 0.29, fill: { color: RED }, line: { type: "none" } });
  slide.addText(text, { x: x + 0.15, y, w: w - 0.3, h, align: "center", valign: "middle", fontFace: BODY_FONT, fontSize: 15, bold: true, color: WHITE, margin: 0 });
}

// ===================== SLIDE 1 — CAPA =====================
{
  const s = pres.addSlide();
  addBgRed(s);
  addLogoOnRed(s, { y: 0.5 });
  s.addShape("roundRect", { x: 2.77, y: 2.5, w: 2.3, h: 0.48, rectRadius: 0.09, fill: { color: WHITE }, line: { type: "none" } });
  s.addText("CLCA", { x: 2.77, y: 2.5, w: 2.3, h: 0.48, align: "center", valign: "middle", fontFace: BODY_FONT, fontSize: 17, bold: true, color: RED, charSpacing: 2, margin: 0 });
  s.addText("ELABORAÇÃO, EXECUÇÃO E CONTROLE DO\nPLANO DE CONTRATAÇÃO ANUAL", {
    x: MARGIN, y: 3.15, w: SLIDE_W - MARGIN * 2, h: 1.55, align: "center", valign: "top",
    fontFace: TITLE_FONT, fontSize: 37, bold: true, color: WHITE, margin: 0, lineSpacingMultiple: 1.05,
  });
  s.addText("EXPERIÊNCIA MPPI", {
    x: MARGIN, y: 4.6, w: SLIDE_W - MARGIN * 2, h: 0.65, align: "center", valign: "top",
    fontFace: TITLE_FONT, fontSize: 26, bold: true, color: WHITE, margin: 0,
  });
  s.addText("3º Encontro Nacional de Gestão Administrativa do Ministério Público  ·  CPGA 3.0", {
    x: MARGIN, y: 5.45, w: SLIDE_W - MARGIN * 2, h: 0.4, align: "center",
    fontFace: BODY_FONT, fontSize: 15, italic: true, color: WHITE, margin: 0,
  });
  s.addText("5 de agosto  ·  Procuradoria-Geral do Trabalho, Brasília/DF", {
    x: MARGIN, y: 5.85, w: SLIDE_W - MARGIN * 2, h: 0.4, align: "center",
    fontFace: BODY_FONT, fontSize: 14, color: WHITE, margin: 0,
  });
}

// ===================== SLIDE 2 — Painel e Painelistas =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addKicker(s, "Bloco 1 · Abertura e Alinhamento");
  addTitle(s, "As experiências do MPPI com o PCA:", { y: 1.05, fontSize: 26 });
  s.addText("DO ANALÓGICO AO DIGITAL", { x: MARGIN, y: 1.7, w: SLIDE_W - MARGIN * 2, h: 0.6, fontFace: TITLE_FONT, fontSize: 26, bold: true, color: RED, margin: 0 });

  const cardW = 5.4, cardH = 3.15, gap = 0.9;
  const startX = (SLIDE_W - (cardW * 2 + gap)) / 2;
  const y = 3.15;
  [
    { nome: "Afrânio Oliveira", cargo: "Analista Ministerial\nCoordenador de Licitações e Contratos · Gestor do PCA" },
    { nome: "Thiago Nogueira", cargo: "Técnico Ministerial\nAssessor de Compras" },
  ].forEach((p, i) => {
    const x = startX + i * (cardW + gap);
    card(s, x, y, cardW, cardH, { fill: LIGHTGREY });
    s.addShape("ellipse", { x: x + cardW / 2 - 0.6, y: y + 0.3, w: 1.1, h: 1.1, fill: { color: RED }, line: { type: "none" } });
    const iniciais = p.nome.split(" ").map((w) => w[0]).slice(0, 2).join("");
    s.addText(iniciais, { x: x + cardW / 2 - 0.6, y: y + 0.3, w: 1.1, h: 1.1, align: "center", valign: "middle", fontFace: TITLE_FONT, fontSize: 28, bold: true, color: WHITE, margin: 0 });
    s.addText(p.nome, { x: x + 0.2, y: y + 1.6, w: cardW - 0.4, h: 0.5, align: "center", fontFace: BODY_FONT, fontSize: 21, bold: true, color: BLACK, margin: 0 });
    s.addText(p.cargo, { x: x + 0.2, y: y + 2.1, w: cardW - 0.4, h: 0.95, align: "center", fontFace: BODY_FONT, fontSize: 14.5, color: GREY, margin: 0, lineSpacingMultiple: 1.2 });
  });
  addLogoCorner(s);
  addFooterNum(s, 2);
}

// ===================== SLIDE 3 — Mensagem Inicial =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  s.addText("“", { x: SLIDE_W / 2 - 3.5, y: 1.5, w: 1.2, h: 1.4, fontFace: "Georgia", fontSize: 130, bold: true, color: RED, margin: 0 });
  s.addText("Unir-se é um bom começo, manter a união é um\nprogresso, e trabalhar em conjunto é a vitória.", {
    x: MARGIN + 0.3, y: 2.9, w: SLIDE_W - MARGIN * 2 - 0.6, h: 1.7, align: "center",
    fontFace: BODY_FONT, fontSize: 29, italic: true, color: BLACK, margin: 0, lineSpacingMultiple: 1.2,
  });
  s.addText("— Henry Ford", {
    x: MARGIN, y: 4.8, w: SLIDE_W - MARGIN * 2, h: 0.5, align: "center",
    fontFace: BODY_FONT, fontSize: 18, bold: true, color: RED, margin: 0,
  });
  addLogoCorner(s);
  addFooterNum(s, 3);
}

// ===================== SLIDE 4 — Objetivos =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addTitle(s, "O que faremos hoje?", { fontSize: 32 });
  s.addText("OBJETIVOS DESTE PAINEL", { x: MARGIN, y: 1.68, w: SLIDE_W - MARGIN * 2, h: 0.4, fontFace: BODY_FONT, fontSize: 16, color: GREY, margin: 0 });

  const items = [
    "Apresentar as experiências do MPPI na elaboração, execução e controle do PCA.",
    "Mostrar a parte prática: uma demonstração do sistema PCA em uso.",
  ];
  const cardH = 1.75, gapY = 0.5, y0 = 2.65;
  items.forEach((t, i) => {
    const y = y0 + i * (cardH + gapY);
    card(s, MARGIN, y, SLIDE_W - MARGIN * 2, cardH, { fill: LIGHTGREY });
    s.addShape("ellipse", { x: MARGIN + 0.35, y: y + cardH / 2 - 0.45, w: 0.9, h: 0.9, fill: { color: RED }, line: { type: "none" } });
    s.addText(String(i + 1), { x: MARGIN + 0.35, y: y + cardH / 2 - 0.45, w: 0.9, h: 0.9, align: "center", valign: "middle", fontFace: TITLE_FONT, fontSize: 28, bold: true, color: WHITE, margin: 0 });
    s.addText(t, { x: MARGIN + 1.6, y, w: SLIDE_W - MARGIN * 2 - 1.9, h: cardH, valign: "middle", fontFace: BODY_FONT, fontSize: 20, color: BLACK, margin: 0, lineSpacingMultiple: 1.15 });
  });
  addLogoCorner(s);
  addFooterNum(s, 4);
}

// ===================== SLIDE 5 — O que é o PCA? =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addKicker(s, "Bloco 2 · O Desafio e o Contexto");
  addTitle(s, "O que é o PCA?");

  const cardW = 5.7, cardH = 3.15, gap = 0.53;
  const y = 2.55;
  card(s, MARGIN, y, cardW, cardH, { fill: LIGHTGREY });
  s.addText("Instrumento de planejamento", { x: MARGIN + 0.3, y: y + 0.22, w: cardW - 0.6, h: 0.5, fontFace: BODY_FONT, fontSize: 17, bold: true, color: RED, margin: 0 });
  s.addText(
    "O PCA consolida as compras e as renovações de contratos de um órgão público para o ano seguinte. Previsto na Lei nº 14.133/2021, organiza gastos, melhora o uso do dinheiro público e dá mais transparência à administração.",
    { x: MARGIN + 0.3, y: y + 0.72, w: cardW - 0.6, h: cardH - 0.95, fontFace: BODY_FONT, fontSize: 14.5, color: BLACK, margin: 0, lineSpacingMultiple: 1.22 }
  );
  const x2 = MARGIN + cardW + gap;
  card(s, x2, y, cardW, cardH, { fill: LIGHTGREY });
  s.addText("O que diz a Lei 14.133/2021", { x: x2 + 0.3, y: y + 0.22, w: cardW - 0.6, h: 0.5, fontFace: BODY_FONT, fontSize: 17, bold: true, color: RED, margin: 0 });
  s.addText(
    [
      { text: "Art. 12, VII — ", options: { bold: true, color: BLACK } },
      { text: "os órgãos responsáveis pelo planejamento de cada ente federativo poderão, na forma de regulamento, elaborar plano de contratações anual.", options: { color: BLACK }, breakLine: true },
      { text: "\nArt. 11, parágrafo único — ", options: { bold: true, color: BLACK } },
      { text: "a alta administração do órgão ou entidade é responsável pela governança das contratações e deve implementar processos e estruturas (...)", options: { color: BLACK } },
    ],
    { x: x2 + 0.3, y: y + 0.72, w: cardW - 0.6, h: cardH - 0.95, fontFace: BODY_FONT, fontSize: 13, margin: 0, lineSpacingMultiple: 1.2 }
  );
  addLogoCorner(s);
  addFooterNum(s, 5);
}

// ===================== SLIDE 6 — Ecossistema de contratações =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addTitle(s, "Como está estruturado o ecossistema", { fontSize: 26 });
  s.addText("DE CONTRATAÇÕES DO MPPI?", { x: MARGIN, y: 1.6, w: SLIDE_W - MARGIN * 2, h: 0.55, fontFace: TITLE_FONT, fontSize: 26, bold: true, color: RED, margin: 0 });

  flowRow(
    s,
    ["PGJ", "Ordenador de\nDespesas", "Planejamento e\nControle\nOrçamentário", "Controladoria\nInterna", "Licitações e\nContratos\n(Gestão do PCA)", "Fiscais de\nContratos", "Unidades\nRequisitantes"],
    MARGIN, 3.15, SLIDE_W - MARGIN * 2, 2.25, { labelSize: 12, gap: 0.14 }
  );
  s.addText("Unidades Requisitantes conforme art. 7º, § 1º do Ato PGJ-PI nº 1381/2024  ·  fluxo de responsabilidade, da ordenação de despesa ao pedido que nasce na ponta.", {
    x: MARGIN, y: 5.7, w: SLIDE_W - MARGIN * 2, h: 0.5, align: "center", fontFace: BODY_FONT, fontSize: 13, italic: true, color: GREY, margin: 0,
  });
  addLogoCorner(s);
  addFooterNum(s, 6);

  s.addNotes(
    "Nomes completos dos elos (abreviados no slide por espaço): PGJ (Ordenador de Despesas); Assessoria de Planejamento de Gestão - Controle Orçamentário; " +
    "Controladoria Interna; Coordenadoria de Licitações e Contratos (Gestão do PCA); Fiscais de Contratos; Unidades Requisitantes, conforme art. 7º, § 1º do Ato PGJ-PI nº 1381/2024."
  );
}

// ===================== SLIDE 7 — Nossas Dores =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addTitle(s, "Qual o contexto inicial?", { fontSize: 30 });
  s.addText("NOSSAS DORES", { x: MARGIN, y: 1.65, w: SLIDE_W - MARGIN * 2, h: 0.5, fontFace: TITLE_FONT, fontSize: 22, bold: true, color: RED, margin: 0 });

  const dores = [
    "Demandas pulverizadas e urgentes",
    "Dificuldade de consolidar informações",
    "Ausência de indicadores de avaliação e gestão de riscos",
    "Retrabalho nos procedimentos de contratações",
    "Pouca integração entre áreas técnicas e diretores de sede do interior",
    "Sobrecarga da coordenadoria de licitações e contratos",
    "Solução de continuidade de serviços por não renovação de contratos",
    "Falta de cronograma de licitações e renovações",
    "Ausência de cultura de planejamento integrado",
  ];
  const colW7 = (SLIDE_W - MARGIN * 2 - 0.4) / 2;
  const rowH7 = 0.84;
  dores.forEach((t, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = MARGIN + col * (colW7 + 0.4);
    const y = 2.3 + row * rowH7;
    s.addShape("roundRect", { x, y, w: colW7, h: rowH7 - 0.14, rectRadius: 0.06, fill: { color: LIGHTGREY }, line: { color: CARDGREY, width: 1 } });
    s.addShape("ellipse", { x: x + 0.18, y: y + (rowH7 - 0.14) / 2 - 0.09, w: 0.18, h: 0.18, fill: { color: RED }, line: { type: "none" } });
    s.addText(t, { x: x + 0.5, y, w: colW7 - 0.68, h: rowH7 - 0.14, valign: "middle", fontFace: BODY_FONT, fontSize: 13, color: BLACK, margin: 0, lineSpacingMultiple: 1.05 });
  });
  addLogoCorner(s);
  addFooterNum(s, 7);
}

// ===================== SLIDE 8 — Contexto Histórico-Legal =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addTitle(s, "O contexto histórico-legal", { fontSize: 30 });

  const marcos = ["Acórdão TCU\n2622/2015", "IN 05/2017", "Lei\n14.133/2021", "Ato PGJ-PI\n1108/2021", "Ato PGJ-PI\n1381/2024"];
  const n = marcos.length, boxW = 2.15, gap = (SLIDE_W - MARGIN * 2 - boxW * n) / (n - 1);
  const y = 3.4;
  // linha do tempo
  s.addShape("line", { x: MARGIN + boxW / 2, y: y - 0.35, w: SLIDE_W - MARGIN * 2 - boxW, h: 0, line: { color: CARDGREY, width: 3 } });
  marcos.forEach((t, i) => {
    const x = MARGIN + i * (boxW + gap);
    s.addShape("ellipse", { x: x + boxW / 2 - 0.14, y: y - 0.49, w: 0.28, h: 0.28, fill: { color: RED }, line: { color: WHITE, width: 2 } });
    card(s, x, y, boxW, 1.7, { fill: LIGHTGREY });
    s.addText(t, { x: x + 0.1, y: y + 0.18, w: boxW - 0.2, h: 1.35, align: "center", valign: "top", fontFace: BODY_FONT, fontSize: 15.5, bold: true, color: BLACK, margin: 0, lineSpacingMultiple: 1.1 });
  });
  addLogoCorner(s);
  addFooterNum(s, 8);
}

// ===================== SLIDE 9 — O que fizemos? =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addKicker(s, "Bloco 3 · A Virada de Chave");
  addTitle(s, "O que fizemos?", { fontSize: 28 });
  s.addText("AÇÕES PRÁTICAS", { x: MARGIN, y: 1.6, w: SLIDE_W - MARGIN * 2, h: 0.4, fontFace: BODY_FONT, fontSize: 15, color: GREY, margin: 0 });

  const acoes = [
    "Sensibilização da Alta Administração (movimento bottom-up)",
    "Criação de regulamentação interna do PCA",
    "Metodologia de construção, execução e monitoramento",
    "Definição das ferramentas utilizadas (Excel, Forms, BI)",
    "Capacitação das unidades envolvidas",
    "Padronização de formulários para captação das demandas",
    "Calendário de contratações e renovações de contratos",
    "Definição de responsáveis para gerir o PCA",
    "Acompanhamento periódico (gestão de riscos) das demandas",
  ];
  const colW = (SLIDE_W - MARGIN * 2 - 0.4) / 2;
  const rowH = 0.78;
  acoes.forEach((t, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = MARGIN + col * (colW + 0.4);
    const y = 2.3 + row * rowH;
    s.addText("✓", { x, y, w: 0.35, h: rowH - 0.08, valign: "middle", fontFace: BODY_FONT, fontSize: 16, bold: true, color: RED, margin: 0 });
    s.addText(t, { x: x + 0.35, y, w: colW - 0.35, h: rowH - 0.08, valign: "middle", fontFace: BODY_FONT, fontSize: 13, color: BLACK, margin: 0, lineSpacingMultiple: 1.05 });
  });
  addLogoCorner(s);
  addFooterNum(s, 9);

  s.addNotes(
    "Sensibilização: a mudança foi \"bottom-up\". Convencemos a gestão provando que a falta de planejamento gerava riscos jurídicos e interrupção de serviços.\n\n" +
    "Regulamentação: transformamos a Lei 14.133 em obrigação interna via atos normativos.\n\n" +
    "Metodologia: criamos um rito de como a demanda nasce, é aprovada e acompanhada.\n\n" +
    "Ferramentas: começamos com o que tínhamos (Forms, Excel, BI) para arrumar a casa antes de termos um sistema.\n\n" +
    "Capacitação/Padronização: ensinamos as áreas a planejar (fim do \"pedido para amanhã\") e forçamos o preenchimento de formulários padronizados para basear o ETP.\n\n" +
    "Calendário/Responsáveis: definimos janelas rígidas de pedido para evitar a \"corrida de final de ano\" e responsabilizamos a Chefia de Gabinete, Planejamento e Licitações pela gestão.\n\n" +
    "Acompanhamento: monitoramento ativo para corrigir atrasos antes que o recurso seja perdido."
  );
}

// ===================== SLIDE 10 — Fluxo do PCA (Macroprocesso) =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addTitle(s, "Fluxo do PCA", { fontSize: 28 });
  s.addText("MACROPROCESSO", { x: MARGIN, y: 1.6, w: SLIDE_W - MARGIN * 2, h: 0.4, fontFace: BODY_FONT, fontSize: 15, color: GREY, margin: 0 });

  const linha1 = ["Requisitante /\nDemandante", "Diretor de Sede e\nCoord. Técnicos\npreenchem", "Planejamento da\nconstrução\n(como preencher)", "Análise e\nconsolidação"];
  const linha2 = ["Submissão à Alta\nAdministração", "Aprovação", "Execução pelas\nUnid. Técnicas", "Monitoramento\n(reuniões periódicas)"];
  flowRow(s, linha1, MARGIN, 2.25, SLIDE_W - MARGIN * 2, 1.55, { startIndex: 0, labelSize: 13 });
  flowRow(s, linha2, MARGIN, 4.05, SLIDE_W - MARGIN * 2, 1.55, { startIndex: 4, labelSize: 13 });
  s.addText("Sem Comitê de Contratações formalmente instituído — a Alta Administração avalia diretamente as submissões.", {
    x: MARGIN, y: 5.75, w: SLIDE_W - MARGIN * 2, h: 0.4, align: "center", fontFace: BODY_FONT, fontSize: 12, italic: true, color: GREY, margin: 0,
  });
  addLogoCorner(s);
  addFooterNum(s, 10);

  s.addNotes(
    "Como funciona: a demanda nasce na ponta (requisitante).\n\n" +
    "O filtro: como não temos um Diretor Administrativo centralizador, a filtragem inicial fica com os Diretores de Sede e Coordenadores Técnicos. Eles validam e enviam.\n\n" +
    "O bastidor: nossa equipe técnica limpa e unifica os pedidos parecidos para ganhar economia de escala.\n\n" +
    "Aprovação: submetemos à Alta Administração. Ainda não temos um Comitê de Contratações na prática (está em minuta de regulamentação), então a gestão do PCA hoje avalia tudo. Após a aprovação do PGJ, vira lei interna.\n\n" +
    "Fim da linha: com o cronograma na mão, as equipes executam TRs de forma proativa e monitoramos tudo em reuniões periódicas."
  );
}

// ===================== SLIDE 11 — Resultados alcançados (2026) =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addKicker(s, "Bloco 4 · Resultados e Lições");
  addTitle(s, "Resultados alcançados", { fontSize: 28 });
  s.addText("2026", { x: MARGIN, y: 1.6, w: SLIDE_W - MARGIN * 2, h: 0.4, fontFace: BODY_FONT, fontSize: 15, color: GREY, margin: 0 });

  const boxW = 2.85, gap = 0.28, y = 2.35, h = 1.9;
  statBox(s, MARGIN, y, boxW, h, "529", "demandas cadastradas");
  statBox(s, MARGIN + (boxW + gap), y, boxW, h, "R$ 50,07 M", "planejados (R$ 50.070.886,53)", { fontSize: 22 });
  statBox(s, MARGIN + 2 * (boxW + gap), y, boxW, h, "100%", "participação das coordenadorias técnicas");
  statBox(s, MARGIN + 3 * (boxW + gap), y, boxW, h, "↓", "redução de demandas urgentes");

  // barra 437 novas / 93 renovações
  const barY = 4.7, barW = SLIDE_W - MARGIN * 2, barH = 0.55;
  const pctNovas = 437 / 529;
  s.addText("Composição das 529 demandas", { x: MARGIN, y: barY - 0.4, w: barW, h: 0.35, fontFace: BODY_FONT, fontSize: 14, bold: true, color: GREY, margin: 0 });
  s.addShape("rect", { x: MARGIN, y: barY, w: barW, h: barH, fill: { color: CARDGREY }, line: { type: "none" } });
  s.addShape("rect", { x: MARGIN, y: barY, w: barW * pctNovas, h: barH, fill: { color: RED }, line: { type: "none" } });
  s.addText("437 novas (83%)", { x: MARGIN + 0.15, y: barY, w: barW * pctNovas - 0.3, h: barH, valign: "middle", fontFace: BODY_FONT, fontSize: 14, bold: true, color: WHITE, margin: 0 });
  s.addText("93 renovações (17%)", { x: MARGIN + barW * pctNovas + 0.15, y: barY, w: barW * (1 - pctNovas) - 0.3, h: barH, valign: "middle", fontFace: BODY_FONT, fontSize: 13, bold: true, color: BLACK, margin: 0 });
  addLogoCorner(s);
  addFooterNum(s, 11);
}

// ===================== SLIDE 12 — Lições Aprendidas =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addTitle(s, "Lições aprendidas", { fontSize: 28 });

  const colW = 5.7, gap = 0.53, y = 2.35, h = 3.75;
  card(s, MARGIN, y, colW, h, { fill: LIGHTGREY });
  s.addText("O QUE DEU CERTO", { x: MARGIN + 0.3, y: y + 0.22, w: colW - 0.6, h: 0.4, fontFace: BODY_FONT, fontSize: 16, bold: true, color: RED, margin: 0 });
  bulletList(s, [
    "Apoio da Administração Superior",
    "Participação das áreas técnicas",
    "Capacitação dos envolvidos",
    "Reuniões periódicas",
    "Monitoramento",
    "Calendário de contratações",
    "Mudança de cultura",
  ], { x: MARGIN + 0.3, y: y + 0.78, w: colW - 0.6, h: h - 1.0, fontSize: 13.5, bulletColor: RED, spaceAfter: 6 });

  const x2 = MARGIN + colW + gap;
  card(s, x2, y, colW, h, { fill: LIGHTGREY });
  s.addText("O QUE AINDA PRECISA EVOLUIR", { x: x2 + 0.3, y: y + 0.22, w: colW - 0.6, h: 0.4, fontFace: BODY_FONT, fontSize: 16, bold: true, color: BLACK, margin: 0 });
  bulletList(s, [
    "Integração de sistemas",
    "Automatização das tarefas de execução e monitoramento",
    "Comunicação entre unidades envolvidas",
  ], { x: x2 + 0.3, y: y + 0.78, w: colW - 0.6, h: h - 1.0, fontSize: 14.5, color: BLACK, bulletColor: BLACK, spaceAfter: 10 });
  addLogoCorner(s);
  addFooterNum(s, 12);
}

// ===================== SLIDE 13 — Sistema Atual PCA-PI =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addKicker(s, "Bloco 5 · A Evolução Tecnológica");
  addTitle(s, "O sistema atual de gestão", { fontSize: 26 });
  s.addText("PCA-PI", { x: MARGIN, y: 1.55, w: SLIDE_W - MARGIN * 2, h: 0.55, fontFace: TITLE_FONT, fontSize: 26, bold: true, color: RED, margin: 0 });

  placeholderFrame(s, MARGIN, 2.3, SLIDE_W - MARGIN * 2, 3.4, "PCA-PI");
  chip(s, MARGIN, 6.0, 3.6, "Catálogo obrigatório de itens");
  chip(s, MARGIN + 3.8, 6.0, 3.4, "Fluxo de aprovação parcial");
  addLogoCorner(s);
  addFooterNum(s, 13);

  s.addNotes(
    "Toda essa metodologia que detalhamos se sustenta na prática graças ao nosso sistema atual, o PCA-PI, desenvolvido pelo nosso colega Clériston. " +
    "Ele é a nossa realidade hoje e foi o que nos tirou das planilhas. Os grandes acertos que garantem o nosso controle estão nele: a trava do catálogo obrigatório " +
    "(que padroniza os pedidos) e o fluxo de aprovação parcial (que dá agilidade para não travar o processo inteiro por erro de um único item)."
  );
}

// ===================== SLIDE 14 — Nasce o Sistema de Gestão PCA-26/27 =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addTitle(s, "Nasce o sistema de gestão do PCA", { fontSize: 24 });
  s.addText("PCA-26 E PCA-2027", { x: MARGIN, y: 1.55, w: SLIDE_W - MARGIN * 2, h: 0.5, fontFace: TITLE_FONT, fontSize: 22, bold: true, color: RED, margin: 0 });
  s.addText("OBJETIVOS", { x: MARGIN, y: 2.15, w: SLIDE_W - MARGIN * 2, h: 0.35, fontFace: BODY_FONT, fontSize: 15, color: GREY, margin: 0 });

  const objetivos = ["Centralizar informações", "Reduzir retrabalho", "Integrar áreas", "Gerar indicadores", "Acompanhar a execução", "Apoiar decisões da Administração"];
  let y = 2.6;
  const rowH = 0.7;
  objetivos.forEach((t) => {
    s.addShape("roundRect", { x: MARGIN, y, w: SLIDE_W - MARGIN * 2, h: rowH - 0.13, rectRadius: 0.06, fill: { color: LIGHTGREY }, line: { color: CARDGREY, width: 1 } });
    s.addShape("ellipse", { x: MARGIN + 0.2, y: y + (rowH - 0.13) / 2 - 0.1, w: 0.2, h: 0.2, fill: { color: RED }, line: { type: "none" } });
    s.addText(t, { x: MARGIN + 0.58, y, w: SLIDE_W - MARGIN * 2 - 0.78, h: rowH - 0.13, valign: "middle", fontFace: BODY_FONT, fontSize: 16, color: BLACK, margin: 0 });
    y += rowH;
  });
  addLogoCorner(s);
  addFooterNum(s, 14);
}

// ===================== SLIDE 15 — Novo PCA Multiexercício =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addTitle(s, "O novo PCA Multiexercício", { fontSize: 26 });
  s.addText("EM DESENVOLVIMENTO", { x: MARGIN, y: 1.55, w: SLIDE_W - MARGIN * 2, h: 0.4, fontFace: BODY_FONT, fontSize: 15, color: GREY, margin: 0 });

  placeholderFrame(s, MARGIN, 2.15, SLIDE_W - MARGIN * 2, 3.2, "Dashboards PCA Multiexercício");
  chip(s, MARGIN, 5.65, 3.5, "Modelo multiexercício");
  chip(s, MARGIN + 3.7, 5.65, 3.0, "Dashboards inteligentes");
  chip(s, MARGIN + 6.9, 5.65, 3.5, "Alertas de vencimento");
  addLogoCorner(s);
  addFooterNum(s, 15);

  s.addNotes(
    "Aqui apresento o meu projeto: como a arquitetura moderna do PCA Multiexercício vai facilitar a visão de longo prazo (histórico entre anos, não só o exercício corrente) " +
    "e reduzir ainda mais o trabalho manual através de automação — alertas de vencimento de contrato/ata, cruzamento de saldo antes de empenhar e painéis orientados a decisão."
  );
}

// ===================== SLIDE 16 — Próximos Passos =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addTitle(s, "Próximos passos", { fontSize: 30 });

  const items = [
    "Integração completa com o SEI",
    "Gestão integrada das contratações e ARP",
    "Inteligência artificial para execução automática de tarefas repetitivas",
  ];
  const cardH = 1.1, gapY = 0.32, y0 = 2.4;
  items.forEach((t, i) => {
    const y = y0 + i * (cardH + gapY);
    card(s, MARGIN, y, SLIDE_W - MARGIN * 2, cardH, { fill: LIGHTGREY });
    s.addShape("ellipse", { x: MARGIN + 0.3, y: y + cardH / 2 - 0.3, w: 0.6, h: 0.6, fill: { color: RED }, line: { type: "none" } });
    s.addText(String(i + 1), { x: MARGIN + 0.3, y: y + cardH / 2 - 0.3, w: 0.6, h: 0.6, align: "center", valign: "middle", fontFace: TITLE_FONT, fontSize: 18, bold: true, color: WHITE, margin: 0 });
    s.addText(t, { x: MARGIN + 1.15, y, w: SLIDE_W - MARGIN * 2 - 1.45, h: cardH, valign: "middle", fontFace: BODY_FONT, fontSize: 18, color: BLACK, margin: 0, lineSpacingMultiple: 1.15 });
  });
  addLogoCorner(s);
  addFooterNum(s, 16);
}

// ===================== SLIDE 17 — Demonstração: Visão do Requisitante =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addKicker(s, "Bloco 6 · Prática e Encerramento");
  addTitle(s, "Demonstração", { fontSize: 28 });
  s.addText("VISÃO DO REQUISITANTE", { x: MARGIN, y: 1.6, w: SLIDE_W - MARGIN * 2, h: 0.5, fontFace: TITLE_FONT, fontSize: 22, bold: true, color: RED, margin: 0 });

  placeholderFrame(s, MARGIN, 2.35, SLIDE_W - MARGIN * 2, 4.15, "Painel do Requisitante");
  addLogoCorner(s);
  addFooterNum(s, 17);

  s.addNotes(
    "Mostrar na prática como a unidade requisitante cadastra, preenche os campos obrigatórios e acompanha o status (pendente, aprovado) da sua própria demanda."
  );
}

// ===================== SLIDE 18 — Demonstração: Visão do Gestor =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  addTitle(s, "Demonstração", { fontSize: 28 });
  s.addText("VISÃO DO GESTOR", { x: MARGIN, y: 1.6, w: SLIDE_W - MARGIN * 2, h: 0.5, fontFace: TITLE_FONT, fontSize: 22, bold: true, color: RED, margin: 0 });

  placeholderFrame(s, MARGIN, 2.35, SLIDE_W - MARGIN * 2, 4.15, "Painel de Controle da Gestão");
  addLogoCorner(s);
  addFooterNum(s, 18);

  s.addNotes(
    "Mostrar os gráficos consolidados, como a CLCA acompanha o progresso geral e cobra quem está atrasado, garantindo o calendário."
  );
}

// ===================== SLIDE 19 — Mensagem Final =====================
{
  const s = pres.addSlide();
  addBgLight(s);
  s.addText("“", { x: SLIDE_W / 2 - 3.5, y: 1.35, w: 1.2, h: 1.4, fontFace: "Georgia", fontSize: 120, bold: true, color: RED, margin: 0 });
  s.addText("O talento vence jogos, mas o trabalho\nem equipe vence campeonatos.", {
    x: MARGIN + 0.5, y: 2.75, w: SLIDE_W - MARGIN * 2 - 1, h: 1.5, align: "center",
    fontFace: BODY_FONT, fontSize: 26, italic: true, color: BLACK, margin: 0, lineSpacingMultiple: 1.2,
  });
  s.addText("— Michael Jordan", {
    x: MARGIN, y: 4.35, w: SLIDE_W - MARGIN * 2, h: 0.5, align: "center",
    fontFace: BODY_FONT, fontSize: 17, bold: true, color: RED, margin: 0,
  });
  s.addText("Gratidão a todos!", {
    x: MARGIN, y: 5.3, w: SLIDE_W - MARGIN * 2, h: 0.5, align: "center",
    fontFace: TITLE_FONT, fontSize: 20, bold: true, color: BLACK, margin: 0,
  });
  addLogoCorner(s);
  addFooterNum(s, 19);
}

// ===================== SLIDE 20 — Encerramento / Contatos =====================
{
  const s = pres.addSlide();
  addBgRed(s);
  addLogoOnRed(s, { y: 0.6, w: 3.2 });
  s.addText("PERGUNTAS?", {
    x: MARGIN, y: 2.7, w: SLIDE_W - MARGIN * 2, h: 1.1, align: "center",
    fontFace: TITLE_FONT, fontSize: 46, bold: true, color: WHITE, margin: 0,
  });
  s.addShape("roundRect", { x: SLIDE_W / 2 - 3, y: 4.35, w: 6, h: 1.5, rectRadius: 0.1, fill: { color: WHITE, transparency: 12 }, line: { type: "none" } });
  s.addText("clca@mppi.mp.br", { x: SLIDE_W / 2 - 3, y: 4.55, w: 6, h: 0.5, align: "center", fontFace: BODY_FONT, fontSize: 20, bold: true, color: RED, margin: 0 });
  s.addText("Ramal 1234", { x: SLIDE_W / 2 - 3, y: 5.1, w: 6, h: 0.5, align: "center", fontFace: BODY_FONT, fontSize: 17, color: BLACK, margin: 0 });
  s.addText("Coordenadoria de Licitações e Contratos Administrativos — CLCA", {
    x: MARGIN, y: 6.7, w: SLIDE_W - MARGIN * 2, h: 0.4, align: "center", fontFace: BODY_FONT, fontSize: 13, italic: true, color: WHITE, margin: 0,
  });
}

pres.writeFile({ fileName: "roteiro_apresentacao_pca_mppi_cpga.pptx" }).then(() => {
  console.log("done");
});
