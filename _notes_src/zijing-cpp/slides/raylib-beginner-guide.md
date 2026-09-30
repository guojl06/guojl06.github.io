# raylib\-beginner\-guide

# Raylib Beginner's Guide

---

## What is Raylib?

**Raylib** is a simple and easy\-to\-use library for learning game programming\. It is written in C and provides bindings for C\+\+\. Raylib is perfect for beginners because:

- **Simple API**: Clean, straightforward functions that are easy to understand

- **No external dependencies**: Everything you need is included

- **Cross\-platform**: Works on Windows, macOS, Linux, and even web browsers

- **Well\-documented**: Extensive examples and documentation available

- **Active community**: Friendly community ready to help beginners

Raylib can help you create:

- 2D and 3D games

- Interactive applications

- Visualizations and simulations

- Prototypes and proof\-of\-concepts

---

## Prerequisites

Before installing Raylib, you should have:

1. **Basic C\+\+ knowledge**: Understanding of variables, loops, functions, and basic syntax

2. **A C\+\+ compiler**: Different for each platform \(we'll cover installation below\)

3. **An IDE or text editor**: Visual Studio, VS Code, or Xcode \(We recommend VS and Xcode\)

---

## Installation Guides

### Visual Studio \(Windows\)

First try raylib\_quickstart provided by raylib\. You can find it through the cloud link as follows:

https://cloud\.tsinghua\.edu\.cn/f/9d457c32c0ec444ca074/?dl=1



which will download a zip file\(raylib\-quickstart\-main2026\.zip\)\. You can unzip it and open the folder\.

if you are able to connect to github, you may be able to successfully run the program by following the instructions in the README\.md file\.

If you are not able to connect to github, or you did not see the files compiled in the external folder, please try the following steps:

1. download a new zip file from the cloud link:
[https://cloud\.tsinghua\.edu\.cn/f/a8bfca7f920a44e29f41/?dl=1](https://cloud.tsinghua.edu.cn/f/a8bfca7f920a44e29f41/?dl=1)
which is raylib\_master\.zip\.

2. copy raylib\_master\.zip to the external folder\.

3. run the batch file again\.

4. you should be able to see the files compiled in the external folder\.

If the previous steps did not work and you are using visual studio 2022, you can download a complete folder which holds all the files you need to build and run the program\.
[https://cloud\.tsinghua\.edu\.cn/d/d04b040a523d49ed8e75/](https://cloud.tsinghua.edu.cn/d/d04b040a523d49ed8e75/)

If the previous steps did not work, please wait until the tutorial session\.

---

### Xcode \(macOS\)

For the Xcode user, First try raylib\_quickstart provided by raylib\. You can find it through the cloud link as follows:

[https://cloud\.tsinghua\.edu\.cn/f/9d457c32c0ec444ca074/?dl=1](https://cloud.tsinghua.edu.cn/f/5696e0fab5ac4bfe878c/?dl=1)

which will download a zip file\(raylib\-quickstart\-main2026\.zip\)\. You can unzip it and open the folder\.

You may be able to successfully run the program by following the instructions in the README\.md file\.

If the previous steps did not work, please try the following steps:

#### Step 1: Install Xcode

1. Open the **App Store** on your Mac

2. Search for **"Xcode"**

3. Click **Get** and then **Install**

4. Wait for the download and installation to complete \(this is a large download, \~10\+ GB\)

#### Step 2: Install Xcode Command Line Tools

1. Open **Terminal** \(Applications → Utilities → Terminal\)

2. Run:

```Bash
xcode-select --install
```

3. Click **Install** in the dialog that appears

#### Step 3: Install Raylib

You have two options:

**Option A: Using Homebrew \(Easiest\)**

1. If you don't have Homebrew, install it:

```Bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Raylib:

```Bash
brew install raylib
```

**Option B: Build from Source**

```Bash
git clone https://github.com/raysan5/raylib.git
cd raylib
mkdir build && cd build
cmake .. -DBUILD_SHARED_LIBS=ON
make
sudo make install
```

#### Step 4: Create a New Xcode Project

1. Open Xcode

2. Click **"Create a new Xcode project"** \(or File → New → Project\)

3. In the template selector, choose **macOS** → **Command Line Tool**

4. Click **Next**

#### Step 5: Configure the Project

1. **Project Details**:

- Product Name: `MyFirstRaylibGame`

- Organization: \(your name or leave blank\)

- Language: **C\+\+**

- Click **Next**

2. **Choose a location** to save your project

3. **Add Raylib to the project**:

- In the Project Navigator \(left sidebar\), click on your project name

- Select your target under **TARGETS**

- Go to **Build Settings** tab

- Search for **"Header Search Paths"**

- Add the Raylib include path:

    - If using Homebrew on Apple Silicon: `/opt/homebrew/include`

    - If using Homebrew on Intel: `/usr/local/include`

    - If built from source: `/usr/local/include`

4. **Add Library Search Paths**:

- Search for **"Library Search Paths"** in Build Settings

- Add the Raylib library path:

    - Apple Silicon: `/opt/homebrew/lib`

    - Intel Mac: `/usr/local/lib`

5. **Link the Raylib Library**:

- Go to **Build Phases** tab

- Expand **"Link Binary With Libraries"**

- Click the **\+** button

- Click **"Add Other\.\.\."** → **"Add Files\.\.\."**

- Navigate to the Raylib library:

    - Apple Silicon: `/opt/homebrew/lib/libraylib.dylib`

    - Intel: `/usr/local/lib/libraylib.dylib`

- Select the file and click **Open**

6. **Add Required Frameworks**:

- In the same **"Link Binary With Libraries"** section, click **\+**

- Add the following frameworks \(search for each and add\):

    - `CoreVideo.framework`

    - `IOKit.framework`

    - `Cocoa.framework`

    - `GLUT.framework`

    - `OpenGL.framework`

#### Step 6: Write Your Code

1. In the Project Navigator, find `main.cpp`

2. Replace the contents with the sample code from "Your First Raylib Program" section

#### Step 7: Build and Run

1. Click the **Play button** \(▶\) in the top\-left corner

2. Or press `Cmd+R`

3. Your Raylib window should appear\!

---

## Your First Raylib Program

Here's a simple program to test your Raylib installation\. Create a file named `main.cpp` with this code:

```C++
#include "raylib.h"

int main() {
    // Initialize the window
    const int screenWidth = 800;
    const int screenHeight = 450;
    
    InitWindow(screenWidth, screenHeight, "My First Raylib Program");
    
    // Set the game to run at 60 frames-per-second
    SetTargetFPS(60);
    
    // Main game loop
    while (!WindowShouldClose()) {  // Detect window close button or ESC key
        // Update
        // TODO: Add game logic here
        
        // Draw
        BeginDrawing();
        
        ClearBackground(RAYWHITE);
        
        DrawText("Congrats! You created your first window!", 
                 190, 200, 20, LIGHTGRAY);
        
        DrawCircle(screenWidth/2, screenHeight/2, 50, RED);
        
        EndDrawing();
    }
    
    // De-initialize
    CloseWindow();
    
    return 0;
}
```

### Understanding the Code

|Function|What It Does|
|---|---|
|`InitWindow()`|Creates a window with specified width, height, and title|
|`SetTargetFPS()`|Limits the game to run at 60 frames per second|
|`WindowShouldClose()`|Returns true if the window should close \(ESC key or close button\)|
|`BeginDrawing()`|Starts the drawing phase|
|`ClearBackground()`|Fills the screen with a color|
|`DrawText()`|Draws text on the screen|
|`DrawCircle()`|Draws a circle|
|`EndDrawing()`|Ends the drawing phase and updates the screen|
|`CloseWindow()`|Closes the window and frees resources|

---

## Project Structure

A typical Raylib project structure:

```Plaintext
MyRaylibProject/
├── src/
│   ├── main.cpp
│   ├── player.cpp
│   ├── player.h
│   └── utils.cpp
├── include/
│   └── (third-party headers)
├── lib/
│   └── (third-party libraries)
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
├── build/
│   └── (compiled output)
└── README.md
```

---

## Learning Resources

### Official Resources

- **Raylib Website**: [https://www\.raylib\.com/](https://www.raylib.com/)

- **Raylib Examples**: [https://www\.raylib\.com/examples\.html](https://www.raylib.com/examples.html)

- **Raylib Cheatsheet**: [https://www\.raylib\.com/cheatsheet/cheatsheet\.html](https://www.raylib.com/cheatsheet/cheatsheet.html)

- **Raylib GitHub**: [https://github\.com/raysan5/raylib](https://github.com/raysan5/raylib)

### Community

- **Raylib Discord**: Join the official Discord for help and discussion

- **r/raylib Subreddit**: Community discussions and showcases

### Tutorial Series

- **Raylib Tutorial Series**: Search YouTube for "raylib tutorial beginner"

- **Programming Knowledge**: Various channels offer step\-by\-step Raylib guides

### Next Steps

1. Study the official examples

2. Try modifying the sample code

3. Create a simple game \(like Pong or Snake\)

4. Experiment with different shapes, colors, and inputs

5. Learn about textures, sounds, and game state management

---

## Troubleshooting

### Common Issues and Solutions

**Issue: "raylib\.h not found"**

- Solution: Check that the include path is correctly set in your project settings

**Issue: "undefined reference to\.\.\." linker errors**

- Solution: Make sure the library is correctly linked in your project settings

**Issue: Window doesn't open or crashes immediately**

- Solution: Ensure `InitWindow()` is called before any other Raylib function

**Issue: Black screen**

- Solution: Make sure `BeginDrawing()` and `EndDrawing()` are properly paired

---

## Part 2: Raylib Basics and Chess Game Tutorial

Now that you have Raylib installed, let's learn the basics by building a chess game\. We will progress **from simple to complex**, focusing on:

1. Drawing the chessboard

2. Loading and displaying chess pieces

3. Moving pieces with mouse interaction

**Note**: This tutorial focuses on graphics and interaction, not chess rules\. We won't implement check, checkmate, or move validation\.

---

## Chapter 1: Basic Raylib Concepts

### 1\.1 Colors in Raylib

Raylib provides predefined colors you can use directly:

```C++
RAYWHITE    // Light background color
WHITE       // Pure white
BLACK       // Pure black
RED         // Red
GREEN       // Green
BLUE        // Blue
YELLOW      // Yellow
ORANGE      // Orange
PURPLE      // Purple
GRAY        // Gray
DARKGRAY    // Dark gray
LIGHTGRAY   // Light gray
BROWN       // Brown
PINK        // Pink
```

You can also create custom colors:

```C++
Color myColor = {255, 100, 50, 255};  // R, G, B, Alpha (0-255 each)
Color semiTransparent = {0, 0, 0, 128}; // Black with 50% transparency
```

### 1\.2 Drawing Basic Shapes

```C++
// Rectangle
DrawRectangle(x, y, width, height, color);

// Circle
DrawCircle(centerX, centerY, radius, color);

// Line
DrawLine(startX, startY, endX, endY, color);

// Text
DrawText("Hello", x, y, fontSize, color);
```

### 1\.3 Input Handling

```C++
// Mouse position
Vector2 mousePos = GetMousePosition();
int mouseX = GetMouseX();
int mouseY = GetMouseY();

// Mouse button states
IsMouseButtonPressed(MOUSE_LEFT_BUTTON);    // Just clicked
IsMouseButtonDown(MOUSE_LEFT_BUTTON);         // Currently held down
IsMouseButtonReleased(MOUSE_LEFT_BUTTON);     // Just released

// Keyboard
IsKeyPressed(KEY_A);      // A key just pressed
IsKeyDown(KEY_SPACE);     // Space bar held down
IsKeyReleased(KEY_ESCAPE);// ESC just released
```

---

### 1\.4 Practical Example: Moving Ball with Sound

Let's create a complete example that combines shapes, keyboard input, and sound\. This program displays a red ball that you can move with arrow keys\. When the ball hits the screen border, it plays a sound\.

```C++
#include "raylib.h"
#include <cmath>    // For sinf()
#include <cstring>  // For memset

int main() {
    // Window setup
    const int screenWidth = 800;
    const int screenHeight = 600;
    InitWindow(screenWidth, screenHeight, "Moving Ball with Sound");
    
    // Initialize audio system
    InitAudioDevice();
    
    // Ball properties
    float ballX = screenWidth / 2.0f;   // Start in center
    float ballY = screenHeight / 2.0f;
    const float ballRadius = 30.0f;
    const float ballSpeed = 5.0f;       // Pixels per frame
    
    // Create a simple "bounce" sound
    // Method 1: Try to load from file (if bounce.wav exists)
    Sound bounceSound = {0};
    Wave bounceWave = {0};
    
    // Check if bounce.wav file exists
    if (FileExists("bounce.wav")) {
        bounceWave = LoadWave("bounce.wav");
        bounceSound = LoadSoundFromWave(bounceWave);
    }
    
    // Method 2: If file doesn't exist or failed to load, generate a simple tone
    if (bounceSound.frameCount == 0) {
        // Create a 440Hz tone for 0.2 seconds
        Wave generatedWave = {0};
        generatedWave.frameCount = static_cast<unsigned int>(44100 * 0.2f);  // 0.2 seconds at 44100Hz
        generatedWave.sampleRate = 44100;
        generatedWave.sampleSize = 16;
        generatedWave.channels = 1;
        
        // Allocate memory for audio samples
        size_t dataSize = generatedWave.frameCount * sizeof(short);
        generatedWave.data = MemAlloc(dataSize);
        
        // Clear memory first
        if (generatedWave.data != nullptr) {
            std::memset(generatedWave.data, 0, dataSize);
            
            // Generate sine wave
            short *data = static_cast<short*>(generatedWave.data);
            for (unsigned int i = 0; i < generatedWave.frameCount; i++) {
                float time = static_cast<float>(i) / static_cast<float>(generatedWave.sampleRate);
                float sineValue = std::sin(2.0f * 3.14159265f * 440.0f * time);
                data[i] = static_cast<short>(32000.0f * sineValue);
            }
            
            bounceSound = LoadSoundFromWave(generatedWave);
            UnloadWave(generatedWave);  // Can unload wave after creating sound
        }
    }
    
    SetTargetFPS(60);
    
    // Timer for displaying "BOUNCE!" text (in frames)
    int bounceDisplayTimer = 0;
    const int BOUNCE_DISPLAY_FRAMES = 45;  // Show for 45 frames (~0.75 seconds at 60 FPS)
    
    while (!WindowShouldClose()) {
        // --- UPDATE ---
        
        // Move ball with arrow keys
        if (IsKeyDown(KEY_RIGHT)) ballX += ballSpeed;
        if (IsKeyDown(KEY_LEFT))  ballX -= ballSpeed;
        if (IsKeyDown(KEY_UP))    ballY -= ballSpeed;
        if (IsKeyDown(KEY_DOWN))  ballY += ballSpeed;
        
        // Check border collision and play sound
        bool hitBorder = false;
        
        // Left border
        if (ballX - ballRadius < 0.0f) {
            ballX = ballRadius;  // Keep inside screen
            hitBorder = true;
        }
        // Right border
        if (ballX + ballRadius > static_cast<float>(screenWidth)) {
            ballX = static_cast<float>(screenWidth) - ballRadius;
            hitBorder = true;
        }
        // Top border
        if (ballY - ballRadius < 0.0f) {
            ballY = ballRadius;
            hitBorder = true;
        }
        // Bottom border
        if (ballY + ballRadius > static_cast<float>(screenHeight)) {
            ballY = static_cast<float>(screenHeight) - ballRadius;
            hitBorder = true;
        }
        
        // Play sound and start timer when hitting border
        if (hitBorder && bounceSound.frameCount > 0) {
            PlaySound(bounceSound);
            bounceDisplayTimer = BOUNCE_DISPLAY_FRAMES;  // Reset timer to show text
        }
        
        // Decrease timer each frame (but not below 0)
        if (bounceDisplayTimer > 0) {
            bounceDisplayTimer--;
        }
        
        // --- DRAWING ---
        BeginDrawing();
        
        ClearBackground(RAYWHITE);
        
        // Draw border lines to show boundaries
        DrawRectangleLines(1, 1, screenWidth - 2, screenHeight - 2, DARKGRAY);
        
        // Draw the ball
        DrawCircle(static_cast<int>(ballX), static_cast<int>(ballY), ballRadius, RED);
        
        // Add a highlight to make it look 3D
        Color highlightColor = {255, 100, 100, 200};
        DrawCircle(static_cast<int>(ballX) - 8, static_cast<int>(ballY) - 8, 
                   ballRadius / 3.0f, highlightColor);
        
        // Draw instructions
        DrawText("Use ARROW KEYS to move the ball", 10, 10, 20, DARKGRAY);
        DrawText("Hit the border to hear a sound!", 10, 35, 20, DARKGRAY);
        DrawText(TextFormat("Ball Position: (%.0f, %.0f)", ballX, ballY), 10, 60, 20, GRAY);
        
        // Show "BOUNCE!" text when timer is active
        if (bounceDisplayTimer > 0) {
            // Calculate alpha (transparency) for fade effect
            // Start at 255 (fully opaque) and fade to 0
            unsigned char alpha = static_cast<unsigned char>(
                255 * bounceDisplayTimer / BOUNCE_DISPLAY_FRAMES
            );
            Color bounceColor = {190, 33, 33, alpha};  // MAROON with variable alpha
            
            DrawText("BOUNCE!", screenWidth / 2 - 60, screenHeight / 2 - 20, 40, bounceColor);
        }
        
        EndDrawing();
    }
    
    // Cleanup
    if (bounceSound.frameCount > 0) {
        UnloadSound(bounceSound);
    }
    if (bounceWave.data != nullptr) {
        UnloadWave(bounceWave);
    }
    CloseAudioDevice();
    CloseWindow();
    
    return 0;
}
```

#### Understanding the Code

**Key Components:**

|Section|Purpose|
|---|---|
|`InitAudioDevice()`|Starts the audio system|
|`LoadSound()` / `LoadSoundFromWave()`|Loads sound effect|
|`PlaySound()`|Plays the loaded sound|
|`IsKeyDown()`|Checks if arrow keys are held|
|`ballX += ballSpeed`|Updates ball position|
|Border collision checks|Prevents ball from leaving screen|
|`bounceDisplayTimer`|Keeps "BOUNCE\!" text visible for multiple frames|
|Fade effect|Text gradually fades out using alpha transparency|
|`TextFormat()`|Creates formatted text string|
|`UnloadSound()` / `CloseAudioDevice()`|Cleans up audio resources|

**Sound System Functions:**

```C++
void InitAudioDevice(void);              // Initialize audio device
void CloseAudioDevice(void);             // Close audio device
bool IsAudioDeviceReady(void);           // Check if audio is ready

// Loading sounds
Sound LoadSound(const char *fileName);   // Load from file (.wav, .ogg, .mp3)
Sound LoadSoundFromWave(Wave wave);      // Create from Wave data
void UnloadSound(Sound sound);           // Free sound memory

// Playing sounds
void PlaySound(Sound sound);             // Play once
void StopSound(Sound sound);             // Stop playing
void PauseSound(Sound sound);            // Pause
void ResumeSound(Sound sound);           // Resume
void SetSoundVolume(Sound sound, float volume);  // 0.0 to 1.0
void SetSoundPitch(Sound sound, float pitch);      // 1.0 = normal

// Wave operations
Wave LoadWave(const char *fileName);     // Load wave from file
void UnloadWave(Wave wave);              // Free wave data
```

**How the Collision Detection Works:**

1. Store the ball's position before moving

2. Update position based on key presses

3. Check if ball intersects with any screen border

4. If collision detected:

    - Clamp position to stay within bounds

    - Play the bounce sound

    - Reset the `bounceDisplayTimer` to show "BOUNCE\!" text

**Timer and Fade Effect:**
Instead of showing "BOUNCE\!" for just one frame \(which is too fast to see\), we use a timer system:

```C++
// When collision happens:
bounceDisplayTimer = 45;  // Show text for 45 frames (~0.75 seconds)

// Each frame, decrease timer:
if (bounceDisplayTimer > 0) bounceDisplayTimer--;

// Draw text while timer is active:
if (bounceDisplayTimer > 0) {
    // Calculate fade based on remaining time
    unsigned char alpha = 255 * bounceDisplayTimer / 45;
    DrawText("BOUNCE!", x, y, 40, {190, 33, 33, alpha});
}
```

The alpha value makes the text fade out gradually \- it starts fully opaque \(255\) and becomes more transparent until it disappears\.

**Try Modifying:**

- Change `ballSpeed` to make it move faster/slower

- Change `ballRadius` to make the ball bigger/smaller

- Change the color from `RED` to another color

- Add diagonal movement \(check two keys at once\)

- Add multiple balls

- Use `IsKeyPressed()` instead of `IsKeyDown()` for step\-by\-step movement

---

## Chapter 2: Drawing the Chessboard

Let's start by creating a simple chessboard using rectangles\.

### Step 1: Basic Chessboard

```C++
#include "raylib.h"

int main() {
    const int screenWidth = 800;
    const int screenHeight = 800;
    const int squareSize = 100;  // Each square is 100x100 pixels
    
    InitWindow(screenWidth, screenHeight, "Chess Board - Step 1");
    SetTargetFPS(60);
    
    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);
        
        // Draw 8x8 grid
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                // Determine color: alternate between light and dark
                Color squareColor;
                if ((row + col) % 2 == 0) {
                    squareColor = {240, 217, 181, 255};  // Light wood color
                } else {
                    squareColor = {181, 136, 99, 255};   // Dark wood color
                }
                
                // Calculate position
                int x = col * squareSize;
                int y = row * squareSize;
                
                // Draw the square
                DrawRectangle(x, y, squareSize, squareSize, squareColor);
            }
        }
        
        EndDrawing();
    }
    
    CloseWindow();
    return 0;
}
```

### Understanding the Code

**The Pattern Logic:**

```C++
if ((row + col) % 2 == 0)
```

This creates the checkerboard pattern:

- When `row + col` is even → light color

- When `row + col` is odd → dark color

**Example:**

- Row 0, Col 0: 0\+0=0 \(even\) → Light

- Row 0, Col 1: 0\+1=1 \(odd\) → Dark

- Row 1, Col 0: 1\+0=1 \(odd\) → Dark

- Row 1, Col 1: 1\+1=2 \(even\) → Light

### Step 2: Add Border and Labels

Let's enhance the board with coordinates \(a\-h, 1\-8\):

```C++
#include "raylib.h"

