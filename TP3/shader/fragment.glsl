#version 330

out vec4 fragColor;

uniform float u_time;       // iempo
uniform vec2 u_resolution;  // tamaño ventana
uniform vec2 u_mouse;       // posicion mouse
uniform int u_mode;         // teclado

vec3 random3(vec3 c) {
    float j = 4096.0 * sin(dot(c, vec3(17.0, 59.4, 15.0)));
    vec3 r;
    r.z = fract(512.0 * j);
    j *= .125;
    r.x = fract(512.0 * j);
    j *= .125;
    r.y = fract(512.0 * j);
    return r - 0.5;
}

const float F3 = 0.3333333;
const float G3 = 0.1666667;

float simplex3d(vec3 p) {
    vec3 s = floor(p + dot(p, vec3(F3)));
    vec3 x = p - s + dot(s, vec3(G3));
    vec3 e = step(vec3(0.0), x - x.yzx);
    vec3 i1 = e * (1.0 - e.zxy);
    vec3 i2 = 1.0 - e.zxy * (1.0 - e);
    vec3 x1 = x - i1 + G3;
    vec3 x2 = x - i2 + 2.0 * G3;
    vec3 x3 = x - 1.0 + 3.0 * G3;
    vec4 w, d;
    w.x = dot(x, x);
    w.y = dot(x1, x1);
    w.z = dot(x2, x2);
    w.w = dot(x3, x3);
    w = max(0.6 - w, 0.0);
    d.x = dot(random3(s), x);
    d.y = dot(random3(s + i1), x1);
    d.z = dot(random3(s + i2), x2);
    d.w = dot(random3(s + 1.0), x3);
    w *= w; w *= w;
    d *= w;
    return dot(d, vec4(52.0));
}

float noise(vec3 m) {
    return 0.5333333 * simplex3d(m)
         + 0.2666667 * simplex3d(2.0 * m)
         + 0.1333333 * simplex3d(4.0 * m)
         + 0.0666667 * simplex3d(8.0 * m);
}

void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    uv = uv * 2.0 - 1.0;

    vec2 p = gl_FragCoord.xy / u_resolution.x;
    vec3 p3 = vec3(p, u_time * 0.4);

    float intensity = noise(p3 * 8.0 + 12.0);

    float t = clamp((uv.x * -uv.x * 0.16) + 0.15, 0., 1.);
    float y = abs(intensity * -t + uv.y);

    float g = pow(y, 0.2);

    // color base
    vec3 col = vec3(1.25, 1.48, 1.78);
    col = col * -g + col;
    col = col * col;
    col = col * col;

    // === Interacciones ===
    if (u_mode == 1) {
        // cambair fondo con "2"
        col = vec3(intensity, 0.4, 0.2);
    }
    if (u_mode == 2) {
        // ruido con la posición del mouse
        col *= vec3(3.0 - u_mouse.x, 1.0 - u_mouse.y, 7.0);
    }

    fragColor = vec4(col, 1.0);
}
