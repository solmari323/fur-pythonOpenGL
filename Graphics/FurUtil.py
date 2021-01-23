from material import Material
from OpenGL.GL import *
from HairModel import HairModel
from material import Material
import numpy as np
import random


class FurUtils:
    """
    A utility class which handles the necessary fur transformations
    """

    def __init__(self, M, scene, vertices, normals, indices, fur_length, fur_density, fur_angle):
        """
        The constructor takes the same information a model would, namely:
        :param scene: The scene reference
        :param vertices: Initial vertices to which the fur is being appended
        :param normals: Initial normals to which the fur is being appended
        :param indices: Initial faces
        :param fur_length: fur length parameter
        :param fur_density: fur density parameter
        :param fur_angle: fur angle parameter
        """
        # create a two way relationship with the scene
        self.scene = scene
        self.scene.fur_model = self
        self.M = M

        # initialize mesh information
        self.initial_vertices = vertices
        self.initial_normals = normals
        self.indices = indices

        # initialize fur parameters
        self.fur_length = fur_length
        self.fur_density = fur_density
        self.fur_angle = fur_angle

        # generate new vertices for the fur model
        self.create_vertices()



    def create_vertices(self):
        """
        Calculate coordinates for the hairs on the fur model and then pass to the HairModel to render
        """
        # calculate starting points for each hair
        fur_vertices, fur_normals = self.new_startpoints(self.initial_vertices, self.initial_normals, self.fur_density)

        # calculate endpoints for each hair
        all_fur_vertices = self.new_endpoints(fur_vertices, fur_normals, self.fur_length, self.fur_angle)

        # add the same normals from starting points to endpoints
        all_fur_normals = []
        for n in fur_normals:
            all_fur_normals.extend([n, n])

        # generate hair model
        fur_model = HairModel(M=self.M, scene=self.scene, vertices=np.array(all_fur_vertices), normals=np.array(all_fur_normals))
        fur_model.bind()
        self.scene.add_model(fur_model)

    def new_startpoints(self, vertices, normals, density):
        """
        Calculate the starting points of each hair
        :param vertices: model initial vertices
        :param normals: model initial normals
        :param density: desired density
        :return:
        """
        startpoints = [[],[]]

        if density > 0:
            # find the list of all faces
            vertex_faces = self.get_face_vertices(vertices, self.indices)
            normal_faces = self.get_face_vertices(normals, self.indices)

            # split each face further based on density
            for i in range(len(vertex_faces)):
                new_startpoints = self.densify_fur(vertex_faces[i], normal_faces[i], density)
                startpoints[0] += new_startpoints[0]
                startpoints[1] += new_startpoints[1]

            # Add newly found vertices/normals to list of strand origins
            vertices = np.concatenate((vertices, startpoints[0]))
            normals = np.concatenate((normals, startpoints[1]))

        return vertices, normals

    def get_face_vertices(self, vertices, indices):
        """
        Using a list of indices and vertex coords, return a list of faces they correspond to
        :param vertices: vertices (can also be used for normals)
        :param indices: indices
        :return:
        """
        faces = []
        for index in indices:
            face = [vertices[i] for i in index]
            faces.append(face)
        return np.array(faces)

    def densify_fur(self, vertices, normals, density):
        """
        Simulate splitting of each face to generate new coordinates
            :param vertices: vertices
            :param normals: quad normals
            :param density: desired density
            :return: list of new coordinates
        """

        # Find strand origins of the face
        vert_origin = sum(vertices) / len(vertices)
        norm_origin = sum(normals) / len(normals)

        # Add to list
        vert_origins = [vert_origin]
        norm_origins = [norm_origin]

        # For each level of density (integer), create new small triangles/quads with origins
        if (density - 1) > 0:  # Density not yet reached
            if len(vertices) == 3:
                # Triangle: create 3 new small triangles
                new_vert = [[vertices[0], vertices[1], vert_origin],
                            [vertices[0], vertices[2], vert_origin],
                            [vertices[1], vertices[2], vert_origin]]
                new_norm = [[normals[0], normals[1], norm_origin],
                            [normals[0], normals[2], norm_origin],
                            [normals[1], normals[2], norm_origin]]
            elif len(vertices) == 4:
                # Quad: create 4 new small quads
                new_vert = [[vertices[0], vertices[1], vert_origin],
                            [vertices[1], vertices[2], vert_origin],
                            [vertices[2], vertices[3], vert_origin],
                            [vertices[3], vertices[0], vert_origin]]
                new_norm = [[normals[0], normals[1], norm_origin],
                            [normals[1], normals[2], norm_origin],
                            [normals[2], normals[3], norm_origin],
                            [normals[3], normals[0], norm_origin]]

            # Call function recursively to check if density reached for each new origin
            for v in range(len(new_vert)):
                next_level = self.densify_fur(new_vert[v], new_norm[v], density - 1)
                vert_origins += next_level[0]
                norm_origins += next_level[1]

        return [vert_origins, norm_origins]

    def new_endpoints(self, vertices, normals, length,angle):
        """
        Find the end of each hair on the model
        :param vertices: vertices
        :param normals:normals (used for hair direction)
        :param length: hair length
        :param angle: a flag to denote whether random angle is used
        :return:
        """
        # a list which will record the location of each hair endpoint
        endpoints = []

        # choose a normal at random to use for all vertices if the random angle flag is true
        rand_normal_index = random.randint(0, len(normals) - 1)


        # for each vertex, calculate the endpoint location
        for v_idx in range(len(vertices)):
            rand_length = length * (random.randint(1, 10) / 10)
            endpoints.append(vertices[v_idx])

            #check whether to use a random direction to put fur in
            if angle:
                # use random normal direction
                endpoints.append(vertices[v_idx] + normals[rand_normal_index]*rand_length)
            else:
                # use regular normal direction
                endpoints.append(vertices[v_idx] + normals[v_idx] * rand_length)

        return endpoints

    def update_fur_length(self, new_len):
        """
        Generate a new fur model with an updated fur length
        :param new_len: length to be added to current value taken from user input
        """

        # Update strand length value to regenerate fur using new length
        self.fur_length += new_len

        # Fur length value must be above 0
        if self.fur_length > 0:
            self.create_vertices()
        else:
            # hair length cannot go into negatives, creates funky results
            print('(W) Warning: fur length at shortest value and will not go under 0')
            self.fur_length = 0
            self.create_vertices()

    def update_fur_density(self, new_den):
        """
        Generate a new fur model with an updated fur density
        :param new_den: desity to be added to current value taken from user input
        """

        # Update density value to regenerate fur using new density number
        self.fur_density += new_den

        # Density must be above 0
        if self.fur_density > 0:
            self.create_vertices()
        else:
            # Prevent from going into negative density
            print('(W) Warning: fur density at lowest value and will not go under 0')
            self.fur_density = 0
            self.create_vertices()

    def update_fur_direction(self):
        """
        Generate a new fur model with an updated fur direction by toggling a variable
        decideing wether to generate directions using a single angle or face normals
        """

        # Update direction boolean to regenerate fur using a random angle
        self.fur_angle = not self.fur_angle
        self.create_vertices()