int main() {
    const int squareSize = 100;
    const int boardOffset = 50;  // Space for labels
    const int screenWidth = squareSize * 8 + boardOffset * 2;
    const int screenHeight = squareSize * 8 + boardOffset * 2;
    
    InitWindow(screenWidth, screenHeight, "Chess Board - Step 2");
    SetTargetFPS(60);
    
    // Colors
    Color lightSquare = {240, 217, 181, 255};
    Color darkSquare = {181, 136, 99, 255};
    Color borderColor = {64, 64, 64, 255};
    
    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);
        
        // Draw border background
        DrawRectangle(0, 0, screenWidth, screenHeight, borderColor);
        
        // Draw squares
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                Color squareColor = ((row + col) % 2 == 0) ? lightSquare : darkSquare;
                int x = boardOffset + col * squareSize;
                int y = boardOffset + row * squareSize;
                DrawRectangle(x, y, squareSize, squareSize, squareColor);
            }
        }
        
        // Draw file labels (a-h) at the bottom
        for (int col = 0; col < 8; col++) {
            char label[2] = {'a' + col, '\0'};
            int x = boardOffset + col * squareSize + squareSize/2 - 5;
            int y = screenHeight - boardOffset + 15;
            DrawText(label, x, y, 20, WHITE);
        }
        
        // Draw rank labels (1-8) on the left
        for (int row = 0; row < 8; row++) {
            char label[2] = {'8' - row, '\0'};  // 8 at top, 1 at bottom
            int x = boardOffset - 30;
            int y = boardOffset + row * squareSize + squareSize/2 - 10;
            DrawText(label, x, y, 20, WHITE);
        }
        
        EndDrawing();
    }
    
    CloseWindow();
    return 0;
}
```

---

## Chapter 3: Chess Piece Representation

Before loading images, let's understand how to represent pieces\. We'll use a simple approach with character codes\.

### 3\.1 Piece Representation

```C++
// Piece types (using single characters)
// Uppercase = White, Lowercase = Black
// K/k = King, Q/q = Queen, R/r = Rook, B/b = Bishop, N/n = Knight, P/p = Pawn

