from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Load Titanic dataset
df = pd.read_csv('titanic.csv')

# Initialize FastAPI app
app = FastAPI()

class QuestionRequest(BaseModel):
    query: str

@app.post("/ask_question/")
async def ask_question(request: QuestionRequest):
    query = request.query.lower()
    print(f"Received query: {query}")  # Log the received query
    
    if "percentage of passengers were male" in query:
        male_percentage = (df['Sex'] == 'male').mean() * 100
        return {"answer": f"The percentage of male passengers was {male_percentage:.2f}%"}

    elif "histogram of passenger ages" in query:
        # Create histogram for passenger ages
        plt.figure(figsize=(6,4))
        plt.hist(df['Age'].dropna(), bins=30, edgecolor='black')
        plt.title('Histogram of Passenger Ages')
        plt.xlabel('Age')
        plt.ylabel('Frequency')

        # Save the plot to a BytesIO object to return as a base64 string
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

        return {"answer": "Here is a histogram of passenger ages.", "image": img_base64}

    elif "average ticket fare" in query:
        avg_fare = df['Fare'].mean()
        return {"answer": f"The average ticket fare was ${avg_fare:.2f}"}

    elif "embarked from each port" in query:
        embark_counts = df['Embarked'].value_counts()
        embark_text = "\n".join([f"{port}: {count}" for port, count in embark_counts.items()])
        return {"answer": f"Number of passengers embarked from each port:\n{embark_text}"}

    else:
        return {"answer": "Sorry, I can't answer that question."}
