import feedparser
from django.core.management.base import BaseCommand
from blogs.models import Blog
from django.utils import timezone
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = 'Import blood-related blog posts from external RSS feeds'

    def handle(self, *args, **kwargs):
        feed_urls = [
            'https://www.carterbloodcare.org/feed',
            'https://stanfordbloodcenter.org/feed',
            'https://www.bbguy.org/feed',
            'https://blog.bloodworksnw.org/feed',
            'https://biobridgeglobal.org/feed',
            'https://medium.com/feed/@ayushbindu',
            'https://incept-health.com/insights/feed',
            # Add more RSS feed URLs as needed
        ]

        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if not Blog.objects.filter(link=entry.link).exists():
                    published_time = entry.get('published_parsed')
                    if published_time:
                        published_datetime = datetime(*published_time[:6], tzinfo=pytz.utc)
                    else:
                        published_datetime = timezone.now()

                    Blog.objects.create(
                        title=entry.title,
                        content=entry.summary,
                        link=entry.link,
                        published_date=published_datetime,
                        source=feed.feed.get('title', 'Unknown Source')
                    )
                    self.stdout.write(self.style.SUCCESS(f'Imported: {entry.title}'))
