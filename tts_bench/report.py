def generate_report(results: list[dict], output_path: str) -> None:
    lines = ["<html><body>"]
    for row in results:
        lines.append(f"<h2>{row['model']}</h2>")
        lines.append("<ul>")
        for metric, score in row["scores"].items():
            lines.append(f"  <li>{metric}: {score}</li>")
        lines.append("</ul>")
    lines.append("</body></html>")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))
