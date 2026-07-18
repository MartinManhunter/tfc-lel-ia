"""Ejecuta el baseline spaCy y guarda el LEL producido. Requiere es_core_news_md."""
import os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
from baseline_spacy import construir

CORPUS = [os.path.join(RAIZ, "data/corpus/entrevista_1_dueno.txt"),
          os.path.join(RAIZ, "data/corpus/entrevista_4_operario.txt")]

if __name__ == "__main__":
    lel = construir(CORPUS)
    salida = os.path.join(RAIZ, "resultados/lel_baseline_spacy.json")
    lel.save(salida)
    print(f"{len(lel.simbolos)} candidatos -> {salida}")
