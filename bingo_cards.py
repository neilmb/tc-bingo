#!/usr/bin/env python

"""Create bingo cards from a configuration file with possible entries."""

import importlib
import random

import click

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

N = 5


def _paragraph(text):
    """Make text into a flowed paragraph."""
    stylesheet=getSampleStyleSheet()
    normalStyle = stylesheet['Normal']
    normalStyle.fontSize = 12
    return Paragraph(text, normalStyle)


def draw_card(canv, config):
    """Draw one bingo card on the canvas."""
    # title
    canv.setFont("Helvetica-Bold", 24)
    canv.drawString(72, 72 + 24, config.TITLE)

    # grid
    left = 72
    right = 612 - 72
    top = 72 + 24 + 12
    bottom = 792 - 72
    width = (right - left) / N
    height = (bottom - top) / N
    canv.lines(
        # verticals
        [ (left + i*width, bottom, left + i*width, top) for i in range(N+1) ] + 
        # horizontals
        [ (left, top + i*height, right, top + i*height) for i in range(N+1)]
    )

    # texts
    chosen_texts = set()  # don't allow repeated texts
    for i in range(N):
        box_left = left + i*width + 10
        for j in range(N):
            box_top = top + j*height + 10
            if (i,j) == ((N-1)/2, (N-1)/2):
                # free space
                text = config.FREE
            else:
                text = random.choice(list(set(config.TEXTS).difference(chosen_texts)))
                chosen_texts.add(text)
            P = _paragraph(text)
            w, h = P.wrap(width-20, height)
            P.drawOn(canv, box_left, box_top - h + 12 + 12)

    canv.showPage()


def generate_cards(config, num_cards):
    """Generate num_cards random bingo cards in a PDF file."""
    # initialize the PDF file
    c = Canvas("bingo_cards.pdf", pagesize=letter, bottomup=False)

    for i in range(num_cards):
        draw_card(c, config)
    c.save()

@click.command()
@click.argument("config_filename",)
@click.option("--num_cards", "-n", default=25, help="Number of cards to generate")
def main(config_filename, num_cards):
    # load the config file as a python module
    spec = importlib.util.spec_from_file_location('config', config_filename)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    generate_cards(config, num_cards)


if __name__ == "__main__":
    main()
