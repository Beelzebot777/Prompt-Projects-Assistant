# src/controller/prompt_controller.py

from tkinter import messagebox
from src.core import FileManager
from src.config import FOLDERS_TO_IGNORE


class PromptController:
    def __init__(self, gui_helper, view):
        self.view = view
        self.gui_helper = gui_helper
        self.file_manager = FileManager(FOLDERS_TO_IGNORE)

        self.prompt_base_path = None
        self.project_folder = None
        self.selected_files = []
        self.estructura = ''
        self.contenido_archivos = ''
        self.prompt_final = ''

    def seleccionar_prompt_base(self):
        path = self.gui_helper.seleccionar_ruta(tipo="archivo")
        if path:
            self.prompt_base_path = path

            # Actualizar estado y mostrar contenido
            self.view.left_panel.set_prompt_base_estado(True)
            with open(path, 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.view.center_panel.mostrar_prompt_base(contenido)

            self.actualizar_prompt_final()
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")

    def seleccionar_proyecto(self):
        path = self.gui_helper.seleccionar_ruta(tipo="carpeta")
        if path:
            self.project_folder = path

            self.estructura = self.file_manager.genera_estructura_de_carpetas(path)
            self.view.left_panel.set_project_estado(True)
            self.view.center_panel.mostrar_estructura(self.estructura)

            self.actualizar_prompt_final()
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna carpeta.")

    def seleccionar_archivos(self):
        if not self.project_folder:
            messagebox.showerror("Error", "Primero seleccione una carpeta de proyecto.")
            return

        self.selected_files = self.gui_helper.mostrar_arbol_directorios(self.project_folder)
        if self.selected_files:
            self.view.left_panel.set_archivos_estado(True, len(self.selected_files))
            self.view.left_panel.mostrar_lista_archivos(self.selected_files)

            self.contenido_archivos = self.file_manager.extrae_contenido_archivos(self.selected_files)
            self.view.center_panel.mostrar_contenido_archivos(self.contenido_archivos)

            self.actualizar_prompt_final()
        else:
            messagebox.showwarning("Advertencia", "No se seleccionaron archivos.")
            self.view.left_panel.set_archivos_estado(False)

    def actualizar_prompt_final(self):
        prompt_base = self.view.center_panel.obtener_prompt_base()
        if not prompt_base:
            return

        self.prompt_final = self.view.right_panel.construir_prompt_final(
            prompt_base,
            self.estructura,
            self.contenido_archivos
        )        
        self.prompt_final = self.view.right_panel.obtener_prompt_final()

    def copiar_prompt(self):
        if self.prompt_final:
            self.gui_helper.copiar_al_portapapeles(self.prompt_final)
        else:
            messagebox.showwarning("Advertencia", "El prompt final está vacío.")

    def limpiar_todo(self):
        self.prompt_base_path = None
        self.project_folder = None
        self.selected_files = []
        self.estructura = ''
        self.contenido_archivos = ''
        self.prompt_final = ''

        self.view.left_panel.set_prompt_base_estado(False)
        self.view.left_panel.set_project_estado(False)
        self.view.left_panel.set_archivos_estado(False)
        self.view.left_panel.mostrar_lista_archivos([])

        self.view.center_panel.mostrar_prompt_base("")
        self.view.center_panel.mostrar_estructura("")
        self.view.center_panel.mostrar_contenido_archivos("")

        self.view.right_panel.mostrar_prompt_final("")

        messagebox.showinfo("Prompt Assistant", "Todos los campos han sido limpiados correctamente.")
