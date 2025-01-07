from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import quaternion
from PIL import Image
from novel_toy_tools.core.view_renderer import ViewRenderer

class OpenGLViewRenderer(ViewRenderer):
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

    def render_all_views(self, object_path, euler_angles, output_path):
        # Load the object once
        self.vertices, self.normals, self.faces = self.load_obj(object_path)
        
        # Now render each view
        for i, rotation in enumerate(euler_angles):
            output_filename = f"{output_path}/view_{i:03d}.png"
            self.render_single_view(rotation, output_filename)
            
        return [f"view_{i:03d}.png" for i in range(len(euler_angles))]

    def load_obj(self, filename):
        vertices = []
        normals = []
        faces = []

        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.split()
                    vertex = list(map(float, parts[1:4]))
                    vertices.append(vertex)
                elif line.startswith('vn '):
                    parts = line.split()
                    normal = list(map(float, parts[1:4]))
                    normals.append(normal)
                elif line.startswith('f '):
                    parts = line.split()
                    face = []
                    for p in parts[1:]:
                        vals = p.split('/')
                        vertex_idx = int(vals[0]) - 1
                        normal_idx = int(vals[2]) - 1
                        face.append((vertex_idx, normal_idx))
                    faces.append(face)
        
        return np.array(vertices), np.array(normals), np.array(faces)

    def draw_object(self, vertices, normals, faces):
        glBegin(GL_TRIANGLES)
        for face in faces:
            for vertex, normal in face:
                glNormal3fv(normals[normal])
                glVertex3fv(vertices[vertex])
        glEnd()

    def quat_to_axis_angle(self, q: quaternion.quaternion):
        theta = 2 * np.arccos(q.w) * 180 / np.pi
        sin_theta = np.sqrt(1 - q.w ** 2)

        if sin_theta < 0.001:
            return theta, 1.0, 0.0, 0.0

        x = q.x / sin_theta
        y = q.y / sin_theta
        z = q.z / sin_theta

        return theta, x, y, z

    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        light_position = [0.0, 400.0, 400.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        diffuse_light = [1.0, 1.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)

        ambient_light = [0.25, 0.25, 0.25, 1.0]
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)

    def save_framebuffer_to_png(self, filename):
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (self.width, self.height), data)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip the image vertically
        image.save(filename)

    def render_single_view(self, object_path, rotation, output_filename):
        """Render a single view using the existing GLUT window"""
        # Make our window current
        glutSetWindow(self.window)
        self.vertices, self.normals, self.faces = self.load_obj(object_path)
        
        # Clear the buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Apply rotation
        theta, x, y, z = self.quat_to_axis_angle(rotation)
        glPushMatrix()
        glRotatef(theta, x, y, z)
        
        # Draw the object
        self.draw_object(self.vertices, self.normals, self.faces)
        
        # Reset transformation
        glPopMatrix()

        # Save the frame
        self.save_framebuffer_to_png(output_filename)
        
        # Swap buffers to ensure all commands are executed
        glutSwapBuffers()
        
    def __del__(self):
        """Cleanup GLUT resources when the object is destroyed"""
        if hasattr(self, 'window'):
            glutDestroyWindow(self.window)