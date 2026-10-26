#!/usr/bin/env python3
"""
elfboi site builder.

Edit the TOOLS list (and the copy blocks further down), then run:

    python3 build.py

It writes every .html file in this folder. Nothing else is needed —
no npm, no framework, no build step at deploy time.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ==========================================================
#  TOOL DATA — edit here, pages regenerate
# ==========================================================

TOOLS = [
    {
        "slug": "clipped",
        "live": True,
        "hue_solid": "#C04334",
        "hue": "#C44536", "hue_wash": "#EBCBBF", "hue_mid": "#DA9285",
        "sticker": "Plug-in and<br>standalone<br>coming soon",
        "audio": [("moderate", "Moderate clipping"),
                  ("severe", "Severe clipping"),
                  ("extreme", "Extreme clipping")],
        "collab": "Josh Hong",
        "tutorial_id": "sfWDlQ38FDg",   # youtu.be/sfWDlQ38FDg
        "video": "images/clipped-ui.webm",
        "video_mp4": "images/clipped-ui.mp4",
        "poster": "images/clipped-poster.jpg",
        "shots": [("images/clipped-plugin.webp",
                   "Clipped in its dark and artist looks, one behind the other", "still")],
        "versions": [
            {
                "id": "plugin", "label": "Clipped Pro",
                "title": "Clipped Pro", "price": "$99",
                "summary": "Clipped Pro includes the plug-in and the standalone app. The plug-in runs inside a "
                           "DAW or NLE and the standalone app exists right on your computer. You will get both "
                           "when you buy Clipped Pro.",
                "buy": "clipped-pro",
                "specs": [("included", "Plug-in and Standalone app"),
                          ("runs in", "Plug-in: Any digital audio workstation (DAW) or video editor (NLE) "
                                      "that takes plug-ins<br>"
                                      "Standalone app: On the computer, tablet, or mobile device"),
                          ("formats", "VST3, AU, and AAX"),
                          ("processing", "Render only, not realtime"),
                          ("upload", "Batch uploading multiple files in workstation or on your computer "
                                     "with no time or file amount constraint"),
                          ("audio", "24-bit, 48 kHz. Mono and stereo. Outputs to .wav"),
                          ("looks", "Dark, light, and artist looks"),
                          ("computers", "Mac (macOS 12 and later) and Windows (10 and later)")],
                "shots": [("images/clipped-plugin.webp",
                           "Clipped Pro in its dark and artist looks, one behind the other", "still")],
            },
            {
                "id": "browser", "label": "Clipped Browser",
                "title": "Clipped Browser", "price": "Free",
                "summary": "Free, and there is nothing to install. Restore clipped dialogue and vocals straight in "
                           "the browser, up to six hours of audio a day.",
                "buttons": [("Open the browser version", "tools-clipped-browser.html")],
                "specs": [("price", "Free"),
                          ("limits", "Six hours of audio a day, one file at a time"),
                          ("runs in", "Any current browser, on a laptop or a phone"),
                          ("audio", "24-bit, 48 kHz. Mono and stereo. Outputs to .wav")],
                "shots": [("images/clipped-browser.jpg",
                           "Clipped running in a browser, with the render and daily usage panel beside it")],
            },
        ],
        "name": "clipped",
        "line": "Repairs recordings that are clipped.",
        "desc": "Rebuilds the peaks that were destroyed by a recording that was too loud. Free in your browser, or as an app and a plug-in.",
        "long": "When a recording is accidentally too loud for what your recorder can handle, the waveform gets "
                "cut off flat and it starts to sound harsh and distorted. Clipped works to restore the audio and "
                "its resolution.",
        "tags": ["restoration", "declipper"],
        "status": "v1",
        "status_class": "is-building",
        "formats": "In your browser, or as a plug-in and standalone app that ship together",
        "audience": "dialogue of any kind: podcasts, audio books, location recording, singing, film and television",
        "price": "The browser version is free. The app and plug-in are priced at release.",
        "demo": "Drop in a recording that was captured too loud and hear the repair before you download anything.",
    },
    {
        "slug": "xen",
        "live": False,
        "hue_solid": "#7A51B1",
        "hue": "#7A51B1", "hue_wash": "#DBCEDA", "hue_mid": "#B299C8",
        "name": "xen",
        "line": "A sequencer that breaks the rules of grids and tuning.",
        "desc": "Write music outside the usual twelve notes and off the usual grid, for anything experimental.",
        "long": "Most music software assumes twelve notes to an octave and a strict rhythmic grid, which quietly "
                "rules out a great deal of music. Xen lets you build your own tuning and place notes at any point "
                "in time, so you can write pieces that sit between the notes and between the beats. It drives "
                "whatever instrument you already play through.",
        "tags": ["sequencer", "tuning"],
        "status": "in development",
        "status_class": "is-building",
        "formats": "As a plug-in inside your editing program, or as an app on its own",
        "audience": "composers, sound designers, experimental musicians",
        "price": "Priced at release.",
        "demo": "Load a tuning, draw a phrase, and hear it against a steady reference note.",
    },
    {
        "slug": "identify",
        "live": False,
        "hue_solid": "#33658A",
        "hue": "#33658A", "hue_wash": "#CBD2D1", "hue_mid": "#8BA4B3",
        "name": "identify",
        "line": "Makes a large sound collection searchable.",
        "desc": "Listens to each file, works out what is in it, and writes that description into the file so you can search for it later.",
        "long": "A sound collection is only as good as your ability to find things in it. Identify listens to each "
                "file, works out what it contains, and writes that description into the file itself, where any "
                "editing program or library tool can search it. It handles tens of thousands of files in one pass "
                "and never renames or moves anything unless you ask it to.",
        "tags": ["searching", "organising"],
        "status": "in development",
        "status_class": "is-building",
        "formats": "An app that runs on its own, on Mac and Windows",
        "audience": "sound designers, post-production studios, library managers",
        "price": "Priced at release.",
        "demo": "Point it at a folder and see a sample of the descriptions it writes.",
    },
    {
        "slug": "impulse",
        "live": False,
        "hue_solid": "#197278",
        "hue": "#197278", "hue_wash": "#C6D5CD", "hue_mid": "#7CABA9",
        "name": "impulse",
        "line": "The sound of a room, from a photograph.",
        "desc": "Turns photographs or 3D scans of a space into a reverb you can use. Get the sound of a room from a thousand miles away.",
        "long": "Capturing how a real room sounds normally means carrying speakers and microphones into it and "
                "getting permission to make a very loud noise. Impulse works the same thing out from photographs "
                "or a 3D scan, using the shape of the space and the surfaces it can see. What comes out is a "
                "standard reverb file that works in the reverb tools you already have.",
        "tags": ["reverb", "spaces"],
        "status": "concept",
        "status_class": "",
        "formats": "An app that runs on its own, and exports a standard reverb file",
        "audience": "composers, sound designers, location sound",
        "price": "Priced at release.",
        "demo": "Upload a photograph of a room and hear a dry recording placed inside it.",
    },
    {
        "slug": "leveler",
        "live": False,
        "hue_solid": "#B94A24",
        "hue": "#D8572A", "hue_wash": "#F0CFBC", "hue_mid": "#E59C7E",
        "name": "leveler",
        "line": "Set your levels first, on the clip itself.",
        "desc": "Draws a volume line straight onto the clip and shows the sound reshaping as you move it, so levels are set before anything else.",
        "long": "Most editing is really volume adjustment, and most of that belongs on the clip itself rather than "
                "somewhere further down the chain. Leveler draws an editable volume line onto the clip, shows the "
                "sound changing shape as you drag it, and measures in either decibels or the loudness standard "
                "your delivery asks for. Room sound, breaths, and performance stay where they were.",
        "tags": ["volume", "dialogue"],
        "status": "in development",
        "status_class": "is-building",
        "formats": "As a plug-in inside your editing program",
        "audience": "dialogue editors, documentary, podcast, film and television",
        "price": "Priced at release.",
        "demo": "Compare a raw spoken clip against the same clip with a volume line drawn on it.",
    },
]

# ==========================================================
#  COURSES
# ==========================================================

COURSES = [
    {
        "slug": "audio-basics", "hue": "#33658A", "name": "audio basics",
        "outcome": "Learn the building blocks of sound so you walk into a project already prepared.",
        "who": "Anyone who can open an editing program but is guessing at half the controls.",
        "not_for": "People already comfortable with signal flow and filters.",
        "length": "6 lessons, about 2 hours", "price": "\u2014",
        "lessons": ["What sound actually is, in terms you can hear",
                    "Signal flow: where the sound goes and in what order",
                    "The physics, without the maths",
                    "The electronics, and why gear sounds different",
                    "Volume, loudness, and why they are not the same",
                    "Setting up a project you can actually work in"],
    },
    {
        "slug": "mixing-101", "hue": "#772E25", "name": "mixing 101",
        "outcome": "Take a recording from raw to finished, and know why you made every move.",
        "who": "People who can mix but cannot explain their own decisions.",
        "not_for": "Anyone looking for a formula to copy.",
        "length": "8 lessons, about 3 hours", "price": "\u2014",
        "lessons": ["Listening before you touch anything",
                    "Balance first, and how far that alone gets you",
                    "Shaping tone with equalisation",
                    "Controlling volume with compression",
                    "Reverb, delay, and the sense of a space",
                    "Effects, and when they help",
                    "Referencing other work without copying it",
                    "Knowing when it is finished"],
    },
    {
        "slug": "eq-advanced", "hue": "#7A51B1", "name": "advanced equalisation",
        "outcome": "Know every way to shape tone, and which one a problem actually calls for.",
        "who": "Engineers who shape tone confidently but by feel.",
        "not_for": "Anyone who has not finished a full mix yet.",
        "length": "6 lessons, about 2.5 hours", "price": "\u2014",
        "lessons": ["Mid and side: treating the centre and the edges separately",
                    "Dynamic: shaping that only acts when it needs to",
                    "Spectral: working on one narrow part at a time",
                    "Linear phase, and what it costs you",
                    "Matching and analysis tools, used honestly",
                    "On a group against on a single track"],
    },
    {
        "slug": "film-basics", "hue": "#197278", "name": "audio for film, basics",
        "outcome": "Know what to ask the picture editor for, how to set up, and what your delivery has to hit.",
        "who": "People moving into film and television from music, or from picture.",
        "not_for": "Anyone working only on music.",
        "length": "6 lessons, about 2.5 hours", "price": "\u2014",
        "lessons": ["What you need from the picture editor, and how to ask for it",
                    "Setting up a project so it stays workable",
                    "Finding your way around a large session",
                    "Loudness standards, and what the numbers mean",
                    "The order things happen in, from shoot to delivery",
                    "Handing your work on to the next person"],
    },
    {
        "slug": "film-advanced", "hue": "#C44536", "name": "audio for film, advanced",
        "outcome": "Balance dialogue, music, and sound design together, and deliver to industry specification.",
        "who": "People who have finished a film soundtrack and want to do it properly.",
        "not_for": "Anyone new to working with picture. Take the basics course first.",
        "length": "7 lessons, about 3 hours", "price": "\u2014",
        "lessons": ["Mixing with three competing elements at once",
                    "Where dialogue always wins, and where it does not",
                    "Music that supports rather than fights",
                    "Sound design you feel rather than notice",
                    "Reading a delivery specification without guessing",
                    "Producing every version a distributor asks for",
                    "The mix stage, and what happens there"],
    },
    {
        "slug": "dialogue-editing", "hue": "#B94A24", "name": "dialogue editing",
        "outcome": "Clean, level, and cut speech without it ever sounding edited.",
        "who": "Film and television editors, documentary editors, podcast producers.",
        "not_for": "People working only with sung vocals.",
        "length": "7 lessons, about 3 hours", "price": "\u2014",
        "lessons": ["Working with several microphones on the same scene",
                    "Choosing takes, and cutting between them invisibly",
                    "Room sound, and why it hides your edits",
                    "Setting volume before anything else",
                    "Removing noise without the strange artefacts",
                    "Reverb fills, so a cut does not jump",
                    "Breaths, plosives, and mouth noise"],
    },
    {
        "slug": "surround-mixing", "hue": "#2766B9", "name": "5.1 surround mixing",
        "outcome": "Work in surround sound, and know what changes when the room has more speakers.",
        "who": "People who have delivered a stereo mix and are taking a first surround job.",
        "not_for": "Anyone who has not finished a stereo mix professionally.",
        "length": "6 lessons, about 2.5 hours", "price": "\u2014",
        "lessons": ["Setting up a surround room you can trust",
                    "Placing sound around a listener",
                    "What the centre speaker is really for",
                    "The low frequency channel against low end in the main speakers",
                    "Traditional surround and atmospheric surround, side by side",
                    "Mixes that still work when folded down to stereo"],
    },
    {
        "slug": "atmos-basics", "hue": "#4F7942", "name": "atmos mixing, basics",
        "outcome": "Learn a way of working that translates to whatever speaker arrangement you are handed.",
        "who": "People already comfortable in surround sound.",
        "not_for": "Anyone new to multichannel work. Take 5.1 surround mixing first.",
        "length": "7 lessons, about 3 hours", "price": "\u2014",
        "lessons": ["What changes when sound can move in three dimensions",
                    "Sounds that move against sounds that sit still",
                    "Setting up, and working in a room that is not perfect",
                    "What headphone listeners actually hear",
                    "Loudness, and the specification you deliver to",
                    "Producing every speaker arrangement from one mix",
                    "A workflow you can repeat under deadline"],
    },
]

# ==========================================================
#  TEMPLATES
# ==========================================================

# Lemon Squeezy checkout links.
# Get one from the product page in Lemon Squeezy: Products -> your product ->
# Share -> Copy checkout link. It looks like
#   https://elfboi.lemonsqueezy.com/buy/8f2c1a94-...
# Paste it against the template's slug and its buy button goes live. Leave it
# empty and the button reads "not on sale yet" instead of leading nowhere.
# Marked "screenshot 02" slides stand in the gallery until the real pictures
# arrive. Set this to False before the site goes public.
SHOW_EMPTY_SLOTS = True

BUY = {
    "film-surround": "https://elfboi.lemonsqueezy.com/checkout/buy/febf6946-6c05-4fdd-94da-cfa92fbddd9d",
}

TEMPLATES = [
    {
        "slug": "film-surround", "cats": ["sessions", "mixing", "film", "pro-tools"],
        "art": "panner", "format": "Pro Tools template",
        "hue": "#7A51B1", "name": "5.1 Dolby Atmos mixing session", "price": "$39",
        "video": "images/template-51-sample.mp4",
        "video_webm": "images/template-51-sample.webm",
        "poster": "images/template-51-poster.jpg",
        "film_note": "A sample of the walkthrough of the session. Full video comes with the template.",
        "desc": "A Pro Tools session for mixing film in 5.1 Dolby Atmos, fully routed, with presets for every "
                "plug-in it uses.",
        "long": "Dolby Atmos 5.1 works the way traditional 5.1 does but with an easier workflow: clearer object "
                "and speaker positioning, and none of the echo problems traditional 5.1 runs into. This session is "
                "fully routed, so every section feeds its own bus and every bus feeds a bed, letting you ride a "
                "whole section at once. Prefer to work in objects instead? Press the object button and the routing "
                "switches over. It comes with the I/O setup, a preset for every plug-in in the chain, a links page "
                "for all of them, and a full video walkthrough.",
        "includes": ["The Pro Tools session template, fully routed",
                     "An I/O setup template for Dolby Atmos",
                     "A preset for every plug-in used in the session",
                     "Dialogue: 18 mono tracks in six scene sets of boom, lav 1 and lav 2, plus a roomtone track",
                     "Dialogue: 20 stereo tracks in ten pairs, same chain and sends as the mono tracks",
                     "Matching ambience and Foley reverb folders, eight returns each",
                     "Metering and a master monitor aux, set up for trim and downmix",
                     "Render print tracks ready to assign",
                     "A links page for every plug-in, with swaps, prices and descriptions",
                     "A full video walkthrough of the session"],
        "compat": "Pro Tools Studio or Ultimate 2023.12 or later, for the built-in Dolby Atmos renderer.",
        "needs": [("required",
                   "Pro Tools Studio or Ultimate 2023.12 or later. Avid Space and Avid Pro Subharmonic, both in "
                   "the Avid Complete Plugin Bundle, plus the Avid Space IR library. Youlean Loudness Meter or "
                   "Nugen VisLM."),
                  ("recommended",
                   "dxRevive Pro, Hush Pro, VoiceAssist, Soothe 2, Nugen Halo Upmix, FabFilter Pro-Q 4, Pro-R 2, "
                   "Pro-L 2, Pro-C 2, Pro-DS and Pro-MB, and SoundQ."),
                  ("if you do not own them",
                   "Every recommended plug-in can be swapped for your own. The manual lists the settings for each "
                   "one so you can copy them across.")],
        "hero": ("images/template-51-stack.webp",
                 "Three views of the 5.1 session stacked: the dialogue track list and groups, the routed "
                 "session with a reverb open, and the dialogue chain's plug-ins"),
        "shots": [("images/templates-session.jpg",
                   "The 5.1 session open in Pro Tools, showing the dialogue tracks, groups and reverb sends")],
    },
    {
        "slug": "dialogue-session", "cats": ["sessions", "editing", "film", "pro-tools"],
        "art": "waveform", "format": "Pro Tools template",
        "hue": "#C44536", "name": "dialogue session", "price": "\u2014",
        "desc": "A project laid out for speech: track order, routing, groups, and naming, ready to work in.",
        "long": "Built from the layout used on real jobs. Tracks arrive in the order a mixer expects, groups are "
                "already routed, and every track carries a note saying what belongs on it. Open it, import your "
                "recordings, and start editing.",
        "includes": ["Pro Tools project", "Reaper project", "Track naming and numbering scheme",
                     "A one-page map of how everything is routed", "Notes on what belongs on each track"],
        "compat": "Pro Tools 2022 and later, Reaper 6 and later",
    },
    {
        "slug": "atmos-session", "cats": ["sessions", "mixing", "presets", "pro-tools"],
        "art": "panner2", "format": "Pro Tools template",
        "hue": "#2766B9", "name": "atmos mixing session", "price": "\u2014",
        "desc": "Set up for 7.1.2, and folds down through every arrangement to plain stereo.",
        "long": "A project built for a 7.1.2 speaker arrangement that will collapse cleanly all the way down to "
                "stereo, taking in everything in between. Routing, monitoring, and versions for each arrangement "
                "are already configured, so you can check how a mix behaves on any setup without rebuilding it.",
        "includes": ["Project set up for 7.1.2", "Fold-down paths to 7.1, 5.1, and stereo",
                     "Monitoring switching between arrangements", "Loudness metering per arrangement",
                     "Notes on what to check at each stage"],
        "compat": "Pro Tools Ultimate 2022 and later",
    },
    {
        "slug": "band-session", "cats": ["sessions", "recording", "pro-tools"],
        "art": "session", "format": "Pro Tools + Logic template",
        "hue": "#197278", "name": "music recording session", "price": "\u2014",
        "desc": "A recording project set up for a full band, with everything labelled before anyone arrives.",
        "long": "Drums, bass, guitars, keys, and vocals, laid out and labelled, with headphone sends already "
                "routed so players can hear themselves. Built so the hour before a session is spent on "
                "microphones rather than on menus.",
        "includes": ["Pro Tools project", "Logic project", "Full drum, bass, guitar, keys and vocal layout",
                     "Headphone sends already routed", "A pre-session checklist"],
        "compat": "Pro Tools 2022 and later, Logic Pro 10.7 and later",
    },
    {
        "slug": "vocal-tracking", "cats": ["sessions", "recording", "presets", "pro-tools"],
        "art": "chain", "format": "Pro Tools + Logic template",
        "hue": "#B94A24", "name": "vocal tracking session", "price": "\u2014",
        "desc": "A hip hop and rap vocal setup with the headphone sound already dialled in.",
        "long": "Set up for fast vocal takes: a main track, doubles and ad-libs already grouped, and a headphone "
                "chain that makes a performer want to sing. The recorded sound stays clean, so nothing is baked "
                "in that you cannot undo later.",
        "includes": ["Pro Tools project", "Logic project", "Main, double, and ad-lib layout",
                     "A headphone chain that stays out of the recording", "Comping and take-folder setup"],
        "compat": "Pro Tools 2022 and later, Logic Pro 10.7 and later",
    },
    {
        "slug": "podcast-session", "cats": ["sessions", "editing", "pro-tools"],
        "art": "waveform2", "format": "Pro Tools + Reaper template",
        "hue": "#4F7942", "name": "podcast session", "price": "\u2014",
        "desc": "Up to five speakers, each on their own track, already routed and labelled.",
        "long": "Built for a conversation with as many as five people at the table. Every speaker gets a track, "
                "a group, and a place in the stereo picture, with noise handling and levelling ready to go. Works "
                "the same whether three people turn up or five.",
        "includes": ["Pro Tools project", "Reaper project", "Five speaker tracks, routed and labelled",
                     "Levelling and noise handling already in place", "A layout for remote guests"],
        "compat": "Pro Tools 2022 and later, Reaper 6 and later",
    },
    {
        "slug": "delivery-one-sheet", "cats": ["one-sheets", "film"],
        "art": "sheet", "format": "one-sheet",
        "hue": "#33658A", "name": "delivery one-sheet", "price": "\u2014",
        "desc": "What you need from the client and what you hand back, with every specification, on one page.",
        "long": "Most delivery problems come from a specification nobody wrote down. This is a single page you fill "
                "in at the start of a job and attach to the contract. It covers what you need from them, what you "
                "owe them, in what format, and at what loudness.",
        "includes": ["Editable one-sheet, as a document and a PDF", "A filled-in example from a real delivery",
                     "Common broadcast and streaming targets", "A checklist for delivery day"],
        "compat": "Any word processor. Prints at A4 or US Letter.",
    },
    {
        "slug": "surround-one-sheet", "cats": ["one-sheets", "mixing"],
        "art": "sheet2", "format": "one-sheet",
        "hue": "#772E25", "name": "5.1 mixing one-sheet", "price": "\u2014",
        "desc": "How to mix in surround sound, and the specifications, on one page for any editing program.",
        "long": "A single reference page covering how a surround mix is put together and what each delivery "
                "specification asks for. Written to be program-agnostic, so it is as useful in Logic or Reaper as "
                "it is in Pro Tools.",
        "includes": ["Reference sheet, print and screen versions", "Speaker layout and level standards",
                     "Delivery targets with the standard each comes from", "A fold-down checklist"],
        "compat": "Any editing program. Prints at A4 or US Letter.",
    },
    {
        "slug": "loudness-reference", "cats": ["one-sheets", "mixing"],
        "art": "card", "format": "one-sheet",
        "hue": "#E3A347", "name": "loudness reference card", "price": "\u2014",
        "desc": "Every loudness target you are likely to be handed, with the standard each one comes from.",
        "long": "A single card with the loudness targets for broadcast, streaming, film, and podcast, and the "
                "specification each one comes from, so you can check rather than remember. Sized for a desk or "
                "for a second screen.",
        "includes": ["Reference card, print and screen versions", "Sources cited for every figure",
                     "A short note on the two ways loudness is measured"],
        "compat": "Print at A5, or keep it open on a screen.",
    },
]

# ==========================================================
#  DRAWINGS
#  Built from point lists, not typed path strings, so every
#  stroke can be given a hand-drawn wobble. Seeded, so the
#  wobble is the same every build.
# ==========================================================

import math
import random


def wob(points, seed, amp=3.4, close=False, overshoot=2.8):
    """Turn a list of points into a path that looks drawn rather than plotted."""
    rnd = random.Random(seed)
    pts = list(points)
    if close:
        pts = pts + [pts[0]]
    d = "M%.1f,%.1f" % pts[0]
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** 0.5 or 1.0
        px, py = -dy / L, dx / L
        off = rnd.uniform(-amp, amp)
        ex, ey = x2, y2
        # let the last stroke run past the corner, the way a pen does
        if i == len(pts) - 2 and not close and overshoot:
            ex += dx / L * overshoot
            ey += dy / L * overshoot
        d += " Q%.1f,%.1f %.1f,%.1f" % (x1 + dx / 2 + px * off, y1 + dy / 2 + py * off, ex, ey)
    return d


def poly(points, seed, amp=3.4):
    """A closed wobbly shape, for the gold fill behind the linework."""
    return wob(points, seed, amp=amp, close=True, overshoot=0)


def star_path(cx, cy, r):
    """The four-point mark, as a bare path string."""
    k = r * 0.26
    return ("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f "
            "Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z") % (
        cx, cy - r, cx + k, cy - k, cx + r, cy,
        cx + k, cy + k, cx, cy + r,
        cx - k, cy + k, cx - r, cy,
        cx - k, cy - k, cx, cy - r)


def star(cx, cy, r, cls="spark"):
    """A four-pointed sparkle with pinched waists, so it reads as drawn."""
    k = r * 0.26
    d = ("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f "
         "Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z") % (
        cx, cy - r, cx + k, cy - k, cx + r, cy,
        cx + k, cy + k, cx, cy + r,
        cx - k, cy + k, cx - r, cy,
        cx - k, cy - k, cx, cy - r)
    return '<path class="%s" d="%s"/>' % (cls, d)


def _art_clipped():
    body = [(44, 92), (70, 106), (96, 92), (96, 58), (70, 44), (44, 58)]
    tip = [(52, 34), (70, 8), (88, 34), (70, 44)]
    p = []
    p.append('<path class="riso" d="%s"/>' % poly(body, 11))
    p.append('<path d="%s"/>' % wob(body, 12, close=True))
    p.append('<path d="%s"/>' % wob([(70, 106), (70, 72)], 13))
    p.append('<path d="%s"/>' % wob([(44, 58), (70, 72), (96, 58)], 14))
    # the sliced-off tip, hovering just above, dropping back in on hover
    p.append('<g class="pop"><path d="%s"/><path d="%s"/></g>'
             % (wob(tip, 15, close=True), wob([(52, 34), (70, 44), (88, 34)], 16)))
    p.append(star(30, 40, 5))
    p.append(star(112, 30, 4))
    p.append(star(20, 74, 3.5))
    return p


def _art_xen():
    plane = [(18, 90), (70, 62), (122, 90), (70, 118)]
    p = ['<path class="riso" d="%s"/>' % poly(plane, 21),
         '<path d="%s"/>' % wob(plane, 22, close=True)]
    for i, (a, b) in enumerate([((31, 83), (83, 111)), ((44, 76), (96, 104)), ((57, 69), (109, 97)),
                                ((31, 97), (83, 69)), ((44, 104), (96, 76)), ((57, 111), (109, 83))]):
        p.append('<path class="thin" d="%s"/>' % wob([a, b], 30 + i, amp=2.0, overshoot=0))
    # blocks standing off the grid at unrelated heights
    for i, (cx, base, h, seed) in enumerate([(50, 48, 13, 41), (77, 74, 12, 42), (97, 38, 14, 43)]):
        a, bb = 9, 5.2
        cube = [(cx - a, base - bb), (cx, base), (cx + a, base - bb),
                (cx + a, base - bb - h), (cx, base - 2 * bb - h), (cx - a, base - bb - h)]
        p.append('<path d="%s"/>' % wob(cube, seed, amp=2.2, close=True))
        p.append('<path d="%s"/>' % wob([(cx, base), (cx, base - h)], seed + 100, amp=1.8))
        p.append('<path d="%s"/>' % wob([(cx - a, base - bb - h), (cx, base - h), (cx + a, base - bb - h)],
                                        seed + 200, amp=1.8, overshoot=0))
        p.append('<path class="thin" stroke-dasharray="2 4" d="%s"/>'
                 % wob([(cx, base), (cx, base + 22 + i * 6)], seed + 300, amp=1.6, overshoot=0))
    p.append(star(112, 22, 5))
    p.append(star(24, 40, 4))
    return p


def _art_identify():
    c3 = [(36, 54), (76, 34), (112, 52), (72, 74)]
    c2 = [(32, 74), (72, 54), (108, 72), (68, 94)]
    c1 = [(30, 94), (70, 74), (106, 92), (66, 114)]
    p = ['<path class="riso" d="%s"/>' % poly(c3, 51)]
    for i, c in enumerate([c1, c2, c3]):
        p.append('<path d="%s"/>' % wob(c, 52 + i, close=True))
    # marks written on the top card
    for i, (a, b) in enumerate([((48, 56), (72, 68)), ((56, 51), (78, 62)), ((64, 46), (80, 54))]):
        p.append('<path class="thin" d="%s"/>' % wob([a, b], 60 + i, amp=1.8, overshoot=0))
    # tags flying off the corner
    p.append('<g class="pop">')
    for i, (a, b) in enumerate([((100, 26), (116, 20)), ((104, 34), (120, 28)), ((108, 42), (124, 36))]):
        p.append('<path d="%s"/>' % wob([a, b], 70 + i, amp=1.4, overshoot=1.2))
    p.append("</g>")
    p.append(star(22, 34, 4))
    return p


def _art_impulse():
    frame = [(14, 48), (58, 48), (58, 86), (14, 86)]
    p = ['<path class="riso" d="%s"/>' % poly(frame, 81),
         '<path d="%s"/>' % wob(frame, 82, close=True),
         '<circle cx="26" cy="60" r="4.5"/>',
         '<path d="%s"/>' % wob([(17, 82), (29, 64), (38, 75), (47, 61), (56, 80)], 83, amp=2.2, overshoot=0)]
    # the room the picture becomes
    p.append('<path d="%s"/>' % wob([(92, 20), (92, 62)], 84))
    p.append('<path d="%s"/>' % wob([(60, 38), (92, 20), (124, 38)], 85, overshoot=0))
    p.append('<path d="%s"/>' % wob([(60, 78), (92, 62), (124, 78)], 86, overshoot=0))
    p.append('<path d="%s"/>' % wob([(60, 38), (60, 78)], 87))
    p.append('<path d="%s"/>' % wob([(124, 38), (124, 78)], 88))
    p.append('<path d="%s"/>' % wob([(60, 78), (92, 96), (124, 78)], 89, overshoot=0))
    p.append('<path class="thin" stroke-dasharray="3 4" d="%s"/>' % wob([(61, 64), (86, 58)], 90, amp=2.0))
    # the sound arriving in it
    p.append('<g class="pop">')
    p.append('<path class="thin" d="M80,52 A13,13 0 0,1 104,52"/>')
    p.append('<path class="thin" d="M74,56 A20,20 0 0,1 110,56"/>')
    p.append("</g>")
    p.append(star(112, 100, 4.5))
    p.append(star(34, 30, 4))
    return p


def _art_leveler():
    top = [(20, 82), (70, 54), (120, 82), (70, 110)]
    line = [(20, 44), (45, 28), (70, 39), (95, 22), (120, 33)]
    p = ['<path class="riso" d="%s"/>' % poly(top, 101),
         '<path d="%s"/>' % wob(top, 102, close=True)]
    for i, (a, b) in enumerate([((20, 82), (20, 96)), ((120, 82), (120, 96)), ((70, 110), (70, 124))]):
        p.append('<path d="%s"/>' % wob([a, b], 110 + i, amp=1.6))
    p.append('<path d="%s"/>' % wob([(20, 96), (70, 124), (120, 96)], 113, overshoot=0))
    p.append('<g class="pop">')
    p.append('<path class="gainline" d="%s"/>' % wob(line, 114, amp=2.6, overshoot=0))
    for i, (x, y) in enumerate(line):
        p.append('<circle class="bead" cx="%d" cy="%d" r="3"/>' % (x, y))
    p.append("</g>")
    for i, (x, y) in enumerate(line):
        p.append('<path class="thin" stroke-dasharray="2 4" d="%s"/>'
                 % wob([(x, y + 4), (x, 80)], 120 + i, amp=1.5, overshoot=0))
    p.append(star(132, 58, 4))
    return p


def _svg(parts, label):
    return ('<svg viewBox="-6 0 152 132" role="img" aria-label="%s">\n  %s\n</svg>'
            % (label, "\n  ".join(parts)))


def _art_next():
    body = [(46, 88), (70, 102), (94, 88), (94, 54), (70, 40), (46, 54)]
    p = ['<path class="thin" stroke-dasharray="4 6" d="%s"/>' % wob(body, 201, amp=4.0, close=True),
         '<path class="thin" stroke-dasharray="4 6" d="%s"/>' % wob([(70, 102), (70, 68)], 202, amp=1.4),
         '<path class="thin" stroke-dasharray="4 6" d="%s"/>' % wob([(46, 54), (70, 68), (94, 54)], 203, amp=1.4, overshoot=0)]
    p.append(star(112, 44, 5))
    p.append(star(28, 62, 4))
    p.append(star(96, 108, 3.5))
    return p


ART = {
    "next": _svg(_art_next(), "A shape still being sketched, drawn in dashes"),
    "clipped": _svg(_art_clipped(), "A drawn solid with its top sliced off, the piece hovering above it"),
    "xen": _svg(_art_xen(), "A drawn grid with blocks floating above it at unrelated heights"),
    "identify": _svg(_art_identify(), "A fanned stack of drawn cards with tags flying off the corner"),
    "impulse": _svg(_art_impulse(), "A drawn picture linked to an open room with sound arriving in it"),
    "leveler": _svg(_art_leveler(), "A drawn slab with a bouncing gain line and bead handles above it"),
}



def _art_hub():
    """Monitors on a grid, a signal overhead, and each point on that
    signal dropped to the grid with a dashed guide."""
    p = []

    # gold under the grid, out of register until you hover
    plane = [(30, 322), (210, 240), (390, 322), (210, 404)]
    p.append('<path class="riso f-grid" d="%s"/>' % poly(plane, 301, amp=4))
    p.append('<path class="thin pt-grid" d="%s"/>' % wob(plane, 302, amp=4, close=True))
    for i, (a, b) in enumerate([((75, 301), (255, 383)), ((120, 281), (300, 363)), ((165, 260), (345, 342)),
                                ((75, 343), (255, 261)), ((120, 363), (300, 281)), ((165, 383), (345, 301))]):
        p.append('<path class="thin pt-grid" d="%s"/>' % wob([a, b], 310 + i, amp=2.5, overshoot=0))

    # the line lying on the grid
    sine = []
    for k in range(61):
        x = 42 + k * (336 / 60.0)
        taper = math.sin(k / 60.0 * math.pi)
        sine.append((x, 322 + math.sin(k / 60.0 * math.pi * 5) * 22 * taper))
    p.append('<path class="sine pt-sine" d="%s"/>' % wob(sine, 305, amp=1.0, overshoot=0))

    # dashed guides, drawn first so the solid objects sit over them
    wave = [(52, 128), (105, 74), (158, 116), (211, 50), (264, 108), (317, 66), (370, 110)]
    for i, (x, y) in enumerate(wave):
        p.append('<path class="thin drop-line" stroke-dasharray="3 5" d="%s"/>'
                 % wob([(x, y + 8), (x, 318)], 380 + i, amp=1.0, overshoot=0))

    # three monitors standing on the grid
    for idx, (cx, base, w_, d_, h_, seed) in enumerate(
            ((88, 330, 30, 17, 56, 360), (332, 330, 30, 17, 56, 365), (210, 288, 24, 14, 44, 370))):
        front = [(cx - w_, base - d_), (cx, base), (cx + w_, base - d_),
                 (cx + w_, base - d_ - h_), (cx, base - 2 * d_ - h_), (cx - w_, base - d_ - h_)]
        p.append('<path class="riso f-speaker f-spk%d" d="%s"/>' % (idx + 1, poly(front, seed, amp=3)))
        p.append('<path class="pt-speaker" d="%s"/>' % wob(front, seed + 1, amp=3, close=True))
        p.append('<path class="pt-speaker" d="%s"/>' % wob([(cx, base), (cx, base - h_)], seed + 2, amp=2))
        p.append('<path class="pt-speaker" d="%s"/>' % wob(
            [(cx - w_, base - d_ - h_), (cx, base - h_), (cx + w_, base - d_ - h_)], seed + 3, amp=2, overshoot=0))
        fx = cx - w_ / 2
        p.append('<ellipse class="cone pt-speaker" cx="%.0f" cy="%.0f" rx="13" ry="9" transform="rotate(-30 %.0f %.0f)"/>'
                 % (fx, base - 28, fx, base - 28))
        p.append('<ellipse class="cone pt-speaker" cx="%.0f" cy="%.0f" rx="6" ry="4" transform="rotate(-30 %.0f %.0f)"/>'
                 % (fx, base - 52, fx, base - 52))
        # the dust cap in the middle of the woofer
        p.append('<ellipse class="fill-solid" cx="%.0f" cy="%.0f" rx="4.4" ry="3" transform="rotate(-30 %.0f %.0f)"/>'
                 % (fx, base - 28, fx, base - 28))

    # loose blocks, floating
    for i, (cx, base, h, a, seed) in enumerate(((140, 206, 22, 14, 340), (288, 186, 20, 13, 341), (214, 150, 17, 11, 342))):
        b = a * 0.577
        cube = [(cx - a, base - b), (cx, base), (cx + a, base - b),
                (cx + a, base - b - h), (cx, base - 2 * b - h), (cx - a, base - b - h)]
        p.append('<g class="float f%d pt-box%d">' % (i + 1, i + 1))
        p.append('<path class="riso f-box" d="%s"/>' % poly(cube, seed, amp=3))
        p.append('<path d="%s"/>' % wob(cube, seed + 1, amp=3, close=True))
        p.append('<path d="%s"/>' % wob([(cx, base), (cx, base - h)], seed + 2, amp=2))
        p.append('<path d="%s"/>' % wob([(cx - a, base - b - h), (cx, base - h), (cx + a, base - b - h)],
                                        seed + 3, amp=2, overshoot=0))
        p.append("</g>")

    p.append('<g class="drift"><g class="gain-drop">')
    p.append('<path class="wave pt-signal" d="%s"/>' % wob(wave, 330, amp=4, overshoot=0))
    for x, y in wave:
        p.append('<circle class="bead" cx="%d" cy="%d" r="6"/>' % (x, y))
    p.append("</g></g>")

    for cx, cy, r in [(64, 40, 13), (376, 34, 10), (156, 22, 8), (24, 246, 8), (398, 258, 9)]:
        p.append(star(cx, cy, r))
    return p


def _art_collab():
    """A canvas and a monitor, joined by one signal running through both.
    Art on one side, audio on the other."""
    p = []

    canvas = [(26, 22), (128, 8), (132, 150), (30, 166)]
    p.append('<path class="riso f-canvas" d="%s"/>' % poly(canvas, 601, amp=3))
    p.append('<path class="pt-canvas" d="%s"/>' % wob(canvas, 602, amp=3, close=True))
    p.append('<path class="pt-canvas" d="%s"/>' % wob([(50, 113), (72, 65), (90, 96), (106, 53), (122, 105)], 603, amp=2, overshoot=0))
    p.append('<circle class="pt-canvas" cx="53" cy="52" r="9"/>')
    for i, (a, b) in enumerate([((44, 162), (30, 244)), ((112, 154), (128, 244)), ((38, 204), (121, 199))]):
        p.append('<path class="pt-canvas" d="%s"/>' % wob([a, b], 610 + i, amp=2))

    w_, d_, h_ = 34, 19, 74
    cx, base = 300, 122
    box = [(cx - w_, base - d_), (cx, base), (cx + w_, base - d_),
           (cx + w_, base - d_ - h_), (cx, base - 2 * d_ - h_), (cx - w_, base - d_ - h_)]
    p.append('<path class="riso f-speaker" d="%s"/>' % poly(box, 620, amp=3))
    p.append('<path class="pt-speaker" d="%s"/>' % wob(box, 621, amp=3, close=True))
    p.append('<path class="pt-speaker" d="%s"/>' % wob([(cx, base), (cx, base - h_)], 622, amp=2))
    p.append('<path class="pt-speaker" d="%s"/>' % wob([(cx - w_, base - d_ - h_), (cx, base - h_), (cx + w_, base - d_ - h_)], 623, amp=2, overshoot=0))
    fx = cx - w_ / 2
    p.append('<ellipse class="cone pt-speaker" cx="%.0f" cy="%.0f" rx="15" ry="10" transform="rotate(-30 %.0f %.0f)"/>' % (fx, base - 34, fx, base - 34))
    p.append('<ellipse class="cone pt-speaker" cx="%.0f" cy="%.0f" rx="7" ry="4.6" transform="rotate(-30 %.0f %.0f)"/>' % (fx, base - 66, fx, base - 66))
    for i, (a, b) in enumerate([((cx - 22, base + 4), (cx - 34, 244)), ((cx + 22, base - 8), (cx + 36, 240))]):
        p.append('<path class="pt-speaker" d="%s"/>' % wob([a, b], 630 + i, amp=2))

    # dashed, leaving the picture and heading right
    for i, r in enumerate((26, 42, 58)):
        p.append('<path class="arc pt-arc a%d" stroke-dasharray="4 5" d="M%.0f,%.0f A%d,%d 0 0,1 %.0f,%.0f"/>'
                 % (i + 1, 146 + r * 0.42, 78 - r * 0.72, r, r, 146 + r * 0.42, 78 + r * 0.72))

    # solid, coming off the monitor and heading left
    for i, r in enumerate((26, 42, 58)):
        p.append('<path class="arc arc-solid s%d" d="M%.0f,%.0f A%d,%d 0 0,0 %.0f,%.0f"/>'
                 % (i + 1, 250 - r * 0.42, 78 - r * 0.72, r, r, 250 - r * 0.42, 78 + r * 0.72))

    # one smooth line running underneath both
    sig = []
    for k in range(97):
        t = k / 96.0
        sig.append((44 + t * 292, 268 + math.sin(t * math.pi * 3) * 20))
    p.append('<path class="wave pt-signal smooth" d="%s"/>'
             % ("M" + " L".join("%.1f,%.1f" % pt for pt in sig)))
    for x in (44, 141, 239, 336):
        p.append('<circle class="bead" cx="%d" cy="268" r="6"/>' % x)

    for cx2, cy2, r in [(196, 24, 13), (354, 34, 10), (24, 258, 9), (338, 256, 11)]:
        p.append(star(cx2, cy2, r))
    return p


ART["collab"] = ('<svg viewBox="0 0 380 296" role="img" '
                 'aria-label="A drawn canvas and a studio monitor joined by one signal running through both">\n  '
                 + "\n  ".join(_art_collab()) + "\n</svg>")

ART["hub"] = ('<svg viewBox="12 8 400 424" role="img" '
              'aria-label="Three drawn studio monitors and floating blocks measured against a signal line">\n  '
              + "\n  ".join(_art_hub()) + "\n</svg>")


# ==========================================================
#  SHARED CHROME
# ==========================================================



# ==========================================================
#  PORTRAITS
#  Doodle faces: one weight of line, dot eyes, a plain mouth.
#  Not likenesses. Each person gets one or two features that
#  make them recognisable and nothing else.
# ==========================================================

import math


def ring(cx, cy, rx, ry, n=15, start=-1.57):
    return [(cx + rx * math.cos(start + 2 * math.pi * i / n),
             cy + ry * math.sin(start + 2 * math.pi * i / n)) for i in range(n)]


def _head(seed, rx=27, ry=31, cy=52):
    """Face outline and neck. Drawn first, then masked by hair."""
    return ['<path class="ink" d="%s"/>' % wob(ring(50, cy, rx, ry), seed, amp=1.1, close=True),
            '<path class="ink" d="%s"/>' % wob([(43, cy + ry - 3), (43, cy + ry + 9)], seed + 1, amp=0.8, overshoot=0),
            '<path class="ink" d="%s"/>' % wob([(57, cy + ry - 3), (57, cy + ry + 9)], seed + 2, amp=0.8, overshoot=0)]


def _features(seed, cy=52, square=False):
    """Eyes, glasses, and two mouths. The smile is hidden until hover."""
    if square:
        lens = ['<rect class="ink" x="30.5" y="%d" width="19" height="14" rx="1.5"/>' % (cy - 8),
                '<rect class="ink" x="50.5" y="%d" width="19" height="14" rx="1.5"/>' % (cy - 8)]
    else:
        lens = ['<circle class="ink" cx="40" cy="%d" r="8.5"/>' % (cy - 1),
                '<circle class="ink" cx="60" cy="%d" r="8.5"/>' % (cy - 1)]
    return lens + [
            '<path class="ink" d="%s"/>' % wob([(49.5, cy - 1), (50.5, cy - 1)], seed, amp=0.3, overshoot=0),
            '<path class="ink" d="%s"/>' % wob([(31.5, cy - 2), (26, cy - 4)], seed + 1, amp=0.5, overshoot=0),
            '<path class="ink" d="%s"/>' % wob([(68.5, cy - 2), (74, cy - 4)], seed + 2, amp=0.5, overshoot=0),
            '<circle class="dot-eye" cx="40" cy="%d" r="2.5"/>' % (cy - 1),
            '<circle class="dot-eye" cx="60" cy="%d" r="2.5"/>' % (cy - 1),
            '<path class="ink mouth-flat" d="%s"/>' % wob([(45, cy + 14), (55, cy + 14)], seed + 3, amp=1.1, overshoot=0),
            '<path class="ink mouth-smile" d="M42,%d Q50,%d 58,%d"/>' % (cy + 11, cy + 21, cy + 11)]


def portrait_lien():
    """Wolf cut. Shaggy layers, spiky ends, curtain fringe."""
    p = _head(401)
    hair = [(18, 70), (16, 44), (22, 26), (36, 15), (52, 12), (68, 16), (80, 28), (84, 48), (82, 72),
            (76, 58), (74, 40), (68, 30), (58, 26), (50, 25), (42, 27), (32, 33), (26, 44), (24, 62)]
    p.append('<path class="hair" d="%s"/>' % wob(hair, 410, amp=1.7, close=True))
    p.append('<path class="ink" d="%s"/>' % wob([(50, 26), (43, 33), (38, 41)], 411, amp=1.2, overshoot=0))
    p.append('<path class="ink" d="%s"/>' % wob([(50, 26), (57, 33), (62, 41)], 412, amp=1.2, overshoot=0))
    p.append('<path class="ink" d="%s"/>' % wob([(20, 62), (17, 76)], 413, amp=1.0, overshoot=2))
    p.append('<path class="ink" d="%s"/>' % wob([(81, 60), (84, 75)], 414, amp=1.0, overshoot=2))
    p += _features(415, square=True)
    return p


def portrait_anthony():
    """Taller, narrower head. Neat side part."""
    p = _head(421, rx=25, ry=33)
    hair = [(25, 44), (27, 26), (39, 16), (56, 15), (71, 22), (76, 38),
            (72, 31), (62, 24), (48, 23), (37, 28), (30, 40)]
    p.append('<path class="hair" d="%s"/>' % wob(hair, 430, amp=1.3, close=True))
    p.append('<path class="ink" d="%s"/>' % wob([(43, 21), (63, 30)], 431, amp=1.0, overshoot=0))
    p += _features(435)
    return p


def portrait_josh():
    """Chin-length curtains, middle part."""
    p = _head(441)
    # Spikes across the crown. Every point is kept inside a radius of
    # 41 from the centre, so nothing pokes through the portrait circle.
    hair = []
    for k in range(13):
        ang = math.pi * (1.04 + k * (0.92 / 12))          # left round to right
        r = 41 if k % 2 else 31
        hair.append((50 + r * math.cos(ang), 50 + r * math.sin(ang)))
    hair += [(78, 56), (70, 44), (68, 32), (58, 26), (50, 25), (40, 28), (31, 36), (29, 50), (22, 56)]
    p.append('<path class="hair" d="%s"/>' % wob(hair, 450, amp=1.1, close=True))
    p.append('<path class="ink" d="%s"/>' % wob([(44, 24), (41, 34)], 451, amp=0.9, overshoot=0))
    p.append('<path class="ink" d="%s"/>' % wob([(57, 24), (60, 34)], 452, amp=0.9, overshoot=0))
    p += _features(455)
    return p


PORTRAITS = {"\u201cElfboi\u201d Lenny": portrait_lien, "Anthony Leedom": portrait_anthony, "Josh Hong": portrait_josh}


# ==========================================================
#  TEMPLATE DRAWINGS
# ==========================================================

def _art_session():
    p = []
    lanes = [(24, 40), (24, 56), (24, 72), (24, 88)]
    p.append('<path class="riso" d="%s"/>' % poly([(24, 32), (116, 32), (116, 96), (24, 96)], 501, amp=2.5))
    for i, (x, y) in enumerate(lanes):
        p.append('<path d="%s"/>' % wob([(x, y), (116, y)], 510 + i, amp=1.4, overshoot=1.2))
        p.append('<path d="%s"/>' % wob([(x + 8 + i * 14, y - 5), (x + 40 + i * 12, y - 5)], 520 + i, amp=1.0, overshoot=0))
    p.append('<path d="%s"/>' % wob([(24, 32), (116, 32), (116, 96), (24, 96)], 502, amp=2.5, close=True))
    p.append(star(122, 26, 5)); p.append(star(16, 104, 4))
    return p


def _art_sheet(v=0):
    page = [(34, 20), (104, 20), (104, 104), (34, 104)]
    p = ['<path class="riso" d="%s"/>' % poly(page, 531, amp=2.5),
         '<path d="%s"/>' % wob(page, 532, amp=2.5, close=True)]
    for i, y in enumerate([36, 48, 60, 72, 84] if v == 0 else [34, 46, 62, 74, 86]):
        w = (58 if i % 2 == 0 else 40) if v == 0 else (30 if i == 0 else (54 if i % 2 else 42))
        # The second cut hangs its lines off the right edge instead of the
        # left, and opens with a short heading, so the two one-sheets read
        # as different pages of the same kind of document.
        x0 = 44 if v == 0 else (94 - w)
        p.append('<path class="thin" d="%s"/>' % wob([(x0, y), (x0 + w, y)], 540 + i, amp=1.1, overshoot=0))
    p.append(star(114, 30, 5) if v == 0 else star(116, 94, 5))
    p.append(star(24, 92, 4) if v == 0 else star(26, 28, 4))
    return p


def _art_card():
    card = [(20, 40), (120, 34), (122, 88), (22, 94)]
    p = ['<path class="riso" d="%s"/>' % poly(card, 551, amp=3),
         '<path d="%s"/>' % wob(card, 552, amp=3, close=True)]
    for i, y in enumerate([54, 66, 78]):
        p.append('<path class="thin" d="%s"/>' % wob([(32, y), (86 - i * 10, y - 1)], 560 + i, amp=1.1, overshoot=0))
    p.append(star(112, 24, 5)); p.append(star(16, 104, 4))
    return p


def _art_tags():
    p = []
    for i, (x, y) in enumerate([(26, 34), (34, 58), (26, 82)]):
        tag = [(x, y), (x + 58, y - 4), (x + 70, y + 8), (x + 58, y + 20), (x, y + 16)]
        if i == 1:
            p.append('<path class="riso" d="%s"/>' % poly(tag, 571 + i, amp=2))
        p.append('<path d="%s"/>' % wob(tag, 575 + i, amp=2, close=True))
        p.append('<circle class="fill-solid" cx="%d" cy="%d" r="2.6"/>' % (x + 56, y + 8))
    p.append(star(116, 24, 5)); p.append(star(112, 100, 4))
    return p


def _art_chain():
    p = []
    for i, cx in enumerate([34, 70, 106]):
        box = [(cx - 16, 52), (cx + 16, 48), (cx + 16, 78), (cx - 16, 82)]
        if i == 1:
            p.append('<path class="riso" d="%s"/>' % poly(box, 581, amp=2))
        p.append('<path d="%s"/>' % wob(box, 585 + i, amp=2, close=True))
        if i < 2:
            p.append('<path class="thin" d="%s"/>' % wob([(cx + 16, 64), (cx + 20, 64)], 590 + i, amp=0.8, overshoot=1))
    p.append('<path class="wave pt-signal" d="%s"/>' % wob([(10, 26), (40, 16), (70, 28), (100, 14), (128, 24)], 595, amp=2, overshoot=0))
    p.append(star(20, 100, 5)); p.append(star(120, 100, 4))
    return p


def _art_panner(v_=0):
    """A Dolby Atmos spatial panner: the room seen from above, speakers around
    the edge, a position puck off centre, and an elevation bar beside it."""
    room = [(16, 16), (108, 16), (108, 108), (16, 108)]
    p = ['<path class="riso" d="%s"/>' % poly(room, 651, amp=2.2),
         '<path d="%s"/>' % wob(room, 652, amp=2.2, close=True)]

    # the grid inside the room
    for i, v in enumerate((39, 62, 85) if v_ == 0 else (47, 77)):
        p.append('<path class="thin" d="%s"/>' % wob([(16, v), (108, v)], 660 + i, amp=1.1, overshoot=0))
        p.append('<path class="thin" d="%s"/>' % wob([(v, 16), (v, 108)], 670 + i, amp=1.1, overshoot=0))

    # speakers around the edge: four corners, centre front, two surrounds
    for i, (x, y) in enumerate([(16, 16), (62, 16), (108, 16), (16, 62), (108, 62), (16, 108), (108, 108)]):
        p.append('<circle class="spk" cx="%d" cy="%d" r="4.2"/>' % (x, y))
    # the second cut marks the opposite corner, so the two rooms do not
    # read as the same picture at tile size
    if v_:
        p.append('<circle class="fill-solid" cx="108" cy="16" r="4.2"/>')
    else:
        p.append('<circle class="fill-solid" cx="16" cy="108" r="4.2"/>')

    # the puck, off centre, with its crosshair
    px, py = (80, 44) if v_ == 0 else (38, 88)
    p.append('<path class="thin" stroke-dasharray="3 4" d="%s"/>' % wob([(16, py), (108, py)], 680, amp=0.8, overshoot=0))
    p.append('<path class="thin" stroke-dasharray="3 4" d="%s"/>' % wob([(px, 16), (px, 108)], 681, amp=0.8, overshoot=0))
    p.append('<circle class="puck" cx="%d" cy="%d" r="9"/>' % (px, py))
    p.append('<circle class="fill-solid" cx="%d" cy="%d" r="3"/>' % (px, py))

    # elevation, read bottom to top
    ex = 122 if v_ == 0 else 4
    p.append('<path d="%s"/>' % wob([(ex, 16), (ex, 108)], 690, amp=1.0, overshoot=0))
    for i, y in enumerate((16, 62, 108)):
        p.append('<path class="thin" d="%s"/>' % wob([(ex - 4, y), (ex + 4, y)], 694 + i, amp=0.6, overshoot=0))
    p.append('<circle class="puck" cx="%d" cy="%d" r="5.5"/>' % (ex, 34 if v_ == 0 else 92))

    p.append(star(126, 124, 5) if v_ == 0 else star(124, 8, 5))
    p.append(star(8, 8, 4) if v_ == 0 else star(10, 126, 4))
    return p


def _art_waveform(v=0):
    """A waveform sitting in an audio track lane, the way it looks in a session."""
    p = []
    lane = [(12, 34), (128, 34), (128, 94), (12, 94)]
    p.append('<path class="riso" d="%s"/>' % poly(lane, 701, amp=2))
    p.append('<path d="%s"/>' % wob(lane, 702, amp=2, close=True))

    # the centre line the waveform sits on
    p.append('<path class="thin" d="%s"/>' % wob([(12, 64), (128, 64)], 703, amp=0.8, overshoot=0))

    # the waveform itself, drawn as vertical strokes of varying height
    rnd = random.Random(704 + v * 37)
    x = 18
    while x < 124:
        env = math.sin((x - 18) / 106.0 * math.pi)
        h = (3 + rnd.random() * 24) * (0.3 + env * 0.9)
        p.append('<path class="wf" d="M%.1f,%.1f L%.1f,%.1f"/>' % (x, 64 - h, x, 64 + h))
        x += 3.4

    # the clip name strip along the top of the lane
    p.append('<path class="thin" d="%s"/>' % wob([(12, 42), (128, 42)], 705, amp=0.8, overshoot=0))
    p.append('<path class="thin" d="%s"/>' % wob([(18, 38), (18 + (36 if v == 0 else 68), 38)], 706, amp=0.7, overshoot=0))

    p.append(star(122, 20, 5))
    p.append(star(16, 110, 4))
    return p


ART["panner"] = _svg(_art_panner(), "A spatial panner seen from above, with speakers around the edge and a position puck")
ART["panner2"] = _svg(_art_panner(1), "A spatial panner seen from above, the position puck low and left")
ART["waveform"] = _svg(_art_waveform(), "A waveform sitting in an audio track lane")
ART["waveform2"] = _svg(_art_waveform(1), "A different waveform sitting in an audio track lane")

ART["session"] = _svg(_art_session(), "A drawn session layout with labelled tracks")
ART["sheet"] = _svg(_art_sheet(), "A drawn one-page document")
ART["sheet2"] = _svg(_art_sheet(1), "A drawn one-page document with a heading block")
ART["card"] = _svg(_art_card(), "A drawn reference card")
ART["tags"] = _svg(_art_tags(), "Three drawn metadata tags")
ART["chain"] = _svg(_art_chain(), "A drawn chain of three processors under a waveform")




# Brand colours, cycled one per letter for the accent word in an h1.
LETTER_HUES = ["#C04334", "#E3A347", "#33658A", "#7A51B1", "#197278", "#4F7942", "#B94A24"]


def rainbow(word):
    """Each letter takes the next brand colour. Spaces and hyphens keep
    their own colour so the word still reads as one thing."""
    out = []
    i = 0
    for ch in word:
        if ch.strip() == "":
            out.append(" ")
            continue
        out.append('<span class="l" style="color:%s">%s</span>' % (LETTER_HUES[i % len(LETTER_HUES)], ch))
        i += 1
    return '<span class="starred">%s</span>' % "".join(out)


def starred(word):
    """A word with stars behind it, in a single colour."""
    return '<span class="starred">%s</span>' % word


WORDMARK = ('<img class="logo" src="images/elfboi-logo-onDark.png" '
            'alt="elfboi" width="600" height="196">')

NAV = [
    ("tools", "index.html#tools"),
    ("learn", "learn.html"),
    ("templates", "templates.html"),
    ("about", "about.html"),
    # blog.html exists but is deliberately not in the menu
]


# Vercel Web Analytics, the plain-HTML version: no package, no framework, no
# cookies. Enabling it in the Vercel dashboard serves the script from the
# project itself, which is why it is a same-origin path rather than a URL to
# somewhere else — ad blockers rarely touch it.
#
# The dashboard, with its framework dropdown set to HTML, shows the exact path
# for this project. If it differs from the default below, change this one line.
ANALYTICS_SRC = "/_vercel/insights/script.js"

ANALYTICS = f"""<script>
  window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
