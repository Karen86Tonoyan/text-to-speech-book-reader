#!/usr/bin/env python3
"""
Minimalny program do czytania książek z TTS (Kivy + Edge-TTS)
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import threading
import os
from pathlib import Path
import tempfile
import asyncio

class TTSEngine:
    def __init__(self):
        self.voice = "pl-PL-ZofiaNeural"
        self.speed = 1.0
        self.temp_dir = Path(tempfile.gettempdir()) / "book_tts"
        self.temp_dir.mkdir(exist_ok=True)
        try:
            import edge_tts
            self.edge_available = True
        except ImportError:
            print("pip install edge-tts")
            self.edge_available = False

    def text_to_speech(self, text):
        if self.edge_available:
            return self._edge_tts(text)
        return None

    def _edge_tts(self, text):
        import edge_tts
        import hashlib
        filename = self.temp_dir / f"tts_{hashlib.sha1(text.encode()).hexdigest()[:12]}_{self.speed}.mp3"
        if filename.exists():
            return str(filename)
        async def generate():
            communicate = edge_tts.Communicate(text, self.voice, rate=f"+{int((self.speed-1)*100)}%")
            await communicate.save(str(filename))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generate())
        loop.close()
        return str(filename)

class BookReaderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts = TTSEngine()
        self.current_text = ""
        self.current_position = 0
        self.is_playing = False

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.status_label = Label(text='Wybierz książkę', font_size='18sp')
        layout.add_widget(self.status_label)
        self.play_btn = Button(text='▶️ Play', on_press=self.toggle_playback, disabled=True)
        layout.add_widget(self.play_btn)
        self.load_btn = Button(text='📖 Wczytaj', on_press=self.show_file_chooser)
        layout.add_widget(self.load_btn)
        return layout

    def show_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(filters=['*.txt'])
        content.add_widget(filechooser)
        select_btn = Button(text='Wczytaj')
        content.add_widget(select_btn)
        popup = Popup(title='Wybierz książkę', content=content, size_hint=(0.9, 0.9))
        def select_file(btn):
            if filechooser.selection:
                self.load_book(filechooser.selection[0])
            popup.dismiss()
        select_btn.bind(on_press=select_file)
        popup.open()

    def load_book(self, filepath):
        self.status_label.text = f'Ładowanie: {Path(filepath).name}'
        def load_thread():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.current_text = f.read()
                self.current_position = 0
                self.status_label.text = f'Załadowano: {Path(filepath).name}'
                self.play_btn.disabled = False
            except Exception as e:
                self.status_label.text = f'Błąd: {e}'
        threading.Thread(target=load_thread, daemon=True).start()

    def toggle_playback(self, instance):
        if self.is_playing:
            self.is_playing = False
            self.play_btn.text = '▶️ Play'
            self.status_label.text = 'Pauza'
        else:
            self.is_playing = True
            self.play_btn.text = '⏸️ Pauza'
            self.status_label.text = 'Odtwarzanie...'
            threading.Thread(target=self._playback_loop, daemon=True).start()

    def _playback_loop(self):
        text_remaining = self.current_text[self.current_position:]
        sentences = [s.strip() + '.' for s in text_remaining.split('.') if s.strip()]
        for sentence in sentences:
            if not self.is_playing:
                break
            try:
                audio_file = self.tts.text_to_speech(sentence.strip())
                self._play_audio(audio_file)
                self.current_position += len(sentence)
            except Exception as e:
                self.status_label.text = f'TTS Error: {e}'
                continue
        self.is_playing = False
        self.play_btn.text = '▶️ Play'
        self.status_label.text = 'Koniec książki'

    def _play_audio(self, audio_file):
        from kivy.core.audio import SoundLoader
        sound = SoundLoader.load(audio_file)
        if sound:
            sound.play()
            while sound.state == 'play':
                pass

if __name__ == '__main__':
    BookReaderApp().run()
