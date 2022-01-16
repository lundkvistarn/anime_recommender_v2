
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Läser in datan
PROJECT_DIR = r'D:/Maskininlärning/anime_recommender_v2/flask-server/DB'
anime_info_df = pd.read_csv(PROJECT_DIR + '/anime.csv', low_memory=True)
anime_desc_df = pd.read_csv(
    PROJECT_DIR + '/anime_with_synopsis.csv', low_memory=True)
rating_df = pd.read_csv(PROJECT_DIR + '/rating_complete.csv', low_memory=True)

# mergar dem olika datasetsen och displayar första 10
anime_df = pd.merge(anime_desc_df, anime_info_df[[
                    'MAL_ID', 'Type', 'Popularity', 'Members', 'Favorites']], on='MAL_ID')

# Tar bort alla som har unknown score
anime_df = anime_df[(anime_df["Score"] != "Unknown")]

# Om det inte finns någon beskrivning så lääger vi till ''
anime_df['sypnopsis'] = anime_df['sypnopsis'].fillna('')

# Transformerar till count-vectorized form
# fit_transform ger transformern med datan och skapar en TF-IDF matris
# Vi har en TF-IDF matris med 11091 rader och 386042  kolumner
tfidf = TfidfVectorizer(analyzer='word', ngram_range=(
    1, 2), min_df=0, stop_words='english')
tfidf_matrix = tfidf.fit_transform(anime_df['sypnopsis'])

# Räknar ut Linear_kernel mellan matriser
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# skapar en series med alla namnen
anime_df = anime_df.reset_index()
titles = anime_df['Name']
indices = pd.Series(anime_df.index, index=anime_df['Name'])


def content_recommendations(title):
    idx = indices[title]  # Tar ut just den animen beroende på namnet
    # skapar en lista med cosine_sim med serien vi skickade in
    sim_scores = list(enumerate(cosine_sim[idx]))
    # sorterar alla cosine_sim scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]  # Tar den första 31 värdena i listen
    # skapar en array med siffror från 0 till 31
    anime_indices = [i[0] for i in sim_scores]

    # skapar en variabel som bara har namn members och score
    anime_lst = anime_df.iloc[anime_indices][['Name', 'Members', 'Score']]
    favorite_count = anime_lst[anime_lst['Members'].notnull()]['Members'].astype(
        'int')  # Tar ut antalet favorites den har
    score_avg = anime_lst[anime_lst['Score'].notnull()]['Score'].astype(
        'float')  # Tar ut alla scores
    C = score_avg.mean()  # räknar ut medelvärdet på scoresen
    m = favorite_count.quantile(0.60)  # tar ut top 40% av favorites
    qualified = anime_lst[(anime_lst['Members'] >= m) & (anime_lst['Members'].notnull()) & (
        anime_lst['Score'].notnull())]  # kollar så att det inte finns null svar
    qualified['Members'] = qualified['Members'].astype(
        'int')  # gör om så att alla members är int
    qualified['Score'] = qualified['Score'].astype(
        'float')  # gör om så att alla scores är floats

    def weighted_rating(x):
        v = x['Members']  # tar ut members för x
        R = x['Score']  # tar ut score för x
        return (v/(v+m) * R) + (m/(m+v) * C)

    qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(10)

    return qualified.to_json(orient='table')
