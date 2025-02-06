import csv
import openai
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
# Function to load attendees from CSV file
def load_attendees_from_csv(csv_file):
  with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    attendees = []
    for row in reader:
      attendees.append(row)
  return attendees

# Load attendees from CSV
attendees = load_attendees_from_csv('/content/attendence.csv')

# Load OpenAI API key from environment variable
openai.api_key = os.environ["OPENAI_API_KEY"] = "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"

# Check if the API key is set
if openai.api_key is None:
  print("Error: OpenAI API key not found. Please set the environment variable 'OPENAI_API_KEY'.")
else:
  # Load the transcript text file
  with open('/content/Meeting.txt', 'r') as file:
    transcript_text = file.read()

  # Function to extract tasks and deadlines
  def extract_tasks_and_deadlines(attendee_name, transcript_text):
    prompt = f"What tasks and deadlines were assigned to {attendee_name} in the following transcript?\n\n{transcript_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

  # Extract tasks and deadlines for all attendees
  for attendee in attendees:
    name = attendee['First name']
    tasks_and_deadlines = extract_tasks_and_deadlines(name, transcript_text)
    attendee['Tasks & Deadlines'] = tasks_and_deadlines  # Add new column

  # Write updated data back to the CSV file
  with open('/content/attendence.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=attendees[0].keys())
    writer.writeheader()
    writer.writerows(attendees)

  print("Tasks and deadlines added to 'atten.csv' for attendees with existing data.")


def load_attendees_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        attendees = []
        for row in reader:
            attendees.append(row)
    return attendees

def read_password_from_file(file_path):
    with open(file_path, 'r') as file:
        password = file.read().strip()
    return password

# Function to send email with attachment
def send_email_with_attachment(receiver_email, subject, message, attachment_path):
    sender_email = "adityashri.gupta2021@vitstudent.ac.in"  # Change this to your email
    sender_password_file = "/content/password.txt"  # File containing sender's password

    # Read sender's password from file
    sender_password = read_password_from_file(sender_password_file)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Read the contents of the file as a string
    with open(attachment_path, 'r') as file:
        attachment_content = file.read()

    part = MIMEText(attachment_content, 'plain')
    part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()


# Load attendees from CSV
attendees = load_attendees_from_csv('/content/attendence.csv')

# Load the list of random text files
text_files = ['/content/Meeting.txt']  # Update with your text files

# Load OpenAI API key from environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

# Check if the API key is set
if openai.api_key is None:
    print("Error: OpenAI API key not found. Please set the environment variable 'OPENAI_API_KEY'.")
else:
    # Load the transcript text file
    with open('/content/Meeting.txt', 'r') as file:
        transcript_text = file.read()

    # Function to extract tasks and deadlines
    def extract_tasks_and_deadlines(attendee_name, transcript_text):
        prompt = f"What tasks and deadlines were assigned to {attendee_name} in the following transcript?\n\n{transcript_text}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()

    # Extract tasks and deadlines for all attendees
    for attendee in attendees:
        name = attendee['First name']
        tasks_and_deadlines = extract_tasks_and_deadlines(name, transcript_text)
        attendee['Tasks & Deadlines'] = tasks_and_deadlines  # Add new column

        # Choose a random text file to attach
        attachment_path = random.choice(text_files)

        # Send email to attendee with attachment
        email = attendee['Email']
        subject = f"Task Information and Random File for {name}"
        message = f"Dear {name},\n\n"
        message += f"Your tasks:\n{tasks_and_deadlines}\n\n"
        message += "Attached is a random file.\n\n"
        message += "Best regards,\nAdityashri Gupta"

        send_email_with_attachment(email, subject, message, attachment_path)

        print(f"Email sent to {name} at {email} with attachment {attachment_path}")

    # Write updated data back to the CSV file
    with open('/content/attendence.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=attendees[0].keys())
        writer.writeheader()
        writer.writerows(attendees)

    print("Tasks and deadlines added to 'atten.csv' for attendees with existing data.")