char board[8][8] = {
    {'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'},  // Black back rank
    {'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'},  // Black pawns
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},  // Empty
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},  // Empty
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},  // Empty
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},  // Empty
    {'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'},  // White pawns
    {'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'}   // White back rank
};
```

### 3\.2 Loading Piece Images

For a polished look, we need piece images\. You can download free chess piece images from:

- Wikimedia Commons \(SVG chess pieces\)

- OpenGameArt\.org

- Or create your own simple images

**Recommended**: Use 60x60 or 64x64 PNG images with transparent backgrounds\.

**File naming convention:**

```Plaintext
pieces/
├── w_king.png    // White king
├── w_queen.png   // White queen
├── w_rook.png    // White rook
├── w_bishop.png  // White bishop
├── w_knight.png  // White knight
├── w_pawn.png    // White pawn
├── b_king.png    // Black king
├── b_queen.png   // Black queen
├── b_rook.png    // Black rook
├── b_bishop.png  // Black bishop
├── b_knight.png  // Black knight
└── b_pawn.png    // Black pawn
```

### Step 3: Drawing Pieces on the Board

```C++
#include "raylib.h"
#include <string>

// Convert piece character to filename
std::string GetPieceFilename(char piece) {
    std::string prefix = (piece >= 'A' && piece <= 'Z') ? "w_" : "b_";
    std::string name;
    
    switch (tolower(piece)) {
        case 'k': name = "king"; break;
        case 'q': name = "queen"; break;
        case 'r': name = "rook"; break;
        case 'b': name = "bishop"; break;
        case 'n': name = "knight"; break;
        case 'p': name = "pawn"; break;
        default: return "";
    }
    
    return "pieces/" + prefix + name + ".png";
}

