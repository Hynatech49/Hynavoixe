import pyaudio
import wave
import threading

class AudioRecorder:
    def __init__(self, filename="output.wav", chunk=1024, channels=1, rate=44100, record_seconds=5):
        self.filename = filename
        self.chunk = chunk
        self.channels = channels
        self.rate = rate
        self.record_seconds = record_seconds
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)

        print("Recording...")
        t = threading.Thread(target=self._record)
        t.start()

    def _record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        if self.audio.is_format_supported(self.rate, input_device=self.audio.get_default_input_device()):
            print("Finished recording.")
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            with wave.open(self.filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
                print(f"Audio saved as {self.filename}")
        else:
            print("Error: Recording format not supported.")

    def __del__(self):
        if hasattr(self, 'audio') and hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.start_recording()
    input("Press Enter to stop recording...")
    recorder.stop_recording()
