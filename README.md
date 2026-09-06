# Czytanie książek dla ADHD i innych

> **Minimalny czytnik plików TXT z tekstem-na-mowę**

Repozytorium zawiera pojedynczą aplikację Kivy. Użytkownik wybiera lokalny plik
`.txt`, aplikacja wczytuje jego zawartość i przekazuje zdania do `edge-tts`.
Domyślny głos w kodzie to `pl-PL-ZofiaNeural`.

## Funkcje potwierdzone w kodzie

- graficzny wybór plików ograniczony do `*.txt`;
- wczytywanie UTF-8 w osobnym wątku;
- przycisk odtwarzania/pauzy i prosta pozycja odczytu;
- generowanie plików MP3 w katalogu tymczasowym systemu;
- odtwarzanie przez `kivy.core.audio.SoundLoader`.

## Wymagania

- Python 3;
- Kivy;
- `edge-tts`;
- dostęp do usługi używanej przez `edge-tts` podczas generowania mowy.

## Instalacja i uruchomienie

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install kivy edge-tts
python book_reader.py
```

`setup_ios.sh` jest dodatkowym skryptem pomocniczym; przed użyciem na iOS
należy sprawdzić jego wymagania i ograniczenia platformy.

## Ograniczenia

To minimalny prototyp: obsługuje wyłącznie tekstowe pliki TXT, dzieli tekst
prostym rozdzieleniem po kropce i nie zapisuje trwałego postępu czy biblioteki.
Szybkość, jakość i dostępność mowy zależą od środowiska oraz usługi TTS.

## Prywatność

Tekst książki jest czytany lokalnie, lecz generowanie przez `edge-tts` może
wiązać się z wysłaniem tekstu do usługi TTS. Nie używaj materiałów poufnych
bez sprawdzenia aktualnych warunków tego dostawcy.

## Licencja

Brak pliku licencji w repozytorium.
