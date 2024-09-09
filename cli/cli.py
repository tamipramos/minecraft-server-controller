from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.shortcuts import radiolist_dialog

def menu1():
    choices = [('Sencilla',1),('Avanzada',2)]
    result = button_dialog(
        title='MINECRAFT SERVER ADMIN',
        text='Por favor, seleccione una instalación:',
        buttons=[(option, value) for option, value in choices]
    ).run()
    return result
  
def menu2():
      result = radiolist_dialog(
            title="MINECRAFT SERVER ADMIN",
            text="¿Que tipo de instalación desea?",
            values=[
                ("option1", "Sin Mods"),
                ("option2", "Forge"),
                ("option3", "Fabrik"),                
                ("option4", "Forge+Fabrik")
            ]
        ).run()
      return result

def app_flow():
  result1 = menu1()
  if result1 == 1:
    ...
  if result1 == 2:
    result2=menu2()