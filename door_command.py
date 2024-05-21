import argparse

from door_controller import move


def main(args):
    move(
        speed_rpm=args.speed_rpm,
        clockwise_direction=args.direction,
        duration_seconds=args.duration_seconds,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to move servo motor.")

    parser.add_argument("speed_rpm", type=float)
    parser.add_argument("direction", type=int)
    parser.add_argument("duration_seconds", type=float)

    args = parser.parse_args()

    main(args)
