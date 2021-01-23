from OpenGL.GL import *
from matutils import *
from material import Material
from BaseModel import BaseModel

class HairModel(BaseModel):
    """
    A simple hair model, which will be fed fur information to draw fur using Line Primitives
    """

    def __init__(self, scene, vertices, normals, M=poseMatrix(), primitive=GL_LINES, material=None):
        """
        :param scene: reference to the scene the model is instantiated in
        :param vertices: model vertices read from obj file
        :param normals: model normals read from obj file
        :param M:position matrix
        :param material:
        :param primitive:
        """

        BaseModel.__init__(self, scene=scene, M=M,
                           primitive=primitive, visible=True)

        # initialize the vertices/normals/indices of the shape
        self.vertices = vertices
        self.normals = normals
        self.indices = None

        # set position and other attributes necessary for drawing
        self.vertex_colors = np.zeros((self.vertices.shape[0], 3), dtype='f')

        # override the default material
        self.material = Material(
            Ka=np.array([0.0, 0.0, 0.0], 'f'),
            Kd=np.array([0.5, 0.5, 0.5], 'f'),
            Ks=np.array([1.0, 1.0, 1.0], 'f'),
            Ns=10.0
            )

