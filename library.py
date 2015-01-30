# Classes and methods for a simple library program
# Authors: Jincheng Cao, Alex Fiuk, Dave Matuszek
#--------------------------------------------------------------

class Calendar(object):
    """Keeps track of the durrent date (as an integer)."""
    
    def __init__(self):
        """Creates the initial calendar."""
        self.date = 0

    def get_date(self):
        """Returns (as a positive integer) the current date."""
        return self.date

    def advance(self):
        """Advances this calendar to the next date."""
        self.date += 1 

#--------------------------------------------------------------

class Book(object):
    """Represents one copy of a book. There may be many copies
       of a book with the same title and author.
       Each book has:
         * An id (a unique integer)
         * A title
         * An author (one string, even if many authors)
         * A due date (or None if the book is not checked out.)."""

    def __init__(self, title, author):
        """Creates a book, not checked out to anyone."""
        self.title = title
        self.author = author
        self.due_date = None

    def get_title(self):
        """Returns the title of this book."""
        return self.title

    def get_author(self):
        """Returns the author(s) of this book, as a single string."""
        return self.author

    def get_due_date(self):
        """If this book is checked out, returns the date on
           which it is due, else returns None."""
        return self.due_date

    def check_out(self, due_date):
        """Sets the due date for this book."""
        self.due_date = due_date

    def check_in(self):
        """Clears the due date for this book (sets it to None)."""
        self.due_date = None

    def __str__(self):
        """Returns a string representation of this book,
        of the form: title, by author"""
        return '%s, by %s' % (self.title, self.author)

    def __eq__(self, other):
        """Tests if this book equals the given parameter. Not
        required by assignment, but fairly important."""
        return self.title == other.title and self.author == other.author

#--------------------------------------------------------------

class Patron(object):
    """Represents a patron of the library. A patron has:
         * A name
         * A set of books checked out"""

    def __init__(self, name):
        """Constructs a new patron, with no books checked out yet."""
        self.name = name
        self.books = set()

    def get_name(self):
        """Returns this patron's name."""
        return self.name

    def get_books(self):
        """Returns the set of books checked out to this patron."""
        return self.books

    def take(self, book):
        """Adds a book to the set of books checked out to this patron."""
        self.books.add(book)

    def give_back(self, book):
        """Removes a book from the set of books checked out to this patron."""
        self.books.remove(book)

    def __str__(self):
        """Returns the name of this patron."""
        return self.name

#--------------------------------------------------------------

