# whois-julius – Terminal-Based Developer Portfolio

```
██╗    ██╗██╗  ██╗ ██████╗ ██╗███████╗         ██╗██╗   ██╗██╗     ██╗██╗   ██╗███████╗
██║    ██║██║  ██║██╔═══██╗██║██╔════╝         ██║██║   ██║██║     ██║██║   ██║██╔════╝
██║ █╗ ██║███████║██║   ██║██║███████╗         ██║██║   ██║██║     ██║██║   ██║███████╗
██║███╗██║██╔══██║██║   ██║██║╚════██║    ██   ██║██║   ██║██║     ██║██║   ██║╚════██║
╚███╔███╔╝██║  ██║╚██████╔╝██║███████║    ╚█████╔╝╚██████╔╝███████╗██║╚██████╔╝███████║
 ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝     ╚════╝  ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚══════╝
```

> Ein interaktives CLI-Portfolio, das wie ein minimalistisches Terminal-Betriebssystem funktioniert.

## 🚀 Features

- **Interaktive Terminal-Erfahrung** – Vollständig steuerbar über Tastaturbefehle
- **Retro-inspiriertes Design** – ASCII-Art und Matrix-Effekte
- **Portfolio-Showcase** – Projekte, CV und Kontaktdaten im Terminal-Stil
- **Mini-Games** – Snake und Matrix-Rain für den Extra-Nerd-Faktor
- **Cross-Platform** – Läuft in VS Code, Bash, Zsh und anderen Terminals

## 📦 Installation

```bash
# Repository klonen
git clone https://github.com/juliusduden/whois-julius.git
cd whois-julius

# Ausführbar machen und starten
chmod +x run.sh
./run.sh
```

## 💻 Verfügbare Befehle

```
> help            # Zeigt alle verfügbaren Befehle
> cv              # Gibt den Lebenslauf aus
> projects        # Zeigt Portfolio-Projekte
> contact         # Gibt Kontaktmöglichkeiten zurück
> quote           # Zufälliges Tech-Zitat
> asciiart        # Zeigt cooles ASCII-Art
> snake           # Startet Snake-Game
> matrix          # Startet Matrix-Rain
> clear           # Leert das Terminal
> exit            # Beendet die App
```

## 🛠 Tech Stack

- **Python 3.11** – Hauptlogik & Datenhandling
- **Bash** – Launch & Wrapper-Scripts
- **ANSI Escape Codes** – Farbe & Formatierung
- **JSON** – Strukturierte Datenspeicherung

## 📂 Projektstruktur

```
whois-julius/
├── run.sh                  # Bash-Starter
├── core/                   # Hauptlogik (Python)
│   ├── main.py            # Entry Point
│   ├── commands.py        # Command-Dispatcher
│   ├── ascii.py           # ASCII-Kunst
│   └── utils.py           # Terminal-Tools
├── data/                   # Inhalte
│   ├── cv.txt             # Lebenslauf
│   ├── projects.json      # Portfolio-Projekte
│   ├── contact.json       # Kontaktdaten
│   └── quotes.txt         # Tech-Zitate
├── games/                  # Mini-Games
│   ├── snake.py           # Snake-Game
│   └── matrix.py          # Matrix-Rain
├── requirements.txt        # Dependencies
└── README.md              # Diese Datei
```

## 🎯 Zielgruppe

Tech-affine Personaler, Entwickler und Recruiter, die eine kreative und technisch versierte Präsentation schätzen.

## 📝 Lizenz

MIT License - siehe LICENSE für Details

## 👨‍💻 Autor

**Julius Duden**  
IT-Consultant & Developer @ Cedima

---

*"Talk is cheap. Show me the code." – Linus Torvalds*

