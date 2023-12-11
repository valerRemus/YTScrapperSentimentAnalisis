import tkinter as tk
import customtkinter as ctk
import threading
from web_srapper import yt_sentiment_analisis as ytsa
from tkinter import ttk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x200")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.url_input = ctk.CTkEntry(self)
        self.url_input.grid(row=0, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        self.progress = ctk.CTkProgressBar(self, orientation="horizontal", mode="indeterminate")
        self.progress.grid(row=1, column=0, columnspan=2, pady=5, padx=20, sticky="ew")

        self.button = ctk.CTkButton(self, text="Start", command=self.run_sentiment_analysis)
        self.button.grid(row=2, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        self.url_input.bind("<Button-3>", self.show_context_menu)

        # ... (otros códigos)

    def show_context_menu(self, event):
            # Crear un menú contextual
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Paste URL", command=self.paste_text)

            # Mostrar el menú en la posición del evento
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def paste_text(self):
            # Pegar texto desde el portapapeles en la entrada de texto
        text_to_paste = self.clipboard_get()
        self.url_input.insert(tk.INSERT, text_to_paste)

    def run_sentiment_analysis(self):
            self.progress.start()  # Start the progress bar

            scraper_thread = threading.Thread(target=self.perform_analysis)
            scraper_thread.start()

    def perform_analysis(self):
            ytsa_instance = ytsa()
            url = self.url_input.get()# Get the URL from the Entry widget

            print('Leyendo comentarios...')
            ytsa_instance.scrapper(url)

            print('Traduciendo...')
            ytsa_instance.traductor('comments.csv')

            print('Analizando emociones...')
            ytsa_instance.sentiment_detection('translated.csv')

            print('Mostrando grafico...')
            ytsa_instance.grafico('sentiments.csv')  # Call the grafico method with the CSV file


            self.progress.stop()  # Stop the progress bar after processing

    """def run_sentiment_analysis(self):
        self.progress.start()  # Start the progress bar

        scraper_thread = threading.Thread(target=self.perform_scrapper(), args=(url,))
        scraper_thread.start()

        self.after(100, self.perform_scrapper)  # Queue scrapper operation after 100ms

    def perform_scrapper(self):
        ytsa_instance = ytsa()
        url = self.url_input.get()  # Get the URL from the Entry widget
        ytsa_instance.scrapper(url)
        self.after(100, self.perform_traductor)  # Queue traductor operation after 100ms

    def perform_traductor(self):
        ytsa_instance = ytsa()
        ytsa_instance.traductor('comments.csv')
        self.after(100, self.perform_sentiment_detection)  # Queue sentiment detection after 100ms

    def perform_sentiment_detection(self):
        ytsa_instance = ytsa()
        ytsa_instance.sentiment_detection('translated.csv')
        self.after(100, self.perform_grafico)  # Queue grafico operation after 100ms

    def perform_grafico(self):
        ytsa_instance = ytsa()
        ytsa_instance.grafico('sentiments.csv')  # Call the grafico method with the CSV file
        self.progress.stop()  # Stop the progress bar after processing"""

app = App()
app.mainloop()
