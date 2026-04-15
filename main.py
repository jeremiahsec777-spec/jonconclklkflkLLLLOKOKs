import os
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger
from plyer import audio

from cocoonglass.ui.orb import LiquidGlassOrb
from cocoonglass.ui.glass_card import GlassCard
from cocoonglass.storage.manager import NoteManager
from cocoonglass.storage.database import NoteIndex
from cocoonglass.transcription.engine import TranscriptionEngine
from cocoonglass.utils.android_helper import AndroidHelper

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        # Base path for data
        self.base_path = os.path.expanduser("~/CocoonGlass") if os.name != 'nt' else "CocoonGlass"
        os.makedirs(self.base_path, exist_ok=True)

        # Initialize Managers
        self.note_manager = NoteManager(self.base_path)
        self.note_index = NoteIndex(self.base_path)

        # Engine paths
        model_path = os.path.join(self.base_path, "models", "ggml-tiny.bin")
        whisper_bin = os.path.join(os.getcwd(), "whisper-bin")
        self.engine = TranscriptionEngine(model_path, whisper_bin)

        # UI components
        self.orb = LiquidGlassOrb(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.orb.bind(is_recording=self.on_recording_toggle)

        self.layout.add_widget(self.orb)
        self.add_widget(self.layout)

        # Notification card
        self.card = None

        # Audio recording path
        self.audio_path = os.path.join(self.base_path, "cache", "capture.wav")
        os.makedirs(os.path.dirname(self.audio_path), exist_ok=True)

    def on_recording_toggle(self, instance, value):
        if value:
            Logger.info("App: Started Recording")
            try:
                audio.start_recording(self.audio_path)
            except Exception as e:
                Logger.error(f"App: Could not start recording: {e}")
        else:
            Logger.info("App: Stopped Recording")
            try:
                audio.stop_recording()

                # Check if file exists and has size
                if os.path.exists(self.audio_path) and os.path.getsize(self.audio_path) > 0:
                    if not os.path.exists(self.engine.whisper_bin_path):
                        Logger.warning("App: Whisper binary not found, using mock transcription for the captured file")
                        self.on_transcription_complete(f"Captured audio saved to {self.audio_path}. (Mock transcription)")
                    else:
                        self.engine.transcribe(self.audio_path, self.on_transcription_complete)
                else:
                    Logger.warning("App: No audio data captured")
                    self.on_transcription_complete("No voice detected or recording failed.")
            except Exception as e:
                Logger.error(f"App: Error stopping recording: {e}")
                self.on_transcription_complete("Recording error occurred.")

    def on_transcription_complete(self, text):
        if text:
            # Save note
            file_path = self.note_manager.save_note(text)
            metadata, _ = self.note_manager.load_note(file_path)

            # Index note
            self.note_index.index_note(
                metadata['id'], metadata['title'], metadata['category'],
                metadata['created_at'], file_path, text
            )

            # Show Glass Card
            Clock.schedule_once(lambda dt: self.show_card(metadata['title'], text), 0.5)

    def show_card(self, title, text):
        if self.card:
            self.layout.remove_widget(self.card)

        self.card = GlassCard(
            title=title,
            text=text,
            size_hint=(0.8, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.layout.add_widget(self.card)

class CocoonGlassApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        # Android specific setup
        AndroidHelper.request_miui_permissions()
        AndroidHelper.disable_battery_optimization()

        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    CocoonGlassApp().run()
