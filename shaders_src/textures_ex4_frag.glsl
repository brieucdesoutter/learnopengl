#version 330 core

uniform sampler2D texture1;
uniform sampler2D texture2;
uniform float alpha;

in vec2 texCoord;

out vec4 FragColor;
void main() {
    FragColor = mix(texture(texture1, texCoord),
                    texture(texture2, texCoord), alpha);
}