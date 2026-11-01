#!/usr/bin/env python3
"""Generator for the GummiVital N°02 Feierabend-Komplex Klaviyo e-mail flows.

Builds 15 table-based, mobile-responsive HTML e-mails (Klaviyo CODE templates)
from one shared component library so all flows share the same design system.

    python3 email/feierabend/build.py

Output: email/feierabend/templates/*.html + manifest.json
"""
import json
import pathlib
import re

OUT = pathlib.Path(__file__).parent / "templates"

# --- Brand tokens (from the live theme: gv-feierabend sections + settings) ---
NAVY = "#1B2838"
NAVY2 = "#24344A"
GOLD = "#B8955A"
SAND = "#F3EAD9"
CREAM = "#F6F7F1"
INK = "#3B4658"
MUT = "#6B7587"
LINE = "#E3E6EA"
PILL = "#EEF1F5"

SHOP = "https://www.gummivital.de"
PDP = SHOP + "/products/gummivital-feierabend-komplex"
CODE = "FEIERABEND10"
PDP_CODE = f"{SHOP}/discount/{CODE}?redirect=/products/gummivital-feierabend-komplex"
CART = SHOP + "/cart"
CHECKOUT = "{{ event.extra.checkout_url|default:'" + CART + "' }}"

K = "https://cdn.klaviyomail.com/company/UZEf2V/images/"
IMG = {
    "hero": K + "2fb0ed56-97f7-4545-82a2-9d8f0a979b65.jpeg",
    "dose": K + "8164bbb7-1604-4fda-885b-051bbbbeb02d.jpeg",
    "pack": K + "9ab32e3b-a009-49bc-b676-f55f68ca2ff8.jpeg",
    "problem": K + "858681e1-cc1b-4950-a107-f9e3e57c3578.jpeg",
    "ashwa": K + "ee82cf07-73fe-4ccf-8b55-a02ab27efa51.jpeg",
    "melisse": K + "fed5884f-c7c3-4096-a2d5-a7b9e6f2fb84.jpeg",
    "kamille": K + "dd77eeb8-2c24-4172-b588-e7714b674992.jpeg",
    "lavendel": K + "31245461-8a79-4049-b951-6686828f946d.jpeg",
    "b6": K + "a1689453-fb57-4ce4-9777-1288a1b6a992.jpeg",
    "labor": K + "c54b412f-2655-4ce8-a986-63e1822e6848.jpeg",
    "life1": K + "d45c17e1-11d7-49e8-85fe-8c5d788460e4.jpeg",
    "life2": K + "f8459c34-d69c-4e7a-998a-6381d6511766.jpeg",
    "life3": K + "f5936087-7ce9-424d-a383-6a43c7c55703.jpeg",
    "life4": K + "80c55e65-9461-4a40-8608-ffde34d073b3.jpeg",
    "life5": K + "ae7b5991-cc25-45ed-8b20-b3cf1b13a2f1.jpeg",
    "life6": K + "70a487f9-03f1-4895-8fc6-ca43662e80d2.jpeg",
}

CSS = f"""
body{{margin:0;padding:0;background:{CREAM};-webkit-text-size-adjust:100%}}
table{{border-collapse:collapse}}img{{border:0;display:block;max-width:100%;height:auto}}
a{{color:{NAVY}}}
.f{{font-family:Montserrat,'Helvetica Neue',Arial,sans-serif}}
.w{{width:600px;max-width:600px;background:#ffffff}}
.p{{padding-left:40px;padding-right:40px}}
.eb{{font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:{GOLD}}}
.h1{{font-size:34px;line-height:40px;font-weight:800;letter-spacing:-.5px;color:{NAVY};margin:0}}
.h2{{font-size:26px;line-height:32px;font-weight:800;letter-spacing:-.3px;color:{NAVY};margin:0}}
.em{{color:{GOLD}}}
.t{{font-size:16px;line-height:26px;color:{INK};margin:0}}
.s{{font-size:13px;line-height:20px;color:{MUT};margin:0}}
.btn{{display:inline-block;background:{NAVY};color:#ffffff!important;text-decoration:none;font-size:15px;font-weight:700;letter-spacing:.04em;padding:17px 38px;border-radius:999px}}
.btng{{background:{GOLD};color:{NAVY}!important}}
.btnw{{background:#ffffff;color:{NAVY}!important}}
.card{{background:{CREAM};border-radius:18px}}
.dark{{background:{NAVY}}}
.dark .h1,.dark .h2{{color:#ffffff}}.dark .t{{color:#D5DAE2}}.dark .s{{color:#9AA5B5}}
.sand{{background:{SAND}}}
.chk{{color:{GOLD};font-weight:800}}
@media only screen and (max-width:620px){{
 .w{{width:100%!important}}
 .p{{padding-left:22px!important;padding-right:22px!important}}
 .h1{{font-size:28px!important;line-height:34px!important}}
 .h2{{font-size:23px!important;line-height:29px!important}}
 .stk{{display:block!important;width:100%!important;box-sizing:border-box}}
 .stk-pad{{padding:0 0 14px 0!important}}
 .hide-m{{display:none!important}}
 .btn{{display:block!important;text-align:center}}
 .code{{font-size:24px!important;letter-spacing:.06em!important}}
 .stat{{font-size:22px!important;line-height:26px!important}}
}}
"""


def minify(html):
    html = re.sub(r">\s+<", "><", html)
    return re.sub(r"\s{2,}", " ", html).strip()


# ----------------------------- components -----------------------------------
def row(inner, cls="", style=""):
    return f'<tr><td class="{cls}" style="{style}">{inner}</td></tr>'


def topbar(text):
    return row(
        f'<p class="f" style="margin:0;font-size:12px;font-weight:700;letter-spacing:.14em;'
        f'text-transform:uppercase;color:{NAVY}">{text}</p>',
        style=f"background:{GOLD};padding:11px 20px;text-align:center",
    )


def logo(bg="#ffffff"):
    return row(
        f'<a href="{SHOP}" style="text-decoration:none">'
        f'<span class="f" style="font-size:24px;font-weight:800;letter-spacing:-.5px;color:{NAVY}">'
        f'GummiVital<span style="color:{GOLD}">®</span></span><br>'
        f'<span class="f" style="font-size:10px;font-weight:700;letter-spacing:.32em;color:{MUT}">'
        f"N°02 · FEIERABEND-KOMPLEX</span></a>",
        style=f"background:{bg};padding:26px 20px 22px;text-align:center",
    )


def image(src, alt, href=PDP, pad="0", radius="0"):
    return row(
        f'<a href="{href}"><img src="{src}" width="600" alt="{alt}" '
        f'style="width:100%;border-radius:{radius}"></a>',
        style=f"padding:{pad}",
    )


def button(label, href, variant="", align="center"):
    return (
        f'<table role="presentation" align="{align}" style="margin:0 auto"><tr><td>'
        f'<a href="{href}" class="btn {variant} f">{label}</a></td></tr></table>'
    )


def text_block(eyebrow="", h="", em="", body="", cta=None, href=PDP, cls="", align="center",
               h_cls="h1", pad="44px 40px 44px", variant=""):
    parts = []
    if eyebrow:
        parts.append(f'<p class="eb f" style="margin:0 0 14px">{eyebrow}</p>')
    if h:
        emh = f' <span class="em">{em}</span>' if em else ""
        parts.append(f'<h1 class="{h_cls} f">{h}{emh}</h1>')
    if body:
        parts.append(f'<div class="t f" style="margin-top:16px">{body}</div>')
    if cta:
        parts.append(f'<div style="margin-top:28px">{button(cta, href, variant)}</div>')
    return row("".join(parts), cls=f"p {cls}", style=f"padding:{pad};text-align:{align}")


def spacer(h=24, bg="#ffffff"):
    return f'<tr><td style="height:{h}px;line-height:{h}px;font-size:1px;background:{bg}">&nbsp;</td></tr>'


