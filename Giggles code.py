import random
import tkinter as tk
import pygame
from PIL import Image, ImageTk
import os
import pyttsx3
import speech_recognition as sr

class MusicRecommenderBot:
    def _init_(self, root):
        self.root = root
        self.root.title("GIGGLE - Music Recommender Chatbot")

        # Initialize Pygame mixer for playing audio
        pygame.mixer.init()

        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()

        # Create GUI elements
        self.create_widgets()

        # Setup the music database
        self.setup_music_database()

    def create_widgets(self):
        # Create a frame to hold chat history, user input, and image display
        self.chat_frame = tk.Frame(self.root, bg="grey")  # Black background color for chat frame
        self.chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Load and display an image in the chatbot interface
        image_path = r"C:\Users\DELL\Pictures\Capture.PNG"  # Update with your image path
        self.load_and_display_image(image_path)

        # Create and configure chat history text widget
        self.chat_history = tk.Text(self.chat_frame, width=80, height=15, bg="white", bd=2, relief=tk.GROOVE, font=("Arial", 12), wrap=tk.WORD)
        self.chat_history.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=(10, 0), expand=True)

        # Create user input entry widget
        self.user_input = tk.Entry(self.chat_frame, width=60, bd=2, relief=tk.SOLID, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, padx=10, pady=(0, 10), fill=tk.X, expand=True)

        # Create send button
        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message, bd=2, relief=tk.RAISED, font=("Arial", 12))
        self.send_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

        # Create voice input button
        self.voice_button = tk.Button(self.chat_frame, text="Voice", command=self.listen_and_reply, bd=2, relief=tk.RAISED, font=("Arial", 12))
        self.voice_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

    def load_and_display_image(self, image_path):
        try:
            if os.path.exists(image_path):
                # Load the image using PIL (Python Imaging Library) and resize
                image = Image.open(image_path)
                image = image.resize((1000, 300))  # Resize the image as needed
                photo = ImageTk.PhotoImage(image)

                # Create a label to display the image above chat history
                self.image_label = tk.Label(self.chat_frame, image=photo, bg="grey")  # Match background color
                self.image_label.image = photo  # Keep a reference to the image to prevent garbage collection
                self.image_label.pack(pady=(10, 0))
            else:
                print(f"Error: Image file not found at {image_path}")
        except Exception as e:
            print(f"Error loading image: {e}")

    def setup_music_database(self):
        # Define the music database
        self.music_database = {
            'happy': [
                r'C:\Users\DELL\Downloads\dramatic-atmosphere-with-piano-and-violin-short-version-199232 (1).mp3',

            ],
            'sad': [
                r'C:\Users\DELL\Downloads\sad-violin-150146 (4).mp3',

            ],
            'angry': [
                r'C:\Users\DELL\Downloads\Death Grips - Get Got.mp3',

            ]
        }

    def send_message(self):
        # Get user input from the entry widget
        user_message = self.user_input.get()

        # Display user message in the chat history
        self.display_message("User", user_message)

        # Get bot response based on user message
        bot_response = self.get_bot_response(user_message)

        # Display bot response in the chat history
        self.display_message("GIGGLE", bot_response)

        # Speak the bot response
        self.speak(bot_response)

        # Check if bot response is a song category and play a random song from that category
        if bot_response in self.music_database:
            song_to_play = random.choice(self.music_database[bot_response])
            self.play_song(song_to_play)

        # Clear the user input entry widget
        self.user_input.delete(0, tk.END)

    def display_message(self, sender, message):
        # Insert the message into the chat history
        self.chat_history.insert(tk.END, f"{sender}: {message}\n")
        # Scroll to the end of the chat history
        self.chat_history.see(tk.END)

    def get_bot_response(self, user_message):
        # Determine bot response based on user input
        user_message = user_message.lower()

        if any(word in user_message for word in ['hello', 'hi', 'hey']):
            return "Hello! GIGGLE this side, How can I assist you today?"
        elif any(word in user_message for word in ['happy', 'joy', 'good']):
            return 'happy'
        elif any(word in user_message for word in ['sad', 'unhappy', 'cry']):
            return 'sad'
        elif any(word in user_message for word in ['angry', 'mad', 'frustrated']):
            return 'angry'
        else:
            return "I'm sorry, I didn't quite get that. Can you please clarify?"

    def speak(self, text):
        # Use text-to-speech engine to speak the provided text
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def play_song(self, song_file):
        try:
            if os.path.exists(song_file):
                # Load and play the specified song file using Pygame mixer
                pygame.mixer.music.load(song_file)
                pygame.mixer.music.play()
            else:
                print(f"Error: Song file not found at {song_file}")
        except pygame.error as e:
            print(f"Error playing song: {e}")

    def listen_and_reply(self):
        # Listen for user voice input and process the response
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            # Use speech recognition to convert audio to text
            user_voice_input = recognizer.recognize_google(audio)
            print("User said:", user_voice_input)

            # Set the user voice input to the input entry widget
            self.user_input.delete(0, tk.END)
            self.user_input.insert(0, user_voice_input)

            # Send the user voice input for processing
            self.send_message()

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error fetching results from Google Speech Recognition service; {e}")

# Create the main window
if _name_ == "_main_":
    root = tk.Tk()
    bot = MusicRecommenderBot(root)
    root.mainloop()
