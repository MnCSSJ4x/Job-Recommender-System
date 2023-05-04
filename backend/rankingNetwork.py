from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd
import itertools
import torch.nn.functional as F
import numpy as np
import pickle
import math

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"
tokenizer = AutoTokenizer.from_pretrained(
    "MohammedDhiyaEddine/job-skill-sentence-transformer-tsdae"
)
model = AutoModel.from_pretrained(
    "MohammedDhiyaEddine/job-skill-sentence-transformer-tsdae"
).to(torch.device(device))
print("Server device detected! Running on ", device)

# with open("jobEmbeddingArya.pickle", "rb") as f:
#     # Use pickle to load the variable from the file
#     job_embeddings = torch.load(f, map_location=torch.device("cpu"))
job_embeddings = torch.load("jobEmbeddingArya.pickle", map_location=torch.device("cpu"))
print("Loading of job descriptions done!")
df = pd.read_csv("cleaned_jobs.csv")
df = df.rename(columns={"Unnamed: 0": "Index"}).set_index("Index")
df.head()


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[
        0
    ]  # First element of model_output contains all token embeddings
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )


def getUserEmbedding(userResume):
    embeddings = torch.Tensor([]).to(device)
    sentences = userResume
    encoded_sentences = tokenizer(
        sentences, padding=True, truncation=True, return_tensors="pt"
    )
    encoded_sentences.to(device)
    with torch.no_grad():
        temp = model(**encoded_sentences)
    sentence_embeddings = mean_pooling(temp, encoded_sentences["attention_mask"])
    embeddings = sentence_embeddings
    print("User Embedding obtained!!!")
    return embeddings


def getCosineMatrix(userResume):
    user_embedding = getUserEmbedding(userResume)
    #     print(user_embedding.shape)
    #     print(job_embeddings.shape)
    # Create two example tensors
    tensor1 = user_embedding
    tensor2 = job_embeddings

    # Generate all permutations of the two tensors
    permutations = itertools.product(tensor1, tensor2)

    # Convert tuples to rows in a DataFrame
    Embedding_df = pd.DataFrame(permutations, columns=["tensor1", "tensor2"])

    # Display the resulting DataFrame
    #     print(Embedding_df.shape)
    Embedding_df["Index"] = range(tensor2.shape[0])
    Embedding_df.set_index("Index")
    Embedding_df["cosine_similarity"] = np.zeros((Embedding_df.shape[0]))
    #     print(Embedding_df.shape)

    for i in range(math.ceil(Embedding_df.shape[0])):
        tensor1 = Embedding_df.iloc[i]["tensor1"]
        tensor2 = Embedding_df.iloc[i]["tensor2"]
        # compute the cosine similarity between the two tensors
        cosine_similarity_value = F.cosine_similarity(
            tensor1.unsqueeze(0), tensor2.unsqueeze(0)
        ).item()
        Embedding_df["cosine_similarity"].iloc[i] = cosine_similarity_value
    Embedding_df = Embedding_df.sort_values(by="cosine_similarity", ascending=False)

    merged_df = pd.merge(Embedding_df, df, on="Index").set_index("Index")
    #     merged_df
    print("Returning Ranks")
    return Embedding_df, merged_df


if __name__ == "__main__":
    CosineMatrix, merged_df = getCosineMatrix("I am familiar with python")
    CosineMatrix.head()
