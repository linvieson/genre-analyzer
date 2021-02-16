'''
This module analyzes different genres of books and their ecranizations.
User's input is either genre, or EXIT. If it the former, start analyzing
the genre and provide user ith relevant information. If it is the latter, the
program ends its work.
'''
import sys
from random import sample
from time import sleep
import pandas as pd
from termcolor import colored
from read_data import form_database

SLEEP_TIME = 0.03
COUNTER = 1
DF = form_database()

def timeprint(line: str):
    '''
    Print string with certain interval in time.
    >>> timeprint('Hello world!')
    Hello world!
    '''
    for char in line:
        print(char, end='', flush = True)
        sleep(SLEEP_TIME)
    print()


def print_text():
    '''
    Print welcoming string.
    '''
    print('______________________________________________________________')
    timeprint(colored('\nE. M. Forster is a british novelist, essayist, and\
 social and\nliterary critic. His fame rests largely on his novels\nHowards\
 End (1910) and A Passage to India (1924) and on a large\nbody of\
 criticism.\n', attrs = ['bold']))
    print('______________________________________________________________')
    sleep(0.5)
    timeprint('\nThis program will help you to analyze different genres, in\
 which\nE. M. Forster wrote. It will also provide you with a list\
 of\nreccommended ecranizations of his books to watch, and a list\
 of\nreccommended books with no ecranization yet to read.\n')


def generate_genres() -> list:
    '''
    Generate list of available genres.
    >>> generate_genres()[-1:]
    ['EXIT']
    '''
    genres = list({str(elem) for elem in list(iter(DF['genres'].dropna()))})
    genres.extend(list(iter(str(elem)\
                  for elem in list(iter(DF['bookgenre'].dropna())))))
    index = 0
    genres_lst = []

    while index < len(genres):
        if '\\' in genres[index] or 'nan' in genres[index]:
            genres.pop(index)
        elif ',' in genres[index]:
            some_genres = genres[index].split(',')
            genres_lst.extend(some_genres)
            index += 1
        elif ';' in genres[index]:
            some_genres = genres[index].split(';')
            genres_lst.extend(some_genres)
            index += 1
        else:
            genres_lst.append(genres[index])
            index += 1

    for elem in genres_lst:
        if elem.startswith(' '):
            elem = elem[1:]
        if elem.endswith(' '):
            elem = elem[:-1]

    genres = list(set(genres_lst)) + ['EXIT']
    return genres


def choose_genre() -> str:
    '''
    Allow user to choose a genre. If he types the genre that is not in the
    list of available genres, get the input again, until the right genre is not
    gotten.
    >>> choose_genre()
    Choose a genre you want to analyze:
    '''
    genres1 = ', '.join(generate_genres()[:6])
    genres2 = ', '.join(generate_genres()[6:12])
    genres3 = ', '.join(generate_genres()[12:18])
    genres4 = ', '.join(generate_genres()[18:24])
    genres5 = ', '.join(generate_genres()[24:30])
    genres6 = ', '.join(generate_genres()[30:36])
    genres7 = ', '.join(generate_genres()[36:-2])
    sleep(0.5)
    print('______________________________________________________________')
    timeprint(colored('\nAvailable genres:', attrs = ['bold']))
    sleep(1)
    print(f'{genres1},\n{genres2},\n{genres3},\n{genres4},\n{genres5}\
\n{genres6}\n{genres7}')
    print('______________________________________________________________')
    print('Choose a genre you want to analyze:')
    genre = input()

    while genre not in generate_genres():
        print("There are no ecranizations this genre of this author's\
 books. Please, try again: ")
        genre = input()
    return genre


def calculate_average_rating(genre: str) -> float:
    '''
    Calculate average rating of films of certain genre. Return averag number.
    >>> calculate_average_rating('War')
    7.24
    >>> calculate_average_rating('Drama')
    7.51
    '''
    DF['all_genres'] = DF['genres'].fillna('') + DF['bookgenre'].fillna('')
    df = DF.dropna(subset = ['all_genres'])
    df = df.loc[df['all_genres'].str.contains(genre)]
    return round(df['rating'].mean(), 2)


