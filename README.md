# MakerLabels Documentation

## Table of Contents
- [Overview](#overview)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Code Structure](#code-structure)
- [Adding New Features](#adding-new-features)
- [Future Development and Contributions](#future-development-and-contributions)

## Overview
MakerLabels is a Python script designed for creating customizable labels for various components. It's particularly useful in the context of electronics, filaments, nuts, bolts, and similar items. The script allows for extensive customization through templates, elements, and components.

## Setup Instructions
### Prerequisites
- Python 3.x
- reportlab library
- Optional: QR Code support (`qrcode` and `Pillow` libraries)
### Installation
1. Clone the repository: `git clone https://github.com/xtraorange/MakerLabels.git`
2. Navigate to the directory: `cd MakerLabels`
3. Install dependencies: `pip install reportlab`
4. For QR code support: `pip install qrcode Pillow`

## Usage Guide
To generate labels using MakerLabels:
1. Configure `GenerateLabels.py` according to your needs.
2. Run the script: `python GenerateLabels.py`
3. The labels will be generated based on the specified configurations.

### Generating Zach Poff/Martin Stumpf Labels
The original idea (and fork) for this project came from another project (details below) from Martin Stumpf.  You can mimic his labels using the template created for this.
- This template replicates the style and layout of their original labels, offering a familiar and proven design for various components.
- To use this template, select the `MartinStumpfTemplate` in the script configuration and adjust the settings according to your labeling needs.

## Code Structure
### Elements
Elements are the basic units of label design, representing text, images, or shapes.  Elements can have other elements within them.
#### Example
- `TextElement`: Defines text characteristics like font, size, and content.

### Templates
Templates are the blueprint for label layouts, organizing elements into a cohesive design.  Templates can have other templates within them.
#### Example
- `ResistorLabelTemplate`: A template for resistor labels, arranging elements specific to resistors.

### Components
Components are abstractions of real-world objects, making label creation more intuitive.
#### Example
- `ResistorComponent`: Represents a resistor and its properties like resistance value and tolerance.

## Adding New Features
### Adding New Templates
1. Create a `.py` file in the `templates` directory.
2. Define the layout using existing elements or create new ones.
3. Specify positioning, sizing, and styling for each element in the template.
### Adding New Elements
1. Add a new `.py` file in the `elements` directory.
2. Code the element's properties, including type (text, image, shape), dimensions, and style attributes.
### Adding New Components
1. Add a `.py` file in the `components` directory.
2. Define the component's properties, including any specific label requirements and data representations.

## Future Development
- [ ] Expand the range of templates for different types of labels.
- [ ] Introduce more elements for greater design versatility.
- [ ] Add new components to represent a wider variety of real-world objects.
- [ ] Develop a command-line interface for easier and faster label generation.


## Contribution Guidelines
1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and commit them.
4. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Original project forked and loosely based on [Finomnis/ResistorLabels](https://github.com/Finomnis/ResistorLabels).
- The original project was based on an idea from Zach Poff.

For more details on how to use these labels, visit his website:
https://www.zachpoff.com/resources/quick-easy-and-cheap-resistor-storage/