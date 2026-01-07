"""
Pong Game in C using SDL2 - Python wrapper
This Python script will build and run the provided C code using SDL2.

Instructions:
- Save the C code of the original Pong game into 'pong_c.c' in the same directory as this Python script.
- Make sure you have SDL2 installed (e.g., via apt: sudo apt install libsdl2-dev)
- Run this Python script: python c.py
  (It will build and run the Pong C program.)
"""

import subprocess
import os
import sys

C_FILENAME = "pong_c.c"
EXECUTABLE = "pong_c_exe"

C_SOURCE = r'''
// Pong Game in C using SDL2
// Compile with: gcc c.c -o pong -lSDL2

#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>

#define WINDOW_WIDTH 640
#define WINDOW_HEIGHT 480
#define PADDLE_WIDTH 10
#define PADDLE_HEIGHT 60
#define BALL_SIZE 10
#define BALL_SPEED_X 4
#define BALL_SPEED_Y 4

int main(int argc, char *argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("Failed to initialize SDL2: %s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *window = SDL_CreateWindow(
        "Pong - Now in C",
        SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        WINDOW_WIDTH, WINDOW_HEIGHT, 0
    );
    if (!window) {
        printf("Failed to create window: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    int paddle1_x = 10;
    int paddle1_y = (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2);
    int paddle2_x = WINDOW_WIDTH - PADDLE_WIDTH - 10;
    int paddle2_y = (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2);
    int ball_x = (WINDOW_WIDTH / 2) - (BALL_SIZE / 2);
    int ball_y = (WINDOW_HEIGHT / 2) - (BALL_SIZE / 2);
    int ball_dx = BALL_SPEED_X;
    int ball_dy = BALL_SPEED_Y;
    int score1 = 0;
    int score2 = 0;

    int running = 1;
    SDL_Event ev;
    while (running) {
        while (SDL_PollEvent(&ev)) {
            if (ev.type == SDL_QUIT) running = 0;
            if (ev.type == SDL_KEYDOWN) {
                if (ev.key.keysym.sym == SDLK_ESCAPE) running = 0;
            }
        }
        const Uint8 *keys = SDL_GetKeyboardState(NULL);
        // WASD / arrows
        if (keys[SDL_SCANCODE_W]) paddle1_y -= 5;
        if (keys[SDL_SCANCODE_S]) paddle1_y += 5;
        if (keys[SDL_SCANCODE_UP]) paddle2_y -= 5;
        if (keys[SDL_SCANCODE_DOWN]) paddle2_y += 5;
        // Clamp paddles
        if (paddle1_y < 0) paddle1_y = 0;
        if (paddle1_y > WINDOW_HEIGHT - PADDLE_HEIGHT) paddle1_y = WINDOW_HEIGHT - PADDLE_HEIGHT;
        if (paddle2_y < 0) paddle2_y = 0;
        if (paddle2_y > WINDOW_HEIGHT - PADDLE_HEIGHT) paddle2_y = WINDOW_HEIGHT - PADDLE_HEIGHT;
        // Move ball
        ball_x += ball_dx;
        ball_y += ball_dy;
        // Ball collision with top/bottom
        if (ball_y <= 0 || ball_y >= WINDOW_HEIGHT - BALL_SIZE) ball_dy = -ball_dy;
        // Paddle 1
        if (ball_x <= paddle1_x + PADDLE_WIDTH &&
            paddle1_y <= ball_y + BALL_SIZE &&
            ball_y <= paddle1_y + PADDLE_HEIGHT) {
            ball_dx = -ball_dx;
            ball_x = paddle1_x + PADDLE_WIDTH;
        }
        // Paddle 2
        if (ball_x + BALL_SIZE >= paddle2_x &&
            paddle2_y <= ball_y + BALL_SIZE &&
            ball_y <= paddle2_y + PADDLE_HEIGHT) {
            ball_dx = -ball_dx;
            ball_x = paddle2_x - BALL_SIZE;
        }
        // Left wall
        if (ball_x < 0) {
            score2 += 1;
            ball_x = (WINDOW_WIDTH / 2) - (BALL_SIZE / 2);
            ball_y = (WINDOW_HEIGHT / 2) - (BALL_SIZE / 2);
            ball_dx = BALL_SPEED_X;
            ball_dy = BALL_SPEED_Y;
        }
        // Right wall
        if (ball_x > WINDOW_WIDTH) {
            score1 += 1;
            ball_x = (WINDOW_WIDTH / 2) - (BALL_SIZE / 2);
            ball_y = (WINDOW_HEIGHT / 2) - (BALL_SIZE / 2);
            ball_dx = -BALL_SPEED_X;
            ball_dy = BALL_SPEED_Y;
        }
        // Render
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // black
        SDL_RenderClear(renderer);
        SDL_Rect paddle1 = {paddle1_x, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT};
        SDL_Rect paddle2 = {paddle2_x, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT};
        SDL_Rect ball = {ball_x, ball_y, BALL_SIZE, BALL_SIZE};
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // white
        SDL_RenderFillRect(renderer, &paddle1);
        SDL_RenderFillRect(renderer, &paddle2);
        SDL_RenderFillRect(renderer, &ball);
        // Net
        int y = 0;
        while (y < WINDOW_HEIGHT) {
            SDL_Rect net = {WINDOW_WIDTH/2-1, y, 2, 10};
            SDL_RenderFillRect(renderer, &net);
            y += 15;
        }
        // Score: printf style (no font rendering)
        char scorebuf[32];
        snprintf(scorebuf, sizeof(scorebuf), "%d : %d", score1, score2);
        // (Cheat) Draw numbers using SDL_SetWindowTitle for display
        SDL_SetWindowTitle(window, scorebuf);

        SDL_RenderPresent(renderer);
        SDL_Delay(1000 / 60);
    }
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
'''

def ensure_c_file():
    """Write the C code to disk if it's not present."""
    if not os.path.exists(C_FILENAME):
        with open(C_FILENAME, "w") as f:
            f.write(C_SOURCE)
        print(f"Wrote C Pong source to {C_FILENAME}")

def build_c():
    """Compile the C code to an executable using gcc."""
    if os.name == 'nt':
        exe_file = EXECUTABLE + ".exe"
        sdl2_flag = "-lSDL2"
    else:
        exe_file = "./" + EXECUTABLE
        sdl2_flag = "-lSDL2"
    if not os.path.exists(exe_file):
        print("Building the C Pong game...")
        # On Windows, the built executable gets the .exe extension,
        # and on Linux/macOS, we can execute via ./pong_c_exe
        cmd = [
            "gcc", C_FILENAME, "-o", EXECUTABLE + (".exe" if os.name == "nt" else ""),
            sdl2_flag
        ]
        try:
            subprocess.check_call(cmd)
            print("Build successful.")
        except FileNotFoundError:
            print("Could not find the gcc compiler. Please make sure gcc is installed and on your PATH.")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print("Build failed. Make sure you have SDL2 and gcc installed.")
            sys.exit(1)
    return exe_file

def run_game():
    exe_file = build_c()
    print("Launching Pong...")
    if os.name == 'nt':
        # On Windows, run as .exe (same dir)
        subprocess.run([exe_file])
    else:
        # On Unix, run as ./pong_c_exe
        subprocess.run([exe_file])

if __name__ == "__main__":
    ensure_c_file()
    run_game()
