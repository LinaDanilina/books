from django.db import models

class Book(models.Model):
    book_title=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')
    book_description = models.CharField(max_length=1000)
    book_author = models.CharField(max_length=200)

    def __str__(self):
        return self.book_title

class Opinion(models.Model):
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    opinion_text=models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.opinion_text
