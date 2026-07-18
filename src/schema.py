"""
schema.py — Estructura de datos del LEL y utilidades de normalización.

Define un esquema único para representar un LEL, usado tanto por el Gold Standard
como por las salidas de los métodos automáticos (LLM y baselines de PLN). Tener un
único esquema es lo que permite que el motor de evaluación compare cualquier salida
contra la verdad de referencia.

Formato JSON de un LEL:
{
  "proyecto": "ecoFactory",
  "simbolos": [
    {"id": "S06", "nombre": "Sistema ERP", "sinonimos": [],
     "tipo": "Sujeto", "nocion": ["..."], "impacto": ["...", "..."]}
  ]
}
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List
import json, re, unicodedata

TIPOS = ("Sujeto", "Objeto", "Verbo", "Estado")

# Stopwords y rasgos lingüísticos mínimos (sin dependencias externas).
STOPWORDS = {
    # artículos, preposiciones, conjunciones, determinantes
    "el","la","los","las","un","una","unos","unas","lo","al","del","de","a","ante",
    "con","contra","desde","en","entre","hacia","hasta","para","por","segun","según",
    "sin","sobre","tras","y","e","o","u","que","qué","como","cómo","cuando","cuándo",
    "donde","dónde","quien","quién","cual","cuál","cuales","cuáles","si","sí","no",
    "su","sus","mi","mis","tu","tus","nuestro","nuestra","esta","este","esto","estos",
    "estas","ese","esa","eso","esos","esas","aquel","aquella","cada","otro","otra",
    "otros","otras","mismo","misma","todo","toda","todos","todas","alguno","alguna",
    "algunos","algunas","ningun","ningún","ninguna","poco","poca","pocos","pocas",
    "mucho","mucha","muchos","muchas","tanto","tanta","demasiado",
    # pronombres y adverbios
    "yo","tu","vos","el","ella","nosotros","ustedes","ellos","ellas","me","te","se",
    "nos","le","les","mas","más","menos","muy","ya","tambien","también","pero","porque",
    "pues","entonces","ahi","ahí","aca","acá","alla","allá","aqui","aquí","bien","mal",
    "ahora","antes","despues","después","siempre","nunca","casi","solo","sólo","asi",
    "así","bastante","bueno","buena","digamos","perfecto","claro","mira","etc","quizas",
    "quizás","tal","cual","algo","nada","alguien","cosa","cosas","tipo","parte","vez",
    "veces","manera","forma","punto","gente","lado","modo","caso","día","dia","dias",
    "días","idea","uno","dos","tres","x",
    # verbos de altísima frecuencia (auxiliares/soporte) y sus conjugaciones comunes
    "ser","es","son","era","eran","fue","fueron","sera","será","sea","sido","siendo","soy","eres","somos",
    "estar","esta","está","estan","están","estoy","estamos","estaba","estaban","estuvo","estar","este","esté",
    "haber","hay","ha","han","he","hemos","habia","había","habian","habían","hubo","habra","habrá",
    "tener","tengo","tiene","tienen","tenemos","tenia","tenía","tenian","tenían","tuvo","tendra","tendrá","tienes",
    "poder","puedo","puede","pueden","podemos","podia","podía","pudo","podra","podrá","podria","podría",
    "hacer","hago","hace","hacen","hacemos","hacia","hacía","hizo","hara","hará","haria","haría","haciendo","hecho",
    "ir","voy","va","van","vamos","iba","iban","fui","ido","yendo",
    "ver","veo","ve","ven","vemos","veia","veía","vio","visto","viendo",
    "decir","digo","dice","dicen","decimos","dijo","dicho","diciendo",
    "querer","quiero","quiere","quieren","queremos","queria","quería","quiso","querer","querran","querrán","querría",
    "dar","doy","da","dan","damos","dio","dado","dando","saber","se","sabe","saben","sabemos","sabia","sabía",
}


def quitar_acentos(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def normalizar(nombre: str) -> str:
    """Forma canónica para comparar nombres: minúsculas, sin acentos ni puntuación."""
    s = quitar_acentos(nombre.lower())
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def tokens_significativos(nombre: str) -> set:
    """Tokens del nombre sin stopwords (para emparejamiento por solapamiento)."""
    return {t for t in normalizar(nombre).split() if t not in STOPWORDS and len(t) > 1}


@dataclass
class Simbolo:
    nombre: str
    tipo: str = ""                       # Sujeto | Objeto | Verbo | Estado | ""
    nocion: List[str] = field(default_factory=list)
    impacto: List[str] = field(default_factory=list)
    sinonimos: List[str] = field(default_factory=list)
    id: str = ""

    def nombres(self) -> List[str]:
        base = [self.nombre] + list(self.sinonimos)
        return [n for n in base if n]


@dataclass
class LEL:
    proyecto: str = ""
    simbolos: List[Simbolo] = field(default_factory=list)
    conjunto: str = ""
    version: str = ""

    # --- serialización ---
    @classmethod
    def from_dict(cls, d: dict) -> "LEL":
        sims = [Simbolo(
            nombre=s.get("nombre", ""), tipo=s.get("tipo", ""),
            nocion=s.get("nocion", []) or [], impacto=s.get("impacto", []) or [],
            sinonimos=s.get("sinonimos", []) or [], id=s.get("id", ""),
        ) for s in d.get("simbolos", [])]
        return cls(proyecto=d.get("proyecto", ""), simbolos=sims,
                   conjunto=d.get("conjunto", ""), version=d.get("version", ""))

    def to_dict(self) -> dict:
        return {"proyecto": self.proyecto, "version": self.version,
                "conjunto": self.conjunto,
                "simbolos": [asdict(s) for s in self.simbolos]}

    @classmethod
    def load(cls, path: str) -> "LEL":
        with open(path, encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    def conteo_por_tipo(self) -> dict:
        c = {t: 0 for t in TIPOS}
        for s in self.simbolos:
            if s.tipo in c:
                c[s.tipo] += 1
        return c
