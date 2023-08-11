class GraphQLClientError(Exception):
    def __init__(self, errors):
        self.errors = errors.get('errors') or errors
        super().__init__(self.errors)

    def __str__(self):
        return f'{self.errors}'
