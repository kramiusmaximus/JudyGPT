import os
from math import ceil
from typing import List, Dict
import logging
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import dotenv
from langchain.schema import Document

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)


LAWS_DIR = os.getenv("LAWS_DIR")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
MAX_LEN_METADATA_PINECONE = 20000

class Codex:

    def __init__(self, codex_name, header, top, parts, footer):
        self.name = codex_name
        self.header = header
        self.top = top
        self.parts = parts
        self.footer = footer

        logging.info(f'Created Codex {codex_name} with {len(parts)} laws')

    @classmethod
    def from_text_data(cls, file_name:str, data:List[str]):
        name = file_name.strip('-u.txt')

        parsed_n = 0
        parsed, header = ParseFunctions.parse_header(data)
        parsed_n += parsed

        parsed, top = ParseFunctions.parse_top(data[parsed_n:])
        parsed_n += parsed

        parsed, parts = ParseFunctions.parse_laws(data[parsed_n:])
        parsed_n += parsed

        parsed, footer = ParseFunctions.parse_footer(data)

        logging.info(f"Parsed {file_name} with {len(data)} lines")
        return cls(name, header, top, parts, footer)


    def to_docs(self, text_max_len: int):
        docs = []
        for part in self.parts:
            if len(part['details']) > text_max_len:
                to_iter = self.divide_part(part, text_max_len)
            else:
                to_iter = [part]
            for sub_part in to_iter:
                doc = Document(page_content=sub_part["details"],
                               metadata={'codex': self.name, 'article_num': sub_part["article"],
                                         'article_name': sub_part['name']})
                docs.append(doc)
        return docs

    @staticmethod
    def divide_part(part, text_max_len):
        parts = []

        t = ceil(len(part['details']) / text_max_len)
        for i in range(t):
            start = i * text_max_len
            rem = len(part['details']) - start
            end = min((i + 1) * text_max_len, rem)
            sub_part = {
                "details": part['details'][start:end],
                "article": part['article'] + f' [PART {i + 1}/{t}]',
                "name": part['name'] + f' [PART {i + 1}/{t}]'
            }
            parts.append(sub_part)
        return parts

class ParseFunctions:
    STOP_WORDS = {"Статья", "Глава", "Раздел", "Президент", "ЧАСТЬ"}

    @staticmethod
    def parse_header(data: List[str]) -> (int, str):
        header = ""

        parsed_n = 0
        for line in data:
            if line == "------------------------------------------------------------------\n":
                break
            parsed_n += 1
            header += line

        return parsed_n, header.strip("\n")

    @classmethod
    def parse_top(cls, data: List[str]) -> (int, str):
        top = ""

        parsed_n = 0
        for line in data:
            wo_n = line.strip("\n")
            if len(cls.STOP_WORDS.intersection(set(wo_n.split(" ")))) > 0:
                break
            parsed_n += 1
            top += line

        return parsed_n, top.strip("\n")

    @classmethod
    def parse_law(cls, data: List[str]) -> (int, Dict[str, Dict]):
        # Parse all text in data until end or until stop word is reached
        txt = data[0]
        parsed_n = 1

        for line in data[1:]:
            wo_n = line.strip("\n")
            if len(cls.STOP_WORDS.intersection(set(wo_n.split(" ")))) > 0:
                break
            txt += line
            parsed_n += 1

        return parsed_n, txt

    @classmethod
    def parse_laws(cls, data: List[str]) -> (int, List[Dict]):
        laws = []
        i = 0

        while i < len(data):
            line = data[i]
            if ("Статья" in line):
                wo_n = line.strip("\n")
                (full_name, name, article) = wo_n, " ".join(wo_n.split(" ")[2:]), wo_n.split(" ")[1].strip(".")
                parsed_n, content = cls.parse_law(data[i:])
                laws.append({
                    "article": article,
                    "name": name,
                    "details": content
                })
                i += parsed_n
            else:
                i += 1

        return (i, laws)

    @classmethod
    def parse_footer(cls, data: List[str]) -> (int, str):
        footer = ""

        parsed_n = 0
        for line in data:
            wo_n = line.strip("\n")
            if len(cls.STOP_WORDS.intersection(set(wo_n.split(" ")))) > 0:
                break
            parsed_n += 1
            footer += line

        return parsed_n, footer.strip("\n")


def ingest_codex(codex:Codex):
    docs = codex.to_docs(MAX_LEN_METADATA_PINECONE)
    embeddings = OpenAIEmbeddings(embedding_ctx_length=7000)
    vector_store = Pinecone.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)
    if not vector_store:
        vector_store = Pinecone.from_documents(documents=docs,
                                     embedding=embeddings,
                                     index_name=INDEX_NAME,
                                     batch_size=4)
    else:
        vector_store.add_documents(documents=docs,
                                     batch_size=4)
    logging.info(f"Codex {codex.name} uploaded into vector store")

if __name__ == '__main__':
    data = []
    file_names = os.listdir(LAWS_DIR)
    for file_name in file_names:
        with open(LAWS_DIR + file_name, encoding="utf16") as file:
            for line in file:
                data.append(line)
            codex = Codex.from_text_data(file_name, data)
        ingest_codex(codex)
