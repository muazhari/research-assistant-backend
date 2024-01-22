class QueryProcessorUtility:

    def __init__(self):
        pass

    def prefixer(self, query: str, prefix: str) -> str:
        prefixed_query: str = prefix + query

        return prefixed_query

    def deprefixer(self, query: str, prefix: str) -> str:
        deprefixed_query: str = query[len(prefix):]

        return deprefixed_query

    def process(self, query: str, prefix: str) -> str:
        prefixed_query: str = self.prefixer(query, prefix)

        return prefixed_query
