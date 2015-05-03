import csv
import datetime
from app.models import *
from app import db


def create_publish_date(year_string, month_string):
    try:
        year = int(year_string)
    except:
        return
    if year_string and month_string:
        month = int(month_string)
        if month > 12 or month < 1:
            month = 1
        if year > 12 or year < 1:
            month = 1
        day = 1
        date_object = datetime.datetime(year, month, day)

        return date_object

def get_boolean_val(val):
    return True if val == '-1' else False

def warp_csv_dict(data):
    new_book_dict = {}
    book_fields = ('booklists','title','lexile','google_book_preview', 'age_group', 'type', 'illustrator','isbn_13','publish_date','pages',
                   'description','reading_grade_level','interest_level','dra','guided_reading_level', 'publisher', 'parent_publisher',
                   'bbr_estore_link','ebay_link','amazon_link','biography_person','picture', 'series','pages')
    boolean_fields = ('out_of_print','reading_room')

    for key, val in data.iteritems():
        if key.lower() in book_fields:
            new_book_dict[key.lower()] = val.strip()
        elif key.lower() in boolean_fields:
            new_book_dict[key.lower()] = get_boolean_val(val)

    if new_book_dict.get('date_entered'):
        new_book_dict['date_entered'] = datetime.datetime.strptime(new_book_dict.get('date_entered'),"%m/%d/%Y")

    publish_date = create_publish_date(data.get('Month'), data.get('Publish_Year'))
    new_book_dict['publish_date'] = publish_date
    return new_book_dict

def create_authors(authors_string):
    authors = authors_string.split(',')
    authors = [Author(author.strip()) for author in authors]
    return authors

def create_keywords(keywords_string):
    keywords = keywords_string.split(',')
    keywords = [Keyword(keyword.strip()) for keyword in keywords]
    return keywords

def create_curriculum(curriculum):
    curriculum = [Curricula(curricula.strip()) for curricula in curriculum if curricula]
    for c in curriculum:
        print c.link
    return curriculum

all_authors = []
all_keywords = []
all_curriculum = []
all_publishers = []

with open('/Users/lorenamesa/Desktop/brown-baby-reads/books.csv', 'rb') as csvfile:
    counter = 0
    bookreader = csv.DictReader(csvfile)
    for row in bookreader:
        book_data = warp_csv_dict(row)
        book = Book(book_data)
        # print book.to_dict()['title']
        # authors = create_authors(row['Authors_1'])
        authors = row['Authors_1'].split(',')
        for author in authors:
            a = Author.query.filter_by(name=author.strip()).first()
            # all_authors.append(author)
            if a:
                book.authors.append(a)

        keywords = row['Keywords'].split(',')
        for keyword in keywords:
            k = Keyword.query.filter_by(keyword=keyword.strip()).first()
            # all_authors.append(author)
            if k:
                book.keywords.append(k)

        curriculum = [row.get('Curriculum_Links1'), row.get('Curriculum_Links2'), row.get('Curriculum_Links3'), row.get('Curriculum_Links4')]
        # curriculum = create_curriculum(curriculum)
        for curricula in curriculum:
            # all_curriculum.append(curricula)
            c = Curricula.query.filter_by(link=curricula.strip()).first()
            if c:
                book.curriculum.append(c)

        counter += 1
        # print book.to_dict()

        db.session.add(book)
        db.session.commit()
        print "counter %s" % counter

    # all_things = all_authors + all_keywords + all_curriculum + all_publishers
    # for author in all_authors:
    #     found = Author.query.filter_by(name=author.name).first()
    #     if not found:
    #         db.session.add(author)
    #         db.session.commit()
    # for keyword in all_keywords:
    #     found = Keyword.query.filter_by(keyword=keyword.keyword).first()
    #     if not found:
    #         db.session.add(keyword)
    #         db.session.commit()
    # for c in all_curriculum:
    #     found = Curricula.query.filter_by(link=c.link).first()
    #     if not found:
    #         db.session.add(c)
    #         db.session.commit()


    # db.session.commit()
# ['Distribution_Age_Gender_Sampler', 'Classroom_Support', 'CSP_BookType', 'BookLists',
#  'Audio_Book', 'NewCurriculum', 'Title', 'BBR_Page_Link', 'Book_Tournament_K_1st',
#  'Audiobook_Link', 'Lexile', 'Feature_Date', 'CSP_Curriculum', 'Reading_Room_Quantity',
#  'Reading_Room', 'Authors_1', 'Distribtuion_Book_Bundle_Series', 'DRA', 'google_book_preview',
#  'Distribution_BoxBook', 'Age_Group', 'Book_Tournament_4th_5th', 'Picture', 'CurriculumEnterDate',
#  'Date_Entered', 'Description', 'BookID', 'Hardcover', 'Type', 'Author_Link', 'Kids_Description',
#  'Distribution_Merchandising', 'BoardBook_Retail', 'CurriculumLink1_Acknowledgement', 'BoardBook',
#  'Curriculum_Links5', 'Interest_Level', 'Book_Reviewer_Highlight', 'Pages', 'Curriculum_Links4',
#  'Publisher', 'Illustrator', 'Curriculum_Links1', 'Curriculum_Links2', 'Curriculum_Links3', 'Biography_Person',
#  'Gender', 'Ebay_Link', 'Guided_Reading_Level', 'Out_of_Print', 'Curriculum_on_File', 'Distribution_Subscription',
#  'Title_alphabetical', 'Recommended_Age', 'Paperback_Retail', 'classroom_support_choice', 'BBR_estore_link', 'Distribution_Book_Box', 'Paperback', 'BookClubCategory', 'Reading_Grade_Level', 'Hardcover_Retail', 'Book_Tournament_2nd_3rd', 'Series', 'Parent_Publisher', 'Author_on_File', 'Month', 'ISBN_13', 'GenreSubject_1', 'Publish_Year', 'Amazon_Link', 'Classroom_Support_Book', 'Keywords', 'Publish_Month', 'Distribution_Book_Bundle_Group']
