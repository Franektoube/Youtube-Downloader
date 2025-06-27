import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp

def download(links, output_format):
    yt_dlp_options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
    }

    if output_format in ['mp3', 'wav']:
        yt_dlp_options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }]
    elif output_format in ['mp4', 'avi']:
        yt_dlp_options['format'] = 'bestvideo+bestaudio[ext=mp4]/best'
        yt_dlp_options['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': output_format,
        }]

    with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
        for video in links:
            ydl.download([video])

def read_file(file_path):
    with open(file_path, 'r') as file:
        links = file.readlines()
    return [link.strip() for link in links if link.strip()]

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Pliki tekstowe", "*.txt")])
    if not file_path:
        return
    links = read_file(file_path)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, "\n".join(links))

def run():
    output_format = format_var.get()
    if not output_format:
        messagebox.showerror("Błąd", "Proszę wybrać format wyjściowy.")
        return

    links = text_box.get("1.0", tk.END).strip().split('\n')
    links = [link for link in links if link]

    if not links:
        messagebox.showerror("Błąd", "Proszę podać linki.")
        return

    download(links, output_format)

def main():
    root = tk.Tk()
    root.title("Video Downloader")

    global format_var
    format_var = tk.StringVar()

    tk.Label(root, text="Links To video (one per line):",font=("Arial", 11, "bold")).pack(pady=5)

    global text_box
    text_box = tk.Text(root, height=10, width=50)
    text_box.pack()

    tk.Button(root, text="Read From File", command=open_file, font=("Arial", 11, "bold")).pack(pady=10)

    tk.Label(root, text="Chose format:", font=("Arial", 11, "bold")).pack(pady=0)

    formats = ["mp3", "mp4", "avi", "wav"]
    for format in formats:
        tk.Radiobutton(root, text=format, variable=format_var, value=format, font=("Arial", 8, "bold")).pack(anchor=tk.W, padx=10)

    tk.Button(root, text="Pobierz", command=run).pack()

    root.mainloop()

if __name__ == "__main__":
    main()

