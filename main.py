import fasthtml.common as fh
from pytubefix import YouTube
import validators
from urllib.parse import urlparse

app, rt, database, video = fh.fast_app(db="data/videos.db", live=True, id=str, pk="id", captions=str)

@rt("/")
def get():
    return fh.Titled(
        "ASL Video",
        fh.Div(fh.P('Welcome to ASL Video Converter!')),
        fh.A("Convertor", href="/convertor")
    )

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

def success():
    return fh.Titled(
        fh.Card(
            make_file_import(),
            header=fh.A("Home", href="/"),
            id="vid-container"
        )
    )

@rt("/convertor")
def get():
    return success()

@rt("/convertor")
def post(link: str):
    if not validators.url(link):
        return unable_to_parse_link()
    
    vid = urlparse(link).query
    if not vid:
        return unable_to_parse_link()
    else:
        vid = vid.split("=")[1]
    
    yt = YouTube(link)
    captions = yt.captions.get_by_language_code('a.en')
    if captions:
        captions.save_captions("captions.txt")
    return success()

fh.serve()