def calculate_relative_rating(genre: str) -> float:
    '''
    Calculate rating of films of certain genre in relation to rating of films
    of other genres.
    >>> calculate_relative_rating('Action')
    0
    >>> calculate_relative_rating('Romance')
    5.29
    '''
    relatives = []
    genres = generate_genres()

    for elem in genres:
        if elem != genre:
            relative = calculate_average_rating(elem)
            if str(relative) != 'nan':
                relatives.append(relative)
    average_of_relatives = sum(relatives) // len(relatives)
    relative_rating = ((calculate_average_rating(genre) * 100) / average_of_relatives) - 100
    relative_rating = 0 if relative_rating < 0 else relative_rating
    return round(relative_rating, 2)


def reccommend_films(genre: str) -> pd.DataFrame:
    '''
    Create a list of films of particular genre, sorted by the highest rating.
    >>> reccommend_films('Comedy')
                 film  rating
1  A Room with a View     8.6
2      What I Believe     8.0
3               Egypt     7.8
4        Howard's End     7.6
    >>> reccommend_films('Romance')
                 film  rating
1             Maurice     7.7
2         Howards End     7.4
3  A Room with a View     7.3
4      Correspondence     6.1
    >>> reccommend_films('Fiction')
    Empty DataFrame
Columns: [film, rating]
Index: []
    '''
    df = DF.dropna(subset = ['genres'])
    df = df.loc[df['genres'].str.contains(genre)]
    df = df.sort_values(['rating'], ascending = False)
    df = df.drop_duplicates(subset = 'film')
    try:
        indexes = pd.Series([ind for ind in range(1,\
                    len(list(iter(df['film'])))+1)], dtype=pd.StringDtype())
    except TypeError:
        return []
    df = df.set_index(indexes)
    return df[['film', 'rating']]


def reccommend_books(genre: str) -> pd.DataFrame:
    '''
    Create a list of books (with no ecranizations yet) of particular genre.
    >>> reccommend_books('Diary)
    ['The journals and diaries of E.M. Forster']
    >>> reccommend_books('Action')
    []
    '''
    df = DF.loc[DF['film'].isnull()]
    df = df.dropna(subset = ['bookgenre'])
    df = df.loc[df['bookgenre'].str.contains(genre)]
    df = df.drop_duplicates(subset = 'book')
    books = list(iter(df['book']))

    for index, elem in enumerate(books):
        if '(' in elem or '[' in elem:
            books.pop(index)
        if elem.startswith('E. M. Forster'):
            books.pop(index)
        if 'Edited' in elem or 'edit' in elem:
            books.pop(index)
    try:
        return sample(books, 5)
    except ValueError:
        return books


def print_end():
    '''
    Print text at the end of the program.
    '''
    timeprint(colored('\nThank you for using this program! Hope you did find\
 it useful. See you next time!\n', attrs = ['bold']))


if __name__ == '__main__':
    print_text()
    genre = choose_genre()
    while True:
        if genre == 'EXIT':
            print_end()
            sys.exit()
        else:  
            average = calculate_average_rating(genre)
            relative = calculate_relative_rating(genre)
            films_list = reccommend_films(genre)
            books_list = reccommend_books(genre)

        timeprint(colored(f'\n                        {genre}\
                        ', attrs = ['bold']))


        if len(films_list) == 0:
            print(f"\nThere are no films of {genre} genre, that are\
 ecranizations of E. M. Forster's books. You can choose another genre.")
            genre = choose_genre()
        else:
            print(f'\nThe average rating of films of {genre} genre is\
 {average}.\n')
            sleep(0.5)
            print(f'The {genre} genre films are {relative}% more\
 successful than films of other genres.\n')

            sleep(1.5)
            print(f'Here is the list of {genre} genre films, formed\
 specially for you.\n')
            print(f'{films_list}')

            sleep(1.5)
            if len(books_list) == 0:
                print(f'\nThere are no books of {genre} genre, that were\
 not ecranized. You may read ecranized books instead:')
                books = list(iter(films_list["film"]))
                for ind in range(len(films_list)):
                    print(f'{books[ind]}')
            else:
                print(f'\nHere is the list of {genre} genre books, formed\
 specially for you.\n')
                for book in books_list:
                    timeprint(book)

            sleep(3)
            print('_______________________________________________________\
_______')
            print('If you want to analyze more genres, type the next\
 genre, if you want to finish the program, type EXIT.')
            sleep(1)
            genre = choose_genre()
