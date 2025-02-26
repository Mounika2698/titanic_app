import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Load Titanic dataset
df = pd.read_csv("titanic.csv")

# FastAPI App
app = FastAPI()

class Query(BaseModel):
    question: str

# Helper functions to get answers and visualizations from the Titanic dataset
def get_gender_percentage():
    male_count = df[df['Sex'] == 'male'].shape[0]
    total_count = df.shape[0]
    return (male_count / total_count) * 100

def get_age_histogram():
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Age'].dropna(), kde=True, bins=30, color="blue")
    plt.title("Histogram of Passenger Ages")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("age_histogram.png")
    return "age_histogram.png"

def get_avg_ticket_fare():
    return df['Fare'].mean()

def get_passenger_count_by_port():
    return df['Embarked'].value_counts()

# Initialize LangChain
def langchain_query_handler(question: str):
    template = "Answer the question based on the Titanic dataset: {question}"
    prompt = PromptTemplate(input_variables=["question"], template=template)
    llm = ChatOpenAI(temperature=0)
    chain = LLMMathChain(llm=llm, verbose=True)
    return chain.run(question)

# FastAPI route to process queries
@app.post("/query/")
async def process_query(query: Query):
    question = query.question.lower()

    if "percentage of passengers were male" in question:
        answer = get_gender_percentage()
        return {"response": f"Percentage of male passengers: {answer:.2f}%"}

    elif "show me a histogram of passenger ages" in question:
        img_path = get_age_histogram()
        return {"response": "Here is the histogram of passenger ages.", "image": img_path}

    elif "average ticket fare" in question:
        answer = get_avg_ticket_fare()
        return {"response": f"Average ticket fare: ${answer:.2f}"}

    elif "how many passengers embarked from each port" in question:
        answer = get_passenger_count_by_port()
        return {"response": f"Passengers embarked from each port:\n{answer}"}

    else:
        return {"response": langchain_query_handler(query.question)}

