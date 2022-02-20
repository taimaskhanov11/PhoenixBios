import re
import time

from loguru import logger
from pywinauto.controls.hwndwrapper import HwndWrapper

from phoenixbios.config import PHOENIX_EXE_PATH, FILENAME

from pywinauto import application
from pywinauto import keyboard

app = application.Application()

try:
    app.start(PHOENIX_EXE_PATH)

except Exception as e:
    app.connect(path=PHOENIX_EXE_PATH)
    logger.error(e)

app.PhoenixBIOSEditorProNEW6006.wrapper_object().set_focus()
# app.PhoenixBIOSEditorPro.move_window(x=500, y=500, width=1200, height=600, repaint=True)
toolbar: HwndWrapper = app.PhoenixBIOSEditorPro.child_window(class_name="ToolbarWindow32").wrapper_object()
toolbar.click_input(coords=(30, 30))
open_rom = app.OpenROMFile

open_rom.print_control_identifiers()
fiel_names_type: HwndWrapper = open_rom.child_window(class_name="Edit").wrapper_object()
open_button: HwndWrapper = open_rom.child_window(title="&Открыть", class_name="Button").wrapper_object()
address: HwndWrapper = open_rom.child_window(title="Адресная строка", class_name="ToolbarWindow32").wrapper_object()
address.click()

keyboard.send_keys(r"C:\Users\taima\Downloads")
keyboard.send_keys("{ENTER}")
fiel_names_type.type_keys(FILENAME)
open_button.type_keys("{ENTER}")
app.PhoenixBIOSEditorPro.Yes.click()

attr_name = re.findall(r"(.*)\.", FILENAME)
if attr_name:
    FILENAME = attr_name[0]

phoenix = getattr(app, f"PhoenixBIOSEditorPro{FILENAME}")
phoenix.print_control_identifiers()
dmi = phoenix.child_window(title="DMI Strings", class_name="ThunderRT6FormDC")
dmi_wrap: HwndWrapper = dmi.wrapper_object()
time.sleep(1)
