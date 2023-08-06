import enum
import inspect
import sys
import types
import msgpack


def ser_type(ty):
    if ty is inspect._empty:
        return None
    if type(ty) is types.GenericAlias:
        return repr(ty)
    return getattr(ty, "__name__", "None")


def ser_kind(kind):
    if kind is inspect._empty:
        return None
    return int(kind)


def ser_value(val):
    if val is inspect._empty:
        return None
    return repr(val)


def ser_parameter(param):
    return {
        "name": param.name,
        "default": ser_value(param.default),
        "kind": ser_kind(param.kind),
        "type": getattr(param.annotation, "__name__", "None"),
        "annotation": ser_type(param.annotation)
    }


def count_leading_spaces(line):
    n = 0
    for c in line:
        if c == ' ':
            n += 1
        else:
            return n
    return sys.maxsize


def parse_doc(doc: str):
    if doc is None:
        return
    lines = doc.strip().splitlines()
    indent = min(map(count_leading_spaces, lines))
    lines = [l[indent:].rstrip() for l in lines]

    return '\n'.join(lines)


def parse_func(func):
    sign = inspect.signature(func)
    return {
        "doc": parse_doc(func.__doc__),
        "meta": getattr(func, "__lev_meta__", {}),
        "signature": str(sign),
        "parameters": tuple(map(ser_parameter, sign.parameters.values()))
    }


def parse_module(module):
    modes = {
        mode: parse_func(getattr(module, mode))
        for mode in module.__modes__
    }
    return {
        "doc": parse_doc(module.__doc__),
        "meta": getattr(module, "__lev_meta__", {}),
        "modes": modes,
    }


def parse(project):
    from site import getsitepackages
    from subprocess import check_output

    module = project.meta.name
    msl = check_output([
        "pdm", "run", "python", __file__, module,
        str(project.root), *getsitepackages()
    ])
    return msgpack.loads(msl)


def main(project, *python_paths):
    import importlib
    import inspect

    sys.path.extend(python_paths)
    module = importlib.import_module(project)

    kits = {}
    funcs = {}

    exports = getattr(module, "__exports__", ())
    exports = exports or getattr(module, "__all__", ())
    for name in exports:
        try:
            attr = getattr(module, name)
            if inspect.ismodule(attr):
                kits[name] = parse_module(attr)
            elif inspect.iscoroutinefunction(attr):
                funcs[name] = parse_func(attr)
            elif inspect.isfunction(attr):
                kits[name] = parse_func(attr)
        except Exception as e:
            print(f"parse <{name}> failed", file=sys.stderr)
            raise e

    return {"kits": kits, "funcs": funcs}


def encoder(obj):
    if inspect.isclass(obj):
        return obj.__name__
    if isinstance(obj, enum.Enum):
        return obj.value
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(type(obj), obj)


if __name__ == "__main__":
    import sys

    ret = main(*sys.argv[1:])
    msg: bytes = msgpack.dumps(ret, default=encoder)  #type: ignore
    sys.stdout.buffer.write(msg)
