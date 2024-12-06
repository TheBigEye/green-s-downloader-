import tkinter as tk
from tkinter import filedialog, ttk
from pytubefix import YouTube, Playlist, Channel
from pytubefix.cli import on_progress
import threading
import time
from PIL import Image, ImageTk
import os

class App:
    def __init__(self, root):
        self.ico = Image.open('./resources/icon.png')
        self.photo = ImageTk.PhotoImage(self.ico)

        self.font_family = "Segoe UI"

        self.root = root
        self.root.title("PyTubeGet")
        self.root.geometry("500x550")
        self.root.config(bg="#FFFFFF")
        self.root.resizable(False, False)
        root.wm_iconphoto(False, self.photo)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.main_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.main_frame.grid(row=1, column=1, sticky="nsew")

        self.link_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Waiting for URL...")
        self.percentage_var = tk.StringVar(value="0%")
        self.time_remaining_var = tk.StringVar()
        self.download_folder = None
        self.progress_circle = None
        self.download_start_time = None
        self.widgets = []
        self.current_angle = 0
        self.target_angle = 0
        self.animation_speed = 5

        self.audio_only_var = tk.BooleanVar(value=False)


    def create_widgets(self):
        title_label = tk.Label(
            self.main_frame,
            text="YouTube Downloader",
            font=(self.font_family, 24, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        self.widgets.append(title_label)

        url_entry = tk.Entry(
            self.main_frame,
            textvariable=self.link_var,
            font=(self.font_family, 12),
            width=40,
            relief="solid",
            bd=1,
            bg="#FFFFFF",
            fg="#333333"
        )
        url_entry.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
        url_entry.insert(0, "Enter video, playlist, or channel URL")
        url_entry.bind('<FocusIn>', self.on_entry_click)
        url_entry.bind('<FocusOut>', self.on_focusout)
        self.widgets.append(url_entry)

        style = ttk.Style()
        style.configure(
            "Modern.TCheckbutton",
            font=(self.font_family, 10),
            background="#FFFFFF"
        )

        audio_only_checkbox = ttk.Checkbutton(
            self.main_frame,
            text="Download audio only",
            variable=self.audio_only_var,
            style="Modern.TCheckbutton"
        )
        audio_only_checkbox.grid(row=2, column=0, columnspan=2, pady=10)
        self.widgets.append(audio_only_checkbox)

        button_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        folder_button = tk.Button(
            button_frame,
            text="Select Folder",
            command=self.select_folder,
            font=(self.font_family, 10),
            relief="flat",
            bg="#e0e0e0",
            fg="#333333",
            activebackground="#d0d0d0",
            padx=15,
            pady=8
        )
        folder_button.grid(row=0, column=0, padx=10)
        self.widgets.append(folder_button)

        download_button = tk.Button(
            button_frame,
            text="Download",
            command=self.start_download_thread,
            font=(self.font_family, 10),
            relief="flat",
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            padx=15,
            pady=8
        )
        download_button.grid(row=0, column=1, padx=10)
        self.widgets.append(download_button)

        self.canvas = tk.Canvas(
            self.main_frame,
            width=200,
            height=200,
            bg="#FFFFFF",
            bd=0,
            highlightthickness=0
        )

        self.canvas.create_arc(
            50, 50, 150, 150,
            start=0, extent=359.9,
            outline="#ddd",
            width=10,
            style="arc"
        )

        self.percentage_label = tk.Label(
            self.main_frame,
            textvariable=self.percentage_var,
            font=("Helvetica", 16, "bold"),
            bg="#FFFFFF"
        )

        self.time_remaining_label = tk.Label(
            self.main_frame,
            textvariable=self.time_remaining_var,
            font=("Helvetica", 10),
            bg="#FFFFFF"
        )

        # Status Label with modern font
        self.status_label = tk.Label(
            self.main_frame,
            textvariable=self.status_var,
            font=(self.font_family, 10),
            bg="#FFFFFF",
            fg="#666666",
            wraplength=400
        )
        self.status_label.grid(row=6, column=0, columnspan=2, pady=10)
        self.widgets.append(self.status_label)

        url_entry.delete(0, tk.END)
        url_entry.insert(0, "Enter video, playlist, or channel URL")


    def on_entry_click(self, event):
        if event.widget.get() == "Enter video, playlist, or channel URL":
            event.widget.delete(0, tk.END)
            event.widget.config(fg='#333333')


    def on_focusout(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, "Enter video, playlist, or channel URL")
            event.widget.config(fg='#999999')


    def download_content(self):
        link = self.link_var.get()
        if not link:
            self.status_var.set("Please enter a valid URL")
            return

        if not self.download_folder:
            self.status_var.set("Select a folder before downloading")
            return

        try:
            self.hide_widgets()
            self.download_start_time = time.time()

            if "playlist" in link.lower():
                self.download_playlist(link)
            elif "@" in link.lower():
                self.download_channel(link)
            else:
                self.download_single_video(link)

        except Exception as e:
            self.status_var.set(f"Download error: {e}")
            self.show_widgets()


    def download_single_video(self, link):
        youtube_object = YouTube(link, on_progress_callback=self.update_progress)
        video_title = youtube_object.title
        self.status_var.set(f"{video_title}")

        if self.audio_only_var.get():
            stream = youtube_object.streams.get_audio_only()
        else:
            stream = youtube_object.streams.get_highest_resolution()

        stream.download(output_path=self.download_folder)
        self.status_var.set("Download complete!")
        self.percentage_var = tk.StringVar(value="0%")

        self.show_widgets()


    def download_playlist(self, link):
        playlist = Playlist(link)
        total_videos = len(playlist.videos)
        self.status_var.set(f"{playlist.title} ({total_videos} videos)")

        for i, video in enumerate(playlist.videos, 1):
            try:
                self.status_var.set(f"Downloading {i}/{total_videos}: {video.title}")

                if self.audio_only_var.get():
                    stream = video.streams.get_audio_only()
                else:
                    stream = video.streams.get_highest_resolution()

                stream.download(
                    output_path=self.download_folder,
                    filename=f"{i}. {video.title}"
                )
            except Exception as e:
                self.status_var.set(f"Error downloading {video.title}: {e}")

        self.status_var.set("Playlist download complete!")
        self.show_widgets()

    def download_channel(self, link):
        channel = Channel(link)
        total_videos = len(channel.videos)
        self.status_var.set(f"Downloading {channel.channel_name} ({total_videos} videos)")

        for i, video in enumerate(channel.videos, 1):
            try:
                self.status_var.set(f"Downloading {i}/{total_videos}: {video.title}")

                if self.audio_only_var.get():
                    stream = video.streams.get_audio_only()
                else:
                    stream = video.streams.get_highest_resolution()

                stream.download(
                    output_path=self.download_folder,
                    filename=f"{i}. {video.title}"
                )
            except Exception as e:
                self.status_var.set(f"Error downloading {video.title}: {e}")

        self.status_var.set("Channel download complete!")
        self.show_widgets()

    def start_download_thread(self):
        self.current_angle = 0
        self.target_angle = 0
        download_thread = threading.Thread(target=self.download_content)
        download_thread.daemon = True
        download_thread.start()

    def animate_progress(self):
        if abs(self.current_angle - self.target_angle) > 0.1:
            self.current_angle += (self.target_angle - self.current_angle) / self.animation_speed

            self.canvas.delete("progress")
            self.progress_circle = self.canvas.create_arc(
                50, 50, 150, 150,
                start=90, extent=-self.current_angle,
                outline="#2196F3", width=10,
                style="arc", tags="progress"
            )

            self.root.after(16, self.animate_progress)

    def hide_widgets(self):
        for widget in self.widgets:
            widget.grid_remove()
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20)
        self.percentage_label.grid(row=2, column=0, columnspan=2)
        self.time_remaining_label.grid(row=3, column=0, columnspan=2)
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)

    def show_widgets(self):
        self.canvas.grid_remove()
        self.percentage_label.grid_remove()
        self.time_remaining_label.grid_remove()
        self.status_label.grid_remove()
        self.create_widgets()


    def select_folder(self):
        self.download_folder = filedialog.askdirectory()
        if self.download_folder:
            self.status_var.set(f"Destination folder: {self.download_folder}")

    def update_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        downloaded = total_size - bytes_remaining
        percentage = (downloaded / total_size) * 100
        self.percentage_var.set(f"{percentage:.1f}%")

        self.target_angle = 360 * (percentage / 100)

        if abs(self.current_angle - self.target_angle) > 0.1:
            self.root.after(16, self.animate_progress)

        elapsed_time = time.time() - self.download_start_time
        if percentage > 0:
            total_time = elapsed_time * 100 / percentage
            remaining_time = total_time - elapsed_time
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            self.time_remaining_var.set(f"Time remaining: {minutes}m {seconds}s")

def main():
    root = tk.Tk()
    app = App(root)
    app.create_widgets()
    root.mainloop()

if __name__ == "__main__":
    main()
