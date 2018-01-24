import os

from setuptools_scm import trace, _do_parse, format_version, dump_version


def get_version(root='.',
                version_scheme='guess-next-dev',
                local_scheme='node-and-date',
                write_to=None,
                write_to_template=None,
                relative_to=None,
                parse=None,
                ):
    """
    If supplied, relative_to should be a file from which root may
    be resolved. Typically called by a script or module that is not
    in the root of the repository to direct setuptools_scm to the
    root of the repository by supplying ``__file__``.
    """
    if relative_to:
        root = os.path.join(os.path.dirname(relative_to), root)
    root = os.path.abspath(root)
    trace('root', repr(root))

    parsed_version = _do_parse(root, parse)

    if parsed_version:
        version_string = format_version(
            parsed_version,
            version_scheme=version_scheme,
            local_scheme=local_scheme)
        dump_version(
            root=root,
            version=version_string,
            write_to=write_to,
            template=write_to_template)

        return version_string