def stats(items, bg=CREAM):
    w = int(100 / len(items))
    cells = "".join(
        f'<td class="f" width="{w}%" style="text-align:center;padding:22px 6px;vertical-align:top">'
        f'<div class="stat" style="font-size:30px;font-weight:800;color:{NAVY};line-height:34px">{n}</div>'
        f'<div style="font-size:11px;line-height:15px;color:{MUT};margin-top:6px;font-weight:600">{l}</div></td>'
        for n, l in items
    )
    return row(f'<table role="presentation" width="100%"><tr>{cells}</tr></table>',
               style=f"background:{bg};padding:6px 20px")


def ticks(items, color=INK):
    li = "".join(
        f'<tr><td class="f chk" style="width:26px;vertical-align:top;font-size:15px;padding:5px 0">✓</td>'
        f'<td class="f" style="font-size:15px;line-height:23px;color:{color};padding:5px 0">{i}</td></tr>'
        for i in items
    )
    return f'<table role="presentation" style="margin:0 auto;text-align:left">{li}</table>'


def trust_bar(bg=NAVY):
    items = ["60 Tage Geld-zurück", "Kein Abo", "Gratis-Versand mit DHL"]
    cells = "".join(
        f'<td class="f stk" style="text-align:center;padding:8px 4px;font-size:12px;font-weight:700;'
        f'letter-spacing:.06em;color:#ffffff"><span style="color:{GOLD}">✦</span>&nbsp; {i}</td>'
        for i in items
    )
    return row(f'<table role="presentation" width="100%"><tr>{cells}</tr></table>',
               style=f"background:{bg};padding:14px 20px")


def code_box(note="Gilt für deine erste Bestellung des Feierabend-Komplex."):
    return row(
        f'<table role="presentation" width="100%"><tr><td style="border:2px dashed {GOLD};border-radius:16px;'
        f'background:{SAND};padding:24px;text-align:center">'
        f'<p class="eb f" style="margin:0 0 8px;color:{NAVY}">Dein Code</p>'
        f'<p class="f code" style="margin:0;font-size:32px;font-weight:800;letter-spacing:.12em;color:{NAVY}">{CODE}</p>'
        f'<p class="s f" style="margin-top:8px">10 % Rabatt · {note}</p></td></tr></table>',
        cls="p", style="padding:0 40px 8px",
    )


def ingredients():
    data = [
        ("ashwa", "Ashwagandha", "300 mg Wurzel*"),
        ("melisse", "Zitronenmelisse", "240 mg Blätter*"),
        ("kamille", "Kamille", "132 mg Blüten*"),
        ("lavendel", "Lavendel", "16 mg Blüten*"),
        ("b6", "Vitamin B6", "2,8 mg · 200 % NRV"),
    ]

    def cell(k, n, d):
        return (
            f'<td width="33%" style="padding:0 5px 14px;vertical-align:top;text-align:center">'
            f'<img src="{IMG[k]}" width="170" alt="{n}" style="width:100%;border-radius:14px">'
            f'<p class="f" style="margin:10px 0 0;font-size:14px;font-weight:800;color:{NAVY}">{n}</p>'
            f'<p class="s f">{d}</p></td>'
        )

    r1 = "".join(cell(*d) for d in data[:3])
    r2 = "".join(cell(*d) for d in data[3:])
    return row(
        f'<table role="presentation" width="100%"><tr>{r1}</tr></table>'
        f'<table role="presentation" width="68%" align="center" style="margin:0 auto"><tr>{r2}</tr></table>'
        f'<p class="s f" style="text-align:center;font-size:11px;margin-top:4px">'
        f"*Pflanzenmenge, aus der der Extrakt einer Tagesportion (2 Gummies) gewonnen wird.</p>",
        cls="p", style="padding:4px 34px 30px",
    )


def compare():
    rows_ = [
        ("4 Pflanzen + Vitamin B6 in einer Portion", "✓", "–", "–"),
        ("Ohne Melatonin", "✓", "✓", "–"),
        ("Exakt dosiert pro Portion", "✓", "–", "✓"),
        ("Ohne Aufbrühen, überall dabei", "✓", "–", "✓"),
        ("60 Tage Geld-zurück", "✓", "–", "–"),
    ]
    head = (
        f'<tr><td class="f" style="padding:12px 10px;font-size:11px;color:{MUT}"></td>'
        f'<td class="f" style="background:{NAVY};color:#fff;border-radius:12px 12px 0 0;padding:12px 6px;'
        f'font-size:11px;font-weight:800;text-align:center;letter-spacing:.06em">FEIERABEND-<br>KOMPLEX</td>'
        f'<td class="f" style="padding:12px 6px;font-size:11px;font-weight:700;text-align:center;color:{MUT}">ABEND-<br>TEE</td>'
        f'<td class="f" style="padding:12px 6px;font-size:11px;font-weight:700;text-align:center;color:{MUT}">MELATONIN-<br>PRODUKTE</td></tr>'
    )
    body = ""
    for i, (f_, a, b, c) in enumerate(rows_):
        last = i == len(rows_) - 1
        rad = "border-radius:0 0 12px 12px;" if last else ""
        body += (
            f'<tr><td class="f" style="padding:13px 10px;font-size:13px;line-height:18px;color:{INK};border-top:1px solid {LINE}">{f_}</td>'
            f'<td class="f" style="background:{NAVY};{rad}color:{GOLD};font-size:18px;font-weight:800;text-align:center;border-top:1px solid {NAVY2}">{a}</td>'
            f'<td class="f" style="text-align:center;color:{MUT};font-size:16px;border-top:1px solid {LINE}">{b}</td>'
            f'<td class="f" style="text-align:center;color:{MUT};font-size:16px;border-top:1px solid {LINE}">{c}</td></tr>'
        )
    return row(f'<table role="presentation" width="100%">{head}{body}</table>',
               cls="p", style="padding:6px 30px 34px")


def myth_fact(pairs):
    out = ""
    for myth, fact in pairs:
        out += (
            f'<tr><td class="stk stk-pad" width="50%" style="padding:0 8px 16px 0;vertical-align:top">'
            f'<div style="background:#ffffff;border-radius:14px;padding:18px">'
            f'<span class="f" style="display:inline-block;background:#F7E1DE;color:#A2392B;font-size:10px;font-weight:800;'
            f'letter-spacing:.16em;padding:5px 12px;border-radius:999px">MYTHOS</span>'
            f'<p class="f" style="margin:12px 0 0;font-size:14px;line-height:21px;color:{INK}">{myth}</p></div></td>'
            f'<td class="stk stk-pad" width="50%" style="padding:0 0 16px 8px;vertical-align:top">'
            f'<div style="background:{NAVY};border-radius:14px;padding:18px">'
            f'<span class="f" style="display:inline-block;background:{GOLD};color:{NAVY};font-size:10px;font-weight:800;'
            f'letter-spacing:.16em;padding:5px 12px;border-radius:999px">FAKT</span>'
            f'<p class="f" style="margin:12px 0 0;font-size:14px;line-height:21px;color:#ffffff">{fact}</p></div></td></tr>'
        )
    return row(f'<table role="presentation" width="100%">{out}</table>', cls="p",
               style=f"background:{CREAM};padding:4px 40px 24px")


def review(quote, name, detail="Kundenstimme", img=None, bg="#ffffff"):
    pic = (
        f'<td class="hide-m" width="120" style="vertical-align:top;padding-right:18px">'
        f'<img src="{img}" width="120" alt="" style="border-radius:14px"></td>' if img else ""
    )
    return row(
        f'<table role="presentation" width="100%" class="card"><tr><td style="padding:24px">'
        f'<table role="presentation" width="100%"><tr>{pic}<td style="vertical-align:top">'
        f'<p class="f" style="margin:0;font-size:16px;letter-spacing:3px;color:{GOLD}">★★★★★</p>'
        f'<p class="f" style="margin:10px 0 0;font-size:16px;line-height:25px;color:{NAVY};font-weight:500">„{quote}“</p>'
        f'<p class="f" style="margin:12px 0 0;font-size:13px;font-weight:800;color:{NAVY}">{name}'
        f' <span style="font-weight:500;color:{MUT}">· {detail}</span></p>'
        f"</td></tr></table></td></tr></table>",
        cls="p", style=f"background:{bg};padding:0 40px 16px",
    )