</script>
<script defer src="{ANALYTICS_SRC}"></script>"""


def head(title, description, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en" data-display="bungee">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png?v=2">
<link rel="icon" type="image/png" sizes="16x16" href="images/favicon-16.png?v=2">
<link rel="apple-touch-icon" sizes="180x180" href="images/icon-180.png?v=2">
<meta property="og:type" content="website">
<meta property="og:site_name" content="elfboi">
<meta name="theme-color" content="#C04334">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600&family=Bungee&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="elfboi.css">
<!-- Proves to Google that this domain is ours. It is one of the three ways
     AdSense will verify a site, alongside ads.txt at the root and the ad
     loader script, and it is the only one that costs a page anything close to
     nothing: no JavaScript, no request to Google. It does NOT put ads on a
     page — the ad units live only in src/clipped-web.html, and this tag
     changes nothing about where they appear. -->
<meta name="google-adsense-account" content="ca-pub-3965216469889452">
{ANALYTICS}

{extra}</head>
<body>
<a class="skip" href="#main">skip to content</a>
<div class="page">
"""


def masthead(current=""):
    """Sticky. The wordmark sits in the same corner on every page."""
    drop = "".join(
        ('<li><a href="%s.html"><span class="dot" style="background:%s"></span>%s</a></li>'
         % (t["slug"], t["hue"], t["name"])) if t["live"] else
        ('<li><span class="drop-soon"><span class="dot" style="background:%s"></span>%s</span></li>'
         % (t["hue"], t["name"]))
        for t in TOOLS
    )
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if label == current else ""
        if label == "tools":
            links.append(
                '<li class="has-drop">'
                '<a href="%s"%s>tools</a>'
                '<div class="drop"><ul>%s'
                '<li class="drop-all"><a href="index.html#tools">all tools</a></li>'
                '</ul></div></li>' % (href, cur, drop)
            )
        else:
            links.append('<li><a href="%s"%s>%s</a></li>' % (href, cur, label))

    return """<header class="masthead-bar">
  <div class="wrap">
    <div class="masthead">
      <a class="wordmark" href="index.html">%s</a>
      <nav class="nav" aria-label="Main"><ul>%s</ul></nav>
    </div>
  </div>
</header>
""" % (WORDMARK, "".join(links))


