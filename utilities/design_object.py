from Logger import Logger
from .typed_attributes import TypedAttributes

class DesignObject(TypedAttributes):
    _attributes = {
            'x': (float, 0), 
            'y': (float, 0),
            'width': (float, 0),
            'height': (float, 0),

            'shape': (str, "rectangle"),
            'radius': (int, 0),

            'draw_outline': (bool, False),
            'outline_color': (str, "#000000"),
            'outline_width': (float, 0.5),

            'allow_overflow': (bool, False),
            'rotation_angle': (float, None),
            'background_color': (str, None),

            'horizontal_align': (str, "left"),
            'vertical_align': (str, "top"),
        }


    def __init__(self):
        super().__init__()
        self.children = []


    def set_position(self, x, y):
        self.x = x
        self.y = y
        return self

    def set_size(self, width, height):
       
        self.width = width
        self.height = height
        return self
    
    def set_shape(self, shape, radius=None):
        self.shape = shape
        if radius is not None:
            self.radius = radius
        return self
    
    def outline(self, draw_outline, outline_color=None, outline_width=None):
        self.draw_outline = draw_outline
        if outline_color is not None:
            self.outline_color = outline_color
        if outline_width is not None:
            self.outline_width = outline_width
        return self
    
    def overflow(self, overflow):
        self.allow_overflow = overflow
        return self
    
    def rotate(self, rotation_angle):
        self.rotation_angle = rotation_angle
        return self
    
    def background(self, background, background_color):
        if background:
            self.background_color = background_color
        else:
            self.background_color = None
        return self

    def set_alignment(self, horizontal_align=None, vertical_align=None):
        if horizontal_align is not None:
            self.horizontal_align = horizontal_align
        if vertical_align is not None:
            self.vertical_align = vertical_align
        return self
    
    def configure(self, **kwargs):
        return self.set_attribute(**kwargs)


        

    def add_child(self, child):
        if isinstance(child, DesignObject):
            self.children.append(child)
        else:
            raise TypeError("Child must be an instance of DesignObject... current type: " + str(type(child)))


    def render(self, canvas):
        canvas.create_sub_canvas(self.x, self.y, self.width, self.height, self.shape, self.radius, self.allow_overflow, self.rotation_angle, self.draw_outline, self.outline_color, self.outline_width, self.background_color)
        
        self._pre_render(canvas)
        
        self._render_self(canvas)

        self._render_children(canvas)

        self._post_render(canvas)
        
        canvas.restore_canvas()
        

    def _render_self(self, canvas):
        pass

    def _render_children(self, canvas):
        for child in self.children:
            child.render(canvas)

    def _pre_render(self, canvas):
        pass

    def _post_render(self, canvas):
        pass