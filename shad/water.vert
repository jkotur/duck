#version 130                

uniform mat4 modelview; 
uniform mat4 projection;
  
out vec3 normal;
out vec3 position;
  
void main()
{
    gl_Position    = projection * modelview * gl_Vertex;
	gl_TexCoord[0] = gl_MultiTexCoord0;
    normal         = gl_Normal;
	position       = gl_Vertex.xyz;
}

