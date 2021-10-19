from datetime import datetime
from turtle import ondrag
from django.contrib.auth.models import User
from django_bookmark_base.models import BookmarkModel
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from cloudinary.models import CloudinaryField




class Recipe(models.Model):
    """
    A users-uploaded recipes. Recipes can be created by registered users and are the core feature of the application.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
 
    summary = models.CharField(max_length=1000)
    
    image = CloudinaryField('image')
    prep_time = models.CharField(max_length=200)
    cook_time = models.CharField(max_length=200)
    servings = models.IntegerField()
    calories = models.IntegerField()
    favorites=models.ManyToManyField(
        User,related_name='favorite',default=None,blank=True
    )
    country=models.CharField(max_length=30,default='Kenya')
    is_featured = models.BooleanField(default=False)
    ratings = GenericRelation(Rating, related_query_name='foos')
    free=models.BooleanField(default=True)
    # recipe_price=models.DecimalField(max_digits=10,decimal_places=2)
    @classmethod
    def filter_by_rating(cls):
        return cls.objects.filter(ratings__isnull=False).order_by('ratings__average').reverse()
    @classmethod
    def filter_by_country(cls):
        return cls.objects.order_by('country').reverse()
    

    @classmethod
    def filter_by_recent(cls):
        return cls.objects.order_by('created_at').reverse()

    @classmethod
    def search(cls,q):
        return cls.objects.filter(
            Q(name__icontains=q) | Q(summary__icontains=q)
        )
    

    def avg_rating(self):
        """
        Returns the average rating of this recipe based on all reviews submitted by users.

        :return: average rating
        """
       
        return self.ratings__average
    def __str__(self):
        return '%s by %s' % (self.name, self.user.username)


class Ingredient(models.Model):
    """
    An ingredient in a users-submitted recipes. Each ingredient has a name entry, quantity, and index in the order of
    appearance in the recipes.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    ingredient = models.ForeignKey('IngredientName', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    index = models.IntegerField()
    def __str__(self):
        return '%s by %s' % (self.recipe)


class Direction(models.Model):
    """
    A single direction for a recipes. Directions tell the users "how" to make the recipes. Each direction has a
    description text and index in the order of appearance.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)
    index = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


    def __str__(self):
        return '%s by %s' % (self.recipe)


class IngredientName(models.Model):
    """
    An ingredient name value. Normalized so that an ingredient's name is not simply a string but rather a row in the
    database. This is useful for browsing purpose.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name



from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name





class Review(models.Model):
    """
    A users-submitted review on a recipes. Every users can submit one review on each recipes that is not their own. Each
    review has a description and number rating between one and five.
    """
    user= models.ForeignKey(User,default=1, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    comment=models.TextField(max_length=300)
    title=models.CharField(max_length=100)

   

    def __str__(self):
        return 'Review for recipes #%d' % (self.recipe.id)



class UserProfile(models.Model):
    """
    User profile data that is displayed on the associated user's profile page.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = CloudinaryField('image')
    bio = models.CharField(max_length=1000, default=None, blank=True, null=True)

    @staticmethod
    def get_or_create(user):
        return UserProfile.objects.get_or_create(user=user, defaults={'created_at': timezone.now()})

    def __str__(self):
        return 'User profile for %s' % self.user.username

