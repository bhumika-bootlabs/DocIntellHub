import weaviate

client = weaviate.connect_to_local(skip_init_checks=True)
print("Connected to Weaviate:", client.is_ready())