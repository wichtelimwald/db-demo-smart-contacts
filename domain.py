"""
domain.py - Minimale Domaenenschicht
────────────────────────────────────
Einfache Datenobjekte fuer Kontakte und Gruppen.
Keine API-Details, kein Dateizugriff.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class RelatedContact:
    id: int
    relation: Optional[str] = None


@dataclass(frozen=True)
class Group:
    id: int
    name: str


@dataclass(frozen=True)
class Contact:
    id: int
    name: str
    alias: Optional[str] = None
    species: Optional[str] = None
    organization: Optional[str] = None
    relationship: Optional[str] = None
    met_at: Optional[str] = None
    met_when: Optional[str] = None
    notes: Optional[str] = None
    known_preferences: list[str] = field(default_factory=list)
    related_to: list[RelatedContact] = field(default_factory=list)

    @property
    def organization_text(self) -> str:
        return self.organization or ""

    @property
    def species_text(self) -> str:
        return self.species or ""