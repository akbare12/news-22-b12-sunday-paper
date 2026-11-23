#!/usr/bin/env python3
"""SUNDAY PAPER — news-image-20261122 entry.
Magazine style: 3 hero stories as long-form features with pull-quotes,
plus a numbered briefs sidebar with the rest of the day. 32 stories.
Draws entry.png (1024x1024) with PIL only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FDIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = os.path.join(FDIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FDIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FDIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FDIR, "DejaVuSans-Bold.ttf")
SANS_I = os.path.join(FDIR, "DejaVuSans.ttf")  # no oblique shipped; gold colour marks quotes
SANS_BI = os.path.join(FDIR, "DejaVuSans-BoldOblique.ttf")

CREAM = (247, 243, 232)
INK = (26, 26, 26)
RED = (158, 24, 24)
NAVY = (24, 44, 84)
GOLD = (184, 134, 11)
GREY = (90, 90, 90)
LIGHT = (233, 227, 210)
YELLOW = (255, 243, 176)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def badge(draw, x, y, label, bg):
    f = font(SANS_B, 11)
    w = int(draw.textlength(label, font=f)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=bg)
    draw.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def tanker_panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # sun
    draw.ellipse([x + w - 70, y + 14, x + w - 30, y + 54], fill=(255, 176, 32))
    # smoke
    for i, r in enumerate((26, 20, 15)):
        draw.ellipse([x + 150 + i * 26, y + 18 + i * 6, x + 150 + i * 26 + r * 2,
                      y + 18 + i * 6 + r * 2], fill=(40, 40, 40))
    # hull
    draw.rectangle([x + 18, y + h - 58, x + w - 18, y + h - 30], fill=(20, 20, 20))
    draw.rectangle([x + 40, y + h - 86, x + 120, y + h - 58], fill=(40, 40, 40))
    draw.rectangle([x + 60, y + h - 104, x + 100, y + h - 86], fill=(60, 60, 60))
    # flames on deck
    for fx in (150, 190, 230):
        draw.polygon([(x + fx, y + h - 58), (x + fx + 12, y + h - 96),
                      (x + fx + 24, y + h - 58)], fill=(255, 120, 0))
        draw.polygon([(x + fx + 6, y + h - 58), (x + fx + 12, y + h - 80),
                      (x + fx + 18, y + h - 58)], fill=(255, 210, 0))
    # sea
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=(30, 80, 130))
    for sx in range(x + 8, x + w - 8, 44):
        draw.arc([sx, y + h - 22, sx + 34, y + h - 6], 200, 340, fill=(180, 220, 240), width=2)


def globe_panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=RED)
    cx, cy, r = x + w // 2, y + h // 2, 52
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 180, 120))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=3)
    # land blobs
    draw.ellipse([cx - 34, cy - 26, cx - 2, cy + 6], fill=(60, 130, 70))
    draw.ellipse([cx + 4, cy + 8, cx + 34, cy + 34], fill=(60, 130, 70))
    draw.ellipse([cx - 10, cy - 40, cx + 18, cy - 18], fill=(60, 130, 70))
    # crack
    draw.line([(cx - 6, cy - r), (cx + 8, cy - 14), (cx - 10, cy + 10),
               (cx + 12, cy + 34), (cx - 2, cy + r)], fill=(255, 255, 255), width=4)


def capitol_panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    cx = x + w // 2
    # dome
    draw.pieslice([cx - 46, y + 8, cx + 46, y + 56], 180, 360, fill=(240, 240, 235))
    draw.rectangle([cx - 4, y + 2, cx + 4, y + 12], fill=(240, 240, 235))
    # base + columns
    draw.rectangle([cx - 62, y + 56, cx + 62, y + 62], fill=(240, 240, 235))
    for i in range(5):
        colx = cx - 52 + i * 26
        draw.rectangle([colx, y + 62, colx + 10, y + 80], fill=(240, 240, 235))
    draw.rectangle([cx - 62, y + 80, cx + 62, y + 86], fill=(240, 240, 235))
    # stars
    for sx, sy in ((x + 16, y + 10), (x + w - 22, y + 10), (x + 16, y + 66),
                   (x + w - 22, y + 66)):
        draw.text((sx, sy), "*", font=font(SANS_B, 16), fill=(255, 210, 0))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # outer border
    d.rectangle([6, 6, W - 7, H - 7], outline=RED, width=3)
    d.rectangle([12, 12, W - 13, H - 13], outline=RED, width=1)

    # ---- masthead ----
    d.text((W // 2, 22), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    d.line([24, 96, W - 24, 96], fill=INK, width=2)
    d.text((24, 102), "SUNDAY PAPER", font=font(SANS_B, 17), fill=RED)
    d.text((W // 2, 102), "SUNDAY 22 NOVEMBER 2026", font=font(SANS_B, 17),
           fill=INK, anchor="ma")
    d.text((W - 24, 102), "32 STORIES", font=font(SANS_B, 17), fill=INK, anchor="ra")
    d.line([24, 126, W - 24, 126], fill=INK, width=1)

    # ---- FEATURE 1: HORMUZ (full width) ----
    fy = 136
    tanker_panel(d, 24, fy, 300, 150)
    tx = 340
    d.text((tx, fy), "CONFLICT  ·  STRAIT OF HORMUZ", font=font(SANS_B, 13), fill=RED)
    d.text((W - 24, fy), "17:13 UTC", font=font(SANS_B, 13), fill=GREY, anchor="ra")
    d.text((tx, fy + 20), "2 TANKERS HIT", font=font(SERIF_B, 40), fill=INK)
    body1 = ("Two supertankers struck mines east of the Strait of Hormuz on Sunday "
             "and caught fire, in the first reported mine attack in the strait in "
             "years. The blasts were first reported at 17:13 UTC. Shipping through "
             "the world's busiest oil chokepoint faces new risk as navies move to "
             "secure the lanes.")
    y = draw_text_block(d, tx, fy + 66, body1, font(SANS, 13), W - 24 - tx, leading=17)
    d.line([tx, fy + 138, W - 24, fy + 138], fill=GOLD, width=1)
    d.text((tx, fy + 144), "\u201cThe strait \u2014 the world's oil artery \u2014 is on edge.\u201d",
           font=font(SANS_I, 13), fill=GOLD)
    d.line([24, 296, W - 24, 296], fill=INK, width=1)

    # ---- FEATURES 2 + 3 side by side ----
    fy2 = 306
    col_w = 476
    # COP31 left
    lx = 24
    d.text((lx, fy2), "CLIMATE  ·  ANTALYA", font=font(SANS_B, 13), fill=RED)
    d.text((lx + col_w, fy2), "EVENING", font=font(SANS_B, 13), fill=GREY, anchor="ra")
    d.text((lx, fy2 + 20), "NO DEAL", font=font(SERIF_B, 36), fill=INK)
    globe_panel(d, lx, fy2 + 62, 110, 88)
    body2 = ("The COP31 climate summit in Antalya ended with no deal \u2014 the first "
             "collapse of a climate summit since 2009. The EU and about 130 parties "
             "rejected a draft text with no mention of fossil fuels. Talks ran past "
             "deadline, then broke up with nothing agreed.")
    draw_text_block(d, lx + 122, fy2 + 62, body2, font(SANS, 12), col_w - 122, leading=16)
    d.line([lx, fy2 + 156, lx + col_w, fy2 + 156], fill=GOLD, width=1)
    d.text((lx, fy2 + 162), "\u201cThe first climate summit to collapse",
           font=font(SANS_I, 12), fill=GOLD)
    d.text((lx, fy2 + 178), "without a deal since 2009.\u201d",
           font=font(SANS_I, 12), fill=GOLD)
    # Dems right
    rx = 524
    d.text((rx, fy2), "POLITICS  ·  WASHINGTON", font=font(SANS_B, 13), fill=RED)
    d.text((rx + col_w, fy2), "18:00 UTC", font=font(SANS_B, 13), fill=GREY, anchor="ra")
    d.text((rx, fy2 + 20), "258", font=font(SERIF_B, 36), fill=INK)
    d.text((rx + 118, fy2 + 30), "DEMS TAKE THE HOUSE", font=font(SERIF_B, 17), fill=INK)
    capitol_panel(d, rx, fy2 + 62, 110, 88)
    body3 = ("Democrats won the US House with 258 seats, their largest majority "
             "since 1992. The decisive race was settled by a recount in North "
             "Carolina, where Hubbard beat Foxx by 330 votes. Republicans hold "
             "173 seats; four races remain uncalled.")
    draw_text_block(d, rx + 122, fy2 + 62, body3, font(SANS, 12), col_w - 122, leading=16)
    d.line([rx, fy2 + 156, rx + col_w, fy2 + 156], fill=GOLD, width=1)
    d.text((rx, fy2 + 162), "\u201cThe largest Democratic majority",
           font=font(SANS_I, 12), fill=GOLD)
    d.text((rx, fy2 + 178), "since 1992.\u201d", font=font(SANS_I, 12), fill=GOLD)
    d.line([24, 512, W - 24, 512], fill=INK, width=2)

    # ---- BRIEFS header ----
    d.text((24, 522), "THE REST OF THE DAY \u2014 BRIEFS 04\u201332",
           font=font(SANS_B, 15), fill=INK)
    d.text((W - 24, 522), "ALL TIMES UTC", font=font(SANS_B, 12), fill=GREY, anchor="ra")
    d.line([24, 546, W - 24, 546], fill=INK, width=1)

    briefs = [
        ("04", "Dymer drone hits flats", "7 killed in first reports; boy pulled alive", "AP", None),
        ("05", "Merkury hit off Benghazi", "Russian corvette struck by sea drones", "AP", None),
        ("06", "Khartoum drones kill 4", "UN building damaged in strike", "", "CLAIM"),
        ("07", "Zelenskyy pleads for Patriots", "~2,700 drones fired in a week", "BBC", None),
        ("08", "Iran shows missile city", "Underground base unveiled on state TV", "IRGC", None),
        ("09", "Saudis stop Houthi attack", "Drone+missile downed; Rabigh claimed", "", "CLAIM"),
        ("10", "Bahrain blames Iran", "Industrial site struck; UAE condemns", "Fr 24", None),
        ("11", "UAE condemns Bahrain strike", "Calls it a sovereign violation", "WAM", None),
        ("12", "Europe protests, day 3", "144 arrested in France", "AP", None),
        ("13", "Settlers burn West Bank cars", "12 vehicles torched near Ramallah", "Guard.", None),
        ("14", "Benghazi depot blast", "Ammo depot explodes in naval base", "Local", None),
        ("15", "Unity talks stall", "Eisenkot\u2013Likud meet; wide gap remains", "Isr. media", None),
        ("16", "Finland: war spreads to Baltic", "Baltic shipping at risk as drones spread", "Fin. govt", None),
        ("17", "Gaza aid van strike", "WCK: three killed were not its team", "WCK", None),
        ("18", "Banten factory fire", "3 dead, 36 missing in candy-plant blaze", "BBC", None),
        ("19", "Fidan: Israel may use Druze", "Ankara warns of Syria pretext", "", "CLAIM"),
        ("20", "Fidan: war fallout hits markets", "War burden threatens global trade", "Anadolu", None),
        ("21", "Mongolia snap vote", "Presidential vote after resignation", "Euronews", None),
        ("22", "Mexico cartel boss captured", "11 killed in the operation", "Al Jaz.", None),
        ("23", "Russian cargo ship burns", "Vessel still ablaze off Finland", "Al Jaz.", None),
        ("24", "Asian stocks slide", "War fears hit markets in the region", "SCMP", None),
        ("25", "Korea minister quits, AI cheat", "111 test-takers caught using devices", "BBC", None),
        ("26", "Gaza: 350,000 homeless", "Families displaced near Yellow Line", "Al Jaz.", None),
        ("27", "Settlers attack Hebron homes", "Homes attacked; tear gas fired", "WAFA", None),
        ("28", "Gaza homes blocked", "Turkey: Israel blocks container homes", "", "CLAIM"),
        ("29", "Germany urged to arrest soldier", "Hind Rajab Foundation files case", "HRF", None),
        ("30", "Fred Nile dies at 92", "Died 21 Nov, announced 22 Nov", "Guardian", None),
        ("31", "Gamer rescues missing girl", "Teen, 16, and mother help FBI", "FBI", None),
        ("32", "Gaza toll 1,661", "Death toll since Oct 2025 ceasefire", "Gaza HM", None),
    ]
    cols, rows = 3, 10
    gx, gy = 24, 552
    cw = (W - 48 - (cols - 1) * 14) // cols
    ch = 37
    for i, (num, head, line, src, claim) in enumerate(briefs):
        col, row = i % cols, i // cols
        x = gx + col * (cw + 14)
        y = gy + row * ch
        d.text((x, y), num, font=font(SANS_B, 13), fill=RED)
        d.text((x + 26, y), head, font=font(SANS_B, 12), fill=INK)
        ly = y + 16
        d.text((x + 26, ly), line, font=font(SANS, 11), fill=INK)
        if claim:
            badge(d, x + cw - 52, ly - 2, "CLAIM", GOLD)
        elif src:
            d.text((x + cw, ly), src, font=font(SANS_I, 10), fill=GREY, anchor="ra")

    # ---- footer ----
    fy3 = 930
    d.rectangle([24, fy3, W - 24, fy3 + 20], fill=YELLOW, outline=INK)
    d.text((W // 2, fy3 + 3), "NOT YET \u2014 DO NOT READ AS DONE:  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  Gaza ceasefire talks: no deal announced",
           font=font(SANS_B, 11), fill=INK, anchor="ma")
    y = draw_text_block(d, 24, fy3 + 25,
        "DATE CHECK \u2014 Every item first reported 22 Nov, unless its kicker says otherwise. EXCLUDED: El Chapo Isidro captured 20 Nov \u00b7 BepiColombo Mercury orbit 21 Nov \u00b7 ICJ Myanmar ruling 19 Nov \u00b7 Wall St rout 20 Nov \u00b7 FBI NCIC hack first reported 21 Nov \u00b7 Paolo Bulgari died 21 Nov",
        font(SANS, 10), W - 48, fill=GREY, leading=12)
    draw_text_block(d, 24, y + 2,
        "LEGEND:  REPORTED = confirmed by 2+ sources  \u00b7  CLAIM = one side alleges, unverified  \u00b7  ONGOING = still developing.   SOURCES: AP \u00b7 Reuters \u00b7 BBC \u00b7 CNN \u00b7 France 24 \u00b7 Al Jazeera \u00b7 Guardian \u00b7 SCMP \u00b7 IRNA \u00b7 Anadolu \u00b7 WAFA \u00b7 WCK \u00b7 FBI",
        font(SANS, 10), W - 48, fill=GREY, leading=12)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
