#!/usr/bin/env python3.12
"""Generate the Summary Report (.docx) for aeacrA rhythm game."""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def main():
    doc = Document()

    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing = 1.5
    for lv in range(1, 4):
        doc.styles[f'Heading {lv}'].font.color.rgb = RGBColor(0x4A, 0x1A, 0x3A)

    # ── Cover ──
    for _ in range(5):
        doc.add_paragraph()
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run('aeacrA — Summary Report')
    r.bold = True; r.font.size = Pt(28); r.font.color.rgb = RGBColor(0x9B, 0x4D, 0x6A)
    s = doc.add_paragraph()
    s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = s.add_run('C++ Programming Final Project\nGuo Jiale (郭嘉乐)')
    r.font.size = Pt(16); r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.add_page_break()

    # ── 1. Project Overview ──
    doc.add_heading('1. Project Overview', level=1)
    doc.add_paragraph(
        'aeacrA is a 6-lane rhythm game built in C++17 using raylib for graphics and audio, '
        'and aubio for audio analysis. The project implements a complete game loop with menu navigation, '
        'song selection, gameplay with judgment and scoring, results display, and an audio import system '
        'that generates playable charts from any music file. The game features a polished visual style '
        'with perspective-projected tracks, particle effects, and beat-synced animations.'
    )

    # ── 2. Development Process ──
    doc.add_heading('2. Development Process', level=1)
    doc.add_paragraph(
        'The development followed an iterative approach across approximately 3 weeks:'
    )

    doc.add_heading('2.1 Phase 1: Core Framework', level=2)
    doc.add_paragraph(
        'Established the project structure with separate .h and .cpp files for each module. '
        'Implemented the Game state machine, Config constants, and basic raylib window setup. '
        'Created the Chart data structure with JSON loading using a custom parser. '
        'Built the initial Renderer with perspective projection math.'
    )

    doc.add_heading('2.2 Phase 2: Gameplay Systems', level=2)
    doc.add_paragraph(
        'Implemented the JudgeSystem with timing windows (PERFECT/GREAT/GOOD/MISS) and scoring. '
        'Added InputManager for keyboard event handling. '
        'Created AudioManager with synthesized lane tones and beat metronome. '
        'Implemented note rendering with glow effects and trail animations for both Tap and Hold notes.'
    )

    doc.add_heading('2.3 Phase 3: Visual Polish', level=2)
    doc.add_paragraph(
        'Added the ParticleSystem with explosion, spiral, and fire effects. '
        'Designed the pastel color scheme and cream background aesthetic. '
        'Implemented floating petal particles, rotating ring decorations, and screen flash effects. '
        'Added combo counter scaling animation and beat-synced pulsing.'
    )

    doc.add_heading('2.4 Phase 4: Song Management', level=2)
    doc.add_paragraph(
        'Created SongManager to scan songs/ and charts/ directories. '
        'Implemented audio file import with native macOS file dialog (FilePicker.mm). '
        'Integrated ChartGenerator using aubio for BPM detection, onset detection with spectral analysis, '
        'and automatic lane assignment based on audio features. '
        'Added the song selection menu with scroll and navigation.'
    )

    doc.add_heading('2.5 Phase 5: Polish and Testing', level=2)
    doc.add_paragraph(
        'Added auto-demo mode for previewing charts. '
        'Implemented the results screen with letter grades. '
        'Added countdown timer before gameplay. '
        'Performed manual testing of all features and fixed bugs.'
    )

    # ── 3. Challenges ──
    doc.add_heading('3. Challenges and Solutions', level=1)

    doc.add_heading('3.1 Perspective Projection', level=2)
    doc.add_paragraph(
        'Challenge: Creating a convincing 3D tunnel effect for the note track required non-linear depth mapping. '
        'A simple linear mapping made distant notes too compressed.'
    )
    doc.add_paragraph(
        'Solution: Used a power function (exponent 1.55) for the Y-axis mapping: '
        'perspY(d) = VP_Y + TRACK_LEN × d^1.55. This creates a natural perspective where distant notes '
        'are compressed and close notes spread out, mimicking real-world perspective.'
    )

    doc.add_heading('3.2 Audio Analysis Accuracy', level=2)
    doc.add_paragraph(
        'Challenge: The automatic chart generation needed to produce playable, musically sensible charts '
        'from arbitrary audio files. Initial attempts produced chaotic note patterns.'
    )
    doc.add_paragraph(
        'Solution: Combined multiple audio features for lane assignment — spectral centroid for brightness, '
        'bass ratio for low-frequency content, and energy for note intensity. Added section-based variation '
        'patterns to create musical interest and prevent monotonous patterns. Post-processing removes '
        'overlapping and duplicate notes.'
    )

    doc.add_heading('3.3 JSON Parsing', level=2)
    doc.add_paragraph(
        'Challenge: The project needed to parse chart files in JSON format, but adding a full JSON library '
        'dependency seemed unnecessary for the limited subset required.'
    )
    doc.add_paragraph(
        'Solution: Implemented a minimal recursive descent JSON parser covering the subset needed for charts: '
        'objects, arrays, strings (with escape sequences), numbers, booleans, and null. The parser is ~60 lines '
        'of code and handles all chart formats without external dependencies.'
    )

    doc.add_heading('3.4 Hold Note Judgment', level=2)
    doc.add_paragraph(
        'Challenge: Hold notes require two separate judgments (head press and tail release), '
        'and the player must hold the key continuously. Tracking this state was error-prone.'
    )
    doc.add_paragraph(
        'Solution: Added a "holding" boolean to each Note. When the head is hit, holding=true. '
        'The tail is judged when the key is released (manual) or when gameTime passes endTime (auto-complete). '
        'Separate head and tail judgment results allow independent scoring.'
    )

    doc.add_heading('3.5 Cross-Language Integration', level=2)
    doc.add_paragraph(
        'Challenge: The native file dialog requires macOS Cocoa APIs (Objective-C++), but the rest of the '
        'project is pure C++.'
    )
    doc.add_paragraph(
        'Solution: Isolated the file dialog code in FilePicker.mm (Objective-C++ source). '
        'The Makefile compiles .mm files alongside .cpp files. The C++ header declares a plain C++ function '
        'signature, and the implementation uses Objective-C++ internally. This keeps the cross-language boundary minimal.'
    )

    # ── 4. Achievements ──
    doc.add_heading('4. Achievements', level=1)

    doc.add_heading('4.1 Technical Achievements', level=2)
    achievements = [
        'Built a complete game with 11 source files (13 headers + 11 implementations) in a clean multi-file structure.',
        'Implemented a custom JSON parser covering all types needed for chart loading.',
        'Integrated real-time audio analysis using aubio for automatic chart generation from any music file.',
        'Created a visually polished game with perspective rendering, particle effects, and synchronized animations.',
        'Achieved consistent 60 FPS performance during gameplay.',
        'Implemented the audio import pipeline: file dialog → copy → analyze → generate chart → play, all within the game.',
    ]
    for a in achievements:
        doc.add_paragraph(a, style='List Bullet')

    doc.add_heading('4.2 C++ Concepts Demonstrated', level=2)
    concepts = [
        ('Classes and Encapsulation', '10 classes/structs with private data and public interfaces.'),
        ('Multi-file Structure', 'Each class has a separate .h and .cpp file.'),
        ('File I/O', 'JSON chart loading/saving, audio file copying, directory scanning with POSIX API.'),
        ('Composition', 'Game class composes all subsystems through member objects.'),
        ('Enums', 'JudgeResult and NoteType enums for type-safe state representation.'),
        ('Namespaces', 'Config namespace for compile-time constants.'),
        ('STL Containers', 'vector for notes, particles, and song lists; string for text handling; pair for JSON object entries.'),
        ('Algorithms', 'std::sort for note ordering, std::remove_if for particle cleanup, std::unique for deduplication.'),
        ('Lambda Expressions', 'Used with std::sort, std::remove_if, and std::unique for custom comparisons.'),
        ('constexpr', 'All configuration values are compile-time constants.'),
    ]
    for name, desc in concepts:
        p = doc.add_paragraph()
        r = p.add_run(f'{name}: ')
        r.bold = True
        p.add_run(desc)

    # ── 5. AI Usage ──
    doc.add_heading('5. AI Usage Description', level=1)
    doc.add_paragraph(
        'AI tools (Claude) were used during development in the following ways:'
    )

    doc.add_heading('5.1 Framework Construction', level=2)
    doc.add_paragraph(
        'AI assisted in setting up the initial project structure, including the Makefile configuration '
        'for compiling multiple source files with raylib and aubio dependencies. The multi-file class structure '
        'was designed collaboratively with AI suggestions for module separation.'
    )

    doc.add_heading('5.2 Algorithm Implementation', level=2)
    doc.add_paragraph(
        'The perspective projection algorithm was developed with AI guidance on the mathematical approach '
        '(power function for depth mapping). The audio analysis pipeline (aubio integration for BPM detection, '
        'onset detection, and spectral feature computation) was implemented with AI assistance in understanding '
        'the aubio C API and designing the lane assignment heuristics.'
    )

    doc.add_heading('5.3 Debugging and Optimization', level=2)
    doc.add_paragraph(
        'AI helped debug rendering issues (perspective projection artifacts, particle system performance) '
        'and suggested optimizations for the note scanning loop during gameplay.'
    )

    doc.add_heading('5.4 Understanding and Modification', level=2)
    doc.add_paragraph(
        'All AI-generated code was thoroughly reviewed, understood, and modified before inclusion. '
        'The JSON parser was rewritten for clarity. The particle system parameters were adjusted through '
        'iterative testing. The chart generation algorithm was refined with custom lane assignment logic '
        'and post-processing rules. I fully understand every line of code in the project and can explain '
        'the purpose and behavior of each module.'
    )

    # ── 6. Lessons Learned ──
    doc.add_heading('6. Lessons Learned', level=1)
    lessons = [
        'Multi-file project structure requires careful header management (include guards, forward declarations) to avoid circular dependencies.',
        'Game development involves balancing visual quality with code maintainability — the Renderer is the largest file but is kept separate from all game logic.',
        'Audio signal processing is complex — the aubio library significantly simplified BPM and onset detection, but understanding the results and using them effectively required careful tuning.',
        'File I/O is critical in a game with user-created content — the chart format needed to be flexible enough for both handcrafted and auto-generated charts.',
        'Testing game features requires manual testing — automated unit tests work for pure logic (judgment, parsing) but visual and audio features need human verification.',
    ]
    for l in lessons:
        doc.add_paragraph(l, style='List Bullet')

    # ── 7. Future Improvements ──
    doc.add_heading('7. Possible Future Improvements', level=1)
    improvements = [
        'Add difficulty levels (easy/normal/hard) with different note densities.',
        'Implement a high score system with persistent storage.',
        'Add more visual effects (lane-specific themes, song background images).',
        'Support custom key bindings.',
        'Port to other platforms (Windows, Linux) by replacing FilePicker.mm.',
        'Add a practice mode with speed adjustment.',
    ]
    for imp in improvements:
        doc.add_paragraph(imp, style='List Bullet')

    # ── Save ──
    out_path = os.path.join(os.path.dirname(__file__), 'Summary_Report.docx')
    doc.save(out_path)
    print(f'Saved: {out_path}')

if __name__ == '__main__':
    main()
