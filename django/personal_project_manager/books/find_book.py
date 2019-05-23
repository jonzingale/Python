import django_rq
from 'lcc_scraper/loc_book_scraper' import find_book

# be sure that redis is running: start_redis
# to pick up queue run: python manage.py rqworker default
def find_by_title(title)
  queue = django_rq.get_queue('default')
  queue.enqueue(find_book, title)