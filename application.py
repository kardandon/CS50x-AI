import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    id = session.get("user_id")
    rows = db.execute("SELECT symbol,sum(shares) FROM history WHERE user_id = :id GROUP BY symbol ORDER BY symbol", id=id)
    current_cash = db.execute("SELECT cash FROM users WHERE id=:id", id=id)[0]["cash"]
    total = current_cash
    for i in range(len(rows)):
        w = rows[i]
        if w["sum(shares)"] == 0:
            del rows[i]
            continue
        sym = lookup(w["symbol"])
        w["name"], w["price"], w["total"] = sym["name"], usd(sym["price"]), sym["price"] * w["sum(shares)"]
        w["shares"] = w["sum(shares)"]
        total += w["total"]
        w["total"] = usd(w["total"])
    return render_template("index.html", values=rows, current_cash=usd(current_cash), total_value=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        try:
            sym = request.form.get("symbol")
            shares = int(request.form.get("shares"))
            if shares == None:
                return apology("Missing Shares", 400)
            value = lookup(sym)
            if value == None:
                return apology("Invalid Symbol", 400)
            id = session.get("user_id")
            money = db.execute("SELECT cash FROM users WHERE id = :id", id=id)[0]["cash"]

            transection = value["price"] * shares
            if money < transection:
                return apology("CAN'T AFFORD", 400)
            else:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db.execute("INSERT INTO history (user_id,symbol,shares,price,transacted) VALUES(:userid, :symbol, :shares, :price, :transacted)",
                           userid=id, symbol=sym, shares=shares, price=value["price"], transacted=now)
                db.execute("UPDATE users SET cash = :cash WHERE id=:id", cash=money - transection, id=id)
            flash('Bought')
            return redirect("/")
        except:
            return apology("Something Happened")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    try:
        id = session.get("user_id")
        values = db.execute("SELECT symbol, shares, price, transacted FROM history WHERE user_id=:id", id=id)
        for w in values:
            w["price"] = usd(w["price"])
        return render_template("history.html", values=values)
    except:
        return apology("Something went wrong")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    try:
        if request.method == "GET":
            return render_template("quote.html", string="")
        else:
            symbol = request.form.get("symbol")
            value = lookup(symbol)
            if value == None:
                return render_template("quote.html", string="Invalid Symbol of The Stock")
            return render_template("quote.html", string="A share of " + str(value["name"]) + " ("+symbol + ") costs " + str(value["price"]))
    except:
        return apology("Something went wrong")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    try:
        usrn = request.form.get("username")
        pw1 = request.form.get("password")
        pw2 = request.form.get("passwordC")
        if request.method == "POST":

            # Ensure username was submitted
            if not usrn or len(usrn) > 15:
                return apology("must provide username less then 15 digits", 403)

            # Ensure password was submitted
            elif not pw1 or len(pw1) < 8:
                return apology("must provide at least 8 digit long password", 403)
            elif not (pw1 == pw2):
                return apology("passwords do not match", 403)
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))

            # Ensure username exists and password is correct
            if len(rows) != 0:
                return apology("username is already in use", 403)

            db.execute("INSERT INTO users (username,hash) VALUES(:username, :hash)",
                       username=usrn, hash=generate_password_hash(pw1))
            # Login and Remember which user has logged in
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")

        # User reached route via GET (as by clicking a link or via redirect)
        else:
            return render_template("register.html")
    except:
        return apology("Something went wrong")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    try:
        id = session.get("user_id")
        rows = db.execute("SELECT symbol, sum(shares) FROM history WHERE user_id=:id GROUP BY symbol ORDER BY symbol", id=id)
        values = []
        for r in rows:
            if (r["sum(shares)"] > 0):
                values.append([r["symbol"], r["sum(shares)"]])
        if request.method == "GET":
            return render_template("sell.html", values=values)
        else:
            sym = request.form.get("symbol")
            shares = int(request.form.get("shares"))
            if sym == None:
                return apology("Please Choose A Symbol", 400)
            sym = sym.split(":")[0]
            if shares == None:
                return apology("Missing Shares", 400)
            value = lookup(sym)
            if value == None:
                return apology("Invalid Symbol", 400)
            for r in values:
                if r[0] == sym:
                    max_limit = r[1]
                    break
            if max_limit < shares:
                flash("Not Enough Shares")
                return redirect("/sell")
            money = db.execute("SELECT cash FROM users WHERE id = :id", id=id)[0]["cash"]
            transection = value["price"] * shares
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.execute("INSERT INTO history (user_id,symbol,shares,price,transacted) VALUES(:userid, :symbol, :shares, :price, :transacted)",
                       userid=id, symbol=sym, shares=-shares, price=value["price"], transacted=now)
            db.execute("UPDATE users SET cash = :cash WHERE id=:id", cash=money + transection, id=id)
            flash('Sold!')
            return redirect("/")
    except:
        return apology("Something went wrong")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
