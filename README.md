# 📊 DACH Kleinunternehmer- & USt-Vorsteuer-Rechner 2026

[![Python Tests](https://github.com/DACHDigitalwerk/kleinunternehmer-vorsteuer-rechner-dach/actions/workflows/python-tests.yml/badge.svg)](https://github.com/DACHDigitalwerk/kleinunternehmer-vorsteuer-rechner-dach/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![EU-Richtlinie 2026](https://img.shields.io/badge/EU--Richtlinie-2020%2F285-emerald.svg)](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32020L0285)
[![Web-Tool Live](https://img.shields.io/badge/Web--Tool-Live%20Rechner-emerald.svg)](https://dach-digitalwerk.netlify.app/kleinunternehmer-vorsteuer-rechner/)

> **Offizielles Open-Source-Fintech- & Legaltech-Paket von [@DACHDigitalwerk](https://dach-digitalwerk.netlify.app/).**  
> Mathematische Schwellenwertprüfung und dynamische Vorsteuer-Rentabilitätsanalyse für Deutschland (**§ 19 UStG n.F.**), Österreich (**§ 6 Abs. 1 Z 27 UStG n.F.**) und die Schweiz (**Art. 10 & 37 MWSTG**).

---

## 🌐 Interaktives Web-Tool

Für eine sofortige Berechnung im Browser ohne Installation nutzen Sie unser kostenloses Web-Tool:  
👉 **[DACH Kleinunternehmer- & Vorsteuer-Rechner 2026 (Live Web-App)](https://dach-digitalwerk.netlify.app/kleinunternehmer-vorsteuer-rechner/)**

---

## 🏛️ Gesetzliche Grenzwerte & Neuerungen 2026

Mit der Umsetzung der **EU-Kleinunternehmer-Richtlinie (RL (EU) 2020/285)** und dem deutschen Wachstumschancengesetz gelten ab 2025/2026 grundlegend neue Schwellenwerte im DACH-Raum:

| Land | Rechtsgrundlage | Schwellenwert Vorjahr | Schwellenwert Laufendes Jahr | Toleranzregelung |
| :--- | :--- | :--- | :--- | :--- |
| **🇩🇪 Deutschland** | § 19 UStG n.F. & EU-RL 2020/285 | **25.000 €** *(bisher 22.000 €)* | **25.000 €** national / **100.000 €** EU-weit | Keine Toleranz *(Sofortige USt-Pflicht bei Überschreitung)* |
| **🇦🇹 Österreich** | § 6 Abs. 1 Z 27 UStG n.F. | **42.000 €** *(bisher 35.000 €)* | **42.000 €** netto | **55.000 €** Toleranz *(einmalig in 5 Wirtschaftsjahren)* |
| **🇨🇭 Schweiz** | Art. 10 MWSTG | **100.000 CHF** weltweit | **100.000 CHF** *(150.000 CHF für gemeinnützige Vereine)* | Freiwillige Unterstellung gem. Art. 10 Abs. 3 MWSTG |

---

## 💡 Das mathematische Rentabilitäts-Dilemma

Viele Selbstständige und Gründer fragen sich: **„Lohnt sich die Kleinunternehmerregelung für mich?“**

Die Entscheidung ist keine reine Formsache, sondern eine mathematische Abwägung zwischen zwei gegenläufigen Effekten:

1. **Vorteil bei Privatkunden (B2C):**  
   Im B2C-Geschäft verhandeln Endverbraucher stets **Bruttopreise**. Als Kleinunternehmer müssen Sie keine Umsatzsteuer an das Finanzamt abführen. Sie behalten die Umsatzsteuer entweder als zusätzlichen Deckungsbeitrag (`USt-Ersparnis = Umsatz_B2C × (Steuersatz / (1 + Steuersatz))`) oder bieten 19 % günstiger als die Konkurrenz an.
2. **Nachteil bei Unternehmenskunden (B2B) & Investitionen:**  
   B2B-Kunden sind vorsteuerabzugsberechtigt; für sie ist die Umsatzsteuer ein durchlaufender Posten. Als Kleinunternehmer sind Sie jedoch **vom Vorsteuerabzug (§ 15 UStG) ausgeschlossen**! Jeder Wareneinkauf, jede Software-Lizenz und jede Hardware-Investition kostet Sie den vollen Bruttopreis.
3. **Bürokratiekosten:**  
   Bei Regelbesteuerung fallen monatliche/quartalsweise Voranmeldungen und ggf. höhere Steuerberaterhonorare an (typisch 300–800 € / Jahr).

### Die Entscheidungsgleichung:
$$\text{Netto-Vorteil} = \text{USt-Ersparnis}_{\text{B2C}} + \text{Bürokratie-Ersparnis} - \text{Entgangene Vorsteuer}_{\text{Ausgaben & CAPEX}}$$

* **Netto-Vorteil > 0:** Kleinunternehmerregelung lohnt sich finanziell.
* **Netto-Vorteil < 0:** Regelbesteuerung (Verzicht auf die Befreiung gem. § 19 Abs. 2 UStG) verschafft einen messbaren Liquiditäts- und Ertragsvorteil!

---

## 🚀 Installation

```bash
git clone https://github.com/DACHDigitalwerk/kleinunternehmer-vorsteuer-rechner-dach.git
cd kleinunternehmer-vorsteuer-rechner-dach
pip install -e .
```

---

## 💻 CLI-Nutzung (`dach-kleinunternehmer`)

Nach der Installation steht das CLI-Tool `dach-kleinunternehmer` zur Verfügung:

### 1. Amtliche Schwellenwert-Prüfung 2026
```bash
# Deutschland: Prüfung gegen die neue 25.000 €-Grenze
dach-kleinunternehmer check --country DE --prev 21000 --curr 24200

# Österreich: Prüfung gegen 42.000 € und 55.000 € Toleranzzone
dach-kleinunternehmer check --country AT --prev 38000 --curr 46000

# Schweiz: Prüfung gegen 100.000 CHF Schwelle
dach-kleinunternehmer check --country CH --prev 65000 --curr 82000
```

### 2. Rentabilitäts- & Vorsteuervergleich
```bash
# Beispiel IT-Freelancer (hoher B2B-Anteil, 4.000 € Betriebsausgaben, 3.500 € Investition)
dach-kleinunternehmer compare \
  --country DE \
  --revenue 24000 \
  --b2b 85 \
  --expenses 4000 \
  --investments 3500 \
  --admin-cost 400
```

### 3. Break-Even-Berechnung
Ermittelt exakt, ab welchem Investitionsvolumen oder welchem B2B-Anteil sich die Regelbesteuerung lohnt:
```bash
dach-kleinunternehmer break-even --country DE --revenue 22000 --b2b 40 --expenses 2500
```

### 4. JSON-Pipeline für Automatisierung
```bash
dach-kleinunternehmer compare --country DE --revenue 24000 --b2b 20 --json
```

---

## 🐍 Python API

```python
from kleinunternehmer_dach import (
    check_threshold,
    calculate_profitability,
    ProfitabilityInput
)

# 1. Schwellenwert-Check
status = check_threshold(
    country="DE",
    prev_year_turnover=22000.0,
    current_year_turnover=24500.0
)
print(status.threshold_status)  # "WARNING_NEAR_LIMIT"
print(status.is_eligible)       # True

# 2. Rentabilitäts-Simulation
params = ProfitabilityInput(
    country="DE",
    planned_revenue=24000.0,
    b2b_share_pct=30.0,         # 30% B2B, 70% B2C
    expenses_operating=3000.0,
    investments=1500.0,
    admin_cost_standard_tax=400.0
)
res = calculate_profitability(params)

print(f"Empfehlung: {res.recommendation}")
print(f"Netto-Vorteil: {res.net_advantage_kleinunternehmer:,.2f} EUR")
print(f"Break-Even Investitionshöhe: {res.break_even_investments:,.2f} EUR")
```

---

## 🧪 Tests

Das Projekt verfügt über eine umfassende Unit-Test-Suite mit 30+ Tests:

```bash
pytest -v
```

---

## 🛡️ Haftungsausschluss & Rechtliche Hinweise

**Keine Steuer- oder Rechtsberatung gem. § 2 RDG / § 5 StBerG:**  
Dieses Softwarepaket ist ein reines mathematisches Simulations- und Berechnungswerkzeug. Es ersetzt keine individuelle betriebswirtschaftliche, steuerliche oder rechtliche Beratung durch einen Steuerberater, Wirtschaftsprüfer oder Rechtsanwalt. Alle Angaben und Schwellenwerte basieren auf den gesetzlichen Bestimmungen des Jahres 2026 und erfolgen ohne Gewähr.

* Allgemeine Geschäftsbedingungen: [https://dach-digitalwerk.netlify.app/agb/](https://dach-digitalwerk.netlify.app/agb/)
* Haftungsausschluss: [https://dach-digitalwerk.netlify.app/haftungsausschluss/](https://dach-digitalwerk.netlify.app/haftungsausschluss/)

---

## 📄 Lizenz

Veröffentlicht unter der [MIT License](LICENSE). Erstellt mit ❤️ von **[DACH Digitalwerk](https://dach-digitalwerk.netlify.app/)**.