SIGNUP = """<div class="wrap">
  <section class="signup sec sec-4" id="signup">
    <div class="signup-inner">
      <div>
        <h2>Get updated</h2>
        <p class="muted">On beta and full releases, new templates, and course drops.</p>
      </div>
      <div>
        <!-- Kit: paste your form action into KIT_FORM_ACTION in elfboi.js -->
        <form class="signup-form">
          <label class="sr" for="email-%ID%">Email address</label>
          <input id="email-%ID%" type="email" name="email_address" placeholder="you@somewhere" required autocomplete="email">
          <button type="submit">join</button>
        </form>
              </div>
    </div>
  </section>
</div>
"""

FOOT = """<div class="wrap">
  <footer class="foot">
    <span>&copy; 2026 elfboi</span>
    <a href="mailto:hello@elfboi.io">hello@elfboi.io</a>
  </footer>
</div>
"""

TAIL = """</div>
<script src="elfboi.js"></script>
</body>
</html>
"""


def signup(page_id):
    return SIGNUP.replace("%ID%", page_id)


def sketch_box(seed, w=120, h=44):
    """A wobbly rectangle, drawn the same way as everything else."""
    pts = [(3, 3), (w - 3, 3), (w - 3, h - 3), (3, h - 3)]
    return ('<svg class="sketch" viewBox="0 0 %d %d" preserveAspectRatio="none" aria-hidden="true">'
            '<path d="%s"/></svg>' % (w, h, wob(pts, seed, amp=1.6, close=True, overshoot=0)))



