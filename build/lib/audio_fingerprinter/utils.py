#!/usr/bin/env python


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def print_flask(message):
    print(f"[Flask] {message}")
