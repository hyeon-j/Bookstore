import sqlite3

conn = sqlite3.connect("project.sqlite")
c = conn.cursor()


# books Table
# c.execute("""
# CREATE TABLE books (
#     bookID INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT NOT NULL,
#     author TEXT NOT NULL,
#     average_rating DECIMAL(3,2) NOT NULL,
#     isbn INTEGER NOT NULL,
#     isbn13 INTEGER NOT NULL,
#     language_code TEXT NOT NULL,
#     num_pages INTEGER NOT NULL,
#     ratings_count INTEGER NOT NULL,
#     text_reviews_count INTEGER NOT NULL,
#     publication_date TEXT NOT NULL,
#     publisher TEXT NOT NULL
# )
# """)

# book_prices Table
# c.execute("""
# CREATE TABLE book_prices (
#     priceID INTEGER PRIMARY KEY AUTOINCREMENT,
#     bookID INTEGER NOT NULL,
#     price DECIMAL(6,2) NOT NULL,
#     FOREIGN KEY(bookID) REFERENCES books(bookID)
# )
# """)

# keywords Table
# c.execute("""
# CREATE TABLE keywords (
#     keywordID INTEGER PRIMARY KEY AUTOINCREMENT,
#     bookID INTEGER NOT NULL,
#     keyword TEXT NOT NULL,
#     FOREIGN KEY(bookID) REFERENCES books(bookID)
# )
# """)

# users Table
# c.execute("""
# CREATE TABLE users (
#     userID INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT NOT NULL UNIQUE,
#     password TEXT NOT NULL,
#     address TEXT NOT NULL,
#     phone_number TEXT NOT NULL,
#     manager INT NOT NULL
# )
# """)

# trusts Table
# c.execute("""
# CREATE TABLE trusts (
#     trustID INTEGER PRIMARY KEY AUTOINCREMENT,
#     userID INTEGER NOT NULL,
#     trustUserID INTEGER NOT NULL,
#     FOREIGN KEY(userID) REFERENCES users(userID),
#     FOREIGN KEY(trustUserID) REFERENCES users(userID)
# )
# """)

# orders Table
# c.execute("""
# CREATE TABLE orders (
#     orderID INTEGER PRIMARY KEY AUTOINCREMENT,
#     userID INTEGER NOT NULL,
#     total DECIMAL(6,2) NOT NULL,
#     order_date TEXT NOT NULL,
#     FOREIGN KEY (userID) REFERENCES users(userID)
# )
# """)

# ordered_books Table
# c.execute("""
# CREATE TABLE ordered_books (
#     ordered_bookID INTEGER PRIMARY KEY AUTOINCREMENT,
#     orderID INTEGER NOT NULL,
#     bookID INTEGER NOT NULL,
#     count INTEGER NOT NULL,
#     FOREIGN KEY (orderID) REFERENCES orders(orderID),
#     FOREIGN KEY (bookID) REFERENCES books(bookID)
# )
# """)

# stock Table
# c.execute("""
# CREATE TABLE stock (
#     stockID INTEGER PRIMARY KEY AUTOINCREMENT,
#     bookID INTEGER NOT NULL UNIQUE,
#     count INTEGER NOT NULL,
#     FOREIGN KEY (bookID) REFERENCES books(bookID)
# )
# """)

# comments Table
# c.execute("""
# CREATE TABLE comments (
#     commentID INTEGER PRIMARY KEY AUTOINCREMENT,
#     bookID INTEGER NOT NULL,
#     userID INTEGER NOT NULL,
#     score INT NOT NULL,
#     text TEXT,
#     average_rating DECIMAL(3,2) NOT NULL,
#     date TEXT NOT NULL,
#     FOREIGN KEY (bookID) REFERENCES books(bookID),
#     FOREIGN KEY (userID) REFERENCES users(userID)
# )
# """)

# comment_ratings Table
# c.execute("""
# CREATE TABLE comment_ratings (
#     comment_ratingID INTEGER PRIMARY KEY AUTOINCREMENT,
#     commentID INTEGER NOT NULL,
#     userID INTEGER NOT NULL,
#     rating INT NOT NULL,
#     FOREIGN KEY (commentID) REFERENCES comments(commentID)
#     FOREIGN KEY (userID) REFERENCES users(userID)
# )
# """)

# wishlists Table
# c.execute("""
# CREATE TABLE wishlists (
#     wishlistID INTEGER PRIMARY KEY AUTOINCREMENT,
#     userID INTEGER NOT NULL,
#     bookID INTEGER NOT NULL,
#     FOREIGN KEY (bookID) REFERENCES books(bookID),
#     FOREIGN KEY (userID) REFERENCES users(userID)
# )
# """)

# carts Table
# c.execute("""
# CREATE TABLE carts (
#     cartID INTEGER PRIMARY KEY AUTOINCREMENT,
#     userID INTEGER NOT NULL,
#     total DECIMAL(6,2) NOT NULL,
#     FOREIGN KEY (userID) REFERENCES users(userID)
# )
# """)

# cart_books Table
# c.execute("""
# CREATE TABLE cart_books (
#     cart_bookID INTEGER PRIMARY KEY AUTOINCREMENT,
#     cartID INTEGER NOT NULL,
#     bookID INTEGER NOT NULL,
#     count INT NOT NULL,
#     FOREIGN KEY (cartID) REFERENCES carts(cartID),
#     FOREIGN KEY (bookID) REFERENCES books(bookID)
# )
# """)

# book_overviews Table
# c.execute("""
# CREATE TABLE book_overviews (
#     book_overviewID INTEGER PRIMARY KEY AUTOINCREMENT,
#     bookID INTEGER NOT NULL,
#     overview TEXT NOT NULL,
#     FOREIGN KEY (bookID) REFERENCES books(bookID)
# )
# """)

# author_descriptions Table
# c.execute("""
# CREATE TABLE author_descriptions (
#     author_descriptionID INTEGER PRIMARY KEY AUTOINCREMENT,
#     author TEXT NOT NULL UNIQUE,
#     description TEXT NOT NULL
# )
# """)

# Inserting books to books
# import csv
# with open('books.csv', 'r', encoding = 'utf-8') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     next(csv_reader)
#     count = 0
#     for line in csv_reader:
#         if count >= 100:
#             break

#         date = line[10].split('/')
#         temp = date[2] + "-"
#         if int(date[0]) < 10:
#             temp = temp + "0" + date[0] + "-"
#         else:
#             temp = temp + date[0] + "-"
#         if int(date[1]) < 10:
#             temp = temp + "0" + date[1]
#         else:
#             temp = temp + date[1]
        
#         c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], temp, line[11]))
#         conn.commit()


conn.commit()
conn.close()