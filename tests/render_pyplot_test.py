
import os
from novel_toy_tools.implementations.render_pyplot import PyPlotViewRenderer

objectpath = os.path.join("/", "../data/teapot.obj")

renderer = PyPlotViewRenderer()
renderer.render_view( objectpath, (0, 0, 0), ".../tests/test_rendition.png")