def timeline():
    pts = [("17:30", "Laptop zu", False), ("19:00", "Abendessen", False),
           ("20:30", "Zwei Gummies", True), ("22:00", "Licht aus", False)]
    cells = ""
    for t, l, hi in pts:
        dot_bg = GOLD if hi else "#ffffff"
        col = GOLD if hi else "#ffffff"
        cells += (
            f'<td width="25%" class="f" style="text-align:center;vertical-align:top;padding:0 4px">'
            f'<div style="width:14px;height:14px;border-radius:50%;background:{dot_bg};border:2px solid {GOLD};margin:0 auto"></div>'
            f'<p style="margin:10px 0 0;font-size:18px;font-weight:800;color:{col}">{t}</p>'
            f'<p style="margin:4px 0 0;font-size:12px;line-height:16px;color:#C9D0DA">{l}</p></td>'
        )
    return row(f'<table role="presentation" width="100%"><tr>{cells}</tr></table>',
               cls="dark p", style=f"background:{NAVY};padding:6px 30px 40px")


def bundles(href=PDP, title="Wähle dein Paket", sub="Je mehr Abende, desto mehr sparst du.", eyebrow="Herbst-Aktion", cta="Paket auswählen"):
    offers = [
        ("1 Dose", "30 Abende", "29,99 €", "≈ 1,00 € pro Abend", "", False),
        ("2 Dosen + 1 gratis", "90 Abende · + 14-Tage-Reset-Guide gratis", "59,98 €", "≈ 0,67 € pro Abend",
         "BELIEBTESTE WAHL", True),
        ("3 Dosen + 2 gratis", "150 Abende · + alle 3 Bonus-Guides gratis", "89,97 €", "≈ 0,60 € pro Abend",
         "BESTER PREIS", False),
    ]
    cards = ""
    for n, d, p, per, badge, hi in offers:
        border = f"2px solid {GOLD}" if hi else f"1px solid {LINE}"
        bdg = (
            f'<span class="f" style="display:inline-block;background:{GOLD};color:{NAVY};font-size:10px;font-weight:800;'
            f'letter-spacing:.14em;padding:5px 12px;border-radius:999px;margin-bottom:10px">{badge}</span><br>'
            if badge else ""
        )
        cards += (
            f'<tr><td style="padding:0 0 12px"><a href="{href}" style="text-decoration:none">'
            f'<table role="presentation" width="100%" style="border:{border};border-radius:16px;background:#ffffff">'
            f'<tr><td style="padding:18px 20px">{bdg}'
            f'<p class="f" style="margin:0;font-size:17px;font-weight:800;color:{NAVY}">{n}</p>'
            f'<p class="s f" style="margin-top:3px">{d}</p></td>'
            f'<td style="padding:18px 20px;text-align:right;white-space:nowrap">'
            f'<p class="f" style="margin:0;font-size:19px;font-weight:800;color:{NAVY}">{p}</p>'
            f'<p class="f" style="margin:3px 0 0;font-size:12px;font-weight:700;color:{GOLD}">{per}</p></td></tr>'
            f"</table></a></td></tr>"
        )
    head = text_block(eyebrow, title, "", f"<p class='t'>{sub}</p>", pad="44px 40px 22px",
                      h_cls="h2")
    return head + row(
        f'<table role="presentation" width="100%">{cards}</table>'
        f'<div style="margin-top:14px">{button(cta, href)}</div>'
        f'<p class="s f" style="text-align:center;margin-top:14px">Kein Abo · einmaliger Kauf · Gratis-Versand</p>',
        cls="p", style="padding:0 40px 44px",
    )


def guarantee(bg=SAND, cta=None, href=PDP):
    btn = f'<div style="margin-top:22px">{button(cta, href)}</div>' if cta else ""
    return row(
        f'<table role="presentation" width="100%"><tr>'
        f'<td width="96" class="hide-m" style="vertical-align:middle;padding-right:20px">'
        f'<div style="width:92px;height:92px;border-radius:50%;background:{NAVY};text-align:center">'
        f'<p class="f" style="margin:0;padding-top:22px;font-size:28px;line-height:28px;font-weight:800;color:{GOLD}">60</p>'
        f'<p class="f" style="margin:4px 0 0;font-size:9px;font-weight:800;letter-spacing:.16em;color:#ffffff">TAGE</p></div></td>'
        f'<td style="vertical-align:middle"><p class="eb f" style="margin:0 0 8px">Unser Versprechen</p>'
        f'<p class="f" style="margin:0;font-size:20px;line-height:26px;font-weight:800;color:{NAVY}">60 Tage testen. Oder Geld zurück.</p>'
        f'<p class="t f" style="margin-top:8px;font-size:15px;line-height:23px">Wenn der Feierabend-Komplex nicht zu dir passt, '
        f"schreibst du uns eine E-Mail und bekommst dein Geld zurück. Kein Abo, keine Diskussion.</p>{btn}</td>"
        f"</tr></table>",
        cls="p", style=f"background:{bg};padding:34px 40px",
    )


def faq(items, bg="#ffffff"):
    out = "".join(
        f'<tr><td style="padding:16px 0;border-top:1px solid {LINE}">'
        f'<p class="f" style="margin:0;font-size:15px;font-weight:800;color:{NAVY}">{q}</p>'
        f'<p class="t f" style="margin-top:6px;font-size:14px;line-height:22px">{a}</p></td></tr>'
        for q, a in items
    )
    return row(f'<table role="presentation" width="100%">{out}</table>', cls="p",
               style=f"background:{bg};padding:0 40px 36px")


def lifestyle_grid(keys, caption="Symbolbilder"):
    cells = "".join(
        f'<td class="stk stk-pad" width="50%" style="padding:0 6px 12px;vertical-align:top">'
        f'<a href="{PDP}"><img src="{IMG[k]}" width="270" alt="Feierabend-Ritual" '
        f'style="width:100%;border-radius:16px"></a></td>'
        for k in keys
    )
    return row(f'<table role="presentation" width="100%"><tr>{cells}</tr></table>'
               f'<p class="s f" style="text-align:center;font-size:11px">{caption}</p>',
               cls="p", style="padding:0 34px 34px")


def split(img_key, eyebrow, h, em, body, cta=None, href=PDP, img_left=True, bg="#ffffff"):
    img = (f'<td class="stk stk-pad" width="46%" style="vertical-align:middle;padding:0 12px 0 0">'
           f'<img src="{IMG[img_key]}" width="250" alt="" style="width:100%;border-radius:18px"></td>')
    btn = f'<div style="margin-top:22px">{button(cta, href, align="left")}</div>' if cta else ""
    txt = (f'<td class="stk" width="54%" style="vertical-align:middle;padding:0 0 0 12px">'
           f'<p class="eb f" style="margin:0 0 10px">{eyebrow}</p>'
           f'<h2 class="h2 f">{h} <span class="em">{em}</span></h2>'
           f'<div class="t f" style="margin-top:12px;font-size:15px;line-height:24px">{body}</div>{btn}</td>')
    cells = img + txt if img_left else txt + img
    return row(f'<table role="presentation" width="100%"><tr>{cells}</tr></table>', cls="p",
               style=f"background:{bg};padding:36px 40px")


def product_card(img_src=IMG["dose"], name="GummiVital® Feierabend-Komplex",
                 meta="60 Mango-Gummies · 30 Abende", price="ab 29,99 €", href=PDP, cta="Jetzt ansehen"):
    return row(
        f'<table role="presentation" width="100%" class="card"><tr>'
        f'<td class="stk stk-pad" width="42%" style="padding:20px;vertical-align:middle">'
        f'<a href="{href}"><img src="{img_src}" width="210" alt="{name}" style="width:100%;border-radius:14px"></a></td>'
        f'<td class="stk" style="padding:20px 24px 24px 4px;vertical-align:middle">'
        f'<p class="f" style="margin:0;font-size:13px;letter-spacing:2px;color:{GOLD}">★★★★★</p>'
        f'<p class="f" style="margin:8px 0 0;font-size:19px;line-height:25px;font-weight:800;color:{NAVY}">{name}</p>'
        f'<p class="s f" style="margin-top:6px">{meta}</p>'
        f'<p class="f" style="margin:12px 0 18px;font-size:20px;font-weight:800;color:{NAVY}">{price}</p>'
        f'{button(cta, href, align="left")}</td></tr></table>',
        cls="p", style="padding:0 40px 30px",
    )


