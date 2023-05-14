# Hybrid Advanced_Sementic_Search


## WorkFlow

![Workflow](https://github.com/Manish06097/Advanced_Sementic_Search/assets/73208573/96ed55b7-78d3-4e33-86f5-98d93c6a2fee | width=100)

1. Introduction

In our project, we introduce a novel approach to question-answering systems by integrating the hybrid search methodology, which makes use of both dense and sparse vectors. This approach allows us to encompass a wide array of search features including semantic understanding through dense vectors and exact matching plus keyword searching via sparse vectors.

2. The Hybrid Search Approach

The hybrid search approach is a powerful technique that combines the strengths of both dense and sparse vectors. While the dense vectors capture the semantic meaning of queries, the sparse vectors excel in providing precise matching based on exact terms and keywords. This dual capability ensures an overall robust and comprehensive search result.

3. Role of SPLADE

For the implementation of sparse vectors, we employ SPLADE - a state-of-the-art sparse embedding method that outperforms traditional techniques like BM25 across diverse tasks. SPLADE not only enhances the benefits of sparse search but also introduces the feature of learning term expansion, effectively addressing the vocabulary mismatch problem often faced in question-answering systems.

4. Integration of Sentence Transformers

In order to handle the dense vectors, we have used a sentence transformer model trained on the MS-MARCO dataset. Sentence transformers are adept at understanding the semantic context, thus making them an integral part of our hybrid search approach.

5. Implementation via Hugging Face Transformers

All these components – SPLADE, sentence transformer model, and the hybrid search approach – are implemented through Hugging Face Transformers, a widely-used library for state-of-the-art Natural Language Processing tasks.

6. Conclusion

By combining sentence transformers and SPLADE in a hybrid search approach, our project presents a comprehensive question-answering system that is capable of handling both semantic understanding and precise term matching. This makes it an effective tool for any use-case that requires an advanced search capability, promising high-quality results that balance both precision and context understanding.