int main() {
    const int squareSize = 100;
    const int boardOffset = 50;
    const int screenWidth = squareSize * 8 + boardOffset * 2;
    const int screenHeight = squareSize * 8 + boardOffset * 2;
    
    InitWindow(screenWidth, screenHeight, "Chess Board - Step 3: Pieces");
    SetTargetFPS(60);
    
    // Initialize board
    char board[8][8] = {
        {'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'},
        {'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'},
        {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
        {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
        {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
        {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
        {'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'},
        {'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'}
    };
    
    // Load all piece textures
    Texture2D pieceTextures[12];  // 6 piece types x 2 colors
    std::string pieceFiles[] = {
        "pieces/w_king.png", "pieces/w_queen.png", "pieces/w_rook.png",
        "pieces/w_bishop.png", "pieces/w_knight.png", "pieces/w_pawn.png",
        "pieces/b_king.png", "pieces/b_queen.png", "pieces/b_rook.png",
        "pieces/b_bishop.png", "pieces/b_knight.png", "pieces/b_pawn.png"
    };
    
    for (int i = 0; i < 12; i++) {
        pieceTextures[i] = LoadTexture(pieceFiles[i].c_str());
    }
    
    // Helper function to get texture index from piece character
    auto GetTextureIndex = [](char piece) -> int {
        bool isWhite = (piece >= 'A' && piece <= 'Z');
        int baseIndex = isWhite ? 0 : 6;
        
        switch (tolower(piece)) {
            case 'k': return baseIndex + 0;
            case 'q': return baseIndex + 1;
            case 'r': return baseIndex + 2;
            case 'b': return baseIndex + 3;
            case 'n': return baseIndex + 4;
            case 'p': return baseIndex + 5;
            default: return -1;
        }
    };
    
    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);
        
        // Draw border
        DrawRectangle(0, 0, screenWidth, screenHeight, DARKGRAY);
        
        // Draw squares
        Color lightSquare = {240, 217, 181, 255};
        Color darkSquare = {181, 136, 99, 255};
        
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                Color squareColor = ((row + col) % 2 == 0) ? lightSquare : darkSquare;
                int x = boardOffset + col * squareSize;
                int y = boardOffset + row * squareSize;
                DrawRectangle(x, y, squareSize, squareSize, squareColor);
                
                // Draw piece if present
                char piece = board[row][col];
                if (piece != ' ') {
                    int texIndex = GetTextureIndex(piece);
                    if (texIndex >= 0) {
                        // Center the piece in the square
                        Texture2D tex = pieceTextures[texIndex];
                        int pieceX = x + (squareSize - tex.width) / 2;
                        int pieceY = y + (squareSize - tex.height) / 2;
                        DrawTexture(tex, pieceX, pieceY, WHITE);
                    }
                }
            }
        }
        
        // Draw labels (simplified)
        for (int col = 0; col < 8; col++) {
            char label[2] = {'a' + col, '\0'};
            DrawText(label, boardOffset + col * squareSize + 40, 
                     screenHeight - 35, 20, WHITE);
        }
        for (int row = 0; row < 8; row++) {
            char label[2] = {'8' - row, '\0'};
            DrawText(label, 15, boardOffset + row * squareSize + 35, 20, WHITE);
        }
        
        EndDrawing();
    }
    
    // Unload textures
    for (int i = 0; i < 12; i++) {
        UnloadTexture(pieceTextures[i]);
    }
    
    CloseWindow();
    return 0;
}
```

**Important**: Place your piece images in a `pieces/` folder relative to your executable\.

---

## Chapter 4: Interactive Piece Movement

Now let's make the pieces movable with mouse interaction\!

### Key Concepts

1. **Selecting a piece**: Click on a square with a piece

2. **Dragging**: Move the piece with the mouse

3. **Dropping**: Release to place the piece on a new square

4. **Highlighting**: Show which square is selected

### Step 4: Basic Piece Selection and Movement

```C++
#include "raylib.h"
#include <string>

