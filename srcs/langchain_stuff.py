import logging
import os

import dotenv
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.chains import ConversationalRetrievalChain, StuffDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.vectorstores.base import VectorStoreRetriever
import pinecone

from srcs.prompts import QUESTION_PROMPT, CATEGORIZATION_PROMPT

logger = logging.getLogger('prom') if os.getenv('ENV') == 'prom' else logging.getLogger('dev')
dotenv.load_dotenv()

CHAT_HISTORY = [
    ('Hello, who are you?','I am frodoAI, you personal LOTR QA assistant')
]


class Core:
    categorization_prompt: PromptTemplate = CATEGORIZATION_PROMPT
    qa_prompt: PromptTemplate = QUESTION_PROMPT

    def __init__(self, pine_cone_api_key, pine_cone_env, pine_cone_index_name, search_k = 5, model_name = 'gpt-4'):
        pinecone.init(api_key=pine_cone_api_key, environment=pine_cone_env)
        vectorstore = Pinecone.from_existing_index(index_name=pine_cone_index_name,embedding=OpenAIEmbeddings(embedding_ctx_length=7000))
        retriever = VectorStoreRetriever(vectorstore=vectorstore, search_kwargs={"k": search_k}, search_type="similarity")

        self.query_categorization_chain = LLMChain(llm=OpenAI(), prompt=CATEGORIZATION_PROMPT)
        self.qa_chain = ConversationalRetrievalChain.from_llm(llm=ChatOpenAI(model_name=model_name), retriever=retriever, return_source_documents=True, prompt=QUESTION_PROMPT)


    def _get_topic(self, question: str) -> str:
        response = self.query_categorization_chain({'input': question})
        return response['text']

    def _make_query(self, query):
        # query_topic = self._get_topic(query)
        # return self.qa_chain({'query': query, 'query_topic': query_topic})
        return self.qa_chain({'question': query, 'chat_history':CHAT_HISTORY})

    def handle_question(self, query):
        query_response = self._make_query(query)
        logging.info(query_response)
        query_response_msg = query_response['result']
        query_response_srcs = [document.metadata['codex'] + ' - ст.' + document.metadata['article_num'] + ' - ' + document.metadata['article_name'] for document in query_response['source_documents']]
        response = query_response_msg + '\n\nРесурсы:'
        for src in query_response_srcs:
            response += '\n' + src
        return response

