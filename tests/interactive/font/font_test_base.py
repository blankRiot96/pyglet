"""
Interactive tests for pyglet.font
"""
import pytest

from pyglet import gl
from pyglet import font

from tests.interactive.event_loop_test_base import TestWindow, EventLoopFixture
from tests.interactive.windowed_test_base import WindowedTestCase


class FontTestWindow(TestWindow):
    def __init__(self,
                 font_name='',
                 font_size=24,
                 text='Quickly brown fox',
                 color=(0, 0, 0, 1),
                 font_options=None,
                 text_options=None,
                 fill_width=False,
                 draw_baseline=False,
                 draw_metrics=False,
                 *args, **kwargs):
        super(FontTestWindow, self).__init__(*args, **kwargs)

        self.draw_baseline = draw_baseline
        self.draw_metrics = draw_metrics

        font_options = font_options or {}
        text_options = text_options or {}

        if fill_width:
            text_options['width'] = self.width - 10

        self.font = font.load(font_name, font_size, **font_options)
        assert self.font is not None
        self.label = font.Text(self.font, text, 5, 200, color=color, **text_options)

    def on_draw(self):
        super(FontTestWindow, self).on_draw()
        if self.draw_baseline:
            self._draw_baseline()
        self.label.draw()
        if self.draw_metrics:
            self._draw_metrics()

    def _draw_baseline(self):
        gl.glColor3f(0, 0, 0)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex2f(0, 200)
        gl.glVertex2f(self.width, 200)
        gl.glEnd()

    def _draw_metrics(self):
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(0, 1, 0)
        gl.glVertex2f(self.label.x, self.label.y + self.label.font.descent)
        gl.glVertex2f(self.label.x, self.label.y + self.label.font.ascent)
        gl.glColor3f(1, 0, 0)
        gl.glVertex2f(self.label.x, self.label.y + self.label.font.ascent)
        gl.glVertex2f(self.label.x + self.label.width, self.label.y + self.label.font.ascent)
        gl.glColor3f(0, 0, 1)
        gl.glVertex2f(self.label.x + self.label.width, self.label.y + self.label.font.ascent)
        gl.glVertex2f(self.label.x + self.label.width, self.label.y + self.label.font.descent)
        gl.glColor3f(1, 0, 1)
        gl.glVertex2f(self.label.x + self.label.width, self.label.y + self.label.font.descent)
        gl.glVertex2f(self.label.x, self.label.y + self.label.font.descent)
        gl.glEnd()


class FontFixture(EventLoopFixture):
    window_class = FontTestWindow

    def test_font(self, question, **kwargs):
        self.show_window(**kwargs)
        self.ask_question(question)

    @property
    def label(self):
        assert self.window is not None
        return self.window.label


@pytest.fixture
def font_fixture(request):
    return FontFixture(request)


class FontTestBase(WindowedTestCase):
    """
    Default test implementation. Use by creating a subclass and then calling the
    `create_test_case` class method with the name of the test case and any class/instance
    variables to set. This should be called outside the class definition!
    """

    # Defaults
    font_name = ''
    font_size = 24
    text = 'Quickly brown fox'
    color = 1, 1, 1, 1

    def on_expose(self):
        gl.glClearColor(0.5, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glLoadIdentity()
        self.draw()
        self.window.flip()

    def render(self):
        fnt = font.load(self.font_name, self.font_size) 
        self.label = font.Text(fnt, self.text, 10, 10, color=self.color)

    def draw(self):
        self.label.draw()
