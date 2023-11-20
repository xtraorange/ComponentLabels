#Generally speaking, you will want to position the text element 25% lower, since the baseline starts 25% above the bottom of the element

from reportlab.lib.colors import black
from reportlab.lib.units import inch
from Logger import Logger

class TextElement:
    def __init__(self, text, wrap=True, auto_truncate=True, font_size=None, line_gap=2, font_color=black, font_name=None):
        self.text = text
        self.wrap = wrap
        self.font_size = font_size  # Can be a specific size or 'auto'
        self.font_color = font_color
        self.font_name = font_name
        self.line_gap = line_gap
        self.auto_truncate = auto_truncate
        self.descender_spacer = .25


    def render(self, canvas, width, height):
        self.max_width = width
        self.max_height = height
        self.font_name = self.font_name if self.font_name else canvas.font_name
        self.font_color = self.font_color if self.font_color else canvas.fill_color

        canvas.save_style_state()
        canvas.set_font_name(self.font_name)
        canvas.set_fill_color(self.font_color)

        if self.font_size == 'auto':
            self.font_size = self._find_max_font_size_that_fits(canvas)

        canvas.set_font_size(self.font_size)
        
        if self.wrap:
            lines = self._wrap_text(canvas, self.text, self.font_size)
        else:
            lines = [self.text]

        if self.auto_truncate:
            lines = self._truncate_lines(canvas, lines)

        self._draw_lines(canvas, lines)
        canvas.restore_style_state()

    def _find_max_font_size_that_fits(self, canvas):
        Logger.debug("Finding maximum font size that fits")
        min_font_size = 1  # Minimum possible font size
        max_font_size = 200  # A reasonable upper limit for font size
        last_fitting_size = min_font_size

        while min_font_size <= max_font_size:
            mid_font_size = (min_font_size + max_font_size) // 2
            Logger.debug(f"Trying font size: {mid_font_size}")

            canvas.set_font_size(mid_font_size)
            if self.wrap:
                lines = self._wrap_text(canvas, self.text, mid_font_size)
            else:
                lines = [self.text]

            line_height = mid_font_size / 72 * inch  # Convert point size to inches
            total_height = len(lines) * (line_height + self.line_gap) - self.line_gap

            fits_in_width = all(canvas.stringWidth(line, self.font_name, mid_font_size) <= self.max_width for line in lines)
            fits_in_height = total_height <= self.max_height

            if fits_in_width and fits_in_height:
                last_fitting_size = mid_font_size
                min_font_size = mid_font_size + 1
            else:
                max_font_size = mid_font_size - 1

        Logger.debug(f"Final fitting font size: {last_fitting_size}")
        return last_fitting_size

    def _wrap_text(self, canvas, text, font_size):
        Logger.debug(f"Wrapping text with font size: {font_size}")
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            # Add a space if the line is not empty
            test_line = current_line + (" " if current_line else "") + word
            line_width = canvas.stringWidth(test_line, self.font_name, font_size)

            if line_width <= self.max_width:
                current_line = test_line
            else:
                # If the current line is not empty, append it to lines
                if current_line:
                    lines.append(current_line)
                current_line = word

        # Add the last line if it's not empty
        if current_line:
            lines.append(current_line)

        return lines

    def _truncate_lines(self, canvas, lines):
        Logger.debug("Truncating lines")
        truncated_lines = []
        for line in lines:
            while canvas.stringWidth(line, self.font_name, self.font_size) > self.max_width and len(line) > 0:
                line = line[:-1]
            truncated_lines.append(line)
        return truncated_lines

    def _draw_lines(self, canvas, lines):
        Logger.debug("Drawing lines")
        y_position = self.max_height
        line_height = self.font_size / 72 * inch  # Convert point size to inches

        descender_space = self.font_size * self.descender_spacer  

        y_position += descender_space

        for line in lines:
            if y_position - line_height < 0 and self.auto_truncate:
                break  # Stop drawing if we run out of vertical space
            y_position -= line_height
            canvas.drawString(0, y_position, line)
            y_position -= self.line_gap






    # def render(self, canvas, width, height):
    #     self.max_width = width
    #     self.max_height = height
    #     self.font_name = self.font_name if self.font_name else canvas.font_name
    #     self.font_color = self.font_color if self.font_color else canvas.fill_color
    #     self.font_size = self.font_size if self.font_size else canvas.font_size

    #     canvas.save_style_state()
        
    #     canvas.set_font_name(self.font_name)
    #     canvas.set_fill_color(self.font_color)
        
    #     Logger.debug("Rendering text element using font %s" % self.font_name)

    #     if self.font_size == 'auto':
    #         self._auto_resize_text(canvas)

    #     canvas.set_font_size(self.font_size)
        
    #     lines = self._reflow_text(canvas, self.text.split()) if self.wrap else [self.text]
    #     if self.auto_truncate:
    #         lines = [line if canvas.stringWidth(line, self.font_name, self.font_size) <= self.max_width else line[:self.max_chars_in_line(canvas, line)] for line in lines]

    #     self._draw_lines(canvas, lines)

    #     canvas.restore_style_state()

    # def _auto_resize_text(self, canvas):
    #     min_font_size = 1  # Minimum possible font size
    #     max_font_size = 200  # A reasonable upper limit for font size
    #     last_fitting_size = min_font_size

    #     while min_font_size <= max_font_size:
    #         mid_font_size = (min_font_size + max_font_size) // 2
    #         Logger.debug(f"Trying font size: {mid_font_size}")

    #         canvas.setFont(self.font_name, mid_font_size)
    #         estimated_line_height = mid_font_size * (1 / 72) * inch

    #         if self.wrap:
    #             lines = self._reflow_text(canvas, self.text.split(), mid_font_size)
    #             total_text_height = len(lines) * estimated_line_height + (len(lines) - 1) * self.line_gap
    #         else:
    #             lines = [self.text]
    #             total_text_height = estimated_line_height

    #         fits_in_width = all(canvas.stringWidth(line, self.font_name, mid_font_size) <= self.max_width for line in lines)
    #         fits_in_height = total_text_height <= self.max_height

    #         if fits_in_width and fits_in_height:
    #             last_fitting_size = mid_font_size
    #             min_font_size = mid_font_size + 1
    #         else:
    #             max_font_size = mid_font_size - 1

    #     Logger.debug(f"Final fitting font size: {last_fitting_size}")
    #     self.font_size = last_fitting_size





    # def _reflow_text(self, canvas, words, font_size=None):
    #     if font_size is None:
    #         font_size = self.font_size

    #     Logger.debug(f"Reflowing text with font size: {font_size}")
    #     lines, line = [], ""
    #     for word in words:
    #         test_line = line + " " + word if line else word
    #         if canvas.stringWidth(test_line, self.font_name, font_size) <= self.max_width:
    #             line = test_line
    #         else:
    #             if line: 
    #                 lines.append(line)
    #             line = word
    #     if line: 
    #         lines.append(line)
    #     return lines


    # def _draw_lines(self, canvas, lines):
    #     Logger.debug(f"Drawing lines: {lines}")
    #     estimated_line_height = self.font_size * (1 / 72) * inch
    #     y_position = self.max_height - estimated_line_height
    #     for line in lines:
    #         canvas.drawString(0, y_position, line)
    #         y_position -= (estimated_line_height + self.line_gap)


    # def _max_chars_in_line(self, canvas, text):
    #     Logger.debug(f"Calculating max chars in line for text: '{text}'")
    #     for i in range(1, len(text) + 1):
    #         if canvas.stringWidth(text[:i], self.font_name, self.font_size) > self.max_width:
    #             return i - 1
    #     return len(text)
