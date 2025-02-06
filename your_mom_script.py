import whisper
import whisperx
import csv
import gc
from googletrans import Translator
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from typing_extensions import Concatenate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import heapq
import urllib.request
import re
from moviepy.video.io.VideoFileClip import VideoFileClip
import pandas as pd
import csv
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import platform
import ctypes

if platform.system() != "Windows":
    libc = ctypes.CDLL("libc.so.6")


# Code Accepting for Prefered Language
def language(choice):
  if choice == 1:
      source_lang = 'hi'
  elif choice == 2:
      source_lang = 'bn'
  elif choice == 3:
      source_lang = 'te'
  elif choice == 4:
      source_lang = 'mr'
  elif choice == 5:
      source_lang = 'ta'
  elif choice == 6:
      source_lang = 'ur'
  elif choice == 7:
      source_lang = 'gu'
  elif choice == 8:
      source_lang = 'kn'
  elif choice == 9:
      source_lang = 'ml'
  elif choice == 10:
      source_lang = 'en'
  return source_lang

# Code for Converting MP4 format to MP3 format
def mp4tomp3(video_file_path, mp3_file_path):
  command_to_mp3 = f"ffmpeg -i {video_file_path} {mp3_file_path}"
  os.system(command_to_mp3)

# Code for Transcription in Mutliple languages
def translate_transcript(text, target_lang='en'):
    translator = Translator()
    translated_text = ""
    segments = text.split()
    prev_lang = None
    current_segment = ""
    for segment in segments:
        detected_lang = translator.detect(segment).lang
        if detected_lang != prev_lang:
            if prev_lang:
                if prev_lang != 'en':
                    translated_segment = translator.translate(current_segment, src=prev_lang, dest=target_lang)
                    translated_text += translated_segment.text.strip() + " "
                else:
                    translated_text += current_segment.strip() + " "
                current_segment = ""
            prev_lang = detected_lang
        current_segment += segment + " "
    if prev_lang and prev_lang != 'en':
        translated_segment = translator.translate(current_segment.strip(), src=prev_lang, dest=target_lang)
        translated_text += translated_segment.text.strip()
    else:
        translated_text += current_segment.strip()
    return translated_text.strip()

def transcriptnormal(file_path, filename):
    model = whisper.load_model("small")
    result = model.transcribe(file_path)
    transcript = result["text"]
    with open(filename, 'w', encoding='utf-8') as file:
      file.write(transcript)
    translated_transcript=translate_transcript(transcript)
    return translated_transcript

# Code for TimeStamp Function
def translate_text(text, target_lang='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_lang).text
    return translated_text

def transcriptcsv(audio_file, csv_filename):
  device = "cuda"
  batch_size = 16
  compute_type = "float16"
  model = whisperx.load_model("large-v2", device, compute_type=compute_type)
  audio = whisperx.load_audio(audio_file)
  result = model.transcribe(audio, batch_size=batch_size)
  with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'start', 'end']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for segment in result['segments']:
            writer.writerow(segment)
  df = pd.read_csv(csv_filename)
  output_csv_file_name = f"{name}translated_file.csv"
  for index, row in df.iterrows():
      translated_row = row.apply(lambda x: translate_text(str(x)))
      df.loc[index] = translated_row
  df.to_csv(output_csv_file_name, index=False)

# Code for Minutes of Meeting Preparation
def translateentolang(text, target_lang):
  source_lang='en'
  translator = Translator()
  translated_text = translator.translate(text, src=source_lang, dest=target_lang)
  return translated_text.text

def save_to_txt(txt_path, title, summary_text, agenda, tasks, important):
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write("Title:\n" + title + "\n\n")
        file.write("Agenda:\n" + agenda + "\n\n")
        file.write("Summary:\n" + summary_text + "\n\n")
        file.write("Tasks:\n" + tasks + "\n\n")
        file.write("Important:\n" + important + "\n\n")

def MOMAnswer(query, document_search, chain):
    docs = document_search.similarity_search(query)
    return chain.run(input_documents=docs, question=query)

