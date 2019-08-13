import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from recipes import Recipe
from ingredients import Ingredient
from common.database import Database
import re


Database.initialize(database='beer',
                    user='postgres',
                    password='tensleep9!23',
                    host='postgres')

# new_recipe = Recipe("test title2", "test type2", "test image url2", "test beer url2", 3, 2, 2, 2, 2, "test directions2", None)
#
# new_recipe.save_to_db()


beerRecipes = []
recipeURLs = []
baseURL = 'https://www.homebrewersassociation.org/homebrew-recipes/page/'


def scrapeSite(link):
    for x in range(60, 85):
        newURL = f'{link}{x}/'
        scrapePageRecipes(newURL)
    for item in recipeURLs:
        checkAvail(item)

def scrapePageRecipes(page):
    html = urllib.request.urlopen(page).read()
    soup = BeautifulSoup(html, 'html.parser')
    recipeBlock = soup.find('div', {'id': 'recipe-list'})
    tags = recipeBlock.find_all('a')
    for tag in tags:
        htag = tag.get('href', None)
        if htag not in recipeURLs and 'page' not in htag and 'recipes' not in htag:
            recipeURLs.append(htag)

# make sure recipe is available to non-members
def checkAvail(recURL):
    # print(recURL)
    html = urllib.request.urlopen(recURL).read()
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('h2').text == 'Members Only':
        print('members only')
    else:
        getRecipe(recURL)

def getRecipe(rec):
    html = urllib.request.urlopen(rec).read()
    soup = BeautifulSoup(html, 'html.parser')
    recipe = soup.find('div', class_='info-box')
    entry = soup.find('div', class_='entry')
    recipeContents = recipe.contents

    # gets beer title and type
    titleBlock = recipe.find('h3')
    titleInfo = titleBlock.contents
    title = titleInfo[0].split(' |')[0]
    type = titleInfo[1].text

    # gets the beer image url
    img = entry.find('img', class_='wp-post-image')['src']

    # this gets the batch yield size
    batch = recipe.find('strong')
    yld = batch.text.replace('For ', '')
    yld = re.sub('[\ (].*?[\)]', ' gal', yld)

    # parses the ingredients
    ingredientsBlock = recipe.find('div', {'itemprop':'ingredients'})
    for i in ingredientsBlock('strong'):
        i.decompose()
    ingredients = ingredientsBlock.find_all('li')
    ingredientList = []
    for ingredient in ingredients:
        i = ingredient.text.replace(u'\xa0', ' ').replace(u'a.a., ', '').replace(u'a.a. ', '')
        if i != '':
            ingredientList.append(i)

    # parses the specifications section
    specsBlock = recipe.find('ul', class_='specs')
    finalSpecs = {'original_gravity': 0, 'final_gravity': 0, 'abv': 0, 'ibu': 0}
    specs = {}
    for i in specsBlock('li'):
        i.strong.unwrap()
        iStr = i.text
        spec, value = i.text.split(": ")
        value = value.replace('%', '')
        value = re.sub('[\(].*?[\)]', '', value)
        value = re.sub('\~', '', value)
        re.sub(r'\s*/.*?', '', value)
        value = value.replace(' *', '')
        try:
            value = float(value)
        except ValueError:
            value = 0
        specs["_".join(spec.lower().split())] = value
    specs = {k: specs.get(k, 0) for (k, v) in finalSpecs.items()}


    # gets the brew directions
    directionsBlock = recipe.find('div', {'itemprop':'recipeInstructions'})
    directions = directionsBlock.find_all('p')
    finalDirections = ''
    for direction in directions:
        finalDirections = finalDirections + direction.text + ' '

    #print to check
    new_beer = [title, type, img, rec, yld]
    for item in specs.values():
        new_beer.append(item)
    new_beer.append(finalDirections)
    new_beer.append(None)
    print(new_beer)
    #create new_beer object and save to db
    new_recipe = Recipe(*new_beer)
    new_recipe.save_to_db()


    #insert ingredients
    for item in ingredientList:
        new_ingredient = Ingredient(28, item, None)
        new_ingredient.save_to_db(title)


scrapeSite(baseURL)