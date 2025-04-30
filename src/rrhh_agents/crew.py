from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# 🔥 IMPORTAMOS LAS TOOLS
from rrhh_agents.tools.custom_tool import LeerCandidatosGoogleSheetsTool, BuscarOfertaLaboralTool, AnalizarOfertaManualTool


@CrewBase
class RrhhAgents():
    """Crew de agentes de Recursos Humanos"""

    @tool
    def leer_candidatos_google_sheets_tool(self):
        return LeerCandidatosGoogleSheetsTool()
    
    @tool
    def buscar_oferta_laboral_tool(self):
        return BuscarOfertaLaboralTool()
    
    @tool
    def analizar_oferta_manual_tool(self):
        return AnalizarOfertaManualTool()


    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def analizador_cvs(self) -> Agent:
        return Agent(
            config=self.agents_config['analizador_cvs'],
            verbose=True
        )

    @agent
    def analizador_candidatos(self) -> Agent:
        return Agent(
            config=self.agents_config['analizador_candidatos'],
            verbose=True
        )

    @agent
    def selector_talentos(self) -> Agent:
        return Agent(
            config=self.agents_config['selector_talentos'],
            verbose=True
        )

    @task
    def analizar_cvs_task(self) -> Task:
        return Task(
            config=self.tasks_config['analizar_cvs_task'],
        )

    @task
    def analizar_candidatos_task(self) -> Task:
        return Task(
            config=self.tasks_config['analizar_candidatos_task'],
        )

    @task
    def seleccionar_talentos_task(self) -> Task:
        return Task(
            config=self.tasks_config['seleccionar_talentos_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
