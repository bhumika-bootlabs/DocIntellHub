# from ragas import evaluate
# from ragas.metrics.collections import faithfulness, answer_relevancy, context_precision
# from datasets import Dataset
# from ragas.llms import LangchainLLMWrapper
# import os
# from ragas.embeddings import LangchainEmbeddingsWrapper
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_groq import ChatGroq

# llm = LangchainLLMWrapper(
#     ChatGroq(
#         groq_api_key=os.getenv("GROQ_API_KEY"),
#         model_name="llama3-8b-8192",   # or mixtral
#         temperature=0
#     )
# )

# embeddings = LangchainEmbeddingsWrapper(
#     HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# )
# print("DEBUG: contexts exists?", "contexts" in locals())
# def evaluate_response(query: str, answer: str, contexts: list):
#     print("\n--- RAG EVALUATION DEBUG ---")
#     print("Question:", query)
#     print("Answer:", answer)
#     print("DEBUG contexts:", contexts)
#     print("DEBUG wrapped contexts:", [contexts])
#     print("Length:", len(contexts))
#     print("Contexts:", contexts[:2])
#     try:
#         data = {
#             "question": [query],
#             "answer": [answer],
#             "contexts": [contexts]
#         }

#         dataset = Dataset.from_dict(data)

#         result = evaluate(
#             dataset,
#             metrics=[faithfulness, answer_relevancy, context_precision],
#             llm=llm,
#             embeddings=embeddings
#         )

#         print("Evaluation Result:", result)
#         print("FINAL SCORES:", result)

#         return {
#             "faithfulness": float(result["faithfulness"]),
#             "answer_relevancy": float(result["answer_relevancy"]),
#             "context_precision": float(result["context_precision"])
#         }

#     except Exception as e:
#         # Prevent breaking main pipeline
#         return {
#             "error": str(e)
#         }