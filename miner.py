from python_graphql_client import GraphqlClient


class PullRequestsIterator:
    def __init__(self, api_url: str, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        self.client = GraphqlClient(endpoint=api_url, headers=headers)

    @staticmethod
    def __query__(owner: str, name: str, after_cursor=None):
        return (
            """
            query {
                repository(owner: OWNER, name: NAME) {
                    pullRequests(first: 100, after: AFTER) {
                        nodes {
                            author {
                                login
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                }
            }
        """.replace(
                "AFTER", '"{}"'.format(after_cursor) if after_cursor else "null"
            )
            .replace("OWNER", '"{}"'.format(owner))
            .replace("NAME", '"{}"'.format(name))
        )

    def get_iterator(self, repo_owner: str, repo_name: str):
        has_next_page = True
        after_cursor = None
        while has_next_page:
            data = self.client.execute(
                query=self.__query__(repo_owner, repo_name, after_cursor),
            )
            has_next_page = data["data"]["repository"]["pullRequests"]["pageInfo"][
                "hasNextPage"
            ]
            after_cursor = data["data"]["repository"]["pullRequests"]["pageInfo"][
                "endCursor"
            ]

            yield data
