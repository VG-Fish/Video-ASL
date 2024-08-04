from fasthtml import common as fh

def render(DB):
    db_id = f"todo-{DB.id}"
    toggle = fh.A("Toggle", hx_get=f"/toggle/{DB.id}", target_id=db_id)
    delete = fh.A("Delete", hx_delete=f"/{DB.id}", hx_swap="outerHTML", target_id=db_id)
    return fh.Li(toggle, delete, DB.title + (" ✅" if DB.done else " ❌"), id=db_id)

app, rt, db, DB = fh.fast_app(db="db.db", live=True, render=render, id=int, title=str, done=bool, pk="id")

def make_input():
    # FastHTML automatically adds a name if an id is defined
    return fh.Input(placeholder="Add a new todo", id="title", hx_swap_oob="true")
 
@rt('/')
def get():
    form = fh.Form(
        fh.Group(
            make_input(), 
            fh.Button("Add")
        ), 
        hx_post="/",
        hx_swap="beforeend",
        target_id="todo-list"
    )

    return fh.Titled(
        "Practice", 
        fh.Div(fh.P('Hello World!'), hx_get="/change"),
        fh.Card(
            fh.Ul(*db(), id="todo-list"),
            header=form
        ),
    )

@rt("/")
def post(todo: DB):
    return db.insert(todo), make_input()

@rt("/{db_id}")
def delete(db_id: int):
    db.delete(db_id)

@rt("/change")
def get():
    return fh.P("Bruh")

@rt("/toggle/{db_id}")
def get(db_id: int):
    item = db[db_id]
    item.done = not item.done
    return db.update(item)

fh.serve()