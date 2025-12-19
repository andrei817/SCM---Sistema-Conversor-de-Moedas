from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api.frankfurter.app/latest"

NOMES_MOEDAS = {
    "BRL": "Real Brasileiro",
    "AUD": "Dólar Australiano",
    "BGN": "Lev Búlgaro",
    "CAD": "Dólar Canadense",
    "CHF": "Franco Suíço",
    "CNY": "Yuan Chinês",
    "CZK": "Coroa Tcheca",
    "DKK": "Coroa Dinamarquesa",
    "EUR": "Euro",
    "GBP": "Libra Esterlina",
    "HKD": "Dólar de Hong Kong",
    "HUF": "Forint Húngaro",
    "IDR": "Rupia Indonésia",
    "ILS": "Novo Shekel Israelense",
    "INR": "Rupia Indiana",
    "ISK": "Coroa Islandesa",
    "JPY": "Iene Japonês",
    "KRW": "Won Sul-Coreano",
    "MXN": "Peso Mexicano",
    "MYR": "Ringgit Malaio",
    "NOK": "Coroa Norueguesa",
    "NZD": "Dólar Neozelandês",
    "PHP": "Peso Filipino",
    "PLN": "Zloty Polonês",
    "RON": "Leu Romeno",
    "SEK": "Coroa Sueca",
    "SGD": "Dólar de Singapura",
    "THB": "Baht Tailandês",
    "TRY": "Lira Turca",
    "USD": "Dólar Americano",
    "ZAR": "Rand Sul-Africano"
}

SIMBOLOS = {
    "BRL": "R$",
    "EUR": "€",
    "USD": "$",
    "GBP": "£",
    "JPY": "¥",
    "CNY": "¥",
    "AUD": "A$",
    "CAD": "C$",
    "CHF": "CHF",
    "BGN": "лв",
    "CZK": "Kč",
    "DKK": "kr",
    "HKD": "HK$",
    "HUF": "Ft",
    "IDR": "Rp",
    "ILS": "₪",
    "INR": "₹",
    "ISK": "kr",
    "KRW": "₩",
    "MXN": "MX$",
    "MYR": "RM",
    "NOK": "kr",
    "NZD": "NZ$",
    "PHP": "₱",
    "PLN": "zł",
    "RON": "lei",
    "SEK": "kr",
    "SGD": "S$",
    "THB": "฿",
    "TRY": "₺",
    "ZAR": "R"
}

def buscar_moedas():
    resposta = requests.get(API_URL).json()

    if "rates" not in resposta:
        print("Erro na API:", resposta)
        return {}

    taxas = resposta["rates"]
    taxas["EUR"] = 1.0  # base da API

    return taxas


def converter_moeda(valor, moeda_origem, moeda_destino, taxas):
    if moeda_origem not in taxas or moeda_destino not in taxas:
        return None

    return valor * (taxas[moeda_destino] / taxas[moeda_origem])

@app.route("/", methods=["GET", "POST"])
def index():
    taxas = buscar_moedas()
    resultado = ""
    simbolo = ""
    moeda_origem = "BRL"
    moeda_destino = "USD"
    valor = ""

    if request.method == "POST":
        valor = float(request.form.get("valor", 0))
        moeda_origem = request.form.get("moeda_origem", "BRL")
        moeda_destino = request.form.get("moeda_destino", "USD")

        resultado = converter_moeda(valor, moeda_origem, moeda_destino, taxas)

        if resultado is not None:
            resultado = f"{resultado:,.2f}"
            simbolo = SIMBOLOS.get(moeda_destino, "")

    return render_template(
        "index.html",
        moedas=sorted(NOMES_MOEDAS.keys()),
        resultado=resultado,
        simbolo=simbolo,
        moeda_origem=moeda_origem,
        moeda_destino=moeda_destino,
        valor=valor,
        nomes=NOMES_MOEDAS
    )


if __name__ == "__main__":
    app.run(debug=True)
