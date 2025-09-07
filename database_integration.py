from pinecone import Pinecone, ServerlessSpec

debug = False

#placeholder
def embed(string):
    return [0]

def get_env_parameter(key: str) -> str:
    with open("./.env", "r") as env:
        for raw_line in env:
            parts = raw_line.strip().split("=", 1)
            if len(parts) == 2 and parts[0] == key:
                return parts[1]
    raise ValueError(f"key \"{key}\" not found in .env")

class Query:
    def __init__(self) -> None:
        self.text = ""
        self.count = 10 
        self.clamped = False
        self.max_reqs_length = 100 

    def __str__(self) -> str:
        return f"Query:\ntext: {self.text}\ncount: {self.count}"

    def prepare(self) -> dict:
        if not self._valid():
            raise ValueError("Query found to be invalid at execute")
        return {"vector": self._generate_query_embedding(), "top_k": self.count} 

    def set_body(self, text: str) -> "Query":
        self.text = text
        return self

    def _match_key_to_set_method(self, key: str, value: any) -> None:
        match key:
            case "top_k":
                self.set_count(value)
            case "query":
                self.set_body(value)
            case _:
                raise ValueError(f"unkown key {key} passed to _match_key_to_set_method")
    
    def from_dict(self, data: dict) -> "Query":
        for key in data.keys():
            self._match_key_to_set_method(key, data[key])
        return self

    def set_count(self, count: int) -> "Query":
        if count > self.max_reqs_length:
            self.count = self.max_reqs_length
            self.clamped = True
        elif count < 1:
            self.count = 1 
            self.clamped = True
        else:
            self.count = count
        return self

    def _valid(self) -> bool:
        if self.text.strip() == "":
            print("Query invaild because of no text body at _valid")
            return False
        if self.count > self.max_reqs_length or self.count < 1:
            print("Query must request between 1-100 results at _valid")
            return False
        if self.clamped and debug:
            print("clamped count query is being executed at _valid")

        return True

    def _generate_query_embedding(self) -> list:
        return embed(self.text)


class Database_handler:
    def __init__(self) -> None:
        self.pinecone = None
        self.index = None
        self.index_target = None
        self.connected = False
        self.reattempt_connection = 3
        self.vector_size = 512
    
    def __str__(self):
        return f"pc: {self.pinecone}\nindex: {self.index}"

    def _connect_to_db(self) -> bool:
        self.pinecone = Pinecone(api_key=get_env_parameter("pinecone_api"))
        self.index = get_env_parameter("index_name")
        self._set_index_target(self.index)

        self.connected = self._test_connection()
        return self.connected
    
    def _set_index_target(self, target: str) -> None:
        if not self.pinecone.has_index(target):
            #TODO replace {} with something
            self.genrate_index({}, target)
        self.index_target = self.pinecone.Index(self.index)


    def _test_connection(self) -> bool:
        try:
            self.index_target.describe_index_stats()
            return True
        except Exception as e:
            print(f"Error connecting to Pinecone index '{self.index}': {e}")
            return False

    def connect_db(self) -> None:
        if self.connected:
            return

        for _ in range(self.reattempt_connection):
            if self._connect_to_db():
                break
        else:
            self.pinecone = None
            self.index = None
            self.index_target = None
            raise ValueError("Failed to open a connection to db")

    def search(self, query: Query) -> dict:
        if not self.connected:
            self.connect_db()

        prepared = query.prepare()
        return self.index_target.query(**prepared)

    def upload_vector_set(self, key: dict, records: list) -> bool:
        if not self.connected:
            self.connect_db()

        id_key = key.get("id", "id")
        vec_key = key.get("values") or key.get("vector") or key.get("embedding")
        meta_key = key.get("metadata", "metadata")
        ns_spec = key.get("namespace", None)

        by_ns: dict[str | None, list[dict]] = {}
        for rec in records:
            ns = None
            if ns_spec is not None:
                ns = rec[ns_spec] if isinstance(ns_spec, str) and ns_spec in rec else ns_spec

            payload = {
                "id": str(rec[id_key]),
                "values": rec[vec_key],
                "metadata": rec[meta_key],
            }
            by_ns.setdefault(ns, []).append(payload)

        for ns, vecs in by_ns.items():
            self.index_target.upsert(vectors=vecs, namespace=ns)

        return True


    def genrate_index(self, key: dict, name: str) -> None:
        if self.pinecone.has_index(name):
            raise ValueError(f"Index {name} already exists")
        self.pinecone.create_index(
            name = name,
            vector_type = "dense",
            dimension=self.vector_size,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=get_env_parameter("cloud"),
                region=get_env_parameter("region")
            ),
                
            #temporary 
            deletion_protection="disabled",
            tags={
                "environment": "development"
            }
        )
