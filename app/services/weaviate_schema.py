from app.core.weaviate_client import client

def create_schema():

    schema = {
        "class": "DocumentChunk",
        "vectorizer": "none",
        "properties": [
            {"name": "text", "dataType": ["text"]},
            {"name": "source_id", "dataType": ["text"]},
            {"name": "domain", "dataType": ["text"]}
        ]
    }

    existing_schema = client.schema.get()

    classes = [c["class"] for c in existing_schema.get("classes", [])]

    if "DocumentChunk" not in classes:
        client.schema.create_class(schema)
        print("Weaviate schema created")
    else:
        print("Weaviate schema already exists")