// Board state
char board[8][8] = {
    {'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'},
    {'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'},
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
    {'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'},
    {'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'}
};

// Game state
struct GameState {
    int selectedRow = -1;    // -1 means no selection
    int selectedCol = -1;
    bool isDragging = false;
    int dragPieceX = 0;        // Screen coordinates while dragging
    int dragPieceY = 0;
    char draggedPiece = ' '; // The piece being dragged
};

// Convert screen coordinates to board coordinates
bool ScreenToBoard(int screenX, int screenY, int boardOffset, int squareSize, 
                   int& outRow, int& outCol) {
    int relativeX = screenX - boardOffset;
    int relativeY = screenY - boardOffset;
    
    // Check if within board bounds
    if (relativeX < 0 || relativeX >= squareSize * 8) return false;
    if (relativeY < 0 || relativeY >= squareSize * 8) return false;
    
    outCol = relativeX / squareSize;
    outRow = relativeY / squareSize;
    return true;
}

int main() {
    const int squareSize = 100;
    const int boardOffset = 50;
    const int screenWidth = squareSize * 8 + boardOffset * 2;
    const int screenHeight = squareSize * 8 + boardOffset * 2;
    
    InitWindow(screenWidth, screenHeight, "Chess - Step 4: Moving Pieces");
    SetTargetFPS(60);
    
    GameState state;
    
    // Load textures (same as before)
    Texture2D pieceTextures[12];
    std::string pieceFiles[] = {
        "pieces/w_king.png", "pieces/w_queen.png", "pieces/w_rook.png",
        "pieces/w_bishop.png", "pieces/w_knight.png", "pieces/w_pawn.png",
        "pieces/b_king.png", "pieces/b_queen.png", "pieces/b_rook.png",
        "pieces/b_bishop.png", "pieces/b_knight.png", "pieces/b_pawn.png"
    };
    for (int i = 0; i < 12; i++) {
        pieceTextures[i] = LoadTexture(pieceFiles[i].c_str());
    }
    
    auto GetTextureIndex = [](char piece) -> int {
        bool isWhite = (piece >= 'A' && piece <= 'Z');
        int baseIndex = isWhite ? 0 : 6;
        switch (tolower(piece)) {
            case 'k': return baseIndex + 0;
            case 'q': return baseIndex + 1;
            case 'r': return baseIndex + 2;
            case 'b': return baseIndex + 3;
            case 'n': return baseIndex + 4;
            case 'p': return baseIndex + 5;
            default: return -1;
        }
    };
    
    while (!WindowShouldClose()) {
        // --- INPUT HANDLING ---
        Vector2 mousePos = GetMousePosition();
        int mouseRow, mouseCol;
        bool onBoard = ScreenToBoard(mousePos.x, mousePos.y, boardOffset, 
                                     squareSize, mouseRow, mouseCol);
        
        // Mouse button pressed - try to select a piece
        if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON) && onBoard) {
            char piece = board[mouseRow][mouseCol];
            if (piece != ' ') {
                state.isDragging = true;
                state.draggedPiece = piece;
                state.selectedRow = mouseRow;
                state.selectedCol = mouseCol;
                board[mouseRow][mouseCol] = ' ';  // Remove from board temporarily
            }
        }
        
        // Mouse button released - drop the piece
        if (IsMouseButtonReleased(MOUSE_LEFT_BUTTON) && state.isDragging) {
            if (onBoard) {
                // Place piece at new position
                board[mouseRow][mouseCol] = state.draggedPiece;
            } else {
                // Drop off board - return to original position
                board[state.selectedRow][state.selectedCol] = state.draggedPiece;
            }
            
            // Reset drag state
            state.isDragging = false;
            state.draggedPiece = ' ';
            state.selectedRow = -1;
            state.selectedCol = -1;
        }
        
        // Update drag position
        if (state.isDragging) {
            state.dragPieceX = mousePos.x - squareSize / 2;
            state.dragPieceY = mousePos.y - squareSize / 2;
        }
        
        // --- DRAWING ---
        BeginDrawing();
        ClearBackground(RAYWHITE);
        
        // Draw border
        DrawRectangle(0, 0, screenWidth, screenHeight, DARKGRAY);
        
        // Draw squares
        Color lightSquare = {240, 217, 181, 255};
        Color darkSquare = {181, 136, 99, 255};
        Color highlightColor = {255, 255, 0, 100};  // Yellow semi-transparent
        
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                int x = boardOffset + col * squareSize;
                int y = boardOffset + row * squareSize;
                
                // Draw square
                Color squareColor = ((row + col) % 2 == 0) ? lightSquare : darkSquare;
                DrawRectangle(x, y, squareSize, squareSize, squareColor);
                
                // Highlight selected square
                if (row == state.selectedRow && col == state.selectedCol) {
                    DrawRectangle(x, y, squareSize, squareSize, highlightColor);
                }
                
                // Draw piece (only if not being dragged)
                char piece = board[row][col];
                if (piece != ' ') {
                    int texIndex = GetTextureIndex(piece);
                    if (texIndex >= 0) {
                        Texture2D tex = pieceTextures[texIndex];
                        int pieceX = x + (squareSize - tex.width) / 2;
                        int pieceY = y + (squareSize - tex.height) / 2;
                        DrawTexture(tex, pieceX, pieceY, WHITE);
                    }
                }
            }
        }
        
        // Draw dragged piece at mouse position
        if (state.isDragging) {
            int texIndex = GetTextureIndex(state.draggedPiece);
            if (texIndex >= 0) {
                DrawTexture(pieceTextures[texIndex], state.dragPieceX, 
                           state.dragPieceY, WHITE);
            }
        }
        
        // Draw instructions
        DrawText("Click and drag pieces to move them", 10, 10, 20, DARKGRAY);
        
        EndDrawing();
    }
    
    // Cleanup
    for (int i = 0; i < 12; i++) {
        UnloadTexture(pieceTextures[i]);
    }
    CloseWindow();
    return 0;
}
```

### Understanding the Movement Logic

**1\. Selection Phase:**

```C++
if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON) && onBoard) {
    char piece = board[mouseRow][mouseCol];
    if (piece != ' ') {
        state.isDragging = true;
        state.draggedPiece = piece;
        board[mouseRow][mouseCol] = ' ';  // Temporarily remove from board
    }
}
```

**2\. Dragging Phase:**

- Piece follows mouse cursor

- Original square is highlighted

**3\. Drop Phase:**

```C++
if (IsMouseButtonReleased(MOUSE_LEFT_BUTTON) && state.isDragging) {
    if (onBoard) {
        board[mouseRow][mouseCol] = state.draggedPiece;  // Place at new position
    } else {
        board[state.selectedRow][state.selectedCol] = state.draggedPiece;  // Return
    }
    state.isDragging = false;
}
```

---

## Chapter 5: Visual Enhancements

Let's add visual polish to make the game look better\.

### Step 5: Highlighting Valid Moves and Hover Effects

```C++
#include "raylib.h"
#include <string>
#include <cmath>