def wav_seconds(path):
    """Length of a WAV, read from its own header, so the player can show a
    duration before anything is downloaded."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(4096)
        i = head.index(b"fmt ")
        import struct
        ch, rate = struct.unpack("<HI", head[i + 10:i + 16])
        bits = struct.unpack("<H", head[i + 30:i + 32])[0] if False else None
        bps = struct.unpack("<I", head[i + 16:i + 20])[0]          # bytes per second
        j = head.index(b"data", i)
        n = struct.unpack("<I", head[j + 4:j + 8])[0]
        return n / float(bps)
    except Exception:
        return 0.0


def mmss(sec):
    m, s = divmod(int(round(sec)), 60)
    return "%d:%02d" % (m, s)


def tag_list(tags, accent_first=False):
    """Discs, alternating filled and outlined, so a tag never reads
    like a link."""
    out = []
    for i, t in enumerate(tags):
        out.append(
            f'<li class="tag-mark">'
            f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{star_path(12, 12, 11)}"/></svg>'
            f'<span>{t}</span></li>')
    return '<ul class="tags tags-mark">' + "".join(out) + "</ul>"


# ==========================================================
#  PAGES
# ==========================================================

def build_home():
    tiles = []
    for i, tool in enumerate(TOOLS):
        tag_html = "".join(f'<li class="ttag">{sketch_box(760 + n)}<span>{t}</span></li>'
                           for n, t in enumerate(tool["tags"][:2]))
        style = (f"--tool-hue:{tool['hue']};--tool-solid:{tool['hue_solid']};"
                 f"--tool-wash:{tool['hue_wash']};--tool-mid:{tool['hue_mid']}")
        inner = f"""        <div class="tile-body">
          <div class="tile-art">{ART[tool['slug']]}</div>
          <div class="tile-copy">
            <p class="tile-name">{tool['name']}</p>
            <p class="tile-desc">{tool['desc']}</p>
            <ul class="tile-tags">{tag_html}</ul>
          </div>
        </div>
        <div class="tile-foot">
          <span class="status {tool['status_class']}">{tool['status']}</span>
          <span class="tile-go">{'open &rarr;' if tool['live'] else ''}</span>
        </div>"""

        if tool["live"]:
            tiles.append(f'      <a class="tile" href="{tool["slug"]}.html" style="{style}">\n{inner}\n      </a>')
        else:
            # Page exists and can be worked on, but nothing links to it yet.
            tiles.append(
                f'      <div class="tile tile-soon" style="{style}">\n{inner}\n'
                f'        <div class="soon" style="--spin:{-16 + i * 8}deg">'
                f'<svg class="soon-star" viewBox="0 0 200 200" aria-hidden="true"><path d="{star_path(100, 100, 96)}"/></svg>'
                f'<span class="soon-text">coming<br>soon</span></div>\n'
                f'      </div>'
            )

    return head(
        "elfboi — an artist-led audio hub",
        "elfboi is an artist-led audio hub for tools and learning.",
    ) + masthead("tools") + f"""<main id="main">

  <div class="wrap">
    <section class="band band-hero sec sec-1">
      <div class="hero">
        <div class="hero-text">
          <h1 class="h1-xl"><span class="nowrap">An {rainbow("artist-led")}</span><br><span class="nowrap">audio hub for</span><br><span class="nowrap">tools &amp; learning</span></h1>
        <aside class="scroll-note">
              <div class="note-body">
                <span class="eyebrow">newsletter</span>
                <p>Keep up to date with beta and full releases,<br>new templates, and course drops.</p>
                <form class="signup-form">
                  <label class="sr" for="email-hero">Email address</label>
                  <input id="email-hero" type="email" name="email_address" placeholder="you@somewhere" required autocomplete="email">
                  <button type="submit">join</button>
                </form>
                <p class="note-foot">Want to collaborate with us? <a href="mailto:hello@elfboi.io">Say hello</a></p>
              </div>
        </aside>
        </div>
        <div class="hero-art">{ART['hub']}</div>
      </div>
    </section>
  </div>

  <div class="wrap">
    <section class="band sec sec-2" id="tools">
      <h2 class="section-label">tools</h2>
      <div class="grid">
{chr(10).join(tiles)}
      </div>
    </section>
  </div>

  <div class="wrap">
    <section class="band band-photo sec sec-3">
      <div class="photo-holder"><div class="photo-frame"><img class="photo-wide" src="images/studio-wide.jpg" alt="A studio control room seen from behind the engineer, large console and monitors">
        <svg class="photo-spark ps-left" viewBox="0 0 60 60" aria-hidden="true"><path d="{star_path(22, 22, 15)}"/><path d="{star_path(44, 42, 8)}"/></svg>
        <svg class="photo-spark ps-right" viewBox="0 0 60 60" aria-hidden="true"><path d="{star_path(38, 24, 16)}"/><path d="{star_path(16, 44, 9)}"/></svg></div></div>
    </section>
  </div>

