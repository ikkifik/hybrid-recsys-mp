from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

import pandas as pd
import numpy as np
import json

class RecommenderSystem:
    def __init__(self, data, content_col='description'):
        self.engine = create_engine("mysql+pymysql://kopi:kopi@localhost/mp_recomsys")
        self.dbCon = self.engine.connect()
        self.df = pd.read_sql(data, self.dbCon)
        
        self.content_col = content_col
        self.encoder = None
        self.bank = None
                
    def fit(self):
        sw_indo = stopwords.words("indonesian")
        text = self.df[self.content_col]
        text = [''.join(c for c in s if c not in punctuation) for s in text]
        self.encoder = TfidfVectorizer(ngram_range=(1, 3), tokenizer=word_tokenize, stop_words=sw_indo)
        self.bank = self.encoder.fit_transform(text)
    
    def recommend_cb(self, idx, top=3):
        df = self.df.copy()
        df = df.loc[df['keywords'] == df['keywords'][idx]]
        desc = df.loc[idx, self.content_col]
        desc = self.encoder.transform([desc])
        
        sim = cosine_similarity(desc, self.bank)
        rec_idx = sim.argsort()[0, -(top+1):-1]
        rec_idx = rec_idx[::-1]

        try:
            reverse_idx = sim[0, rec_idx]
            
            score = []
            for p in reverse_idx:
                percentage = "{:.0%}".format(p)
                score.append(percentage)
            df = df.loc[rec_idx]
            df['score'] = score
            
            df = df.reset_index().set_index('index', drop=False)

            result = df.loc[rec_idx, ["index", "id_product", "url", "image", "name", "price", "score"]]
            result = result.to_json(orient="records")
            result = json.loads(result)

            return result
        except:
            result = {}
        
        return result
        
    def recommend_demo(self, keyword=None, prices=None, topk=20):
        df = self.df.copy()
        df = self.demographic_filter(df, keyword=keyword, prices=prices)
        df = self.compute_mp_score(df)
        
        df = df.reset_index().set_index('index', drop=False)
        result = df.loc[:, "index":"score"]
        result = result.drop_duplicates(subset=['name'])
        result = result.sort_values(by=["score"], ascending=False)
        result = result.head(topk)
        result = result.to_json(orient="records")
        result = json.loads(result)
        
        return result
    
    @staticmethod
    def demographic_filter(df, keyword=None, prices=None):
        df = df.copy()
        
        if keyword is not None:
            df = df[(df.keywords == keyword)]
        if prices is not None:
            df = df[df.price.gt(prices)]
            
        return df
    
    @staticmethod
    def compute_mp_score(df, q=0.85):
        df = df.copy()

        m = df.review.quantile(q)
        C = (df.rate * df.review).sum() / df.review.sum()

        df = df[df.review >= m]
        df["score"] = df.apply(lambda x: (x.rate * x.review + C*m) / (x.review + m), axis=1)
        
        return df