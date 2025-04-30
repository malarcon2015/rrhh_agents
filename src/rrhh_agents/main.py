#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from dotenv import load_dotenv
from rrhh_agents.crew import RrhhAgents

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Cargamos .env para obtener SERPER_API_KEY
load_dotenv()

def run():
    """
    Run the crew.
    """
    # Inputs que tu proyecto realmente necesita
    sheet_url = "https://docs.google.com/spreadsheets/d/1fbcQRmT1hd-8G_3MOMrb2MW_nqPgb11zXCJSvNXcT2Y/edit?usp=sharing"#input("🔗 Ingrese la URL del Google Sheet con candidatos: ")
    #query = input("🔗 Ingrese la URL de la búsqueda de emple: ")
    oferta_manual = input("📄 Ingrese la oferta laboral redactada (puede pegarla aquí): ")

    inputs = {
        'sheet_url': sheet_url,
        'oferta_manual': oferta_manual,
        'current_year': str(datetime.now().year)
    }
    #inputs = {
    #    'sheet_url': sheet_url,
    #    'query': query,
    #    'current_year': str(datetime.now().year)  # Puedes dejarlo si quieres, aunque no lo uses
    #}
    
    try:
        result = RrhhAgents().crew().kickoff(inputs=inputs)
        print("\n✅ Resultado Final:\n")
        print(result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    sheet_url = input("🔗 Ingrese la URL del Google Sheet con candidatos: ")
    query = input("🔍 Ingrese la búsqueda de oferta laboral: ")
    
    inputs = {
        'sheet_url': sheet_url,
        'query': query,
        'current_year': str(datetime.now().year)
    }
    
    try:
        RrhhAgents().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        RrhhAgents().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    sheet_url = input("🔗 Ingrese la URL del Google Sheet con candidatos: ")
    query = input("🔍 Ingrese la búsqueda de oferta laboral: ")

    inputs = {
        'sheet_url': sheet_url,
        'query': query,
        'current_year': str(datetime.now().year)
    }
    
    try:
        RrhhAgents().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()