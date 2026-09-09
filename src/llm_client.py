"""
llm_client.py — Abstracción de proveedor de LLM.

Permite ejecutar el mismo pipeline contra distintos modelos (OpenAI, Anthropic o uno
local vía un endpoint compatible) cambiando solo la configuración. Esto habilita el
mini-experimento de "qué modelo funciona mejor" sin tocar el código del pipeline.

Las claves se leen de variables de entorno (OPENAI_API_KEY / ANTHROPIC_API_KEY); NUNCA
se escriben en el código ni en el repositorio.

Requiere instalar el SDK correspondiente (ver requirements.txt). En un entorno sin red,
usar el proveedor 'echo' para validar el armado del pipeline sin llamar a ningún modelo.
"""
from __future__ import annotations
from dataclasses import dataclass
import os, re, time


@dataclass
class LLMConfig:
    proveedor: str = "anthropic"      # "openai" | "anthropic" | "echo" | "mock"
    modelo: str = ""                  # nombre del modelo (configurable)
    temperatura: float = 0.2
    max_tokens: int = 8000
    reintentos: int = 3
    pausa_seg: float = 2.0


class LLMClient:
    """Interfaz común. Implementaciones concretas devuelven texto plano."""
    def __init__(self, cfg: LLMConfig):
        self.cfg = cfg

    def completar(self, system: str, user: str, stage: str = "") -> str:
        raise NotImplementedError

    def _con_reintentos(self, fn):
        ultimo = None
        for i in range(self.cfg.reintentos):
            try:
                return fn()
            except Exception as e:           # noqa: BLE001
                ultimo = e
                time.sleep(self.cfg.pausa_seg * (i + 1))
        raise RuntimeError(f"LLM falló tras {self.cfg.reintentos} intentos: {ultimo}")


class OpenAIClient(LLMClient):
    def __init__(self, cfg: LLMConfig):
        super().__init__(cfg)
        from openai import OpenAI            # import diferido
        self._cli = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def completar(self, system: str, user: str, stage: str = "") -> str:
        def _call():
            r = self._cli.chat.completions.create(
                model=self.cfg.modelo,
                temperature=self.cfg.temperatura,
                max_tokens=self.cfg.max_tokens,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
            )
            return r.choices[0].message.content
        return self._con_reintentos(_call)


class AnthropicClient(LLMClient):
    def __init__(self, cfg: LLMConfig):
        super().__init__(cfg)
        import anthropic                     # import diferido
        self._cli = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self._sin_temperatura = False

    def _crear(self, system: str, user: str, con_temperatura: bool = True) -> str:
        kw = dict(model=self.cfg.modelo, max_tokens=self.cfg.max_tokens,
                  system=system, messages=[{"role": "user", "content": user}])
        if con_temperatura:
            kw["temperature"] = self.cfg.temperatura
        r = self._cli.messages.create(**kw)
        return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")

    def completar(self, system: str, user: str, stage: str = "") -> str:
        def _call():
            try:
                return self._crear(system, user, con_temperatura=not self._sin_temperatura)
            except Exception as e:             # noqa: BLE001
                # Los modelos más nuevos deprecaron 'temperature'. Se reintenta sin fijarla,
                # avisando: la reproducibilidad deja de estar garantizada por ese parámetro.
                if "temperature" in str(e).lower() and not self._sin_temperatura:
                    self._sin_temperatura = True
                    print("[anthropic] el modelo no acepta 'temperature': se continúa sin "
                          "fijarla (la reproducibilidad ya no queda garantizada por ese "
                          "parámetro; conviene reportarlo).", flush=True)
                    return self._crear(system, user, con_temperatura=False)
                raise
        return self._con_reintentos(_call)


class EchoClient(LLMClient):
    """Cliente offline para pruebas sin red: no llama a ningún modelo."""
    def completar(self, system: str, user: str, stage: str = "") -> str:
        raise RuntimeError(
            "EchoClient activo: no hay acceso a un modelo. Configurá proveedor "
            "'openai' o 'anthropic' con su API key para ejecutar el pipeline real.")


