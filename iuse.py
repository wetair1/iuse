#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import random
import re
import sys
import shutil

__version__ = "0.3.0"


def detect_lang():
    for var in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        v = os.environ.get(var, "")
        if v:
            low = v.lower()
            if low.startswith("ru") or low.startswith("uk"):
                return "ru"
            return "en"
    return "en"


LANG = detect_lang()

STR = {
    "ru": {
        "mode_title": "iuse \u2014 что флексим?",
        "mode_hint": " \u2191\u2193 \u00b7 Enter \u2014 выбрать \u00b7 Esc \u2014 выход",
        "mode_distro": "Дистрибутив",
        "mode_de": "DE / WM (рабочее окружение)",
        "pick_title_distro": " iuse \u2014 шаг 2/3: выбери дистрибутив",
        "pick_title_de": " iuse \u2014 шаг 2/3: выбери DE / WM",
        "pick_hint": " Печатай для поиска \u00b7 \u2191\u2193 \u00b7 Enter \u2014 далее \u00b7 Esc \u2014 назад",
        "not_found": " Ничего не найдено. Измени запрос или Backspace.",
        "color_title": " iuse \u2014 шаг 3/3: цвет для %s",
        "color_hint": " \u2191\u2193 \u00b7 Enter \u2014 выбрать \u00b7 Esc \u2014 назад",
        "color_default": "По умолчанию (цвет %s)",
        "color_custom": "Свой цвет (HEX или 0\u2013255)\u2026",
        "color_gradient": "Градиент (несколько цветов)\u2026",
        "grad_count_title": " iuse \u2014 градиент: сколько цветов?",
        "grad_color_title": " iuse \u2014 градиент: цвет %d/%d",
        "grad_type_title": " iuse \u2014 тип градиента",
        "grad_type_horizontal": "Горизонтальный (\u2192)",
        "grad_type_vertical": "Вертикальный (\u2193)",
        "grad_type_diagonal": "Диагональный (\u2198)",
        "prompt_hint": " Цвет: #RRGGBB, RGB, код 0\u2013255 или имя (red/blue\u2026)",
        "prompt_keys": " Enter \u2014 ок \u00b7 Esc \u2014 отмена",
        "prompt_bad": "\u2717 неверно",
        "list_distros": "Поддерживаемые дистрибутивы:",
        "list_total_distros": "Всего: %d дистрибутивов.",
        "list_des": "Поддерживаемые DE и WM:",
        "list_total_des": "Всего: %d DE/WM.",
        "cancelled": "Отменено.",
        "not_in_base": "(\u00ab%s\u00bb нет в базе \u2014 напечатал как есть. Список: -l)",
        "not_in_base_de": "(\u00ab%s\u00bb нет в базе DE/WM \u2014 напечатал как есть. Список: --list-de)",
        "no_detect": "Не смог определить дистрибутив. Укажи явно: iuse.py arch",
        "curses_required": "Ошибка: нужен модуль curses (поставь python-curses или запускай с аргументами, например: iuse arch)",
        "bad_color": "Непонятный цвет \u00ab%s\u00bb. Примеры: red, 196, #ff8800",
        "bad_gradient": "Непонятный градиент \u00ab%s\u00bb. Нужно \u22652 цветов через запятую, напр.: red,blue или #f00,#00f",
        "exported": "Список сохранён: %s\nРедактируй этот файл и добавляй свои дистрибутивы/DE \u2014 iuse подхватит их автоматически.",
        "load_warn": "\u26a0 не смог загрузить %s: %s",
        "loaded_info": "Загружен пользовательский список: %s",
        "h_distro": "имя дистрибутива (см. -l)",
        "h_random": "случайный дистрибутив",
        "h_list": "показать все дистрибутивы",
        "h_color": "цвет: имя (red\u2026), код 0-255 или #RRGGBB",
        "h_gradient": "градиент: цвета через запятую, напр. red,blue или #f00,#00f",
        "h_gradient_type": "тип градиента: horizontal | vertical | diagonal",
        "h_banner": "размер шрифта",
        "h_de": "вывести DE/WM вместо дистрибутива: kde, gnome, hyprland, i3\u2026",
        "h_listde": "показать все DE и WM",
        "h_nocolor": "отключить цвет",
        "h_distros": "путь к своему файлу со списком (.json или .txt)",
        "h_export": "выгрузить список в файл (.json) и выйти (по умолчанию ~/.config/iuse/distros.json)",
        "desc": "I USE <DISTRO> BTW \u2014 флексим дистрибутивом.",
        "epilog": "Без аргументов: меню выбора, затем меню цвета (можно градиент). Список дистрибутивов хранится в distros.json \u2014 см. --export-distros.",
    },
    "en": {
        "mode_title": "iuse \u2014 what are you repping?",
        "mode_hint": " \u2191\u2193 \u00b7 Enter \u2014 select \u00b7 Esc \u2014 quit",
        "mode_distro": "Distribution",
        "mode_de": "DE / WM (desktop environment)",
        "pick_title_distro": " iuse \u2014 step 2/3: pick a distro",
        "pick_title_de": " iuse \u2014 step 2/3: pick a DE / WM",
        "pick_hint": " Type to search \u00b7 \u2191\u2193 \u00b7 Enter \u2014 next \u00b7 Esc \u2014 back",
        "not_found": " Nothing found. Change the query or Backspace.",
        "color_title": " iuse \u2014 step 3/3: color for %s",
        "color_hint": " \u2191\u2193 \u00b7 Enter \u2014 select \u00b7 Esc \u2014 back",
        "color_default": "Default (%s color)",
        "color_custom": "Custom color (HEX or 0\u2013255)\u2026",
        "color_gradient": "Gradient (multiple colors)\u2026",
        "grad_count_title": " iuse \u2014 gradient: how many colors?",
        "grad_color_title": " iuse \u2014 gradient: color %d/%d",
        "grad_type_title": " iuse \u2014 gradient type",
        "grad_type_horizontal": "Horizontal (\u2192)",
        "grad_type_vertical": "Vertical (\u2193)",
        "grad_type_diagonal": "Diagonal (\u2198)",
        "prompt_hint": " Color: #RRGGBB, RGB, code 0\u2013255 or name (red/blue\u2026)",
        "prompt_keys": " Enter \u2014 ok \u00b7 Esc \u2014 cancel",
        "prompt_bad": "\u2717 invalid",
        "list_distros": "Supported distributions:",
        "list_total_distros": "Total: %d distributions.",
        "list_des": "Supported DEs and WMs:",
        "list_total_des": "Total: %d DEs/WMs.",
        "cancelled": "Cancelled.",
        "not_in_base": "(\u00ab%s\u00bb not in the database \u2014 printed as is. List: -l)",
        "not_in_base_de": "(\u00ab%s\u00bb not in the DE/WM database \u2014 printed as is. List: --list-de)",
        "no_detect": "Couldn't detect the distro. Specify it: iuse.py arch",
        "curses_required": "Error: curses module required (install python-curses or run with arguments, e.g.: iuse arch)",
        "bad_color": "Unknown color \u00ab%s\u00bb. Examples: red, 196, #ff8800",
        "bad_gradient": "Unknown gradient \u00ab%s\u00bb. Need \u22652 comma-separated colors, e.g.: red,blue or #f00,#00f",
        "exported": "List saved: %s\nEdit this file and add your own distros/DEs \u2014 iuse will pick them up automatically.",
        "load_warn": "\u26a0 couldn't load %s: %s",
        "loaded_info": "Loaded custom list: %s",
        "h_distro": "distro name (see -l)",
        "h_random": "random distro",
        "h_list": "list all distributions",
        "h_color": "color: name (red\u2026), code 0-255 or #RRGGBB",
        "h_gradient": "gradient: comma-separated colors, e.g. red,blue or #f00,#00f",
        "h_gradient_type": "gradient type: horizontal | vertical | diagonal",
        "h_banner": "font size",
        "h_de": "print a DE/WM instead of a distro: kde, gnome, hyprland, i3\u2026",
        "h_listde": "list all DEs and WMs",
        "h_nocolor": "disable color",
        "h_distros": "path to your own list file (.json or .txt)",
        "h_export": "dump the list to a file (.json) and exit (default ~/.config/iuse/distros.json)",
        "desc": "I USE <DISTRO> BTW \u2014 rep your distro.",
        "epilog": "No arguments: selection menu, then color menu (gradient supported). The distro list lives in distros.json \u2014 see --export-distros.",
    },
}


def t(key):
    table = STR.get(LANG, STR["en"])
    if key in table:
        return table[key]
    return STR["en"].get(key, key)


