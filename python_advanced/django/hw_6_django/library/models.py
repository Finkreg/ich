from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    surname = models.CharField(max_length=100, verbose_name="Surname")
    birthday = models.DateField(null=True, blank=True, verbose_name="Birthday")
    profile = models.URLField(null=True, blank=True, verbose_name="Link to the author's website")
    is_removed = models.BooleanField(default=False, help_text='Was the author removed from database')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.name} {self.surname}"
    
genre_choices = {'Fiction':'Fiction', 
                 'Fantasy': 'Fantasy', 
                 'Mystery': 'Mystery',
                 'Default':'not-set'}
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    genre = models.CharField(choices=genre_choices, default='not-set')
    pages_ammount = models.PositiveIntegerField(validators=[MaxValueValidator(10000)], default = 100)
    publisher = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True, verbose_name="Publisher")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, verbose_name='Category', null=True)
    libraries = models.ManyToManyField('Library', related_name='books', verbose_name="Library")


    @property
    def rating(self):
        return self.reviews.all().aggregate(models.Avg('rating')['rating__avg'])

    def __str__(self):
        return f"{self.title}"


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Category Title", unique=True)


    def __str__(self):
        return f"{self.name}"


class Library(models.Model):
    title = models.CharField(max_length=100, verbose_name="Library Ttile")
    location = models.CharField(max_length=100, null=True, blank=False, verbose_name='Location')
    website=models.URLField(null=True, blank=True, verbose_name='Website')


    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name_plural = "Libraries"

gender_choice = {
    "M": "Male",
    "F": "Female"
}

role_choices = {
    "A": "Administrator",
    "R": "Reader",
    "E": "Employee"
}

class Member(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First_name")
    last_name = models.CharField(max_length=50, verbose_name="Last_name")
    email = models.EmailField(null=False, blank=False, unique=True, verbose_name="Email")
    gender = models.CharField(max_length=1, verbose_name="Gender", choices=gender_choice) 
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    age = models.PositiveIntegerField(verbose_name="Age") 
    role = models.CharField(max_length=1, verbose_name="Role", choices=role_choices) 
    active = models.BooleanField(default=True, verbose_name="Is active")
    libraries = models.ManyToManyField('Library', related_name="members")

    def save(self, *args, **kwargs):
        ages = timezone.now().year - self.date_of_birth.year
        if 6 <= ages < 120:
            self.age = ages
            super().save(*args, **kwargs)
        else:
            raise ValidationError ("Age must be between 6 and 120")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Post(models.Model):
    created_at = models.DateTimeField(verbose_name="Created at")
    title = models.CharField(max_length=255, unique_for_date=created_at, verbose_name="Title")
    text = models.TextField(null=False, blank=False, verbose_name="Text")
    author = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    moderated = models.BooleanField(default=False, verbose_name="Moderated")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, verbose_name="Library")
    updated_at = models.DateTimeField(auto_now=True)


class Borrow(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="Member")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Book")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, verbose_name="Library")
    book_take_date = models.DateField(auto_now_add=True, verbose_name="Book Take Date")
    book_return_date = models.DateField(verbose_name="Book return date")
    is_returned = models.BooleanField(default=False, verbose_name="Is returned?")

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name} took '{self.book.title}' on {self.book_take_date}"


    def check_to_date(self):
        if timezone.now().date() > self.book_return_date and self.is_returned == False:
            return True
        else:
            return False
        


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Book", related_name='reviews')
    reviewer = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="Reviewer")
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Rating")
    review = models.TextField(verbose_name="Review")


class AuthorDetail(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Author")
    biography = models.TextField(verbose_name="Biography")
    city = models.CharField(verbose_name="City", max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=gender_choice, verbose_name="Gender")

    def __str__(self):
        return f"{self.author}"
    

class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    timestamp = models.DateTimeField(verbose_name="Event date")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, verbose_name="Library")
    book = models.ManyToManyField(Book, verbose_name="Books", related_name="Event")

    def __str__(self):
        return f"{self.name} on {self.timestamp}"

class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Event")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="Member")
    register_date = models.DateField(auto_now_add=True, verbose_name="Register date")

    def __str__(self):
        return f"{self.event.name}. Member: {self.member.first_name} {self.member.last_name} registered on {self.register_date}"