char board[8][8] = {
    {'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'},
    {'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'},
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
    {'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'},
    {'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'}
};

struct GameState {
    int selectedRow = -1;
    int selectedCol = -1;
    bool isDragging = false;
    int dragPieceX = 0;
    int dragPieceY = 0;
    char draggedPiece = ' ';
    int hoverRow = -1;    // Current square under mouse
    int hoverCol = -1;
};

bool ScreenToBoard(int screenX, int screenY, int boardOffset, int squareSize,
                   int& outRow, int& outCol) {
    int relativeX = screenX - boardOffset;
    int relativeY = screenY - boardOffset;
    if (relativeX < 0 || relativeX >= squareSize * 8) return false;
    if (relativeY < 0 || relativeY >= squareSize * 8) return false;
    outCol = relativeX / squareSize;
    outRow = relativeY / squareSize;
    return true;
}

// Draw a rounded rectangle (using multiple rectangles and circles)
void DrawRoundedRect(int x, int y, int width, int height, int radius, Color color) {
    DrawRectangle(x + radius, y, width - 2*radius, height, color);
    DrawRectangle(x, y + radius, width, height - 2*radius, color);
    DrawCircle(x + radius, y + radius, radius, color);
    DrawCircle(x + width - radius, y + radius, radius, color);
    DrawCircle(x + radius, y + height - radius, radius, color);
    DrawCircle(x + width - radius, y + height - radius, radius, color);
}

int main() {
    const int squareSize = 100;
    const int boardOffset = 60;
    const int screenWidth = squareSize * 8 + boardOffset * 2;
    const int screenHeight = squareSize * 8 + boardOffset * 2;
    
    InitWindow(screenWidth, screenHeight, "Chess - Step 5: Visual Polish");
    SetTargetFPS(60);
    
    GameState state;
    
    // Colors
    Color lightSquare = {240, 217, 181, 255};
    Color darkSquare = {181, 136, 99, 255};
    Color borderColor = {48, 46, 43, 255};
    Color hoverColor = {255, 255, 255, 40};      // Subtle white glow
    Color selectColor = {255, 255, 0, 60};       // Yellow highlight
    Color validMoveColor = {0, 255, 0, 40};      // Green for valid moves
    
    // Load textures
    Texture2D pieceTextures[12];
    std::string pieceFiles[] = {
        "pieces/w_king.png", "pieces/w_queen.png", "pieces/w_rook.png",
        "pieces/w_bishop.png", "pieces/w_knight.png", "pieces/w_pawn.png",
        "pieces/b_king.png", "pieces/b_queen.png", "pieces/b_rook.png",
        "pieces/b_bishop.png", "pieces/b_knight.png", "pieces/b_pawn.png"
    };
    for (int i = 0; i < 12; i++) {
        pieceTextures[i] = LoadTexture(pieceFiles[i].c_str());
    }
    
    auto GetTextureIndex = [](char piece) -> int {
        bool isWhite = (piece >= 'A' && piece <= 'Z');
        int baseIndex = isWhite ? 0 : 6;
        switch (tolower(piece)) {
            case 'k': return baseIndex + 0;
            case 'q': return baseIndex + 1;
            case 'r': return baseIndex + 2;
            case 'b': return baseIndex + 3;
            case 'n': return baseIndex + 4;
            case 'p': return baseIndex + 5;
            default: return -1;
        }
    };
    
    while (!WindowShouldClose()) {
        // --- INPUT HANDLING ---
        Vector2 mousePos = GetMousePosition();
        int mouseRow, mouseCol;
        bool onBoard = ScreenToBoard(mousePos.x, mousePos.y, boardOffset,
                                     squareSize, mouseRow, mouseCol);
        
        // Update hover state
        if (onBoard) {
            state.hoverRow = mouseRow;
            state.hoverCol = mouseCol;
        } else {
            state.hoverRow = -1;
            state.hoverCol = -1;
        }
        
        // Mouse button pressed
        if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON) && onBoard) {
            char piece = board[mouseRow][mouseCol];
            if (piece != ' ') {
                state.isDragging = true;
                state.draggedPiece = piece;
                state.selectedRow = mouseRow;
                state.selectedCol = mouseCol;
                board[mouseRow][mouseCol] = ' ';
            }
        }
        
        // Mouse button released
        if (IsMouseButtonReleased(MOUSE_LEFT_BUTTON) && state.isDragging) {
            if (onBoard) {
                board[mouseRow][mouseCol] = state.draggedPiece;
            } else {
                board[state.selectedRow][state.selectedCol] = state.draggedPiece;
            }
            state.isDragging = false;
            state.draggedPiece = ' ';
            state.selectedRow = -1;
            state.selectedCol = -1;
        }
        
        if (state.isDragging) {
            state.dragPieceX = mousePos.x - squareSize / 2;
            state.dragPieceY = mousePos.y - squareSize / 2;
        }
        
        // --- DRAWING ---
        BeginDrawing();
        ClearBackground(RAYWHITE);
        
        // Draw outer border with rounded corners
        DrawRectangle(0, 0, screenWidth, screenHeight, borderColor);
        
        // Draw inner board background
        int boardSize = squareSize * 8;
        DrawRectangle(boardOffset - 5, boardOffset - 5, 
                      boardSize + 10, boardSize + 10, borderColor);
        
        // Draw squares with highlights
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                int x = boardOffset + col * squareSize;
                int y = boardOffset + row * squareSize;
                
                // Base square color
                Color squareColor = ((row + col) % 2 == 0) ? lightSquare : darkSquare;
                DrawRectangle(x, y, squareSize, squareSize, squareColor);
                
                // Hover effect
                if (row == state.hoverRow && col == state.hoverCol && !state.isDragging) {
                    DrawRectangle(x, y, squareSize, squareSize, hoverColor);
                }
                
                // Selected square highlight
                if (row == state.selectedRow && col == state.selectedCol) {
                    DrawRectangle(x, y, squareSize, squareSize, selectColor);
                    // Draw border around selected square
                    DrawRectangleLines(x, y, squareSize, squareSize, YELLOW);
                }
                
                // Draw piece
                char piece = board[row][col];
                if (piece != ' ') {
                    int texIndex = GetTextureIndex(piece);
                    if (texIndex >= 0) {
                        Texture2D tex = pieceTextures[texIndex];
                        int pieceX = x + (squareSize - tex.width) / 2;
                        int pieceY = y + (squareSize - tex.height) / 2;
                        DrawTexture(tex, pieceX, pieceY, WHITE);
                    }
                }
            }
        }
        
        // Draw dragged piece (larger and centered on mouse)
        if (state.isDragging) {
            int texIndex = GetTextureIndex(state.draggedPiece);
            if (texIndex >= 0) {
                Texture2D tex = pieceTextures[texIndex];
                // Scale up slightly while dragging
                float scale = 1.1f;
                int scaledWidth = tex.width * scale;
                int scaledHeight = tex.height * scale;
                int drawX = mousePos.x - scaledWidth / 2;
                int drawY = mousePos.y - scaledHeight / 2;
                
                // Draw shadow
                DrawRectangle(drawX + 5, drawY + 5, scaledWidth, scaledHeight,
                           {0, 0, 0, 100});
                // Draw scaled piece
                DrawTextureEx(tex, {float(drawX), float(drawY)}, 0, scale, WHITE);
            }
        }
        
        // Draw coordinates
        for (int col = 0; col < 8; col++) {
            char fileLabel[2] = {'a' + col, '\0'};
            DrawText(fileLabel, boardOffset + col * squareSize + squareSize/2 - 5,
                     boardSize + boardOffset + 10, 20, WHITE);
        }
        for (int row = 0; row < 8; row++) {
            char rankLabel[2] = {'8' - row, '\0'};
            DrawText(rankLabel, boardOffset - 30,
                     boardOffset + row * squareSize + squareSize/2 - 10, 20, WHITE);
        }
        
        // Draw instructions
        DrawText("Hover to preview, click and drag to move pieces",
                 boardOffset, 15, 20, WHITE);
        
        EndDrawing();
    }
    
    for (int i = 0; i < 12; i++) {
        UnloadTexture(pieceTextures[i]);
    }
    CloseWindow();
    return 0;
}
```

---

## Chapter 6: Complete Chess Board Application

Here's the final, complete code with all features:

### Features Summary

- Chessboard with proper colors

- All pieces in starting positions

- Click and drag to move pieces

- Hover highlighting

- Selected square highlighting

- Visual polish \(shadows, borders\)

- Coordinates display

```C++
#include "raylib.h"
#include <string>