BUILTIN_DISTROS = {
    "arch": ("Arch", 81),
    "artix": ("Artix", 33),
    "archbang": ("ArchBang", 81),
    "archcraft": ("Archcraft", 244),
    "archlabs": ("ArchLabs", 245),
    "arcolinux": ("ArcoLinux", 39),
    "xerolinux": ("XeroLinux", 39),
    "hefftor": ("HefftorLinux", 81),
    "bridge": ("Bridge", 81),
    "blackarch": ("BlackArch", 245),
    "rebornos": ("RebornOS", 129),
    "mabox": ("Mabox", 240),
    "manjaro": ("Manjaro", 41),
    "endeavouros": ("EndeavourOS", 129),
    "antergos": ("Antergos", 39),
    "garuda": ("Garuda", 203),
    "cachyos": ("CachyOS", 81),
    "crystal": ("Crystal", 141),
    "blendos": ("BlendOS", 81),
    "chakra": ("Chakra", 39),
    "snigdha": ("Snigdha", 81),
    "instantos": ("instantOS", 39),
    "obarun": ("Obarun", 33),
    "parabola": ("Parabola", 129),
    "hyperbola": ("Hyperbola", 93),
    "debian": ("Debian", 197),
    "devuan": ("Devuan", 93),
    "siduction": ("Siduction", 33),
    "neptune": ("Neptune", 39),
    "grml": ("Grml", 46),
    "kanotix": ("Kanotix", 33),
    "pardus": ("Pardus", 46),
    "astra": ("Astra", 39),
    "ubuntu": ("Ubuntu", 208),
    "kubuntu": ("Kubuntu", 39),
    "xubuntu": ("Xubuntu", 33),
    "lubuntu": ("Lubuntu", 27),
    "ubuntumate": ("Ubuntu MATE", 118),
    "ubuntubudgie": ("Ubuntu Budgie", 214),
    "ubuntustudio": ("Ubuntu Studio", 196),
    "ubuntutouch": ("Ubuntu Touch", 208),
    "lmde": ("LMDE", 77),
    "pop": ("Pop!_OS", 44),
    "mint": ("Mint", 77),
    "elementary": ("elementary", 45),
    "zorin": ("Zorin", 39),
    "feren": ("Feren", 39),
    "linuxlite": ("Linux Lite", 250),
    "peppermint": ("Peppermint", 203),
    "bodhi": ("Bodhi", 118),
    "netrunner": ("Netrunner", 39),
    "tuxedo": ("TUXEDO OS", 39),
    "rhino": ("Rhino", 202),
    "pinguy": ("Pinguy", 208),
    "emmabuntus": ("Emmabuntus", 214),
    "linspire": ("Linspire", 39),
    "freespire": ("Freespire", 45),
    "mx": ("MX", 255),
    "antix": ("antiX", 244),
    "sparky": ("Sparky", 214),
    "bunsenlabs": ("BunsenLabs", 240),
    "q4os": ("Q4OS", 33),
    "kali": ("Kali", 27),
    "parrot": ("Parrot", 50),
    "backbox": ("BackBox", 46),
    "pentoo": ("Pentoo", 135),
    "athena": ("Athena", 196),
    "kodachi": ("Kodachi", 245),
    "whonix": ("Whonix", 240),
    "tails": ("Tails", 99),
    "qubes": ("Qubes", 33),
    "wifislax": ("Wifislax", 46),
    "caine": ("CAINE", 244),
    "nst": ("NST", 46),
    "fedora": ("Fedora", 33),
    "nobara": ("Nobara", 39),
    "silverblue": ("Silverblue", 33),
    "kinoite": ("Kinoite", 39),
    "sericea": ("Sericea", 45),
    "bluefin": ("Bluefin", 39),
    "aurora": ("Aurora", 141),
    "bazzite": ("Bazzite", 135),
    "ultramarine": ("Ultramarine", 27),
    "risios": ("RisiOS", 203),
    "korora": ("Korora", 33),
    "chapeau": ("Chapeau", 33),
    "rhel": ("RHEL", 196),
    "centos": ("CentOS", 99),
    "rocky": ("Rocky", 35),
    "alma": ("Alma", 202),
    "oracle": ("Oracle", 196),
    "amazon": ("Amazon Linux", 214),
    "scientific": ("Scientific", 33),
    "springdale": ("Springdale", 35),
    "photon": ("Photon", 45),
    "eurolinux": ("EuroLinux", 33),
    "miraclelinux": ("MIRACLE", 196),
    "circle": ("Circle", 196),
    "opensuse": ("openSUSE", 70),
    "tumbleweed": ("Tumbleweed", 106),
    "suse": ("SUSE", 70),
    "regata": ("Regata", 33),
    "gecko": ("GeckoLinux", 70),
    "gentoo": ("Gentoo", 141),
    "funtoo": ("Funtoo", 135),
    "calculate": ("Calculate", 141),
    "redcore": ("Redcore", 196),
    "exherbo": ("Exherbo", 129),
    "sourcemage": ("Source Mage", 46),
    "lunar": ("Lunar", 129),
    "slackware": ("Slackware", 63),
    "salix": ("Salix", 118),
    "slackel": ("Slackel", 63),
    "zenwalk": ("Zenwalk", 63),
    "absolute": ("Absolute", 63),
    "vector": ("VectorLinux", 33),
    "void": ("Void", 41),
    "chimera": ("Chimera", 45),
    "serpent": ("Serpent", 46),
    "venom": ("Venom", 46),
    "nixos": ("NixOS", 39),
    "guix": ("Guix", 214),
    "nutyx": ("NuTyX", 39),
    "alpine": ("Alpine", 27),
    "clear": ("Clear", 45),
    "solus": ("Solus", 39),
    "pclinuxos": ("PCLinuxOS", 33),
    "mageia": ("Mageia", 45),
    "openmandriva": ("OpenMandriva", 33),
    "mandriva": ("Mandriva", 45),
    "rosa": ("ROSA", 39),
    "deepin": ("Deepin", 39),
    "kaos": ("KaOS", 45),
    "nitrux": ("Nitrux", 39),
    "kdeneon": ("KDE neon", 39),
    "regolith": ("Regolith", 202),
    "biglinux": ("BigLinux", 41),
    "frugalware": ("Frugalware", 33),
    "kwort": ("Kwort", 46),
    "nutos": ("NutOS", 39),
    "altlinux": ("ALT Linux", 196),
    "openkylin": ("openKylin", 39),
    "kylin": ("Kylin", 196),
    "puppy": ("Puppy", 226),
    "fatdog": ("Fatdog64", 226),
    "quirky": ("Quirky", 226),
    "easyos": ("EasyOS", 226),
    "macpup": ("Macpup", 226),
    "tinycore": ("Tiny Core", 250),
    "dsl": ("Damn Small", 250),
    "knoppix": ("Knoppix", 33),
    "slax": ("Slax", 39),
    "slitaz": ("SliTaz", 214),
    "porteus": ("Porteus", 27),
    "austrumi": ("AUSTRUMI", 214),
    "wattos": ("wattOS", 118),
    "4mlinux": ("4MLinux", 214),
    "systemrescue": ("SystemRescue", 196),
    "finnix": ("Finnix", 244),
    "clonezilla": ("Clonezilla", 214),
    "gparted": ("GParted Live", 240),
    "rescuezilla": ("Rescuezilla", 39),
    "gobolinux": ("GoboLinux", 118),
    "sabayon": ("Sabayon", 240),
    "pisi": ("Pisi", 214),
    "trisquel": ("Trisquel", 118),
    "uruk": ("Uruk", 118),
    "dragora": ("Dragora", 118),
    "ututo": ("Ututo", 46),
    "pureos": ("PureOS", 45),
    "crux": ("CRUX", 244),
    "kiss": ("KISS", 250),
    "carbs": ("Carbs", 244),
    "t2": ("T2", 244),
    "lfs": ("LFS", 250),
    "asahi": ("Asahi", 203),
    "spiral": ("SpiralLinux", 46),
    "kaisen": ("Kaisen", 33),
    "drauger": ("Drauger", 39),
    "freebsd": ("FreeBSD", 196),
    "openbsd": ("OpenBSD", 227),
    "netbsd": ("NetBSD", 208),
    "ghostbsd": ("GhostBSD", 240),
    "dragonfly": ("DragonFly", 203),
    "haiku": ("Haiku", 46),
    "serenityos": ("SerenityOS", 39),
    "vanilla": ("Vanilla", 214),
    "mobian": ("Mobian", 197),
    "postmarketos": ("postmarketOS", 118),
    "steamos": ("SteamOS", 33),
    "holoiso": ("HoloISO", 33),
    "batocera": ("Batocera", 214),
    "lakka": ("Lakka", 129),
    "recalbox": ("Recalbox", 46),
    "retropie": ("RetroPie", 196),
    "libreelec": ("LibreELEC", 46),
    "osmc": ("OSMC", 39),
    "volumio": ("Volumio", 39),
    "dietpi": ("DietPi", 118),
    "armbian": ("Armbian", 196),
    "raspbian": ("Raspberry Pi", 197),
    "proxmox": ("Proxmox", 202),
    "truenas": ("TrueNAS", 39),
    "unraid": ("Unraid", 202),
    "openwrt": ("OpenWrt", 27),
    "pfsense": ("pfSense", 203),
    "opnsense": ("OPNsense", 202),
    "endless": ("Endless", 33),
    "chromeos": ("ChromeOS", 45),
    "android": ("Android-x86", 118),
    "redstar": ("Red Star", 196),
    "temple": ("TempleOS", 226),
    "pythonistalinux": ("Pythonista Linux", 196),
    "avlinux": ("Avlinux", 202),
    "elive": ("Elive", 208),
    "legacyos": ("Legacyos", 214),
    "commodoreosvision": ("Commodore OS", 220),
    "dynebolic": ("Dynebolic", 226),
    "crowz": ("Crowz", 190),
    "refracta": ("Refracta", 118),
    "exe": ("Exe", 46),
    "star": ("Star", 82),
    "miyolinux": ("Miyolinux", 48),
    "gnuinos": ("Gnuinos", 49),
    "fluxuanlinux": ("Fluxuanlinux", 50),
    "decodeos": ("Decodeos", 51),
    "heads": ("Heads", 45),
    "virage": ("Virage", 39),
    "vuudo": ("Vuu Do", 33),
    "goodlifelinux": ("Goodlifelinux", 27),
    "nelumdev1": ("Nelum Dev1", 21),
    "minimimo": ("Mini Mimo", 57),
    "puffos": ("Puffos", 93),
    "crunkbongos": ("Crunkbong OS", 129),
    "expirionlinux": ("Expirionlinux", 135),
    "alienos": ("Alien OS", 141),
    "relianoid": ("Relianoid", 165),
    "gnoppixlinux": ("Gnoppixlinux", 201),
    "drpartedlive": ("Dr Partedlive", 199),
    "bros": ("Bros", 203),
    "syslinuxos": ("Syslinuxos", 210),
    "linuxkodachi": ("Linuxkodachi", 215),
    "makululinux": ("Makululinux", 221),
    "extix": ("Extix", 229),
    "skudonet": ("Skudonet", 244),
    "ubuntupack": ("Ubuntupack", 250),
    "ubuntuunity": ("Ubuntuunity", 81),
    "clonezillalive": ("Clonezillalive", 77),
    "rebeccablackos": ("Rebeccablackos", 70),
    "ufficiolinux": ("Ufficiolinux", 106),
    "joborun": ("Joborun", 40),
    "spark": ("Spark", 212),
    "alphaos": ("Alphaos", 196),
    "porteuskiosk": ("Porteuskiosk", 202),
    "porteux": ("Porteux", 208),
    "slint": ("Slint", 214),
    "slaxbmc": ("Slaxbmc", 220),
    "superbminiserver": ("Superb Mini", 226),
    "daphile": ("Daphile", 190),
    "garyos": ("Garyos", 118),
    "exgent": ("Exgent", 46),
    "agarimos": ("Agarimos", 82),
    "fvoid": ("F Void", 48),
    "cereuslinux": ("Cereuslinux", 49),
    "tinypawlinux": ("Tinypaw Linux", 50),
    "nanolinux": ("Nanolinux", 51),
    "cruxex": ("Cruxex", 45),
    "thinstation": ("Thinstation", 39),
    "ploplinux": ("Ploplinux", 33),
    "linuxconsole": ("Linuxconsole", 27),
    "pldlinux": ("Pldlinux", 21),
    "merelinux": ("Merelinux", 57),
    "iglunix": ("Iglunix", 93),
    "glaucus": ("Glaucus", 129),
    "glasnostlinux": ("Glasnostlinux", 135),
    "sabotagelinux": ("Sabotagelinux", 141),
    "adelielinux": ("Adelielinux", 165),
    "partedmagic": ("Partedmagic", 201),
    "cucumberlinux": ("Cucumberlinux", 199),
    "kanapi": ("Kanapi", 203),
    "lombixos": ("Lombixos", 210),
    "stali": ("Stali", 215),
    "sulinos": ("Sulinos", 221),
    "turkmanlinux": ("Turkmanlinux", 229),
    "minimallinuxlive": ("Minimal Live", 244),
    "nixng": ("Nixng", 250),
    "voidpup": ("Voidpup", 81),
    "lxpup": ("Lxpup", 77),
    "lesssystemdgnulinux": ("LessSystemd", 70),
    "alicelinux": ("Alicelinux", 106),
    "funos": ("Funos", 40),
    "ubuntukylin": ("Ubuntukylin", 212),
    "ubuntucinnamon": ("Ubuntucinnamon", 196),
    "debianedu": ("Debianedu", 202),
    "windowmakerlive": ("Windowmakerlive", 208),
    "dragonos": ("Dragonos", 214),
    "openmediavault": ("Openmediavault", 220),
    "canaima": ("Canaima", 226),
    "selks": ("SELKS", 190),
    "yunohost": ("Yunohost", 118),
    "edubuntu": ("Edubuntu", 46),
    "linuxschools": ("Linuxschools", 82),
    "maxmadridlinux": ("Max Madrid Linux", 48),
    "liveraizo": ("Liveraizo", 49),
    "crunchbang": ("Crunchbang++", 50),
    "robolinux": ("Robolinux", 51),
    "runtu": ("Runtu", 45),
    "solydxk": ("Solydxk", 39),
    "accesiblecoconut": ("Accesible Coconut", 33),
    "untanglengfirewall": ("Untanglengfirewall", 27),
    "vyos": ("VyOS", 21),
    "anduinos": ("Anduinos", 57),
    "ubuntuchristianedition": ("Ubuntuchristianedition", 93),
    "zephix": ("Zephix", 129),
    "nova": ("Nova", 135),
    "zentyalserver": ("Zentyalserver", 141),
    "diamondlinuxtt": ("Diamondlinux TT", 165),
    "kumanderlinux": ("Kumanderlinux", 201),
    "lliurex": ("Lliurex", 199),
    "freedombox": ("Freedombox", 203),
    "hamonikr": ("Hamonikr", 210),
    "lernstick": ("Lernstick", 215),
    "univentioncorporateserver": ("Univention", 221),
    "elearnix": ("Elearnix", 229),
    "nexentastor": ("Nexentastor", 244),
    "pakos": ("Pakos", 250),
    "primtux": ("Primtux", 81),
    "turnkeylinux": ("Turnkeylinux", 77),
    "ob2dlinux": ("Ob2dlinux", 70),
    "arma": ("Arma", 106),
    "osgeolive": ("Osgeolive", 40),
    "pelicanhpcgnulinux": ("PelicanHPC", 212),
    "voyagerlive": ("Voyagerlive", 196),
    "berrylinux": ("Berrylinux", 202),
    "navylinux": ("Navylinux", 208),
    "networksecuritytoolkit": ("Net Security", 214),
    "baruwaenterpriseedition": ("Baruwa", 220),
    "openeuler": ("Openeuler", 226),
    "smeserver": ("Smeserver", 190),
    "minios": ("Minios", 118),
    "simplylinux": ("Simplylinux", 46),
    "bluestarlinux": ("Bluestarlinux", 82),
    "sdesk": ("Sdesk", 48),
    "ultimateedition": ("Ultimateedition", 49),
    "archman": ("Archman", 50),
    "snallinux": ("Snallinux", 51),
    "ubos": ("Ubos", 45),
    "suselinuxenterprise": ("Suselinuxenterprise", 39),
    "openmandrivalx": ("Openmandrivalx", 33),
    "rlxos": ("Rlxos", 27),
    "peropesis": ("Peropesis", 21),
    "openmamba": ("Openmamba", 57),
    "bedrocklinux": ("Bedrocklinux", 93),
    "uncomos": ("Uncomos", 129),
    "alteros": ("Alteros", 135),
    "utopia": ("Utopia", 141),
    "magos": ("Magos", 165),
    "keepos": ("Keepos", 201),
    "igos": ("Igos", 199),
    "govonix": ("Govonix", 203),
    "ubermix": ("Ubermix", 210),
    "escuelas": ("Escuelas", 215),
    "goslinux": ("Goslinux", 221),
    "matuntu": ("Matuntu", 229),
    "winuxos": ("Winuxos", 244),
    "uos": ("UOS", 250),
    "puppyrus": ("Puppyrus", 81),
    "aldos": ("Aldos", 77),
    "chromiumos": ("Chromiumos", 70),
    "devillinux": ("Devil Linux", 106),
    "linuxbbq": ("Linuxbbq", 40),
    "xenialinux": ("Xenialinux", 212),
    "ximperlinux": ("Ximperlinux", 196),
    "milislinux": ("Milislinux", 202),
    "oasislinux": ("Oasislinux", 208),
    "noirlinux": ("Noirlinux", 214),
    "eweos": ("Eweos", 220),
    "msvsphereos": ("Msvsphere OS", 226),
    "gnomeos": ("Gnomeos", 190),
    "lingmo": ("Lingmo", 118),
    "mocaccinoos": ("Mocaccinoos", 46),
    "linuxkamarada": ("Linuxkamarada", 82),
    "securityonion": ("Securityonion", 48),
    "refreshos": ("Refreshos", 49),
    "maunalinux": ("Maunalinux", 50),
    "exelentos": ("Exelentos", 51),
    "droidian": ("Droidian", 45),
    "elinos": ("Elinos", 39),
    "galliumos": ("Galliumos", 33),
    "linuxcnc": ("Linuxcnc", 27),
    "librecmc": ("Librecmc", 21),
    "junest": ("Junest", 57),
    "lineageos": ("Lineageos", 93),
    "windriver": ("Windriver", 129),
    "rocketshow": ("Rocketshow", 135),
    "redribbon": ("Redribbon", 141),
    "taloslinux": ("Taloslinux", 165),
    "altimalinux": ("Altimalinux", 201),
    "deblinux": ("Deblinux", 199),
    "ubixlinux": ("Ubixlinux", 203),
    "snowflakeos": ("Snowflakeos", 210),
    "picoreplayer": ("Picoreplayer", 215),
    "tuxnmix": ("Tuxnmix", 221),
    "acoros": ("Acoros", 229),
    "coffeelinux": ("Coffeelinux", 244),
    "omegalinux": ("Omegalinux", 250),
    "chimbalix": ("Chimbalix", 81),
    "sleeperos": ("Sleeperos", 77),
    "quieuxlinux": ("Quieuxlinux", 70),
    "radixlinux": ("Radixlinux", 106),
    "vendefoulwolflinux": ("Vendefoulwolflinux", 40),
    "malbianlinux": ("Malbianlinux", 212),
    "quirinux": ("Quirinux", 196),
    "helwanlinux": ("Helwanlinux", 202),
    "twisteros": ("Twisteros", 208),
    "calyxos": ("Calyxos", 214),
    "traveleros": ("Traveleros", 220),
    "heliumos": ("Heliumos", 226),
    "deblightos": ("Deblightos", 190),
    "starbuntu": ("Starbuntu", 118),
    "startos": ("Startos", 46),
    "shebanglinux": ("Shebanglinux", 82),
    "increaseos": ("Increaseos", 48),
    "minkiscrappylinux": ("Minkiscrappylinux", 49),
    "cybr": ("Cybr", 50),
    "stalix": ("Stal Ix", 51),
    "spacefun": ("Spacefun", 45),
    "flickos": ("Flickos", 39),
    "quemos": ("Quemos", 33),
    "staticlinux": ("Staticlinux", 27),
    "titanlinux": ("Titanlinux", 21),
    "txikilinux": ("Txikilinux", 57),
}

