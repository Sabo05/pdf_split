# Importa le librerie necessarie
import os  # Per operazioni sui file system
from PyPDF2 import PdfReader, PdfWriter  # Per manipolare PDF
import tkinter as tk  # Per la GUI
from tkinter import filedialog, ttk, messagebox  # Componenti GUI avanzati

class PDFSplitterGUI:
    def __init__(self, master):
        # Inizializza la finestra principale
        self.master = master
        master.title("PDF Splitter")  # Titolo applicazione
        master.geometry("500x300")  # Dimensioni finestra

        # Variabili di stato per memorizzare:
        self.pdf_path = tk.StringVar()  # Percorso del PDF selezionato
        self.output_dir = tk.StringVar(value=os.path.join(
            os.path.expanduser('~'), 'Desktop'))  # Cartella output predefinita (Desktop)
        self.split_page = tk.StringVar()  # Pagina di divisione

        # Crea i componenti grafici
        self.create_widgets()

    def create_widgets(self):
        # Frame principale con padding
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sezione selezione file PDF
        ttk.Label(main_frame, text="File PDF:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.pdf_path, width=40, state='readonly').grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Sfoglia...", command=self.select_pdf).grid(row=0, column=2)

        # Sezione inserimento pagina di split
        ttk.Label(main_frame, text="Dividi alla pagina:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.page_entry = ttk.Entry(main_frame, textvariable=self.split_page, width=10)
        self.page_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
        # Validazione input: solo numeri
        self.page_entry.configure(validate='key', validatecommand=(self.page_entry.register(self.validate_page), '%P'))

        # Sezione selezione cartella output
        ttk.Label(main_frame, text="Salva in:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=40, state='readonly').grid(row=2, column=1, padx=5)
        ttk.Button(main_frame, text="Scegli...", command=self.select_output_dir).grid(row=2, column=2)

        # Pulsante per avviare la divisione
        ttk.Button(main_frame, text="Dividi PDF", command=self.split_pdf).grid(row=3, column=1, pady=20)

        # Etichetta per messaggi di stato/errori
        self.status_label = ttk.Label(main_frame, text="", foreground='red')
        self.status_label.grid(row=4, column=0, columnspan=3)

    def validate_page(self, new_text):
        # Permette solo input numerici o campo vuoto
        return new_text.isdigit() or new_text == ''

    def select_pdf(self):
        # Apre dialog per selezione file PDF
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_path.set(file_path)
            self.clear_status()

    def select_output_dir(self):
        # Apre dialog per selezione cartella
        dir_path = filedialog.askdirectory(initialdir=self.output_dir.get())
        if dir_path:
            self.output_dir.set(dir_path)
            self.clear_status()

    def clear_status(self):
        # Resetta i messaggi di errore
        self.status_label.config(text="")

    def split_pdf(self):
        self.clear_status()
        # Recupera i valori dall'interfaccia
        file_path = self.pdf_path.get()
        split_page = self.split_page.get()
        output_dir = self.output_dir.get()

        # Validazioni input
        if not file_path:
            self.show_error("Seleziona un file PDF!")
            return
        if not split_page:
            self.show_error("Inserisci il numero di pagina!")
            return

        try:
            split_page = int(split_page)
        except ValueError:
            self.show_error("Numero di pagina non valido!")
            return

        try:
            # Apre il file PDF
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                total_pages = len(reader.pages)

                # Controlla validità pagina di split
                if split_page < 1 or split_page >= total_pages:
                    self.show_error(f"Pagina deve essere tra 1 e {total_pages - 1}")
                    return

                # Crea due nuovi PDF
                writer1 = PdfWriter()
                writer2 = PdfWriter()

                # Divide le pagine
                for i in range(split_page):
                    writer1.add_page(reader.pages[i])
                for i in range(split_page, total_pages):
                    writer2.add_page(reader.pages[i])

                # Genera i nomi dei file
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path1 = os.path.join(output_dir, f"{base_name}_part1.pdf")
                output_path2 = os.path.join(output_dir, f"{base_name}_part2.pdf")

                # Salva i file
                with open(output_path1, 'wb') as out_file:
                    writer1.write(out_file)
                with open(output_path2, 'wb') as out_file:
                    writer2.write(out_file)

                # Messaggio di successo
                messagebox.showinfo("Successo", "Divisione file pdf Completa")

        except Exception as e:
            self.show_error(f"Errore durante l'elaborazione: {str(e)}")

    def show_error(self, message):
        # Mostra messaggi di errore
        self.status_label.config(text=message)

if __name__ == "__main__":
    # Avvia l'applicazione
    root = tk.Tk()
    app = PDFSplitterGUI(root)
    root.mainloop()