import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from database import NoteObject, UserObject, User, Note
from app import db
from collections import namedtuple

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_notes = SQLAlchemyConnectionField(NoteObject)
    all_users = SQLAlchemyConnectionField(UserObject)
    coolNotes = graphene.List(NoteObject)
    getNote = graphene.List(NoteObject, q=graphene.String())

    def resolve_coolNotes(root, info):
        query = NoteObject.get_query(info).filter(
            Note.author_id == 1
        )
        print(query.all())
        return query.all()
    
    def resolve_getNote(self, info, **args):
        q = args.get("q")
        cursor = db.session.connection()
        query = cursor.execute("SELECT * FROM NOTES where uuid='%s'" % q)
        return query.fetchall()

class CreateNote(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True) 
        username = graphene.String(required=True)
    note = graphene.Field(lambda: NoteObject)
    def mutate(self, info, title, body, username):
        user = User.query.filter_by(username=username).first()
        note = Note(title=title, body=body)
        if user is not None:
            note.author = user
        db.session.add(note)
        db.session.commit()
        return CreateNote(note=note)

class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
