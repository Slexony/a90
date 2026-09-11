import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class A90RansomwareMobileApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # Arka plan rengini siyah yap
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.size)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Oyun değişkenleri
        self.time_remaining = 89  # 01:29 süresi
        self.coins = 500

        # --- SES DOSYASINI BAŞLAT ---
        self.sound = SoundLoader.load('music.mp3')
        if self.sound:
            self.sound.loop = True
            self.sound.play()

        # --- 1. ÜST KIRMIZI ALAN (A90 Görseli + Metin) ---
        header = BoxLayout(orientation='horizontal', size_hint_y=0.35, spacing=10)
        with header.canvas.before:
            Color(0.8, 0, 0, 1) # Kırmızı arka plan
            Rectangle(pos=header.pos, size=header.size)

        # A90 Görseli
        if os.path.exists('a90_image.png'):
            header.add_widget(Image(source='a90_image.png', size_hint_x=0.35))
        else:
            header.add_widget(Label(text="[A90]", color=(1,1,1,1), font_size='20sp', size_hint_x=0.35))

        # Title Metni
        header.add_widget(Label(
            text="YOUR ITEMS\nHAVE BEEN\nENCRYPTED",
            font_size='22sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        ))
        self.add_widget(header)

        # --- 2. ORTA SİYAH UYARI KUTUSU ---
        warning_box = Label(
            text="IF YOU DO NOT PAY THIS RANSOM BEFORE\nTHE TIMER ENDS, YOUR ITEMS WILL BE\nUNRECOVERABLE BY ANY MEANS.",
            font_size='14sp',
            bold=True,
            color=(1, 0.2, 0.2, 1),
            halign='center',
            valign='middle',
            size_hint_y=0.25
        )
        self.add_widget(warning_box)

        # --- 3. ALT BİLGİ ALANI (COIN VE SAYAÇ) ---
        bottom_panel = GridLayout(cols=2, size_hint_y=0.2, spacing=10)

        # Sol: Coin Paneli
        self.coin_label = Label(
            text=f"{self.coins} 🪙",
            font_size='26sp',
            bold=True,
            color=(1, 0.8, 0, 1)
        )
        bottom_panel.add_widget(self.coin_label)

        # Sağ: Zaman Sayacı Paneli
        self.timer_label = Label(
            text="TIME: 01:29",
            font_size='24sp',
            bold=True,
            color=(1, 0, 0, 1)
        )
        bottom_panel.add_widget(self.timer_label)
        self.add_widget(bottom_panel)

        # --- 4. KLAVYE GİRDİ ALANI VE ÇIKIŞ (X Tuşu Kontrolü) ---
        input_panel = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)
        
        self.input_field = TextInput(
            hint_text="Kapatmak için 'X' yazın...",
            multiline=False,
            font_size='18sp',
            size_hint_x=0.7
        )
        self.input_field.bind(text=self.check_exit_code)
        input_panel.add_widget(self.input_field)

        self.add_widget(input_panel)

        # Zamanlayıcı Döngüsü
        Clock.schedule_interval(self.update_timer, 1)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_timer(self, dt):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            mins, secs = divmod(self.time_remaining, 60)
            self.timer_label.text = f"TIME: {mins:02d}:{secs:02d}"
        else:
            self.timer_label.text = "TIME EXPIRED!"

    def check_exit_code(self, instance, text):
        if text.strip().upper() == 'X':
            if self.sound:
                self.sound.stop()
            App.get_running_app().stop()

class RansomwareApp(App):
    def build(self):
        return A90RansomwareMobileApp()

if __name__ == '__main__':
    RansomwareApp().run()