from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field



class Categorie(str, Enum):
    BUGET = "Buget"
    ECONOMII = "Economii"
    CREDITE = "Credite"
    INVESTITII = "Investitii"
    PENSIE = "Pensie"
    ALTELE = "Altele"

class LectieIn(BaseModel):
    titlu: str = Field(min_length=3, max_length=200)
    categorie: Categorie
    continut: str = Field(min_length=50)

class MesajChat(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatIn(BaseModel):
    mesaj: str
    istoric: list[MesajChat] = []


class ApelTool(BaseModel):
    tool: str
    rezultat: str


class ChatOut(BaseModel):
    raspuns: str
    apeluri: list[BaseModel]
