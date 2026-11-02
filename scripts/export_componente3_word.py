#!/usr/bin/env python3
"""Exporta componente-3-avance-proyecto-integrador.md a Word (.docx)."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

BASE = Path(__file__).resolve().parents[1]
MD_PATH = BASE / "entregables" / "componente-3-avance-proyecto-integrador.md"
OUT_PATH = BASE / "entregables" / "componente-3-avance-proyecto-integrador.docx"


def set_doc_defaults(doc: Document) -> None:
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(12)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")


def add_code_block(doc: Document, lines: list[str]) -> None:
    p = doc.add_paragraph()
    run = p.add_run("\n".join(lines))
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)


def parse_table_row(line: str) -> list[str]:
    parts = [c.strip() for c in line.strip().strip("|").split("|")]
    return parts


def is_table_separator(line: str) -> bool:
    return bool(re.match(r"^\|?[\s\-:|]+\|?$", line.strip()))


def add_table(doc: Document, rows: list[list[str]]) -> None:
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.style = "Table Grid"
    for i, row in enumerate(rows):
        for j in range(ncols):
            cell_text = row[j] if j < len(row) else ""
            cell_text = re.sub(r"\*\*(.+?)\*\*", r"\1", cell_text)
            cell_text = cell_text.replace("`", "")
            table.rows[i].cells[j].text = cell_text
            if i == 0:
                for paragraph in table.rows[i].cells[j].paragraphs:
                    for run in paragraph.runs:
                        run.bold = True
    doc.add_paragraph()


def add_rich_paragraph(doc: Document, text: str, style: str | None = None) -> None:
    text = text.strip()
    if not text:
        return
    p = doc.add_paragraph(style=style)
    parts = re.split(r"(\*\*.+?\*\*|`[^`]+`)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = p.add_run(part[2:-2])
            run.bold = True
        elif part.startswith("`") and part.endswith("`"):
            run = p.add_run(part[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(10)
        else:
            p.add_run(part)


def convert_md_to_docx(md_path: Path, out_path: Path) -> None:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    doc = Document()

    # Portada
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run("Componente 3. Avance del proyecto integrador")
    r.bold = True
    r.font.size = Pt(16)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.add_run("Ingeniería de Datos — Taller Primer Corte (Semana 3)")

    team = doc.add_paragraph()
    team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    team.add_run(
        "\nDaniel Alejandro Monroy\nKevin Sebastian Soto\nSamuel Eduardo Preciado"
    )

    doc.add_page_break()
    set_doc_defaults(doc)

    i = 0
    table_buffer: list[list[str]] = []
    code_buffer: list[str] | None = None
    skip_until = 0

    while i < len(lines):
        line = lines[i]

        if i < skip_until:
            i += 1
            continue

        # Skip mermaid blocks — replace with note
        if line.strip().startswith("```mermaid"):
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            add_rich_paragraph(
                doc,
                "[Figura: diagrama de arquitectura / modelo — ver versión Markdown del repositorio "
                "o insertar captura exportada desde el diagrama del informe.]",
            )
            skip_until = j + 1
            i += 1
            continue

        if line.strip().startswith("```"):
            if code_buffer is None:
                code_buffer = []
            else:
                add_code_block(doc, code_buffer)
                code_buffer = None
            i += 1
            continue

        if code_buffer is not None:
            code_buffer.append(line)
            i += 1
            continue

        if line.strip().startswith("|"):
            if is_table_separator(line):
                i += 1
                continue
            table_buffer.append(parse_table_row(line))
            i += 1
            continue

        if table_buffer:
            add_table(doc, table_buffer)
            table_buffer = []

        if line.startswith("# "):
            doc.add_heading(line[2:].strip(), level=1)
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), level=2)
        elif line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=3)
        elif line.startswith("> "):
            add_rich_paragraph(doc, line[2:], style="Intense Quote")
        elif line.strip() == "---":
            doc.add_paragraph()
        elif re.match(r"^\d+\.\s", line.strip()):
            add_rich_paragraph(doc, line.strip(), style="List Number")
        elif line.strip().startswith("- "):
            add_rich_paragraph(doc, line.strip()[2:], style="List Bullet")
        elif line.strip():
            add_rich_paragraph(doc, line)

        i += 1

    if table_buffer:
        add_table(doc, table_buffer)
    if code_buffer:
        add_code_block(doc, code_buffer)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)
    print(f"Word generado: {out_path}")


if __name__ == "__main__":
    convert_md_to_docx(MD_PATH, OUT_PATH)
