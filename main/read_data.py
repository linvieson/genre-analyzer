'''
This module reads data from csv and tsv files and forms a database, which can
be used in the main.py module.
'''
import pandas as pd
from data_cache import pandas_cache

@pandas_cache
def read_titles_and_genres() -> pd.DataFrame:
    '''
    Read the csv file (titles.csv) and format it inro a DataFrame.
    >>> read_titles_and_genres()['Title'].head(1)
    0    'Billy Budd.' Oper ... Libretto von E. M. Fors...
    Name: Title, dtype: object
    '''
    df = pd.read_csv('titles.csv', skiprows=0)
    return df


@pandas_cache
def read_film_names() -> pd.DataFrame:
    '''
    Read the tsv file (title.basics.tsv) and format it inro a DataFrame.
    >>> read_film_names()['originalTitle'].head(1)
    0    Carmencita
    Name: originalTitle, dtype: object
    '''
    df = pd.read_csv('title.basics.tsv', skiprows=0, sep = '\t')
    return df


@pandas_cache
def read_film_ratings() -> pd.DataFrame:
    '''
    Read the tsv file (title.ratings.tsv) and format it inro a DataFrame.
    >>> read_film_ratings()['averageRating'].head(1)
    0    5.6
    Name: averageRating, dtype: float64
    '''
    df = pd.read_csv('title.ratings.tsv', skiprows=0, sep = '\t')
    return df


@pandas_cache
def take_title_genre() -> pd.DataFrame:
    '''
    Take out lines that contain books written only by E. M. Forster. Take out
    columns with titles from the titles.csv file.
    >>> take_title_genre()['Title'].head(1)
    0    'Billy Budd.' Oper ... Libretto von E. M. Fors...
    Name: Title, dtype: object
    '''
    df = read_titles_and_genres()
    df = df.dropna(subset = ['All names'])
    df = df.loc[df['All names'].str.contains('Forster')]
    return df[['Title', 'Other titles', 'Genre']]


@pandas_cache
def take_film_names() -> pd.DataFrame:
    '''
    Take out columns with tconst, titles and genres from title.basics.tsv file.
    >>> take_film_names()['originalTitle'].head(1)
    0    Carmencita
    Name: originalTitle, dtype: object
    '''
    df_films = read_film_names()
    return df_films[['tconst', 'primaryTitle', 'originalTitle', 'genres']]


@pandas_cache
def extract_films_by_author() -> pd.DataFrame:
    '''
    Take out films based on books of E. M. Forster, from title.basics.tsv file.
    >>> extract_films_by_author()['originalTitle'].head(1)
    51665    Billy Budd
    Name: originalTitle, dtype: object
    '''
    df_titles = take_title_genre()
    df_films = take_film_names()
    condition = df_films['primaryTitle'].isin(df_titles['Title'])\
              | df_films['primaryTitle'].isin(df_titles['Other titles'])\
              | df_films['originalTitle'].isin(df_titles['Title'])\
              | df_films['originalTitle'].isin(df_titles['Other titles'])
    df_films = df_films[condition]
    return df_films


@pandas_cache
def take_film_rating() -> pd.DataFrame:
    '''
    Take out columns with tconst and rating from title.ratings.tsv file.
    >>> take_film_rating()['averageRating'].head(1)
    0    5.6
    Name: averageRating, dtype: float64
    '''
    df = read_film_ratings()
    return df[['tconst', 'averageRating']]


@pandas_cache
def extract_ratings() -> pd.DataFrame:
    '''
    Take out ratings of films based on books of E. M. Forster, from
    title.basics.tsv file.
    >>> extract_ratings()['averageRating'].head(1)
    34573    7.8
    Name: averageRating, dtype: float64
    '''
    df_films = extract_films_by_author()
    df_ratings = take_film_rating()
    condition = df_ratings['tconst'].isin(df_films['tconst'])
    df_ratings = df_ratings[condition]
    return df_ratings

@pandas_cache
def form_database() -> pd.DataFrame:
    '''
    Form an overall dataframe, which contains book name, film name (if the
    ecranization exists, else NaN value), film genre (if the film exists, else
    NaN value) and average rating of the film (if th efilm exists, else NaN
    value).
    >>> form_database()['book'].head(1)
    0    'Billy Budd.' Oper ... Libretto von E. M. Fors...
    Name: book, dtype: object
    '''
    df_books = take_title_genre().drop(['Other titles'], axis = 1)
    df_films = extract_films_by_author().drop(['originalTitle'], axis = 1)
    df_ratings = extract_ratings()
    df = df_films.merge(df_ratings)
    df = df.drop(['tconst'], axis = 1)
    df = df_books.merge(df, how = 'left', left_on = 'Title', right_on = 'primaryTitle')
    df = df.rename(columns = {'Title': 'book', 'Genre': 'bookgenre',\
                  'primaryTitle': 'film', 'averageRating': 'rating'})
    return df


def write_to_file(df):
    '''
    Transform DataFrame to a csv file. Write it to the filtered_data.csv file.
    Use this function to see the data better and analyze it correctly.
    '''
    df = form_database()
    with open('filtered_data.csv', 'w', encoding = 'utf-8') as my_file:
        df_csv = df.to_csv(encoding = 'utf-8')
        my_file.write(df_csv)
