from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import quaternion
from PIL import Image
from novel_toy_tools.core.view_renderer import ViewRenderer

# TODO remove the selfs from some of the functions here

class OpenGLViewRenderer(ViewRenderer):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        super().__init__()

    def render_all_views(self, object_path, euler_angles, output_path):
        # TODO implement this
        return super().render_all_views(object_path, euler_angles, output_path)

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


    def render_single_view(self, obj_filename, rotation, output_filename):
        width, height = 800, 600
        glutInit()
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutCreateWindow("OpenGL Render")

        glEnable(GL_DEPTH_TEST)
        gluPerspective(45, width / height, 0.1, 1000.0)
        glTranslatef(0.0, 0.0, -400)

        vertices, normals, faces = self.load_obj(obj_filename)
        self.setup_lighting()

        grey_color = [1.0, 1.0, 1.0, 1.0]
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, grey_color)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        theta, x, y, z = self.quat_to_axis_angle(rotation)
        glPushMatrix()
        glRotatef(theta, x, y, z)
        self.draw_object(vertices, normals, faces)
        glPopMatrix()

        self.save_framebuffer_to_png(output_filename)
        print(f"Saved rendered image to {output_filename}")
        glutDestroyWindow(glutGetWindow())