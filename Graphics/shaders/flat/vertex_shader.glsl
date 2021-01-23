#version 130		// required to use OpenGL core standard

//=== in attributes are read from the vertex array, one row per instance of the shader
in vec3 position;	// the position attribute contains the vertex position
in vec3 normal;		// store the vertex normal
in vec3 color; 		// store the vertex colour

//=== out attributes are interpolated on the face, and passed on to the fragment shader
out vec3 fragment_color;        // the output of the shader will be the colour of the vertex
out vec3 position_view_space;   // the position of the vertex in view coordinates

//=== uniforms
uniform mat4 PVM; 	// the Perspective-View-Model matrix is received as a Uniform
uniform mat4 VM; 	// the View-Model matrix is received as a Uniform
uniform mat3 VMiT;  // The inverse-transpose of the view model matrix, used for normals
uniform int mode;	// the rendering mode (better to code different shaders!)

uniform vec3 fur_displacement;
uniform float fur_length;

void main(){
    // 1. first, we transform the position using PVM matrix.
    gl_Position = PVM * vec4(position, 1.0f);

    // 2. calculate vectors used for shading calculations
    position_view_space = vec3(VM*vec4(position, 1.0f));

    // 3. for now, we just pass on the color from the data array.
    fragment_color = color;
}
