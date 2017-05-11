# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
from utils import *
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from note_mapping import *
from opensimplex import OpenSimplex
from power_supply_spatial import *
import sys

octaves = [3, 4, 5, 6]
note_values = ["C", "D", "F", "G"]
notes = [0, 2, 5, 7]

midi = Midi(number_tracks=1, tempo=120, instrument=11)
noteSeq = []

for t in range(0, 80):
	noteSeq.append(Note(t, 0, 0.125, 127))

midi.seq_notes(noteSeq, time=0)
midi.write("midi_output/test_pyknon.mid")
