#!/usr/bin/env python3.12
"""Generate the Project Final Report (.docx) for aeacrA rhythm game."""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import os

def set_cell_shading(cell, color):
    shading = cell._element.get_or_add_tcPr()
    shading_elem = shading.makeelement(qn('w:shd'), {
        qn('w:val'): 'clear',
        qn('w:color'): 'auto',
        qn('w:fill'): color
    })
    shading.append(shading_elem)

def add_styled_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(10)
        set_cell_shading(cell, 'F2E6EE')

    # Data rows
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = table.rows[ri + 1].cells[ci]
            cell.text = str(val)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)

    return table

def main():
    doc = Document()

    # ── Styles ──
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing = 1.5

    for level in range(1, 4):
        hs = doc.styles[f'Heading {level}']
        hs.font.name = 'Times New Roman'
        hs.font.color.rgb = RGBColor(0x4A, 0x1A, 0x3A)

    # ================================================================
    # COVER PAGE
    # ================================================================
    for _ in range(4):
        doc.add_paragraph()

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('aeacrA — A C++ Rhythm Game')
    run.bold = True
    run.font.size = Pt(28)
    run.font.color.rgb = RGBColor(0x9B, 0x4D, 0x6A)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('C++ Programming Final Project\n'
                           'Project Final Report')
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.add_paragraph()
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = info.add_run('Name: Guo Jiale (郭嘉乐)\n'
                       'Student ID: 202401xxxx\n'
                       'Date: June 8, 2026')
    run.font.size = Pt(14)

    doc.add_page_break()

    # ================================================================
    # TABLE OF CONTENTS (placeholder)
    # ================================================================
    doc.add_heading('Table of Contents', level=1)
    toc_items = [
        'Part I: Project Proposal',
        '    1.1 Project Overview',
        '    1.2 Objectives',
        '    1.3 Key Features',
        '    1.4 Technology Stack',
        'Part II: Requirements Analysis Report',
        '    2.1 Functional Requirements',
        '    2.2 Non-Functional Requirements',
        '    2.3 Input/Output Specifications',
        'Part III: Design Specification',
        '    3.1 System Architecture',
        '    3.2 Class Design',
        '    3.3 Class Diagram',
        '    3.4 Data Member Descriptions',
        '    3.5 Function Member Descriptions',
        '    3.6 Algorithm Design',
        '    3.7 File I/O Design',
        '    3.8 Software Structure Analysis',
    ]
    for item in toc_items:
        p = doc.add_paragraph(item)
        p.paragraph_format.space_after = Pt(2)
        for r in p.runs:
            r.font.size = Pt(11)

    doc.add_page_break()

    # ================================================================
    # PART I: PROJECT PROPOSAL
    # ================================================================
    doc.add_heading('Part I: Project Proposal', level=1)

    doc.add_heading('1.1 Project Overview', level=2)
    doc.add_paragraph(
        'aeacrA is a 6-lane rhythm game developed in C++17 using the raylib graphics library. '
        'The player presses keys (S, D, F, J, K, L) in time with musical notes that scroll down '
        'a perspective-projected track toward a hit line. The game features real-time audio analysis '
        'for automatic chart generation, a visual song selection menu, particle effects, scoring, '
        'and combo systems. The project demonstrates core C++ concepts including class-based design, '
        'file I/O with JSON charts, multi-file project structure, and multimedia programming.'
    )

    doc.add_heading('1.2 Objectives', level=2)
    objectives = [
        'Design and implement a fully functional rhythm game with polished visuals and audio.',
        'Apply C++ object-oriented programming principles: encapsulation, class composition, and clean interfaces.',
        'Implement multi-file project structure with separate .h and .cpp files for each module.',
        'Handle file I/O for loading and saving chart data in JSON format.',
        'Integrate third-party libraries (raylib for graphics/audio, aubio for audio analysis).',
        'Create a visually appealing game with perspective rendering, particle effects, and a cohesive aesthetic.',
        'Support audio file import with automatic beat detection and chart generation.',
    ]
    for obj in objectives:
        doc.add_paragraph(obj, style='List Bullet')

    doc.add_heading('1.3 Key Features', level=2)
    features = [
        ('6-Lane Gameplay', 'Notes fall along 6 lanes mapped to keys S, D, F, J, K, L. Two types of notes are supported: Tap notes (press once) and Hold notes (press and hold until the end).'),
        ('Judgment System', 'Four judgment levels based on timing accuracy: PERFECT (±45ms), GREAT (±90ms), GOOD (±140ms), and MISS (beyond threshold). Each judgment awards different points (350/200/100/0).'),
        ('Audio Analysis & Auto-Generation', 'Users can import any MP3/WAV/OGG/FLAC file. The system uses the aubio library to detect BPM and onsets, then generates a playable chart automatically based on spectral features (centroid, bass ratio).'),
        ('Song Library', 'Pre-loaded songs with handcrafted charts, plus a randomly generated demo chart. Users can import their own music and play auto-generated charts.'),
        ('Visual Effects', 'Perspective-projected 3D track, particle explosions on hit, spiral effects, fire effects at high combos, screen flash on PERFECT judgments, floating petals in the background, and beat-synced pulsing.'),
        ('Scoring & Grading', 'Real-time score display, combo counter with scaling animation, and end-of-song results screen with letter grades (S/A/B/C/D).'),
        ('Auto-Demo Mode', 'Press A in song select to watch an automatic perfect play-through of any chart.'),
    ]
    for name, desc in features:
        p = doc.add_paragraph()
        run = p.add_run(f'{name}: ')
        run.bold = True
        p.add_run(desc)

    doc.add_heading('1.4 Technology Stack', level=2)
    add_styled_table(doc,
        ['Component', 'Technology', 'Version / Details'],
        [
            ['Language', 'C++', 'C++17 standard'],
            ['Compiler', 'Clang++', 'Apple Clang (Xcode Command Line Tools)'],
            ['Graphics/Audio', 'raylib', 'Installed via Homebrew'],
            ['Audio Analysis', 'aubio', 'Onset detection, tempo tracking, FFT'],
            ['Build System', 'Make', 'GNU Make with single Makefile'],
            ['Platform', 'macOS', 'Uses CoreVideo, AppKit for file dialogs'],
            ['JSON Parsing', 'Custom', 'Minimal hand-written recursive descent parser'],
            ['File Dialog', 'Cocoa (Obj-C++)', 'NSOpenPanel via FilePicker.mm'],
        ]
    )

    doc.add_page_break()

    # ================================================================
    # PART II: REQUIREMENTS ANALYSIS
    # ================================================================
    doc.add_heading('Part II: Requirements Analysis Report', level=1)

    doc.add_heading('2.1 Functional Requirements', level=2)

    doc.add_heading('2.1.1 Menu System', level=3)
    reqs_menu = [
        ('FR-01', 'The system shall display a main menu with the game title "aeacrA", key labels, and a prompt to press ENTER.'),
        ('FR-02', 'The system shall transition to song selection when ENTER is pressed on the menu.'),
    ]
    add_styled_table(doc, ['ID', 'Requirement'], reqs_menu)

    doc.add_paragraph()
    doc.add_heading('2.1.2 Song Selection', level=3)
    reqs_select = [
        ('FR-03', 'The system shall display a scrollable list of available songs with title and BPM information.'),
        ('FR-04', 'The user shall be able to navigate the song list using UP/DOWN arrow keys or W/S keys.'),
        ('FR-05', 'The system shall start the selected song when ENTER is pressed (manual play mode).'),
        ('FR-06', 'The system shall start an auto-demo play when A is pressed (automatic perfect play).'),
        ('FR-07', 'The system shall allow importing a new audio file when I is pressed, triggering an OS-level file dialog.'),
        ('FR-08', 'The user shall be able to return to the menu by pressing ESC.'),
    ]
    add_styled_table(doc, ['ID', 'Requirement'], reqs_select)

    doc.add_paragraph()
    doc.add_heading('2.1.3 Gameplay', level=3)
    reqs_play = [
        ('FR-09', 'The system shall display a 3-second countdown before gameplay begins.'),
        ('FR-10', 'The system shall render notes scrolling from a vanishing point toward a hit line in perspective projection.'),
        ('FR-11', 'Tap notes shall be judged when the player presses the corresponding lane key within the judgment window.'),
        ('FR-12', 'Hold notes shall require the player to press at the head and release at the tail, with separate head and tail judgments.'),
        ('FR-13', 'The system shall display judgment text (PERFECT/GREAT/GOOD/MISS) with fade-out animation.'),
        ('FR-14', 'The system shall track and display the current score and combo count.'),
        ('FR-15', 'Notes missed due to timing shall automatically be judged as MISS.'),
        ('FR-16', 'The system shall play a tone corresponding to the lane when a note is hit.'),
        ('FR-17', 'The system shall play background music synchronized with the chart.'),
        ('FR-18', 'The system shall spawn particle effects (explosion, spiral, fire) on successful hits.'),
        ('FR-19', 'Pressing ESC during gameplay shall stop the song and return to the menu.'),
    ]
    add_styled_table(doc, ['ID', 'Requirement'], reqs_play)

    doc.add_paragraph()
    doc.add_heading('2.1.4 Results', level=3)
    reqs_result = [
        ('FR-20', 'After all notes are resolved, the system shall display a results screen with PERFECT/GREAT/GOOD/MISS counts, total score, max combo, and a letter grade.'),
        ('FR-21', 'The letter grade shall be: S (>95%), A (>85%), B (>70%), C (>50%), D (≤50%) based on score/max possible score ratio.'),
    ]
    add_styled_table(doc, ['ID', 'Requirement'], reqs_result)

    doc.add_paragraph()
    doc.add_heading('2.1.5 Audio Import & Chart Generation', level=3)
    reqs_import = [
        ('FR-22', 'The system shall present a native OS file dialog for selecting audio files (MP3, WAV, OGG, FLAC, M4A, AAC).'),
        ('FR-23', 'The system shall analyze the audio to detect BPM using aubio tempo tracking.'),
        ('FR-24', 'The system shall detect note onsets and compute spectral features (centroid, bass ratio) for each onset.'),
        ('FR-25', 'The system shall assign notes to lanes based on spectral characteristics and apply section-based variation patterns.'),
        ('FR-26', 'The system shall save the generated chart as a JSON file in the songs/ directory alongside the copied audio.'),
    ]
    add_styled_table(doc, ['ID', 'Requirement'], reqs_import)

    doc.add_heading('2.2 Non-Functional Requirements', level=2)
    nfr = [
        ('NFR-01', 'Performance', 'The game shall maintain 60 FPS during gameplay on a modern Mac.'),
        ('NFR-02', 'Responsiveness', 'Input latency for key presses shall be processed within a single frame (≤16.7ms).'),
        ('NFR-03', 'Compatibility', 'The game shall compile and run on macOS with Homebrew-installed raylib and aubio.'),
        ('NFR-04', 'Code Quality', 'The source code shall be organized into a clear multi-file structure with one class per header/implementation pair.'),
        ('NFR-05', 'Extensibility', 'The chart format (JSON) shall allow easy addition of new songs without modifying source code.'),
    ]
    add_styled_table(doc, ['ID', 'Category', 'Requirement'], nfr)

    doc.add_paragraph()
    doc.add_heading('2.3 Input/Output Specifications', level=2)

    doc.add_heading('2.3.1 User Input', level=3)
    add_styled_table(doc,
        ['Key', 'Context', 'Action'],
        [
            ['S, D, F, J, K, L', 'Gameplay', 'Hit note on lane 0-5'],
            ['ENTER', 'Menu/Select/Result', 'Confirm / Start / Next'],
            ['ESC', 'Select/Playing', 'Back / Quit to menu'],
            ['UP / W', 'Song Select', 'Previous song'],
            ['DOWN / S', 'Song Select', 'Next song'],
            ['A', 'Song Select', 'Start auto-demo mode'],
            ['I', 'Song Select', 'Import audio file'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('2.3.2 Chart File Format (JSON)', level=3)
    doc.add_paragraph(
        'Charts are stored in JSON files with the following structure:'
    )
    code = doc.add_paragraph(
        '{\n'
        '  "title": "Song Title",\n'
        '  "bpm": 140,\n'
        '  "audio": "audio.mp3",       // optional, relative path\n'
        '  "notes": [\n'
        '    {"time": 4.0, "lane": 0},                    // tap note\n'
        '    {"beat": 8, "lane": 1},                      // tap by beat number\n'
        '    {"time": 5.0, "lane": 2, "type": "hold", "end": 6.0},  // hold\n'
        '    {"beat": 10, "lane": 3, "type": "hold", "dur": 2}      // hold by beat duration\n'
        '  ]\n'
        '}'
    )
    for r in code.runs:
        r.font.name = 'Courier New'
        r.font.size = Pt(9)

    doc.add_paragraph(
        'Notes support multiple time formats: absolute "time" in seconds, "beat" numbers (converted via BPM), '
        'and hold notes can specify "end" time, "endBeat", "duration" in seconds, or "dur" in beats. '
        'Lanes are numbered 0-5.'
    )

    doc.add_page_break()

    # ================================================================
    # PART III: DESIGN SPECIFICATION
    # ================================================================
    doc.add_heading('Part III: Design Specification', level=1)

    doc.add_heading('3.1 System Architecture', level=2)
    doc.add_paragraph(
        'The system follows a modular architecture with clear separation of concerns. '
        'The Game class acts as the central controller, coordinating all subsystems through composition. '
        'Each subsystem encapsulates a single responsibility:'
    )

    arch_items = [
        ('Game', 'State machine (MENU → SELECT → IMPORTING → PLAYING → RESULT). Owns and orchestrates all subsystems.'),
        ('Renderer', 'All drawing operations — track, notes, particles, UI, menus. No game logic.'),
        ('AudioManager', 'Sound effect synthesis, music playback, beat synchronization.'),
        ('Chart', 'Note data container with load/save via JSON file I/O.'),
        ('JudgeSystem', 'Timing-based judgment calculation and score tracking.'),
        ('ParticleSystem', 'Visual particle spawning and physics-based updates.'),
        ('InputManager', 'Key event abstraction layer over raylib input.'),
        ('SongManager', 'Song library scanning, audio import, and file management.'),
        ('ChartGenerator', 'Audio analysis using aubio for automatic chart generation.'),
        ('JsonParser', 'Custom recursive descent JSON parser for chart files.'),
    ]
    for name, desc in arch_items:
        p = doc.add_paragraph()
        run = p.add_run(f'{name}: ')
        run.bold = True
        p.add_run(desc)

    doc.add_heading('3.2 Class Design', level=2)
    doc.add_paragraph(
        'The project contains 10 classes/structs organized into separate header and source files. '
        'The class design emphasizes encapsulation (private data with public interfaces), '
        'composition (Game contains all subsystem objects), and single responsibility.'
    )

    doc.add_heading('3.3 Class Diagram', level=2)
    doc.add_paragraph(
        'The following diagram shows the composition relationships between classes. '
        'Game owns instances of all major subsystems. Chart contains Note objects. '
        'SongManager manages SongEntry objects.'
    )

    # Text-based class diagram
    diagram_text = (
        '┌─────────────────────────────────────────────────────────────────┐\n'
        '│                           Game                                  │\n'
        '├─────────────────────────────────────────────────────────────────┤\n'
        '│ - chart_: Chart            - judge_: JudgeSystem               │\n'
        '│ - particles_: ParticleSystem   - audio_: AudioManager          │\n'
        '│ - input_: InputManager     - renderer_: Renderer               │\n'
        '│ - songMgr_: SongManager    - state_: GameState                 │\n'
        '├─────────────────────────────────────────────────────────────────┤\n'
        '│ + run()                                                        │\n'
        '│ - startGame()  - tickMenu()    - tickSelect()                  │\n'
        '│ - tickPlaying() - tickResult() - tickImporting()               │\n'
        '└─────────────────────────────────────────────────────────────────┘\n'
        '       │ 1         │ 1         │ 1         │ 1         │ 1\n'
        '       ▼           ▼           ▼           ▼           ▼\n'
        '  ┌────────┐  ┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐\n'
        '  │ Chart  │  │ Judge  │ │Particle  │ │  Audio   │ │ Renderer │\n'
        '  │        │  │System  │ │ System   │ │ Manager  │ │          │\n'
        '  ├────────┤  ├────────┤ ├──────────┤ ├──────────┤ ├──────────┤\n'
        '  │-notes_ │  │-score_ │ │particles_│ │laneSnd_  │ │petals_   │\n'
        '  │-title_ │  │-combo_ │ │          │ │bgMusic_  │ │          │\n'
        '  │-audio  │  │-counts │ │          │ │          │ │          │\n'
        '  ├────────┤  ├────────┤ ├──────────┤ ├──────────┤ ├──────────┤\n'
        '  │+load   │  │+judge()│ │+spawn*() │ │+init()   │ │+draw*()  │\n'
        '  │+save   │  │+apply()│ │+update() │ │+playLane │ │+beginEnd │\n'
        '  │+generate│ │+apply  │ │+clear()  │ │+loadMusic│ │Frame()   │\n'
        '  │FromFile│  │Hold()  │ │          │ │+playMusic│ │          │\n'
        '  └────────┘  └────────┘ └──────────┘ └──────────┘ └──────────┘\n'
        '       │                                      ▲\n'
        '       │ contains                              │\n'
        '       ▼                                      │ uses\n'
        '  ┌────────┐                           ┌──────────┐\n'
        '  │  Note  │                           │InputMgr  │\n'
        '  │ (struct)│                          ├──────────┤\n'
        '  ├────────┤                           │+pressed  │\n'
        '  │time    │                           │ Lanes()  │\n'
        '  │lane    │                           │+released │\n'
        '  │type    │                           │ Lanes()  │\n'
        '  │endTime │                           │+isKeyDown│\n'
        '  │result  │                           │+enter    │\n'
        '  │holdRes │                           │Pressed() │\n'
        '  │holding │                           │+escape   │\n'
        '  └────────┘                           │Pressed() │\n'
        '                                       └──────────┘\n'
        '\n'
        '  ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐\n'
        '  │SongMgr   │    │Chart      │    │SongEntry │    │JsonParser│\n'
        '  │          │    │Generator  │    │ (struct) │    │          │\n'
        '  ├──────────┤    ├───────────┤    ├──────────┤    ├──────────┤\n'
        '  │-songs_   │    │+analyze() │    │filePath  │    │+parse()  │\n'
        '  ├──────────┤    │(static)   │    │title     │    │parseJson │\n'
        '  │+scanSongs│    └───────────┘    │bpm       │    │(helper)  │\n'
        '  │+import   │         │          │audioPath │    └──────────┘\n'
        '  │  Audio() │         │ uses          ▲           ▲\n'
        '  └──────────┘         │               │           │\n'
        '            ┌──────────┘               │           │\n'
        '            ▼                          │           │\n'
        '       ┌─────────┐  aubio library      │  used by  │\n'
        '       │aubio/   │─────────────────────┘  Chart &   │\n'
        '       │onset    │                        SongMgr   │\n'
        '       │tempo    │──────────────────────────────────┘\n'
        '       │fft      │\n'
        '       └─────────┘\n'
    )

    p = doc.add_paragraph()
    run = p.add_run(diagram_text)
    run.font.name = 'Courier New'
    run.font.size = Pt(7)

    doc.add_heading('3.4 Data Member Descriptions', level=2)

    # Note struct
    doc.add_heading('3.4.1 Note (struct)', level=3)
    add_styled_table(doc,
        ['Member', 'Type', 'Description'],
        [
            ['time', 'float', 'The time (in seconds from song start) when the note should be hit'],
            ['lane', 'int', 'The lane index (0-5) where the note appears. Mapped to keys S,D,F,J,K,L'],
            ['type', 'NoteType', 'Note type: TAP (single press) or HOLD (press and hold)'],
            ['endTime', 'float', 'For HOLD notes, the time when the key should be released'],
            ['result', 'JudgeResult', 'Head judgment result: NONE, PERFECT, GREAT, GOOD, or MISS'],
            ['holdResult', 'JudgeResult', 'Tail judgment for HOLD notes (separate from head)'],
            ['holding', 'bool', 'True if the player is currently holding the key for this note'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.4.2 Chart', level=3)
    add_styled_table(doc,
        ['Member', 'Type', 'Description'],
        [
            ['notes_', 'vector<Note>', 'All notes in the chart, sorted by time'],
            ['title_', 'string', 'Display name of the song/chart'],
            ['audioFile_', 'string', 'Relative path to the audio file (from JSON "audio" field)'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.4.3 JudgeSystem', level=3)
    add_styled_table(doc,
        ['Member', 'Type', 'Description'],
        [
            ['score_', 'int', 'Accumulated score from all judgments'],
            ['combo_', 'int', 'Current consecutive hit count (resets on MISS)'],
            ['maxCombo_', 'int', 'Highest combo achieved in the current play'],
            ['counts_[4]', 'int[4]', 'Count of each judgment type: [PERFECT, GREAT, GOOD, MISS]'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.4.4 AudioManager', level=3)
    add_styled_table(doc,
        ['Member', 'Type', 'Description'],
        [
            ['laneSnd_[6]', 'Sound[6]', 'Synthesized tone for each lane (frequencies: A4-C5)'],
            ['kickSnd_', 'Sound', 'Synthesized kick drum sound for beat metronome'],
            ['hatSnd_', 'Sound', 'Synthesized hi-hat sound for beat metronome'],
            ['nextBeatTime_', 'float', 'Next scheduled beat time for metronome synchronization'],
            ['beatIdx_', 'int', 'Counter for alternating kick/hat patterns'],
            ['bgMusic_', 'Music', 'raylib Music stream for background audio playback'],
            ['musicLoaded_', 'bool', 'Whether background music has been loaded and is playing'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.4.5 ParticleSystem', level=3)
    add_styled_table(doc,
        ['Member', 'Type', 'Description'],
        [
            ['particles_', 'vector<Particle>', 'Active particles with position, velocity, color, lifetime, and size'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.4.6 Game', level=3)
    add_styled_table(doc,
        ['Member', 'Type', 'Description'],
        [
            ['chart_', 'Chart', 'Currently loaded chart data'],
            ['judge_', 'JudgeSystem', 'Scoring and judgment engine'],
            ['particles_', 'ParticleSystem', 'Visual particle effects manager'],
            ['audio_', 'AudioManager', 'Audio playback and synthesis'],
            ['input_', 'InputManager', 'Input event abstraction'],
            ['renderer_', 'Renderer', 'All drawing operations'],
            ['songMgr_', 'SongManager', 'Song library and import manager'],
            ['state_', 'GameState', 'Current game state (MENU/SELECT/IMPORTING/PLAYING/RESULT)'],
            ['gameTime_', 'float', 'Elapsed time since gameplay started'],
            ['bgPhase_', 'float', 'Phase counter for background animations'],
            ['laneFlash_[6]', 'float[6]', 'Flash intensity per lane (decays over time)'],
            ['comboScale_', 'float', 'Current visual scale of the combo counter (animated)'],
            ['screenFlash_', 'float', 'Full-screen white flash intensity'],
            ['beatPulse_', 'float', 'Intensity of beat-synced visual pulse'],
            ['lastJudgeTime_', 'float', 'Time of the most recent judgment (for animation)'],
            ['lastJudge_', 'JudgeResult', 'Type of the most recent judgment'],
            ['keysDown_[6]', 'bool[6]', 'Current key press state per lane'],
            ['chartPath_', 'string', 'Path to the selected chart file'],
            ['audioPath_', 'string', 'Path to the selected audio file'],
            ['selectedSong_', 'int', 'Index of currently selected song in the list'],
            ['selectScroll_', 'float', 'Smooth scroll position for song selection'],
            ['autoplay_', 'bool', 'Whether auto-demo mode is active'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.4.7 Renderer', level=3)
    add_styled_table(doc,
        ['Member', 'Type', 'Description'],
        [
            ['petals_', 'vector<Petal>', 'Background floating petal particles for aesthetic decoration'],
        ]
    )
    doc.add_paragraph(
        'Renderer also contains static helper methods for perspective projection: '
        'perspY(d) converts depth to screen Y, perspX(hx, d) converts horizontal position at depth to screen X, '
        'and noteDepth(note, time) computes the current depth of a note.'
    )

    doc.add_paragraph()
    doc.add_heading('3.4.8 SongManager', level=3)
    add_styled_table(doc,
        ['Member', 'Type', 'Description'],
        [
            ['songs_', 'vector<SongEntry>', 'List of all available songs scanned from disk'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.4.9 SongEntry (struct)', level=3)
    add_styled_table(doc,
        ['Member', 'Type', 'Description'],
        [
            ['filePath', 'string', 'Path to the chart.json file'],
            ['title', 'string', 'Display title of the song'],
            ['bpm', 'float', 'Beats per minute of the song'],
            ['audioPath', 'string', 'Full path to the audio file (empty if no audio)'],
        ]
    )

    doc.add_heading('3.5 Function Member Descriptions', level=2)

    doc.add_heading('3.5.1 Game', level=3)
    add_styled_table(doc,
        ['Function', 'Description'],
        [
            ['void run()', 'Main game loop. Initializes window, audio, renderer, and song library. Runs state machine until window close.'],
            ['void startGame()', 'Resets all gameplay state, loads chart from file, initializes audio. Transitions to PLAYING state.'],
            ['void tickMenu()', 'Renders menu screen, waits for ENTER to go to SELECT.'],
            ['void tickSelect()', 'Handles song list navigation, play/start/import inputs. Renders selection screen.'],
            ['void tickImporting()', 'Manages audio import flow: file dialog → analysis → chart generation → refresh.'],
            ['void tickPlaying(float dt)', 'Core gameplay update: advances time, updates audio/particles, processes input, judges notes, renders frame.'],
            ['void tickResult()', 'Displays results screen, waits for ENTER to return to menu.'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.5.2 Chart', level=3)
    add_styled_table(doc,
        ['Function', 'Prototype', 'Description'],
        [
            ['generate', 'void generate()', 'Creates a hard-coded demonstration chart with varied patterns (stairs, jacks, streams).'],
            ['loadFromFile', 'bool loadFromFile(const string& path)', 'Parses JSON chart file using JsonParser. Supports multiple note formats (time/beat, hold variants). Sorts notes by time.'],
            ['saveToFile', 'bool saveToFile(const string& path) const', 'Writes chart data to JSON file with title, BPM, and note array.'],
            ['reset', 'void reset()', 'Clears all note data.'],
            ['allDone', 'bool allDone() const', 'Returns true if all notes have been resolved (judged).'],
            ['doneCount', 'int doneCount() const', 'Returns count of resolved notes.'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.5.3 JudgeSystem', level=3)
    add_styled_table(doc,
        ['Function', 'Prototype', 'Description'],
        [
            ['reset', 'void reset()', 'Resets score, combo, and all counts to zero.'],
            ['judge', 'JudgeResult judge(float timeDiff) const', 'Returns judgment based on absolute time difference: PERFECT (≤45ms), GREAT (≤90ms), GOOD (≤140ms), or NONE.'],
            ['apply', 'void apply(JudgeResult j)', 'Updates score (+350/200/100/0), increments combo (or resets on MISS), updates max combo and counts.'],
            ['applyHold', 'void applyHold(JudgeResult head, JudgeResult tail)', 'Judges hold note: applies head judgment, then adds tail bonus if both non-MISS.'],
            ['count', 'int count(JudgeResult j) const', 'Returns the count for a specific judgment type.'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.5.4 AudioManager', level=3)
    add_styled_table(doc,
        ['Function', 'Prototype', 'Description'],
        [
            ['init', 'void init()', 'Synthesizes lane tones (A4-G5), kick drum, and hi-hat using waveform generation.'],
            ['cleanup', 'void cleanup()', 'Unloads all sounds and music, closes audio device.'],
            ['resetBeat', 'void resetBeat()', 'Resets beat metronome timing.'],
            ['playLane', 'void playLane(int lane)', 'Plays the synthesized tone for a specific lane.'],
            ['updateBeat', 'float updateBeat(float gameTime)', 'Checks if a beat has occurred, plays kick/hat sounds, returns pulse intensity.'],
            ['loadMusic', 'bool loadMusic(const string& path)', 'Loads an audio file as background music stream with 70% volume.'],
            ['playMusic', 'void playMusic()', 'Starts background music playback.'],
            ['stopMusic', 'void stopMusic()', 'Stops and unloads background music.'],
            ['updateMusic', 'void updateMusic()', 'Feeds the music stream (required each frame by raylib).'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.5.5 ParticleSystem', level=3)
    add_styled_table(doc,
        ['Function', 'Prototype', 'Description'],
        [
            ['update', 'void update(float dt)', 'Updates particle positions (gravity, drag), removes dead particles.'],
            ['clear', 'void clear()', 'Removes all active particles.'],
            ['spawnExplosion', 'void spawnExplosion(float x, float y, int lane)', 'Creates 25 particles burst in random directions with lane-colored mix.'],
            ['spawnSpiral', 'void spawnSpiral(float x, float y, float time, int lane)', 'Creates 8 particles in a spiral pattern around hit point.'],
            ['spawnFire', 'void spawnFire(float x, float y)', 'Creates 6 upward particles (fire effect), triggered at combo > 10.'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.5.6 Renderer', level=3)
    add_styled_table(doc,
        ['Function', 'Prototype', 'Description'],
        [
            ['init', 'void init()', 'Initializes 50 background petal particles with random properties.'],
            ['drawMenu', 'void drawMenu(float bgPhase)', 'Draws title screen with petals, rotating rings, key labels, and prompt.'],
            ['drawSelect', 'void drawSelect(...)', 'Draws song list with selection highlight, BPM info, and control hints.'],
            ['drawImport', 'void drawImport(...)', 'Draws import screen with status text and progress bar.'],
            ['drawPlaying', '(multiple draw calls)', 'Background → Track → Lanes → BeatLines → Notes → HitLine → Receptors → Particles → Flash → Judgment → UI → Countdown.'],
            ['drawResults', 'void drawResults(...)', 'Draws grade (S/A/B/C/D), score, combo, judgment counts.'],
            ['drawNotes', 'void drawNotes(...)', 'Renders tap notes (with glow trail) and hold notes (gradient body + head/tail markers) in perspective.'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.5.7 SongManager', level=3)
    add_styled_table(doc,
        ['Function', 'Prototype', 'Description'],
        [
            ['scanSongs', 'void scanSongs()', 'Scans charts/ and songs/ directories for .json files. Parses each for title and BPM. Adds a "Random (Generated)" entry.'],
            ['importAudio', 'bool importAudio(const string& audioPath, string& outChartPath)', 'Copies audio to songs/<name>/, analyzes with ChartGenerator, writes chart.json.'],
            ['audioPathFor', 'string audioPathFor(const SongEntry& song) const', 'Returns audio file path for a song entry, searching the chart directory.'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.5.8 ChartGenerator (static methods)', level=3)
    add_styled_table(doc,
        ['Function', 'Prototype', 'Description'],
        [
            ['analyze', 'static bool analyze(const string& audioPath, AudioFeatures& out)', 'Detects BPM via aubio tempo tracking, detects onsets with spectral analysis, assigns lanes based on frequency features, generates hold notes for sustained sounds.'],
        ]
    )

    doc.add_paragraph()
    doc.add_heading('3.5.9 JsonParser', level=3)
    doc.add_paragraph(
        'A hand-written recursive descent JSON parser implemented as a class with internal state. '
        'Supports all JSON types (null, bool, number, string, array, object) with minimal memory allocation. '
        'The JsonValue struct provides operator[] for object/array access, asNum() for safe number conversion, '
        'and asStr() for string access. The parseJson() free function creates a parser and parses a string in one call.'
    )

    doc.add_heading('3.6 Algorithm Design', level=2)

    doc.add_heading('3.6.1 Note Judgment Algorithm', level=3)
    doc.add_paragraph(
        'For each key press event, the system scans all unresolved notes on the pressed lane to find the closest '
        'one within the GOOD judgment window (±140ms). The algorithm:'
    )
    steps = [
        'Iterate over all notes, filtering by lane and unresolved status.',
        'Compute absolute time difference |gameTime - note.time| for each candidate.',
        'Select the note with the smallest time difference (best match).',
        'Classify the difference into PERFECT (≤45ms), GREAT (≤90ms), GOOD (≤140ms).',
        'If the note is a HOLD type, mark it as "holding" and defer tail judgment until key release or endTime.',
    ]
    for i, s in enumerate(steps, 1):
        doc.add_paragraph(f'{i}. {s}')

    doc.add_heading('3.6.2 Chart Generation Algorithm', level=3)
    doc.add_paragraph(
        'The automatic chart generation uses audio signal processing through the aubio library:'
    )
    steps = [
        'BPM Detection: Use aubio_tempo to track beats throughout the audio, collect beat times, compute median inter-beat interval, derive BPM = 60 / median.',
        'Onset Detection: Use aubio_onset to detect note attack events. For each onset, compute spectral features via FFT — spectral centroid (brightness) and bass ratio (low-frequency energy).',
        'Lane Assignment: Map spectral features to lanes — bass-heavy onsets → lanes 0-1, mid-range → lanes 2-3, bright → lanes 4-5. Apply section-based variation patterns to create musical interest.',
        'Hold Note Generation: Create hold notes for low-energy, sustained bass sounds at regular intervals.',
        'Post-processing: Remove taps that overlap with holds on the same lane, deduplicate same-time/same-lane notes, sort by time.',
    ]
    for i, s in enumerate(steps, 1):
        doc.add_paragraph(f'{i}. {s}')

    doc.add_heading('3.6.3 Perspective Rendering', level=3)
    doc.add_paragraph(
        'Notes are rendered with a pseudo-3D perspective effect:'
    )
    steps = [
        'Depth calculation: depth = 1 - (note.time - gameTime) * SCROLL_SPEED / TRACK_LEN. Depth 0 = vanishing point, 1 = hit line.',
        'Y position: perspY(depth) = VP_Y + TRACK_LEN * depth^PERSP (PERSP=1.55 for curvature).',
        'X position: perspX(laneCenter, depth) = VP_X + (laneCenter - VP_X) * depth.',
        'Note width and height scale linearly with depth, creating a convincing 3D tunnel effect.',
    ]
    for i, s in enumerate(steps, 1):
        doc.add_paragraph(f'{i}. {s}')

    doc.add_heading('3.7 File I/O Design', level=2)
    doc.add_paragraph(
        'File I/O is central to the project, used in multiple places:'
    )

    doc.add_heading('3.7.1 Chart Loading (Chart::loadFromFile)', level=3)
    doc.add_paragraph(
        'Reads a JSON file, parses it with the custom JsonParser, extracts title, BPM, audio path, and note data. '
        'Supports multiple note formats (time-based, beat-based, hold variants) for flexibility. '
        'Notes are sorted by time after loading.'
    )

    doc.add_heading('3.7.2 Chart Saving (Chart::saveToFile)', level=3)
    doc.add_paragraph(
        'Writes chart data as formatted JSON with indentation. Outputs title, BPM, and note array with time, lane, type, and end fields.'
    )

    doc.add_heading('3.7.3 Song Import (SongManager::importAudio)', level=3)
    doc.add_paragraph(
        'Copies the source audio file to songs/<name>/audio.<ext>, generates a chart via ChartGenerator::analyze, '
        'and writes the chart as chart.json in the same directory. The songs/ directory structure allows the '
        'scanSongs() function to discover imported songs on subsequent launches.'
    )

    doc.add_heading('3.7.4 Song Scanning (SongManager::scanSongs)', level=3)
    doc.add_paragraph(
        'Scans two directories using POSIX opendir/readdir: charts/ for standalone chart files and songs/ for '
        'imported song directories (each containing chart.json + audio file). For each chart, reads title and BPM '
        'from the JSON file. Also scans for audio files (.mp3, .wav, .ogg, .flac, .m4a, .aac) in each song directory.'
    )

    doc.add_heading('3.8 Software Structure Analysis', level=2)

    doc.add_heading('3.8.1 Module Division', level=3)
    doc.add_paragraph(
        'Each module performs a single task and corresponds to a real-world concept in the game domain:'
    )
    modules = [
        ('Chart', 'Data container for musical notes — no rendering or judgment logic.'),
        ('JudgeSystem', 'Pure scoring logic — no rendering, no audio, no timing.'),
        ('AudioManager', 'Audio-only operations — no game logic, no rendering.'),
        ('Renderer', 'Drawing-only — no game state modification, reads data from other modules.'),
        ('ParticleSystem', 'Visual effect management — physics simulation independent of game rules.'),
        ('InputManager', 'Input abstraction — shields game logic from raylib input API.'),
        ('SongManager', 'File system operations — scanning, importing, copying files.'),
        ('ChartGenerator', 'Audio signal processing — completely independent of game logic.'),
        ('Game', 'Coordinator — delegates to subsystems, contains only state machine logic.'),
    ]
    for name, desc in modules:
        p = doc.add_paragraph()
        run = p.add_run(f'{name}: ')
        run.bold = True
        p.add_run(desc)

    doc.add_heading('3.8.2 Coupling Analysis', level=3)
    doc.add_paragraph(
        'The system has low coupling between modules:'
    )
    coupling = [
        'Game depends on all subsystems, but subsystems do not depend on Game or each other.',
        'Renderer receives data through function parameters (const references), never modifies game state.',
        'JudgeSystem operates on simple float values, independent of Chart or Game.',
        'AudioManager is self-contained — only receives timing information.',
        'SongManager and ChartGenerator interact only during import (SongManager calls ChartGenerator::analyze).',
        'No global variables or global objects are used.',
        'Non-const references and pointers are used only where necessary (e.g., modifying Note state during gameplay).',
    ]
    for c in coupling:
        doc.add_paragraph(c, style='List Bullet')

    doc.add_heading('3.8.3 Encapsulation Analysis', level=3)
    doc.add_paragraph(
        'All class data members are private. Access is through well-defined public interfaces:'
    )
    encap = [
        'Chart exposes notes() as const reference, and note() returns a mutable reference only when needed.',
        'JudgeSystem exposes only score(), combo(), maxCombo(), and count() as const getters.',
        'ParticleSystem exposes particles() as const reference for the renderer.',
        'Config constants are in a namespace with constexpr values — no runtime state.',
        'The only public data members are in plain structs (Note, SongEntry, Particle, Petal) which serve as data transfer objects.',
    ]
    for e in encap:
        doc.add_paragraph(e, style='List Bullet')

    # ── Save ──
    out_path = os.path.join(os.path.dirname(__file__), 'Project_Final_Report.docx')
    doc.save(out_path)
    print(f'Saved: {out_path}')

if __name__ == '__main__':
    main()
