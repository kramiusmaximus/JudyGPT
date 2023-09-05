import logging
import os

import dotenv
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.vectorstores.base import VectorStoreRetriever
from telegram import Update
from telegram.ext import ContextTypes
import pinecone

logger = logging.getLogger('prom') if os.getenv('ENV') == 'prom' else logging.getLogger('dev')
dotenv.load_dotenv()


question_prompt_template = """Вопрос: {question}

Ответь на данный вопрос профессионально, обсуждая все важные моменты, ссылаясь на свои знания и ниже приведенные законы. Если не хватает информации для развернутого ответа, можешь запросить всю нужную тебе информацию.

Законы:
{context}

"""

conversation_template = """
Данный текст, является разговором между Человеком и Классификатором который классифицирует юридические вопросы, но не отвечает на них.:

Человек: Вопрос - Я украл компьютер из электронного магазина. Что мне грозит?
Классификатор: [Кража и незаконное обращение с чужим имуществом]

Человек: Вопрос - Я не явился в военкомат по повестке. Что мне грозит?
Классификатор: [Уклонение от воинской службы]

Человек: Вопрос - Я подрался с мужчиной в баре. Не понятно кто начал. У меня нету претензий к нему а у него нету претензей ко мне. Что мне грозит?
Классификатор: [Мелкое хулиганство, причинение вреда здоровью, побои]

Человек: Вопрос - Я препарковался на частной территории, не на парковке, и мне пришел штраф. Я виноват?
Классификатор: [ПДД]

Человек: Вопрос - Какой дают штраф за умышленное убийство?
Классификатор: [Умышленное причинение смерти]

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


class myChain:
    def __init__(self):
        pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENVIRONMENT'))
        vectorstore = Pinecone.from_existing_index(index_name=os.getenv("PINECONE_INDEX_NAME"),
                                                   embedding=OpenAIEmbeddings(embedding_ctx_length=7000))
        retriever = VectorStoreRetriever(vectorstore=vectorstore, search_kwargs={"k": 5})

        self.qa_chain = RetrievalQA.from_llm(llm=ChatOpenAI(model_name='gpt-4'), retriever=retriever, return_source_documents=True,
                                  prompt=QUESTION_PROMPT)
        self.query_categorization_chain = LLMChain(llm=OpenAI(), prompt=CONVERSATION_PROMPT)


    def _get_topic(self, question: str) -> str:
        response = self.query_categorization_chain({'input': question})
        return response['text']

    def _make_query(self, query):
        query_topic = self._get_topic(query)
        return self.qa_chain({'query': query, 'query_topic': query_topic})

    def handle_question(self, query):
        query_response = self._make_query(query)
        logging.info(query_response)
        query_response_msg = query_response['result']
        query_response_srcs = [document.metadata['codex'] + ' - ст.' + document.metadata['article_num'] + ' - ' + document.metadata['article_name'] for document in query_response['source_documents']]
        response = query_response_msg + '\n\nРесурсы:'
        for src in query_response_srcs:
            response += '\n' + src
        return response

