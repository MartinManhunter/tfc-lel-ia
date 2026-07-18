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
import os, time


@dataclass
class LLMConfig:
    proveedor: str = "anthropic"      # "openai" | "anthropic" | "echo" | "mock"
    modelo: str = ""                  # nombre del modelo (configurable)
    temperatura: float = 0.2
    max_tokens: int = 4000
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

    def completar(self, system: str, user: str, stage: str = "") -> str:
        def _call():
            r = self._cli.messages.create(
                model=self.cfg.modelo,
                temperature=self.cfg.temperatura,
                max_tokens=self.cfg.max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
        return self._con_reintentos(_call)


class EchoClient(LLMClient):
    """Cliente offline para pruebas sin red: no llama a ningún modelo."""
    def completar(self, system: str, user: str, stage: str = "") -> str:
        raise RuntimeError(
            "EchoClient activo: no hay acceso a un modelo. Configurá proveedor "
            "'openai' o 'anthropic' con su API key para ejecutar el pipeline real.")


class MockClient(LLMClient):
    """Cliente simulado: devuelve JSON con el formato correcto de cada etapa.
    No produce un LEL real, pero valida de punta a punta la orquestación, el relleno
    de prompts, el parseo de JSON y el esquema, sin red ni API."""
    _CICLO = ["Sujeto", "Objeto", "Verbo", "Estado"]

    def __init__(self, cfg: LLMConfig):
        super().__init__(cfg)
        self._cands = []
        self._tipos = {}

    def completar(self, system: str, user: str, stage: str = "") -> str:
        import json
        if stage == "extraccion":
            self._cands = ["Sistema ERP", "Pedido", "Cliente", "Agregar Pedido", "Pedido Aprobado"]
            return json.dumps([{"nombre": n, "sinonimos": []} for n in self._cands], ensure_ascii=False)
        if stage == "clasificacion":
            self._tipos = {n: self._CICLO[i % 4] for i, n in enumerate(self._cands)}
            return json.dumps([{"nombre": n, "tipo": t} for n, t in self._tipos.items()], ensure_ascii=False)
        if stage == "descripcion":
            return json.dumps({"nocion": ["(simulado) descripción de la noción."],
                               "impacto": ["(simulado) descripción del impacto."]}, ensure_ascii=False)
        if stage == "verificacion":
            sim = [{"nombre": n, "tipo": t, "nocion": ["(simulado) noción"],
                    "impacto": ["(simulado) impacto"], "sinonimos": [], "id": ""}
                   for n, t in self._tipos.items()]
            return json.dumps({"proyecto": "ecoFactory", "conjunto": "mock+verif", "simbolos": sim}, ensure_ascii=False)
        return "[]"


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
