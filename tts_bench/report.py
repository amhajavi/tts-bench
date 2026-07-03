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

    if len(results['models']) == 0:
        raise ValueError("No results to generate report.")
    
    model_reports = {}

    single_template = env.get_template("single_model_report.html")
    
    for result in results['records']:
        single_model_html = single_template.render(result=result)
        model_name = result['model']
        output_file = Path(output_path) / f"{model_name}_report.html"
        with open(output_file, "w") as f:
            f.write(single_model_html)
        model_reports.update({model_name: f"{model_name}_report.html"})
    
    comparison_template = env.get_template("comparison_report.html")    
    comparison_html = comparison_template.render(results=results, model_reports=model_reports)

    output_file = Path(output_path) / "index.html"
    with open(output_file, "w") as f:
        f.write(comparison_html)

    # Copy style file to output directory
    output_dir = Path(output_path)
    assets_src = script_path / "templates/assets/style.css"
    assets_dst = output_dir / "assets/style.css"
    if assets_src.exists():
        assets_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(assets_src, assets_dst)

    