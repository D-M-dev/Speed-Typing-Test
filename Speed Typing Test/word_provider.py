import random

class WordProvider:
    SHORT_WORDS = [
        "auto", "pes", "dům", "měsíc", "kód", "hra", "den", "rok", "čas", "mrak",
        "strom", "list", "modrý", "malý", "velký", "ráno", "noc", "vlak", "bota"
    ]
    LONG_WORDS = [
        "programování", "elektronika", "příležitost", "zodpovědnost", "překvapení",
        "matematika", "technologie", "inteligence", "komunikace", "knihovna",
        "představivost", "přátelství", "nepravděpodobný", "informace", "domluvený"
    ]

    @staticmethod
    def get_words(difficulty, count):
        if "krátká" in difficulty.lower():
            base = WordProvider.SHORT_WORDS
        elif "dlouhá" in difficulty.lower():
            base = WordProvider.LONG_WORDS
        else:
            base = WordProvider.SHORT_WORDS + WordProvider.LONG_WORDS
        return [random.choice(base) for _ in range(count)]