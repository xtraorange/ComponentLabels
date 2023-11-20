from Canvas import Canvas
from Logger import Logger
import importlib
from reportlab.lib.colors import black

from fonts import FontManager


class Document:
    def __init__(self, layout_name, file_name, default_font = "Helvetica", default_font_size = 12, label_outlines = False, fill_page = True):
        self.layout = self._load_layout(layout_name)
        self.labels = []
        self.canvas = Canvas(file_name, pagesize=self.layout.pagesize)
        self.label_outlines = label_outlines
        self.fill_page = fill_page
        self.default_font = default_font
        self.default_size = default_font_size

    @staticmethod
    def _load_layout(layout_name):
        try:
            layout_module = importlib.import_module(f"layouts.{layout_name}")
            layout_class = getattr(layout_module, layout_name)
            return layout_class()
        except (ImportError, AttributeError) as e:
            Logger.error(f"Failed to load layout '{layout_name}': {e}")
            raise

    def _calculate_index(self, page, row, column):
        return (self.layout.num_stickers_horizontal * self.layout.num_stickers_vertical * (page - 1)) + ((row - 1) * self.layout.num_stickers_horizontal) + (column - 1)

    def add_label(self, template, page=None, row=None, col=None):
        if page is not None and row is not None and col is not None:
            index = self._calculate_index(page, row, col)

            # Calculate the number of labels to extend
            missing_labels = index - len(self.labels) + 1
            if missing_labels > 0:
                self.labels.extend([None] * missing_labels)

            if self.labels[index] is not None:
                raise ValueError(f"Label position (Page: {page}, Row: {row}, Column: {col}) is already occupied.")
            
            self.labels[index] = template
        else:
            self._add_label_to_next_available_spot(template)

    def _add_label_to_next_available_spot(self, template):
        for i, label in enumerate(self.labels):
            if label is None:
                self.labels[i] = template
                return
        self.labels.append(template)



    def render(self):
        Logger.info(f"Rendering document with layout '{self.layout.paper_name}' and size '{self.layout.pagesize}'")

        Logger.info(f"Setting font to '{self.default_font}' with size '{self.default_size}'")
        self.canvas.set_font_name(self.default_font)
        self.canvas.set_font_size(self.default_size)


        labels_per_page = self.layout.num_stickers_vertical * self.layout.num_stickers_horizontal
        total_labels = len(self.labels)

        # Fill the labels array to the next page line if fill_page is true
        if self.fill_page and total_labels == 0:
            self.labels.extend([None] * labels_per_page)
            total_labels = len(self.labels)
        elif self.fill_page and total_labels % labels_per_page != 0:
            additional_slots = labels_per_page - (total_labels % labels_per_page)
            self.labels.extend([None] * additional_slots)
            total_labels = len(self.labels)
        
        Logger.info(f"Rendering {total_labels} labels")
            
        page = 1
        for index, template in enumerate(self.labels):
            # Calculate position
            page_index = index % labels_per_page
            row = page_index // self.layout.num_stickers_horizontal
            col = page_index % self.layout.num_stickers_horizontal

            x = self.layout.left_margin + col * self.layout.horizontal_stride
            y = self.layout.pagesize[1] - (self.layout.top_margin + (row + 1) * self.layout.vertical_stride)

            # Call the method to render the label (to be implemented)
            self.render_label(x, y, template)

            if (index + 1) % labels_per_page == 0 and index + 1 < len(self.labels):
                # Finalize the current page and start a new one
                self.canvas.showPage()
                page += 1
        self.canvas.showPage()
        self.canvas.save()

    def render_label(self, x, y, template):
        Logger.info(f"Rendering label at position ({x}, {y})")
        Logger.debug(f"Rendering label with template '{template}' and outlines are")
        # Draw the label area, with or without visible outlines
        if self.label_outlines:
            self.canvas.setStrokeColor(black, 0.2)
            self.canvas.roundRect(x, y, self.layout.sticker_width, self.layout.sticker_height, self.layout.sticker_corner_radius, stroke=1, fill=0)
 
            

        self.canvas.create_sub_canvas(x, y, self.layout.sticker_width, self.layout.sticker_height, 'rounded_rectangle',  self.layout.sticker_corner_radius)

        if template is not None:
            # Render the label using the template
            template.render(self.canvas, self.layout.sticker_width, self.layout.sticker_height)

        self.canvas.restore_canvas()