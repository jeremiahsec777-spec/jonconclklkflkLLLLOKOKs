import os
import subprocess
import threading
from kivy.logger import Logger

class TranscriptionEngine:
    def __init__(self, model_path, whisper_bin_path):
        self.model_path = model_path
        self.whisper_bin_path = whisper_bin_path
        self.is_transcribing = False

    def transcribe(self, audio_path, callback):
        """
        Transcribes the audio file using whisper.cpp.
        Implements Load-Run-Unload logic by calling the binary.
        """
        if self.is_transcribing:
            Logger.warning("TranscriptionEngine: Already transcribing")
            return

        def run_whisper():
            self.is_transcribing = True
            try:
                # Command for whisper.cpp: ./main -m models/ggml-tiny.bin -f samples/jfk.wav -nt
                cmd = [
                    self.whisper_bin_path,
                    "-m", self.model_path,
                    "-f", audio_path,
                    "-nt", # No timestamps
                    "-otxt" # Output text file
                ]

                Logger.info(f"TranscriptionEngine: Running cmd: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    # whisper.cpp usually creates a file with .txt extension
                    txt_path = audio_path + ".txt"
                    if os.path.exists(txt_path):
                        with open(txt_path, 'r') as f:
                            text = f.read().strip()
                        os.remove(txt_path) # Clean up
                        callback(text)
                    else:
                        callback(result.stdout.strip())
                else:
                    Logger.error(f"TranscriptionEngine: Error: {result.stderr}")
                    callback(None)
            except Exception as e:
                Logger.error(f"TranscriptionEngine: Exception: {str(e)}")
                callback(None)
            finally:
                self.is_transcribing = False

        threading.Thread(target=run_whisper).start()

    def unload_model(self):
        # In whisper.cpp calling the binary handles load-run-unload automatically.
        # If we were using a library binding, we'd explicitly free memory here.
        pass