</main>
""" + signup("home") + FOOT + TAIL


TOOL_SECTIONS = [
    ("overview", "overview"),
    ("examples", "listen"),
    ("try", "try it"),
    ("download", "download"),
    ("specs", "specs"),
    ("tutorial", "tutorial"),
    ("gallery", "gallery"),
]


def build_tool(tool):
    # Three looks, said as one sentence with each look wearing itself.
    # The same spans the About page uses, so the idea reads identically
    # wherever it appears; here "light" takes the tool's own colour.
    looks_html = (
        '<p class="looks-line">Every elfboi plug-in comes with three looks: '
        '<span class="m-light">light</span>, <span class="m-dark">dark</span>, and '
        '<span class="movers">' + rainbow("artist") + '</span>.'
        + (f' The artist look for {tool["name"]} was designed with '
           f'<a href="about.html#josh">{tool["collab"]}</a>.' if tool.get("collab")
           else " The artist look is designed with a guest artist, different for every tool.")
        + "</p>")

    # Before and after, at three degrees of damage. Each pair plays through
    # the site's own player rather than the browser's, so it matches
    # everything else on the page.
    if tool.get("audio"):
        sets = []
        for level, label in tool["audio"]:
            rows = "".join(
                f'''<div class="clip" data-src="audio/{level}-{kind}.wav">
              <button class="clip-play" type="button" aria-label="Play the {name.lower()} take, {label.lower()}">
                <svg viewBox="0 0 20 20" aria-hidden="true"><path class="ic-play" d="M6 4 L16 10 L6 16 Z"/><path class="ic-pause" d="M6.5 4.5 V15.5 M13.5 4.5 V15.5"/></svg>
              </button>
              <span class="clip-name">{name}</span>
              <div class="clip-bar"><span class="clip-fill"></span></div>
              <span class="clip-time">{mmss(wav_seconds(f"audio/{level}-{kind}.wav"))}</span>
            </div>'''
                for kind, name in (("clipped", "Clipped"), ("restored", "Restored")))
            sets.append(f'<div class="ab-set"><h3>{label}</h3>{rows}</div>')
        listen_html = '<div class="ab">' + "".join(sets) + "</div>"
    else:
        listen_html = ('<div class="frame frame-audio">before &mdash; audio player</div>'
                       '<div class="frame frame-audio" style="margin-top:0.8rem">after &mdash; audio player</div>')

    if tool.get("versions"):
        sections = ([("overview", "overview"), ("examples", "listen")]
                    + [(v["id"], v["label"]) for v in tool["versions"]]
                    + [("tutorial", "tutorial")])
    else:
        sections = TOOL_SECTIONS
    sidenav = "".join(f'<li><a href="#{sid}">{label}</a></li>' for sid, label in sections)

    if tool.get("versions"):
        # The button carries the version's name and nothing else; what it
        # costs is stated on its own line underneath, so the label stays a
        # name rather than a name and a price crammed into one line.
        links = "".join(
            f'<span class="version-pick">'
            f'<a class="btn" href="#{v["id"]}">{v["label"]}</a>'
            + (f'<span class="version-pick-note">{v["price"]}</span>' if v.get("price") else "")
            + '</span>'
            for v in tool["versions"])
        buttons = f'<p class="versions-label">Versions</p><div class="btn-row">{links}</div>'
    else:
        buttons = '<div class="btn-row"><a class="btn" href="#download">buy</a></div>'

    if tool.get("video"):
        shot = (f'<div class="photo-frame shot-frame">'
                f'<video class="tool-video" poster="{tool.get("poster", "")}"'
                f' autoplay muted loop playsinline preload="metadata"'
                f' aria-label="{tool["name"]} running, with the restore fader being moved">'
                f'<source src="{tool["video"]}" type="video/webm">'
                f'<source src="{tool["video_mp4"]}" type="video/mp4">'
                f'</video>'
                f'</div>')
    else:
        shot = '<div class="frame frame-tall">plug-in photo goes here</div>'

    if tool.get("shots"):
        gallery = "".join(
            (f'<img class="version-still" src="{sh[0]}" alt="{sh[1]}" loading="lazy">'
             if len(sh) > 2 and sh[2] == "still" else
             f'<div class="photo-frame shot-frame"><img src="{sh[0]}" alt="{sh[1]}" loading="lazy"></div>')
            for sh in tool["shots"])
    else:
        gallery = ('<div class="frame">image 01</div><div class="frame">image 02</div>'
                   '<div class="frame">image 03</div>')

    # A tool with a real walkthrough names its YouTube id; the rest keep the
    # placeholder so it stays obvious which ones are still waiting for one.
    tut = tool.get("tutorial_id", "")
    tutorial_block = f"""      <section class="chunk" id="tutorial">
        <h2>Tutorial</h2>
        <div class="video">
          {'' if tut else '<!-- Replace VIDEO_ID with this tool&#39;s walkthrough. -->'}
          <iframe src="https://www.youtube-nocookie.com/embed/{tut or 'VIDEO_ID'}"
                  title="{tool['name']} walkthrough"
                  allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"
                  referrerpolicy="strict-origin-when-cross-origin"
                  allowfullscreen loading="lazy"></iframe>
        </div>
      </section>"""

    if tool.get("versions"):
        blocks = []
        for v in tool["versions"]:
            shots = "".join(
                (f'<img class="version-still" src="{sh[0]}" alt="{sh[1]}" loading="lazy">'
                 if len(sh) > 2 and sh[2] == "still" else
                 f'<div class="photo-frame shot-frame no-shift"><img src="{sh[0]}" alt="{sh[1]}" loading="lazy"></div>')
                for sh in v["shots"])
            # A framed screenshot fills the height of the specs beside it, so the
            # two columns end on the same line. A cut-out still is left alone:
            # it has no frame to square up and stretching it would distort it.
            fills = any(not (len(sh) > 2 and sh[2] == "still") for sh in v["shots"])
            # A version that sells something reads its link from BUY, the same
            # way a template page does. No entry means no checkout yet, so the
            # button says so and does nothing rather than pointing at "#" —
            # a button that looks live and goes nowhere is worse than an
            # honest one. Add the URL to BUY and it becomes a real link.
            if v.get("buy"):
                link = BUY.get(v["buy"], "")
                btns = (f'<a class="btn" href="{link}" target="_blank" rel="noopener">Buy now</a>'
                        if link else '<span class="btn btn-off">coming soon</span>')
            else:
                btns = "".join(
                    f'<a class="btn{"".join(" btn-" + f for f in b[2:])}" '
                    f'href="{b[1]}">{b[0]}</a>'
                    for b in v.get("buttons", []))
            price_chip = (f'<span class="price-chip">{v["price"]}</span>') if v.get("price") else ""
            specs = "".join(f"<div><dt>{k}</dt><dd>{val}</dd></div>" for k, val in v["specs"])
            blocks.append(f"""      <section class="chunk" id="{v['id']}">
        <h2>{v['title']}{price_chip}</h2>
        <p class="version-summary">{v['summary']}</p>
        <h3>Get it</h3>
        <div class="btn-row">{btns}</div>
        <div class="version">
          <div class="version-shots{' shot-fill' if fills else ''}">{shots}</div>
          <div class="version-specs">
            <h3>Specs</h3>
            <dl class="specs">{specs}</dl>
          </div>
        </div>
      </section>""")
        blocks.append(tutorial_block)
        version_blocks = "\n".join(blocks)
    else:
        version_blocks = f"""      <section class="chunk" id="try">
        <h2>Try it</h2>
        <p>{tool['demo']}</p>
        <div class="frame">live demo goes here</div>
      </section>
      <section class="chunk" id="download">
        <h2>Download</h2>
        <p>{tool['price']}</p>
        <div class="btn-row">
          <a class="btn" href="#">macOS</a>
          <a class="btn" href="#">Windows</a>
          <a class="btn btn-quiet" href="#">release notes</a>
        </div>
        <p class="signup-note">Serve paid downloads from expiring signed links, never a fixed URL.</p>
      </section>
      <section class="chunk" id="specs">
        <h2>Specs</h2>
        <dl class="specs">
          <div><dt>where it runs</dt><dd>{tool['formats']}</dd></div>
          <div><dt>computers</dt><dd>Mac (macOS 12 and later) and Windows (10 and later)</dd></div>
          <div><dt>looks</dt><dd>Light mode, dark mode, and an artist mode designed with a guest artist</dd></div>
          <div><dt>licence</dt><dd>Use it on three machines. No account needed to run it.</dd></div>
        </dl>
      </section>
{tutorial_block}
      <section class="chunk" id="gallery">
        <h2>Gallery</h2>
        <div class="shots">{gallery}</div>
      </section>"""

    badge_text = tool.get("sticker") or tool["status"]
    sticker = (f'<div class="sticker">'
               f'<svg class="sticker-star" viewBox="0 0 200 200" aria-hidden="true">'
               f'<path d="{star_path(100, 100, 98)}"/></svg>'
               f'<span>{badge_text}</span></div>')
    status_line = ""

    return head(
        f"{tool['name']} — elfboi",
        tool["desc"],
    ) + masthead("tools") + f"""<main id="main" class="wrap tool-page sec sec-full" style="--tool-hue:{tool['hue']};--tool-solid:{tool['hue_solid']};--tool-wash:{tool['hue_wash']};--tool-mid:{tool['hue_mid']}">

  <div class="layout-sidenav">
    <nav class="sidenav" aria-label="On this page">
      <ol>{sidenav}</ol>
    </nav>

    <div>
      <a class="back back-right" href="index.html#tools">&larr; back to tools</a>
      <header class="tool-head">
        <div class="tool-hero">
          <div>
            <div class="tile-art tool-art" style="height:150px;margin-bottom:1.6rem">{ART[tool['slug']]}</div>
            <h1 class="tool-title">{tool['name']}</h1>
            <p class="tool-sub">{tool['line']}</p>
            <div class="tool-meta">
              <div>
                {f'<p class="collab">Artist version by <a href="about.html#josh">{tool["collab"]}</a></p>' if tool.get("collab") else ""}
                {tag_list(tool['tags'], accent_first=True)}
              </div>
              {f'<p class="tool-price">{tool["headline_price"]}</p>' if tool.get("headline_price") else ""}
            </div>
            <div class="versions" style="margin-top:1.8rem">{buttons}</div>
            {status_line}
          </div>
          <div class="tool-shot">
            {shot}
            {sticker}
          </div>
        </div>
      </header>

      <section class="chunk" id="overview">
        <h2>Overview</h2>
        <p>{tool['long']}</p>
        <p class="audience">For {tool['audience']}.</p>
        {looks_html}
      </section>

      <section class="chunk" id="examples">
        <h2>Listen</h2>
        {listen_html}
      </section>