BUILTIN_ALIASES = {
    "archlinux": "arch",
    "arch-linux": "arch",
    "popos": "pop",
    "pop_os": "pop",
    "pop-os": "pop",
    "linuxmint": "mint",
    "elementaryos": "elementary",
    "opensuse-tumbleweed": "tumbleweed",
    "leap": "opensuse",
    "opensuse-leap": "opensuse",
    "redhat": "rhel",
    "red-hat": "rhel",
    "almalinux": "alma",
    "rockylinux": "rocky",
    "oraclelinux": "oracle",
    "amazonlinux": "amazon",
    "amzn": "amazon",
    "raspberry": "raspbian",
    "raspberrypi": "raspbian",
    "raspios": "raspbian",
    "rpi": "raspbian",
    "void-linux": "void",
    "nix": "nixos",
    "steam": "steamos",
    "templeos": "temple",
    "redstaros": "redstar",
    "neon": "kdeneon",
    "kde-neon": "kdeneon",
    "fedora-silverblue": "silverblue",
    "serpentos": "serpent",
    "dragonflybsd": "dragonfly",
    "tinycorelinux": "tinycore",
    "geckolinux": "gecko",
    "vanillaos": "vanilla",
}

BUILTIN_DES = {
    "gnome": ("GNOME", 33),
    "kde": ("KDE Plasma", 39),
    "xfce": ("Xfce", 45),
    "lxqt": ("LXQt", 39),
    "lxde": ("LXDE", 33),
    "cinnamon": ("Cinnamon", 77),
    "mate": ("MATE", 118),
    "budgie": ("Budgie", 214),
    "dde": ("Deepin DE", 39),
    "pantheon": ("Pantheon", 45),
    "enlightenment": ("Enlightenment", 129),
    "cosmic": ("COSMIC", 141),
    "cutefish": ("CutefishDE", 45),
    "lumina": ("Lumina", 39),
    "trinity": ("Trinity", 33),
    "ukui": ("UKUI", 39),
    "unity": ("Unity", 202),
    "maxx": ("MaXX", 39),
    "cde": ("CDE", 214),
    "liri": ("Liri Shell", 45),
    "theshell": ("theShell", 39),
    "openbox": ("Openbox", 240),
    "fluxbox": ("Fluxbox", 244),
    "blackbox": ("Blackbox", 240),
    "fvwm": ("FVWM", 33),
    "icewm": ("IceWM", 45),
    "jwm": ("JWM", 39),
    "windowmaker": ("Window Maker", 250),
    "cwm": ("CWM", 244),
    "twm": ("TWM", 244),
    "mwm": ("MWM", 240),
    "afterstep": ("AfterStep", 39),
    "sawfish": ("Sawfish", 46),
    "pekwm": ("PekWM", 240),
    "amiwm": ("amiwm", 240),
    "i3": ("i3", 27),
    "i3gaps": ("i3-gaps", 27),
    "bspwm": ("bspwm", 39),
    "dwm": ("dwm", 46),
    "awesome": ("awesome", 39),
    "xmonad": ("Xmonad", 196),
    "qtile": ("Qtile", 196),
    "herbstluftwm": ("herbstluftwm", 118),
    "spectrwm": ("spectrwm", 46),
    "ratpoison": ("ratpoison", 244),
    "stumpwm": ("StumpWM", 46),
    "leftwm": ("LeftWM", 39),
    "wmii": ("wmii", 244),
    "frankenwm": ("FrankenWM", 39),
    "dk": ("dk", 39),
    "exwm": ("EXWM", 129),
    "ion3": ("Ion3", 244),
    "notionwm": ("Notion WM", 39),
    "tinywm": ("TinyWM", 244),
    "catwm": ("catwm", 244),
    "evilwm": ("evilwm", 240),
    "qvwm": ("Qvwm", 240),
    "hyprland": ("Hyprland", 51),
    "sway": ("Sway", 39),
    "river": ("River", 45),
    "wayfire": ("Wayfire", 45),
    "hikari": ("Hikari", 214),
    "dwl": ("dwl", 46),
    "labwc": ("labwc", 39),
    "niri": ("Niri", 141),
    "japokwm": ("japokwm", 39),
    "cagebreak": ("Cagebreak", 244),
    "velox": ("Velox", 39),
    "newm": ("newm", 39),
    "miracle": ("Miracle-WM", 129),
    "cage": ("Cage", 244),
    "compiz": ("Compiz", 39),
}

