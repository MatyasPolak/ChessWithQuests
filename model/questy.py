import random

class Quest:
    OTAZKY = [
        ("5 * 6 = ?", "30"),
        ("12 + 15 = ?", "27"),
        ("100 / 4 = ?", "25"),
        ("8 * 7 = ?", "56"),
        ("50 - 17 = ?", "33"),
        ("Hlavní město Francie?", "paříž"),
        ("Nejdelší řeka světa (na N)?", "nil"),
        ("Na jakém kontinentu leží Brazílie?", "jižní amerika"),
        ("Hlavní město Japonska?", "tokio"),
        ("S jakým státem sousedí ČR na jihu?", "rakousko"),
        ("Kolik nohou má pavouk?", "8"),
        ("Jaká planeta je nejblíže Slunci?", "merkur"),
        ("Kdo napsal Romea a Julii?", "shakespeare"),
        ("Chemická značka pro kyslík?", "o"),
        ("Bod varu vody ve °C?", "100")
    ]

    def __init__(self):
        self.nazev = "Vědomostní Quest"
        # Náhodně vybere otázku ze seznamu výše
        otazka, vysledek = random.choice(self.OTAZKY)
        self.zadani = otazka
        self.spravny_vysledek = str(vysledek).lower()

    def over_odpoved(self, odpoved: str) -> bool:
        # Ořízne mezery a porovná odpověď (nezáleží na velkých/malých písmenech)
        return odpoved.strip().lower() == self.spravny_vysledek