{version_blocks}
    </div>
  </div>

</main>
""" + signup(tool["slug"]) + FOOT + TAIL


def build_browser():
    """The free browser version. This one is not generated: it is Lien's own
    self-contained app, kept at src/clipped-web.html and copied out verbatim,
    so a rebuild never overwrites it. It brings its own header, back link,
    advertising rails and newsletter."""
    with open(os.path.join(HERE, "src", "clipped-web.html"), encoding="utf-8") as fh:
        return fh.read()

def build_learn():
    # None of the courses are finished, so a row is not a link. It still lights
    # up under the pointer, and says where the course is while it does. The pages are still built and still reachable by
    # URL for checking them; nothing on the site points at one. Put the href
    # back and the row becomes an <a> again, with its hover behaviour intact.
    rows = "".join(
        f"""<li><div class="row row-hue row-soon" style="--row-hue:{c['hue']}">
          <span class="row-index">{i+1:02d}</span>
          <span><span class="row-title">{c['name']}</span></span>
          <span class="row-status">in development</span>
          <span class="row-meta">{c['length'].split(',')[0]}</span>
        </div></li>"""
        for i, c in enumerate(COURSES)
    )

    return head("learn — elfboi", "Editing, producing, mixing, and recording, taught from beginner to advanced.") \
        + masthead("learn") + f"""<main id="main">

  <div class="wrap">
    <section class="band band-hero sec sec-1">
      <div class="hero hero-photo">
        <div class="hero-text">
          <span class="page-label" style="--label-hue:#33658A">learn</span>
          <h1>Editing, producing, <span class="nowrap">{rainbow("mixing")}, and</span> recording</h1>
          <p class="lede">Beginner to advanced tutorials. Based on everything I have learned and taught, from the studio to the university.</p>
          <div class="btn-row" style="margin-top:1.6rem">
            <a class="btn" href="https://www.youtube.com/" target="_blank" rel="noopener">Visit the channel</a>
              </div>
        </div>
        <div class="hero-art hero-art-photo">
          <div class="photo-holder"><div class="photo-frame"><img class="photo-feathered" src="images/learn-studio.jpg" alt="Hands on a large mixing console in a studio, monitors above">
            <svg class="photo-spark ps-left" viewBox="0 0 60 60" aria-hidden="true"><path d="{star_path(22, 22, 15)}"/><path d="{star_path(44, 42, 8)}"/></svg>
            <svg class="photo-spark ps-right" viewBox="0 0 60 60" aria-hidden="true"><path d="{star_path(38, 24, 16)}"/><path d="{star_path(16, 44, 9)}"/></svg></div></div>
        </div>
      </div>
    </section>
  </div>

  <div class="wrap">
    <section class="band band-tight">
      <div class="video video-wide">
        <!-- Replace VIDEO_ID with the video you want people to land on. -->
        <iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID"
                title="elfboi on YouTube"
                allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"
                referrerpolicy="strict-origin-when-cross-origin"
                allowfullscreen loading="lazy"></iframe>
      </div>
    </section>
  </div>

  <div class="wrap">
    <section class="band band-tight sec sec-2">
      <div class="section-head">
        <h2 class="section-label">courses</h2>
        <p class="section-note">All coming soon. <a href="#signup">Join the newsletter</a>
          and we will tell you the moment one drops.</p>
      </div>
      <ul class="rows">{rows}</ul>
    </section>
  </div>

</main>
""" + signup("learn") + FOOT + TAIL


def build_course(c):
    lessons = "".join(
        f"""<li class="lesson"><span class="lesson-n">{i+1:02d}</span><span>{t}</span></li>"""
        for i, t in enumerate(c["lessons"])
    )
    return head(f"{c['name']} — elfboi", c["outcome"]) + masthead("learn") + f"""<main id="main" class="tool-page" style="--tool-hue:{c['hue']};--tool-solid:{c['hue']};--tool-mid:{c['hue']};--tool-wash:{c['hue']}22">

  <div class="wrap">
    <section class="band band-tight sec sec-1">
      <a class="back back-right" href="learn.html">&larr; back to courses</a>
      <span class="page-label" style="--label-hue:#C04334">course</span>
      <h1>{c['name']}</h1>
      <p class="lede">{c['outcome']}</p>
      <div class="btn-row" style="margin-top:1.6rem">
        <a class="btn" href="#">tell me when it opens</a>
      </div>
    </section>
  </div>

  <div class="wrap">
    <section class="band band-tight sec sec-2">
      <div class="cols">
        <div><h2>What is covered</h2>
          <p class="muted">{c['length']}</p>
        </div>
        <div><ol class="lessons">{lessons}</ol></div>
      </div>
    </section>
  </div>

  <div class="wrap">
    <section class="band band-tight sec sec-3">
      <div class="cols">
        <div><h2>Is this for you</h2></div>
        <div>
          <dl class="specs">
            <div><dt>made for</dt><dd>{c['who']}</dd></div>
            <div><dt>not for</dt><dd>{c['not_for']}</dd></div>
            <div><dt>length</dt><dd>{c['length']}</dd></div>
            <div><dt>price</dt><dd>{c['price']}</dd></div>
            <div><dt>access</dt><dd>Yours once bought. No subscription, no expiry.</dd></div>
          </dl>
        </div>
      </div>
    </section>
  </div>

</main>
""" + signup("course-" + c["slug"]) + FOOT + TAIL


def build_templates():
    order = ["sessions", "mixing", "editing", "recording", "one-sheets", "presets", "pro-tools", "film"]
    present = [c for c in order if any(c in t["cats"] for t in TEMPLATES)]
    filters = '<li><button class="filter" data-filter="all" aria-pressed="true">all</button></li>'
    filters += "".join(
        f'<li><button class="filter" data-filter="{c}" aria-pressed="false">{c.replace("-", " ")}</button></li>'
        for c in present
    )

    # A template is only a link once it is actually on sale. The rest keep the
    # same tile, but say where they are in the slot the arrow used to occupy
    # and go nowhere: the pages are still built and still open by URL, so the
    # moment a checkout link lands in BUY the tile becomes a link again.
    def _tile(t, i):
        inner = f"""        <div class="tile-body">
          <div class="tile-art">{ART[t['art']]}</div>
          <div class="tile-copy">
            <p class="tile-name">{t['name']}</p>
            <p class="tile-desc">{t['desc']}</p>
            <ul class="tile-tags">{"".join(f'<li class="ttag">{sketch_box(780 + n)}<span>{x.replace("-", " ")}</span></li>' for n, x in enumerate(t['cats'][:2]))}</ul>
          </div>
        </div>"""
        style = (f"--tool-hue:{t['hue']};--tool-solid:{t['hue']};"
                 f"--tool-wash:{t['hue']}1f;--tool-mid:{t['hue']}")
        tags = " ".join(t["cats"])
        if BUY.get(t["slug"]):
            return (f'      <a class="tile" href="template-{t["slug"]}.html" data-tags="{tags}" style="{style}">\n'
                    f'{inner}\n'
                    f'        <div class="tile-foot">\n'
                    f'          <span class="status">{t["format"]}</span>\n'
                    f'          <span class="tile-go">open &rarr;</span>\n'
                    f'        </div>\n'
                    f'      </a>')
        # Exactly the shape an unreleased tool tile has on the home grid: the
        # state on the left with its gold dot, the arrow slot left empty, and
        # the burst that springs up in the corner on hover.
        return (f'      <div class="tile tile-soon" data-tags="{tags}" style="{style}">\n'
                f'{inner}\n'
                f'        <div class="tile-foot">\n'
                f'          <span class="status is-building">in development</span>\n'
                f'          <span class="tile-go"></span>\n'
                f'        </div>\n'
                f'        <div class="soon" style="--spin:{-16 + i * 8}deg">'
                f'<svg class="soon-star" viewBox="0 0 200 200" aria-hidden="true"><path d="{star_path(100, 100, 96)}"/></svg>'
                f'<span class="soon-text">coming<br>soon</span></div>\n'
                f'      </div>')

    tiles = "".join(_tile(t, i) for i, t in enumerate(TEMPLATES))

    return head("templates — elfboi", "Session templates, one-sheets, and reference documents for audio work.") \
        + masthead("templates") + f"""<main id="main">

  <div class="wrap">
    <section class="band band-hero sec sec-1">
      <div class="hero hero-photo">
        <div class="hero-text">
          <span class="page-label" style="--label-hue:#7A51B1">templates</span>
          <h1>Start from something that already {rainbow("works")}</h1>
          <p class="lede">Projects, one-sheets, presets, and reference documents from real sessions.</p>
        </div>
        <div class="hero-art hero-art-photo hero-art-tall">
          <div class="photo-holder"><div class="photo-frame">
            <svg class="photo-spark ps-left" viewBox="0 0 60 60" aria-hidden="true"><path d="{star_path(22, 22, 15)}"/><path d="{star_path(44, 42, 8)}"/></svg>
            <svg class="photo-spark ps-right" viewBox="0 0 60 60" aria-hidden="true"><path d="{star_path(38, 24, 16)}"/><path d="{star_path(16, 44, 9)}"/></svg>
            <img class="photo-session" src="images/templates-session.jpg" alt="A Pro Tools session showing the dialogue tracks, groups and reverb sends of the 5.1 template"></div></div>
        </div>
      </div>
    </section>
  </div>

  <div class="wrap">
    <section class="band band-tight sec sec-2">
      <h2 class="section-label">available</h2>
      <ul class="filters filters-stick" aria-label="Filter templates">{filters}</ul>
      <div class="grid grid-tpl">{tiles}</div>
    </section>
  </div>

