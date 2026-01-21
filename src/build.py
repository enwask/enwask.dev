from functools import cached_property
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# Keeping it simple, so this is one (hopefully forever short) build script
# Builds templates with hardcoded data intake (sue me) and copies static
# assets and source files to dist.
# Also performs minification where possible (TODO).


class Data:
    """
    Organizational class for loaded dynamic data.
    """
    def __init__(self, root: Path) -> None:
        self.root = root

        # Ensure data directory exists
        self.data = root / 'data'
        self.data.mkdir(exist_ok=True)

    @cached_property
    def works(self) -> list[dict]:
        """
        Load the works data from the data/works directory.
        """
        works_dir = self.data / 'works'
        works = []
        for work_file in works_dir.glob('*.yaml'):
            # For simplicity, just return the filename as title
            works.append({
                'title': work_file.stem.replace('_', ' ').title(),
                'url': f'work/{work_file.stem}',
                'tags': ['example', 'tag']
            })
        return works


# The Jinja2 environment, loaded when run as the main module
jinja_env: Environment = None  # type: ignore
template_data: Data = None  # type: ignore


def make_jinja_env(root: Path) -> Environment:
    """
    Initialize the Jinja2 environment for template rendering.
    """
    return Environment(
        loader=FileSystemLoader(root / 'src' / 'templates'),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True
    )


def visit_data_node(path: Path) -> None:
    """
    Visit a file or directory in the data directory.
    This handles the dispatch for dynamic content.

    Path may point to a file or directory.
    """
    pass


def build_template(root: Path, template_path: str, output: Path,
                   context: dict) -> None:
    """
    Build a template with the given context.
    """
    global jinja_env
    template = jinja_env.get_template(template_path)
    rendered = template.render(**context)

    with open(output, 'w', encoding='utf-8') as f:
        f.write(rendered)


def build_index(root: Path, dist: Path) -> None:
    """
    Build the index.html file.
    """

    # Collect parameters for the index page
    # TODO: Placeholder data
    context = {
        'works': [
            {
                'title': 'The Devito Project',
                'url': 'work/devito',
                'tags': ['DSLs', 'compilers', 'optimization']
            },
            {
                'title': 'Logic Networks',
                'url': 'work/logic-networks',
                'tags': ['modding', 'compilers', 'opengl']
            },
            {
                'title': 'Multitool',
                'url': 'work/multitool',
                'tags': ['modding', 'opengl']
            },
            {
                'title': 'The Last Shuttle',
                'url': 'work/the-last-shuttle',
                'tags': ['games', 'unreal engine']
            }
        ]
    }

    build_template(root, 'index.html', dist / 'index.html', context)


def build(root: Path, dist: Path) -> None:
    """
    Build into the dist directory.
    """
    static_src = root / 'src' / 'static'
    static_assets = root / 'assets'

    # Delete the dist directory if it exists
    if dist.exists():
        shutil.rmtree(dist)

    # Create the dist directory as a copy of the static source
    shutil.copytree(static_src, dist, symlinks=True)

    # Copy static assets into the dist directory
    shutil.copytree(static_assets, dist / 'assets', symlinks=True)

    # Build data
    data_dir = root / 'data'
    for item in data_dir.iterdir():
        visit_data_node(item)

    # Build index.html
    build_index(root, dist)


if __name__ == '__main__':
    project_root = Path(__file__).parent.parent
    dist_dir = project_root / 'dist'

    # Initialize Jinja2 template rendering environment
    jinja_env = make_jinja_env(project_root)
    template_data = Data(project_root)

    build(project_root, dist_dir)
