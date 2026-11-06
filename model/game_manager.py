from typing import List
from model.herni_plocha import HerniPlocha
from model.revizor import RevizorTahu
from model.Hrac import Hrac
from model.Timer import Timer
from model.Logger import GameLogger
from model.Umanager import Uzivatel
from model.tah import Tah
from model.questy import Quest


class GameManager:
    def __init__(self, limit_minut: int = 10):
        self.plocha = HerniPlocha()
        self.revizor_tahu = RevizorTahu(self.plocha)
        self.aktivni_hrac = 1
        self.hraci: List[Hrac] = []
        self.aktualni_tah = None
        self.casovac = Timer(limit_minut)
        self.game_logger = GameLogger()
        self.aktualni_quest = None
        self.cekajici_tah = None
        self.vybrane_pole = None

    def zkus_vybrat_pole(self, souradnice: tuple) -> dict:
        """
        Zpracuje kliknutí na hrací plochu a vrátí slovník s instrukcemi pro Controller.
        Vrací např.: {"akce": "oznac", "souradnice": (x,y)}, {"akce": "quest", "zadani": "5+5"}, nebo {"akce": "konec_vyberu"}
        """
        if self.cekajici_tah is not None:
            return {"akce": "nic"}  # Čeká se na quest

        obsah = self.plocha.vrat_obsah(souradnice)

        # 1. Výběr vlastní figurky
        if self.vybrane_pole is None:
            if obsah and self.je_vlastni_figurka(souradnice):
                self.vybrane_pole = souradnice
                return {"akce": "oznac", "souradnice": souradnice}
            return {"akce": "nic"}

        # 2. Pokus o tah vybranou figurkou
        start_x, start_y = self.vybrane_pole
        figurka = self.plocha.vrat_obsah((start_x, start_y))
        tah = Tah((start_x, start_y), souradnice, figurka)

        vysledek = {"akce": "konec_vyberu"}

        if self.revizor_tahu.simulate_Move(tah):
            cilova_fig = self.plocha.vrat_obsah(souradnice)

            # Útok = spuštění questu
            if cilova_fig is not None:
                self.cekajici_tah = tah
                self.aktualni_quest = Quest()
                vysledek = {"akce": "quest", "zadani": self.aktualni_quest.zadani}
            # Běžný přesun bez boje
            else:
                self._proved_fyzicky_tah(tah)
                vysledek = {"akce": "tah_proveden"}

        self.vybrane_pole = None
        return vysledek

    def over_odpoved_questu(self, odpoved: str) -> bool:
        """Zpracuje odpověď na quest. Vrací True (úspěch) nebo False (neúspěch)."""
        if not self.aktualni_quest:
            return False

        uspech = self.aktualni_quest.over_odpoved(odpoved)

        if uspech:
            self._proved_fyzicky_tah(self.cekajici_tah)
        else:
            # Tah se ruší, ale mění se hráč (stejně jako v původním kódu)
            self.aktivni_hrac *= -1

        self.cekajici_tah = None
        self.aktualni_quest = None
        return uspech

    def _proved_fyzicky_tah(self, tah):
        """Pomocná interní metoda pro fyzické provedení tahu a změnu hráče."""
        self.plocha.posun_figurky(tah)
        self.aktivni_hrac *= -1

    def zkontroluj_stav_hry(self) -> str:
        """Vrátí aktuální stav hry pro zobrazení hlášek (šach, mat, pat, hraje_se)."""
        if self.revizor_tahu.check_Mat(self.aktivni_hrac):
            return "mat"
        elif self.revizor_tahu.check_Pat(self.aktivni_hrac):
            return "pat"
        elif self.revizor_tahu.je_sach(self.aktivni_hrac):
            return "sach"
        return "hraje_se"

    def zacni_tah(self) -> Tah:
        return None

    def mozne_tahy(self) -> List[Tah]:
        return []

    def zrus_tah(self):
        pass

    def uloz_log(self):
        pass

    def get_stav(self) -> int:
        return 0

    def najdi_uzivatele(self, id_uzivatele: int) -> Uzivatel:
        return None

    def je_vlastni_figurka(self, souradnice: tuple) -> bool:
        fig = self.plocha.vrat_obsah(souradnice)
        return fig is not None and fig.barva == self.aktivni_hrac