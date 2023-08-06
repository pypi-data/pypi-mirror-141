
class Product():
    def __init__(self, record):
        self.code = record['fields']['code']
        self.name = record['fields']['name']
        self.type = record['fields']['type']
        self.themes = record['fields']['themes']
        self.collection = record['fields']['collection']
        self.topview_present = True if 'Topview found' in record['fields'].keys() else False
        self.shader_present = True if 'Shader found' in record['fields'].keys() else False
        self.data_present = True if 'Database found' in record['fields'].keys() else False

    def __str__(self) -> str:
        return f"{self.code} - {self.name} ({self.type})"

    def to_dict(self) -> dict:
        return {
            'name':self.name,
            'code':self.code,
            'collection':self.collection,
            'themes':self.themes,
            'topview':self.topview_present,
            'shader':self.shader_present,
            'database':self.data_present
            }

