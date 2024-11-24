import os
import pandas as pd
from datetime import datetime
import webbrowser

base_dir_analysis = '/Users/havish/havishponnaganti/scrape_data/analysis'
base_dir_data = '/Users/havish/havishponnaganti/scrape_data/data'

csv_paths = [
    os.path.join(base_dir_analysis, 'analytics.csv'),
    os.path.join(base_dir_analysis, 'rankings', 'highest_rated_top_10.csv'),
    os.path.join(base_dir_analysis, 'rankings', 'least_expensive_top_10.csv'),
    os.path.join(base_dir_analysis, 'rankings', 'least_purchased_top_10.csv'),
    os.path.join(base_dir_analysis, 'rankings', 'lowest_rated_top_10.csv'),
    os.path.join(base_dir_analysis, 'rankings', 'most_expensive_top_10.csv'),
    os.path.join(base_dir_analysis, 'rankings', 'most_purchased_top_10.csv'),
    os.path.join(base_dir_analysis, 'data_with_sentiments.csv'),
    os.path.join(base_dir_analysis, 'advanced_analysis', 'recommendations.csv'),
    os.path.join(base_dir_data, 'data.csv')
]

image_paths = [
    os.path.join(base_dir_analysis, 'advanced_analysis', 'forecast_plot.png'),
    os.path.join(base_dir_analysis, 'advanced_analysis', 'shap_summary_plot.png'),
    os.path.join(base_dir_analysis, 'advanced_analysis', 'price_rating_prediction_plot.png'),
    os.path.join(base_dir_analysis, 'advanced_analysis', 'correlation_analysis_price_rating.png'),
    os.path.join(base_dir_analysis, 'advanced_analysis', 'product_clusters.png')
]

def make_links_clickable(df):
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].str.startswith('http').any():
            df[col] = df[col].apply(lambda x: f'<a href="{x}">{x}</a>' if pd.notnull(x) and x.startswith('http') else x)
    return df

def generate_html_report(csv_paths, image_paths, report_name='analysis_report.html'):
    html_content = """
    <html>
        <head>
            <title>Comprehensive Data Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.3; }
                h2, h3 { margin-bottom: 10px; }
                .data-table { margin: 10px auto; width: 90%; text-align: center; }
                img { margin: 20px auto; display: block; }
                .toc { margin-bottom: 20px; }
                .toc a { display: block; margin: 5px 0; text-decoration: none; color: blue; }
            </style>
        </head>
        <body>
    """
    html_content += "<h1>Comprehensive Data Analysis Report</h1>"
    html_content += f"<p>Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
    html_content += "<div class='toc'><h2>Table of Contents</h2><ul>"
    
    for csv_path in csv_paths:
        if os.path.exists(csv_path):
            file_name = os.path.basename(csv_path)
            section_id = file_name.replace(' ', '_').replace('.', '_')
            html_content += f"<li><a href='#{section_id}'>{file_name.replace('_', ' ').title()}</a></li>"
    
    html_content += "<li><a href='#graphs'>Graphs and Visualizations</a></li>"
    html_content += "</ul></div>"

    for csv_path in csv_paths:
        if os.path.exists(csv_path):
            file_name = os.path.basename(csv_path)
            section_id = file_name.replace(' ', '_').replace('.', '_')
            df = pd.read_csv(csv_path)
            df = make_links_clickable(df)
            
            html_content += f"<h2 id='{section_id}'>{file_name.replace('_', ' ').title()}</h2>"
            html_content += f"<div class='data-table'>{df.head(10).to_html(index=False, escape=False, border=1)}</div>"

    html_content += "<h2 id='graphs'>Graphs and Visualizations</h2>"
    
    for image_path in image_paths:
        if os.path.exists(image_path):
            img_name = os.path.basename(image_path).replace('_', ' ').title()
            html_content += f"<h3>{img_name}</h3>"
            html_content += f"<img src='{image_path}' alt='{img_name}' style='max-width: 90%; height: auto;'>"

    html_content += "</body></html>"

    with open(report_name, 'w', encoding='utf-8') as report_file:
        report_file.write(html_content)

    webbrowser.open(f'file://{os.path.abspath(report_name)}')

generate_html_report(csv_paths, image_paths)
