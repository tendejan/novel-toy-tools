from novel_toy_tools.interfaces.abstract_renderer import AbstractRenderer
from novel_toy_tools.src.slow_rendition import SlowRendition
#TODO may want to use the abstract class here
from novel_toy_tools.src.wavefront_novel_toy import WavefrontNovelToy

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from scipy.spatial.transform import Rotation

class OpenGlRenderer(AbstractRenderer):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self._initialize_glut()
        self.vertices = None
        self.normals = None
        self.faces = None
        super().__init__()

    def _initialize_glut(self):
        """Initialize GLUT and create a hidden window once"""
        glutInit()
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        # Create window with a unique title to ensure we can find it later
        self.window = glutCreateWindow("OpenGL Render Context")
        
        # Initialize OpenGL context
        glEnable(GL_DEPTH_TEST)
        gluPerspective(45, self.width / self.height, 0.1, 1000.0)
        glTranslatef(0.0, 0.0, -400)
        
        # Setup lighting once
        self.setup_lighting()
        
        # Setup material properties once
        grey_color = [1.0, 1.0, 1.0, 1.0]
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, grey_color)

    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        light_position = [0.0, 400.0, 400.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        diffuse_light = [1.0, 1.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)

        ambient_light = [0.25, 0.25, 0.25, 1.0]
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)

    def scipy_rotation_to_axis_angle(self, rotation:Rotation):
        """convert the scipy rotation object into axis angel format"""
        rot_vec = rotation.as_rotvec()
        angle_degrees = np.degrees(np.linalg.norm(rot_vec))

        #normalization step
        if np.linalg.norm(rot_vec) > 1e-6:
            axis = rot_vec/ np.linalg.norm(rot_vec)
        else:
            axis = np.array([1.0, 0.0, 0.0]) #default to x if no rot
        return angle_degrees, *axis

    def draw_object(self, vertices, normals, faces):
        glBegin(GL_TRIANGLES)
        for face in faces:
            for vertex, normal in face:
                glNormal3fv(normals[normal])
                glVertex3fv(vertices[vertex])
        glEnd()

    #TODO this is loading the object numerous times and then applying a new rotation
    #TODO it would likely be faster to only load a new object when presented and to appy rotations by rotating then unrotating
    #TODO alternatively this could be completely parallelized if I new more about graphics computing pipelines
    #TODO may want to use the abstract novel toy here
    def render_single_view(self, novel_toy:WavefrontNovelToy, rotation:Rotation):
        """Render a single view using the existing GLUT window"""
        # Make our window current
        glutSetWindow(self.window)
        self.vertices, self.normals, self.faces = novel_toy.vertices, novel_toy.normals, novel_toy.faces
        
        # Clear the buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Apply rotation
        theta, x, y, z = self.scipy_rotation_to_axis_angle(rotation)
        glPushMatrix()
        glRotatef(theta, x, y, z)
        
        # Draw the object
        self.draw_object(self.vertices, self.normals, self.faces)
        
        # Reset transformation
        glPopMatrix()
        
        # Swap buffers to ensure all commands are executed
        glutSwapBuffers()

    def generate_rendition(self, novel_toy:WavefrontNovelToy, rotation:Rotation) -> SlowRendition:
        #TODO think about the implementation here
        self.render_single_view(novel_toy, rotation)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (self.width, self.height), data)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip the image vertically

        return SlowRendition(rendition_image=image)
        

    def __del__(self):
        """Cleanup GLUT resources when the object is destroyed"""
        if hasattr(self, 'window'):
            glutDestroyWindow(self.window)