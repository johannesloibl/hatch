from hatch.template import File
from hatch.utils.fs import Path
from hatchling.__about__ import __version__
from hatchling.metadata.spec import DEFAULT_METADATA_VERSION

from ..new.feature_no_src_layout import get_files as get_template_files
from .utils import update_record_file_contents


def get_files(**kwargs):
    metadata_directory = kwargs.get('metadata_directory', '')
    namespace_package = kwargs['namespace']

    files = []
    for f in get_template_files(**kwargs):
        if str(f.path) == 'LICENSE.txt':
            files.append(File(Path(metadata_directory, 'licenses', f.path), f.contents))

        if f.path.parts[0] != kwargs['package_name']:
            continue

        f.path = Path(namespace_package, f.path)
        files.append(f)

    files.extend((
        File(
            Path(metadata_directory, 'WHEEL'),
            f"""\
Wheel-Version: 1.0
Generator: hatchling {__version__}
Root-Is-Purelib: true
Tag: py2-none-any
Tag: py3-none-any
""",
        ),
        File(
            Path(metadata_directory, 'METADATA'),
            f"""\
Metadata-Version: {DEFAULT_METADATA_VERSION}
Name: {kwargs['project_name']}
Version: 0.0.1
""",
        ),
    ))

    record_file = File(Path(metadata_directory, 'RECORD'), '')
    update_record_file_contents(record_file, files)
    files.append(record_file)

    return files
