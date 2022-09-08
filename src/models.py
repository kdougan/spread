from pony.orm import Database
from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import Optional
from pony.orm import Json
from pony.orm import Set
from config import settings

db = Database()

db.bind(provider='cockroach',
        user=settings.database.user,
        password=settings.database.password,
        host=settings.database.host,
        database=settings.database.db)


class User(db.Entity):  # type: ignore
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    email = Required(str, unique=True)
    hashed_password = Required(str, unique=True, hidden=True)
    meta = Optional(Json, default="{}")
    posts = Set('Post')
    comments = Set('Comment')


class Post(db.Entity):  # type: ignore
    id = PrimaryKey(int, auto=True)
    title = Required(str, 256)
    content = Optional(str, nullable=True)
    user = Required(User)
    meta = Optional(Json, default="{}")
    comments = Set('Comment')


class Comment(db.Entity):  # type: ignore
    id = PrimaryKey(int, auto=True)
    content = Required(str)
    user = Required(User)
    post = Optional(Post)
    parent = Optional('Comment', reverse='comments')
    comments = Set('Comment', reverse='parent')
    meta = Optional(Json, default="{}")


class Article(db.Entity):  # type: ignore
    id = PrimaryKey(int, auto=True)
    title = Optional(str)


db.generate_mapping()