BUILTIN_DE_ALIASES = {
    "plasma": "kde",
    "kdeplasma": "kde",
    "kde5": "kde",
    "kde6": "kde",
    "gnomeshell": "gnome",
    "gnome3": "gnome",
    "deepinde": "dde",
    "ddeshell": "dde",
    "e16": "enlightenment",
    "e17": "enlightenment",
    "wmaker": "windowmaker",
    "herbst": "herbstluftwm",
    "swaywm": "sway",
    "hypr": "hyprland",
    "i3wm": "i3",
    "notion": "notionwm",
    "miraclewm": "miracle",
    "elementaryde": "pantheon",
}

# Runtime catalogs: start from built-ins, then merge user files in load_catalogs().
DISTROS = dict(BUILTIN_DISTROS)
ALIASES = dict(BUILTIN_ALIASES)
DES = dict(BUILTIN_DES)
DE_ALIASES = dict(BUILTIN_DE_ALIASES)

PALETTE = [
    ("Красный", 196),
    ("Оранжевый", 208),
    ("Жёлтый", 226),
    ("Зелёный", 46),
    ("Лаймовый", 118),
    ("Бирюзовый", 51),
    ("Голубой", 39),
    ("Синий", 33),
    ("Фиолетовый", 129),
    ("Розовый", 201),
    ("Белый", 255),
    ("Серый", 244),
]

