#Generally speaking, you will want to position the text element 25% lower, since the baseline starts 25% above the bottom of the element
from elements import Element
from reportlab.lib.units import inch
from Logger import Logger
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY


import re

class TextElement(Element):
    _attributes = {
        'text': (str, ""),
        'wrap': (bool, True),
        'font_size': (float, None),
        'font_color': (str, None),
        'font_name': (str, None),
        'line_gap': (float, 2),
        'descender_spacer': (float, .25),

    }

    def __init__(self, text):
        super().__init__()
        if text is not None:
            self.text = str(text)
        else:
            self.text = ""


    def _render_self(self, canvas):
        Logger.debug(f"Rendering text element: {self.text}")

        # Set the width and height from the canvas
        self.width = canvas.width
        self.height = canvas.height

        # Set default style attributes
        self.font_name = self.font_name if self.font_name else canvas.font_name
        self.font_color = self.font_color if self.font_color else canvas.fill_color
        self.font_size = self.font_size if self.font_size is not None else canvas.font_size


        # If auto font size is set, adjust font size to fit
        if self.font_size == 0 or self.font_size is None:
            self.font_size = self._determine_font_size(canvas, self.text)

        if not self.wrap:
            self._truncate(canvas)

        paragraph = self._create_paragraph(self.text, self.font_size)
        
        paragraph.wrap(self.width, self.height)


        
        x_position = 0
        if self.vertical_align == "top":
            y_position = canvas.height - paragraph.height + self.descender_spacer * self.font_size
        elif self.vertical_align == "middle":
            y_position = (canvas.height - paragraph.height + self.descender_spacer * self.font_size) / 2
        elif self.vertical_align == "bottom":
            y_position = 0


        paragraph.drawOn(canvas, x_position, y_position)


    def _determine_line_gap(self, text):
        return 1.25 * max(self.font_size, self._get_max_font_size(text))

    

    def _get_max_font_size(self, text):
        font_tag_regex = re.compile(r'<font size="(\d+%?)">')
        font_sizes = re.findall(font_tag_regex, text)
        if not font_sizes:
            return None
        return max(font_sizes, key=lambda size: int(size.rstrip('%')))


    def adjust_font_sizes(self, text, default_font_size):
        font_tag_regex = re.compile(r'<font size="?(\d+%?)"?>')
        end_tag_regex = re.compile(r'</font>')
        
        stack = [default_font_size]  # Stack to keep track of current font sizes
        adjusted_text = ""
        last_idx = 0

        for match in re.finditer(r'<font size="?(\d+%?)"?>|</font>', text):
            tag_start, tag_end = match.span()
            adjusted_text += text[last_idx:tag_start]

            if font_tag_regex.match(match.group()):
                size_value = match.group(1)
                # Calculate new size based on the top value of the stack
                base_size = stack[-1]
                if size_value.endswith('%'):
                    new_size = round(base_size * (int(size_value[:-1]) / 100.0))
                else:
                    new_size = int(size_value)
                stack.append(new_size)
                adjusted_text += f'<font size="{new_size}">'
            elif end_tag_regex.match(match.group()):
                if len(stack) > 1:  # Ensure there's an opening tag for this closing tag
                    stack.pop()
                    if len(stack) > 1:  # Check if there's still another item in the stack
                        adjusted_text += f'<font size="{stack[-1]}">'
                    else:
                        adjusted_text += '</font>'
                else:
                    raise ValueError("Unmatched closing </font> tag: " + match.group())

            last_idx = tag_end

        adjusted_text += text[last_idx:]

        if len(stack) > 1:
            raise ValueError("Missing closing </font> tag(s)")

        return adjusted_text




    def _determine_font_size(self, canvas, text, max_font_size=250):
        #use _create_paragraph to test font sizes for the given text
        best_font_size = None
        for font_size in range(1,max_font_size):
            paragraph = self._create_paragraph(text, font_size)
            paragraph.wrap(canvas.width, canvas.height)

            if self.wrap and (paragraph.height - self.line_gap) <= canvas.height:
                best_font_size = font_size
            elif not self.wrap:
                sized_text = self.adjust_font_sizes(text, font_size)
                max_size = self._get_max_font_size(sized_text)
                if max_size is None:
                    font_size = font_size
                else:
                    font_size = max(self._get_max_font_size(self.text), font_size)
                height = self._font_size_to_pixels(canvas, font_size) * 1.5
                if paragraph.height <= height:
                    best_font_size = font_size

        if best_font_size is not None:
            return best_font_size    
        raise(ValueError("Unable to determine font size"))




    def _create_paragraph(self, text, font_size):
        text = self.adjust_font_sizes(text, font_size)

        if self.line_gap is None:
            self.line_gap = self._determine_line_gap(text)

        if self.horizontal_align == "left":
            alignment = TA_LEFT
        elif self.horizontal_align == "center":
            alignment = TA_CENTER
        elif self.horizontal_align == "right":
            alignment = TA_RIGHT
        elif self.horizontal_align == "justify":
            alignment = TA_JUSTIFY
        else:
            alignment = TA_LEFT


        style = ParagraphStyle(name='Normal', fontName=self.font_name, fontSize=font_size, 
                            textColor=self.font_color, leading=font_size + self.line_gap, alignment=alignment)

        # Create a Paragraph object
        paragraph = Paragraph(text, style)
        return paragraph
    

    def _truncate(self, canvas):
        while True:
            max_size = self._get_max_font_size(self.text)
            if max_size is None:
                font_size = self.font_size
            else:
                font_size = max(self._get_max_font_size(self.text), self.font_size)
            height = self._font_size_to_pixels(canvas, font_size) * 1.5

            # Check if the current text fits within the desired height
            paragraph = self._create_paragraph(self.text, self.font_size)
            paragraph.wrap(self.width, self.height)
            if paragraph.height < height:
                break

            # If it doesn't fit, remove one character (considering tags)
            self.text = self._remove_one_character(self.text)

            # Check for an empty string to avoid an infinite loop
            if not self.text:
                raise ValueError("Unable to truncate text to fit the canvas.")



    def _font_size_to_pixels(self, canvas, font_size):
        return round(font_size * 1)
    
    def _remove_one_character(self, text):
        # Split text into segments of tags and non-tag text
        segments = re.findall(r'(<[^>]+>|[^<>]+)', text)

        # Remove one character from the last non-tag segment
        for i in range(len(segments) - 1, -1, -1):
            if not segments[i].startswith('<'):  # Find the last non-tag segment
                if len(segments[i]) > 1:
                    segments[i] = segments[i][:-1]  # Remove one character
                else:
                    segments.pop(i)  # Remove the segment if it's a single character
                break

        # Reconstruct the text and remove empty tags
        new_text = ''.join(segments)
        return self._remove_empty_tags(new_text)

    def _remove_empty_tags(self, text):
        # Remove empty tags from the text
        return re.sub(r'<[^>]+>\s*</[^>]+>', '', text)