// ============================================================================
// CONSTANTS AND CONFIGURATION
// ============================================================================
const int SQUARE_SIZE = 100;
const int BOARD_OFFSET = 60;
const int SCREEN_WIDTH = SQUARE_SIZE * 8 + BOARD_OFFSET * 2;
const int SCREEN_HEIGHT = SQUARE_SIZE * 8 + BOARD_OFFSET * 2;

// Colors
const Color COLOR_LIGHT_SQUARE = {240, 217, 181, 255};
const Color COLOR_DARK_SQUARE = {181, 136, 99, 255};
const Color COLOR_BORDER = {48, 46, 43, 255};
const Color COLOR_HOVER = {255, 255, 255, 40};
const Color COLOR_SELECT = {255, 255, 0, 60};

// ============================================================================
// GAME STATE
// ============================================================================
struct ChessGame {
    char board[8][8];
    int selectedRow = -1;
    int selectedCol = -1;
    bool isDragging = false;
    Vector2 dragPosition = {0, 0};
    char draggedPiece = ' ';
    int hoverRow = -1;
    int hoverCol = -1;
    Texture2D pieceTextures[12];
    
    void InitializeBoard() {
        char initial[8][8] = {
            {'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'},
            {'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'},
            {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
            {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
            {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
            {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
            {'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'},
            {'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'}
        };
        for (int r = 0; r < 8; r++)
            for (int c = 0; c < 8; c++)
                board[r][c] = initial[r][c];
    }
    
    void LoadTextures() {
        const char* files[] = {
            "pieces/w_king.png", "pieces/w_queen.png", "pieces/w_rook.png",
            "pieces/w_bishop.png", "pieces/w_knight.png", "pieces/w_pawn.png",
            "pieces/b_king.png", "pieces/b_queen.png", "pieces/b_rook.png",
            "pieces/b_bishop.png", "pieces/b_knight.png", "pieces/b_pawn.png"
        };
        for (int i = 0; i < 12; i++) {
            pieceTextures[i] = LoadTexture(files[i]);
        }
    }
    
    void UnloadTextures() {
        for (int i = 0; i < 12; i++) {
            UnloadTexture(pieceTextures[i]);
        }
    }
    
    int GetTextureIndex(char piece) {
        bool isWhite = (piece >= 'A' && piece <= 'Z');
        int base = isWhite ? 0 : 6;
        switch (tolower(piece)) {
            case 'k': return base + 0;
            case 'q': return base + 1;
            case 'r': return base + 2;
            case 'b': return base + 3;
            case 'n': return base + 4;
            case 'p': return base + 5;
            default: return -1;
        }
    }
};

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================
bool ScreenToBoard(int screenX, int screenY, int& row, int& col) {
    int relX = screenX - BOARD_OFFSET;
    int relY = screenY - BOARD_OFFSET;
    if (relX < 0 || relX >= SQUARE_SIZE * 8) return false;
    if (relY < 0 || relY >= SQUARE_SIZE * 8) return false;
    col = relX / SQUARE_SIZE;
    row = relY / SQUARE_SIZE;
    return true;
}

// ============================================================================
// INPUT HANDLING
// ============================================================================
void HandleInput(ChessGame& game) {
    Vector2 mousePos = GetMousePosition();
    int row, col;
    bool onBoard = ScreenToBoard(mousePos.x, mousePos.y, row, col);
    
    // Update hover
    if (onBoard) {
        game.hoverRow = row;
        game.hoverCol = col;
    } else {
        game.hoverRow = -1;
        game.hoverCol = -1;
    }
    
    // Mouse pressed - select piece
    if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON) && onBoard) {
        char piece = game.board[row][col];
        if (piece != ' ') {
            game.isDragging = true;
            game.draggedPiece = piece;
            game.selectedRow = row;
            game.selectedCol = col;
            game.board[row][col] = ' ';
        }
    }
    
    // Mouse released - drop piece
    if (IsMouseButtonReleased(MOUSE_LEFT_BUTTON) && game.isDragging) {
        if (onBoard) {
            game.board[row][col] = game.draggedPiece;
        } else {
            game.board[game.selectedRow][game.selectedCol] = game.draggedPiece;
        }
        game.isDragging = false;
        game.draggedPiece = ' ';
        game.selectedRow = -1;
        game.selectedCol = -1;
    }
    
    // Update drag position
    if (game.isDragging) {
        game.dragPosition = {mousePos.x - SQUARE_SIZE/2.0f, 
                           mousePos.y - SQUARE_SIZE/2.0f};
    }
}

// ============================================================================
// RENDERING
// ============================================================================
void DrawChessBoard(ChessGame& game) {
    // Border
    DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BORDER);
    
    // Inner board edge
    int boardSize = SQUARE_SIZE * 8;
    DrawRectangle(BOARD_OFFSET - 5, BOARD_OFFSET - 5,
                  boardSize + 10, boardSize + 10, COLOR_BORDER);
    
    // Squares
    for (int row = 0; row < 8; row++) {
        for (int col = 0; col < 8; col++) {
            int x = BOARD_OFFSET + col * SQUARE_SIZE;
            int y = BOARD_OFFSET + row * SQUARE_SIZE;
            
            // Base color
            Color squareColor = ((row + col) % 2 == 0) ? 
                                 COLOR_LIGHT_SQUARE : COLOR_DARK_SQUARE;
            DrawRectangle(x, y, SQUARE_SIZE, SQUARE_SIZE, squareColor);
            
            // Hover effect
            if (row == game.hoverRow && col == game.hoverCol && !game.isDragging) {
                DrawRectangle(x, y, SQUARE_SIZE, SQUARE_SIZE, COLOR_HOVER);
            }
            
            // Selection highlight
            if (row == game.selectedRow && col == game.selectedCol) {
                DrawRectangle(x, y, SQUARE_SIZE, SQUARE_SIZE, COLOR_SELECT);
                DrawRectangleLines(x, y, SQUARE_SIZE, SQUARE_SIZE, YELLOW);
            }
            
            // Piece
            char piece = game.board[row][col];
            if (piece != ' ') {
                int idx = game.GetTextureIndex(piece);
                if (idx >= 0) {
                    Texture2D tex = game.pieceTextures[idx];
                    int px = x + (SQUARE_SIZE - tex.width) / 2;
                    int py = y + (SQUARE_SIZE - tex.height) / 2;
                    DrawTexture(tex, px, py, WHITE);
                }
            }
        }
    }
}

void DrawDraggedPiece(ChessGame& game) {
    if (!game.isDragging) return;
    
    int idx = game.GetTextureIndex(game.draggedPiece);
    if (idx < 0) return;
    
    Texture2D tex = game.pieceTextures[idx];
    float scale = 1.1f;
    int scaledW = tex.width * scale;
    int scaledH = tex.height * scale;
    int drawX = game.dragPosition.x + SQUARE_SIZE/2 - scaledW/2;
    int drawY = game.dragPosition.y + SQUARE_SIZE/2 - scaledH/2;
    
    // Shadow
    DrawRectangle(drawX + 5, drawY + 5, scaledW, scaledH, {0, 0, 0, 100});
    // Scaled piece
    DrawTextureEx(tex, {float(drawX), float(drawY)}, 0, scale, WHITE);
}

void DrawCoordinates() {
    int boardSize = SQUARE_SIZE * 8;
    
    // File labels (a-h)
    for (int col = 0; col < 8; col++) {
        char label[2] = {'a' + col, '\0'};
        DrawText(label, BOARD_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE/2 - 5,
                 BOARD_OFFSET + boardSize + 10, 20, WHITE);
    }
    
    // Rank labels (1-8)
    for (int row = 0; row < 8; row++) {
        char label[2] = {'8' - row, '\0'};
        DrawText(label, BOARD_OFFSET - 30,
                 BOARD_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE/2 - 10, 20, WHITE);
    }
}

// ============================================================================
// MAIN
// ============================================================================
int main() {
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Complete Chess Board Application");
    SetTargetFPS(60);
    
    ChessGame game;
    game.InitializeBoard();
    game.LoadTextures();
    
    while (!WindowShouldClose()) {
        HandleInput(game);
        
        BeginDrawing();
        ClearBackground(RAYWHITE);
        
        DrawChessBoard(game);
        DrawDraggedPiece(game);
        DrawCoordinates();
        
        // Instructions
        DrawText("Click and drag pieces to move them",
                 BOARD_OFFSET, 15, 20, WHITE);
        DrawText("Press ESC to exit", BOARD_OFFSET, SCREEN_HEIGHT - 35, 18, LIGHTGRAY);
        
        EndDrawing();
    }
    
    game.UnloadTextures();
    CloseWindow();
    return 0;
}
```

---

## Chapter 7: Exercises for Further Learning

Now that you have a working chess board, try these exercises:

### Exercise 1: Reset Button

Add a button to reset the board to starting position\.

**Hint**: Use `DrawRectangle()` and `CheckCollisionPointRec()` for button detection\.

### Exercise 2: Sound Effects

Add sounds when picking up and dropping pieces\.

**Hint**: Use `LoadSound()`, `PlaySound()`, `UnloadSound()`\.

### Exercise 3: Last Move Highlight

Highlight the squares of the last move \(from \-\> to\)\.

**Hint**: Store the last move in your game state\.

### Exercise 4: Flip Board

Add a key press \(like 'F'\) to flip the board perspective\.

**Hint**: Change how you calculate `row` when drawing\.

### Exercise 5: Simple Move Validation

Only allow moves to empty squares \(no captures yet\)\.

**Hint**: Check the destination square before placing the piece\.

### Exercise 6: Save/Load Position

Save the current board state to a file and load it later\.

**Hint**: Write the board array to a text file\.

---

## Summary of Raylib Functions Used

|Category|Functions|
|---|---|
|**Window**|`InitWindow()`, `CloseWindow()`, `WindowShouldClose()`, `SetTargetFPS()`|
|**Drawing**|`BeginDrawing()`, `EndDrawing()`, `ClearBackground()`|
|**Shapes**|`DrawRectangle()`, `DrawRectangleLines()`, `DrawCircle()`, `DrawRectangleRec()`|
|**Text**|`DrawText()`|
|**Textures**|`LoadTexture()`, `UnloadTexture()`, `DrawTexture()`, `DrawTextureEx()`|
|**Input**|`GetMousePosition()`, `GetMouseX()`, `GetMouseY()`, `IsMouseButtonPressed()`, `IsMouseButtonReleased()`, `IsKeyPressed()`|
|**Collision**|`CheckCollisionPointRec()`|

---

## Conclusion

Raylib is an excellent library for learning game programming\. Start with simple shapes and text, then gradually add more complexity\. Remember:

- **Read the examples**: They are your best learning resource

- **Experiment**: Change values and see what happens

- **Ask for help**: The community is friendly and supportive

- **Have fun**: Game programming should be enjoyable\!

Happy coding\!

---

*This guide was created for C\+\+ beginners\. If you find any errors or have suggestions for improvement, please share your feedback\.*

