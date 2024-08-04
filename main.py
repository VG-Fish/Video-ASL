import fasthtml.common as fh
from pytubefix import YouTube
import validators
from urllib.parse import urlparse

app, rt, database, Video = fh.fast_app(db="data/videos.db", live=True, id=str, pk="id", captions=str)

def make_file_import():
    return fh.Form(
        fh.Group(
            fh.Input(placeholder="Paste your youtube link", id="link"),
            fh.Button("Submit")
        ),
        hx_post="/convertor",
        hx_swap="innerHTML",
        target_id="vid-container"
    )

def unable_to_parse_link():
    return fh.Card(
        make_file_import(),
        header=fh.A("Home", href="/"),
        footer=fh.P("Unable to parse link. Make sure it's a valid youtube link.")
    )

def successully_uploaded_video():
    return fh.Titled(
        fh.Card(
            make_file_import(),
            header=fh.A("Home", href="/"),
            id="vid-container"
        )
    )

def stringify_captions_file(id):
    pass

@rt("/")
def get():
    return fh.Titled(
        "ASL Video Transcriber",
        fh.Div(fh.P('Welcome to ASL Video Converter!')),
        fh.A("Convertor", href="/convertor")
    )

@rt("/convertor")
def get():
    return successully_uploaded_video()

@rt("/convertor")
def post(link: str):
    if not validators.url(link):
        return unable_to_parse_link()
    
    video_id = urlparse(link).query
    if not video_id:
        return unable_to_parse_link()
    else:
        video_id = video_id.split("=")[1]

    yt = YouTube(link)
    captions = yt.captions.get_by_language_code('a.en')

    try:
        database.insert(Video(id=video_id, captions=captions.generate_srt_captions()))
    except:
        pass
    
    return successully_uploaded_video()

fh.serve()