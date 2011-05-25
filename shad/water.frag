#version 130
 
in vec3 normal;
 
out vec4 out_color;

uniform sampler2D normalmap;
 
void main() {
		vec3 norm = normalize(texture2D(normalmap,gl_TexCoord[0].st).rgb)*10;
		out_color = vec4(norm+vec3(.5,.5,.5),1);
}

