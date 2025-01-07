import numpy as np
import quaternion
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import LightSource
import trimesh
from scipy.spatial.transform import Rotation
from novel_toy_tools.core.view_renderer import ViewRenderer

# TODO mark part of this code as gpt generated
#TODO also get rid of this it is pitifully slow

class PyPlotViewRenderer(ViewRenderer):
    def render_all_views(self, object_path, euler_angles, output_path):
        self.load_toy_mesh(object_path) #TODO implement the rendering here
        return super().render_views(object_path, euler_angles, output_path)
    
    def load_toy_mesh(self, object_path):
        self.mesh = trimesh.load_mesh(object_path)

    def render_view(self, object_path, euler_angle:tuple, output_file):
        self.load_toy_mesh(object_path)
        mesh_copy:trimesh.Trimesh = self.mesh.copy()
        rotation = Rotation.from_euler('xyz', euler_angle, degrees=True).as_matrix()
        #TODO investigate this
        mesh_copy.apply_transform(np.eye(4)) #reset to origin?

        mesh_copy.apply_transform(np.pad(rotation, ((0, 1), (0,1)), mode='constant', constant_values=0))

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.axis('off')

        for face in mesh_copy.faces:
            tri = mesh_copy.vertices[face]
            ax.add_collection3d(Poly3DCollection([tri], alpha=1.0, facecolor='gray', edgecolor='gray')) #TODO edges may need to be a different color
        
        scale = mesh_copy.vertices.flatten()
        ax.auto_scale_xyz(scale, scale, scale)

        plt.savefig(output_file, format='png', bbox_inches='tight', pad_inches=0, dpi=300)
        plt.close(fig)

if __name__ == "__main__":
    #TODO take args with argparse and make this usable as a script from cli, maybe push this up to the interface
    
    pass