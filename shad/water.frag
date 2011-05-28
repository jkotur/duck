#version 130
 
in vec3 normal;
in vec3 position;
 
out vec4 out_color;

uniform sampler2D normalmap;
uniform samplerCube cubemap;

uniform vec3 campos;

vec3 ray2cube( vec3 p , vec3 d )
{
	vec3 a;
	vec3 b;
	vec3 c;

	if( d.x < 0 )
			a = d * (-1-p.x) / d.x;
	else	a = d * ( 1-p.x) / d.x;

	if( d.y < 0 )
			b = d * (-1-p.y) / d.y;
	else	b = d * ( 1-p.y) / d.y;

	if( d.z < 0 )
			c = d * (-1-p.z) / d.z;
	else	c = d * ( 1-p.z) / d.z;

	float la = length(a);
	float lb = length(b);
	float lc = length(c);

	vec3  res = a;
	float len = la;

	if( lb < len ) { res = b; len = lb; }
	if( lc < len )   res = c;

	return res + p;
}
 
void main()
{
	vec3 norm =-normalize(texture2D(normalmap,gl_TexCoord[0].st).rgb);
	vec3 cdir =-normalize(campos-position);

	vec3 rdir = refract(cdir,norm,1.2);
	vec3 ldir = reflect(cdir,norm);
	//cdir = reflect(cdir,norm);

	vec4 rcol = textureCube(cubemap,ray2cube(position,rdir));
	vec4 lcol = textureCube(cubemap,ray2cube(position,ldir));

	if( rdir == vec3(0) )
		rcol = vec4(0);
	else
		lcol *= (1-dot(-cdir,norm));

	out_color = rcol * vec4(.60,.60,.75,1.0)+lcol;
}

