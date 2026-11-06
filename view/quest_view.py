import tkinter as tk


class QuestView(tk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent, bg="#111111", bd=2, relief="ridge")
        self.callback = callback

        # Titulek
        self.lbl_titulek = tk.Label(self, text="Boj o figurku!", bg="#111111", fg="#555555", font=("Arial", 12, "bold"))
        self.lbl_titulek.pack(pady=5)

        # Otázka
        self.lbl_otazka = tk.Label(self, text="Čekání na útok...", bg="#111111", fg="gray", font=("Arial", 14), wraplength=200)
        self.lbl_otazka.pack(pady=5)

        # Vstupní pole (ve výchozím stavu vypnuté)
        self.entry_odpoved = tk.Entry(self, font=("Arial", 14), width=10, state="disabled")
        self.entry_odpoved.pack(pady=5)

        # Tlačítko (ve výchozím stavu vypnuté)
        self.btn_potvrdit = tk.Button(self, text="Potvrdit", state="disabled", command=self.odeslat)
        self.btn_potvrdit.pack(pady=5)

    def zobraz_quest(self, otazka):
        # Aktivuje se panel s questem
        self.lbl_titulek.config(fg="#f6f669")
        self.lbl_otazka.config(text=f"Kolik je {otazka}?", fg="white")
        self.entry_odpoved.config(state="normal")
        self.entry_odpoved.delete(0, tk.END)
        self.btn_potvrdit.config(state="normal")

    def skryj(self):
        # Zašedne a vypne se panel
        self.lbl_titulek.config(fg="#555555")
        self.lbl_otazka.config(text="Čekání na útok...", fg="gray")
        self.entry_odpoved.delete(0, tk.END)
        self.entry_odpoved.config(state="disabled")
        self.btn_potvrdit.config(state="disabled")

    def odeslat(self):
        self.callback(self.entry_odpoved.get())