</main>
""" + signup("templates") + FOOT + TAIL


def build_template(t):
    includes = "".join(f"<li>{x}</li>" for x in t["includes"])
    if t.get("needs"):
        rows = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in t["needs"])
        needs = '<div class="version-info"><dl class="specs">' + rows + "</dl></div>"
    else:
        needs = ""

    # The gallery holds whatever screenshots this template has, and fills the
    # rest of the row with marked slots so it is obvious where the next ones
    # go and the one real shot does not stretch across the whole column.
    shots_ = t.get("shots") or []
    # A template can hand the header a composed picture — several screenshots
    # stacked into one — which hangs on the page without a photo frame and is
    # given more room than a single screenshot gets.
    hero = t.get("hero")
    if hero:
        first_shot = f'<img class="tool-still" src="{hero[0]}" alt="{hero[1]}">'
    elif shots_:
        first_shot = f'<img src="{shots_[0][0]}" alt="{shots_[0][1]}">'
    else:
        first_shot = '<div class="frame" style="min-height:260px">screenshot</div>'
    # One picture at a time, flipped through, so extra screenshots cost no
    # page height. Marked slots fill the set out to three while the real
    # pictures are still missing; they sit in the same box, so they are only
    # seen by someone who presses next.
    slides = ['<img class="shot-slide" src="%s" alt="%s" loading="lazy">' % (src, alt)
              for src, alt in shots_]
    if SHOW_EMPTY_SLOTS:
        slides += ['<div class="shot-slide frame">screenshot %02d</div>' % n
                   for n in range(len(slides) + 1, 4)]
    if not slides:
        slides = ['<div class="shot-slide frame">screenshot 01</div>']
    nav = ("" if len(slides) < 2 else
           '<div class="shotbox-nav">'
           '<button class="shotbox-arrow" type="button" data-dir="-1" aria-label="Previous screenshot">'
           '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M12.5 3.5 L5.5 10 L12.5 16.5"/></svg></button>'
           f'<span class="shotbox-count"><b>01</b> / {len(slides):02d}</span>'
           '<button class="shotbox-arrow" type="button" data-dir="1" aria-label="Next screenshot">'
           '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 3.5 L14.5 10 L7.5 16.5"/></svg></button>'
           "</div>")
    inside = (f'<div class="shotbox" tabindex="0" aria-roledescription="carousel" aria-label="Screenshots">'
              f'<div class="photo-frame shot-frame no-shift shotbox-stage">{"".join(slides)}</div>'
              f'{nav}</div>')

    link = BUY.get(t["slug"], "")
    if link:
        buy_btn = ('<a class="btn" href="' + link + '" target="_blank" rel="noopener">'
                   'Buy now</a>')
    elif t["price"].startswith("$"):
        buy_btn = '<span class="btn btn-off">not on sale yet</span>'
    else:
        buy_btn = '<span class="btn btn-off">priced at release</span>'
    price_chip = (f'<span class="price-chip">{t["price"]}</span>'
                  if t["price"].startswith("$") else "")

    sidenav = "".join(
        f'<li><a href="#{sid}">{label}</a></li>'
        for sid, label in [("overview", "overview"), ("inside", "a look inside"), ("needs", "what you need")])

    if t.get("video"):
        film = (f'<div class="video video-film">'
                f'<video class="film-video" controls playsinline preload="metadata"'
                f' poster="{t.get("poster", "")}">'
                + (f'<source src="{t["video_webm"]}" type="video/webm">'
                   if t.get("video_webm") else "")
                + f'<source src="{t["video"]}" type="video/mp4">'
                + '</video></div>')
    else:
        film = ('<div class="video">'
                '<!-- Replace VIDEO_ID with the short walkthrough of this template. -->'
                '<iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID"'
                f' title="{t["name"]} walkthrough"'
                ' allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"'
                ' referrerpolicy="strict-origin-when-cross-origin"'
                ' allowfullscreen loading="lazy"></iframe></div>')

    return head(f"{t['name']} — elfboi", t["desc"]) + masthead("templates") \
        + f"""<main id="main" class="wrap tool-page sec sec-full" style="--tool-hue:{t['hue']};--tool-solid:{t['hue']};--tool-wash:{t['hue']}22;--tool-mid:{t['hue']}">

  <div class="layout-sidenav">
    <nav class="sidenav" aria-label="On this page">
      <ol>{sidenav}</ol>
    </nav>

    <div>
      <a class="back back-right" href="templates.html">&larr; back to templates</a>
      <header class="tool-head">
        <div class="tool-hero">
          <div>
            <div class="tile-art tool-art" style="height:150px;margin-bottom:1.6rem">{ART[t['art']]}</div>
            <h1 class="tool-title">{t['name']}{price_chip}</h1>
            <p class="tool-sub">{t['desc']}</p>
            <div class="tool-meta">
              <div>{tag_list([c.replace('-', ' ') for c in t['cats']], accent_first=True)}</div>
            </div>
            <div class="versions" style="margin-top:1.8rem">
              {buy_btn}
              <a class="btn btn-outline" href="#needs">What you need</a>
            </div>
          </div>
          <div class="tool-shot{' tool-shot-still' if hero else ''}">
            {first_shot if hero else f'<div class="photo-frame shot-frame no-shift">{first_shot}</div>'}
          </div>
        </div>
      </header>

      <section class="chunk" id="overview">
        <h2>Overview</h2>
        <p>{t['long']}</p>
        <p class="audience">Works with {t['compat']}</p>
        <h3>In the download</h3>
        <ul class="ticks">{includes}</ul>
      </section>

      <section class="chunk" id="inside">
        <h2>A look inside</h2>
        <div class="inside{' inside-solo' if t.get('video') else ''}">
          {'' if t.get('video') else inside}
          <div class="inside-film">
            {film}
            <p class="film-note">{t.get('film_note', 'A short walkthrough of the session.')}</p>
          </div>
        </div>
      </section>

      <section class="chunk" id="needs">
        <h2>What you need</h2>
        <div class="version{'' if needs else ' version-solo'}">
          {needs}
          <div class="version-specs">
            <h3>Specs</h3>
            <dl class="specs">
              <div><dt>format</dt><dd>{t['format']}</dd></div>
              <div><dt>works with</dt><dd>{t['compat']}</dd></div>
              <div><dt>delivery</dt><dd>Instant download. Expiring link, sent by email.</dd></div>
              <div><dt>updates</dt><dd>Free, for as long as the file is maintained.</dd></div>
            </dl>
          </div>
        </div>
      </section>
    </div>
  </div>

</main>
""" + signup("template-" + t["slug"]) + FOOT + TAIL


def build_blog():
    posts = [
        ("What clipping actually removes", "Why a flattened peak sounds wrong, in terms you can hear rather than see.", "soon"),
        ("Clip gain before plug-in gain", "The order that makes dialogue easier to mix, and why.", "soon"),
        ("Metadata that survives a handover", "Fields worth filling in, and fields nobody ever reads.", "soon"),
    ]
    rows = "".join(
        f"""<li><a class="row" href="#">
          <span class="row-index">{i+1:02d}</span>
          <span><span class="row-title">{name}</span><span class="row-desc">{desc}</span></span>
          <span class="row-meta">{when}</span>
        </a></li>"""
        for i, (name, desc, when) in enumerate(posts)
    )

    return head("writing — elfboi", "Written versions of the tutorials, plus notes on building audio software.") \
        + masthead() + f"""<main id="main">

  <div class="wrap">
    <section class="band">
      <span class="page-label" style="--label-hue:#B94A24">writing</span>
      <h1>The written version of everything on {starred("video")}</h1>
      <p class="lede">Not linked in the menu on purpose. This exists so the tutorials are findable in a search, and so there is somewhere to point people.</p>
    </section>
  </div>

  <div class="wrap">
    <section class="band">
      <h2>Posts</h2>
      <ul class="rows">{rows}</ul>
    </section>
  </div>

</main>
""" + signup("blog") + FOOT + TAIL


PEOPLE_CORE = [
    ("\u201cElfboi\u201d Lenny", "founder",
     "Lenny created elfboi as an artist, recording studio manager, and University professor in the Bay "
     "Area. She writes the courses and builds the templates and collaborates with artists on every tool!"),
    ("Anthony Leedom", "engineering, and a constant",
     "Anthony builds the machinery behind several of the tools and works on training them. He is a music "
     "producer, and he and Lenny were in a band together at college, which is roughly how this started."),
]

PEOPLE_GUEST = [
    ("Josh Hong", "artist mode for", "Clipped", "clipped.html", "https://josh-hong.com/",
     "Josh designed the artist mode for Clipped: the third look every tool ships with, alongside light and dark."),
]


FACE_HUES = {"\u201cElfboi\u201d Lenny": "#C04334", "Anthony Leedom": "#33658A", "Josh Hong": "#7A51B1"}
FACE_TINTS = {"\u201cElfboi\u201d Lenny": "#F0CFC9", "Anthony Leedom": "#CBD9E6", "Josh Hong": "#DDD0EE"}


def face(name, size):
    """A doodle portrait. One line weight, dot eyes, one or two
    identifying features. Not a likeness."""
    parts = PORTRAITS.get(name, portrait_anthony)()
    hue = FACE_HUES.get(name, "#4F7942")
    tint = FACE_TINTS.get(name, "#DDE5D0")
    return f'''<svg class="face face-{size}" style="--face-hue:{hue};--face-tint:{tint}" viewBox="0 0 100 100" role="img" aria-label="Doodle portrait of {name}">
      <circle class="face-fill" cx="50" cy="50" r="47"/>
      <circle class="face-ring" cx="50" cy="50" r="47"/>
      {"".join(parts)}
    </svg>'''


PILLAR_HUES = ["#C04334", "#33658A", "#197278", "#7A51B1"]


def build_about():
    pillars = [
        ("design", "Every tool is drawn before it is built, and drawn to be understood in five minutes. "
                   "Each one ships with a light mode, a dark mode, and an artist mode made with a guest artist."),
        ("utility", "Tools that each solve one very specific thing that anyone can use."),
        ("access", "Understandable in five minutes and priced so it is not only for studios. "
                   "Built to work for people whose eyes, ears, and hands differ."),
        ("collaboration", "We work with artists on all of our plug-ins. The artist mode is how we put their "
                          "work in front of the people using ours."),
    ]
    pillar_html = "".join(
        f'''<li class="pillar" style="--pill:{PILLAR_HUES[i]}">
        <span class="pillar-n">{i+1:02d}</span>
        <h3>{t}</h3><p>{d}</p>
        <svg class="pillar-spark" viewBox="0 0 100 40" aria-hidden="true">{star(14, 20, 7)}{star(50, 12, 5)}{star(84, 24, 6)}</svg>
        </li>'''
        for i, (t, d) in enumerate(pillars)
    )

    core = "".join(
        f'''<li class="person">{face(n, 132)}
        <div><h3>{n}</h3><p class="person-role">{role}</p><p>{bio}</p></div></li>'''
        for n, role, bio in PEOPLE_CORE
    )

    guest = "".join(
        f'''<li class="person" id="{n.split()[0].lower()}">
        <a class="face-link" href="{url}" target="_blank" rel="noopener" aria-label="{n}, opens in a new tab">{face(n, 110)}</a>
        <div><h3><a class="person-link" href="{url}" target="_blank" rel="noopener">{n}</a></h3>
        <p class="person-role">{role} <a class="role-link" href="{worked_on}">{on}</a></p>
        <p>{bio}</p></div></li>'''
        for n, role, on, worked_on, url, bio in PEOPLE_GUEST
    )

    return head("about — elfboi", "elfboi is where design, utility, access, and collaboration meet.") \
        + masthead("about") + f"""<main id="main" class="page-about">

  <div class="wrap">
    <section class="band band-hero sec sec-1">
      <div class="hero">
        <div class="hero-text">
          <span class="page-label" style="--label-hue:#197278">about</span>
          <h1 class="about-lead">{rainbow("elfboi")} is</h1>
          <h2 class="about-rest">where design, utility, access, and collaboration meet</h2>
        </div>
        <div class="hero-art art-collab">{ART['collab']}</div>
      </div>
    </section>
  </div>

  <div class="wrap">
    <section class="band band-tight sec sec-2 band-values">
      <h2 class="section-label">our values</h2>
      <ul class="pillars">{pillar_html}</ul>
    </section>
  </div>

  <div class="wrap">
    <section class="band band-tight sec sec-3 band-after-values">
      <h2 class="section-label">who makes it</h2>
      <ul class="people-grid">{core}</ul>
    </section>
  </div>

  <div class="wrap">
    <section class="band band-tight sec sec-4">
      <h2 class="section-label">artists we work with</h2>
      <p class="lede lede-wide">Every plug-in comes with three looks: <span class="m-light">light</span>, <span class="m-dark">dark</span>, and <span class="movers">{rainbow("artist")}</span>. The artist mode is designed by somebody whose work we admire, and it is how we get their work in front of the people using ours.</p>
      <div class="artists-row">
        <ul class="people-grid people-grid-sm">{guest}</ul>
        <a class="callout" href="mailto:hello@elfboi.io">
          <span>Want to collaborate with us? Write to <strong>hello@elfboi.io</strong></span>
        </a>
      </div>
    </section>
  </div>

</main>
""" + signup("about") + FOOT + TAIL



def data_uri(path):
    """Inline an image so the holding page stays a single file."""
    import base64
    with open(os.path.join(HERE, path), "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode("ascii")


def build_placeholder():
    """A single self-contained page. No stylesheet, no script file, no
    build step. Copy index.html to a host and it works on its own."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>elfboi &mdash; an artist-led audio hub</title>
<meta name="description" content="elfboi is an artist-led audio hub for tools and learning. The site is under construction.">
<meta property="og:title" content="elfboi">
<meta property="og:description" content="An artist-led audio hub for tools and learning.">
<meta property="og:type" content="website">
<meta name="theme-color" content="#C04334">
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png?v=2">
<link rel="icon" type="image/png" sizes="16x16" href="images/favicon-16.png?v=2">
<link rel="apple-touch-icon" sizes="180x180" href="images/icon-180.png?v=2">
<meta property="og:type" content="website">
<meta property="og:site_name" content="elfboi">
<meta name="theme-color" content="#C04334">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600&family=Bungee&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {
  --ink:#22281D; --paper:#F7F2E6; --lift:#F3EDDC; --grey:#6E7266;
  --moss:#4F7942; --moss-deep:#2C4425; --gold:#E3A347; --gold-light:#E5BF80;
  --sans:"Fredoka","Helvetica Neue",Arial,sans-serif;
  --display:"Bungee","Fredoka",Arial,sans-serif;
  --mono:"DM Mono","SFMono-Regular",Consolas,monospace;
}
*,*::before,*::after{box-sizing:border-box}
html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:clamp(.96rem,.93rem + .15vw,1.02rem);line-height:1.55;-webkit-font-smoothing:antialiased}
em,i{font-style:normal;font-weight:600}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 clamp(1.25rem,4vw,3.5rem);position:relative;z-index:2}
.bar{display:flex;align-items:baseline;justify-content:space-between;gap:1.5rem;
  padding:1.6rem 0 1.3rem;border-bottom:1px solid #D9E2CF;flex-wrap:wrap}
.mark{display:inline-flex;align-items:center;line-height:0;text-decoration:none}
.mark img{display:block;height:30px;width:auto;transition:opacity .2s ease}
.mark:hover img{opacity:.78}
@media (max-width:620px){.mark img{height:24px}}
.status{font-family:var(--mono);font-size:.66rem;letter-spacing:.05em;color:var(--grey);
  display:inline-flex;align-items:center;gap:.45rem}
.status::before{content:"";width:6px;height:6px;background:var(--gold);display:block}
main{padding:clamp(2.6rem,6vw,4.6rem) 0 0}
.hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.9fr);
  gap:clamp(2rem,5vw,4rem);align-items:center}
h1{font-family:var(--display);font-size:clamp(2rem,1.3rem + 2.8vw,3.7rem);line-height:1.08;
  letter-spacing:.005em;font-weight:400;margin:0 0 1.5rem;max-width:13ch}
