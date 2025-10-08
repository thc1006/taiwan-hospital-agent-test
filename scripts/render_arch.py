#!/usr/bin/env python
"""Generate a simple architecture diagram using matplotlib.

This implementation avoids dependencies on external Graphviz binaries by
using matplotlib primitives to draw a high‑level architecture diagram.
It creates a PNG under `docs/arch.png`.
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def draw_box(ax, xy, text):
    """Draw a rounded box with centred text."""
    x, y = xy
    width, height = 2.2, 0.8
    box = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.2",
        edgecolor="black",
        facecolor="white",
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=10)


def draw_arrow(ax, start, end, text=""):
    """Draw an arrow with optional label."""
    arrow = FancyArrowPatch(
        posA=start,
        posB=end,
        arrowstyle="->",
        mutation_scale=10,
        linewidth=1,
        color="black",
    )
    ax.add_patch(arrow)
    if text:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y + 0.1, text, ha="center", va="center", fontsize=8)


def render(output_path: str = "docs/arch.png") -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    # Define node positions
    positions = {
        "User": (1.0, 2.5),
        "API": (3.5, 2.5),
        "Agent": (6.0, 3.5),
        "Tools": (6.0, 1.5),
        "S3": (8.5, 2.5),
    }
    labels = {
        "User": "User / Admin",
        "API": "API Gateway\nFastAPI / Lambda",
        "Agent": "Bedrock AgentCore",
        "Tools": "Tools (HTTP, SQL, ticket)",
        "S3": "S3 Bucket",
    }
    # Draw boxes
    for key, pos in positions.items():
        draw_box(ax, pos, labels[key])
    # Draw arrows with labels
    draw_arrow(ax, positions["User"], positions["API"], text="POST /run")
    draw_arrow(ax, positions["API"], positions["Agent"], text="invoke")
    draw_arrow(ax, positions["Agent"], positions["Tools"], text="tool calls")
    draw_arrow(ax, positions["Tools"], positions["S3"], text="store reports")
    # Save figure
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    print(f"Architecture diagram saved to {output_path}")


if __name__ == "__main__":
    render()