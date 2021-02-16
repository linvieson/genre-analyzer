# GENRE ANALYZER

## Description
This program analyzes different genres of books and their ecranizations. It works with data 
about Edward Morgan Forster's works. The main purpose is to encourage people to read more 
by providing statistics that the user is interested in.

The program analazyses the art genre input by user and gives the following information, 
using databases of books and films:
1) The average ratign of films of this genre.
2) Success of the films of this genre (in percentage) in comparison to ecranizations of 
other geners of the author.
3) List of recommended ecranizations of books of this genre, sorted by rating from the 
most successful to the least successful.
4) List of recommended books of this genre, that have not been ecranized yet.


## Modules
[read_data.py](https://github.com/linvieson/genre-analyzer/blob/main/main/read_data.py) - 
module that contains functions that read data from csv and tsv database files; creates a new 
database (to impove the performance of the program), which is used in the main module.

[termcolor.py](https://github.com/linvieson/genre-analyzer/blob/main/main/termcolor.py) - 
external module, that is used to print formatted and colored text.

[main.py](https://github.com/linvieson/genre-analyzer/blob/main/main/main.py) - main module, 
in which the program is realized. Gets input from user, checks if the input is correct, 
analyzes data, performs calculations and outputs the requeted infromation.


## Imported modules
1) sys - to be able to end the program manually.
2) random (sample function) - to generate a list of books, randomly gotten from the database.
3) time (sleep function) - to create a delay between the outputs of the program. To write the 
timeprint() function, that outputs the text gradually, with delay in 0.03 seconds.
4) pandas - to read data from csv and tsv files.
5) termcolor (colored function) - to make some text bold.


## Databases
1) British Library Catalogue Dataset ([titles.csv](https://www.bl.uk/bibliographic/downloads/EMForsterResearcherFormat_202001_csv.zip) file). Data with all works of E. M. Forster 
is used.
2) IMDb Datasets ([title.basics.tsv](https://datasets.imdbws.com/title.basics.tsv.gz) 
and [title.ratings.tsv](https://datasets.imdbws.com/title.ratings.tsv.gz) files). 
Data with names of films, their code (in tconst), genre and average rating is used.
3) Own created dataset (filtered_data.csv). Contains sorted data from databases 1) and 2). 
Created for better visualisation and more accurate data analysis. Conists of data about 
book names, film names (if such exist), book genres, film genres, average filmratings. 

All data is in free access and can be downloaded by links.

filtered_data_csv is created by calling the function write_to_file(df) 
in [read_data.py](https://github.com/linvieson/genre-analyzer/blob/main/main/read_data.py) module.


## Usage
```python
import main.py
```
These lines start the work of the program. The information, which describes the work of the
program is output on the screen:

![Screenshot](/images/usage1.png?raw=true "usage")

After that, the program ouputs a list of available genres, which the user can choose to 
analyze. The user is asked to input a genre:

![Screenshot](/images/usage2.png?raw=true "usage")

If the user inputs a genre, that is not in a list or just a incorrect string, the program 
outputs a message to try one more time. The user can input a genre again:

![Screenshot](/images/usage3.png?raw=true "usage")

If the next input of the user is incorrect again, that message appears again and the user is 
asked to input a genre again. This continues till the valid string is gotten.

When the genre is input (for example, "Bibloigraphy"), the program outputs the following:

![Screenshot](/images/usage4.png?raw=true "usage")

Other options of output (when user enteres "Comedy" and "Fiction" accordingly:

![Screenshot](/images/usage5.png?raw=true "usage")

![Screenshot](/images/usage6.png?raw=true "usage")

The film list is formed by rating from the highest in descending order. If there are no 
films of the input genre in the database, the program outputs according message on the 
screen and asks to enter another genre.

The book list contains 5 random books of this genre. If there are no books of the input 
genre in the database, the user is welcomed to read the books that were already ecranized.

The following message asks the user to enter a genre again:

![Screenshot](/images/usage7.png?raw=true "usage")

The user can analyze as much genres as he wants. To end the work of the program, the user needs 
to print "EXIT". The program outputs the following:

![Screenshot](/images/usage8.png?raw=true "usage")

The program ends its work.


## Results
The result of a project is a program that analyzes and outputs information about certain 
art genre, in which worked E. M. Forster.

The result of a program is a set of data, that consists of average film rating of certain 
genre, percentage success of this genre in omparison to other genres, list of recommended 
films and books.

Gotten results demonstrate, that E. M. Forster had better success in writing books of certain 
genres. It can be noticed, which film genres have higher rating, thus coming to the conclusion 
that future ecranizations of certain genres will be more successful that the ones of the other 
genres.


## License
[MIT](https://github.com/linvieson/genre-analyzer/blob/main/LICENSE.txt)