class Library(object):
    """Provides operations available to the librarian."""
    
    def __init__(self):
        """Constructs a library, which involves reading in a
           list of books that are in this library's collection."""
        
        # Create a global calendar, to be used by many classes
        global calendar
        calendar = Calendar()
        
        # Initialize some instance variables for _this_ library
        self.is_open = False            # Is library open?
        self.collection = []            # List of all Books
        self.patrons = set()               # Set of all Patrons
        self.patron_being_served = None # Current patron
        self.response = ''              # Accumulated messages to print
        
        # Read in the book collection
        file = open('collection.txt')
        for line in file:
            if len(line) > 1:
                tuple = eval(line.strip())
                self.collection.append(Book(tuple[0], tuple[1]))
        file.close()

    def open(self):
        """Opens this library for business at the start of a new day."""
        if self.is_open:
            return self.talk('The library is already open')
        else:
            calendar.advance()
            self.is_open = True
            return self.talk('Today is day %d' % calendar.get_date())

    def list_overdue_books(self):
        """Returns a nicely formatted, multiline string, listing the names
        of patrons who have overdue books, and for each such patron, the books
        that are overdue. Or, it returns the string "No books are overdue."""
        if not self.is_open:
            raise ValueError(self)
        self.all_overdue = ''
        for patron in self.patrons:
            self.indiv_overdue = []
            for book in patron.get_books():
                if book.get_due_date() < calendar.get_date():
                    self.indiv_overdue.append(book.get_title())
            if self.indiv_overdue != []:
                self.all_overdue += patron.__str__() + ':' + '\n' + self.create_numbered_list(self.indiv_overdue)
        if self.all_overdue == '':
            self.all_overdue += 'No books are overdue'
        self.talk(self.all_overdue)

                
    def issue_card(self, name_of_patron):
        """Allows the named person the use of this library. For
           convenience, immediately begins serving the new patron."""
        if not self.is_open:
            raise ValueError(self)

        else:
            if name_of_patron in self.patrons:
                self.talk("%s already has a library card." % name_of_patron)
                self.serve(name_of_patron)
            else:
                self.patrons.add(Patron(name_of_patron))
                self.talk("Library card issued to %s." % name_of_patron)
                self.serve(name_of_patron)

    def serve(self, name_of_patron):
        """Saves the given patron in an instance variable. Subsequent
           check_in and check_out operations will refer to this patron,
           so that the patron's name need not be entered many times."""
        if not self.is_open:
            raise ValueError(self)
        test_card = False
        for patron in self.patrons:
            if patron.get_name() == name_of_patron:
                self.patron_being_served = patron
                test_card = True
                self.talk("Now serving %s." % name_of_patron)
                if len(self.patron_being_served.get_books()) > 0:
                    self.talk("%s has these books:" % name_of_patron)
                    self.returned_books = []
                    for book in self.patron_being_served.get_books():
                        self.returned_books.append(book.__str__())
                    self.talk(self.create_numbered_list(self.returned_books))

        if not test_card:
            self.talk("%s does not have a library card." % name_of_patron)


    def check_in(self, *book_numbers):
        """Accepts books being returned by the patron being served,
           and puts them back "on the shelf"."""

        if self.is_open == False:
            raise ValueError(self)
        if self.patron_being_served == None:
            raise NameError(self)
        book_counter = 0
        for number in book_numbers:
            if number not in range(1, len(self.patron_being_served.get_books()) + 1):
                print "The patron does not have book %d." % number
                raise IndexError
            for book in self.patron_being_served.get_books():
                if book.__str__() == self.returned_books[number - 1]:
                    self.patron_being_served.give_back(book)
                    book.check_in()
                    self.collection.append(book)
                    book_counter += 1
                    break
        self.talk("%s has returned %d books." % (self.patron_being_served, book_counter))

    def search(self, string):
        """Looks for books with the given string in either the
           title or the author's name, and creates a globally
           available numbered list in self.found_books."""
        if len(string) < 4:
            return self.talk('Search string must contain at least four characters.')
        self.found_books = []
        for book in self.collection:
            if string.lower() in book.get_title().lower() or string in book.get_author().lower():
                if book.__str__() not in self.found_books:
                    self.found_books.append(book.__str__())
        if self.found_books == []:
            return self.talk('No books found')
        self.talk(self.create_numbered_list(self.found_books))

    def create_numbered_list(self, items):
        """Creates and returns a numbered list of the given items,
           as a multiline string. Returns "Nothing found." if the
           list of items is empty."""
        if items == []:
            return self.talk('No books found.')

        numbered_list = ''
        for i in items:
            if items.index(i) < 10:
                numbered_list += '\t' + str(items.index(i) + 1) + '. ' + i + '\n'
            else:
                 more_items = len(items)-items.index(i)
                 numbered_list += '\t...and ' + str(more_items) + 'more.'
                 break
        return numbered_list

    def check_out(self, *book_numbers):
        """Checks books out to the patron currently being served.
           Books will be due seven days from "today".
           Patron must have a library card, and may have not more
           than three books checked out at a time."""
        if self.is_open == False:
            raise ValueError(self)
        if self.patron_being_served == None:
            raise NameError(self)
        book_counter = 0
        for number in book_numbers:
            # ensure patron does not exceed limit of 3 books
            if len(self.patron_being_served.get_books()) == 3:
                return self.talk("Sorry, %s already has 3 books checked out." % self.patron_being_served.get_name())
            # ensure the requested book exists in the library
            if number not in range(1, len(self.found_books) + 1):
                return self.talk("The library does not have book %d." % number)
                raise IndexError
            # check book out to patron and remove from collection
            found_book = False
            for book in self.collection:
                if book.__str__() == self.found_books[number - 1]:
                    found_book = True
                    book_counter += 1
                    self.patron_being_served.take(book)
                    book.check_out(calendar.get_date() + 7)
                    self.collection.remove(book)
                    break
            if not found_book:
                self.talk("Book %d is borrowed." % number)
        self.talk("%d books have been checked out to %s." %(book_counter, self.patron_being_served.get_name()))
        for book in self.patron_being_served.get_books():
            self.talk("%s, checked out to %s." % (book.title, self.patron_being_served.get_name()))

    def close(self):
        """Closes the library for the day."""
        if not self.is_open:
            return self.talk('The library is not open')
        else:
            self.patron_being_served = None
            self.is_open = False
            return self.talk('Good night')

    def quit(self):
        return self.talk('The library is now closed for renovations')

    def help(self):
        self.talk("""
help()
     Repeat this list of commands.
open()
     Opens the library for business; do this once each morning.
     
list_overdue_books()
     Prints out information about books due yesterday.
     
issue_card("name_of_patron")
     Allows the named person the use of the library.
     
serve("name_of_patron")
     Sets this patron to be the current patron being served.
     
search("string")
     Searches for any book or author containing this string
     and displays a numbered list of results.
     
check_out(books...)
     Checks out books (by number) to the current patron.
     
check_in(books...)
     Accepts returned books (by number) from the current patron.
     
close()
     Closes the library at the end of the day.

quit()
     Closes the library for good. Hope you never have to use this!""")

    # ----- Assorted helper methods (of Library) -----

    def talk(self, message):
        """Accumulates messages for later printing. A newline is
           appended after each message."""
        self.response += message + '\n'

    # Feel free to add any more helper methods you would like

#--------------------------------------------------------------

def main():
    library = Library()
    print len(library.collection), 'books in collection.'
    print "Ready for input. Type 'help()' for a list of commands.\n"
    command = '\0'
    while command != 'quit()':
        try:
            command = raw_input('Library command: ').strip()
            if len(command) == 0:
                print "What? Speak up!\n"
            else:
                eval('library.' + command)
                print library.response
                library.response = ''

        except ValueError:
            print "The library is not open."
        except NameError:
            print "No patron is currently being served."
        except IndexError:
            pass
        except AttributeError, e:
            print "Sorry, I didn't understand:", command
            print "Type 'help()' for a list of the things I do understand.\n"
        except Exception, e:
            print "Unexpected error:", e

if __name__ == '__main__':
    main()

