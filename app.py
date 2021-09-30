from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = hash_password(password)

        conn = sqlite3.connect("project.sqlite")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        user_password = str(user[2])

        manager = int(user[5])

        if user_password == None or user_password != password:
            return render_template('login.html')
        
        else:
            return render_template('home.html', userID = user[0], manager = manager)

    else:
        return render_template('login.html')

@app.route('/home/<int:userID>/<int:manager>')
def home(userID, manager):
    return render_template('home.html', userID = userID, manager = manager)


@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        password = hash_password(password)
        address = request.form['address']
        phone_number = request.form['phone_number']
        manager = 0

        conn = sqlite3.connect("project.sqlite")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        exist = c.fetchone()

        if exist == None:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (None ,username, password, address, phone_number, manager))
            conn.commit()
            conn.close()
            return render_template('login.html')
        
        else:
            return render_template('register.html', success = False)
        
    else:
        return render_template('register.html', success = True)

@app.route('/search/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def search(userID, manager):
    if request.method == 'POST':
        
        result = run_search_query(request.form.to_dict(), userID)

        return render_template('search.html', userID = userID, result = result, manager = manager)
    
    else:
        return render_template('home.html', userID = userID, manager = manager)

@app.route('/book/<int:userID>/<int:bookID>/<int:manager>', methods = ['POST', 'GET'])
def book(userID, bookID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    c.execute("SELECT * FROM books WHERE bookID=" + str(bookID))
    book = c.fetchone()

    c.execute("SELECT * FROM author_descriptions WHERE author=?", (book[2],))
    description = c.fetchone()
    if description:
        description = description[2]

    
    
    c.execute("SELECT * FROM book_overviews WHERE bookID=?", (book[0],))
    overview = c.fetchone()
    if overview:
        overview = overview[2]

    c.execute("SELECT * FROM comments WHERE bookID=" + str(bookID))
    comments = c.fetchall()

    if comments:

        comment_users = []
        for comment in comments:
            c.execute("SELECT username FROM users WHERE userID=" + str(comment[2]))
            comment_username = c.fetchone()

            comment_users.append((comment, comment_username))

        return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = False, comments = comment_users, manager = manager, description = description, overview = overview)
    else:
        return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = False, comments = None, manager = manager, description = description, overview = overview)

@app.route('/trust/<int:userID>/<int:commentUserID>/<int:bookID>/<int:manager>', methods = ['POST', 'GET'])
def trust(userID, commentUserID, bookID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    if userID != commentUserID:
        c.execute("INSERT INTO trusts VALUES (?, ?, ?)", (None, userID, commentUserID))
        conn.commit()
    

    c.execute("SELECT * FROM books WHERE bookID=" + str(bookID))
    book = c.fetchone()

    c.execute("SELECT * FROM author_descriptions WHERE author=?", (book[2],))
    description = c.fetchone()
    if description:
        description = description[2]

    c.execute("SELECT * FROM comments WHERE bookID=" + str(bookID))
    comments = c.fetchall()

    if comments:

        comment_users = []
        for comment in comments:
            c.execute("SELECT username FROM users WHERE userID=" + str(comment[2]))
            comment_username = c.fetchone()

            comment_users.append((comment, comment_username))

        return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = False, comments = comment_users, manager = manager, description = description, overview = overview)
    else:
        return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = False, comments = None, manager = manager, description = description, overview = overview)


