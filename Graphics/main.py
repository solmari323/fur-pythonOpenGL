# Main program file used to run the scene

# Import needed modules
from scene import Scene
from blender import load_obj_file, Mesh
from BaseModel import *
from FurUtil import FurUtils


class DrawModelFromMesh(BaseModel):
	'''
	Base class for all models, inherit from this to create new models
	'''

	def __init__(self, scene, M, mesh):
		'''
		Initialises the model data
			:param scene: scene to which model will be viewed
		'''

		BaseModel.__init__(self, scene=scene, M=M),


		# initialises the vertices of the shape
		self.vertices = mesh.vertices
		self.indices = mesh.faces

		if self.indices.shape[1] == 3:
			self.primitive = GL_TRIANGLES

		elif self.indices.shape[1] == 4:
			self.primitive = GL_QUADS

		else:
			print('(E) Error: Mesh should have 3 or 4 vertices per face!')

		# initialise the normals per vertex
		self.normals = mesh.normals

		# and save the material information
		self.material = mesh.material

		# we force a bit of specularity to make it more visible
		self.material.Ns = 15.0

		# and we check which primitives we need to use for drawing
		if self.indices.shape[1] == 3:
			self.primitive = GL_TRIANGLES

		elif self.indices.shape[1] == 4:
			self.primitive = GL_QUADS

		else:
			print('(E) Error in DrawModelFromObjFile.__init__(): index array must have 3 (triangles) or 4 (quads) columns, found {}!'.format(self.indices.shape[1]))
			raise

		# default vertex colors to one (white)
		self.vertex_colors = np.ones((self.vertices.shape[0], 3), dtype='f')

		if self.normals is None:
			print('(W) No normal array was provided.')
			print('--> setting to zero.')
			self.normals = np.zeros(self.vertices.shape, dtype='f')

		# and bind the data to a vertex array
		self.bind()
				
		
if __name__ == '__main__':

	# Create the scene object
	scene = Scene()

	# Load in the model
	meshes = load_obj_file('models/bunny_world.obj')
	
    # Add the main bunny model to be displayed
	scene.add_models_list(
			[DrawModelFromMesh(scene=scene, M=np.matmul(rotationMatrixY(90), poseMatrix()), mesh=mesh) for mesh in meshes]
        )

	# Create the fur model for the object
	fur_model = FurUtils(np.matmul(rotationMatrixY(90), poseMatrix()), scene, meshes[0].vertices, meshes[0].normals, meshes[0].faces, 0.1, 3, False)

	# starts drawing the scene
	scene.run()
