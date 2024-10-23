#include <SDL2/SDL.h>
#include <GL/glew.h>
#include <GL/glu.h>
#include <cmath>
#include <iostream>

// Window dimensions
const int W = 800;
const int H = 800;

// Initialization function
bool init(SDL_Window** window, SDL_GLContext* context) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cerr << "Error: Could not initialize SDL: " << SDL_GetError() << std::endl;
        return false;
    }

    *window = SDL_CreateWindow("3D Beating Heart", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, W, H, SDL_WINDOW_OPENGL | SDL_WINDOW_SHOWN);
    if (*window == NULL) {
        std::cerr << "Error: Could not create window: " << SDL_GetError() << std::endl;
        SDL_Quit();
        return false;
    }

    *context = SDL_GL_CreateContext(*window);
    if (*context == NULL) {
        std::cerr << "Error: Could not create OpenGL context: " << SDL_GetError() << std::endl;
        SDL_DestroyWindow(*window);
        SDL_Quit();
        return false;
    }

    if (glewInit() != GLEW_OK) {
        std::cerr << "Error: Could not initialize GLEW" << std::endl;
        SDL_GL_DeleteContext(*context);
        SDL_DestroyWindow(*window);
        SDL_Quit();
        return false;
    }

    glEnable(GL_DEPTH_TEST);
    return true;
}

// Render a 3D heart shape
void renderHeart(float scale) {
    glBegin(GL_TRIANGLES);
    glColor3f(1.0f, 0.0f, 0.0f);
    for (float t = 0; t < 2 * M_PI; t += 0.01) {
        float x = 16 * pow(sin(t), 3);
        float y = 13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t);
        glVertex3f(x * scale, y * scale, 0);
    }
    glEnd();
}

// Animation loop
void animateHeart(SDL_Window* window) {
    bool running = true;
    SDL_Event event;
    float scale = 1.0;
    bool growing = true;

    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            }
        }

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glLoadIdentity();
        gluLookAt(0.0, 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);

        if (growing) {
            scale += 0.01;
            if (scale > 1.2) growing = false;
        } else {
            scale -= 0.01;
            if (scale < 0.8) growing = true;
        }

        renderHeart(scale);
        SDL_GL_SwapWindow(window);
    }
}

int main(int argc, char* argv[]) {
    SDL_Window* window = NULL;
    SDL_GLContext context;

    if (!init(&window, &context)) {
        return -1;
    }

    animateHeart(window);

    SDL_GL_DeleteContext(context);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