@app.route('/rateComment/<int:userID>/<int:commentID>/<int:bookID>/<int:manager>', methods = ['POST', 'GET'])
def rateComment(userID, commentID, bookID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    score = request.form['score']

    c.execute("SELECT userID FROM comments WHERE commentID=" + str(commentID))
    commentUser = c.fetchone()[0]

    if commentUser == userID:
        c.execute("SELECT * FROM books WHERE bookID=" + str(bookID))
        book = c.fetchone()
        c.execute("SELECT * FROM author_descriptions WHERE author=?", (book[2],))
        description = c.fetchone()
        if description:
            description = description[2]
        c.execute("SELECT * FROM comments WHERE bookID=" + str(bookID))
        comments = c.fetchall()

        if comments:

            comment_users = []
            for comment in comments:
                c.execute("SELECT username FROM users WHERE userID=" + str(comment[2]))
                comment_username = c.fetchone()

                comment_users.append((comment, comment_username))

            return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = False, comments = comment_users, sameUser = True, manager = manager, description = description, overview = overview)
        else:
            return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = False, comments = None, sameUser = True, manager = manager, description = description, overview = overview)

    else:
        c.execute("INSERT INTO comment_ratings VALUES (?, ?, ?, ?, ?)", (None, commentID, userID, score, commentUser))
        conn.commit()

        c.execute("SELECT AVG(rating) FROM comment_ratings WHERE commentID=" + str(commentID) + " AND commentUserID=" + str(commentUser))
        average_rating = c.fetchone()[0]

        c.execute("UPDATE comments SET average_rating=" + str(average_rating) + " WHERE commentID=" + str(commentID))
        conn.commit()

        c.execute("SELECT * FROM books WHERE bookID=" + str(bookID))
        book = c.fetchone()
        c.execute("SELECT * FROM author_descriptions WHERE author=?", (book[2],))
        description = c.fetchone()
        if description:
            description = description[2]
        c.execute("SELECT * FROM comments WHERE bookID=" + str(bookID))
        comments = c.fetchall()

        if comments:

            comment_users = []
            for comment in comments:
                c.execute("SELECT username FROM users WHERE userID=" + str(comment[2]))
                comment_username = c.fetchone()

                comment_users.append((comment, comment_username))

            return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = False, comments = comment_users, sameUser = False, manager = manager, description = description, overview = overview)
        else:
            return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = False, comments = None, sameUser = False, manager = manager, description = description, overview = overview)

     
@app.route('/topNComments/<int:userID>/<int:bookID>/<int:manager>', methods = ['POST', 'GET'])
def topNComments(userID, bookID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    numOfComments = request.form['numOfComments']

    c.execute("SELECT * FROM comments WHERE bookID=" + str(bookID) + " ORDER BY average_rating DESC LIMIT " + str(numOfComments))
    comments = c.fetchall()

    c.execute("SELECT * FROM books WHERE bookID=" + str(bookID))
    book = c.fetchone()
    c.execute("SELECT * FROM author_descriptions WHERE author=?", (book[2],))
    description = c.fetchone()
    if description:
        description = description[2]

    if comments:

        comment_users = []
        for comment in comments:
            c.execute("SELECT username FROM users WHERE userID=" + str(comment[2]))
            comment_username = c.fetchone()

            comment_users.append((comment, comment_username))

        return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = False, comments = comment_users, manager = manager, description = description, overview = overview)
    else:
        return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = False, comments = None, manager = manager, description = description, overview = overview)


@app.route('/addToWishlist/<int:userID>/<int:bookID>/<int:manager>', methods = ['POST', 'GET'])
def addToWishlist(userID, bookID, manager):

    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    c.execute("SELECT * FROM books WHERE bookID=" + str(bookID))
    book = c.fetchone()
    c.execute("SELECT * FROM author_descriptions WHERE author=?", (book[2],))
    description = c.fetchone()
    if description:
        description = description[2]

    c.execute("INSERT INTO wishlists VALUES (?, ?, ?)", (None, userID, bookID))
    conn.commit()
    conn.close()
    return render_template('book.html', userID = userID, book = book, AddedToWishlist = True, AddedToCart = False, manager = manager, description = description, overview = overview)

