# iuse

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey.svg?logo=linux&logoColor=white)](#)
[![Dependencies](https://img.shields.io/badge/dependencies-none-success.svg)](#)
[![Distros](https://img.shields.io/badge/distros-432-orange.svg)](#)
[![DE / WM](https://img.shields.io/badge/DE%20%2F%20WM-72-purple.svg)](#)

> `I USE <DISTRO> BTW` — flex your Linux distro (or desktop) right in the terminal. Made for r/unixporn.

`iuse` is a tiny, dependency-free CLI that prints a big ASCII-art banner like **`I USE ARCH BTW`** in the color of your choice. It ships with **432 distributions** and **72 desktop environments / window managers**, an interactive search menu, and automatic Russian/English localization.

## ✨ Features

- 🎨 **ASCII-art banners** in three sizes (`small`, `big`, `mini`).
- 🔍 **Interactive menu**: pick *Distro* or *DE/WM* → search → pick a color.
- 📦 **432 distros** and **72 DEs/WMs** built in.
- 🌈 **12 preset colors** + custom `#RRGGBB` / `0–255` ANSI.
- 🌍 **Auto localization** — Russian UI for `ru`/`uk` system locales, English everywhere else.
- 🪶 **Zero dependencies** — pure Python 3 standard library.

## 📥 Installation

```bash
# Grab the script
curl -O https://raw.githubusercontent.com/wetair1/iuse/main/iuse.py
chmod +x iuse.py

# Optional: install system-wide
sudo mv iuse.py /usr/local/bin/iuse
# ...or just for your user
mv iuse.py ~/.local/bin/iuse
```

Requires **Python 3.8+** (the interactive menu needs the standard `curses` module, available on Linux/macOS by default).

## 🚀 Usage

```bash
# Interactive menu (Distro/DE → search → color)
iuse

# Print a specific distro
iuse arch

# A random distro
iuse -r

# A desktop environment / window manager
iuse -d kde
iuse -d hyprland

# Pick a color (name, ANSI 0–255 or HEX)
iuse arch -c red
iuse arch -c 196
iuse arch -c "#ff8800"

# Banner size
iuse arch -b big

# List everything
iuse -l          # all distributions
iuse --list-de   # all DEs and WMs

# Disable color
iuse arch --no-color
```

## ⚙️ Options

| Flag | Description |
| --- | --- |
| `distro` | Distro name to print (see `-l`) |
| `-r`, `--random` | Print a random distro |
| `-l`, `--list` | List all distributions |
| `-d`, `--de DE` | Print a DE/WM instead of a distro |
| `--list-de` | List all DEs and WMs |
| `-c`, `--color COLOR` | Color: name (`red`…), ANSI code `0–255`, or `#RRGGBB` |
| `-b`, `--banner {small,big,mini}` | Banner font size (default: `small`) |
| `--no-color` | Disable colored output |
| `-h`, `--help` | Show help |

## 🎨 Preset colors

`red` · `orange` · `yellow` · `green` · `lime` · `cyan` · `blue` · `navy` · `purple` · `pink` · `white` · `gray`

…plus any custom `#RRGGBB` or ANSI `0–255` value.

## 🌍 Localization

The interface language is detected automatically from your environment (`LC_ALL`, `LC_MESSAGES`, `LANG`, `LANGUAGE`):

- Locale starts with `ru` or `uk` → **Russian** UI.
- Anything else → **English** UI.

The banner text itself (`I USE ... BTW`) always stays in English — that's the whole point of the meme. 🙂

## 🤝 Contributing

Found a missing distro or DE? PRs are welcome — add it to the corresponding dictionary in `iuse.py` and open a pull request.

## 📄 License

MIT — do whatever you want.

---

<details>
<summary>🇷🇺 Русский</summary>

<br>

`iuse` — крошечная CLI-утилита без зависимостей, которая выводит большой ASCII-баннер вроде **`I USE ARCH BTW`** в выбранном цвете. Прямо для r/unixporn. В комплекте **432 дистрибутива** и **72 окружения рабочего стола / оконных менеджера**, интерактивное меню с поиском и автоматическая локализация (русский/английский).

### ✨ Возможности

- 🎨 **ASCII-баннеры** трёх размеров (`small`, `big`, `mini`).
- 🔍 **Интерактивное меню**: выбор *Дистрибутив* или *DE/WM* → поиск → выбор цвета.
- 📦 **432 дистрибутива** и **72 DE/WM** прямо из коробки.
- 🌈 **12 готовых цветов** + свой `#RRGGBB` / ANSI `0–255`.
- 🌍 **Автолокализация** — русский интерфейс для систем с локалью `ru`/`uk`, английский для остальных.
- 🪶 **Без зависимостей** — только стандартная библиотека Python 3.

### 📥 Установка

```bash
# Скачать скрипт
curl -O https://raw.githubusercontent.com/wetair1/iuse/main/iuse.py
chmod +x iuse.py

# Опционально: установить для всей системы
sudo mv iuse.py /usr/local/bin/iuse
# ...или только для своего пользователя
mv iuse.py ~/.local/bin/iuse
```

Нужен **Python 3.8+** (для интерактивного меню требуется стандартный модуль `curses`, он есть в Linux/macOS по умолчанию).

### 🚀 Использование

```bash
# Интерактивное меню (Дистрибутив/DE → поиск → цвет)
iuse

# Конкретный дистрибутив
iuse arch

# Случайный дистрибутив
iuse -r

# Окружение рабочего стола / оконный менеджер
iuse -d kde
iuse -d hyprland

# Выбрать цвет (имя, ANSI 0–255 или HEX)
iuse arch -c red
iuse arch -c 196
iuse arch -c "#ff8800"

# Размер баннера
iuse arch -b big

# Показать списки
iuse -l          # все дистрибутивы
iuse --list-de   # все DE и WM

# Отключить цвет
iuse arch --no-color
```

### ⚙️ Опции

| Флаг | Описание |
| --- | --- |
| `distro` | Имя дистрибутива для вывода (см. `-l`) |
| `-r`, `--random` | Случайный дистрибутив |
| `-l`, `--list` | Показать все дистрибутивы |
| `-d`, `--de DE` | Вывести DE/WM вместо дистрибутива |
| `--list-de` | Показать все DE и WM |
| `-c`, `--color COLOR` | Цвет: имя (`red`…), код ANSI `0–255` или `#RRGGBB` |
| `-b`, `--banner {small,big,mini}` | Размер шрифта баннера (по умолчанию: `small`) |
| `--no-color` | Отключить цветной вывод |
| `-h`, `--help` | Показать справку |

### 🌍 Локализация

Язык интерфейса определяется автоматически по переменным окружения (`LC_ALL`, `LC_MESSAGES`, `LANG`, `LANGUAGE`):

- Локаль начинается с `ru` или `uk` → **русский** интерфейс.
- Всё остальное → **английский** интерфейс.

Сам текст баннера (`I USE ... BTW`) всегда остаётся на английском — в этом и весь смысл мема. 🙂

### 🤝 Участие в разработке

Не хватает какого-то дистрибутива или DE? PR приветствуются — добавь его в соответствующий словарь в `iuse.py` и открой pull request.

### 📄 Лицензия

MIT — делай что хочешь.

</details>
