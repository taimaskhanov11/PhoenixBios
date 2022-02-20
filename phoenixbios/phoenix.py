import random
import re
import time

from loguru import logger
from pywinauto.controls.hwndwrapper import HwndWrapper

from phoenixbios.config import PHOENIX_EXE_PATH, FILENAME, FILEPATH, FILE_SAVE_NAME, FILE_SAVE_PATH, CONFIG, \
    LAUNCH_TYPE, MOTHERBOARDS

from pywinauto import application
from pywinauto import keyboard


class PhoenixBios:

    def __init__(self, config: dict):

        self.motherboard_model = config.get("motherboard_model")
        self.serial_number = config.get("serial_number")
        self.system_product_name = config.get("system_product_name")
        self.system_serial_number = config.get("system_serial_number")
        self.chassis_serial_number = config.get("chassis_serial_number")
        self.sleep_time: int | float = config.get("sleep_time")
        self.add_sleep_time: int | float = config.get("add_sleep_time")
        self.app = application.Application()
        self.phoenix = None

    def sleep(self, s=0):
        s = self.sleep_time - s
        time.sleep(s)

    def add_sleep(self):
        time.sleep(self.add_sleep_time)

    def open_file(self):
        # toolbar: HwndWrapper = self.phoenix.child_window(class_name="ToolbarWindow32").wrapper_object()
        # self.phoenix.print_control_identifiers()
        # exit()
        # toolbar.click_input(coords=(30, 30))
        keyboard.send_keys("^o")
        self.sleep(1)
        open_rom = self.app.OpenROMFile
        # open_rom.print_control_identifiers()

        fiel_names_type: HwndWrapper = open_rom.child_window(class_name="Edit").wrapper_object()
        open_button: HwndWrapper = open_rom.child_window(title="&Open", class_name="Button").wrapper_object()
        address: HwndWrapper = open_rom.child_window(title="Address band",
                                                     class_name="ToolbarWindow32").wrapper_object()
        address.click()
        keyboard.send_keys(FILEPATH, pause=0)
        self.sleep(1)
        keyboard.send_keys("{ENTER}")
        fiel_names_type.type_keys(FILENAME, pause=0)
        open_button.type_keys("{ENTER}")
        self.phoenix.Yes.click()

    @staticmethod
    def edit_string(string: str, count=2):
        for i in range(count):
            keyboard.send_keys("{DOWN}")
        keyboard.send_keys("{ENTER}")
        keyboard.send_keys(string, with_spaces=True, pause=0)
        keyboard.send_keys("{ENTER}")

    @staticmethod
    def get_rand() -> str:
        res = str(random.randint(0, 999999999999))
        if len(res) < 12:
            zeros = 12 - len(res)
            res = "0" * zeros + res
        return res

    def edit_dmi(self, motherboard, serial_number):
        self.phoenix = getattr(self.app, f"PhoenixBIOSEditorPro{FILENAME}")
        dmi_wrap: HwndWrapper = self.phoenix.child_window(title="DMI Strings",
                                                          class_name="ThunderRT6FormDC").wrapper_object()
        time.sleep(self.sleep_time)
        dmi_wrap.click_input(coords=(60, 20))
        # time.sleep(self.sleep_time)

        keyboard.send_keys("{RIGHT}")

        # motherboard_model
        self.edit_string(f"'{motherboard}'")

        # serial_number
        self.edit_string(serial_number)

        # system_product_name
        system_product_name = f"'Gigabyte {motherboard}'"
        self.edit_string(system_product_name)

        # system_serial_number
        self.edit_string(serial_number)

        # chassis_serial_number
        self.edit_string(serial_number, count=3)

    def run_phoenix(self):
        try:
            self.app.connect(path=PHOENIX_EXE_PATH)
        except Exception as e:
            logger.error(e)
            self.app.start(PHOENIX_EXE_PATH)

    def save(self, filename, serial_number):
        # self.phoenix.click()
        keyboard.send_keys("^u")
        self.sleep()
        keyboard.send_keys("{ENTER}")
        # time.sleep(0.1)
        keyboard.send_keys("{ENTER}")
        # time.sleep(1)

        open_rom = self.app.SaveROMFile
        # open_rom.print_control_identifiers()
        # logger.info()
        fiel_names_type: HwndWrapper = open_rom.child_window(class_name="Edit").wrapper_object()
        open_button: HwndWrapper = open_rom.child_window(title="&Save", class_name="Button").wrapper_object()
        address: HwndWrapper = open_rom.child_window(title="Address band",
                                                     class_name="ToolbarWindow32").wrapper_object()
        address.click()

        keyboard.send_keys(FILE_SAVE_PATH, pause=0)
        keyboard.send_keys("{ENTER}")
        self.sleep(1)
        fiel_names_type.type_keys(f"{filename}_{serial_number}", pause=0)
        open_button.type_keys("{ENTER}")

    def start(self):
        # match LAUNCH_TYPE:  # todo 19.02.2022 17:19 taima:
        #     case "new":
        #         self.run_phoenix()
        #     case "connect":
        #         pass
        self.run_phoenix()
        for motherboard in MOTHERBOARDS:
            self.phoenix = self.app.PhoenixBIOSEditorPro
            self.phoenix.wrapper_object().set_focus()
            self.open_file()
            self.sleep()
            serial_number = f"'{self.get_rand()}'"
            self.edit_dmi(motherboard, serial_number)
            self.save(motherboard, serial_number)
            self.sleep()

