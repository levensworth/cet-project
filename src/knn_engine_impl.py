import pathlib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

import pydantic
from thefuzz import fuzz, process

class RecommendationRequestDTO(pydantic.BaseModel):
    preference_records: list['PreferenceRecord']

class PreferenceRecord(pydantic.BaseModel):
    id: int
    is_positive: bool


class RecommendationResponseDTO(pydantic.BaseModel):
    records: list['Record']

class Record(pydantic.BaseModel):
    name: str
    band: str
    id: int
    
    
RecommendationRequestDTO.update_forward_refs()
RecommendationResponseDTO.update_forward_refs()


class KNNEngineImpl:
    
    ATTRIBUTES = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'key', 'loudness', 'speechiness']

    def __init__(self, path: pathlib.Path) -> None:
        self.__model = KNeighborsClassifier
        self.__db = pd.read_csv(path)
        self.__db = self.__db[self.__db['year'] >= 2000]

        df = self.__db[self.ATTRIBUTES]
        self.df_normalized = (df - df.mean()) / df.std()

    def predict(self, request: RecommendationRequestDTO) -> RecommendationResponseDTO:
        corpus_idxs = []
        
        for idx in request.preference_records:
            corpus_idxs += self.get_similar(idx.id, amount=100)

        corpus = self.df_normalized.iloc[corpus_idxs]
        # set the target label
        corpus['target'] = [0 for _ in range(len(corpus))]

        for record in request.preference_records:
            corpus.loc[record.id] = 1

        model = self.__model(n_neighbors=3)
        
        train_data = self.df_normalized.loc[(r.id for r in request.preference_records)]
        train_y = [int(r.is_positive) for r in request.preference_records]

        model.fit(train_data[self.ATTRIBUTES], train_y)
        # corpus.drop(labels=(r.id for r in request.preference_records), inplace=True)
        result = model.predict(corpus[self.ATTRIBUTES])
        
        result_info = self.__db.loc[corpus.iloc[np.where(result > 0)].index]
        
        return RecommendationResponseDTO(
            records=[Record(name=row['track_name'], band=row['artist_name'], id=idx) for idx, row in result_info[['artist_name', 'track_name']].iterrows()]
        )
        
    def search_for_song(self, query: str) -> list[Record]:
        result = []
        for row in process.extractBests(query, self.__db['artist_name'], limit=5):
            
            result.append(Record(
                name=self.__db.loc[row[-1]]['track_name'],
                band=self.__db.loc[row[-1]]['artist_name'],
                id=self.__db.loc[row[-1]]['idx']
            ))
        return result
    

    def get_song_by_id(self, id: int) -> Record | None:
        row = self.__db.loc[id]
        if len(row) == 0:
            return
        
        return Record( name=row['track_name'],
                band=row['artist_name'],
                id=row['idx'])
        
    def get_similar(self, idx: int, amount: int = 100) -> list[int]:
        result = cosine_similarity(self.df_normalized,self.df_normalized.loc[idx].to_numpy().reshape((1, -1)))
        return result.argsort(axis=0)[::-1][1:amount+1].reshape((1, amount)).tolist()[0]


            



if __name__ == '__main__':
    model = KNNEngineImpl(path=pathlib.Path('data/spotify_data.csv'))
    result = model.predict(RecommendationRequestDTO(preference_records=[
        PreferenceRecord(id=10, is_positive=True),
        PreferenceRecord(id=50, is_positive=True),
        PreferenceRecord(id=20, is_positive=True),
        PreferenceRecord(id=70, is_positive=False),
        PreferenceRecord(id=80, is_positive=False),
        PreferenceRecord(id=90, is_positive=False),
        PreferenceRecord(id=100, is_positive=False),
        PreferenceRecord(id=130, is_positive=False),
    ]))

    result = model.search_for_song('you')
    print(result)
