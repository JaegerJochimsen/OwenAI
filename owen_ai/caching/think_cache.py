from semantic_text_similarity.models import WebBertSimilarity
from typing import Union

class ThinkCache:
    def __init__(self, similarity_threshold=3.0):
        self.web_model = WebBertSimilarity(device='cpu', batch_size=10)
        self.similarity_threshold = similarity_threshold
        self.cache = dict()

    # unfortunately still slow... could speed up with GPU
    def _compare_text(self, text1: str, text2: str) -> float:
        predictions = self.web_model.predict([(text1, text2)])
        return predictions[0]

    # basic cache, needs to be updated and currently the compare text is not that fast
    # we will use a delaunay triangulation struct to only compare nearest neighbor vectors going forward
    def get(self, query: str) -> Union[str,None]:
        for key in self.cache.keys():
            if self._compare_text(query, key) > self.similarity_threshold:
                return self.cache[key]
        return None

    # fixme should be updated to use the embedding instead of the string
    def put(self, query: str, value: str) -> None:
        self.cache[query] = value
        return


if __name__ == '__main__':
    cache = ThinkCache()
    click.secho(f"{cache._compare_text('Totally unrelated values', 'Tell me about photosynthesis')}", fg='yellow', bg="black")