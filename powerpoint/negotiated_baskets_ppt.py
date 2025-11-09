from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.shapes import MSO_CONNECTOR

p = Presentation()
p.slide_width = Inches(16)
p.slide_height = Inches(9)

# Title Slide
slide = p.slides.add_slide(p.slide_layouts[0])
slide.shapes.title.text = "Negotiated Baskets Trading Application"
slide.placeholders[1].text = "High-Level Specification"

# Application Overview
slide = p.slides.add_slide(p.slide_layouts[1])
slide.shapes.title.text = "Application Overview"
content = slide.placeholders[1]
content.text = (
    "Streamlines negotiating baskets of securities.\n"
    "Spreadsheet-like workflow for traders."
)

# System Architecture
slide = p.slides.add_slide(p.slide_layouts[1])
slide.shapes.title.text = "System Architecture"
content = slide.placeholders[1]
content.text = (
    "Technologies: Python (backend), Vue.js (frontend), IKIT and Markit (remote DB).\n"
    "External Systems: Bloomberg (market data), Markit (reference data), IKIT (logged data)."
)

# Inputs & Outputs Slide
slide = p.slides.add_slide(p.slide_layouts[1])
slide.shapes.title.text = "Inputs & Outputs"
content = slide.placeholders[1]
content.text = (
    "Inputs:\n"
    " Inventory: user may paste data or upload as CSV file\n"
    " Bloomberg: fetches unheld security data and for updating with market data (real-time or daily)\n"
    " Markit: provides held security reference details—daily updates are sufficient\n"
    "\n"
    "Outputs:\n"
    " Basket file: final ISINs and corresponding weights ready for execution"
)

# User Interface Concept
slide = p.slides.add_slide(p.slide_layouts[1])
slide.shapes.title.text = "User Interface Concept"
content = slide.placeholders[1]
content.text = (
    "Spreadsheet-like grid (Excel users).\n"
    "Filtering by attributes (sector, issuer, etc.).\n"
    "Highlighting flagged items.\n"
    "Hiding unused columns\n"
    "Parameterizable fields, locked reference data."
)

# Backend Modules slide
slide = p.slides.add_slide(p.slide_layouts[1])
slide.shapes.title.text = "Backend Modules Overview"
content = slide.placeholders[1]
content.text = (
    "Core backend modules for the application:\n"
    " Database:\n"
    "  - Security master: inventory, reference fund, model fund\n"
    "  - Logging: actions, data changes\n"
    " Inventory uploader:\n"
    "  - Supports pastable form fields and CSV upload\n"
    " Basket file downloader:\n"
    "  - Exports final basket (ISINs/weights) for execution\n"
    " Portfolio shape:\n"
    "  - User-editable model weights, reference weights, calculated differences\n"
    " Constraint tables:\n"
    "  - User sets filters and rules to include/exclude securities\n"
)

# Workflow Visualization Slide (diagrammatic)
slide = p.slides.add_slide(p.slide_layouts[5])  # blank layout for diagram
slide.shapes.title.text = "Application Workflow Overview"

workflow_boxes = [
    {"label": "Inputs:\nInventory\n(BBG, Markit)", "x": 0.5, "y": 2},
    {"label": "Security Master Table", "x": 3, "y": 2},
    {"label": "Portfolio Shape & Constraints", "x": 6, "y": 2},
    {"label": "Basket File Output (CSV)", "x": 9, "y": 2}
]

# Add rectangles as process boxes
for b in workflow_boxes:
    box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(b["x"]), Inches(b["y"]),
        Inches(2.2), Inches(1.1)
    )
    box.text = b["label"]

# Add left-to-right connectors between the boxes
for i in range(len(workflow_boxes) - 1):
    start_x = workflow_boxes[i]["x"] + 2.2
    start_y = workflow_boxes[i]["y"] + 0.55
    end_x = workflow_boxes[i+1]["x"]
    end_y = workflow_boxes[i+1]["y"] + 0.55

    slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(start_x), Inches(start_y),
        Inches(end_x), Inches(end_y)
    )

# Next Steps / Open Questions
slide = p.slides.add_slide(p.slide_layouts[1])
slide.shapes.title.text = "Next Steps / Open Questions"
content = slide.placeholders[1]
content.text = (
    "Review with stakeholders.\n"
    " Does the workflow make sense?\n"
    " Is this approach scalable and aligned with institutional goals?\n"
    "Confirm UI requirements, including:\n"
    " Research spreadsheet-like workflow options: Jspreadsheet, DHTMLX, Webix\n"
    " Schedule UI design meeting\n"
)

p.save("negotiated_baskets_spec.pptx")