NAMED_COLORS = {
    "red": 196, "orange": 208, "yellow": 226, "green": 46, "lime": 118,
    "cyan": 51, "teal": 37, "lightblue": 39, "blue": 33, "purple": 129,
    "violet": 129, "magenta": 201, "pink": 201, "white": 255, "gray": 244,
    "grey": 244, "black": 16,
}

FONT = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ####", "#    ", "#    ", "#    ", "#    ", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ####", "#    ", "# ###", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "#####"],
    "J": ["#####", "   # ", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "###  ", "#  # ", "#   #", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#### ", "#  # ", "#   #", "#   #"],
    "S": [" ####", "#    ", " ### ", "    #", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "## ##", "#   #"],
    "X": ["#   #", " # # ", "  #  ", "  #  ", " # # ", "#   #"],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "#####"],
    "2": [" ### ", "#   #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#####", "   # ", "  ## ", "    #", "#   #", " ### "],
    "4": ["#   #", "#   #", "#####", "    #", "    #", "    #"],
    "5": ["#####", "#    ", "#### ", "    #", "#   #", " ### "],
    "6": [" ### ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "   # ", "  #  ", " #   ", " #   ", " #   "],
    "8": [" ### ", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", " ### "],
    "!": ["  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "],
    "_": ["     ", "     ", "     ", "     ", "     ", "#####"],
    ".": ["     ", "     ", "     ", "     ", "     ", "  #  "],
    "-": ["     ", "     ", "#####", "     ", "     ", "     "],
    "+": ["     ", "  #  ", "#####", "  #  ", "     ", "     "],
    " ": ["   ", "   ", "   ", "   ", "   ", "   "],
}
FONT_HEIGHT = 6
HALF = {(False, False): " ", (True, False): "\u2580", (False, True): "\u2584", (True, True): "\u2588"}

BASIC_RGB = {
    1: (205, 0, 0), 2: (0, 205, 0), 3: (205, 205, 0), 4: (0, 0, 238),
    5: (205, 0, 205), 6: (0, 205, 205), 7: (229, 229, 229),
}


def c256_to_rgb(c):
    if c < 16:
        base = [
            (0, 0, 0), (205, 0, 0), (0, 205, 0), (205, 205, 0),
            (0, 0, 238), (205, 0, 205), (0, 205, 205), (229, 229, 229),
            (127, 127, 127), (255, 0, 0), (0, 255, 0), (255, 255, 0),
            (92, 92, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255),
        ]
        return base[c]
    if c >= 232:
        v = 8 + (c - 232) * 10
        return (v, v, v)
    c -= 16
    r, g, b = c // 36, (c % 36) // 6, c % 6
    conv = lambda x: 0 if x == 0 else 55 + x * 40
    return (conv(r), conv(g), conv(b))


def nearest_basic(rgb):
    r, g, b = rgb
    best, best_d = 7, None
    for k, (R, G, B) in BASIC_RGB.items():
        d = (r - R) ** 2 + (g - G) ** 2 + (b - B) ** 2
        if best_d is None or d < best_d:
            best, best_d = k, d
    return best


def ansi_fg(color):
    if isinstance(color, tuple):
        r, g, b = color
        return "\x1b[38;2;%d;%d;%dm" % (r, g, b)
    return "\x1b[38;5;%dm" % int(color)


def colorize(text, color, enabled):
    return "%s%s\x1b[0m" % (ansi_fg(color), text) if enabled else text


def parse_color(s):
    if s is None:
        return None
    s = s.strip()
    low = s.lower()
    if low in NAMED_COLORS:
        return NAMED_COLORS[low]
    is_hex = low.startswith("#")
    h = low.lstrip("#")
    if not is_hex and s.isdigit():
        n = int(s)
        if 0 <= n <= 255:
            return n
    if re.fullmatch(r"[0-9a-f]{6}", h):
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    if is_hex and re.fullmatch(r"[0-9a-f]{3}", h):
        return tuple(int(c * 2, 16) for c in h)
    return None


def parse_gradient(s):
    if not s:
        return None
    parts = [p for p in re.split(r"[,/]", s) if p.strip()]
    stops = []
    for p in parts:
        c = parse_color(p)
        if c is None:
            return None
        stops.append(c)
    if len(stops) < 2:
        return None
    return stops


def supports_color(force_no=False):
    if force_no or os.environ.get("NO_COLOR") is not None:
        return False
    return sys.stdout.isatty()


# --------------------------------------------------------------------------- #
# External catalog (distros.json / distros.txt)                               #
# --------------------------------------------------------------------------- #

_LOAD_WARNINGS = []
_LOADED_FILES = []


def _config_dir():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "iuse")


def _script_dir():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.getcwd()


def catalog_paths():
    """Highest priority first."""
    paths = []
    env = os.environ.get("IUSE_DISTROS")
    if env:
        paths.append(env)
    cfg = _config_dir()
    paths.append(os.path.join(cfg, "distros.json"))
    paths.append(os.path.join(cfg, "distros.txt"))
    sd = _script_dir()
    paths.append(os.path.join(sd, "distros.json"))
    paths.append(os.path.join(sd, "distros.txt"))
    return paths


def _norm_color(v):
    if isinstance(v, bool):
        return 81
    if isinstance(v, int):
        return v
    if isinstance(v, (list, tuple)) and len(v) == 3:
        try:
            return (int(v[0]), int(v[1]), int(v[2]))
        except (TypeError, ValueError):
            return 81
    if isinstance(v, str):
        c = parse_color(v)
        return c if c is not None else 81
    return 81


def _norm_entry(v):
    if isinstance(v, dict):
        return (str(v.get("name", "?")), _norm_color(v.get("color", 81)))
    if isinstance(v, (list, tuple)) and len(v) >= 2:
        return (str(v[0]), _norm_color(v[1]))
    if isinstance(v, (int, str)):
        return ("?", _norm_color(v))
    return ("?", 81)


