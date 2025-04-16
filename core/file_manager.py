from tkinter import filedialog

def load_audio_file(self):
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
    if file_path:
        print(f"Loaded file: {file_path}")