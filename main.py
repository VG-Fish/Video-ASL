import fasthtml.common as fh

app, rt = fh.fast_app(live=True)

@rt("/")
def get():
    return fh.Titled(
        "ASL Video",
    )

fh.serve()