def cart_table():
    loop = (
        "{% for item in event.extra.line_items %}"
        f'<tr><td width="96" style="padding:14px 14px 14px 0;border-bottom:1px solid {LINE};vertical-align:middle">'
        f"<img src=\"{{{{ item.product.images.0.src|default:'{IMG['dose']}' }}}}\" width=\"84\" alt=\"\" style=\"border-radius:12px\"></td>"
        f'<td class="f" style="padding:14px 0;border-bottom:1px solid {LINE};vertical-align:middle">'
        f'<p style="margin:0;font-size:15px;line-height:21px;font-weight:800;color:{NAVY}">{{{{ item.product.title }}}}</p>'
        f'<p style="margin:4px 0 0;font-size:13px;color:{MUT}">Menge: {{{{ item.quantity|floatformat:0 }}}}</p></td>'
        f'<td class="f" style="padding:14px 0;border-bottom:1px solid {LINE};text-align:right;font-size:15px;'
        f'font-weight:800;color:{NAVY};white-space:nowrap">{{{{ item.line_price|floatformat:2 }}}} €</td></tr>'
        "{% endfor %}"
    )
    total = (
        f'<tr><td></td><td class="f" style="padding:14px 0 0;font-size:14px;color:{MUT}">Gesamt</td>'
        f'<td class="f" style="padding:14px 0 0;text-align:right;font-size:17px;font-weight:800;color:{NAVY}">'
        f"{{{{ event|lookup:'$value'|floatformat:2 }}}} €</td></tr>"
    )
    return row(
        f'<table role="presentation" width="100%" class="card"><tr><td style="padding:10px 22px 22px">'
        f'<p class="eb f" style="margin:14px 0 4px">Dein Warenkorb</p>'
        f'<table role="presentation" width="100%">{loop}{total}</table>'
        f'<div style="margin-top:22px">{button("Zurück zur Kasse", CHECKOUT)}</div></td></tr></table>',
        cls="p", style="padding:0 40px 30px",
    )


def footer(reason="du dich bei GummiVital angemeldet oder unseren Shop besucht hast"):
    links = " &nbsp;·&nbsp; ".join(
        f'<a href="{u}" style="color:#C9D0DA;text-decoration:none">{l}</a>'
        for l, u in [("Shop", PDP), ("FAQ", SHOP + "/pages/faq"), ("Kontakt", SHOP + "/pages/contact")]
    )
    return row(
        f'<p class="f" style="margin:0;font-size:22px;font-weight:800;color:#ffffff">GummiVital<span style="color:{GOLD}">®</span></p>'
        f'<p class="f" style="margin:6px 0 18px;font-size:12px;color:#9AA5B5">Gib deinem Tag einen Schlusspunkt.</p>'
        f'<p class="f" style="margin:0 0 20px;font-size:12px;font-weight:700;letter-spacing:.08em">{links}</p>'
        f'<p class="f" style="margin:0;font-size:11px;line-height:17px;color:#9AA5B5">'
        f"Nahrungsergänzungsmittel. Kein Ersatz für eine ausgewogene, abwechslungsreiche Ernährung und gesunde Lebensweise. "
        f"Die angegebene empfohlene tägliche Verzehrmenge darf nicht überschritten werden. Außerhalb der Reichweite von Kindern "
        f"aufbewahren. Nicht geeignet für Schwangere, Stillende, Kinder und Jugendliche. Kann bei übermäßigem Verzehr abführend wirken.</p>"
        f'<p class="f" style="margin:16px 0 0;font-size:11px;line-height:17px;color:#9AA5B5">'
        f"{{{{ organization.name }}}} · {{{{ organization.full_address }}}}<br>"
        f"Du erhältst diese E-Mail, weil {reason}.<br>"
        f"<span style=\"color:#C9D0DA\">{{% unsubscribe 'Abmelden' %}}</span> &nbsp;·&nbsp; "
        f"<span style=\"color:#C9D0DA\">{{% web_view 'Im Browser ansehen' %}}</span></p>",
        style=f"background:{NAVY};padding:40px 40px 44px;text-align:center",
    )


