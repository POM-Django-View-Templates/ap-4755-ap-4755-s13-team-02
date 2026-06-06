from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    count = models.IntegerField(default=1)
    authors = models.ManyToManyField("author.Author", related_name="books")

    def __str__(self):
        return f"'id': {self.id}, 'name': '{self.name}', 'description': '{self.description}', 'count': {self.count}, 'authors': {list(self.authors.all())}"

    def __repr__(self):
        return f"Book(id={self.id})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "count": self.count,
            "authors": [author.id for author in self.authors.all()],
        }

    @staticmethod
    def create(name, description, count, authors=None):
        try:
            book = Book(name=name, description=description, count=count)
            book.save()
            if authors:
                book.authors.set(authors)
            return book
        except Exception:
            return None

    @staticmethod
    def get_by_id(book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        return list(Book.objects.all())

    def update(self, name=None, description=None, count=None):
        if name:
            self.name = name
        if description:
            self.description = description
        if count:
            self.count = count
        self.save()

    @staticmethod
    def delete_by_id(book_id):
        book = Book.get_by_id(book_id)
        if book:
            book.delete()
            return True
        return False
