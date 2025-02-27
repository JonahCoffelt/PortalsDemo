#version 330 core

layout (location = 0) out vec4 fragColor;

flat in float textureIndex;

uniform vec2 viewportDimensions;
uniform sampler2D portalTexture1;
uniform sampler2D portalTexture2;


void main() {
    // Get the screen UV coord for maping portal and depth textures
    vec2 uv = (gl_FragCoord.xy) / viewportDimensions;  

    vec3 color;
    if (textureIndex == 0){
        color = texture(portalTexture1, uv).rgb;
    }
    else {
        color = texture(portalTexture2, uv).rgb;
    }

    fragColor = vec4(color, 1.0);
}