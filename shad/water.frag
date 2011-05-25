#version 130
 
in vec3 normal;
 
out vec4 out_color;

uniform sampler2D normalmap;
uniform samplerCube cubemap;
 
void main() {
		vec3 norm = texture2D(normalmap,gl_TexCoord[0].st).rgb;
		out_color = textureCube(cubemap,-norm);
}

