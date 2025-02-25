#version 330 core

layout (location = 0) out vec4 fragColor;

flat in int textureIndex;

uniform vec2 viewportDimensions;
// uniform sampler2DArray portalViews;

void main() {
    vec2 uv = (gl_FragCoord.xy) / viewportDimensions;    
    fragColor = vec4(uv, textureIndex, 1.0);
}