#!/usr/bin/env python3
"""Markdown → A4 PDF with the Poly navy spec layout (header/footer bars, DejaVu, zebra tables)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import markdown
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

NAVY = colors.HexColor("#1a365d")
TEAL = colors.HexColor("#2b6cb0")
HEADER_BG = colors.HexColor("#1a365d")
ROW_ALT = colors.HexColor("#edf2f7")
RULE = colors.HexColor("#cbd5e0")
BODY = colors.HexColor("#1a202c")
MUTED = colors.HexColor("#4a5568")
GRID = colors.HexColor("#a0aec0")

FONT_DIRS = (
    Path("/usr/share/fonts/truetype/dejavu"),
    Path("/usr/share/fonts/truetype/DejaVu"),
    Path("/usr/local/share/fonts"),
    Path.home() / ".local/share/fonts",
)


def find_font_dir() -> Path:
    for directory in FONT_DIRS:
        if (directory / "DejaVuSans.ttf").is_file():
            return directory
    sys.stderr.write(
        "DejaVuSans.ttf não encontrado. Instale fonts-dejavu-core "
        "(ex.: sudo apt install fonts-dejavu-core).\n"
    )
    sys.exit(1)


def register_fonts() -> None:
    font_dir = find_font_dir()
    pdfmetrics.registerFont(TTFont("DejaVu", str(font_dir / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(font_dir / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Mono", str(font_dir / "DejaVuSansMono.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Mono-Bold", str(font_dir / "DejaVuSansMono-Bold.ttf")))
    pdfmetrics.registerFontFamily(
        "DejaVu",
        normal="DejaVu",
        bold="DejaVu-Bold",
        italic="DejaVu",
        boldItalic="DejaVu-Bold",
    )


def styles(cover_size: float = 16) -> dict:
    sample = getSampleStyleSheet()
    sample.add(
        ParagraphStyle(
            "CoverTitle",
            fontName="DejaVu-Bold",
            fontSize=cover_size,
            leading=cover_size + 4,
            textColor=NAVY,
            spaceAfter=8,
            alignment=TA_LEFT,
        )
    )
    sample.add(
        ParagraphStyle(
            "Meta",
            fontName="DejaVu",
            fontSize=9,
            leading=13,
            textColor=MUTED,
            spaceAfter=4,
        )
    )
    sample.add(
        ParagraphStyle(
            "Lead",
            fontName="DejaVu",
            fontSize=10.5,
            leading=15,
            textColor=BODY,
            spaceBefore=6,
            spaceAfter=10,
            alignment=TA_JUSTIFY,
        )
    )
    sample.add(
        ParagraphStyle(
            "H2",
            fontName="DejaVu-Bold",
            fontSize=13,
            leading=17,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=6,
        )
    )
    sample.add(
        ParagraphStyle(
            "H3",
            fontName="DejaVu-Bold",
            fontSize=11,
            leading=15,
            textColor=TEAL,
            spaceBefore=10,
            spaceAfter=4,
        )
    )
    sample.add(
        ParagraphStyle(
            "Body",
            fontName="DejaVu",
            fontSize=9.5,
            leading=13.5,
            textColor=BODY,
            spaceBefore=2,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
        )
    )
    sample.add(
        ParagraphStyle(
            "Li",
            fontName="DejaVu",
            fontSize=9.5,
            leading=13.5,
            textColor=BODY,
            leftIndent=0,
        )
    )
    sample.add(
        ParagraphStyle(
            "Cell",
            fontName="DejaVu",
            fontSize=7.5,
            leading=10.5,
            textColor=BODY,
        )
    )
    sample.add(
        ParagraphStyle(
            "CellHead",
            fontName="DejaVu-Bold",
            fontSize=7.5,
            leading=10.5,
            textColor=colors.white,
        )
    )
    sample.add(
        ParagraphStyle(
            "Footer",
            fontName="DejaVu",
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    sample.add(
        ParagraphStyle(
            "CodeBlock",
            fontName="DejaVu-Mono",
            fontSize=7.5,
            leading=10,
            textColor=BODY,
            backColor=ROW_ALT,
            leftIndent=4,
            rightIndent=4,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    return sample


class MdHtmlParser(HTMLParser):
    def __init__(self, sty, skip_handoff: bool = True):
        super().__init__(convert_charrefs=True)
        self.sty = sty
        self.skip_handoff = skip_handoff
        self.story = []
        self._buf = []
        self._list_items = []
        self._list_ordered = False
        self._table_rows = []
        self._row = []
        self._in_header_cell = False
        self._in_pre = False

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "p", "li", "th", "td"):
            self._buf = []
            self._in_header_cell = tag == "th"
        elif tag == "pre":
            self._in_pre = True
            self._buf = []
        elif tag == "strong":
            self._buf.append("<b>")
        elif tag == "em":
            self._buf.append("<i>")
        elif tag == "code":
            if not self._in_pre:
                self._buf.append('<font name="DejaVu-Mono" size="8.5" color="#2d3748">')
        elif tag == "ul":
            self._list_items = []
            self._list_ordered = False
        elif tag == "ol":
            self._list_items = []
            self._list_ordered = True
        elif tag == "table":
            self._table_rows = []
        elif tag == "tr":
            self._row = []
        elif tag == "hr":
            self.story.append(Spacer(1, 2 * mm))
            self.story.append(
                HRFlowable(width="100%", thickness=0.4, color=RULE, spaceBefore=1, spaceAfter=1)
            )
            self.story.append(Spacer(1, 2 * mm))
        elif tag == "br":
            self._buf.append("<br/>")

    def handle_endtag(self, tag):
        if tag == "strong":
            self._buf.append("</b>")
        elif tag == "em":
            self._buf.append("</i>")
        elif tag == "code":
            if not self._in_pre:
                self._buf.append("</font>")
        elif tag == "pre":
            raw = "".join(self._buf).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
            self._buf = []
            self._in_pre = False
            text = raw.strip("\n")
            if text:
                self.story.append(Preformatted(text, self.sty["CodeBlock"]))
        elif tag == "h1":
            self.story.append(Paragraph(self._flush(), self.sty["CoverTitle"]))
        elif tag == "h2":
            self.story.append(Paragraph(self._flush(), self.sty["H2"]))
        elif tag == "h3":
            self.story.append(Paragraph(self._flush(), self.sty["H3"]))
        elif tag == "p":
            text = self._flush()
            if not text:
                return
            if self.skip_handoff and "handoff" in text.lower():
                return
            style = self.sty["Meta"] if self._looks_like_meta(text) else self.sty["Body"]
            if len(self.story) == 1:
                style = self.sty["Lead"]
            self.story.append(Paragraph(text, style))
        elif tag == "li":
            body = self._flush()
            n = len(self._list_items) + 1
            prefix = f"{n}. " if self._list_ordered else "• "
            self._list_items.append(Paragraph(prefix + body, self.sty["Li"]))
        elif tag in ("ul", "ol"):
            for item in self._list_items:
                item.style.leftIndent = 12
                item.style.spaceBefore = 1
                item.style.spaceAfter = 2
                self.story.append(item)
            if self._list_items:
                self.story.append(Spacer(1, 3 * mm))
            self._list_items = []
        elif tag in ("td", "th"):
            style = self.sty["CellHead"] if self._in_header_cell else self.sty["Cell"]
            self._row.append(Paragraph(self._flush() or "&nbsp;", style))
        elif tag == "tr":
            if self._row:
                self._table_rows.append(self._row)
            self._row = []
        elif tag == "table":
            self._emit_table()

    def handle_data(self, data):
        if not data:
            return
        if self._in_pre:
            self._buf.append(data)
        else:
            self._buf.append(self._escape(data))

    def _flush(self):
        text = "".join(self._buf).strip()
        self._buf = []
        return text

    @staticmethod
    def _escape(text):
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    @staticmethod
    def _looks_like_meta(text):
        plain = text.replace("<b>", "").replace("</b>", "")
        return (
            plain.startswith("Criado em:")
            or plain.startswith("Última atualização:")
            or plain.startswith("Versão:")
        )

    def _emit_table(self):
        if not self._table_rows:
            return
        n_cols = max(len(r) for r in self._table_rows)
        rows = [r + [Paragraph("&nbsp;", self.sty["Cell"])] * (n_cols - len(r)) for r in self._table_rows]
        usable = 170 * mm
        first = getattr(rows[0][0], "text", "") or ""
        if n_cols == 4:
            if "Método" in first:
                col_widths = [18 * mm, 58 * mm, 16 * mm, 78 * mm]
            elif first.strip() == "#":
                col_widths = [10 * mm, 78 * mm, 16 * mm, 66 * mm]
            else:
                col_widths = [usable / n_cols] * n_cols
        elif n_cols == 3 and "Método" in first:
            col_widths = [18 * mm, 62 * mm, 90 * mm]
        else:
            col_widths = [usable / n_cols] * n_cols

        table = Table(rows, colWidths=col_widths, repeatRows=1)
        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "DejaVu"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.3, GRID),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ]
        for i in range(1, len(rows)):
            if i % 2 == 0:
                style_cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
        table.setStyle(TableStyle(style_cmds))
        self.story.append(Spacer(1, 2 * mm))
        self.story.append(table)
        self.story.append(Spacer(1, 3 * mm))


def add_header_footer(canvas, doc, header_title: str, version: str) -> None:
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 12 * mm, A4[0], 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("DejaVu", 8)
    version_label = f"v{version}" if version else ""
    right_w = canvas.stringWidth(version_label, "DejaVu", 8) if version_label else 0
    max_w = A4[0] - 36 * mm - right_w - (4 * mm if version_label else 0)
    label = header_title
    if canvas.stringWidth(label, "DejaVu", 8) > max_w:
        while label and canvas.stringWidth(label + "…", "DejaVu", 8) > max_w:
            label = label[:-1]
        label = label + "…"
    canvas.drawString(18 * mm, A4[1] - 8 * mm, label)
    if version_label:
        canvas.drawRightString(A4[0] - 18 * mm, A4[1] - 8 * mm, version_label)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("DejaVu", 8)
    canvas.drawCentredString(A4[0] / 2, 4 * mm, f"Página {doc.page}")
    canvas.restoreState()


def extract_h1(md: str) -> str:
    match = re.search(r"^#\s+(.+)$", md, re.M)
    return match.group(1).strip() if match else ""


def extract_version(md: str) -> str:
    match = re.search(r"\*\*Versão:\*\*\s*([0-9.]+)", md)
    if match:
        return match.group(1)
    match = re.search(r"^Versão:\s*([0-9.]+)", md, re.M)
    return match.group(1) if match else ""


def default_header(author: str, title: str) -> str:
    shortened = title.replace(" — ", " · ", 1) if title else ""
    if not shortened:
        return author
    return f"{author} — {shortened}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Converte Markdown para PDF no layout Poly (faixa navy, DejaVu, tabelas zebradas)."
    )
    parser.add_argument("input", type=Path, help="Arquivo .md de origem")
    parser.add_argument("output", type=Path, nargs="?", help="Arquivo .pdf de destino (default: mesmo nome ao lado do .md)")
    parser.add_argument("--title", help="Título do PDF (metadata). Default: H1 do Markdown")
    parser.add_argument("--header", help="Texto da faixa superior. Default: '{author} — {título}'")
    parser.add_argument("--subject", help="Subject do PDF")
    parser.add_argument("--author", default="Poly", help="Autor / marca da faixa (default: Poly)")
    parser.add_argument("--version", help="Versão na faixa (default: campo **Versão:** do Markdown)")
    parser.add_argument(
        "--keep-handoff",
        action="store_true",
        help="Inclui parágrafos que mencionam handoff (por padrão são omitidos)",
    )
    return parser.parse_args(argv)


def build_pdf(args: argparse.Namespace) -> dict:
    src = args.input.expanduser().resolve()
    if not src.is_file():
        sys.stderr.write(f"arquivo não encontrado: {src}\n")
        sys.exit(1)

    dest = (args.output.expanduser().resolve() if args.output else src.with_suffix(".pdf"))
    dest.parent.mkdir(parents=True, exist_ok=True)

    md = src.read_text(encoding="utf-8")
    title = args.title or extract_h1(md) or src.stem
    version = args.version if args.version is not None else extract_version(md)
    header_title = args.header or default_header(args.author, title)
    subject = args.subject or title
    cover_size = 14 if len(title) > 70 else 16

    register_fonts()
    html = markdown.markdown(md, extensions=["tables", "sane_lists", "nl2br", "fenced_code"])
    sty = styles(cover_size)
    parser = MdHtmlParser(sty, skip_handoff=not args.keep_handoff)
    parser.feed(html)
    while parser.story and isinstance(parser.story[-1], Spacer):
        parser.story.pop()

    doc = SimpleDocTemplate(
        str(dest),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title=title,
        author=args.author,
        subject=subject,
    )

    def _hf(canvas, doc_):
        add_header_footer(canvas, doc_, header_title, version)

    doc.build(parser.story, onFirstPage=_hf, onLaterPages=_hf)
    return {
        "output": str(dest),
        "pages": doc.page,
        "title": title,
        "header": header_title,
        "version": version,
    }


def main() -> None:
    result = build_pdf(parse_args())
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
