import imdb
from pprint import pprint

moviesDB = imdb.IMDb()

# # Help?
# print(dir(moviesDB))
# ----------------------------------------
# 1) Search for a title
# MOVIE_TITLE = 'Lord of the Rings'
MOVIE_TITLE = 'APPLE_DUMPLING_GANG'

movies = set(moviesDB.search_movie(title=MOVIE_TITLE))

# movie = moviesDB.get_movie("0133093")
# pprint(movie.data['runtimes'])

print('movies len: ', len(movies))
for movie in movies:
	m_id = movie.getID()
	movie_2 = moviesDB.get_movie(m_id)
	print(movie)
	print()
	try:
		pprint(f"Title: {movie['title']} - Aspect ratio: {movie_2.data['aspect ratio']}")
	except:
		continue
	# break







# ----------------------------------------
# 2) List movie info
# id = movies[0].getID()
# movie = moviesDB.get_movie(id)
#
# title = movie['title']
# year = movie['year']
# rating = movie['rating']
# directors = movie['directors']
# casting = movie['cast']

# print('Movie info:')
# print(f'{title} - {year}')
# print(f'rating: {rating}')

# direcStr = ' '.join(map(str,directors))
# print(f'directors: {direcStr}')

# actors = ', '.join(map(str, casting))
# print(f'actors: {actors}')

## Help?
#print(movie.keys())
# ----------------------------------------
# 3) List actor info
# id = casting[0].getID()
# person = moviesDB.get_person(id)
# bio = moviesDB.get_person_biography(id)
#
# name = person['name']
# birthDate = person['birth date']
# height = person['height']
# trivia = person['trivia']
# titleRefs = bio['titlesRefs']

# print(f'name: {name}')
# print(f'birth date: {birthDate}')
# print(f'height: {height}')
# print(f'trivia: {trivia[0]}')

# titleRefsStr = ', '.join(map(str, titleRefs))
# print(f'bio title refs: {titleRefsStr}')

## Help?
#print(dir(casting[0]))
#print(person.keys())

## Help?
#print(bio.keys())
#print(bio['titlesRefs'].keys())