@app.route('/addToCart/<int:userID>/<int:bookID>/<int:manager>', methods = ['POST', 'GET'])
def addToCart(userID, bookID, manager):

    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    count = request.form['count']

    c.execute("SELECT * FROM books WHERE bookID=" + str(bookID))
    book = c.fetchone()
    c.execute("SELECT * FROM author_descriptions WHERE author=?", (book[2],))
    description = c.fetchone()
    if description:
        description = description[2]

    c.execute("SELECT price FROM book_prices WHERE bookID=" + str(bookID))
    book_price = c.fetchone()[0]

    c.execute("SELECT cartID FROM carts WHERE userID=" + str(userID))
    userCartID = c.fetchone()

    if not userCartID:
        c.execute("INSERT INTO carts VALUES (?, ?, ?)", (None, userID, 0))
        conn.commit()
        c.execute("SELECT cartID FROM carts WHERE userID=" + str(userID))
        userCartID = c.fetchone()[0]
    else:
        userCartID = userCartID[0]

    c.execute("UPDATE carts SET total = total+ " + count + "*" + str(book_price) + " WHERE userID=" + str(userID))
    conn.commit()

    c.execute("INSERT INTO cart_books VALUES (?, ?, ?, ?)", (None, userCartID, bookID, count))
    conn.commit()

    conn.close()

    return render_template('book.html', userID = userID, book = book, AddedToWishlist = False, AddedToCart = True, manager = manager, description = description, overview = overview)

