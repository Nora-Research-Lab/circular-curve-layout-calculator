import gradio as gr
from circular_curve_layout_calculator import (
    compute_curve,
    parse_station_error,
    format_station,
    DEFAULT_INTERVAL_METERS,
    DEFAULT_INTERVAL_FEET
)
import tempfile
import os

def process_input(delta, radius, unit, pi_station, interval):
    try:
        if not delta or delta <= 0 or delta >= 180:
            return "Error: Intersection angle (Δ) must be between 0 and 180 degrees.", "", None
        if not radius or radius <= 0:
            return "Error: Radius must be positive.", "", None
        if not pi_station or pi_station.strip() == "":
            return "Error: PI station is required.", "", None
        # Use provided interval or default based on unit
        if interval is None or interval <= 0:
            if unit == "meters":
                interval = DEFAULT_INTERVAL_METERS
            else:
                interval = DEFAULT_INTERVAL_FEET
        result = compute_curve(delta, radius, unit, pi_station.strip(), interval)
        # Build summary text
        summary = (
            f"Intersection Angle (Δ): {result['delta_deg']:.2f}°\n"
            f"Radius (R): {result['radius']:.2f} {unit}\n"
            f"Tangent Length (T): {result['T']:.2f} {unit}\n"
            f"Curve Length (L): {result['L']:.2f} {unit}\n"
            f"Chord Length (C): {result['C']:.2f} {unit}\n"
            f"External Distance (E): {result['E']:.2f} {unit}\n"
            f"Mid-ordinate (M): {result['M']:.2f} {unit}\n"
            f"Station PC: {result['pc_station']} {unit}\n"
            f"Station PT: {result['pt_station']} {unit}\n"
        )
        # Build HTML table for layout
        layout = result['layout']
        html = """
        <table style='width:100%; border-collapse: collapse;'>
            <tr style='background-color: #f2f2f2;'>
                <th style='border: 1px solid #ddd; padding: 8px;'>Station</th>
                <th style='border: 1px solid #ddd; padding: 8px;'>Deflection Angle (°)</th>
                <th style='border: 1px solid #ddd; padding: 8px;'>Chord Distance (unit)</th>
            </tr>
        """
        for item in layout:
            html += f"""
            <tr>
                <td style='border: 1px solid #ddd; padding: 8px;'>{item['station']}</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{item['deflection_deg']:.2f}</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{item['chord_distance']:.2f}</td>
            </tr>
            """
        html += "</table>"
        # Prepare CSV data for download
        csv_lines = ["Station,Deflection Angle (deg),Chord Distance (unit)"]
        for item in layout:
            csv_lines.append(f"{item['station']},{item['deflection_deg']:.2f},{item['chord_distance']:.2f}")
        csv_content = "\n".join(csv_lines)
        # Write temporary CSV file
        tmp = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8')
        tmp.write(csv_content)
        tmp.close()
        return summary, html, tmp.name
    except Exception as e:
        return f"Error: {str(e)}", "", None

with gr.Blocks(title="Circular Curve Layout Calculator") as demo:
    gr.HTML("<h1 style='text-align:center;'>Circular Curve Layout Calculator</h1>")
    gr.HTML("<p style='text-align:center;'>Compute the full geometric layout of a horizontal circular curve for route surveying.</p>")
    # Placeholder image banner
    gr.HTML("<div style='text-align:center;'><img src='https://via.placeholder.com/600x100.png?text=Curve+Layout+Banner' alt='Banner' style='max-width:100%;'></div>")
    with gr.Row():
        with gr.Column(scale=1):
            delta_input = gr.Number(label="Intersection Angle (Δ) [degrees]", minimum=0.001, maximum=179.999, step=0.01)
            radius_input = gr.Number(label="Radius (R)", minimum=0.001, step=0.01)
            unit_dropdown = gr.Dropdown(choices=["meters", "feet"], label="Unit", value="meters")
            pi_station_input = gr.Textbox(label="PI Station (format XX+YY.ZZ)", placeholder="12+45.67")
            interval_input = gr.Number(label="Layout Interval", minimum=0.001, step=0.01)
            # Set interval default dynamically based on unit
            def set_interval_default(unit):
                if unit == "meters":
                    return 10.0
                else:
                    return 25.0
            unit_dropdown.change(fn=set_interval_default, inputs=unit_dropdown, outputs=interval_input)
            submit_btn = gr.Button("Calculate")
        with gr.Column(scale=1):
            summary_output = gr.Textbox(label="Curve Summary", lines=12)
            layout_html = gr.HTML(label="Layout Table")
            download_btn = gr.File(label="Download CSV", file_types=[".csv"])
    submit_btn.click(
        fn=process_input,
        inputs=[delta_input, radius_input, unit_dropdown, pi_station_input, interval_input],
        outputs=[summary_output, layout_html, download_btn]
    )

demo.launch(server_name="0.0.0.0", server_port=7860)
