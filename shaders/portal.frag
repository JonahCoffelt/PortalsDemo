#version 330 core

layout (location = 0) out vec4 fragColor;

flat in float textureIndex;

uniform vec2 viewportDimensions;
uniform sampler2DArray portalTextures;
// uniform sampler2DArray portalDepths;

void main() {
    // Get the screen UV coord for maping portal and depth textures
    vec2 uv = (gl_FragCoord.xy) / viewportDimensions;    
    vec3 uvw = vec3(uv, round(textureIndex));

    // Get the depth of the fragment and the depth of the portal view
    // float depth      = gl_FragCoord.z;
    // float view_depth = texture(portalDepths, uvw).r;
    fragColor = vec4(texture(portalTextures, uvw).rgb, 1.0);


    // // DEBUG
    // fragColor.rgb /= 100000;
    // // fragColor.r = 20 * (1 - depth);
    // fragColor.r += 20 * (1 - texture(portalDepths, vec3(uv, 1)).r);
}