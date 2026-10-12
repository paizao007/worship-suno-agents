"""
Ponto de entrada do projeto de Agentes de IA para Adoração e Suno AI.
"""

import sys
from cli import run_cli_interactive

if __name__ == "__main__":
    try:
        run_cli_interactive()
    except KeyboardInterrupt:
        print("\n\nProcessamento interrompido pelo usuário. Que a graça e a paz estejam convosco!")
        sys.exit(0)
