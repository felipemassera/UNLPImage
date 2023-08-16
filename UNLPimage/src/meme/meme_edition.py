import PySimpleGUI as sg
from UNLPimage.src.meme.meme_function import start_edit
from UNLPimage.src.meme.meme_function import update_meme
from UNLPimage.src.meme.meme_function import edition_meme
from UNLPimage.src.meme.meme_function import save_meme
import os
from UNLPimage.common.path import PATH_FONTS
import UNLPimage.src.classes.log as logs
from UNLPimage.src.functions.files_functions import open_record


def run(meme_info, path):
    """Muestra la ventana de edicion en la que
        permite elegir la fuente entre las disponibles,
        escribir en las cajas de texto del meme y un boton
        de actualizar para guardar y mostrar los cambios para
        finalmente guardar con un titulo y como .jpg y .png.

    Args:
        meme_info (dict): la informacion sobre el meme
        path (str): la direccion de la carpeta donde esta el meme
    """
    colors = {"Negro":"black", "Blanco":"white", "Rojo":"red", "Verde":"green"}
    logs.Log.try_open_logs()
    window = start_edit(len(meme_info["text_boxes"]), list(colors.keys()))
    meme = update_meme(window, meme_info["image"], path)
    font = ""
    copy = None
    path_save = open_record()["-MEMEPATH-"]
    written_text = ""
    while True:
        event, values = window.read()
        match event:
            case sg.WIN_CLOSE_ATTEMPTED_EVENT:
                confirm = sg.popup_yes_no("¿Está seguro que desea salir?")
                if confirm == "Yes":
                    exit()
            case "-RETURN-":
                break
            case "-FONTS-":
                font = values["-FONTS-"][0]
                font = os.path.join(PATH_FONTS, font)
            case "-SAVE-":
                if copy != None:
                    text = "".join(text + " " for text in written_text)
                    save_meme(copy, path_save, meme_info, text)
                else:
                    sg.popup_error("No se han realizado cambios")
            case "-UPDATE-":
                if font != "" and values["-FONTCOLOR-"]:
                    answer = sg.popup_yes_no("¿Desea actualizar la imagen?")
                    if answer == "Yes":
                        copy = meme.copy()
                        written_text = [values[f"-TEXT{i+1}-"] for i in range(len(meme_info["text_boxes"]))]
                        edition_meme(
                            window,
                            meme_info,
                            written_text,
                            copy,
                            font,
                            colors[values["-FONTCOLOR-"][0]],
                    )
                else:
                    sg.popup_error("Seleccione una fuente")
    window.close()