def page(title, preheader, rows):
    body = "".join(rows)
    pre = (f'<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent">'
           f'{preheader}{"&#847;&zwnj;&nbsp;" * 12}</div>')
    return minify(f"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting">
<title>{title}</title>
<style>{CSS}</style></head><body>{pre}
<table role="presentation" width="100%" style="background:{CREAM}"><tr><td align="center" style="padding:0">
<table role="presentation" class="w" width="600" style="width:600px;background:#ffffff">{body}</table>
</td></tr></table></body></html>""")


# ------------------------------- shared copy ---------------------------------
R_TIM = ("Ist es ein Wundermittel? Nein. […] Aber: Ich liege nicht mehr stundenlang wach und wälze Probleme. […] "
         "Als tägliche Unterstützung sind die Gummis ihr Geld wert", "Tim G.")
R_CHRISTINA = ("Und ich muss nicht drei verschiedene Kapseln und einen Tee nehmen, sondern kaue einfach zwei leckere "
               "Gummis. Fertig.", "Christina V.")
R_MIKE = ("Dann die GummiVital gefunden. […] Kein einziges Magenproblem. Nehm die jetzt seit 6 Wochen jeden Abend.",
          "Mike L.")
R_NADIA = ("Die Gummis vertrage ich einwandfrei, seit 2 Monaten jetzt […]. Wer unsicher ist: Einfach mal eine Packung "
           "probieren und auf den eigenen Körper hören.", "Nadia H.")

STATS = [("5", "Wirkstoffe,<br>offen deklariert"), ("2", "Mango-Gummies<br>pro Abend"),
         ("0 g", "Zucker"), ("0 mg", "Melatonin")]

FAQ_CORE = [
    ("Enthält der Feierabend-Komplex Melatonin?", "Nein. Keine Hormone – nur vier Pflanzenextrakte und Vitamin B6."),
    ("Wie nehme ich ihn ein?", "2 Gummies am Abend kauen, etwa 1–2 Stunden vor dem Schlafengehen. Ohne Wasser, ohne Aufwand."),
    ("Schließe ich ein Abo ab?", "Nein. Du kaufst einmalig – keine versteckten Kosten, keine Kündigung nötig."),
    ("Was, wenn es nicht zu mir passt?", "Dann schreibst du uns innerhalb von 60 Tagen eine E-Mail und bekommst dein Geld zurück."),
]

B6_NOTE = row('<p class="s f" style="text-align:center;font-size:11px">Vitamin B6 trägt zu einer normalen psychischen '
              "Funktion sowie zur Verringerung von Müdigkeit und Ermüdung bei.</p>", cls="p", style="padding:0 40px 28px")

# --------------------------------- e-mails -----------------------------------
EMAILS = []


def email(slug, flow, name, delay, subject, preheader, rows):
    EMAILS.append(dict(slug=slug, flow=flow, name=name, delay=delay, subject=subject,
                       preheader=preheader, html=page(subject, preheader, rows)))


# ============ WELCOME FLOW ============
email("welcome-1", "Welcome", "FK | Welcome 1/5 – Willkommen + Code", "sofort",
      "Dein Feierabend-Geschenk wartet 🌙",
      "10 % auf deinen ersten Feierabend-Komplex – dein Code ist drin.",
      [topbar("Willkommen · 10 % auf deine erste Bestellung"), logo(), image(IMG["hero"], "Feierabend-Komplex"),
       text_block("Willkommen bei GummiVital", "Der Tag ist erledigt.", "Jetzt beginnt dein Abend.",
                  "<p class='t'>Schön, dass du da bist. Du kennst das: Die Jacke hängt, aber der Kopf ist noch im Büro. "
                  "Genau dafür gibt es den <b>Feierabend-Komplex</b> – zwei Mango-Gummies als fester Schlusspunkt "
                  "für deinen Tag.</p><p class='t' style='margin-top:14px'>Als Dankeschön für deine Anmeldung bekommst du "
                  "<b>10 % auf deine erste Bestellung</b>:</p>", pad="44px 40px 26px"),
       code_box(),
       row(f'<div style="padding-top:22px">{button("Code jetzt einlösen", PDP_CODE)}</div>'
           '<p class="s f" style="text-align:center;margin-top:12px">Der Code wird beim Klick automatisch angewendet.</p>',
           cls="p", style="padding:0 40px 40px;text-align:center"),
       stats(STATS),
       text_block("Was dich erwartet", "Zwei Gummies.", "Ein Ritual.",
                  ticks(["Ashwagandha, Zitronenmelisse, Kamille, Lavendel + Vitamin B6",
                         "Ohne Melatonin · ohne Zucker · vegan",
                         "Fruchtig nach Mango – kein bitterer Nachgeschmack",
                         "Hergestellt in Deutschland, laborgeprüft"]),
                  cta="Feierabend-Komplex entdecken", href=PDP_CODE, h_cls="h2"),
       guarantee(), B6_NOTE, trust_bar(), footer()])

email("welcome-2", "Welcome", "FK | Welcome 2/5 – Problem & Ritual", "+1 Tag",
      "Dein Kopf hat noch nicht Feierabend?",
      "Und plötzlich ist es elf. Warum dein Abend einen Schlusspunkt braucht.",
      [logo(), image(IMG["problem"], "Feierabend"),
       text_block("Der Moment", "Feierabend ist erst,", "wenn du ihn dir nimmst.",
                  "<p class='t'>Die Mails laufen weiter, nur eben auf dem Sofa. Es gibt keinen Moment, der dir sagt: "
                  "<i>Jetzt ist der Tag vorbei.</i> Und plötzlich ist es elf – der Abend, auf den du dich gefreut hast, "
                  "ist einfach durchgerutscht.</p>"),
       row(f'<table role="presentation" width="100%">' + "".join(
           f'<tr><td style="padding:0 0 12px"><table role="presentation" width="100%" class="card"><tr>'
           f'<td class="f" width="54" style="padding:18px 0 18px 20px;font-size:22px;font-weight:800;color:{GOLD};vertical-align:top">{n}</td>'
           f'<td style="padding:18px 20px 18px 6px"><p class="f" style="margin:0;font-size:16px;font-weight:800;color:{NAVY}">{t}</p>'
           f'<p class="s f" style="margin-top:4px;font-size:14px;line-height:21px">{d}</p></td></tr></table></td></tr>'
           for n, t, d in [("01", "Die Jacke hängt, das Handy nicht.", "Mails, Chats, Nachrichten – der Arbeitstag läuft einfach weiter."),
                           ("02", "Es gibt keinen Schlusspunkt.", "Kein Signal, das deinem Kopf sagt: Jetzt ist Schluss."),
                           ("03", "Und plötzlich ist es elf.", "Der Abend ist weg – und morgen geht alles von vorne los.")])
           + "</table>", cls="p", style="padding:0 40px 30px"),
       text_block("Dein Ritual", "Ein klarer Schlusspunkt", "für jeden Abend.",
                  "<p class='t'>Zwei Gummies, jeden Abend zur gleichen Zeit. Ein kleines Ritual, das deinem Tag ein Ende gibt – "
                  "so einfach, dass du es wirklich jeden Tag durchziehst.</p>", cls="dark", h_cls="h2",
                  pad="44px 40px 30px"),
       timeline(),
       lifestyle_grid(["life1", "life2"]),
       text_block("", "Dein Feierabend.", "Wie du ihn willst.",
                  "<p class='t'>Auf dem Sofa, auf dem Balkon, nach dem Training oder mit einem Buch im Bett – "
                  "zwei Gummies passen in jeden Abend.</p>", cta="Mein Ritual starten (−10 %)", href=PDP_CODE,
                  h_cls="h2", pad="10px 40px 44px"),
       trust_bar(), footer()])

email("welcome-3", "Welcome", "FK | Welcome 3/5 – Formel & Transparenz", "+2 Tage",
      "5 Zutaten. Keine Geheimnisse.",
      "Was genau in deinen zwei Gummies steckt – mit exakter Menge.",
      [logo(), text_block("Die Formel", "Fünf Zutaten.", "Keine Geheimnisse.",
                          "<p class='t'>Kein versteckter Blend, keine Alibi-Mengen. Jede Zutat steht mit ihrer genauen Menge "
                          "auf der Dose – und hier.</p>", pad="40px 40px 28px"),
       ingredients(),
       stats(STATS),
       text_block("Mythos vs. Fakt", "Nicht jedes Abendritual", "ist gleich.", "", h_cls="h2",
                  cls="", pad="44px 40px 22px", ),
       myth_fact([("„Gummies sind doch nur Süßigkeiten.“",
                   "Jede Portion enthält 4 Pflanzenextrakte + 2,8 mg Vitamin B6 (200 % NRV) – zuckerfrei."),
                  ("„Für den Abend brauche ich Melatonin.“",
                   "Der Feierabend-Komplex kommt komplett ohne Melatonin und ohne Hormone aus."),
                  ("„Ein Tee tut es auch.“",
                   "Tee musst du aufbrühen – und die Menge variiert. Hier ist jede Portion exakt dosiert.")]),
       split("labor", "Laborgeprüft", "Geprüft.", "Nicht versprochen.",
             "<p>Hergestellt in Deutschland und unabhängig im Labor analysiert. Das Prüfprotokoll findest du "
             "direkt auf der Produktseite.</p>", cta="Formel ansehen"),
       text_block("Der Vergleich", "Mehr als ein Tee.", "Ohne Melatonin.", "", h_cls="h2", pad="10px 40px 18px"),
       compare(),
       row(button("Jetzt 10 % sichern", PDP_CODE), style="padding:0 40px 40px;text-align:center"),
       B6_NOTE, trust_bar(), footer()])

email("welcome-4", "Welcome", "FK | Welcome 4/5 – Social Proof & FAQ", "+2 Tage",
      "„Ist es ein Wundermittel? Nein.“",
      "Warum wir diese ehrliche Bewertung besonders mögen.",
      [logo(), text_block("Echte Stimmen", "Ehrlich gesagt:", "kein Wundermittel.",
                          "<p class='t'>Wir versprechen dir keine Wunder. Wir versprechen dir ein Ritual, das so einfach ist, "
                          "dass du es jeden Abend durchziehst. Das sagen andere nach ein paar Wochen:</p>", pad="40px 40px 28px"),
       review(*R_TIM, img=IMG["life3"]), review(*R_CHRISTINA, img=IMG["life4"]), review(*R_MIKE, img=IMG["life5"]),
       row(button("Selbst ausprobieren (−10 %)", PDP_CODE), style="padding:18px 40px 44px;text-align:center"),
       text_block("FAQ", "Gute Fragen.", "Klare Antworten.", "", h_cls="h2", pad="40px 40px 16px", cls="sand"),
       faq(FAQ_CORE, bg=SAND),
       guarantee(bg="#ffffff", cta="Risikofrei testen", href=PDP_CODE),
       trust_bar(), footer()])

email("welcome-5", "Welcome", "FK | Welcome 5/5 – Letzte Chance Code + Bundles", "+2 Tage",
      "Dein 10 % Code läuft bald ab ⏳",
      "Letzte Erinnerung: Sichere dir deinen Willkommensrabatt.",
      [topbar("Letzte Erinnerung · Dein Code läuft bald ab"), logo(),
       text_block("Nur noch kurz", "Dein Willkommens-Code", "läuft bald ab.",
                  "<p class='t'>Wir wollten sichergehen, dass du ihn nicht verpasst: Mit deinem Code sparst du "
                  "<b>10 % auf deinen ersten Feierabend-Komplex</b>.</p>",
                  pad="36px 40px 26px"),
       code_box(),
       spacer(10),
       image(IMG["pack"], "Feierabend-Komplex", pad="0 40px", radius="18px"),
       bundles(href=PDP_CODE, title="Mehr Abende.", sub="Unser Tipp: Starte mit 3 Dosen – 90 Abende für ein echtes Ritual."),
       guarantee(), trust_bar(), footer()])

# ============ ABANDONED CHECKOUT ============
email("checkout-1", "Abandoned Checkout", "FK | Checkout 1/3 – Erinnerung", "1 Std.",
      "Dein Feierabend wartet noch an der Kasse",
      "Wir haben deinen Warenkorb für dich gespeichert.",
      [logo(), text_block("Fast geschafft", "Du warst nur einen Klick", "vom Feierabend entfernt.",
                          "<p class='t'>Kein Stress – wir haben deinen Warenkorb gespeichert. "
                          "Du kannst genau dort weitermachen, wo du aufgehört hast.</p>", pad="40px 40px 28px"),
       cart_table(),
       stats(STATS),
       text_block("", "Warum der Feierabend-Komplex?", "", ticks([
           "5 Wirkstoffe, jede Menge offen deklariert", "Ohne Melatonin · ohne Zucker · vegan",
           "Kein Abo – du kaufst einmalig", "Versand in 1–3 Werktagen mit DHL – gratis"]),
           cta="Bestellung abschließen", href=CHECKOUT, h_cls="h2"),
       guarantee(), trust_bar(), footer()])

email("checkout-2", "Abandoned Checkout", "FK | Checkout 2/3 – Einwände & Social Proof", "+23 Std.",
      "Noch unsicher? Das fragen sich viele.",
      "Melatonin, Abo, Garantie – die ehrlichen Antworten.",
      [logo(), image(IMG["life6"], "Feierabend-Ritual"),
       text_block("Kurze Frage", "Noch unsicher?", "Völlig normal.",
                  "<p class='t'>Bevor man etwas Neues in seine Abendroutine aufnimmt, will man es genau wissen. "
                  "Hier sind die Antworten auf die Fragen, die uns am häufigsten gestellt werden.</p>",
                  pad="40px 40px 20px"),
       faq(FAQ_CORE),
       review(*R_NADIA, bg="#ffffff"),
       spacer(10),
       cart_table(),
       guarantee(), trust_bar(), footer()])

email("checkout-3", "Abandoned Checkout", "FK | Checkout 3/3 – 10 % Rabatt", "+24 Std.",
      "10 % für deinen ersten Feierabend – nur für dich",
      "Dein Warenkorb ist noch da. Und jetzt gibt’s 10 % on top.",
      [topbar("Exklusiv für dich · 10 % Rabatt"), logo(),
       text_block("Ein kleiner Schubs", "Dein Warenkorb ist noch da.", "Jetzt mit 10 %.",
                  "<p class='t'>Wir möchten, dass du den Feierabend-Komplex ganz entspannt testen kannst. "
                  "Deshalb bekommst du <b>10 % auf deine Bestellung</b> – gib einfach diesen Code an der Kasse ein:</p>",
                  pad="36px 40px 26px"),
       code_box("An der Kasse im Feld „Rabattcode“ eingeben."),
       spacer(16),
       cart_table(),
       bundles(href=PDP_CODE, title="Oder gleich für 90 Abende?",
               sub="Mit dem 2+1-Paket zahlst du nur ≈ 0,67 € pro Abend."),
       guarantee(), trust_bar(), footer()])

# ============ ABANDONED CART (Added to Cart) ============
email("cart-1", "Abandoned Cart", "FK | Warenkorb 1/2 – Erinnerung", "2 Std.",
      "Hast du etwas vergessen?",
      "Dein Feierabend-Komplex liegt noch im Warenkorb.",
      [logo(), text_block("Im Warenkorb", "Dein Feierabend", "liegt noch im Warenkorb.",
                          "<p class='t'>Du hast den Feierabend-Komplex in deinen Warenkorb gelegt – wir halten ihn für dich bereit.</p>",
                          pad="40px 40px 28px"),
       product_card(href=CART, cta="Zum Warenkorb", price="ab 29,99 €"),
       stats(STATS),
       split("life2", "Dein Ritual", "Zwei Gummies.", "Jeden Abend.",
             "<p>Fruchtig nach Mango, ohne Zucker, ohne Melatonin. Zwei Gummies als Schlusspunkt für deinen Tag – "
             "ohne Wasser, ohne Aufwand.</p>", cta="Jetzt abschließen", href=CART),
       guarantee(), trust_bar(), footer()])

email("cart-2", "Abandoned Cart", "FK | Warenkorb 2/2 – Social Proof + Pakete", "+1 Tag",
      "„…kaue einfach zwei leckere Gummis. Fertig.“",
      "Was andere über ihren neuen Feierabend sagen.",
      [logo(), image(IMG["hero"], "Feierabend-Komplex"),
       text_block("Echte Stimmen", "Einfacher", "geht Feierabend nicht.", "", h_cls="h2", pad="36px 40px 20px"),
       review(*R_CHRISTINA), review(*R_TIM),
       bundles(href=CART, title="Dein Warenkorb wartet.", sub="Tipp: Mit 2+1 bekommst du 90 Abende zum Preis von 60."),
       guarantee(), trust_bar(), footer()])

# ============ BROWSE ABANDONMENT ============
BROWSE_IMG = "{{ event.ImageURL|default:'" + IMG["dose"] + "' }}"
BROWSE_URL = "{{ event.URL|default:'" + PDP + "' }}"

email("browse-1", "Browse Abandonment", "FK | Browse 1/3 – Produkt-Erinnerung", "2 Std.",
      "Noch am Überlegen?",
      "Der Feierabend-Komplex – alles auf einen Blick.",
      [logo(), text_block("Gerade angesehen", "Noch am", "Überlegen?",
                          "<p class='t'>Du hast dir den Feierabend-Komplex angesehen. Hier noch mal alles Wichtige auf einen Blick.</p>",
                          pad="40px 40px 28px"),
       product_card(img_src=BROWSE_IMG, href=BROWSE_URL),
       stats(STATS),
       text_block("Auf einen Blick", "Alles, was zählt.", "In zwei Gummies.", ticks([
           "Ashwagandha, Zitronenmelisse, Kamille, Lavendel + Vitamin B6",
           "Ohne Melatonin · ohne Zucker · vegan", "Hergestellt in Deutschland",
           "60 Tage Geld-zurück · kein Abo"]), cta="Zum Feierabend-Komplex", href=BROWSE_URL, h_cls="h2"),
       B6_NOTE, trust_bar(), footer()])

email("browse-2", "Browse Abandonment", "FK | Browse 2/3 – Vergleich", "+1 Tag",
      "Mehr als ein Tee. Ohne Melatonin.",
      "Warum der Feierabend-Komplex anders ist als Tee oder Melatonin.",
      [logo(), image(IMG["pack"], "Feierabend-Komplex", pad="30px 40px 0", radius="18px"),
       text_block("Der Vergleich", "Mehr als ein Tee.", "Ohne Melatonin.",
                  "<p class='t'>Vier Pflanzen und Vitamin B6, genau dosiert in einer Portion – ohne Aufbrühen und ohne Hormon.</p>",
                  pad="36px 40px 18px"),
       compare(),
       review(*R_MIKE, img=IMG["life5"], bg="#ffffff"),
       row(button("Jetzt entdecken", BROWSE_URL), style="padding:18px 40px 44px;text-align:center"),
       trust_bar(), footer()])

email("browse-3", "Browse Abandonment", "FK | Browse 3/3 – Garantie + Pakete", "+2 Tage",
      "Teste ihn 60 Tage – ohne Risiko",
      "Passt er nicht zu dir, bekommst du dein Geld zurück.",
      [logo(), guarantee(bg=SAND),
       text_block("Ohne Risiko", "Probier’s einfach aus.", "60 Tage lang.",
                  "<p class='t'>Du musst dich nicht heute entscheiden, ob der Feierabend-Komplex für immer zu dir passt. "
                  "Teste ihn in Ruhe – und wenn nicht, gibt’s dein Geld zurück.</p>", pad="40px 40px 10px"),
       lifestyle_grid(["life3", "life6"]),
       bundles(href=BROWSE_URL),
       trust_bar(), footer()])

# ============ SITE ABANDONMENT ============
email("site-1", "Site Abandonment", "FK | Site 1/2 – Willkommen zurück", "1 Std.",
      "Schön, dass du vorbeigeschaut hast",
      "Gib deinem Tag einen Schlusspunkt – so funktioniert’s.",
      [logo(), image(IMG["hero"], "Feierabend-Komplex"),
       text_block("Schön, dass du da warst", "Gib deinem Tag", "einen Schlusspunkt.",
                  "<p class='t'>Du warst gerade bei uns im Shop. Falls du dich fragst, was GummiVital eigentlich ist: "
                  "Wir machen den <b>Feierabend-Komplex</b> – zwei Mango-Gummies mit Ashwagandha, Zitronenmelisse, "
                  "Kamille, Lavendel und Vitamin B6. Als festes Ritual für den Moment, in dem du den Tag hinter dir lässt.</p>",
                  cta="Feierabend-Komplex entdecken"),
       stats(STATS),
       text_block("Dein Ritual", "Ein klarer Schlusspunkt", "für jeden Abend.", "", cls="dark", h_cls="h2",
                  pad="44px 40px 30px"),
       timeline(),
       trust_bar(bg=NAVY2), footer()])

email("site-2", "Site Abandonment", "FK | Site 2/2 – Pakete + Garantie", "+1 Tag",
      "Heute Abend schon Feierabend im Kopf?",
      "Zwei Gummies. Jeden Abend. Und der Feierabend gehört wieder dir.",
      [logo(), split("problem", "Heute Abend", "Zwei Gummies.", "Jeden Abend.",
                     "<p>Und der Feierabend gehört wieder dir. Ohne Melatonin, ohne Zucker – einfach als Ritual.</p>",
                     cta="Jetzt entdecken"),
       review(*R_TIM, bg="#ffffff"),
       bundles(),
       guarantee(), trust_bar(), footer()])


# ============ POST-PURCHASE + NACHKAUF ============
REVIEW_URL = PDP + "#judgeme_product_reviews"
HELLO = "{{ first_name|default:'du' }}"
BUYER = "du bei GummiVital bestellt hast"


def steps(items, bg="#ffffff"):
    cells = "".join(
        f'<td class="stk stk-pad" width="33%" style="padding:0 6px;vertical-align:top">'
        f'<table role="presentation" width="100%" class="card"><tr><td style="padding:20px 16px;text-align:center">'
        f'<div class="f" style="width:40px;height:40px;line-height:40px;border-radius:50%;background:{NAVY};color:{GOLD};'
        f'font-size:16px;font-weight:800;margin:0 auto">{i + 1}</div>'
        f'<p class="f" style="margin:12px 0 0;font-size:15px;font-weight:800;color:{NAVY}">{t}</p>'
        f'<p class="s f" style="margin-top:6px;font-size:13px;line-height:19px">{d}</p></td></tr></table></td>'
        for i, (t, d) in enumerate(items)
    )
    return row(f'<table role="presentation" width="100%"><tr>{cells}</tr></table>', cls="p",
               style=f"background:{bg};padding:0 34px 34px")


def supply_bar(day, total, label):
    left = total - day
    pct_used = int(100 * day / total)
    return row(
        f'<table role="presentation" width="100%" class="card"><tr><td style="padding:24px">'
        f'<p class="eb f" style="margin:0 0 10px">Dein Vorrat</p>'
        f'<p class="f" style="margin:0;font-size:22px;font-weight:800;color:{NAVY}">{label}</p>'
        f'<table role="presentation" width="100%" style="margin-top:16px"><tr>'
        f'<td width="{pct_used}%" style="height:12px;background:{GOLD};border-radius:999px 0 0 999px;font-size:1px;line-height:1px">&nbsp;</td>'
        f'<td style="height:12px;background:{LINE};border-radius:0 999px 999px 0;font-size:1px;line-height:1px">&nbsp;</td></tr></table>'
        f'<table role="presentation" width="100%" style="margin-top:8px"><tr>'
        f'<td class="s f" style="font-size:12px">Abend {day}</td>'
        f'<td class="s f" style="font-size:12px;text-align:right">noch ca. {left} Abende</td></tr></table>'
        f'</td></tr></table>',
        cls="p", style="padding:0 40px 30px",
    )


def stars_cta():
    stars = "".join(
        f'<td style="padding:0 4px"><a href="{REVIEW_URL}" style="text-decoration:none;font-size:34px;color:{GOLD}" '
        f'aria-label="{n} Sterne">★</a></td>' for n in range(1, 6)
    )
    return row(
        f'<table role="presentation" align="center" style="margin:0 auto"><tr>{stars}</tr></table>'
        f'<p class="s f" style="text-align:center;margin-top:8px">Tippe auf die Sterne, um deine Bewertung zu schreiben.</p>'
        f'<div style="margin-top:22px">{button("Bewertung schreiben", REVIEW_URL)}</div>',
        cls="p", style="padding:0 40px 40px;text-align:center",
    )


FAQ_USE = [
    ("Wann nehme ich die Gummies?", "Am besten jeden Abend zur gleichen Zeit, etwa 1–2 Stunden vor dem Schlafengehen. Zwei Gummies kauen, ohne Wasser."),
    ("Was, wenn ich einen Abend vergesse?", "Kein Problem. Einfach am nächsten Abend wie gewohnt weitermachen, nicht doppelt nehmen."),
    ("Kann ich mehr als zwei nehmen?", "Bitte nicht. Die empfohlene Verzehrmenge sind 2 Gummies pro Tag."),
    ("Ich nehme Medikamente – ist das okay?", "Sprich vorher kurz mit deinem Arzt oder deiner Apotheke. Nicht geeignet für Schwangere, Stillende, Kinder und Jugendliche."),
]

email("pp-1", "Post-Purchase", "FK | Nach dem Kauf 1/3 – Danke + Einnahme", "sofort",
      "Willkommen im Feierabend-Club 🌙",
      "So holst du das Beste aus deinen ersten Abenden.",
      [topbar("Danke für deine Bestellung"), logo(), image(IMG["pack"], "Feierabend-Komplex", pad="0 40px", radius="18px"),
       text_block("Schön, dass du dabei bist", "Danke für dein Vertrauen.", "Dein Feierabend ist unterwegs.",
                  "<p class='t'>Deine Bestellung ist bei uns eingegangen und geht in 1–3 Werktagen mit DHL raus. "
                  "Die Versandbestätigung mit Sendungsnummer kommt separat.</p>"
                  "<p class='t' style='margin-top:14px'>Damit dein neues Ritual vom ersten Abend an sitzt, hier die drei Dinge, "
                  "auf die es ankommt:</p>", pad="40px 40px 28px"),
       steps([("Feste Uhrzeit", "Jeden Abend zur gleichen Zeit, etwa 1–2 Stunden vor dem Schlafengehen."),
              ("Zwei Gummies", "Kauen, genießen, fertig. Kein Wasser, keine Kapseln."),
              ("Schlusspunkt setzen", "Danach Laptop zu, Handy weg. Das Ritual sagt deinem Tag: Ende.")]),
       text_block("Beispiel-Abend", "Ein klarer Schlusspunkt", "für jeden Abend.", "", cls="dark", h_cls="h2",
                  pad="44px 40px 30px"),
       timeline(),
       text_block("", "Gib dem Ritual Zeit.", "",
                  "<p class='t'>Neue Routinen fühlen sich oft erst nach ein paar Wochen selbstverständlich an. "
                  "Bleib dran, jeden Abend, auch am Wochenende. Wenn du nach 60 Tagen merkst, dass es nicht zu dir passt, "
                  "bekommst du dein Geld zurück.</p>", h_cls="h2", pad="44px 40px 20px"),
       faq(FAQ_USE),
       guarantee(), B6_NOTE, trust_bar(), footer(BUYER)])

email("pp-2", "Post-Purchase", "FK | Nach dem Kauf 2/3 – Ritual-Tipps", "+6 Tage",
      "3 Gewohnheiten für einen echten Feierabend",
      "Kleine Schritte, die dein Abendritual noch runder machen.",
      [logo(), image(IMG["life1"], "Feierabend-Ritual", pad="0 40px", radius="18px"),
       text_block("Dein Ritual", "Drei kleine Gewohnheiten,", "die viel ausmachen.",
                  f"<p class='t'>Hey {HELLO}, deine ersten Abende mit dem Feierabend-Komplex liegen hinter dir. "
                  "Diese drei Gewohnheiten passen perfekt dazu und kosten keine fünf Minuten:</p>", pad="40px 40px 26px"),
       row("".join(
           f'<table role="presentation" width="100%" class="card" style="margin-bottom:12px"><tr>'
           f'<td class="f" width="54" style="padding:18px 0 18px 20px;font-size:22px;font-weight:800;color:{GOLD};vertical-align:top">{n}</td>'
           f'<td style="padding:18px 20px 18px 6px"><p class="f" style="margin:0;font-size:16px;font-weight:800;color:{NAVY}">{t}</p>'
           f'<p class="s f" style="margin-top:4px;font-size:14px;line-height:21px">{d}</p></td></tr></table>'
           for n, t, d in [
               ("01", "Morgen-Liste schreiben", "Notier dir die drei Dinge, die morgen anstehen. Was auf dem Papier steht, muss nicht mehr im Kopf kreisen."),
               ("02", "Bildschirme aus, Licht runter", "30 Minuten vor dem Schlafengehen Handy weglegen und gedimmtes Licht statt Deckenlampe."),
               ("03", "Gummies als Signal", "Nimm sie immer an derselben Stelle, zum Beispiel auf dem Sofa nach dem Abendessen. So wird daraus ein Ritual."),
           ]), cls="p", style="padding:0 40px 30px"),
       lifestyle_grid(["life2", "life4"]),
       text_block("", "Du bist nicht allein.", "",
                  "<p class='t'>Fragen zur Einnahme oder Feedback? Antworte einfach auf diese Mail, wir lesen jede Nachricht.</p>",
                  h_cls="h2", pad="10px 40px 40px"),
       trust_bar(), footer(BUYER)])

email("pp-3", "Post-Purchase", "FK | Nach dem Kauf 3/3 – Bewertung", "+8 Tage",
      "Wie gefällt dir dein Feierabend-Ritual?",
      "Deine ehrliche Meinung hilft anderen bei der Entscheidung.",
      [logo(), text_block("Deine Meinung zählt", f"Hey {HELLO}, wie läuft", "dein Feierabend?",
                          "<p class='t'>Du hast den Feierabend-Komplex jetzt seit etwa zwei Wochen. Wir würden gern wissen, "
                          "wie es dir damit geht – ehrlich, auch wenn noch nicht alles perfekt ist. "
                          "Deine Bewertung hilft anderen, die gerade vor der gleichen Entscheidung stehen.</p>",
                          pad="44px 40px 26px"),
       stars_cta(),
       split("life3", "Nicht ganz zufrieden?", "Sag es uns.", "Wir hören zu.",
             "<p>Wenn etwas nicht passt – Geschmack, Einnahme, Versand – antworte einfach auf diese Mail. "
             "Und denk dran: Du hast 60 Tage Geld-zurück-Garantie.</p>", bg=CREAM),
       trust_bar(), footer(BUYER)])

email("ro-1", "Nachkauf (1 Dose)", "FK | Nachkauf 1/2 – Noch 8 Abende", "22 Tage nach Kauf",
      "Deine Dose reicht noch für ca. 8 Abende",
      "Bestell rechtzeitig nach, damit dein Ritual nicht unterbricht.",
      [logo(), text_block("Kurze Erinnerung", f"Hey {HELLO}, deine Dose", "ist bald leer.",
                          "<p class='t'>Bei zwei Gummies pro Abend reicht eine Dose 30 Abende. Wenn du direkt nach der Lieferung "
                          "gestartet bist, hast du jetzt noch ungefähr eine Woche. Bestell rechtzeitig nach, "
                          "damit dein Ritual keine Pause macht – der Versand dauert 1–3 Werktage.</p>",
                          pad="40px 40px 28px"),
       supply_bar(22, 30, "Noch ca. 8 Abende"),
       bundles(title="Gleich für die nächsten Monate?",
               sub="Mit 2+1 hast du 90 Abende Ruhe vor dem Nachbestellen – für ≈ 0,67 € pro Abend.", eyebrow="Vorrats-Pakete", cta="Jetzt nachbestellen"),
       guarantee(), trust_bar(), footer(BUYER)])

email("ro-2", "Nachkauf (1 Dose)", "FK | Nachkauf 2/2 – Letzte Abende", "27 Tage nach Kauf",
      "Nur noch ein paar Abende übrig",
      "Damit dein Feierabend-Ritual keine Pause macht.",
      [topbar("Kostenloser Versand · in 1–3 Werktagen bei dir"), logo(),
       text_block("Fast leer", "Nur noch ein paar Abende.", "Dann ist die Dose leer.",
                  "<p class='t'>Wenn du jetzt bestellst, ist die neue Dose da, bevor die alte leer ist. "
                  "Routinen leben davon, dass sie nicht unterbrochen werden.</p>", pad="40px 40px 28px"),
       supply_bar(27, 30, "Noch ca. 3 Abende"),
       product_card(cta="Jetzt nachbestellen", price="ab 29,99 €"),
       review(*R_CHRISTINA, bg="#ffffff"),
       bundles(eyebrow="Vorrats-Pakete"), trust_bar(), footer(BUYER)])

email("ro-3", "Nachkauf (Pakete)", "FK | Nachkauf Paket – Vorrat geht zur Neige", "80 / 140 Tage nach Kauf",
      "Dein Feierabend-Vorrat geht bald zur Neige",
      "Zeit, dein Ritual für die nächsten Monate zu sichern.",
      [logo(), image(IMG["pack"], "Feierabend-Komplex", pad="30px 40px 0", radius="18px"),
       text_block("Danke für deine Treue", f"Hey {HELLO}, deine Pakete", "neigen sich dem Ende.",
                  "<p class='t'>Du hast dich für ein Vorratspaket entschieden – stark. Nach unserer Rechnung bist du jetzt "
                  "in den letzten ein bis zwei Wochen. Bestell rechtzeitig nach, damit dein Ritual nahtlos weitergeht.</p>",
                  pad="36px 40px 20px"),
       stats([("2", "Gummies<br>pro Abend"), ("90", "Abende mit<br>2+1"), ("150", "Abende mit<br>3+2"), ("0 €", "Versand")]),
       bundles(title="Dein nächster Vorrat", sub="Wieder mit Gratis-Dosen und ohne Abo.", eyebrow="Vorrats-Pakete", cta="Jetzt nachbestellen"),
       guarantee(), trust_bar(), footer(BUYER)])

email("wb-1", "Winback (1 Dose)", "FK | Winback – Lange nicht gesehen", "60 Tage nach Kauf",
      "Dein Feierabend vermisst dich",
      "Zeit für einen Neustart deines Abendrituals?",
      [logo(), image(IMG["life6"], "Feierabend-Ritual"),
       text_block("Lange nicht gesehen", f"Hey {HELLO}, wie sehen", "deine Abende gerade aus?",
                  "<p class='t'>Vor ungefähr zwei Monaten hast du mit dem Feierabend-Komplex angefangen. Seitdem haben wir "
                  "nichts mehr von dir gehört. Vielleicht ist das Ritual im Alltag untergegangen – das passiert. "
                  "Der beste Zeitpunkt für einen Neustart ist heute Abend.</p>", pad="40px 40px 26px"),
       steps([("Dose bestellen", "In 1–3 Werktagen bei dir, kostenloser Versand."),
              ("Uhrzeit festlegen", "Immer gleich, etwa 1–2 Stunden vor dem Schlafengehen."),
              ("Dranbleiben", "Jeden Abend, auch am Wochenende. So wird es zum Ritual.")]),
       review(*R_TIM, bg="#ffffff"),
       bundles(eyebrow="Neustart", title="Starte dein Ritual neu", sub="Kein Abo, 60 Tage Geld-zurück-Garantie.", cta="Jetzt neu starten"),
       guarantee(), trust_bar(), footer(BUYER)])


def main():
    OUT.mkdir(exist_ok=True)
    manifest = []
    for e in EMAILS:
        (OUT / f"{e['slug']}.html").write_text(e["html"], encoding="utf-8")
        manifest.append({k: v for k, v in e.items() if k != "html"} | {"bytes": len(e["html"].encode())})
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    for m in manifest:
        print(f"{m['slug']:<12} {m['bytes']:>6}  {m['subject']}")


if __name__ == "__main__":
    main()
