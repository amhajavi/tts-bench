import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def generate_report(results: list[dict], output_path: str) -> None:
    """
    Generate an HTML report from the given results and save it to the specified output path.

    Args:
        results (list[dict]): A list of dictionaries containing the results to be included in the report.
        output_path (str): The path where the generated HTML report will be saved.

    Raises:
        ValueError: If the results list is empty.
    """
    script_path = Path(__file__).parent

    env = Environment(loader=FileSystemLoader(script_path / "templates"))

    if len(results) == 0:
        raise ValueError("No results to generate report.")
    elif len(results) == 1:
        template = env.get_template("single_model_report.html")
        rendered_html = template.render(results=results[0])
    else:
        template = env.get_template("comparison_report.html")
        rendered_html = template.render(results=results)
    
    # Copy templates/assets folder to output directory
    output_dir = Path(output_path).parent
    assets_src = script_path / "templates/assets"
    assets_dst = output_dir / "assets"
    if assets_src.exists():
        if assets_dst.exists():
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst)

    with open(output_path, "w") as f:
        f.write(rendered_html)
    