class MockClient(LLMClient):
    """Cliente offline que reproduce la corrida de referencia, sin llamar a ningún modelo.

    Sirve, etapa por etapa, el LEL ya generado que está en resultados/ (los símbolos
    reales con su tipo, noción e impacto). Permite demostrar el flujo completo sin red
    ni API key y con una salida representativa del prototipo.

    IMPORTANTE: es un resultado *pre-cargado*, no una inferencia en vivo. Al mostrarlo
    debe presentarse como tal. Para una corrida genuina hay que usar el proveedor
    'openai' o 'anthropic' con su API key.

    Si el archivo de referencia no está disponible, cae en datos sintéticos mínimos
    para no romper la validación de la orquestación.
    """
    _REF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "resultados", "lel_llm_C2c_referencia.json")
    _CICLO = ["Sujeto", "Objeto", "Verbo", "Estado"]

    def __init__(self, cfg: LLMConfig):
        super().__init__(cfg)
        self._simbolos = self._cargar_referencia()
        self._cands = [s["nombre"] for s in self._simbolos]
        self._tipos = {s["nombre"]: s.get("tipo", "") for s in self._simbolos}
        self._por_nombre = {s["nombre"]: s for s in self._simbolos}

    def _cargar_referencia(self):
        import json
        try:
            with open(self._REF, encoding="utf-8") as f:
                d = json.load(f)
            sims = d.get("simbolos", []) if isinstance(d, dict) else d
            if sims:
                return sims
        except Exception:                      # noqa: BLE001
            pass
        # Respaldo sintético: mantiene el formato correcto aunque no haya referencia.
        return [{"nombre": n, "tipo": self._CICLO[i % 4],
                 "nocion": ["(sin referencia disponible) noción."],
                 "impacto": ["(sin referencia disponible) impacto."],
                 "sinonimos": [], "id": ""}
                for i, n in enumerate(["Sistema ERP", "Pedido", "Cliente",
                                       "Factura", "Remito"])]

    def completar(self, system: str, user: str, stage: str = "") -> str:
        import json
        if stage == "extraccion":
            return json.dumps([{"nombre": s["nombre"], "sinonimos": s.get("sinonimos", [])}
                               for s in self._simbolos], ensure_ascii=False)
        if stage == "clasificacion":
            return json.dumps([{"nombre": n, "tipo": t} for n, t in self._tipos.items()],
                              ensure_ascii=False)
        if stage == "descripcion":
            # El prompt 03 lleva: Símbolo a describir: "<nombre>"
            m = re.search(r'S[íi]mbolo a describir:\s*"([^"]+)"', user)
            s = self._por_nombre.get(m.group(1)) if m else None
            if s is None:
                s = {"nocion": ["(sin referencia para este símbolo)."],
                     "impacto": ["(sin referencia para este símbolo)."]}
            return json.dumps({"nocion": s.get("nocion", []),
                               "impacto": s.get("impacto", [])}, ensure_ascii=False)
        if stage == "verificacion":
            # La referencia ya está verificada: se devuelve el lote recibido tal cual.
            # (auto_verificar envía el borrador por lotes; devolver el LEL entero en
            # cada lote duplicaría símbolos.)
            bloque = self._objeto_json(user)
            if bloque:
                try:
                    borrador = json.loads(bloque)
                    if isinstance(borrador, dict) and borrador.get("simbolos"):
                        return json.dumps(borrador, ensure_ascii=False)
                except Exception:              # noqa: BLE001
                    pass
            return json.dumps({"proyecto": "ecoFactory", "conjunto": "mock+verif",
                               "simbolos": self._simbolos}, ensure_ascii=False)
        return "[]"

    @staticmethod
    def _objeto_json(texto: str):
        """Devuelve el primer objeto JSON balanceado del texto.

        El prompt de verificación trae el borrador en JSON seguido de las
        transcripciones; cortar por la última llave tomaría texto del corpus.
        """
        ini = texto.find("{")
        if ini == -1:
            return None
        prof, en_str, esc = 0, False, False
        for i in range(ini, len(texto)):
            c = texto[i]
            if en_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    en_str = False
                continue
            if c == '"':
                en_str = True
            elif c == "{":
                prof += 1
            elif c == "}":
                prof -= 1
                if prof == 0:
                    return texto[ini:i + 1]
        return None


def get_client(cfg: LLMConfig) -> LLMClient:
    p = cfg.proveedor.lower()
    if p == "openai":
        return OpenAIClient(cfg)
    if p == "anthropic":
        return AnthropicClient(cfg)
    if p == "echo":
        return EchoClient(cfg)
    if p == "mock":
        return MockClient(cfg)
    raise ValueError(f"Proveedor desconocido: {cfg.proveedor}")
