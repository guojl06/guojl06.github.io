#!/usr/bin/env python3.12
"""Generate the User Manual (.docx) for aeacrA rhythm game."""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

def add_styled_table(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(10)
        shading = cell._element.get_or_add_tcPr()
        shading.append(shading.makeelement(qn('w:shd'), {
            qn('w:val'): 'clear', qn('w:color'): 'auto', qn('w:fill'): 'F2E6EE'
        }))
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            table.rows[ri + 1].cells[ci].text = str(val)
            for p in table.rows[ri + 1].cells[ci].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)
    return table

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
    r = t.add_run('aeacrA — User Manual')
    r.bold = True; r.font.size = Pt(28); r.font.color.rgb = RGBColor(0x9B, 0x4D, 0x6A)
    s = doc.add_paragraph()
    s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = s.add_run('C++ Rhythm Game\nVersion 1.0')
    r.font.size = Pt(16); r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.add_page_break()

    # ── 1. Introduction ──
    doc.add_heading('1. Introduction', level=1)
    doc.add_paragraph(
        'aeacrA is a 6-lane rhythm game for macOS. Notes scroll down a 3D-perspective track '
        'toward a hit line. Press the corresponding keys in time with the music to score points. '
        'The game features pre-loaded songs, audio import with automatic chart generation, '
        'particle effects, scoring with combo tracking, and an auto-demo mode.'
    )

    # ── 2. System Requirements ──
    doc.add_heading('2. System Requirements', level=1)
    add_styled_table(doc,
        ['Requirement', 'Details'],
        [
            ['Operating System', 'macOS 12.0 (Monterey) or later'],
            ['Compiler', 'Clang++ with C++17 support'],
            ['Libraries', 'raylib (via Homebrew), aubio (via Homebrew)'],
            ['Frameworks', 'OpenGL, Cocoa, IOKit, CoreVideo, AppKit (system provided)'],
            ['Display', '960 × 640 minimum resolution'],
            ['Input', 'Keyboard (S, D, F, J, K, L keys)'],
            ['Audio', 'Audio output device'],
        ]
    )

    # ── 3. Installation ──
    doc.add_heading('3. Installation and Building', level=1)
    doc.add_heading('3.1 Install Dependencies', level=2)
    code = doc.add_paragraph(
        'brew install raylib aubio\n'
    )
    for r in code.runs:
        r.font.name = 'Courier New'; r.font.size = Pt(10)

    doc.add_heading('3.2 Build the Game', level=2)
    doc.add_paragraph('Navigate to the project root directory (containing the Makefile) and run:')
    code = doc.add_paragraph('make\n')
    for r in code.runs:
        r.font.name = 'Courier New'; r.font.size = Pt(10)
    doc.add_paragraph(
        'This produces an executable named "aeacrA" in the project directory.'
    )

    doc.add_heading('3.3 Clean Build', level=2)
    code = doc.add_paragraph('make clean && make\n')
    for r in code.runs:
        r.font.name = 'Courier New'; r.font.size = Pt(10)

    # ── 4. Running the Game ──
    doc.add_heading('4. Running the Game', level=1)
    code = doc.add_paragraph('./aeacrA\n')
    for r in code.runs:
        r.font.name = 'Courier New'; r.font.size = Pt(10)
    doc.add_paragraph(
        'The game window will open at 960×640. Make sure the terminal is in the project directory '
        'so that the songs/ and charts/ folders are accessible.'
    )
    p = doc.add_paragraph()
    r = p.add_run('Important: ')
    r.bold = True
    p.add_run(
        'The working directory must be the project root, because the game looks for '
        '"songs/" and "charts/" relative to the current directory.'
    )

    # ── 5. Game Screens ──
    doc.add_heading('5. Game Screens', level=1)

    doc.add_heading('5.1 Main Menu', level=2)
    doc.add_paragraph(
        'When the game starts, you see the main menu with the game title "aeacrA", '
        'key labels (S D F J K L), and a pulsing "Press ENTER to start" prompt.'
    )
    doc.add_paragraph('Press ENTER to enter song selection.', style='List Bullet')
    doc.add_paragraph('Close the window or press Cmd+Q to quit.', style='List Bullet')

    doc.add_heading('5.2 Song Selection', level=2)
    doc.add_paragraph(
        'The song list shows all available songs with their titles and BPM. '
        'The first entry is "Random (Generated)" which creates a procedural chart.'
    )
    add_styled_table(doc,
        ['Key', 'Action'],
        [
            ['UP / W', 'Move selection up'],
            ['DOWN / S', 'Move selection down'],
            ['ENTER', 'Start playing the selected song (manual mode)'],
            ['A', 'Start auto-demo of the selected song'],
            ['I', 'Import a new audio file from disk'],
            ['ESC', 'Return to main menu'],
        ]
    )

    doc.add_heading('5.3 Importing Songs', level=2)
    doc.add_paragraph(
        'Press I in the song selection screen to open a file dialog. '
        'Select an audio file (MP3, WAV, OGG, FLAC, M4A, or AAC). '
        'The game will:'
    )
    doc.add_paragraph('Copy the audio file to the songs/ directory.', style='List Bullet')
    doc.add_paragraph('Analyze the audio to detect BPM and note onsets.', style='List Bullet')
    doc.add_paragraph('Generate a chart automatically and save it as chart.json.', style='List Bullet')
    doc.add_paragraph(
        'After import completes, press ENTER to return to the song list. '
        'The new song will appear and can be selected for play.'
    )

    doc.add_heading('5.4 Gameplay', level=2)
    doc.add_paragraph(
        'After selecting a song, a 3-second countdown appears (READY → 3 → 2 → 1). '
        'Then notes begin scrolling down the track.'
    )

    doc.add_heading('5.4.1 Lane Key Mapping', level=3)
    add_styled_table(doc,
        ['Lane', 'Key', 'Color'],
        [
            ['0 (leftmost)', 'S', 'Pink'],
            ['1', 'D', 'Blue'],
            ['2', 'F', 'Orange'],
            ['3', 'J', 'Green'],
            ['4', 'K', 'Purple'],
            ['5 (rightmost)', 'L', 'Coral'],
        ]
    )

    doc.add_heading('5.4.2 Note Types', level=3)
    p = doc.add_paragraph()
    r = p.add_run('Tap Notes: ')
    r.bold = True
    p.add_run('Colored rectangles that scroll toward the hit line. Press the corresponding key when the note reaches the receptors at the bottom. One press = one judgment.')

    p = doc.add_paragraph()
    r = p.add_run('Hold Notes: ')
    r.bold = True
    p.add_run('Long bars with a head and tail marker. Press the key when the head reaches the hit line and hold until the tail arrives. You receive two judgments: one for the head (press timing) and one for the tail (release timing).')

    doc.add_heading('5.4.3 Judgment Windows', level=3)
    add_styled_table(doc,
        ['Judgment', 'Timing Window', 'Points'],
        [
            ['PERFECT', '±45 ms', '350'],
            ['GREAT', '±90 ms', '200'],
            ['GOOD', '±140 ms', '100'],
            ['MISS', 'Beyond ±140 ms', '0 (combo resets)'],
        ]
    )

    doc.add_heading('5.4.4 Scoring', level=3)
    doc.add_paragraph(
        'Your score accumulates based on judgment points. A combo counter tracks consecutive '
        'non-MISS judgments. The combo resets to 0 on any MISS. '
        'At high combos (>10), fire particle effects appear on hits.'
    )

    doc.add_heading('5.4.5 Auto-Demo Mode', level=3)
    doc.add_paragraph(
        'When you press A in song select, the game plays the chart automatically with perfect timing. '
        'An "AUTO DEMO" badge appears in the top-right corner. This mode is useful for previewing '
        'a chart before attempting to play it manually. Press ESC to stop the demo.'
    )

    doc.add_heading('5.5 Results Screen', level=2)
    doc.add_paragraph(
        'After all notes are resolved, the results screen shows:'
    )
    doc.add_paragraph('Count of each judgment type (PERFECT, GREAT, GOOD, MISS)', style='List Bullet')
    doc.add_paragraph('Total score', style='List Bullet')
    doc.add_paragraph('Maximum combo achieved', style='List Bullet')
    doc.add_paragraph('Letter grade:', style='List Bullet')

    add_styled_table(doc,
        ['Grade', 'Score Ratio'],
        [
            ['S', '> 95%'],
            ['A', '> 85%'],
            ['B', '> 70%'],
            ['C', '> 50%'],
            ['D', '≤ 50%'],
        ]
    )
    doc.add_paragraph('Press ENTER to return to the main menu.')

    # ── 6. Visual Guide ──
    doc.add_heading('6. Visual Elements', level=1)

    doc.add_heading('6.1 Track Layout', level=2)
    doc.add_paragraph(
        'The game track is rendered in perspective, creating a 3D tunnel effect. '
        'Notes appear at a vanishing point at the top center and expand as they approach '
        'the hit line near the bottom. Each lane has a unique pastel color. '
        'The receptors (circular key indicators) are positioned below the hit line.'
    )

    doc.add_heading('6.2 Particle Effects', level=2)
    doc.add_paragraph('Explosion burst: 25 particles spawn when a note is hit.', style='List Bullet')
    doc.add_paragraph('Spiral: 8 particles rotate around the hit point.', style='List Bullet')
    doc.add_paragraph('Fire: 6 upward particles appear at combo > 10.', style='List Bullet')
    doc.add_paragraph('Screen flash: Brief white overlay on PERFECT judgments.', style='List Bullet')
    doc.add_paragraph('Beat pulse: Track glows in sync with the beat.', style='List Bullet')

    # ── 7. Chart File Format ──
    doc.add_heading('7. Custom Chart Creation', level=1)
    doc.add_paragraph(
        'You can create custom charts by placing JSON files in the charts/ directory. '
        'The format is:'
    )
    code = doc.add_paragraph(
        '{\n'
        '  "title": "My Song",\n'
        '  "bpm": 140,\n'
        '  "notes": [\n'
        '    {"time": 4.0, "lane": 0},\n'
        '    {"beat": 8, "lane": 1},\n'
        '    {"time": 5.0, "lane": 2, "type": "hold", "end": 6.0},\n'
        '    {"beat": 10, "lane": 3, "type": "hold", "dur": 2}\n'
        '  ]\n'
        '}\n'
    )
    for r in code.runs:
        r.font.name = 'Courier New'; r.font.size = Pt(9)

    doc.add_paragraph('Fields:')
    doc.add_paragraph('title: Display name of the chart.', style='List Bullet')
    doc.add_paragraph('bpm: Beats per minute (used for "beat" time format).', style='List Bullet')
    doc.add_paragraph('time: Note time in seconds (absolute).', style='List Bullet')
    doc.add_paragraph('beat: Note time in beat numbers (converted via bpm).', style='List Bullet')
    doc.add_paragraph('lane: Lane index 0-5.', style='List Bullet')
    doc.add_paragraph('type: "hold" for hold notes (default is tap).', style='List Bullet')
    doc.add_paragraph('end: Hold end time in seconds.', style='List Bullet')
    doc.add_paragraph('endBeat: Hold end time in beat numbers.', style='List Bullet')
    doc.add_paragraph('duration: Hold duration in seconds.', style='List Bullet')
    doc.add_paragraph('dur: Hold duration in beat numbers.', style='List Bullet')

    # ── 8. Troubleshooting ──
    doc.add_heading('8. Troubleshooting', level=1)
    add_styled_table(doc,
        ['Problem', 'Solution'],
        [
            ['No songs appear', 'Ensure charts/ and songs/ directories exist in the working directory. Run from the project root.'],
            ['Build error: raylib not found', 'Run: brew install raylib'],
            ['Build error: aubio not found', 'Run: brew install aubio'],
            ['No audio plays', 'Check system volume and audio output device. Ensure the terminal has microphone access (System Settings → Privacy).'],
            ['Import fails', 'Ensure the audio file is a supported format (MP3, WAV, OGG, FLAC, M4A, AAC). Short files (<5s) may not have enough content for analysis.'],
            ['Game runs slowly', 'Close other applications. The game targets 60 FPS; check Activity Monitor for CPU usage.'],
            ['Keys not responding', 'Click on the game window to ensure it has focus. Do not use Caps Lock.'],
        ]
    )

    # ── 9. Restrictions ──
    doc.add_heading('9. Restrictions and Limitations', level=1)
    doc.add_paragraph('The game only runs on macOS (uses Cocoa framework for file dialogs).', style='List Bullet')
    doc.add_paragraph('Chart files must be valid JSON with the expected structure.', style='List Bullet')
    doc.add_paragraph('Lane values must be integers 0-5; values outside this range are ignored during chart loading.', style='List Bullet')
    doc.add_paragraph('Audio import requires files with at least 5 seconds of content for reliable analysis.', style='List Bullet')
    doc.add_paragraph('The window size is fixed at 960×640 pixels.', style='List Bullet')
    doc.add_paragraph('Only one song can be played at a time (no simultaneous playback).', style='List Bullet')
    doc.add_paragraph('The game must be run from the project root directory for file paths to resolve correctly.', style='List Bullet')

    out_path = os.path.join(os.path.dirname(__file__), 'User_Manual.docx')
    doc.save(out_path)
    print(f'Saved: {out_path}')

if __name__ == '__main__':
    main()
