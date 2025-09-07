# Task 2: Draw a Koch snowflake using recursion with debug and fast render options.

import argparse
import turtle
import sys

# Global-ish counters for simple debugging
segments_drawn = 0

def koch_curve(t, length, level, debug=False, progress=200, batch_update=None):
    """Draw a single Koch curve segment."""
    global segments_drawn

    if level == 0:
        t.forward(length)
        segments_drawn += 1

        # Progress logging
        if debug and progress > 0 and (segments_drawn % progress == 0):
            print(f"[DEBUG] Segments drawn: {segments_drawn}")

        # Batched screen updates for speed
        if batch_update and (segments_drawn % batch_update == 0):
            turtle.update()
        return

    third = length / 3.0
    koch_curve(t, third, level - 1, debug, progress, batch_update)
    t.left(60)
    koch_curve(t, third, level - 1, debug, progress, batch_update)
    t.right(120)
    koch_curve(t, third, level - 1, debug, progress, batch_update)
    t.left(60)
    koch_curve(t, third, level - 1, debug, progress, batch_update)

def koch_snowflake(t, length, level, debug=False, progress=200, batch_update=None):
    """Draw a full Koch snowflake (equilateral triangle with Koch edges)."""
    for _ in range(3):
        koch_curve(t, length, level, debug, progress, batch_update)
        t.right(120)

def expected_segments(level):
    """Return theoretical number of forward moves for the full snowflake."""
    return 3 * (4 ** level)

def main():
    parser = argparse.ArgumentParser(description="Draw a Koch snowflake using recursion.")
    parser.add_argument("--level", type=int, default=3, help="Recursion level (default: 3)")
    parser.add_argument("--length", type=float, default=300.0,
                        help="Side length of the base triangle (default: 300)")
    parser.add_argument("--debug", action="store_true",
                        help="Enable console progress logs (default: off)")
    parser.add_argument("--progress", type=int, default=200,
                        help="Print progress every N segments when --debug (default: 200)")
    parser.add_argument("--fast", action="store_true",
                        help="Use fast rendering (disable tracer and batch updates)")
    parser.add_argument("--batch", type=int, default=200,
                        help="Batch size for screen updates when --fast (default: 200)")
    parser.add_argument("--no-gui", action="store_true",
                        help="Dry run: compute and print expected segment count without drawing")
    args = parser.parse_args()

    # Quick verification without drawing
    if args.no_gui:
        print(f"[INFO] Expected segments at level {args.level}: {expected_segments(args.level)}")
        return

    screen = turtle.Screen()
    screen.title(f"Koch Snowflake (level={args.level})")

    if args.fast:
        # Turn off automatic updates; we will call turtle.update() manually
        turtle.tracer(False)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)  # Fastest drawing

    # Position turtle so the snowflake is roughly centered
    t.penup()
    t.goto(-args.length / 2.0, args.length / 3.0)
    t.pendown()

    # Draw with debug/fast settings
    global segments_drawn
    segments_drawn = 0
    total_expected = expected_segments(args.level)
    if args.debug:
        print(f"[INFO] Expected segments: {total_expected}")

    koch_snowflake(t, args.length, args.level,
                   debug=args.debug,
                   progress=args.progress,
                   batch_update=(args.batch if args.fast else None))

    # Final update to flush any remaining batches
    if args.fast:
        turtle.update()

    if args.debug:
        print(f"[INFO] Done. Segments drawn: {segments_drawn} (expected {total_expected}).")

    # Keep window open until closed by user
    turtle.done()

if __name__ == "__main__":
    sys.exit(main())
