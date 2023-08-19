import pickle
import os
import logging
import faiss
import dotenv
from langchain import LLMChain, OpenAI, PromptTemplate, ConversationChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()




question_prompt_template = """Вопрос: {question}

Ответь на данный вопрос профессионально, обсуждая все важные моменты, ссылаясь на свои знания и ниже приведенные законы. Если не хватает информации для развернутого ответа, можешь запросить всю нужную тебе информацию.

Законы:
{context}

"""

conversation_template = """Следующий текст - деловой разговор между человеком и ИИ. ИИ-собеседник очень разговорчив и предоставляет множество конкретных деталей из своего контекста. Если ИИ не знает ответа на вопрос, он искренне сообщает о своем незнании.

Текущий разговор:

Человек: Tы модель классификатор которая классифицирует юридические вопросы. Отвечать на них НЕ НУЖНО. Например:

Вопрос - У меня полицейский нашел наркотики в кармане. 5 грамм марихуаны. Что мне грозит?
Ответ - [Незаконное хранение наркотических средств]

Теперь попробуй ты.

Человек: Вопрос - Я украл компьютер из электронного магазина. Что мне грозит?
ИИ: [Кража и незаконное обращение с чужим имуществом]
Человек: Вопрос - Я не явился в военкомат по повестке. Что мне грозит?
ИИ: [Уклонение от воинской службы]
Человек: Вопрос - Я подрался с мужчиной в баре. Не понятно кто начал. У меня нету претензий к нему а у него нету претензей ко мне. Что мне грозит?
ИИ: [Мелкое хулиганство, причинение вреда здоровью, побои]
Человек: Вопрос - Я препарковался на частной территории, не на парковке, и мне пришел штраф. Я виноват?
ИИ: [ПДД]
Человек: Вопрос - {input}
ИИ: """
CONVERSATION_PROMPT = PromptTemplate(
    input_variables=["input"], template=conversation_template
)

EXAMPLE_PROMPT = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)
QUESTION_PROMPT = PromptTemplate(
    template=question_prompt_template, input_variables=["context", "question"]
)




def get_topic(question: str) -> str:
    chain = LLMChain(llm=OpenAI(), prompt=CONVERSATION_PROMPT)
    response = chain({'input': question})
    return response['text']


if __name__ == "__main__":
    pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENVIRONMENT'))

    vectorstore = Pinecone.from_existing_index(index_name='laws-test', embedding=OpenAIEmbeddings(embedding_ctx_length=7000))
    retriever = VectorStoreRetriever(vectorstore=vectorstore, search_kwargs={"k": 5})
    qa = RetrievalQA.from_llm(llm=ChatOpenAI(model_name='gpt-4'), retriever=retriever, return_source_documents = True, prompt=QUESTION_PROMPT)

    query = 'У меня в кармане полцейский нашел 5 грамм травы. что мне грозит?'
    query_topic = get_topic(query)
    res = qa({'query': query, 'query_topic':query_topic})

    print(f"Query: {res['query']}")
    print(f"Query Topic: {res['query_topic']}")
    print(f"Answer: {res['result']}")
    print(f"Sources: {res['source_documents']}")
