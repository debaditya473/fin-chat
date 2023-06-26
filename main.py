from .Preprocessor import Preprocessor
from .Finchat import FinChatModel

file = "Apple2022.pdf"

# preprocessing the data
pp = Preprocessor(file)
data = pp.get_full_text()

# initialise our model
My_Model = FinChatModel(data)

questions = [
    "What was the company's net income in 2022?",
    "How much did the company have in total assets in 2022?",
    "How is the company adversely affected by foreign currency risk?"
]

for question in questions:
    print(question)
    print(My_Model.answer_question(query=question, k=50, n=10))
    print()