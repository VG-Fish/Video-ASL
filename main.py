from fasthtml.common import *
from pytubefix import YouTube
import validators, string, os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from video_creator import create_video


app, rt = fast_app(live=True)

def make_file_import():
    return Form(
        Group(
            Input(placeholder="Paste your youtube link", id="link"),
            Button("Submit")
        ),
        hx_post="/converter",
        hx_swap="innerHTML",
        target_id="vid-container"
    )

def unable_to_parse_link():
    return Card(
        make_file_import(),
        header=A("Home", href="/", ),
        footer=P("Unable to parse link. Make sure it's a valid youtube link.")
    )

def  default_video_state():
    return Titled(
        Card(
            make_file_import(),
            header=A("Home", href="/" ),
            id="vid-container"
        )
    )

def successfully_uploaded_video(output_path):
    return (
        default_video_state(),
        A(f"Download Youtube Video ID = {output_path}", href=f"{output_path}.mp4", download=f"output-{output_path}")
    )

def get_captions_text(captions):
    return BeautifulSoup(captions.xml_captions, "lxml-xml").get_text()

def get_asl_letter_file(letter: str):
    if letter in string.ascii_lowercase:
        return rf"asl/{letter}.jpg"

def generate_video(captions: str, output_path):
    input_files = []
    for letter in captions:
        if not letter.isspace():
            input_files.append(get_asl_letter_file(letter.lower()))
    durations = [0.4] * len(input_files)

    input_files = [i for i in input_files if i]
    create_video(input_files, durations, f"{output_path}.mp4")

@rt("/")
def get():
    return (
        Title('Video ASL Converter'),
        Div(A('Home', href='/', style='text-decoration: none; font-size: 25px; margin-left: 20px; margin-right: 20px;'), 
            A('Converter', href='/converter', style='text-decoration: none; font-size: 25px; margin-left: 20px; margin-right: 20px;'), style='background-color: white; display: flex; justify-content: center; align-items: center; height: 80px;'),
        Div(H2('Welcome to Video ASL Converter!', style='text-align: center; font: small-caps bold 24px/1 sans-serif; color: #FF4500;')),
        Div(H3('What Is Video ASL Converter?', style='text-align: center; font: small-caps  24px/1 sans-serif; color:#FFD700 '),
        P('Video ASL Converter is a project designed with the goal of making content accessible for the Deaf and Hard-of-Hearing community. Our platform takes your video and analyzes its components to generate a translation of the video in ASL. Whether it be a presentation, tutorial, or a form of entertainment, our platform ensures that your content is accessible to everyone. Join us as we attempt to overcome and solve barriers to communication and accessability worldwide.', style = 'color: #FFF5EE;')),
        Div(H3('How to Use Video ASL Converter:', style = 'font: small-caps bold 24px/1 sans-serif; color: #FFD700'),
        H4('Step 1: Copy the link to your selected YouTube video.', style = 'color: #FFF5EE;'),
        H4('Step 2: Click this', A('link', href='/converter'), 'and paste the url of the video.', style = 'color: #FFF5EE;')),
        Div(H3('About Us',style = 'font: small-caps bold 24px/1 sans-serif; color: #FFD700; '),
        P('Video ASL Converter was created by a group of three high-school students with the goal of bridging gaps in communication and accessibility globally. We recognized the need for greater accessibility that comes with the global growth of media, and decided to develop a solution. Our work was fueled by a belief that access to information should be universal. Video ASL Converter was created as a means of increasing accessibility by making content more accessible to the Deaf community via converting speech to ASL.', style = 'color: #FFF5EE;'))
    )

@rt("/converter")
def get():
    return (
        Div(A('Home', href='/', style='text-decoration: none; font-size: 25px; margin-left: 20px; margin-right: 20px;'), 
            A('Converter', href='/converter', style='text-decoration: none; font-size: 25px; margin-left: 20px; margin-right: 20px;'), style='background-color: white; display: flex; justify-content: center; align-items: center; height: 80px;'),
        default_video_state()
    )

@rt("/converter")
def post(link: str):
    # check if link is valid
    if not validators.url(link):
        return unable_to_parse_link()
    
    video_id = urlparse(link).query
    if not video_id:
        return unable_to_parse_link()
    else:
        video_id = video_id.split("=")[1]

    # get captions
    yt = YouTube(link)
    captions = yt.captions.get_by_language_code('a.en')
    captions = get_captions_text(captions)

    generate_video(captions, video_id)

    return successfully_uploaded_video(video_id)

serve()