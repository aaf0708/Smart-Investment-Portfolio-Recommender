import matplotlib.pyplot as plt
import os
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

def generate_portfolio(amount, risk):
    """Generate an investment breakdown based on risk preference."""
    amount = float(amount)
    if risk == "low":
        portfolio = {"Bonds": amount * 0.6, "Stocks": amount * 0.3, "ETFs": amount * 0.1}
    elif risk == "medium":
        portfolio = {"Bonds": amount * 0.3, "Stocks": amount * 0.5, "ETFs": amount * 0.2}
    else:  # high risk
        portfolio = {"Bonds": amount * 0.1, "Stocks": amount * 0.7, "ETFs": amount * 0.2}
    return portfolio

def create_pie_chart(portfolio):
    """Generate a pie chart and save it."""
    labels = list(portfolio.keys())
    values = list(portfolio.values())

    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
    plt.title("Investment Allocation")

    img_path = os.path.join("static", "investment_chart.png")
    plt.savefig(img_path)
    plt.close()
    
    return img_path
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/portfolio",methods=["GET","POST"])

def portfolio():
    amount = request.args.get('amount', 1000)  # Default to 1000 if missing
    risk = request.args.get('risk', 'medium')

    if request.method == 'POST':
        amount = request.form['amount']
        risk = request.form['risk']
        return redirect(url_for('portfolio', amount=amount, risk=risk))

    portfolio_data = generate_portfolio(amount, risk)
    img_url = create_pie_chart(portfolio_data)

    return render_template('portfolio.html', amount=amount, risk=risk, investment_data=portfolio_data, img_url=img_url)


if __name__ == "__main__":
    app.run(debug=True)