from re import A
from django.shortcuts import get_object_or_404, render
from django.template import context
from recipeapp.forms.recipe import ReviewForm

from recipeapp.models.models import Recipe, Review


def home(request):
    try:
        query = request.GET.get('q')
       
        recipes=Recipe.search(query)
        print(query)
        context={
            'recipe':recipes
        }
    except:
        recipe=Recipe.objects.all().order_by('created_at').reverse()

        context={
            'recipe':recipe
        }
 
    
    return render(request,'home/home.html',context)
def filter_recipes(request,what):
    recent=Recipe.filter_by_recent()
    ratings=Recipe.filter_by_rating()
    country=Recipe.filter_by_country()
    all=Recipe.objects.all().order_by('created_at').reverse()
    if what=='recent':
         context={
            'recipe':recent
        }
    elif what=='ratings':
        context={
            'recipe':ratings
        }
    elif what=='country':
        context={
            'recipe':country
        }
    else:
        context={
            'recipe':all
        }
    return render(request ,'home/home.html',context)


 
       
   
    
    return render(request,'home/home.html',context)


def viewpage(request,recipe_id):
    """
    Displays a detailed view of the recipes as specified in the URL.
    """
    user = request.user
    form=ReviewForm()
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.ingredient_set.order_by('-index')
    directions = recipe.direction_set.order_by('-index')
    comments=Review.objects.filter(recipe=recipe_id)
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'directions': directions,
        'form':form,
        'comments':comments
        
    }
    return render(request,'core/rec_details.html',context)

