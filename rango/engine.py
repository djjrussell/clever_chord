__author__ = 'Russell'


class Chord():


    def __init__(self):
        self.scale = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        self.map = {"major": "Major",
           "major-seven": "MajorSeven",
           "minor": "Minor",
           "minor-seven": "MinorSeven",
           "augmented": "Augmented",
           "diminished": "Diminished"
        }
        self.scale_dictionary = {}
        for i in range(0, len(self.scale)):
            note_name = self.scale[i]
            self.scale_dictionary[note_name] = i

        self.neck = ["E", "A", "D", "G", "B", "E"]
        self.neck_frets = {}

        for index in range(0, len(self.neck)):
            neck_note = self.neck[index]
            neck_index = self.scale_dictionary[neck_note]
            fret_count = 6
            neck_note_list = []
            for fret in range(0, fret_count):
                scale_note = self.scale[(neck_index + fret) % len(self.scale)]
                neck_note_list.append(scale_note)
            self.neck_frets[index] = neck_note_list
        self.build()


    def get_generic(self, note_name, offsets):
        note_name = note_name.upper()
        index = self.scale_dictionary[note_name]
        output = []
        for i in range(0, len(offsets)):
            sum = index + offsets[i]
            length = len(self.scale)
            output.append(self.scale[sum % length])

        return output


    def major(self,note_name):
        return self.get_generic(note_name, [0, 4, 7])


    def major_seven(self,note_name):
        return self.get_generic(note_name, [0, 4, 7, 10])


    def minor(self,note_name):
        return self.get_generic(note_name, [0, 3, 7])


    def minor_seven(self,note_name):
        return self.get_generic(note_name, [0, 3, 7, 10])


    def augmented(self,note_name):
        return self.get_generic(note_name, [0, 4, 8])


    def diminished(self,note_name):
        return self.get_generic(note_name, [0, 3, 6])

    def build(self):
        self.chords = dict()

        for note in self.scale:
            if (note not in self.chords):
                self.chords[note] = dict()
            self.chords[note]["major"] = self.major(note)
            self.chords[note]["major_seven"] = self.major_seven(note)
            self.chords[note]["minor"] = self.minor(note)
            self.chords[note]["minor_seven"] = self.minor_seven(note)
            self.chords[note]["augmented"] = self.augmented(note)
            self.chords[note]["diminished"] = self.diminished(note)




    def get_frets(self,chord_note_list):
        sf = []
        for i, fret in self.neck_frets.items():
            f=0
            for fret_note in fret:
                try:
                    fi = chord_note_list.index(fret_note)
                except ValueError:
                    fi = -1

                if fi >= 0:
                    #print fret_note
                    sf.append(f)
                    break
                f+=1
        return sf

    def Update(self, display_chord):
        #self.display_chord = Chord[self.map["type"]]("note")
        fingers = self.get_frets(display_chord)
        output = []
        for fp in range(1,5):
            line = ""
            for s in range(0,6):
                if fingers[s] == fp:
                    line += " O "
                else:
                    line += " | "
            output.append(line)
        return "\n".join(output)

    def get_strings(self, note, ch_type):
        c = Chord()
        if ch_type == "Major":
            response = c.Update(c.major(note))
        elif ch_type == "Major Seven":
            response = c.Update(c.major_seven(note))
        elif ch_type == "Minor":
            response = c.Update(c.minor(note))
        elif ch_type == "Minor Seven":
            response = c.Update(c.minor_seven(note))
        elif ch_type == "Augmented":
            response = c.Update(c.augmented(note))
        elif ch_type == "Diminished":
            response = c.Update(c.diminished(note))
        else:
            response = ch_type + ""
        return response
    
    def get_array(self, note, ch_type):
        c = Chord()
        if ch_type == "Major":
            response = c.major(note)
        elif ch_type == "Major Seven":
            response = c.major_seven(note)
        elif ch_type == "Minor":
            response = c.minor(note)
        elif ch_type == "Minor Seven":
            response = c.minor_seven(note)
        elif ch_type == "Augmented":
            response = c.augmented(note)
        elif ch_type == "Diminished":
            response = c.diminished(note)
        else:
            response = []
        return response

if __name__ == "__main__":
    chord_instance = Chord()
    print(chord_instance.get_frets(chord_instance.major("e")))
    print(chord_instance.get_strings("g", "Diminished"))





