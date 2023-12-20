from utilities import TypedAttributes
from templates import Template


class Generator (TypedAttributes):
    _attributes = {
        'template': (type, None),
        'labels': (list, []),
    }


    def generate(self):
        pass

    def set_template(self, template):
        self.template = template
        return self
    
    def _add_label(self, label):
        self.labels.append(label)
        return self