@app.route('/cart/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def cart(userID, manager):

    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    c.execute("SELECT * FROM carts WHERE userID=" + str(userID))
    userCart = c.fetchone()

    if userCart:
        userCartID = userCart[0]
        c.execute("SELECT bookID, count FROM cart_books WHERE cartID=" + str(userCartID))
        book_counts = c.fetchall()

        book_counts_temp = []        
        for book_count in book_counts:
            c.execute("SELECT * FROM books WHERE bookID=" + str(book_count[0]))
            book = c.fetchone()
            book_counts_temp.append((book, book_count[1]))

        return render_template("cart.html", book_counts = book_counts_temp, userID = userID, cart = userCart, manager = manager)
    
    else:
        return render_template("cart.html", book_counts = None, userID = userID, cart = None, manager = manager)

@app.route('/wishlist/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def wishlist(userID, manager):

    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    c.execute("SELECT * FROM wishlists WHERE userID=" + str(userID))
    userWishlists = c.fetchall()

    if userWishlists:
        wishlist_books = []
        for userWishlist in userWishlists:
            c.execute("SELECT * FROM books WHERE bookID=" + str(userWishlist[2]))
            book = c.fetchone()
            wishlist_books.append(book)
        
        return render_template("wishlist.html", books = wishlist_books, userID = userID, manager = manager)
    
    else:
        return render_template("wishlist.html", books = None, userID = userID, manager = manager)

@app.route('/order/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def order(userID, manager):

    from datetime import date

    now = date.today()
    now = now.strftime("%Y-%m-%d")

    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    c.execute("SELECT * FROM carts WHERE userID=" + str(userID))
    userCart = c.fetchone()

    c.execute("SELECT * FROM cart_books WHERE cartID=" + str(userCart[0]))
    userCartBooks = c.fetchall()

    c.execute("INSERT INTO orders VALUES (?, ?, ?, ?)", (None, userID, userCart[2], now))
    conn.commit()

    c.execute("SELECT * FROM orders ORDER BY orderID DESC LIMIT 1")
    userOrder = c.fetchone()

    for userCartBook in userCartBooks:
        c.execute("INSERT INTO ordered_books VALUES (?, ?, ?, ?)", (None, userOrder[0], userCartBook[2], userCartBook[3]))
        conn.commit()

        c.execute("DELETE FROM cart_books WHERE cart_bookID=" + str(userCartBook[0]))
        conn.commit()

    c.execute("DELETE FROM carts WHERE cartID=" + str(userCart[0]))
    conn.commit()
    conn.close()

    return render_template("cart.html", book_counts = None, userID = userID, cart = None, manager = manager)
    
@app.route('/pastOrders/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def pastOrders(userID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    c.execute("SELECT * FROM orders WHERE userID=" + str(userID))
    userOrders = c.fetchall()

    if userOrders:
        purchasedBooks = []

        for userOrder in userOrders:

            c.execute("SELECT * FROM ordered_books WHERE orderID=" + str(userOrder[0]))
            book_orders = c.fetchall()

            for book_order in book_orders:
                c.execute("SELECT * FROM books WHERE bookID=" + str(book_order[2]))
                book = c.fetchone()
                purchasedBooks.append(book)
    
        return render_template("history.html", userID = userID, books = purchasedBooks, manager = manager)
    
    else:
        return render_template("history.html", userID = userID, books = None, manager = manager)
    

@app.route('/managerTab/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def managerTab(userID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE manager = 0")
    usersNotManager = c.fetchall()

    return render_template("manager.html", userID = userID, manager = manager, users = usersNotManager)

@app.route('/makeManager/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def makeManager(userID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    username = request.form['username']

    c.execute("UPDATE users SET manager = 1 WHERE username='" + str(username) + "'")
    conn.commit()

    c.execute("SELECT * FROM users WHERE manager = 0")
    usersNotManager = c.fetchall()

    return render_template("manager.html", userID = userID, manager = manager, users = usersNotManager)

@app.route('/changeStock/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def changeStock(userID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    bookID = request.form['bookID']
    stock = request.form['stock']

    c.execute("UPDATE stock SET count=" + str(stock) + " WHERE bookID=" + str(bookID))
    conn.commit()


    c.execute("SELECT * FROM users WHERE manager = 0")
    usersNotManager = c.fetchall()

    return render_template("manager.html", userID = userID, manager = manager, users = usersNotManager)

@app.route('/bookStats/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def bookStats(userID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    count = request.form['count']
    choice = request.form['choice']

    returnList = []

    if choice == 'book':
        c.execute("SELECT bookID FROM ordered_books GROUP BY bookID ORDER BY SUM(count) DESC LIMIT " + str(count))
        bookIDs = c.fetchall()

        for bookID in bookIDs:
            c.execute("SELECT * FROM books WHERE bookID=" + str(bookID[0]))
            book = c.fetchone()
            returnList.append(book)

    elif choice == 'author':
        c.execute("SELECT bookID, SUM(count) as count FROM ordered_books GROUP BY bookID")
        pairs = c.fetchall()

        author_count = {}

        for pair in pairs:
            c.execute("SELECT author FROM books WHERE bookID=" + str(pair[0]))
            author = c.fetchone()[0]

            if author in author_count:
                author_count[author] = author_count[author] + pair[1]
            else:
                author_count[author] = pair[1]

        returnList = dict(sorted(author_count.items(), key=lambda item: item[1]))
    
    elif choice == 'publisher':
        c.execute("SELECT bookID, SUM(count) as count FROM ordered_books GROUP BY bookID")
        pairs = c.fetchall()

        pub_count = {}

        for pair in pairs:
            c.execute("SELECT publisher FROM books WHERE bookID=" + str(pair[0]))
            publisher = c.fetchone()[0]

            if publisher in pub_count:
                pub_count[publisher] = pub_count[author] + pair[1]
            else:
                pub_count[publisher] = pair[1]

        returnList = dict(sorted(pub_count.items(), key=lambda item: item[1]))
    

    returnList = list(returnList)[0:int(count)]

    print(returnList)

    return render_template("returnList.html", userID = userID, manager = manager, returnList = returnList)

@app.route('/mostUsers/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def mostUsers(userID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    count = request.form['count']
    choice = request.form['choice']

    returnList = []

    if choice == 'trust':
        c.execute("SELECT trustUserID FROM trusts GROUP BY trustUserID ORDER BY COUNT(userID) DESC LIMIT " + str(count))
        returnList = c.fetchall()

    elif choice == 'useful':
        c.execute("SELECT commentUserID FROM comment_ratings GROUP BY commentUserID ORDER BY AVG(rating) DESC LIMIT " + str(count))
        returnList = c.fetchall()

    ret = []

    for e in returnList:
        c.execute("SELECT * FROM users WHERE userID=" + str(e[0]))
        user = c.fetchone()
        ret.append(user[1])  

    return render_template("returnList.html", userID = userID, manager = manager, returnList = ret)

@app.route('/addBook/<int:userID>/<int:manager>', methods = ['POST', 'GET'])
def addBook(userID, manager):
    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    isbn13 = request.form['isbn13']
    lang = request.form['lang']
    num_pages = request.form['num_pages']
    date = request.form['publication_date']
    pub = request.form['publisher']
    price = request.form['price']
    stock = request.form['stock']

    c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, title, author, 0, isbn, isbn13, lang, num_pages, 0, 0, date, pub))
    conn.commit()

    c.execute("SELECT bookID FROM books WHERE isbn=" + str(isbn))
    bookID = c.fetchone()[0]

    c.execute("INSERT INTO book_prices VALUES (?, ?, ?)", (None, bookID, price))
    conn.commit()

    c.execute("INSERT INTO stock VALUES (?, ?, ?)", (None, bookID, stock))
    conn.commit()

    c.execute("SELECT * FROM users WHERE manager = 0")
    usersNotManager = c.fetchall()

    return render_template("manager.html", userID = userID, manager = manager, users = usersNotManager)






def hash_password(password):
    from hashlib import sha256
    return sha256(password.encode('ascii')).hexdigest()

def run_search_query (form, userID):

    conn = sqlite3.connect("project.sqlite")
    c = conn.cursor()

    query = "SELECT * FROM books "
    first = True

    if form['author'] != '':
        query = query + "WHERE author = '" + form['author'] + "' "
        first = False
    
    if form['publisher'] != '':
        if not first:
            query = query + "AND "
        else:
            first = False
            query = query + "WHERE "
        query = query + "publisher = '" + form['publisher'] + "' "
    
    if form['title'] != '':
        if not first:
            query = query + "AND "
        else:
            first = False
            query = query + "WHERE "
        query = query + "title = '" + form['title'] + "' "
    
    if 'language' in form:
        if not first:
            query = query + "AND "
        else:
            first = False
            query = query + "WHERE "        
        language = form['language']
        if language == 'english':
            query = query + "(language_code = 'eng' OR language_code = 'en-US' OR language_code = 'en-GB' OR language_code = 'en-CA') "
        elif language == 'french':
            query = query + "language_code = 'fre' "
        elif language == 'spanish':
            query = query + "language_code = 'spa' "

    if 'order' in form:        
        order = form['order']
        if order == 'date':
            query = query + "ORDER BY date(publication_date) DESC"
        elif order == 'rating':
            query = query + "ORDER BY average_rating DESC"
        elif order == 'trust_rating':

            c.execute(query)
            result = c.fetchall()

            c.execute("""
            SELECT bookID, AVG(score) as average
            FROM (SELECT bookID, score
                  FROM comments INNER JOIN 
                  (
                    SELECT trustUserID FROM trusts WHERE userID=""" + str(userID) + """
                  ) AS trustedUsers
                  ON trustedUsers.trustUserID = comments.userID) AS pair
            GROUP BY pair.bookID
            ORDER BY average DESC
            """)
            pairs = c.fetchall()

            print(pairs)
            print(result)

            returnList = []

            for pair in pairs:
                for book in result:
                    if pair[0] == book[0]:
                        returnList.append(book)

            print(returnList)
            
            return returnList


    c.execute(query)
    result = c.fetchall()

    return result
    

        


if __name__ == "__main__":
    app.run(debug=True)