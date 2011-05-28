#version 130

uniform vec3 light;
uniform vec3 xdir;

uniform sampler2D texture;

in vec3 normal;
in vec3 position;

out vec4 out_color;

void main()
{
	float ka = 0.2;
	float kd = 0.5;
	float ks = 0.5;

	float ax = 1.0;
	float ay = 0.5;

	vec3 L = normalize(light - position);
	vec3 N = normalize(normal);
	vec3 H = normalize((L - normalize(position))/2.0);
	vec3 R = normalize(reflect(-L,N));
	vec3 X = normalize(xdir);
	vec3 Y = normalize(cross(X,N));

	float NL = dot(N,L);
	float NR = dot(N,R);
	float HX = dot(H,X);
	float HY = dot(H,Y);
	float HN = dot(H,N);

	float fd = NL;
	float fs = 1.0/sqrt(NL*NR)*NL/(4*ax*ay)*exp(-2*(pow(HX/ax,2)+pow(HY/ay,2))/(1.0+HN));

	if( fs < 0.0 ) fs = 0.0;

	float I = 2.0/length(light-position);

	float factor = (ka + kd*fd + ks*fs)*I;

	out_color = factor * texture2D(texture,gl_TexCoord[0].st);
}

