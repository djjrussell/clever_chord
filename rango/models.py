from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from engine import Chord


class Category(models.Model):
        name = models.CharField(max_length=128, unique=True)
        views = models.IntegerField(default=0)
        likes = models.IntegerField(default=0)
        slug = models.SlugField(unique=True)

        def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Category, self).save(*args, **kwargs)

        def __unicode__(self):
                return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        output = self.name
        return output


class Note(models.Model):
    letter = models.CharField(max_length=2)
    # sharp = models.BooleanField(default=False)
    #

    def __str__(self):
        output = self.letter
        return output


# class Chord(models.Model):
#     note = models.ForeignKey(Note)
#     type = models.ForeignKey(Type)
#
#     def __str__(self):
#         output = str(self.note) + " " + self.type.name
#         return output
#
#
# # class String(models.Model):
#     note = models.ForeignKey(Note)
#     number = models.IntegerField()
#
#     def __str__(self):
#         output = str(self.number) + str(self.note)
#         return output
#
#
# class Fret(models.Model):
#     number = models.IntegerField()
#
#     def __str__(self):
#         output = str( self.number )
#         return output
#
#
# class Position(models.Model):
#     fret = models.ForeignKey(Fret)
#     string = models.ForeignKey(String)
#     chord = models.ForeignKey(Chord)
#     note = models.ForeignKey(Note)
#
#     def __str__(self):
#         output = str(self.fret.number) + str(self.string) + str(self.note) + str(self.chord)
#         return output


class Favorites(models.Model):
    user = models.ForeignKey(User)
    note = models.CharField(max_length=2)
    ch_type = models.CharField(max_length=255)


    def get_chord(self):
        c = Chord()
        return c.get_strings(self.note, self.ch_type)



