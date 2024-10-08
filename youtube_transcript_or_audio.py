import tkinter as tk
from tkinter import messagebox, filedialog
from youtube_transcript_api import YouTubeTranscriptApi
import re


class YouTubeTranscriptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Transcript Fetcher")
        self.create_widgets()

    def create_widgets(self):
        # URL Entry
        self.url_label = tk.Label(self.root, text="YouTube Video URL:")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5)

        # Fetch Button
        self.fetch_button = tk.Button(
            self.root, text="Fetch Transcript", command=self.fetch_transcript
        )
        self.fetch_button.pack(pady=10)

        # Frame for Text and Scrollbar
        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=5)

        # Transcript Text Area
        self.transcript_text = tk.Text(text_frame, wrap="word", width=60, height=20)
        self.transcript_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=self.transcript_text.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        self.transcript_text.configure(yscrollcommand=scrollbar.set)

        # Save Button
        self.save_button = tk.Button(
            self.root, text="Save Transcript", command=self.save_transcript
        )
        self.save_button.pack(pady=5)

    def fetch_transcript(self):
        video_url = self.url_entry.get()
        video_id = self.extract_video_id(video_url)
        if not video_id:
            messagebox.showerror("Error", "Invalid YouTube URL.")
            return

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(["en"]).fetch()
            transcript_text = "\n".join([entry["text"] for entry in transcript])
            self.transcript_text.delete(1.0, tk.END)
            self.transcript_text.insert(tk.END, transcript_text)
        except Exception as e:
            messagebox.showinfo("Info", "Transcript not available for this video.")

    def save_transcript(self):
        transcript = self.transcript_text.get(1.0, tk.END)
        if not transcript.strip():
            messagebox.showwarning("Warning", "No transcript to save.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(transcript)
            messagebox.showinfo("Success", f"Transcript saved to {file_path}")

    def extract_video_id(self, url):
        # Regex to extract YouTube video ID
        regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(regex, url)
        return match.group(1) if match else None


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeTranscriptApp(root)
    root.mainloop()
