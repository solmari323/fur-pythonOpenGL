# File defining the scene class holding scene-wide parameters

# Import needed files 
import pygame
import numpy as np
from OpenGL.GL import *
from matutils import *
from camera import Camera
from lightSource import LightSource
from shaders import Shaders
# from FurUtil import *


class Scene:
	'''
	This is the main class for drawing an OpenGL scene using the PyGame library
	'''
	
	def __init__(self, width=1250, height=800, shaders=None):
		'''
		Initialises the scene
			:param width: width of window displaying the scene
			:param height: height of window displaying the scene
			:param shaders: shaders being used in the scene
		'''

		# Define display window size
		self.window_size = (width, height)

		# By default, wireframe mode is off
		self.wireframe = False

		# Initialise the window (pygame aspect)
		pygame.init()
		screen = pygame.display.set_mode(self.window_size, pygame.OPENGL | pygame.DOUBLEBUF, 24)

		# Initialise the window (OpenGL aspect)
		glViewport(0, 0, self.window_size[0], self.window_size[1])

		# Define background color
		glClearColor(1.0, 1.0, 1.0, 1.0)

		# Enable back face culling
		glEnable(GL_CULL_FACE)
		glCullFace(GL_BACK)
		
		# Enable the vertex array capability
		glEnableClientState(GL_VERTEX_ARRAY)
		
		# enable depth test for clean output (see lecture on clipping & visibility for an explanation)
		glEnable(GL_DEPTH_TEST)

		#Store, compile and use flat shading (basic shader should be good enough)
		self.useShader = [Shaders('flat')]
		self.useShader[0].compile()
		self.shaders = self.useShader[0]

		# Initialise the projective transform
		near=1.5
		far=20
		left=-1.0
		right=1.0
		top=-1.0
		bottom=1.0

		# Start with, we use an orthographic projection;
		self.P = frustumMatrix(left,right,top,bottom,near,far)

		# Initialises the camera object
		self.camera = Camera(self.window_size)

		# Initialise the light source (aim to light top front of bunny)
		self.light = LightSource(self, position=[-2.5,5.,0.])

		# Rendering mode for the shaders
		self.mode = 6 # Initialise to full interpolated shading

		# Maintain a list of models to draw in the scene,
		self.models = []
		
		self.fur_model = None
				
	def add_model(self,model):
		'''
		This method just adds a model to the scene.
			:param model: The model object to add to the scene
		'''
		self.models.append(model)
		
		
	def add_models_list(self,models_list):
		'''
		This method just adds a model to the scene.
			:param model: The model object to add to the scene
		'''
		self.models.extend(models_list)

		
	def remove_model(self):
		'''
		This method just removes a model to the scene. Used to re-render the fur model
		'''
		self.models.pop(-1) # Used to remove previous model which should always be fur texture due to it being appended after the main model
		
		
	def draw(self):
		'''
		Draw all models in the scene as well as text
		'''

		# Clear the scene as well as the depth buffer to handle occlusions
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		self.camera.update()

		# Loop over list and draw all models
		for model in self.models:
			model.draw(Mp=poseMatrix(), shaders=self.shaders)
		
		# Flip double buffer (draw on separate buffer to one displayed to avoid
		# artifacts) once models are drawn
		pygame.display.flip()
	

	def keyboard(self, event):
		#'Esc' to quit
		if event.key == pygame.K_ESCAPE:
			print('\nQuitting program')
			self.running = False

		# 'UP', 'DOWN', 'RIGHT', 'LEFT' to rotate camera
		elif event.key == pygame.K_UP:
			self.camera.psi += float(0.25)
		elif event.key == pygame.K_DOWN:
			self.camera.psi -= float(0.25)	
		elif event.key == pygame.K_RIGHT:
			self.camera.phi += float(0.25)
		elif event.key == pygame.K_LEFT:
			self.camera.phi -= float(0.25)
		
		# 'k' and 'l' to decrease/incerease fur length
		elif event.key == pygame.K_k:
			print('\n--> Decreasing fur length')
			self.remove_model()
			self.fur_model.update_fur_length(-0.1)
			
		elif event.key == pygame.K_l:
			print('\n--> Increasing fur length')
			self.remove_model()
			self.fur_model.update_fur_length(0.1)
		
		# 'n' and 'm' to decrease/incerease fur density
		elif event.key == pygame.K_n:
			print('\n--> Decreasing fur density')
			self.remove_model()
			self.fur_model.update_fur_density(-0.25)
			
		elif event.key == pygame.K_m:
			print('\n--> Increasing fur density')
			self.remove_model()
			self.fur_model.update_fur_density(0.25)
			
		# 'b' to toggle fur in random direction/use normals to determine direction
		elif event.key == pygame.K_b:
			if self.fur_model.fur_angle:
				print('\n--> Rendering fur using normals for direction')
			else:
				print('\n--> Rendering fur in same direction using a randomly generated angle')
			self.remove_model()
			self.fur_model.update_fur_direction()


	def pygameEvents(self):
		# Check whether the window has been closed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			# Keyboard events
			elif event.type == pygame.KEYDOWN:
				self.keyboard(event)

			# Mouse events
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# 'Scroll up' function to zooom in
				if event.button == 4:
					self.camera.distance = max(3.5, self.camera.distance - 1)
				# 'Scroll down' function to zoom out
				elif event.button == 5:
					self.camera.distance += 1

			elif event.type == pygame.MOUSEMOTION:
				# Translate camera while left click held
				if pygame.mouse.get_pressed()[0]:
					if self.mouse_mvt is not None:
						self.mouse_mvt = pygame.mouse.get_rel()
						# Move camera based on window size
						self.camera.center[0] += (float(self.mouse_mvt[0])/(self.window_size[0]/2))
						self.camera.center[1] -= (float(self.mouse_mvt[1])/(self.window_size[1]/2))
					else:
						self.mouse_mvt = pygame.mouse.get_rel()
				else:
					self.mouse_mvt = None

					
	def run(self):
		'''
		Draws the scene in a loop until exit.
		'''		
		self.running = True
		while self.running:
			# Check for keyboard or mouse actions
			self.pygameEvents()
			
			# Then continue drawing the scene
			self.draw()
