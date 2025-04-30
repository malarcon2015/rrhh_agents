from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import gspread
import json
from crewai_tools import SerperDevTool

# Tool 1: Google Sheets
class GoogleSheetsToolInput(BaseModel):
    sheet_url: str = Field(..., description="URL del Google Sheet con los candidatos")

class LeerCandidatosGoogleSheetsTool(BaseTool):
    name: str = "leer_candidatos_google_sheets_tool"
    description: str = "Lee datos de candidatos desde una hoja de Google Sheets y devuelve una lista JSON"
    args_schema: Type[BaseModel] = GoogleSheetsToolInput

    def _run(self, sheet_url: str) -> str:
        try:
            gc = gspread.service_account(filename="credentials.json")
            sh = gc.open_by_url(sheet_url)
            worksheet = sh.get_worksheet(0)
            records = worksheet.get_all_records()
            return json.dumps(records, indent=2)
        except Exception as e:
            return f"Error accediendo al Google Sheet: {e}"

# Tool 2: Buscar oferta laboral en Google con Serper.dev
class LinkedInOfferSearchInput(BaseModel):
    query: str = Field(..., description="URL de una búsqueda de empleos en LinkedIn")

class BuscarOfertaLaboralTool(BaseTool):
    name: str = "buscar_oferta_laboral_tool"
    description: str = "Lee resultados de una búsqueda de empleos desde una URL"
    args_schema: Type[BaseModel] = LinkedInOfferSearchInput

    def _run(self, query: str) -> str:
        try:
            # ✅ Debe llamarse search_query para el ._run()
            return SerperDevTool()._run(search_query=query)
        except Exception as e:
            return f"Error usando Serper.dev: {e}"


class OfertaManualInput(BaseModel):
    oferta: str = Field(..., description="Texto completo de la oferta laboral redactada manualmente")

class AnalizarOfertaManualTool(BaseTool):
    name: str = "analizar_oferta_manual_tool"
    description: str = "Recibe una oferta laboral redactada manualmente para que el agente pueda compararla con los candidatos"
    args_schema: Type[BaseModel] = OfertaManualInput

    def _run(self, oferta: str) -> str:
        return oferta  # El LLM analizará el contenido en el siguiente paso

# 🔁 REGISTRO CORRECTO PARA CREWAI <= 0.117
#tool_functions = {
#    "leer_candidatos_google_sheets_tool": LeerCandidatosGoogleSheetsTool(),
#    "buscar_oferta_laboral_tool": BuscarOfertaLaboralTool()
#}
