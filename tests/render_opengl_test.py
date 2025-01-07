
import os
from novel_toy_tools.implementations.render_opengl_quaternion import OpenGLViewRenderer
from novel_toy_tools.implementations.generate_SO3_quaternion_fib import generate_uniform_rotations, check_coverage_metrics
import quaternion

raw_obj_path = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/tests/BlockGiraffe.obj"
raw_out_path = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/tests/null_test/"

#TODO create better test cases for this

objectpath = os.path.normpath(raw_obj_path)

NUM_SAMPLES = 1000

rotations = generate_uniform_rotations(num_samples=NUM_SAMPLES)
print(check_coverage_metrics(rotations))

renderer = OpenGLViewRenderer(600, 800)

i = 0
for quat in rotations:
    outpath = os.path.join(raw_out_path, f"view_{i}.png")
    renderer.render_single_view(raw_obj_path, quat, outpath)
    i+=1

