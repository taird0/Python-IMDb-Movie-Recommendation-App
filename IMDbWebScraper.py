import requests
from bs4 import BeautifulSoup
import heapq
import re

class Movie:
    def __init__(self, title, year, runtime, rating, description):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.rating = rating
        self.desc = description

    #Create a function for what to compare with "<" 
    def __lt__(self, other):
         return self.rating > other.rating

class MaxHeap:
    def __init__(self):
         self.heap = []

    def push(self, movie):
         #Turns the rating into a negative float (use minheap to get max values)
         heapq.heappush(self.heap, (-float(movie.rating), movie))
        
    def pop(self):
        return heapq.heappop(self.heap)[1]
    
    def peek(self):
        return self.heap[0][1] if self.heap else None

    def __len__(self):
         return len(self.heap)         


def get_movies(genre = 'comedy'):
    #Creates our url for searching movies of user-defined genre
    url =f"https://www.imdb.com/search/title/?genres={genre}&groups=top_1000"

    #Creates a header to not get 403 forbidden
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    movie_data = soup.find_all('div', attrs={'class': 'ipc-metadata-list-summary-item__tc'})

    movieHeap = MaxHeap()

    for m in movie_data:

            # year, runtime and age are stored in div tags with the same class - this gets the data we need from them
            year_runtime_age = m.find_all('span', class_='sc-b189961a-8 kLaxqf dli-title-metadata-item')
            yra = [yra.text for yra in year_runtime_age]
            #This cuts the number of people out of the rating
            rating = m.find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating').text[:3]
            #Creates the movie object #re.sub replaces the number/dot at the beginning of the movie title
            movie = Movie(re.sub(r'^\d+\.\s+', '', m.h3.text), yra[0], yra[1], rating, m.find('div', class_='ipc-html-content-inner-div').text)
            
            #print(f"{movie.title} : {movie.year} : {movie.rating} : {movie.runtime}\n {movie.desc}")

            movieHeap.push(movie) 
    return movieHeap 

def get_genre():
    usr_in = input("Enter the genre of movie you want to watch!\n").lower()
    matches = [genre for genre in genres if usr_in in genre ]

    if matches:
        print(matches)

        for match in matches:
            usr_in = input(f'Do you want to look at {match} movies? y/n\n').lower()

            if usr_in == 'y':
                return match
    else:
        print("No mathes found.\n")
    
    return get_genre()
         
genres = ['action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama', 'family', 'fantasy', 'film-noir', 
          'game-show', 'history', 'horror', 'music', 'musical', 'mystery', 'news', 'romance', 'sci-fi', 'short', 'sport', 'thriller', 'war', 'western']

with open('MovieGetterArt') as art:
    print("".join(line for line in art)) 

print("Welcome to my Movie Recommendation App - This app gets the most popular movies by genre and sorts them by rating")

genre = get_genre()

while True:
    result_heap = get_movies(genre)

    if result_heap.__len__() > 0:
        while True:
            best_movie = result_heap.pop()

            print("We recommend: ")
            print(f'{best_movie.title}')
            print(f'Released: {best_movie.year} | Runtime: {best_movie.runtime} | Rating: {str(best_movie.rating)}')
            print(f'{best_movie.desc}\n')

            usr_cont = input("Would you like to see another movie? y/n\n").lower()

            if usr_cont == 'n':
                break
    else:
        print("We couldn't find a movie in that genre - please enter a new one and try again")
        genre = get_genre()
        continue
    
    usr_cont = input("Would you like to search for another Movie? y/n\n")

    if usr_cont == 'n':
        break

    genre = get_genre()
    
print("Thanks for using my movie recommendation app - Hope you found something cool to watch!")
