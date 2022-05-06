from python_graphql_client import GraphqlClient
import config

headers = {"Authorization": f"Bearer {config.GITHUB_API_TOKEN}"}
client = GraphqlClient(endpoint=config.GITHUB_API_URL, headers=headers)


def make_query(owner, name, after_cursor=None):
    return """
        query {
        repository (owner: OWNER, name: NAME) {
            pullRequests(first: 100, after: AFTER){
                nodes {
                author{
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
    ).replace(
        "OWNER", '"{}"'.format(owner)
    ).replace(
        "NAME", '"{}"'.format(name)
    )


has_next_page = True
after_cursor = None
while has_next_page:
    data = client.execute(
        query=make_query("vuejs", "vue", after_cursor),
    )

    print(data)
    has_next_page = data["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]
    after_cursor = data["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
    print(has_next_page)
    print(after_cursor)
