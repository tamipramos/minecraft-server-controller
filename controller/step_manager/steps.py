import json
import importlib
from rich.console import Console
from rich.progress import Progress

class StepManager:
    _instance = None
    task = None
    progress = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StepManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, json_path="controller/step_manager/steps.json", module_name="controller.step_manager.functions_lib"):
        if hasattr(self, 'initialized'):
            return
        self.json_path = json_path
        self.module_name = module_name
        self.console = Console()
        self.functions_module = None
        self.steps = None
        self.initialized = True

    def _load_steps(self):
        """Carga el archivo JSON de steps"""
        with open(self.json_path, "r") as file:
            self.steps = json.load(file)

    def _load_functions_module(self):
        """Importa el modulo de funciones"""
        self.functions_module = importlib.import_module(self.module_name)

    def initialize(self):
        """Inicializa el proceso de ejecucion de pasos"""
        global progress
        self._load_steps()
        self._load_functions_module()

        total_steps = sum(len(step.get(key, [])) for step in self.steps["steps"] for key in step)
        #self.console.log(f"[green]Número de pasos: {total_steps}[/green]")

        with Progress() as progress:
            StepManager.task = progress.add_task("[cyan]Realizando tareas: [/cyan]", total=total_steps)
            self._execute_steps(progress)
        self.console.log('[green]Proceso completado.[/green]')
        
    def _execute_steps(self, progress):
        """Ejecuta todos los pasos con una barra de progreso."""
        for step in self.steps["steps"]:
            for key, values in step.items():
                self.execute_step_group(key, progress)

    def execute_step_group(self, group_name, progress=None):
        """Ejecuta un grupo específico de pasos por nombre"""
        for step in self.steps["steps"]:
            if group_name in step:
                values = step[group_name]
                for value in values:
                    func_name = value.get("func")
                    description = value.get("description")
                    automatic_callable = value.get("automatic_callable", True)
                    args = value.get("args", [])
                    if description and func_name:
                        if progress:
                            progress.update(StepManager.task, description=f"[cyan]{description}[/cyan]")
                        if automatic_callable:
                            if hasattr(self.functions_module, func_name):
                                func = getattr(self.functions_module, func_name)
                                func(*args)
                            else:
                                self.console.log(f"[red]Función '{func_name}' no encontrada.[/red]")

                        if progress:
                            progress.update(StepManager.task, advance=1)
        
    def execute_manual_step(self, func_name, *args):
        """Ejecuta manualmente un paso específico por nombre de función y argumentos."""
        progress.update(StepManager.task, advance=1)
        if hasattr(self.functions_module, func_name):
            func = getattr(self.functions_module, func_name)
            for step in self.steps["steps"]:
                for key, values in step.items():
                    for value in values:
                        if value.get("func") == func_name:
                            description = value.get("description", "Descripción no disponible")
                            break
            progress.update(StepManager.task, description=f"[cyan]{description}[/cyan]")
            func(*args)
        else:
            self.console.log(f"[red]Función '{func_name}' no encontrada para ejecución manual.[/red]")

if __name__ == "__main__":
    step_manager = StepManager() 
    step_manager.initialize()
    #step_manager.execute_manual_step("download_file")
    #execute_step_group