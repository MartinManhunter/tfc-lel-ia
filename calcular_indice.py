"""
calcular_indice.py — Calcula los números de página del índice a partir del PDF ya
renderizado y los guarda en toc_pages.json, que build_docx.js usa en la siguiente corrida.

Procedimiento (dos pasadas):
  1. node build_docx.js            -> índice con marcadores "00"
  2. (convertir a PDF)
  3. python calcular_indice.py     -> escribe toc_pages.json
  4. node build_docx.js            -> índice con los números reales

Como la cantidad de entradas del índice no cambia entre pasadas, su extensión en
páginas se mantiene y los números calculados siguen siendo válidos.
"""
import json, os, re, subprocess, sys, unicodedata, zipfile

DIR = os.path.dirname(os.path.abspath(__file__))
DOCX = os.path.join(DIR, "Tesis_TFC_Romano.docx")
PDF = os.path.join(DIR, "Tesis_TFC_Romano.pdf")
SALIDA = os.path.join(DIR, "toc_pages.json")


def normalizar(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.replace("\u2014", "-").replace("\u2013", "-").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def encabezados_del_docx(path):
    z = zipfile.ZipFile(path)
    doc = z.read("word/document.xml").decode("utf-8")
    heads = []
    for p in re.findall(r"<w:p\b.*?</w:p>", doc, re.DOTALL):
        m = re.search(r'<w:pStyle w:val="(Heading[123])"/>', p)
        if not m:
            continue
        txt = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)).strip()
        if txt:
            heads.append((int(m.group(1)[-1]), txt))
    return heads


def texto_por_pagina(pdf):
    n = int(re.search(r"Pages:\s+(\d+)",
        subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    paginas = []
    for i in range(1, n + 1):
        out = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), pdf, "-"],
                             capture_output=True, text=True).stdout
        paginas.append(normalizar(out))
    return paginas


def paginas_del_indice(paginas):
    """Detecta las páginas ocupadas por el índice: tienen muchos guiones de puntos."""
    return {i for i, pg in enumerate(paginas) if pg.count("....") > 10}


def main():
    heads = encabezados_del_docx(DOCX)
    # El índice no se lista a sí mismo
    entradas = [(l, t) for l, t in heads if normalizar(t) != "índice"]
    paginas = texto_por_pagina(PDF)

    # Las páginas del índice contienen todos los títulos: hay que excluirlas de la búsqueda
    saltar = paginas_del_indice(paginas)
    buscables = [i for i in range(len(paginas)) if i not in saltar]
    print(f"Páginas del índice excluidas de la búsqueda: {sorted(p+1 for p in saltar)}")

    numeros, faltantes = [], []
    pos = 0   # posición dentro de 'buscables'
    for lvl, texto in entradas:
        clave = normalizar(texto)
        encontrada = None
        for k in range(pos, len(buscables)):
            if clave in paginas[buscables[k]]:
                encontrada = buscables[k] + 1
                pos = k
                break
        if encontrada is None:   # reintentar desde el principio
            for k, i in enumerate(buscables):
                if clave in paginas[i]:
                    encontrada = i + 1
                    pos = k
                    break
        if encontrada is None:
            faltantes.append(texto)
            encontrada = numeros[-1] if numeros else 1
        numeros.append(encontrada)

    json.dump(numeros, open(SALIDA, "w", encoding="utf-8"))
    print(f"Entradas: {len(entradas)} -> {SALIDA}")
    if faltantes:
        print(f"No ubicadas en el PDF ({len(faltantes)}), se usó la página previa:")
        for f in faltantes[:10]:
            print("   -", f)
    else:
        print("Todas las entradas ubicadas correctamente.")
    # Sanity check: los números deben ser no decrecientes
    if numeros != sorted(numeros):
        print("AVISO: hay números de página fuera de orden, revisar.")
        sys.exit(1)


if __name__ == "__main__":
    main()