.l{display:inline-block;transition:transform .4s cubic-bezier(.34,1.5,.5,1)}
h1:hover .l{transform:translateY(-3px)}
h1:hover .l:nth-child(2n){transform:translateY(3px)}
h1:hover .l:nth-child(3n){transform:translateY(-5px)}
.starred{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='108' height='46' viewBox='0 0 108 46'%3E%3Cg fill='%23FFFFFF'%3E%3Cpath d='M14 2l2.1 5.9L22 10l-5.9 2.1L14 18l-2.1-5.9L6 10l5.9-2.1z'/%3E%3Cpath d='M76 6l1.5 4.2L81.7 12l-4.2 1.5L76 17.7l-1.5-4.2L70.3 12l4.2-1.5z'/%3E%3Cpath d='M46 30l1.7 4.6 4.6 1.7-4.6 1.7L46 42.6l-1.7-4.6-4.6-1.7 4.6-1.7z'/%3E%3Cpath d='M96 33l1.2 3.3 3.3 1.2-3.3 1.2L96 42l-1.2-3.3-3.3-1.2 3.3-1.2z'/%3E%3Cpath d='M30 40l1.1 3 3 1.1-3 1.1L30 48l-1.1-3-3-1.1 3-1.1z'/%3E%3C/g%3E%3C/svg%3E");
  background-repeat:repeat-x;background-size:auto 96%;background-position:0 50%;padding:0 .12em;
  transition:background-position .55s cubic-bezier(.34,1.3,.5,1)}
h1:hover .starred{background-position:14px 42%}
.lede{font-size:clamp(1.05rem,.98rem + .3vw,1.25rem);line-height:1.45;color:var(--moss-deep);
  max-width:46ch;margin:0 0 1.4rem}
p{margin:0 0 1.1rem;max-width:60ch}
.art svg{width:100%;height:auto;overflow:visible}
.art path,.art circle,.art ellipse{fill:none;stroke:var(--moss-deep);stroke-width:1.2;
  stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke}
.art .thin{stroke-width:.8;opacity:.55}
.art .wave,.art .sine{stroke-width:1.7}
.art .riso{fill:var(--gold-light);stroke:none;transform:translate(9px,9px);
  transition:transform .6s cubic-bezier(.2,.85,.25,1),fill .4s}
.art:hover .riso{transform:translate(0,0);fill:var(--gold)}
.art .riso-faint{opacity:.32}
.art .bead{fill:var(--paper);stroke:var(--moss-deep);stroke-width:1.4}
.art:hover .bead{fill:var(--ink);stroke:var(--ink)}
.art .fill-solid{fill:var(--moss-deep);stroke:none}
.art .spark{fill:var(--gold);stroke:none;opacity:0;transform-box:fill-box;transform-origin:center;
  transform:scale(.3) rotate(-30deg);transition:opacity .3s,transform .5s cubic-bezier(.34,1.6,.5,1)}
.art:hover .spark{opacity:1;transform:scale(1) rotate(0)}
.art .float{transition:transform .7s cubic-bezier(.34,1.4,.5,1)}
.art .f1{animation:bob 7s ease-in-out infinite}
.art .f2{animation:bob 9s ease-in-out infinite .8s}
.art .f3{animation:bob 8s ease-in-out infinite 1.6s}
.art:hover .f1{transform:translateY(-16px)}
.art:hover .f2{transform:translateY(-22px)}
.art:hover .f3{transform:translateY(-12px)}
.art .drift{animation:sway 11s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes sway{0%,100%{transform:translateX(0)}50%{transform:translateX(9px)}}
.note{position:relative;max-width:430px;margin-top:2.2rem}
.note-frame{position:absolute;inset:-6px -8px;width:calc(100% + 16px);height:calc(100% + 12px)}
.note-frame .fill{fill:var(--lift)}
.note-frame .edge{fill:none;stroke:var(--ink);stroke-width:1.8}
.note-body{position:relative;padding:1.4rem 1.5rem 1.3rem}
.label{font-family:var(--mono);font-size:.66rem;letter-spacing:.08em;color:#B94A24;
  display:block;margin-bottom:.5rem}
.note-body p{font-size:.88rem;margin-bottom:1rem}
form{display:flex;border-bottom:1px solid var(--ink)}
input{flex:1;min-width:0;background:transparent;border:0;padding:.75rem 0;
  font-family:var(--sans);font-size:1rem;color:var(--ink)}
input::placeholder{color:#B3B5A9}
input:focus{outline:none}
form:focus-within{border-bottom-color:var(--gold)}
button{background:none;border:0;padding:.75rem 0 .75rem 1.2rem;font-family:var(--mono);
  font-size:.68rem;letter-spacing:.05em;color:#33658A;cursor:pointer}
button:hover{color:#C04334}
button[disabled]{opacity:.5;cursor:default}
.small{font-family:var(--mono);font-size:.7rem;letter-spacing:.03em;color:var(--grey);
  margin:.7rem 0 0}
.small a{color:#7A51B1}
.msg{font-family:var(--mono);font-size:.72rem;margin:.8rem 0 0;color:var(--moss)}
.msg.bad{color:#C04334}
.what{border-top:1px solid #D9E2CF;margin-top:clamp(3rem,7vw,5rem);
  padding:clamp(2.4rem,5vw,3.6rem) 0}
.what h2{font-family:var(--sans);font-weight:600;font-size:clamp(1.4rem,1.1rem + 1vw,2rem);
  letter-spacing:-.02em;margin:0 0 1.4rem}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:0;
  border-top:1px solid #D9E2CF;border-left:1px solid #D9E2CF}
.cell{border-right:1px solid #D9E2CF;border-bottom:1px solid #D9E2CF;padding:1.4rem 1.3rem 1.6rem}
.cell h3{font-family:var(--sans);font-weight:600;font-size:1.05rem;margin:0 0 .5rem;
  letter-spacing:-.015em}
.cell:nth-child(1) h3{color:#C04334}
.cell:nth-child(2) h3{color:#33658A}
.cell:nth-child(3) h3{color:#197278}
.cell p{font-size:.86rem;color:var(--moss-deep);margin:0}
.n{font-family:var(--mono);font-size:.62rem;color:#B3B5A9;display:block;margin-bottom:.7rem}
footer{border-top:1px solid #D9E2CF;padding:1.8rem 0 2.6rem;display:flex;
  justify-content:space-between;gap:1.5rem;flex-wrap:wrap;font-family:var(--mono);
  font-size:.68rem;letter-spacing:.03em;color:var(--grey)}
footer a{color:var(--moss);text-decoration:none;border-bottom:1px solid transparent;padding-bottom:1px}
footer a:hover{color:var(--gold);border-bottom-color:var(--gold)}
.backdrop{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.wv{position:absolute;left:0;overflow:visible;animation-name:cross;
  animation-timing-function:linear;animation-fill-mode:both}
.wv path{fill:none;stroke-width:1.6;stroke-linecap:round;opacity:.22}
@keyframes cross{from{transform:translateX(-100%)}to{transform:translateX(100vw)}}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media (max-width:860px){.hero{grid-template-columns:1fr}.art{max-width:440px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}
  .backdrop{display:none}}
</style>
</head>
<body>
<div class="backdrop" aria-hidden="true"></div>

<div class="wrap">
  <header class="bar">
    <a class="mark" href="/"><img src="%LOGO%" alt="elfboi" width="600" height="196"></a>
    <span class="status">under construction</span>
  </header>
</div>

<main>
  <div class="wrap">
    <section class="hero">
      <div>
        <h1>An %HEAD% audio hub for <span class="nowrap">tools &amp; learning</span></h1>
        <p class="lede">elfboi makes audio tools, teaches how to use them, and shares the
        templates behind real sessions. It is being built now.</p>

        <aside class="note">
          <svg class="note-frame" viewBox="0 0 320 210" preserveAspectRatio="none" aria-hidden="true">
            <path class="fill" d="M6,10 L314,5 L316,202 L4,198 Z"/>
            <path class="edge" d="M6,10 L314,5 L316,202 L4,198 Z"/>
          </svg>
          <div class="note-body">
            <span class="label">newsletter</span>
            <p>Keep up to date with beta and full releases,<br>new templates, and course drops.</p>
            <form id="signup" novalidate>
              <label class="sr" for="email">Email address</label>
              <input id="email" name="email_address" type="email" placeholder="you@somewhere"
                     required autocomplete="email">
              <button type="submit">join</button>
            </form>
            <p class="msg" id="msg" role="status" aria-live="polite"></p>
            <p class="small">Want to collaborate with us?
              <a href="mailto:hello@elfboi.io">Say hello</a></p>
          </div>
        </aside>
      </div>

      <div class="art">%ART%</div>
    </section>
  </div>

  <div class="wrap">
    <section class="what">
      <h2>What elfboi is</h2>
      <div class="cols">
        <div class="cell"><span class="n">01</span><h3>tools</h3>
          <p>Small audio tools that each solve one very specific thing that anyone can use.
          Every one comes with a light mode, a dark mode, and an artist mode made with a guest artist.</p></div>
        <div class="cell"><span class="n">02</span><h3>learning</h3>
          <p>Courses and free videos on editing, producing, mixing, and recording, taught from
          beginner to advanced by a working professor and engineer.</p></div>
        <div class="cell"><span class="n">03</span><h3>templates</h3>
          <p>Projects, one-sheets, presets, and reference documents taken straight out of
          real sessions, so you can start from something that already works.</p></div>
      </div>
    </section>
  </div>

  <div class="wrap">
    <footer>
      <span>&copy; 2026 elfboi</span>
      <a href="mailto:hello@elfboi.io">hello@elfboi.io</a>
    </footer>
  </div>
</main>

<script>
/* ============================================================
   NEWSLETTER
   Put your Kit form ID between the quotes and this page starts
   collecting addresses. Nothing else needs changing.

   Where to find it: Kit -> Grow -> Landing Pages & Forms ->
   your form -> Embed -> HTML. The action URL in that snippet
   reads https://app.kit.com/forms/1234567/subscriptions and the
   number in the middle is your form ID.

   Use the form ID, never an API key. An API key (kit_...) is a
   server-side secret and anything in this file is readable by
   every visitor.
   ============================================================ */

var KIT_FORM_ID = "9845746";

(function () {
  var form = document.getElementById("signup");
  var msg = document.getElementById("msg");
  var input = document.getElementById("email");
  var button = form.querySelector("button");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    msg.className = "msg";

    if (!input.value || input.value.indexOf("@") === -1) {
      msg.className = "msg bad";
      msg.textContent = "That address does not look right.";
      return;
    }

    if (!KIT_FORM_ID) {
      msg.className = "msg bad";
      msg.textContent = "Not connected yet: add your Kit form ID in this page's script.";
      return;
    }

    button.disabled = true;
    button.textContent = "sending";

    var body = new FormData();
    body.append("email_address", input.value);

    fetch("https://app.kit.com/forms/" + KIT_FORM_ID + "/subscriptions", {
      method: "POST",
      body: body,
      headers: { Accept: "application/json" }
    })
      .then(function (r) { return r.json(); })
      .then(function () {
        form.style.display = "none";
        msg.textContent = "Thank you. Check your inbox to confirm.";
      })
      .catch(function () {
        msg.className = "msg bad";
        msg.textContent = "Something went wrong. Write to hello@elfboi.io instead.";
      })
      .finally(function () {
        button.disabled = false;
        button.textContent = "join";
      });
  });
})();

/* Drifting waveforms, the same idea as the full site. */
(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var host = document.querySelector(".backdrop");
  var colours = ["#4F7942", "#E3A347", "#C04334", "#33658A", "#7A51B1", "#197278"];
  var kinds = ["sine", "triangle", "saw", "square"];
  var bands = [], live = 0;

  function make() {
    if (live >= 3) return;
    var kind = kinds[Math.floor(Math.random() * 4)];
    var w = 260 + Math.random() * 260, amp = 8 + Math.random() * 14;
    var cycles = 5 + Math.floor(Math.random() * 6);
    var steps = (kind === "square" || kind === "saw") ? cycles * 4 : 72, d = "";
    for (var i = 0; i <= steps; i++) {
      var t = i / steps, ph = t * cycles, y;
      if (kind === "sine") y = Math.sin(ph * Math.PI * 2);
      else if (kind === "triangle") { var f = ph % 1; y = f < .5 ? -1 + f * 4 : 3 - f * 4; }
      else if (kind === "saw") y = ((ph % 1) * 2) - 1;
      else y = (ph % 1) < .5 ? -1 : 1;
      d += (i ? " L" : "M") + (t * w).toFixed(1) + "," + (70 + y * amp).toFixed(1);
    }
    var opts = [0, 1, 2, 3, 4].filter(function (b) { return bands.indexOf(b) === -1; });
    if (!opts.length) opts = [0, 1, 2, 3, 4];
    var band = opts[Math.floor(Math.random() * opts.length)];
    bands.push(band); if (bands.length > 2) bands.shift();

    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "wv"); svg.setAttribute("width", w); svg.setAttribute("height", 140);
    var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", d);
    path.setAttribute("stroke", colours[Math.floor(Math.random() * colours.length)]);
    svg.appendChild(path);
    svg.style.top = (2 + band * 18.4 + Math.random() * 10) + "%";
    var dur = 65 + Math.random() * 45;
    svg.style.animationDuration = dur + "s";
    host.appendChild(svg); live++;
    setTimeout(function () { svg.remove(); live--; }, dur * 1000 + 400);
  }

  make();
  (function loop() {
    setTimeout(function () { make(); loop(); }, 14000 + Math.random() * 12000);
  })();
})();
</script>
</body>
</html>
""".replace("%HEAD%", rainbow("artist-led")).replace("%ART%", ART["hub"]) \
       .replace("%LOGO%", data_uri("images/elfboi-logo-color.png")) \
       .replace("%FAV32%", data_uri("images/favicon-32.png")) \
       .replace("%FAV180%", data_uri("images/icon-180.png")) \
       .replace('href="images/favicon-32.png?v=2"', 'href="%s"' % data_uri("images/favicon-32.png")) \
       .replace('href="images/favicon-16.png?v=2"', 'href="%s"' % data_uri("images/favicon-16.png")) \
       .replace('href="images/icon-180.png?v=2"', 'href="%s"' % data_uri("images/icon-180.png"))


# ==========================================================
#  WRITE
# ==========================================================

KEEP = set()


def prune():
    """Remove pages left behind when a slug is renamed."""
    for f in os.listdir(HERE):
        if f.endswith(".html") and f not in KEEP:
            os.remove(os.path.join(HERE, f))
            print("removed stale", f)


def write(name, content):
    KEEP.add(name)
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)


if __name__ == "__main__":
    # The home page IS index.html. The old single-file holding page is no
    # longer built; build_placeholder() is still below if it is ever needed
    # again, but nothing calls it, so there is no second front door to
    # confuse with the real one.
    write("index.html", build_home())
    write("learn.html", build_learn())
    write("templates.html", build_templates())
    write("blog.html", build_blog())
    write("tools-clipped-browser.html", build_browser())
    write("about.html", build_about())
    for t in TOOLS:
        write(t["slug"] + ".html", build_tool(t))
    for c in COURSES:
        write("course-" + c["slug"] + ".html", build_course(c))
    for t in TEMPLATES:
        write("template-" + t["slug"] + ".html", build_template(t))
    prune()
    print("\ndone. open index.html for the site.")
