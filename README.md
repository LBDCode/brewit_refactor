# brewIt
BrewIt allows homebrewing enthusiants to search through a database of beer recipes by name, style, ABV and IBU.  Developers can use the public brewIt API to power their own apps!

![brewit](https://libby.tech/images/portfolio/beerRecipes.png)


### Link to Website

www.brewit.tech

### Technologies Used
Python, Flask, PostgreSQL, SQLAlchemy, Beautiful Soup, Flask-Login, Flask-CORS


Hosted on AWS EC2.

## API Documentation

#### Using the brewIt API
Developers can access brewIt's database of homebrew recipes by sending a GET request to a query url that is
comprised of the base brewIt API URL, query parameters, and a unique API key.  On success, the API will
return a 200 OK code with the results in JSON format.  If the request fails, the API will return an
error code.

#### Acquiring and using an API key
To obtain an API key, sign up for a brewIt developer account - you will receive an email with your unique
key.  Your key can also be found by logging in to brewIt and navigating to the  Account page.  Your API key
 must be appended to the query search parameters as '&key={your key}'.

#### Constructing a query URL
The query URL is comprised of the base brewIt API URL, query parameters, and a unique API key.  Each query
must include either an 's' (search) or 'r' (random) parameter, and may include any or all of the additional
six optional parameters.

<div><strong>base url:</strong> https://www.brewit.tech/api/search?</div>


#### Parameters
Query parameters must include either the 's' (search) or 'r' (random) parameter.  The 's' parameter takes a string
and searches for recipes with titles or beer types that contain that string.  The 'r' parameter takes an
integer which acts as a limit - it returns random results up to the submitted query limit (or 50,
whichever is lower).

There are six optional parameters (outlined below) that can be combined with the 's' parameter.

| Parameter   | Required    | Type          | Description           |
| :---        |    :----:   |        :----: | :---                  |
| key         | yes         | string        | Your brewIt API key (ex: 'key=233as-234-dc-2341-3').           |
| s           | yes*        | string        | Search query text (ex: 's=brown+ale').  Every call must have either s or r parameters - if both are included, the query will default to the search parameter, and ignore the random command.             |
| r           | yes*        | string        | Random response generator based on number of desired recipes (ex: 'r=24') up to an upper limit of 50 results.  Every call must have either s or r parameters - if both are included, the query will default to the search parameter, and ignore the random command.             |
| type        | no          | string        | Filter results by style of beer (ex: 'type=ipa').             |
| low-ibu     | no          | float         | Filter results by low IBU as a >= operator, and can be used in combination with the high-ibu parameter to define a range (ex: 'low-ibu=30' will return recipes with IBU >= 30, and 'low-ibu=30&high-ibu=60' will return recipes with IBU >=30 and <=60').             |
| high-ibu    | no          | float         | Filter results by high IBU as a <= operator, and can be used in combination with the high-ibu parameter to define a range (ex: 'high-ibu=60' will return recipes with IBU <= 60, and 'low-ibu=30&high-ibu=60' will return recipes with IBU >=30 and <=60').           |
| low-abv     | no          | float         | Filter results by low ABV as a >= operator, and can be used in combination with high-abv to define a range (ex: 'low-abv=4' will return recipes with ABV >= 4, while 'low-abv=4&high-abv=8' will return recipes with IBU >=4 and <=8').            |
| high-abv    | no          | float         | Filter results by high ABV as a <= operator, and can be used in combination with low-abv to define a range (ex: 'high-abv=8' will return recipes with ABV <= 8 while 'low-abv=4&high-abv=8' will return recipes with IBU >=4 and <=8').            |
| limit       | no          | integer       | Limit allows you to restrict the number of results (ex: 'limit=30').  If no limit is defined, the default limit of 50 will be used.  Use limit in combination with offset to paginate searches.            |
| offset      | no          | integer       | Use with the default limit (50 results) or a user defined limit to paginate results (ex: 'offset=20' will return results 21-70 of the search, while 'limit=30&offset=10' will return results 11-40 of the search).            |

#### Examples

<strong>Simple Random Query:</strong>

This example uses just the 'r' parameter to return 15 random recipes.

<strong>Target URL: </strong> http://www.brewit.tech/api/search?r=15&key=8141e1d7-0253-4t6a-9853-71ua8acce027

~~~    
function randomBeer() {
    // construct the query URL
    const baseURL = "http://www.brewit.tech/api/search?"
    const search = "r=15";
    const key = "&key=8141e1d7-0253-4t6a-9853-71ua8acce027";
    const queryURL = baseURL + search + key;
    // send a GET request
    $.ajax({
      url: queryURL,
      method: "GET"
    }).then(function(response) {
      // Printing the entire object to console
      console.log(response);
    });
}
~~~



<strong>Simple Search Query:</strong>

This example will return recipes with 'brown ale' in the title or style,  up to the default limit of 50 results.


<strong>Target URL: </strong> http://www.brewit.tech/api/search?s=brown+ale&key=8141e1d7-0253-4t6a-9853-71ua8acce027

~~~                    
function simpleSearch() {
    // construct the query URL
    const baseURL = "http://www.brewit.tech/api/search?"
    const search = "s=brown+ale";
    const key = "&key=8141e1d7-0253-4t6a-9853-71ua8acce027";
    const queryURL = baseURL + search + key;
    // send a GET request
    $.ajax({
      url: queryURL,
      method: "GET"
    }).then(function(response) {
      // Printing the entire object to console
      console.log(response);
    });
}
~~~

<strong>More complex query with optional parameters:</strong></h6>
              

This example will search for recipes with a minimum abv of 4 and 'brown ale in
the title or type columns.  It will return up to 10 results, offset by 5 (results 5-14).


<strong>Target URL: </strong> http://www.brewit.tech/api/search?s=brown+ale&abv-low=4&limit=10&offset=5&key=8141e1d7-0253-4t6a-9853-71ua8acce027
~~~
function paramsSearch() {
        // construct the query URL
        const baseURL = "http://www.brewit.tech/api/search?"
        const search = "s=brown+ale";
        const params = "&abv-low=4";
        const limit = "&limit=10";
        const offset = "&offset=5";
        const key = "&key=8141e1d7-0253-4t6a-9853-71ua8acce027";
        const queryURL = baseURL + search + params + limit + offset + key;
        // send a GET request
        $.ajax({
          url: queryURL,
          method: "GET"
        }).then(function(response) {
          // Printing the entire object to console
          console.log(response);
        });
    }
~~~