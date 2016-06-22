from mongoengine import Document, StringField, LongField, EmbeddedDocument, ListField, EmbeddedDocumentField


class Youtube(EmbeddedDocument):
    youtube_id = StringField(required=True)
    clicks = LongField()


class Composer(Document):
    uuid = StringField(required=True)
    name = StringField(required=True)
    wikipedia = StringField()
    viaf = StringField()
    youtube = ListField(EmbeddedDocumentField(Youtube))  # List of video's

