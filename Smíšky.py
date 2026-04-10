def najdi_idealni_rozlozeni(celkem_kc):
    max_deti = celkem_kc // 150
    max_dospeli = celkem_kc // 190

    nejlepsi_vysledek = None
    nejmensi_odchylka_smisku = float('inf')

    for deti in range(1, max_deti + 1):
        for dospeli in range(1, max_dospeli + 1):
            vstupne = deti * 150 + dospeli * 190
            smisky_kc = celkem_kc - vstupne

            if smisky_kc < 0:
                continue

            lide = deti + dospeli
            prumer_smisku = smisky_kc / 10 / lide

            # 🎯 Povolíme jen přibližný poměr dospělí/děti (např. 1.6–2.4)
            pomer = dospeli / deti
            if not (1.4 <= pomer <= 2.6):
                continue
            if pomer == 2:
                continue

            # 🎯 Hledáme co nejbližší k ideálnímu průměru (např. 22.5)
            odchylka = abs(prumer_smisku - 3)

            if odchylka < nejmensi_odchylka_smisku:
                nejmensi_odchylka_smisku = odchylka
                nejlepsi_vysledek = {
                    "deti": deti,
                    "dospeli": dospeli,
                    "lide": lide,
                    "vstupne": vstupne,
                    "smisky_kc": smisky_kc,
                    "celkem": celkem_kc,
                    "prumer_smisku_na_osobu": round(prumer_smisku, 2)
                }

    return nejlepsi_vysledek


# Hlavní část
while True:
    try:
        vstup = int(input("Zadej celkovou částku (Kč): "))
        vysledek = najdi_idealni_rozlozeni(vstup)
        if vysledek:
            print("\n--- VÝSLEDEK ---")
            print("Počet lidí celkem:", vysledek["lide"])
            print("Počet dětí:", vysledek["deti"])
            print("Počet dospělých:", vysledek["dospeli"])
            print("Kč za vstupné:", vysledek["vstupne"])
            print("Kč za smíšky:", vysledek["smisky_kc"])
            print("Průměr smíšků na osobu:", vysledek["prumer_smisku_na_osobu"])
            print("Celkem Kč:", vysledek["celkem"])
        else:
            print("\nNepodařilo se najít vhodnou kombinaci.")
    except ValueError:
        print("Zadej prosím platné číslo.")
