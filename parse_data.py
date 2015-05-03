import csv
import datetime
from app.models import *
from app import db


def create_publish_date(month_string, year_string):
    try:
        year = int(year_string)
        month = int(month_string)
    except:
        return
    if year_string and month_string:
        if month > 12 or month < 1:
            month = 1
        day = 1
        date_object = datetime.date(year, month, day)
        print str(date_object)
        return date_object

def get_boolean_val(val):
    return True if val == '-1' or val == 'Yes' else False

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
        new_book_dict['date_entered'] = datetime.datetime.strptime(new_book_dict.get('date_entered'),"%m/%d/%Y").date()

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

# with open('/Users/lorenamesa/Desktop/brown-baby-reads/books.csv', 'rb') as csvfile:
#     counter = 0
#     bookreader = csv.DictReader(csvfile)
#     for row in bookreader:
#         book_data = warp_csv_dict(row)
#         book = Book(book_data)
#         # print book.to_dict()['title']
#         # authors = create_authors(row['Authors_1'])
#         authors = row['Authors_1'].split(',')
#         for author in authors:
#             a = Author.query.filter_by(name=author.strip()).first()
#             # all_authors.append(author)
#             if a:
#                 book.authors.append(a)
#
#         keywords = row['Keywords'].split(',')
#         for keyword in keywords:
#             k = Keyword.query.filter_by(keyword=keyword.strip()).first()
#             # all_authors.append(author)
#             if k:
#                 book.keywords.append(k)
#
#         curriculum = [row.get('Curriculum_Links1'), row.get('Curriculum_Links2'), row.get('Curriculum_Links3'), row.get('Curriculum_Links4')]
#         # curriculum = create_curriculum(curriculum)
#         for curricula in curriculum:
#             # all_curriculum.append(curricula)
#             c = Curricula.query.filter_by(link=curricula.strip()).first()
#             if c:
#                 book.curriculum.append(c)
#
#         counter += 1
#         # print book.to_dict()
#
#         db.session.add(book)
#         db.session.commit()
#         print "counter %s" % counter

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

def warp_article_dict(data):
    new_article_dict = {}
    article_fields = ('article', 'title', 'authors', 'publisher_journal',
                      'volume_page', 'year', 'month', 'summary_link',
                      'keywords', 'picture')
    boolean_fields = ('book','academic_journal')

    for key, val in data.iteritems():
        if key.lower() in article_fields:
            new_article_dict[key.lower()] = val.strip()
        elif key.lower() in boolean_fields:
            new_article_dict[key.lower()] = get_boolean_val(val)

    if new_article_dict.get('entire_article_link'):
        new_article_dict['article_link'] = new_article_dict.get('entire_article_link')

    if new_article_dict.get('subject_topic'):
        new_article_dict['subject'] = new_article_dict.get('subject_topic')

    if new_article_dict.get('description_synopsis'):
        new_article_dict['description'] = new_article_dict.get('description_synopsis')

    publish_date = create_publish_date(data.get('Month'), data.get('Publish_Year'))
    new_article_dict['publish_date'] = publish_date
    return new_article_dict

with open('/Users/lorenamesa/Desktop/brown-baby-reads/research_articles.csv', 'rb') as csvfile:
    counter = 0
    reader = csv.DictReader(csvfile)
    for row in reader:
        data = warp_article_dict(row)
        article = Article(data)

        counter += 1
        # print book.to_dict()

        db.session.add(article)
        db.session.commit()
        print "counter %s" % counter