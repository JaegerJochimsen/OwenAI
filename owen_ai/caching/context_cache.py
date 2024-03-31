from .context_obj import ContextObj
from typing import List


class ContextCache:
    def __init__(self):
        self.local_stack = []
        self.cache_map = set()

    # store context string with timestamp
    def put(self, context: str) -> None:
        if context not in self.cache_map:
            context_obj = ContextObj(context)
            self.local_stack.append(context_obj)

    '''
    Return the first n context objects to be used for context
    TODO make filterable based on context token limit 
    '''
    def get_contexts(self, n: int, token_limit: int) -> List[ContextObj]:
        matching_contexts = None
        if n >= len(self.local_stack):
            matching_contexts = self.local_stack
        else:
            matching_contexts = self.local_stack[:n]

        return matching_contexts
