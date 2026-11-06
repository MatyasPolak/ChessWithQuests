import tkinter as tk
from tkinter import messagebox
from model.game_manager import GameManager
from view.game_view import GameView


class GameManagerController:
    def __init__(self, root: tk.Tk, app_controller, mod: str, cas_minuty: int):
        self.root = root
        self.app_controller = app_controller

        self.game_manager = GameManager(limit_minut=cas_minuty)
        self.timer = self.game_manager.casovac

        self.game_view = GameView(root, self)
        self.game_view.aktualizuj_plochu()

        self.odpocet_bezi = True
        self.aktualizuj_ui()
        self.odpocet_casu()

    def vyber_pole(self, x: int, y: int):
        # 1. Controller pošle stisknutou pozici do GameManageru (připomínka č. 2 splněna)
        odpoved = self.game_manager.zkus_vybrat_pole((x, y))

        # 2. Controller reaguje na výsledek (připomínka č. 1 splněna - logika je v Modelu)
        akce = odpoved.get("akce")

        if akce == "oznac":
            self.game_view.oznac_pole(*odpoved["souradnice"])
        elif akce == "quest":
            self.game_view.ukaz_quest(odpoved["zadani"])
        elif akce in ["konec_vyberu", "tah_proveden"]:
            self.game_view.aktualizuj_plochu()
            self.zkontroluj_konec_hry()
            self.aktualizuj_ui()

    def zkontroluj_quest(self, odpoved: str):
        # Zeptáme se modelu, zda je odpověď správná, on zařídí zbytek
        uspech = self.game_manager.over_odpoved_questu(odpoved)

        self.game_view.skryj_quest()
        self.game_view.aktualizuj_plochu()

        if uspech:
            self.zkontroluj_konec_hry()

        self.aktualizuj_ui()

    def zkontroluj_konec_hry(self):
        """Zkontroluje přes model stav hry a případně vyvolá okna."""
        stav = self.game_manager.zkontroluj_stav_hry()

        if stav == "mat":
            self.odpocet_bezi = False
            vitez = "Bílý" if self.game_manager.aktivni_hrac == -1 else "Černý"
            messagebox.showinfo("Konec hry", f"Šach mat! Vyhrál {vitez}.")
        elif stav == "pat":
            self.odpocet_bezi = False
            messagebox.showinfo("Konec hry", "Remíza! (Pat)")
        elif stav == "sach":
            messagebox.showwarning("Šach", "Tvůj král je v ohrožení (Šach)!")

    def odpocet_casu(self):
        if not self.odpocet_bezi:
            return

        if not self.timer.odecti_vterinu(self.game_manager.aktivni_hrac):
            self.odpocet_bezi = False
            vitez = "Bílý" if self.game_manager.aktivni_hrac == -1 else "Černý"
            messagebox.showinfo("Konec času", f"Vypršel čas! Vyhrál {vitez}.")
            return

        self.aktualizuj_ui()
        self.root.after(1000, self.odpocet_casu)

    def aktualizuj_ui(self):
        cas1 = self.timer.formatuj_cas(1)
        cas2 = self.timer.formatuj_cas(-1)
        vyhozene_b = " ".join([f.znak for f in self.game_manager.plocha.vyhozene_figurky_b])
        vyhozene_c = " ".join([f.znak for f in self.game_manager.plocha.vyhozene_figurky_c])
        self.game_view.aktualizuj_stav(cas1, cas2, vyhozene_c, vyhozene_b)