import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class DetailedA90Ransom(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. ARKA PLAN (Kıpkırmızı Ransomware Teması)
        with self.canvas.before:
            Color(0.85, 0.1, 0.1, 1)  # Kırmızı
            self.rect_bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # 2. ÜST METİN (YOUR ITEMS HAVE BEEN ENCRYPTED)
        self.title_label = Label(
            text="[b]YOUR ITEMS\nHAVE BEEN\nENCRYPTED[/b]",
            markup=True,
            font_size='28sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(1, 0.3),
            pos_hint={'x': 0, 'top': 1}
        )
        self.add_widget(self.title_label)

        # 3. ORTA SİYAH UYARI KUTUSU
        # Siyah arka planı Label'ın canvas'ına ekliyoruz
        self.warning_label = Label(
            text="[b]IF YOU DO NOT PAY THIS RANSOM BEFORE\nTHE TIMER ENDS, YOUR ITEMS WILL BE\n[color=ff0000]UNRECOVERABLE BY ANY MEANS.[/color][/b]",
            markup=True,
            font_size='15sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(0.9, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        with self.warning_label.canvas.before:
            Color(0, 0, 0, 1)  # Siyah kutu
            self.rect_warning = Rectangle(size=self.warning_label.size, pos=self.warning_label.pos)
        self.warning_label.bind(size=self._update_warning_bg, pos=self._update_warning_bg)
        self.add_widget(self.warning_label)

        # 4. ALT BÖLÜM: COIN (500)
        self.coin_label = Label(
            text="[b]500  🪙[/b]",
            markup=True,
            font_size='26sp',
            color=(1, 0.8, 0, 1),  # Altın sarısı
            size_hint=(0.4, 0.15),
            pos_hint={'x': 0.05, 'y': 0.1}
        )
        with self.coin_label.canvas.before:
            Color(0, 0, 0, 1)  # Siyah kutu
            self.rect_coin = Rectangle(size=self.coin_label.size, pos=self.coin_label.pos)
        self.coin_label.bind(size=self._update_coin_bg, pos=self._update_coin_bg)
        self.add_widget(self.coin_label)

        # 5. ALT BÖLÜM: ZAMAN SAYACI (TIME: 01:29)
        self.time_remaining = 89  # 1 dakika 29 saniye
        self.timer_label = Label(
            text=f"[b]TIME:    01:29[/b]",
            markup=True,
            font_size='26sp',
            color=(0.5, 0, 0, 1), # Koyu kırmızı yazı
            size_hint=(0.45, 0.15),
            pos_hint={'right': 0.95, 'y': 0.1}
        )
        with self.timer_label.canvas.before:
            Color(1, 0, 0, 1)  # Parlak kırmızı kutu
            self.rect_timer = Rectangle(size=self.timer_label.size, pos=self.timer_label.pos)
        self.timer_label.bind(size=self._update_timer_bg, pos=self._update_timer_bg)
        self.add_widget(self.timer_label)

        # 6. EKRANDA GEZİNEN A-90 KAFASI
        self.a90_face = Image(source='a90_image.png', size_hint=(None, None), size=(180, 180))
        self.a90_face.pos = (50, 50)
        self.dx = 12  # X eksenindeki hızı
        self.dy = 12  # Y eksenindeki hızı
        self.add_widget(self.a90_face)

        # 7. SES DOSYASINI YÜKLE VE BAŞLAT
        self.sound = SoundLoader.load('Ransom (a-90) theme roblox doors.mp3')
        if self.sound:
            self.sound.loop = True
            self.sound.play()

        # Döngüleri Başlat (Sayaç ve Sekme Animasyonu)
        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.animate_face, 1.0 / 60.0)  # 60 FPS hareket

        # 8. GİZLİ KLAVYE DİNLEYİCİ (Uygulamayı kapatmak için)
        Window.bind(on_keyboard=self.on_keyboard)

    # --- ARKA PLAN ÇİZİM GÜNCELLEMELERİ ---
    def _update_bg(self, instance, value):
        self.rect_bg.pos = instance.pos
        self.rect_bg.size = instance.size

    def _update_warning_bg(self, instance, value):
        self.rect_warning.pos = instance.pos
        self.rect_warning.size = instance.size

    def _update_coin_bg(self, instance, value):
        self.rect_coin.pos = instance.pos
        self.rect_coin.size = instance.size

    def _update_timer_bg(self, instance, value):
        self.rect_timer.pos = instance.pos
        self.rect_timer.size = instance.size

    # --- SAYAÇ GÜNCELLEMESİ ---
    def update_timer(self, dt):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            mins, secs = divmod(self.time_remaining, 60)
            self.timer_label.text = f"[b]TIME:    {mins:02d}:{secs:02d}[/b]"
        else:
            self.timer_label.text = "[b]TIME EXPIRED![/b]"

    # --- A-90 KAFASININ EKRANDA SEKMESİ ---
    def animate_face(self, dt):
        x, y = self.a90_face.pos
        x += self.dx
        y += self.dy

        # Ekran sınırlarına çarpma kontrolü
        if x <= 0 or x + self.a90_face.width >= self.width:
            self.dx *= -1
        if y <= 0 or y + self.a90_face.height >= self.height:
            self.dy *= -1

        self.a90_face.pos = (x, y)

    # --- GİZLİ 'X' TUŞU İLE KAPATMA ---
    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        # Klavyeden 'X' veya 'x' basıldığında yakalar
        if codepoint in ['x', 'X']:
            if self.sound:
                self.sound.stop()
            App.get_running_app().stop()
            return True
        return False

class A90App(App):
    def build(self):
        return DetailedA90Ransom()

if __name__ == '__main__':
    A90App().run()