def parse_txt_catalog(text):
    """Plain-text list: `key | Display Name | color | alias1,alias2`."""
    distros, aliases = {}, {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 2:
            continue
        key = parts[0].lower()
        if not key:
            continue
        name = parts[1] or key
        color = parts[2] if len(parts) >= 3 and parts[2] else "81"
        distros[key] = {"name": name, "color": color}
        if len(parts) >= 4 and parts[3]:
            for a in parts[3].split(","):
                a = a.strip().lower()
                if a:
                    aliases[a] = key
    return {"distros": distros, "distro_aliases": aliases}


def _merge_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if path.lower().endswith(".txt"):
        data = parse_txt_catalog(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("top-level value must be an object")
    for k, v in (data.get("distros") or {}).items():
        DISTROS[k.lower()] = _norm_entry(v)
    for a, k in (data.get("distro_aliases") or {}).items():
        ALIASES[a.lower()] = str(k).lower()
    for k, v in (data.get("des") or {}).items():
        DES[k.lower()] = _norm_entry(v)
    for a, k in (data.get("de_aliases") or {}).items():
        DE_ALIASES[a.lower()] = str(k).lower()


def load_catalogs(extra_path=None):
    paths = catalog_paths()
    if extra_path:
        paths = [extra_path] + paths  # highest priority
    seen = set()
    # merge lowest priority first so higher priority overrides
    for p in reversed(paths):
        if not p:
            continue
        rp = os.path.abspath(os.path.expanduser(p))
        if rp in seen:
            continue
        seen.add(rp)
        if os.path.isfile(rp):
            try:
                _merge_file(rp)
                _LOADED_FILES.append(rp)
            except Exception as e:  # noqa: BLE001
                _LOAD_WARNINGS.append((rp, str(e)))


def cmd_export(path, color_enabled):
    if not path:
        d = _config_dir()
        try:
            os.makedirs(d, exist_ok=True)
        except OSError as e:
            print(t("load_warn") % (d, e), file=sys.stderr)
        path = os.path.join(d, "distros.json")
    data = {
        "distros": {k: {"name": n, "color": c} for k, (n, c) in BUILTIN_DISTROS.items()},
        "distro_aliases": dict(BUILTIN_ALIASES),
        "des": {k: {"name": n, "color": c} for k, (n, c) in BUILTIN_DES.items()},
        "de_aliases": dict(BUILTIN_DE_ALIASES),
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    except OSError as e:
        print(t("load_warn") % (path, e), file=sys.stderr)
        return 1
    print(colorize(t("exported") % path, 81, color_enabled))
    return 0


# --------------------------------------------------------------------------- #
# Banner rendering                                                            #
# --------------------------------------------------------------------------- #

def _full_rows(text):
    text = text.upper()
    rows = [""] * FONT_HEIGHT
    for ch in text:
        glyph = FONT.get(ch, FONT[" "])
        gw = len(glyph[0])
        for i in range(FONT_HEIGHT):
            line = glyph[i] if i < len(glyph) else " " * gw
            rows[i] += line.replace("#", "\u2588") + " "
    return rows


def render_big(text):
    return "\n".join(_full_rows(text))


def render_small(text):
    rows = _full_rows(text)
    width = max(len(r) for r in rows)
    rows = [r.ljust(width) for r in rows]
    out = []
    for r in range(0, FONT_HEIGHT, 2):
        top, bot = rows[r], rows[r + 1]
        out.append("".join(HALF[(top[c] != " ", bot[c] != " ")] for c in range(width)))
    return "\n".join(out)


def banner_width(text, small=True):
    rows = render_small(text).splitlines() if small else _full_rows(text)
    return max((len(r) for r in rows), default=0)


def _wrap_phrase(phrase, small, term_w):
    groups, cur = [], ""
    for w in phrase.split(" "):
        trial = (cur + " " + w).strip()
        if cur and banner_width(trial, small) > term_w:
            groups.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        groups.append(cur)
    return groups


def _build_art_groups(phrase, style):
    """Return a list of multi-line ASCII-art strings, or None to fall back to plain."""
    term_w = shutil.get_terminal_size((80, 24)).columns
    if style != "mini":
        order = ["big", "small"] if style == "big" else ["small"]
        for st in order:
            small = st != "big"
            groups = _wrap_phrase(phrase, small, term_w)
            if all(banner_width(g, small) <= term_w for g in groups):
                return [render_small(g) if small else render_big(g) for g in groups]
    return None


def _stops_rgb(stops):
    out = []
    for s in stops:
        if isinstance(s, tuple):
            out.append(s)
        else:
            out.append(c256_to_rgb(int(s)))
    return out


def gradient_at(stops_rgb, pos):
    if not stops_rgb:
        return (255, 255, 255)
    if len(stops_rgb) == 1:
        return stops_rgb[0]
    pos = 0.0 if pos < 0 else (1.0 if pos > 1 else pos)
    seg = pos * (len(stops_rgb) - 1)
    i = int(seg)
    if i >= len(stops_rgb) - 1:
        return stops_rgb[-1]
    f = seg - i
    a, b = stops_rgb[i], stops_rgb[i + 1]
    return (
        int(round(a[0] + (b[0] - a[0]) * f)),
        int(round(a[1] + (b[1] - a[1]) * f)),
        int(round(a[2] + (b[2] - a[2]) * f)),
    )


def render_gradient(art, stops, gtype, enabled):
    if not enabled:
        return art
    lines = art.split("\n")
    srgb = _stops_rgb(stops)
    height = len(lines)
    width = max((len(l) for l in lines), default=1)
    out = []
    for y, line in enumerate(lines):
        buf, last = [], None
        for x, ch in enumerate(line):
            if ch == " ":
                if last is not None:
                    buf.append("\x1b[0m")
                    last = None
                buf.append(" ")
                continue
            if gtype == "vertical":
                pos = y / max(1, height - 1)
            elif gtype == "diagonal":
                pos = (x + y) / max(1, (width - 1) + (height - 1))
            else:
                pos = x / max(1, width - 1)
            col = gradient_at(srgb, pos)
            if col != last:
                buf.append("\x1b[38;2;%d;%d;%dm" % col)
                last = col
            buf.append(ch)
        if last is not None:
            buf.append("\x1b[0m")
        out.append("".join(buf))
    return "\n".join(out)


def render_gradient_text(text, stops, gtype, enabled):
    if not enabled:
        return text
    srgb = _stops_rgb(stops)
    n = len(text)
    buf = []
    for i, ch in enumerate(text):
        col = gradient_at(srgb, i / max(1, n - 1))
        buf.append("\x1b[38;2;%d;%d;%dm" % col + ch)
    buf.append("\x1b[0m")
    return "".join(buf)


def print_phrase(name, color, color_enabled, style):
    phrase = "I USE %s BTW" % name.upper()
    arts = _build_art_groups(phrase, style)
    if arts is None:
        print(colorize(phrase, color, color_enabled))
        return
    print()
    for art in arts:
        print(colorize(art, color, color_enabled))
    print()


def print_phrase_gradient(name, stops, gtype, color_enabled, style):
    phrase = "I USE %s BTW" % name.upper()
    arts = _build_art_groups(phrase, style)
    if arts is None:
        print(render_gradient_text(phrase, stops, gtype, color_enabled))
        return
    print()
    for art in arts:
        print(render_gradient(art, stops, gtype, color_enabled))
    print()


def print_banner(label, color, gradient_spec, color_enabled, style):
    if gradient_spec:
        print_phrase_gradient(label, gradient_spec["stops"], gradient_spec["type"], color_enabled, style)
    else:
        print_phrase(label, color, color_enabled, style)


def detect_distro():
    data = {}
    for p in ("/etc/os-release", "/usr/lib/os-release"):
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if "=" in line:
                            k, _, v = line.partition("=")
                            data[k.strip()] = v.strip().strip('"')
                break
            except OSError:
                pass
    cands = []
    if "ID" in data:
        cands.append(data["ID"].lower())
    if "ID_LIKE" in data:
        cands += [x.lower() for x in re.split(r"\s+", data["ID_LIKE"]) if x]
    for c in cands:
        k = resolve_key(c)
        if k:
            return k
    return None


def resolve_key(name):
    if not name:
        return None
    n = name.strip().lower().replace(" ", "")
    if n in DISTROS:
        return n
    if n in ALIASES:
        return ALIASES[n]
    for k in DISTROS:
        if k in n or n in k:
            return k
    return None


def resolve_de(name):
    if not name:
        return None
    n = re.sub(r"[ _-]", "", name.strip().lower())
    if n in DES:
        return n
    if n in DE_ALIASES:
        return DE_ALIASES[n]
    for k in DES:
        if len(k) >= 4 and (k in n or n in k):
            return k
    return None


def fuzzy_match(query, key, name):
    q = query.lower().strip()
    if not q:
        return True
    hay = (key + " " + name).lower()
    if q in hay:
        return True
    it = iter(hay)
    return all(ch in it for ch in q)


BACK = object()
CANCELLED = "CANCELLED"


def interactive_flow():
    try:
        import curses
    except Exception:
        print(t("curses_required"), file=sys.stderr)
        sys.exit(1)

    def main_loop(stdscr):
        stdscr.keypad(True)
        try:
            curses.set_escdelay(25)
        except Exception:
            pass
        try:
            curses.start_color()
            curses.use_default_colors()
            has_color = curses.COLORS >= 8
            ncolors = curses.COLORS
            npairs = curses.COLOR_PAIRS
        except curses.error:
            has_color, ncolors, npairs = False, 0, 0
        pair_cache = {}

        def cp(col):
            if not has_color or not isinstance(col, int):
                return curses.A_NORMAL
            use = col
            if use >= ncolors:
                use = nearest_basic(c256_to_rgb(col))
                if use >= ncolors:
                    use = (col % max(1, ncolors - 1)) + 1
                    if use >= ncolors:
                        return curses.A_BOLD
            if use not in pair_cache:
                idx = len(pair_cache) + 1
                if idx >= npairs:
                    return curses.A_NORMAL
                try:
                    curses.init_pair(idx, use, -1)
                    pair_cache[use] = curses.color_pair(idx)
                except curses.error:
                    return curses.A_NORMAL
            return pair_cache[use]

        while True:
            mode = pick_mode(stdscr, cp)
            if mode is None:
                return CANCELLED
            catalog = DISTROS if mode == "distro" else DES
            keys = sorted(catalog, key=lambda k: catalog[k][0].lower())
            while True:
                key = pick_item(stdscr, cp, keys, catalog, mode)
                if key is None:
                    break
                color = pick_color(stdscr, cp, catalog[key])
                if color is BACK:
                    continue
                return (mode, key, color)

    return curses.wrapper(main_loop)


def pick_mode(stdscr, cp):
    import curses
    curses.curs_set(0)
    options = [("distro", t("mode_distro")), ("de", t("mode_de"))]
    idx = 0
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        stdscr.addnstr(0, 0, " " + t("mode_title"), w - 1, curses.A_BOLD)
        stdscr.addnstr(1, 0, t("mode_hint"), w - 1, curses.A_DIM)
        for i, (val, label) in enumerate(options):
            marker = "\u276f " if i == idx else "  "
            attr = curses.A_REVERSE | curses.A_BOLD if i == idx else curses.A_NORMAL
            try:
                stdscr.addnstr(3 + i, 0, (marker + label).ljust(w - 1), w - 1, attr)
            except curses.error:
                pass
        stdscr.refresh()
        try:
            ch = stdscr.get_wch()
        except curses.error:
            continue
        if isinstance(ch, str):
            if ch in ("\n", "\r"):
                return options[idx][0]
            if ch == "\x1b":
                return None
        else:
            if ch == curses.KEY_UP:
                idx = (idx - 1) % len(options)
            elif ch == curses.KEY_DOWN:
                idx = (idx + 1) % len(options)


def pick_item(stdscr, cp, keys, catalog, mode):
    import curses
    curses.curs_set(1)
    query, idx, top = "", 0, 0
    while True:
        filt = [k for k in keys if fuzzy_match(query, k, catalog[k][0])]
        if filt:
            idx = max(0, min(idx, len(filt) - 1))
        else:
            idx = 0
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        stdscr.addnstr(0, 0, t("pick_title_de") if mode == "de" else t("pick_title_distro"), w - 1, curses.A_BOLD)
        stdscr.addnstr(1, 0, t("pick_hint"), w - 1, curses.A_DIM)
        stdscr.addnstr(2, 0, " > " + query, w - 1, curses.A_BOLD)
        list_h = max(1, h - 4)
        if not filt:
            stdscr.addnstr(3, 0, t("not_found"), w - 1, curses.A_DIM)
            try:
                stdscr.addnstr(h - 1, 0, " 0/%d " % len(keys), w - 1, curses.A_DIM)
            except curses.error:
                pass
            stdscr.refresh()
        else:
            if idx < top:
                top = idx
            elif idx >= top + list_h:
                top = idx - list_h + 1
            for i in range(top, min(len(filt), top + list_h)):
                k = filt[i]
                name, col = catalog[k]
                marker = "\u276f " if i == idx else "  "
                attr = cp(col)
                if i == idx:
                    attr |= curses.A_REVERSE | curses.A_BOLD
                try:
                    stdscr.addnstr(3 + (i - top), 0, (marker + name).ljust(w - 1), w - 1, attr)
                except curses.error:
                    pass
            try:
                stdscr.addnstr(h - 1, 0, " %d/%d " % (len(filt), len(keys)), w - 1, curses.A_DIM)
            except curses.error:
                pass
            stdscr.refresh()
        try:
            ch = stdscr.get_wch()
        except curses.error:
            continue
        if isinstance(ch, str):
            if ch in ("\n", "\r"):
                if filt:
                    return filt[idx]
                continue
            if ch == "\x1b":
                return None
            if ch in ("\x7f", "\b"):
                query, idx = query[:-1], 0
            elif ch == "\x15":
                query, idx = "", 0
            elif ch.isprintable():
                query, idx = query + ch, 0
        else:
            if ch == curses.KEY_UP:
                idx -= 1
            elif ch == curses.KEY_DOWN:
                idx += 1
            elif ch == curses.KEY_NPAGE:
                idx += list_h
            elif ch == curses.KEY_PPAGE:
                idx -= list_h
            elif ch == curses.KEY_BACKSPACE:
                query, idx = query[:-1], 0
        if filt:
            idx %= len(filt)


def pick_from(stdscr, cp, title, hint, items, swatches=None):
    import curses
    curses.curs_set(0)
    idx, top = 0, 0
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        stdscr.addnstr(0, 0, title, w - 1, curses.A_BOLD)
        stdscr.addnstr(1, 0, hint, w - 1, curses.A_DIM)
        rows = max(1, h - 4)
        if idx < top:
            top = idx
        elif idx >= top + rows:
            top = idx - rows + 1
        for row, i in enumerate(range(top, min(len(items), top + rows))):
            label = items[i][1]
            sel = i == idx
            marker = "\u276f " if sel else "  "
            sw_code = swatches[i] if swatches else None
            swatch = "\u2588\u2588\u2588 " if sw_code is not None else ""
            attr = cp(sw_code) if sw_code is not None else curses.A_NORMAL
            if sel:
                attr |= curses.A_REVERSE | curses.A_BOLD
            try:
                stdscr.addnstr(3 + row, 0, (marker + swatch + label).ljust(w - 1), w - 1, attr)
            except curses.error:
                pass
        try:
            stdscr.addnstr(h - 1, 0, " %d/%d " % (idx + 1, len(items)), w - 1, curses.A_DIM)
        except curses.error:
            pass
        stdscr.refresh()
        try:
            ch = stdscr.get_wch()
        except curses.error:
            continue
        if isinstance(ch, str):
            if ch in ("\n", "\r"):
                return items[idx][0]
            if ch == "\x1b":
                return None
        else:
            if ch == curses.KEY_UP:
                idx = (idx - 1) % len(items)
            elif ch == curses.KEY_DOWN:
                idx = (idx + 1) % len(items)
            elif ch == curses.KEY_NPAGE:
                idx = min(len(items) - 1, idx + rows)
            elif ch == curses.KEY_PPAGE:
                idx = max(0, idx - rows)


def pick_one_color(stdscr, cp, title):
    import curses
    items = [(code, cname) for cname, code in PALETTE]
    items.append(("__custom__", t("color_custom")))
    swatches = [code for _, code in PALETTE] + [None]
    curses.curs_set(0)
    idx, top = 0, 0
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        stdscr.addnstr(0, 0, title, w - 1, curses.A_BOLD)
        stdscr.addnstr(1, 0, t("color_hint"), w - 1, curses.A_DIM)
        rows = max(1, h - 4)
        if idx < top:
            top = idx
        elif idx >= top + rows:
            top = idx - rows + 1
        for row, i in enumerate(range(top, min(len(items), top + rows))):
            code, label = items[i]
            sel = i == idx
            marker = "\u276f " if sel else "  "
            has_sw = swatches[i] is not None
            swatch = "\u2588\u2588\u2588 " if has_sw else "    "
            attr = cp(swatches[i]) if has_sw else curses.A_NORMAL
            if sel:
                attr |= curses.A_REVERSE | curses.A_BOLD
            try:
                stdscr.addnstr(3 + row, 0, (marker + swatch + label).ljust(w - 1), w - 1, attr)
            except curses.error:
                pass
        try:
            stdscr.addnstr(h - 1, 0, " %d/%d " % (idx + 1, len(items)), w - 1, curses.A_DIM)
        except curses.error:
            pass
        stdscr.refresh()
        try:
            ch = stdscr.get_wch()
        except curses.error:
            continue
        if isinstance(ch, str):
            if ch in ("\n", "\r"):
                code = items[idx][0]
                if code == "__custom__":
                    val = prompt_custom(stdscr)
                    curses.curs_set(0)
                    if val is not None:
                        return val
                else:
                    return code
            elif ch == "\x1b":
                return None
        else:
            if ch == curses.KEY_UP:
                idx = (idx - 1) % len(items)
            elif ch == curses.KEY_DOWN:
                idx = (idx + 1) % len(items)


def pick_gradient(stdscr, cp):
    count = pick_from(
        stdscr, cp, t("grad_count_title"), t("color_hint"),
        [(n, str(n)) for n in (2, 3, 4, 5)],
    )
    if count is None:
        return None
    stops = []
    for i in range(count):
        col = pick_one_color(stdscr, cp, t("grad_color_title") % (i + 1, count))
        if col is None:
            return None
        stops.append(col)
    gtype = pick_from(
        stdscr, cp, t("grad_type_title"), t("color_hint"),
        [
            ("horizontal", t("grad_type_horizontal")),
            ("vertical", t("grad_type_vertical")),
            ("diagonal", t("grad_type_diagonal")),
        ],
    )
    if gtype is None:
        return None
    return {"gradient": stops, "type": gtype}


def pick_color(stdscr, cp, distro):
    import curses
    name, dcolor = distro
    options = [("default", t("color_default") % name, dcolor)]
    options += [("preset", cname, code) for cname, code in PALETTE]
    options.append(("gradient", t("color_gradient"), None))
    options.append(("custom", t("color_custom"), None))
    idx = 0
    top = 0
    curses.curs_set(0)
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        stdscr.addnstr(0, 0, t("color_title") % name, w - 1, curses.A_BOLD)
        stdscr.addnstr(1, 0, t("color_hint"), w - 1, curses.A_DIM)
        rows = max(1, h - 4)
        if idx < top:
            top = idx
        elif idx >= top + rows:
            top = idx - rows + 1
        for row, i in enumerate(range(top, min(len(options), top + rows))):
            kind, label, code = options[i]
            sel = i == idx
            marker = "\u276f " if sel else "  "
            swatch = "\u2588\u2588\u2588 " if code is not None else "    "
            attr = cp(code) if code is not None else curses.A_NORMAL
            if sel:
                attr |= curses.A_REVERSE | curses.A_BOLD
            try:
                stdscr.addnstr(3 + row, 0, (marker + swatch + label).ljust(w - 1), w - 1, attr)
            except curses.error:
                pass
        stdscr.addnstr(h - 1, 0, " %d/%d " % (idx + 1, len(options)), w - 1, curses.A_DIM)
        stdscr.refresh()
        try:
            ch = stdscr.get_wch()
        except curses.error:
            continue
        if isinstance(ch, str):
            if ch in ("\n", "\r"):
                kind, label, code = options[idx]
                if kind == "default":
                    return dcolor
                if kind == "preset":
                    return code
                if kind == "gradient":
                    spec = pick_gradient(stdscr, cp)
                    curses.curs_set(0)
                    if spec is not None:
                        return spec
                if kind == "custom":
                    val = prompt_custom(stdscr)
                    if val is not None:
                        return val
                    curses.curs_set(0)
            elif ch == "\x1b":
                return BACK
        else:
            if ch == curses.KEY_UP:
                idx = (idx - 1) % len(options)
            elif ch == curses.KEY_DOWN:
                idx = (idx + 1) % len(options)
            elif ch == curses.KEY_NPAGE:
                idx = min(len(options) - 1, idx + rows)
            elif ch == curses.KEY_PPAGE:
                idx = max(0, idx - rows)


def prompt_custom(stdscr):
    import curses
    curses.curs_set(1)
    buf, err = "", ""
    while True:
        h, w = stdscr.getmaxyx()
        for yy in (h - 3, h - 2, h - 1):
            stdscr.move(max(0, yy), 0)
            stdscr.clrtoeol()
        stdscr.addnstr(h - 3, 0, t("prompt_hint"), w - 1, curses.A_DIM)
        stdscr.addnstr(h - 2, 0, t("prompt_keys"), w - 1, curses.A_DIM)
        tail = ("   " + err) if err else ""
        stdscr.addnstr(h - 1, 0, " \u276f " + buf + tail, w - 1, curses.A_BOLD)
        stdscr.refresh()
        try:
            ch = stdscr.get_wch()
        except curses.error:
            continue
        if isinstance(ch, str):
            if ch in ("\n", "\r"):
                c = parse_color(buf)
                if c is None:
                    err = t("prompt_bad")
                    continue
                return c
            if ch == "\x1b":
                return None
            if ch in ("\x7f", "\b"):
                buf, err = buf[:-1], ""
            elif ch.isprintable():
                buf, err = buf + ch, ""
        else:
            if ch == curses.KEY_BACKSPACE:
                buf, err = buf[:-1], ""


def cmd_list(color_enabled):
    print(colorize(t("list_distros"), 81, color_enabled))
    print()
    keys = sorted(DISTROS, key=lambda k: DISTROS[k][0].lower())
    width = max(len(DISTROS[k][0]) for k in keys) + 2
    cols = max(1, shutil.get_terminal_size((80, 24)).columns // (width + 2))
    for i, k in enumerate(keys):
        name, color = DISTROS[k]
        print(colorize(name.ljust(width), color, color_enabled), end="\n" if (i + 1) % cols == 0 else "")
    if len(keys) % cols != 0:
        print()
    print()
    print(t("list_total_distros") % len(keys))


def cmd_list_de(color_enabled):
    print(colorize(t("list_des"), 81, color_enabled))
    print()
    keys = sorted(DES, key=lambda k: DES[k][0].lower())
    width = max(len(DES[k][0]) for k in keys) + 2
    cols = max(1, shutil.get_terminal_size((80, 24)).columns // (width + 2))
    for i, k in enumerate(keys):
        name, color = DES[k]
        print(colorize(name.ljust(width), color, color_enabled), end="\n" if (i + 1) % cols == 0 else "")
    if len(keys) % cols != 0:
        print()
    print()
    print(t("list_total_des") % len(keys))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="iuse.py",
        description=t("desc"),
        epilog=t("epilog"),
    )
    parser.add_argument("distro", nargs="?", help=t("h_distro"))
    parser.add_argument("-r", "--random", action="store_true", help=t("h_random"))
    parser.add_argument("-l", "--list", action="store_true", help=t("h_list"))
    parser.add_argument("-c", "--color", help=t("h_color"))
    parser.add_argument("-g", "--gradient", help=t("h_gradient"))
    parser.add_argument("--gradient-type", choices=["horizontal", "vertical", "diagonal"], default="horizontal", help=t("h_gradient_type"))
    parser.add_argument("-b", "--banner", choices=["small", "big", "mini"], default="small", help=t("h_banner"))
    parser.add_argument("-d", "--de", help=t("h_de"))
    parser.add_argument("--list-de", action="store_true", help=t("h_listde"))
    parser.add_argument("--distros", help=t("h_distros"))
    parser.add_argument("--export-distros", nargs="?", const="", metavar="PATH", help=t("h_export"))
    parser.add_argument("--no-color", action="store_true", help=t("h_nocolor"))
    parser.add_argument("--version", action="version", version="iuse " + __version__)
    args = parser.parse_args(argv)

    color_enabled = supports_color(force_no=args.no_color)

    if args.export_distros is not None:
        return cmd_export(args.export_distros or None, color_enabled)

    load_catalogs(args.distros)
    for path, err in _LOAD_WARNINGS:
        print(colorize(t("load_warn") % (path, err), 203, color_enabled), file=sys.stderr)

    if args.list:
        cmd_list(color_enabled)
        return 0

    if args.list_de:
        cmd_list_de(color_enabled)
        return 0

    cli_color = None
    if args.color:
        cli_color = parse_color(args.color)
        if cli_color is None:
            print(colorize(t("bad_color") % args.color, 203, color_enabled), file=sys.stderr)
            return 1

    cli_gradient = None
    if args.gradient:
        stops = parse_gradient(args.gradient)
        if stops is None:
            print(colorize(t("bad_gradient") % args.gradient, 203, color_enabled), file=sys.stderr)
            return 1
        cli_gradient = {"stops": stops, "type": args.gradient_type}

    if args.de is not None:
        dekey = resolve_de(args.de)
        if dekey is None:
            color = cli_color if cli_color is not None else 81
            print_banner(args.de, color, cli_gradient, color_enabled, args.banner)
            print(colorize(t("not_in_base_de") % args.de, 240, color_enabled), file=sys.stderr)
            return 0
        dename, decolor = DES[dekey]
        color = cli_color if cli_color is not None else decolor
        print_banner(dename, color, cli_gradient, color_enabled, args.banner)
        return 0

    chosen_color = None
    catalog = DISTROS
    if args.random:
        key = random.choice(list(DISTROS))
    elif args.distro:
        key = resolve_key(args.distro)
        if key is None:
            color = cli_color if cli_color is not None else 81
            print_banner(args.distro, color, cli_gradient, color_enabled, args.banner)
            print(colorize(t("not_in_base") % args.distro, 240, color_enabled), file=sys.stderr)
            return 0
    else:
        if sys.stdin.isatty() and sys.stdout.isatty():
            result = interactive_flow()
            if result == CANCELLED:
                print(t("cancelled"))
                return 0
            mode, key, chosen_color = result
            catalog = DISTROS if mode == "distro" else DES
        else:
            key = detect_distro()
            if not key:
                print(colorize(t("no_detect"), 203, color_enabled), file=sys.stderr)
                return 1

    name, dcolor = catalog[key]
    gradient_spec = cli_gradient
    if isinstance(chosen_color, dict):
        gradient_spec = {"stops": chosen_color["gradient"], "type": chosen_color["type"]}
        color = dcolor
    elif cli_color is not None:
        color = cli_color
    elif isinstance(chosen_color, (int, tuple)):
        color = chosen_color
    else:
        color = dcolor
    print_banner(name, color, gradient_spec, color_enabled, args.banner)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit(130)
