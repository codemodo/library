import unittest
from library import *

lib = Library()
lib.open()



class CalendarTest(unittest.TestCase):

    def test_calendar(self):
        global cal
        cal = Calendar()
        self.assertEqual(0, cal.get_date())
        cal.advance()
        self.assertEqual(1, cal.get_date())

class BookTest(unittest.TestCase):

    def setUp(self):
        global book
        book = Book("Contact", "Carl Sagan")
        self.assertTrue(type(book) is Book)

    def test_get_title(self):
        self.assertEqual("Contact", book.get_title())

    def test_get_author(self):
        self.assertEqual("Carl Sagan", book.get_author())

    def test_get_due_date(self):
        self.assertEqual(None, book.get_due_date())

    def test_book_check_out_and_check_in(self):
        book = Book("Contact", "Carl Sagan")
        self.assertEqual(None, book.get_due_date())
        lib.serve("Amy Gutmann")
        book.check_out(17)
        self.assertEqual(17, book.get_due_date())
        book.check_in()
        self.assertEqual(None, book.get_due_date())

class PatronTest(unittest.TestCase):

    def test_patron(self):
        patron = Patron("Amy Gutmann")
        self.assertEquals("Amy Gutmann", patron.get_name())
        self.assertEquals(set([]), patron.get_books())

class LibraryTest(unittest.TestCase):

    def setUp(self):
        name = "Amy"
        lib.issue_card(name)
        lib.serve(name)

    def test_open(self):
        lib.is_open = False
        lib.open()
        self.assertEqual(True, lib.is_open)

    def test_list_overdue_books(self):
        lib.patrons = set()
        lib.issue_card("Bob")
        lib.serve("Bob")
        lib.search("20,000")
        lib.all_overdue = ""
        lib.check_out(1)
        for i in range(1,10):
            lib.close()
            lib.open()
            
        lib.list_overdue_books()
        self.assertEqual('Bob:\n\t1. 20,000 Leagues Under the Seas\n', lib.all_overdue)
        
    def test_issue_card(self):
        lib.issue_card("Amy")
        self.assertTrue(lib.patrons is not None)

    def test_serve(self):
        self.assertEqual("Amy", lib.patron_being_served.get_name())

    def test_search(self):
        lib.search("20,000")
        self.assertEqual("\t1. 20,000 Leagues Under the Seas, by Jules Verne\n", lib.create_numbered_list(lib.found_books))
        
    def test_create_numbered_list(self):
        self.assertEqual(None, lib.create_numbered_list([]))
        self.assertEqual('\t1. Apple\n\t2. Orange\n\t3. Kiwi\n', lib.create_numbered_list(['Apple', 'Orange', 'Kiwi']))

    def test_check_out(self):
        lib.search("20,000")
        lib.found_books = ['20,000 Leagues Under the Seas, by Jules Verne']
        a = len(lib.collection)
        lib.check_out(1)
        self.assertEqual(a-1, len(lib.collection))
        book =  lib.patron_being_served.get_books()
        self.assertTrue(book == lib.patron_being_served.books)
        
    def test_check_in(self):
        lib.search("20,000")
        lib.found_books = ['20,000 Leagues Under the Seas, by Jules Verne']
        lib.check_out(1)
        a = len(lib.collection)
        book =  lib.patron_being_served.get_books()
        lib.serve("Amy")
        lib.check_in(1)
        self.assertEqual(0, len(lib.patron_being_served.get_books()))
        self.assertEqual(a+1, len(lib.collection))

    def test_close(self):
        lib.is_open = True
        lib.close()
        self.assertEqual(False, lib.is_open)
        lib.open()
        
unittest.main()