def generate_mom(file_path, Language, txt_path, text_meet, attendence_file_path):
  content_text = re.sub(r'\[[0-9]*\]', ' ', text_meet)
  content_text = re.sub(r'\s+', ' ', content_text)
  formatted_content_text = re.sub('[^a-zA-Z]', ' ', content_text )
  formatted_content_text = re.sub(r'\s+', ' ', formatted_content_text)

  sentence_list = nltk.sent_tokenize(content_text)
  stopwords = nltk.corpus.stopwords.words('english')

  word_frequencies = {}
  for word in nltk.word_tokenize(formatted_content_text):
      if word not in stopwords:
          if word not in word_frequencies.keys():
              word_frequencies[word] = 1
          else:
              word_frequencies[word] += 1
  maximum_frequncy = max(word_frequencies.values())
  for word in word_frequencies.keys():
      word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

  sentence_scores = {}
  for sent in sentence_list:
      for word in nltk.word_tokenize(sent.lower()):
          if word in word_frequencies.keys():
              if len(sent.split(' ')) < 30:
                  if sent not in sentence_scores.keys():
                      sentence_scores[sent] = word_frequencies[word]
                  else:
                      sentence_scores[sent] += word_frequencies[word]

  summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
  summary = ' '.join(summary_sentences)

  attendee_names = []
  with open(attendence_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      first_name = row['First name']
      attendee_names.append(first_name)


  os.environ["OPENAI_API_KEY"]="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"
  text_splitter=CharacterTextSplitter(separator="\n", chunk_size = 100, chunk_overlap = 20,)
  texts=text_splitter.split_text(text_meet)
  embeddings= HuggingFaceEmbeddings()
  document_search=FAISS.from_texts(texts,embeddings)
  chain=load_qa_chain(OpenAI(),chain_type="stuff")
  queries = [
      "Provide suitable title of the meet",
      "What was the agenda of the meet? Provide in points. Maximum 3 Points. After each point end with '\n'",
      f"Mention the task allocated to each attendee for future. Provide in points. These are the attendee list {attendee_names}. In this format (Attendee1) : Task1, Task2,..,Task n;\n (Attendee2) : Task1, Task2,..,Task n;\n ...;\n (Attendee n) : Task1, Task2,..,Task n; where attendee name is in curve brackets. After each Each attendee and his/her tasks end with '\n'",
      "Mention the important topics discussed in the meet. Provide in points. After each point end with '\n'"
  ]
  i = 1
  result=[]
  while i != 5:
      query = queries[i - 1]
      result.append(MOMAnswer(query, document_search, chain))
      i += 1
  title=result[0]
  agenda=result[1]
  tasks=result[2]
  important=result[3]

  if Language!='en':
    title = translateentolang(title, target_lang=Language)
    agenda = translateentolang(agenda, target_lang=Language)
    summary = translateentolang(summary, target_lang=Language)
    tasks = translateentolang(tasks, target_lang=Language)
    important = translateentolang(important, target_lang=Language)
    save_to_txt(txt_path, title, summary, agenda, tasks, important)
  else:
    save_to_txt(txt_path, title, summary, agenda, tasks, important)

# Code for accepting preffered language
print("Available languages:")
print("1. Hindi")
print("2. Bengali")
print("3. Telugu")
print("4. Marathi")
print("5. Tamil")
print("6. Urdu")
print("7. Gujarati")
print("8. Kannada")
print("9. Malayalam")
print("10. English")
Languagechoice=int(input("Choose the prefered languages:"))
Language=language(Languagechoice)
# Code for accepting video file path
video_file_path=input("Enter the video path:")
attendence_file_path=input("Enter the attendence csv:")
name = video_file_path.rsplit(".", 1)[0]
mp3_file_path=f"{name}.mp3"
mp4tomp3(video_file_path, mp3_file_path)
# Code for transcripting video
filename=f"{name}.txt"
text_meet=transcriptnormal(mp3_file_path, filename)
# Code for transcripting video with timestamp
csv_filename=f"{name}.csv"
transcriptcsv(video_file_path, csv_filename)
# Code for saving Minutes of Meeting
txt_path=f"{name}MOM.txt"
generate_mom(filename, Language, txt_path, text_meet, attendence_file_path)
