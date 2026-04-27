# Python 3D Wireframe Engine

A lightweight, from-scratch 3D wireframe rendering engine built using Python. This project demonstrates the core mathematical principles behind 3D graphics, utilizing **Pygame** for screen rendering and **NumPy** for highly optimized, vectorized matrix transformations.

## Features

* **Vectorized Math Pipeline:** Uses NumPy arrays and matrix multiplication (`@`) to transform thousands of vertices simultaneously, completely avoiding slow CPU-bound `for` loops.
* **Standard Perspective Projection:** Implements a true perspective divide (x/z, y/z) for accurate 3D-to-2D screen projection with an adjustable Field of View (FOV).
* **Euler Angle Rotations:** Unified 3x3 matrix transformations for independent control over X, Y, and Z axis rotations.
* **Optimized `.obj` Loader:** A custom 3D model loader that intelligently parses `.obj` files and uses sets to cull duplicate edges, ensuring smooth and efficient wireframe rendering.
* **Procedural Geometry:** Built-in functions to generate customizable primitive shapes, including mathematically mapped spheres with adjustable latitude and longitude divisions.

## Prerequisites

To run this engine, you will need Python 3.x and the following libraries:

```bash
pip install pygame numpy
```

## Usage

1. Clone the repository and navigate to the project folder.
2. Run the main Python script:

```bash
python main.py
```

### Loading Custom 3D Models

To render your own 3D models, place your `.obj` file in the project directory and update the `get_object_from_file()` call in `main.py`:

```python
# Replace "plant.obj" with your file's name
nodes, lines = get_object_from_file("your_model.obj")
```

*Note: The engine currently renders wireframes. Ensure your `.obj` file is exported with vertices (`v`) and faces (`f`).*

## Configuration

You can easily tweak the engine's camera and projection settings at the top of `main.py`:

* **`SC_WIDTH` / `SC_HEIGHT`:** Adjusts the window resolution. The projection math automatically centers the camera based on these values.
* **`camera_pos`:** A list `[x, y, z]` representing the camera's location in 3D space.
* **`fov_factor`:** Located inside the `render_nodes` function, tweak this value to zoom in or out.

## Under the Hood

Unlike basic Python rendering scripts, this engine replicates the math pipeline used by professional graphics APIs (like OpenGL). 

1. **Model Space to World Space:** Vertices are multiplied by rotation matrices.
2. **World Space to Camera Space:** The camera's position is subtracted from the world nodes using vectorized array math.
3. **Projection:** Coordinates undergo a standard perspective divide to create the illusion of depth.