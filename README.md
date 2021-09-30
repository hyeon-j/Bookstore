# Bookstore project by Hyeon Joon Song
Created a simple bookstore website using Python, sqlite, Flask, HTML/CSS.

Project: Online Book Store

Hyeon Joon Song

CMPSC 431W


Software:

•	Python 3.6: https://www.python.org/

•	Flask 1.12: https://flask.palletsprojects.com/

•	sqlite3


The software that is required to deploy the system is Python 3.6 and Flask 1.1.2. Downloads for each software can be found in the websites above



How to deploy:

Once all the files for the system and software mentioned in Software has been downloaded, the only thing left to do to deploy the system is to run the app.py file. This can be achieved by running “python app.py” in the command line in the file directory of the app.py file. Once executed, copy the localhost address into your browser and everything should be there. The OS does not matter when deploying the system.

Functionalities:

•	User Login: On the very first page after deploying the system, the user can input his/her account’s username and password to log in. If they don’t match, it doesn’t let the user log in.

•	Registration: On the very first page after deploying the system, the user can register for an account by pressing on Register. Once clicked, the user can enter their username, password, address, and phone number. If the username is already taken, it will prompt the user that the username is taken.

•	Browse Book: Once logged in, the user can search for books by author and/or publisher and/or title and/or the language. The user can also order the search results by date, overall ratings of the books, or the ratings of the books by whom the user trusts.

•	Browse Customer Profiles: If the user wants to trust another user, the user can click “Trust this User” under the comment.

•	Cart: When viewing a book, the user can add any number of copies of the book into their cart. The user can click “Cart” that is located on the top of every page to view their cart or to order the books in their cart.

•	Order: Once in the cart tab, the user can click on “Order” to process his/her order.

•	Wishlist: The user can click on “Wishlist” located on the top of the page to view his/her books that has been added to their Wishlist.

•	Stock Management: If the user is a manager, the user can click on the “Manager Tab” located on the top of the page to manage the stock level of a specific book.

•	Give Manager Role: If the user is a manager, the user can click on the “Manager Tab” located on the top of every page to set a specific user as a manager.

•	Add book: If the user is a manager, the user can click on the “Manager Tab” located on the top of every page to add a book into the system.

•	Order Statistics: If the user is a manager, the user can click on the “Manager Tab” located on the top of every page to view order statistics. The manager can view the top n books or authors or publisher.

•	User Statistics: If the user is a manager, the user can click on the “Manager Tab” located on the top of every page to view user statistics. The manager can view the top n most useful or trusted users.

•	Purchase History: The user can click on “Purchase History” located on every page to view his/her purchase history.

•	Rate Comments: When viewing a specific book, the user can rate the comments by giving it a score of 0~5.
