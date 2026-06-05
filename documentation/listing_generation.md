### 1. Goal:
A system (agent) that recieves as input information about a product
and can generate listings like a title, a convenient description, etc. 

### 2. Inputs 
    - Product name
    - Product category
    - Main benifit
    - Target country
    - Buyer persona
    - Forbidden claims

### 3. Ouputs
    - Shopee title 
    - 10 keywords 
    - Product description 
    - TikTok 3-second hook 
    - Short video script 
    - Compliance-safe claims 

### 4. Approach 
Build an AI angent powered by llms to generate listings.

1. Approach 1: Single LLM

| input | system | ouput |
| --- | --- | --- |
|Product information| LLM | listing generation |

2. Approach 2: LLM + RAG

| input | system | ouput |
| --- | --- | --- |
|Product information + 50 product listings on shopee | RAG (retrieve best listings) + LLM | listing generation |

3. Approach 3: Compititor analysis + LLM + RAG

| input | system | ouput |
| --- | --- | --- |
|Product information + 10 best compititor listings | RAG + LLM | listing generation |

### 5. Methodology 

1.  
The chosen LLM should be :
- open source (or very low cost) 
- Midium size (less then 30 Billion params)
- Can be used via an API (for the first iteration)

2. Example of llm plateforms and APIs:
- [OpenRouter](https://openrouter.ai/) gives access to many models through a single API.

|Common choices | Advantages | Disadvantages |
| --- | --- | --- |
|Llama 3.3 70B, Qwen 3, DeepSeek V3, Mistral Large | One API, Easy model switching, Very low cost | Not unlimited |


- Host models locally (to garantee unlimited generation ):

| Popular models | Serving frameworks | Advantages | Disadvantages |
| --- | --- | --- | --- |
| Qwen 3 32B, Qwen 3 14B, Llama 3.3 70B, Mistral Small| vLLM, Ollama, Text Generation Inference (TGI) |Unlimited requests, Full control, No per-token costs| Need GPU infrastructure, Operational complexity |

- DeepSeek API

DeepSeek Platform

For listing generation specifically, many developers currently use:

DeepSeek V3

Why?

Strong writing quality
Very cheap
Large context window

For product descriptions and SEO-style content, it is often sufficient.

- Qwen API

The Qwen family is becoming a strong choice for:

E-commerce
Structured outputs
Multilingual content

Especially if you later expand beyond Korea.

3. Open source LLMs: 
- "qwen/qwen3-next-80b-a3b-instruct:free"
- "openai/gpt-oss-120b:free"
- "meta-llama/llama-3.3-70b-instruct:free"
- "google/gemma-4-31b-it:free"