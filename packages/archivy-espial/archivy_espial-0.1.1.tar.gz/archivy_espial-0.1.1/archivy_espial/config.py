from espial.config import Config

class Config(Config):
    def __init__(self):
        super().__init__()
        self.IGNORE = ["concepts/"]

    def get_item_id(self, item):
        return item["path"].split('/')[-1].split('-')[0]

    def get_title(self, path, contents):
        import frontmatter
        item = frontmatter.loads(contents)
        if "title" in item:
            return frontmatter.loads(contents)["title"]
        else: return path.parts[-1]

    def create_concept_note(self, concept, mesh):
        from pathlib import Path
        from archivy.models import DataObj
        from archivy import app
        with app.app_context():
            contents = f"# {concept}\n"
            c_note = DataObj(title=concept, type="note")
            for doc, concept, data in mesh.graph.in_edges(concept, data=True):
                doc = mesh.doc_cache[doc]
                contents += f"- {self.get_link(doc)}: Mentioned {data['count']} times.\n"
            c_note.content = contents
            conc_dir = Path(self.data_dir) / "concepts"
            conc_dir.mkdir(exist_ok=True)
            c_note.path = "concepts/"
            c_note.insert()

    def get_link(self, item):
        return f"[[{item._.title}|{item._.id}]]"

    def get_item_id(self, item):
        return item["path"].split('/')[-1].split('-')[0]
    def get_title(self, path, contents):
        import frontmatter
        item = frontmatter.loads(contents)
        if "title" in item:
            return frontmatter.loads(contents)["title"]
        else: return path.parts[-1]
    def create_concept_note(self, concept, mesh):
        from pathlib import Path
        from archivy.models import DataObj
        from archivy import app
        with app.app_context():
            contents = f"# {concept}\n"
            c_note = DataObj(title=concept, type="note")
            for doc, concept, data in mesh.graph.in_edges(concept, data=True):
                doc = mesh.doc_cache[doc]
                contents += f"- {self.get_link(doc)}: Mentioned {data['count']} times.\n"
            c_note.content = contents
            conc_dir = Path(self.data_dir) / "concepts"
            conc_dir.mkdir(exist_ok=True)
            c_note.path = "concepts/"
            c_note.insert()

    def get_link(self, item):
        return f"[[{item._.title}|{item._.id}]]"
        self.ANALYSIS["cutoffs"]["min_avg_ent_tf_idf"] = 0.01

    def get_item_id(self, item):
        return item["path"].split('/')[-1].split('-')[0]
    def get_title(self, path, contents):
        import frontmatter
        item = frontmatter.loads(contents)
        if "title" in item:
            return frontmatter.loads(contents)["title"]
        else: return path.parts[-1]
    def create_concept_note(self, concept, mesh):
        from pathlib import Path
        from archivy.models import DataObj
        from archivy import app
        with app.app_context():
            contents = f"# {concept}\n"
            c_note = DataObj(title=concept, type="note")
            for doc, concept, data in mesh.graph.in_edges(concept, data=True):
                doc = mesh.doc_cache[doc]
                contents += f"- {self.get_link(doc)}: Mentioned {data['count']} times.\n"
            c_note.content = contents
            conc_dir = Path(self.data_dir) / "concepts"
            conc_dir.mkdir(exist_ok=True)
            c_note.path = "concepts/"
            c_note.insert()

    def get_link(self, item):
        return f"[[{item._.title}|{item._.id}]]"
