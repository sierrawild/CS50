import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session['user_id']
    
    rows = db.execute('SELECT symbol, SUM(shares) AS shares FROM transactions\
        WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0', user_id)
    
    holdings = []
    stocks_total = 0
    
    for row in rows:
        stock = lookup(row['symbol'])
        price = stock['price']
        shares = row['shares']
        total = shares * price
        stocks_total += total
        holdings.append({'symbol': row['symbol'],
                         'shares': shares,
                         'price': price,
                         'total': total})
    
    cash = db.execute('SELECT cash FROM users WHERE id =?', user_id)
    cash = cash[0]['cash']
    grand_total = cash + stocks_total

    return render_template('index.html', holdings=holdings, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == 'GET':
        return render_template('buy.html')
    else:
        symbol = request.form.get('symbol')
        shares = request.form.get('shares')
        if not symbol:
            return apology('Provide a symbol', 400)
        stock = lookup(symbol)
        if stock is None:
            return apology('Invalid symbol', 400)
        
        # check if shares is a positive number
        if not shares or not shares.isdigit() or int(shares) < 1:
            return apology('Provide positive number', 400)
        shares = int(shares)
        
        # get cash off the user
        user_id = session['user_id']
        row = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = row[0]['cash']
        
        cost = shares * stock['price']
        if cost > cash:
            return apology('Sorry, cant afford the purchase')
        cash = cash - cost
        # update cash in db
        db.execute('UPDATE users Set cash = ? WHERE id = ?', cash, user_id)
        # update transactions
        db.execute('INSERT INTO transactions(user_id, symbol, shares, price) VALUES(?,?,?,?)', user_id, stock['symbol'], shares, stock["price"])
        
        return redirect('/')


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == 'GET':
        return render_template("quote.html")
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        if not symbol:
            return apology('Provide a symbol', 400)
        stock = lookup(symbol)
        if stock == None:
            return apology('Invalid symbol', 400)
        
        return render_template("quoted.html", stock=stock)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if not username:
        return apology("must provide username", 400)
    if not password:
        return apology("must provide password", 400)
    if not confirmation:
        return apology("must confirm password", 400)
    if password != confirmation:
        return apology("passwords do not match", 400)

    hash = generate_password_hash(password)

    try:
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username, hash
        )
    except ValueError:
        return apology("username already taken", 400)

    rows = db.execute("SELECT id FROM users WHERE username = ?", username)
    session["user_id"] = rows[0]["id"]
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "GET":
        rows = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            user_id
        )
        symbols = [row["symbol"] for row in rows]
        return render_template("sell.html", symbols=symbols)

    # POST
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    if not symbol:
        return apology("must select a symbol", 400)

    if not shares or not shares.isdigit() or int(shares) < 1:
        return apology("shares must be a positive integer", 400)

    shares = int(shares)

    # How many do they own?
    rows = db.execute(
        "SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ?",
        user_id, symbol
    )
    owned = rows[0]["shares"] or 0

    if owned < shares:
        return apology("not enough shares", 400)

    # Current price
    stock = lookup(symbol)
    if stock is None:
        return apology("invalid symbol", 400)

    price = stock["price"]
    proceeds = shares * price

    # Add cash
    db.execute(
        "UPDATE users SET cash = cash + ? WHERE id = ?",
        proceeds, user_id
    )

    # Record sale (negative shares)
    db.execute(
        "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
        user_id, symbol, -shares, price
    )

    return redirect("/")
