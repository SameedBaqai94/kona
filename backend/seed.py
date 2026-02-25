import requests
from fastembed import TextEmbedding
from models.anime_records import AnimeRecord
from db_config import init_db, SessionLocal

def main():

    print("Loading AI Model...")
    model = TextEmbedding("BAAI/bge-small-en-v1.5")

    print("Initializing Database...")
    init_db()
    session = SessionLocal()

    graphql_query = """
   query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: POPULARITY_DESC) {
      id
      title {
        english
        romaji
      }
      description(asHtml: false)
      genres
      tags {
        name
        rank
      }
    }
  }
}
    """
    
    # 2. Define your variables
    query_variables = {
        "page": 1,
        "perPage": 50
    }
    response = requests.post(
        "https://graphql.anilist.co",
        json={"query": graphql_query, "variables": query_variables}
    )

    print(f"Response:{response.json()['data']['Page']['media']}")
    anime_list = response.json()['data']['Page']['media']

    for anime in anime_list:
        anime_id = anime['id']
       # Fallback to romaji if there is no official English title
        title = anime['title']['english'] or anime['title']['romaji'] 
        description = anime['description'] or "No description available."
        genres = ", ".join(anime['genres']) if anime['genres'] else "No genres"
        
        # Format the text
        top_tags = [t['name'] for t in anime.get('tags', []) if t['rank'] >= 60]
        tags_str = ", ".join(top_tags) if top_tags else "No tags"
        text_to_vectorize = f"Title: {title}. Genres: {genres}. Tags: {tags_str}. Synopsis: {description}"

        # Generate the vector
        embedding = list(model.embed([text_to_vectorize]))[0]
        
       # Create the database record
        new_anime = AnimeRecord(
            id=anime_id,
            title=title,
            description=description,
            genres=genres,
            embedding=embedding
        )
        session.merge(new_anime) # merge() inserts, or updates if the ID already exists
        session.commit()
        
        print(f"Saved to database: {title}")
    session.close()


main()
