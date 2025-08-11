from pinecone import Pinecone, ServerlessSpec

debug = False

def get_env_parameter(key: str) -> str:
    with open("./.env", "r") as env:
        for raw_line in env:
            parts = raw_line.strip().split("=", 1)
            if len(parts) == 2 and parts[0] == key:
                return parts[1]
    raise ValueError(f"key \"{key}\" not found in .env")

def embed(text):
    return [0]

class Query:
    def __init__(self) -> None:
        self.text = ""
        self.count = 10 
        self.clamped = False

    def __str__(self) -> str:
        return f"Query:\ntext: {self.text}\ncount: {self.count}"

    def prepare(self) -> dict:
        if not self._valid():
            raise ValueError("Query found to be invaild at execute")
        return {"vector": self._generate_query_embedding(), "top_k": self.count} 

    def set_body(self, text: str) -> "Query":
        self.text = text
        return self

    def set_count(self, count: int) -> "Query":
        if count > 100:
            self.count = 100
            self.clamped = True
        elif count < 1:
            self.count = 1 
            self.clamped = True
        else:
            self.count = count
        return self

    def _valid(self) -> bool:
        if self.text == "":
            print("Query invaild because of no text body")
            return False
        if self.count > 100 or self.count < 1:
            print("Query must request between 1-100 results")
            return False
        if self.clamped and debug:
            print("clamped count query is being exacuted")

        return True

    def _generate_query_embedding(self) -> list:
        return embed(self.text)


class Database_Handler:
    def __init__(self):
        self.pinecone = Pinecone(api_key=get_env_parameter("pinecone_api"))
        self.index = get_env_parameter("index_name")
        self.index_target = self.pinecone.Index(self.index)

        self._test_connection()

    def _test_connection(self) -> None:
        try:
            self.index_target.describe_index_stats()
        except Exception as e:
            print(f"Error connecting to Pinecone index '{self.index}': {e}")

    def search(self, query: Query):
        prepared = query.prepare()
        return self.index_target.query(**prepared)

