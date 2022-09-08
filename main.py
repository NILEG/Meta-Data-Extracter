from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDIcon
import threading
import json
from tinytag import TinyTag
from plyer import filechooser
Window.size=(900,600)
class Ibtn(ButtonBehavior, MDIcon):
    pass
class Interface(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_dropfile=self.selection)
    def processor(self, path):
        info=TinyTag.get(path)
        str_dict=str(info)
        result=json.loads(str_dict)
        print(len(result))
        self.table=MDDataTable(size_hint=(1,1), column_data=[("[color=#3f51b5]KEYS[/color]", dp(65)), ("[color=#3f51b5]VALUES[/color]", dp(70))], rows_num=19)
        for item in result.items():
            self.table.row_data.append((item[0],item[1]))
        self.ids.tab_plc.add_widget(self.table)
        print(type(result))
        self.ids.sm.current = "output"
        self.ids.sm.transition.direction = "left"
        Window.unbind(on_dropfile=self.selection)
    def selection(self,win,path):
        self.processor(path)
    def upload_file(self):
        file=filechooser.open_file(title="Choose Audio/Video File", filters=[("*.mp3","*.wav","*mp4","*.mkv")])
        self.ids.import_btn.icon = "Drag.png"
        self.processor(file[0])

    def button_press(self):
        self.ids.import_btn.icon="Drop.png"
        thread=threading.Thread(target=self.upload_file)
        thread.start()
    def back_btn(self):
        self.ids.sm.current = "import"
        self.ids.sm.transition.direction="right"
        self.ids.tab_plc.remove_widget(self.table)
        Window.bind(on_dropfile=self.selection)
class MetaApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette="Indigo"
MetaApp().run()