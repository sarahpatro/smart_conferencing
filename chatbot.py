import os
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
import openai

def list_files(directory):
    files = os.listdir(directory)
    return f"Files and directories in {directory}:\n" + "\n".join(files)

def change_directory(path):
    os.chdir(path)
    return f"Current directory changed to {os.getcwd()}"

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return f"Contents of {file_path}:\n{content}"

tools = [
    Tool(
        name="List Files",
        func=list_files,
        description="List all files and directories in a given directory"
    ),
    Tool(
        name="Change Directory",
        func=change_directory,
        description="Change the current working directory"
    ),
    Tool(
        name="Read File",
        func=read_file,
        description="Read the contents of a file"
    )
]
toolsgreet=[]

os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent="conversational-react-description", verbose=True, handle_parsing_errors=True)
agentgreet = initialize_agent(toolsgreet, llm, agent="conversational-react-description", verbose=True, handle_parsing_errors=True)

User_Name=input("Enter your Name: ")
Initial_Path="/content/drive/MyDrive/Meetings"
openai.api_key = os.environ["OPENAI_API_KEY"] = "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"

Greetings = agentgreet.run(
    {
        "input": f"Greet the user {User_Name} and ask how you might assist him/her today",
        "chat_history": "your name is Astute and you are assisting bot"
    }
)
print(Greetings)

chat_history = []

def store_chat_history(input_text, output_text):
    chat_history.append({"input": input_text, "output": output_text})

while True:
    question = input("Enter the Question:")
    if question=="exit":
      break
    else:
      current_file_path = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[{"role": "user", "content": f"Identify the file name in the line :{question}. Only give filename as answer"}],
          max_tokens=1024,
          n=1,
          stop=None,
          temperature=0.5,
      )
      current=current_file_path.choices[0].message.content.strip()
      context = {
          "input": f"Directory: {Initial_Path}, File Path: {Initial_Path}/{current}, I am: {User_Name}, Answer the following question: {question}",
          "chat_history": chat_history[-4:]
      }
      response = agent.run(context)
      print("AI:", response)
      store_chat_history(question, response)