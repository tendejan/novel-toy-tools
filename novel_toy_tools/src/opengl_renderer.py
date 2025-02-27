from novel_toy_tools.core.abstract_renderer import AbstractRenderer
from novel_toy_tools.src.rendition_viewer3d import RenditionViewer3d
#TODO may want to use the abstract class here
from novel_toy_tools.src.wavefront_novel_toy import WavefrontNovelToy

import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from scipy.spatial.transform import Rotation

class ObjectRenderer:
    def __init__(self, width=800, height=600):
        """
        Initialize the renderer with specified dimensions
        
        Args:
            width: Width of the rendering window in pixels
            height: Height of the rendering window in pixels
        """
        self.width = width
        self.height = height
        self.window = None
        self.initialized = False
        
        # Store model data
        self.vertices = None
        self.normals = None
        self.faces = None
        
        # Initialize OpenGL
        self._initialize_opengl()

    def _initialize_opengl(self):
        """Initialize GLUT and create a hidden window for rendering"""
        # Initialize GLUT
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        
        # Create a window with a unique title
        self.window = glutCreateWindow("3D Object Renderer")
        
        # Set up OpenGL context
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        # Setup projection
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / self.height, 0.1, 1000.0)
        
        # Setup modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -400)  # Move camera back
        
        # Setup lighting
        self._setup_lighting()
        
        # Setup material
        self._setup_material()
        
        self.initialized = True
        
        # Register a dummy display function to keep GLUT happy
        def dummy_display():
            pass
        
        glutDisplayFunc(dummy_display)

    def _setup_lighting(self):
        """Configure lighting for the scene"""
        # Light position
        light_position = [0.0, 400.0, 400.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        
        # Light color components
        diffuse_light = [1.0, 1.0, 1.0, 1.0]  # White diffuse light
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
        
        ambient_light = [0.25, 0.25, 0.25, 1.0]  # Soft ambient light
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
        
        # Optional: add specular component
        specular_light = [0.7, 0.7, 0.7, 1.0]
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)

    def _setup_material(self):
        """Configure default material properties"""
        # Set material color (white/gray)
        material_color = [0.8, 0.8, 0.8, 1.0]
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, material_color)
        
        # Optional: add specular reflection
        specular = [0.5, 0.5, 0.5, 1.0]
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

    def load_model(self, vertices, normals, faces):
        """
        Load a 3D model into the renderer
        
        Args:
            vertices: List of vertex coordinates (x, y, z)
            normals: List of normal vectors
            faces: List of faces, where each face contains tuples of (vertex_idx, normal_idx)
        """
        self.vertices = vertices
        self.normals = normals
        self.faces = faces

    def render(self, novel_toy:WavefrontNovelToy, rotation=None, background_color=(0.0, 0.0, 0.0, 1.0)):
        """
        Render the 3D model with the specified rotation
        
        Args:
            rotation: A scipy.spatial.transform.Rotation object or None
            background_color: RGBA tuple for background color
            
        Returns:
            PIL.Image: The rendered image
        """
        self.load_model(novel_toy.vertices, novel_toy.normals, novel_toy.faces)

        if not self.initialized:
            raise RuntimeError("Renderer not properly initialized")
            
        if self.vertices is None or self.normals is None or self.faces is None:
            raise ValueError("No model loaded. Call load_model() first")
        
        # Make our window current
        glutSetWindow(self.window)
        
        # Set background color
        glClearColor(*background_color)
        
        # Clear the buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Reset modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -400)  # Move camera back
        
        # Apply rotation if provided
        if rotation is not None:
            angle, axis = self._rotation_to_axis_angle(rotation)
            glRotatef(angle, *axis)
        
        # Draw the object
        self._draw_object()
        
        # Force OpenGL to finish all operations
        glFlush()
        glFinish()
        
        # Read pixels from framebuffer
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        
        # Convert to PIL Image and flip vertically (OpenGL's origin is bottom-left)
        image = Image.frombytes("RGB", (self.width, self.height), data)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        
        # Swap buffers to prevent artifacts in the window
        glutSwapBuffers()
        
        return image
    
    #TODO this is stupid but conform to the abstract class
    def generate_rendition(self, novel_toy, rotation):
        return self.render(novel_toy, rotation)

    def _rotation_to_axis_angle(self, rotation):
        """
        Convert a scipy.spatial.transform.Rotation to axis-angle representation
        
        Args:
            rotation: A scipy.spatial.transform.Rotation object
            
        Returns:
            tuple: (angle_in_degrees, [x, y, z]) where [x, y, z] is the normalized axis
        """
        # Get rotation vector (axis * angle)
        rot_vec = rotation.as_rotvec()
        
        # Calculate rotation angle in degrees
        angle = np.degrees(np.linalg.norm(rot_vec))
        
        # Get rotation axis (normalized rotation vector)
        if np.linalg.norm(rot_vec) > 1e-6:
            axis = rot_vec / np.linalg.norm(rot_vec)
        else:
            # Default to x-axis for very small rotations
            axis = np.array([1.0, 0.0, 0.0])
            
        return angle, axis

    def _draw_object(self):
        """Draw the 3D object using the loaded geometry"""
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex_idx, normal_idx in face:
                glNormal3fv(self.normals[normal_idx])
                glVertex3fv(self.vertices[vertex_idx])
        glEnd()

    def cleanup(self):
        """Clean up GLUT resources"""
        if self.window is not None:
            glutDestroyWindow(self.window)
            self.window = None
            self.initialized = False

    def __del__(self):
        """Destructor to ensure resources are cleaned up"""
        self.cleanup()
