import os

FILMS_FOLDER = r'C:\Users\Steve\Downloads\[Vidz]\[Films]'

OUTPUT_HTML = r'C:\Users\Steve\Downloads\[Vidz]\index.html'


def generate_html():

    html_template = '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Movies</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 50px;
            }}
            .film-container {{
                display: flex;
                flex-wrap: wrap;
                max-width: 1200px;
                margin: auto;
            }}
            .film-title {{
                font-size: 18px;
            }}
            .film-genre {{
                font-size: 14px;
            }}
            .film {{
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 4px 7px rgba(0, 0, 0, 0.3);
                margin: 10px;
                margin-top: 10px;
                max-width: 200px;
                padding: 10px;
                text-align: center;
            }}
            .film img {{
                max-width: 100%;
                border-radius: 2px;
            }}
        </style>
    </head>
    <body>
        <h1>Movies</h1>
        <div class="film-container">
            {film_items}
        </div>
    </body>
    </html>
    '''

    film_template = '''
    <div class="film">
        <img src="{poster}" alt="{title}">
        <span class="film-title">{title}</span><br>
        <span class="film-genre">{genre}</span>
    </div>
    '''

    film_items = ''

    for genre_folder in os.listdir(FILMS_FOLDER):
        genre_path = os.path.join(FILMS_FOLDER, genre_folder)
        if os.path.isdir(genre_path):
            for movie_folder in os.listdir(genre_path):
                movie_path = os.path.join(genre_path, movie_folder)
                if os.path.isdir(movie_path):
                    title = movie_folder
                    poster = ''
                    synopsis = ''

                    for file in os.listdir(movie_path):
                        if file.endswith('.jpg'):
                            poster = os.path.join(FILMS_FOLDER,
                                                  genre_folder,
                                                  movie_folder,
                                                  file)
                        if file.endswith('.txt'):
                            with open(os.path.join(movie_path, file), 'r',
                                      encoding='utf-8') as f:
                                synopsis = f.read()
                    film_items += film_template.format(title=title,
                                                       poster=poster,
                                                       synopsis=synopsis,
                                                       genre=genre_folder)

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_template.format(film_items=film_items))

    print(f"Successfully created : {OUTPUT_HTML}")
