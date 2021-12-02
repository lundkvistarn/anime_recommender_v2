from sklearn.naive_bayes import MultinomialNB
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
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


train = anime_df['sypnopsis']


target = anime_df['Name']
indices = pd.Series(anime_df.index, index=anime_df['Name'])
cv = CountVectorizer()
X_train_counts = cv.fit_transform(train.values.astype('U'))

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
model = MultinomialNB().fit(X_train_tfidf, indices)


def content_synopsis(title):
    docs_new = [title]
    X_new_counts = cv.transform(docs_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    probs = model.predict_proba(X_new_tfidf)
    best_n = np.argsort(probs, axis=1)[:, -31:]
    probsSorted = sorted(probs[0])

    anime_indices = [i for i in best_n[0]]

    anime_lst = anime_df.iloc[anime_indices][['Name', 'Members', 'Score']]
    anime_lst['best_n'] = probsSorted[-31:]
    anime_lst['n'] = anime_indices
    favorite_count = anime_lst[anime_lst['Members'].notnull()]['Members'].astype(
        'int')
    score_avg = anime_lst[anime_lst['Score'].notnull()
                          ]['Score'].astype('float')
    n_avg = anime_lst[anime_lst['best_n'].notnull()]['best_n'].astype('float')
    C = score_avg.mean()
    N = n_avg.mean()
    m = favorite_count.quantile(0.60)
    qualified = anime_lst[(anime_lst['Members'] >= m) & (
        anime_lst['Members'].notnull()) & (anime_lst['Score'].notnull())]
    qualified['Members'] = qualified['Members'].astype('int')
    qualified['Score'] = qualified['Score'].astype('float')

    def weighted_rating(x):
        v = x['Members']
        R = x['Score']
        a = x['best_n']
        return (v/(v+m) * R) + (m/(m+v) * C) + ((a/N)-1)

    qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(10)

    return qualified.to_json(orient='split')
