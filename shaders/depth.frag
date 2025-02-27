#version 330 core

layout (location = 0) out vec4 fragColor;


void main() {
    float depth = 20 * (1 - gl_FragCoord.z);
    fragColor = vec4(vec3(depth), 1.0);
}