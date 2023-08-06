# ------------------------------------------------------------------------------
# Purpose:       m21utils is a set of music21 utilities for use by musicdiff.
#                musicdiff is a package for comparing music scores using music21.
#
# Authors:       Greg Chapman <gregc@mac.com>
#                musicdiff is derived from:
#                   https://github.com/fosfrancesco/music-score-diff.git
#                   by Francesco Foscarin <foscarin.francesco@gmail.com>
#
# Copyright:     (c) 2022 Francesco Foscarin, Greg Chapman
# License:       MIT, see LICENSE
# ------------------------------------------------------------------------------

from fractions import Fraction
import math
import sys
from typing import List
# import sys
import music21 as m21

class M21Utils:
    @staticmethod
    def get_beamings(note_list):
        _beam_list = []
        for n in note_list:
            if n.isRest:
                _beam_list.append([])
            else:
                _beam_list.append(n.beams.getTypes())
        return _beam_list


    @staticmethod
    def generalNote_to_string(gn):
        """
        Return the NoteString with R or N, notehead number and dots.
        Does not consider the ties (because of music21 ties encoding).
        Arguments:
            gn {music21 general note} -- [description]
        Returns:
            String -- the noteString
        """
        out_string = ""
        # add generalNote type (Rest or Note)
        if gn.isRest:
            out_string += "R"
        else:
            out_string += "N"
        # add notehead information (4,2,1,1/2, etc...). 4 means a black note, 2 white, 1 whole etc...
        type_number = Fraction(m21.duration.convertTypeToNumber(gn.duration.type))
        if type_number >= 4:
            out_string += "4"
        else:
            out_string += str(type_number)
        # add the dot
        n_of_dots = gn.duration.dots
        for _ in range(n_of_dots):
            out_string += "*"
        return out_string


    @staticmethod
    def note2tuple(note):
        # pitch name (including octave, but not accidental)
        if isinstance(note, m21.note.Unpitched):
            # use the displayName (e.g. 'G4') with no accidental
            note_pitch = note.displayName
            note_accidental = "None"
        else:
            note_pitch = note.pitch.step + str(note.pitch.octave)

            # note_accidental is only set to non-'None' if the accidental will
            # be visible in the printed score.
            note_accidental = "None"
            if note.pitch.accidental is None:
                pass
            elif note.pitch.accidental.displayStatus is not None:
                if note.pitch.accidental.displayStatus:
                    note_accidental = note.pitch.accidental.name
            else:
                # note.pitch.accidental.displayStatus was not set.
                # This can happen when there are no measures in the test data.
                # We will guess, based on displayType.
                # displayType can be 'normal', 'always', 'never', 'unless-repeated', 'even-tied'
                # print("accidental.displayStatus unknown, so we will guess based on displayType", file=sys.stderr)
                displayType = note.pitch.accidental.displayType
                if displayType is None:
                    displayType = "normal"

                if displayType in ("always", "even-tied"):
                    note_accidental = note.pitch.accidental.name
                elif displayType == "never":
                    note_accidental = "None"
                elif displayType == "normal":
                    # Complete guess: the accidental will be displayed
                    # This will be wrong if this is not the first such note in the measure.
                    note_accidental = note.pitch.accidental.name
                elif displayType == "unless-repeated":
                    # Guess that the note is not repeated
                    note_accidental = note.pitch.accidental.name

            # TODO: we should append editorial style info to note_accidental here ('paren', etc)

        # add tie information (Unpitched has this, too)
        note_tie = note.tie is not None and note.tie.type in ("stop", "continue")
        return (note_pitch, note_accidental, note_tie)


    @staticmethod
    def pitch_size(pitch):
        """Compute the size of a pitch.
        Arguments:
            pitch {[triple]} -- a triple (pitchname,accidental,tie)
        """
        size = 0
        # add for the pitchname
        size += 1
        # add for the accidental
        if not pitch[1] == "None":
            size += 1
        # add for the tie
        if pitch[2]:
            size += 1
        return size


    @staticmethod
    def generalNote_info(gn):
        """
        Get a json of informations about a general note.
        The fields of the json are "type"-string (chord, rest,note), "pitches" (a list of pitches)-list of strings,"noteHead" (also for rests)-string,"dots"-integer.
        For rests the pitch is set to [\"A0\"].
        Does not consider the ties (because of music21 ties encoding).
        Arguments:
            gn {music21 general note} -- the general note to have the information
        """
        # pitches and type info
        if gn.isChord:
            pitches = [
                (p.step + str(p.octave), p.accidental)
                for p in gn.sortDiatonicAscending().pitches
            ]
            gn_type = "chord"
        elif gn.isRest:
            pitches = ["A0", None]  # pitch is set to ["A0"] for rests
            gn_type = "rest"
        elif gn.isNote:
            pitches = [
                (gn.step + str(gn.octave), gn.pitch.accidental)
            ]  # a list with  one pitch inside
            gn_type = "note"
        else:
            raise TypeError("The generalNote must be a Chord, a Rest or a Note")

        # notehead information (4,2,1,1/2, etc...). 4 means a black note, 2 white, 1 whole etc...
        type_number = Fraction(m21.duration.convertTypeToNumber(gn.duration.type))
        if type_number >= 4:
            note_head = "4"
        else:
            note_head = str(type_number)

        gn_info = {
            "type": gn_type,
            "pitches": pitches,
            "noteHead": note_head,
            "dots": gn.duration.dots,
        }
        return gn_info


    # def get_ties(note_list):
    #     _general_ties_list = []
    #     for n in note_list:
    #         if n.tie == None:
    #             _general_ties_list.append(None)
    #         else:
    #             _general_ties_list.append(n.tie.type)
    #     # keep only the information of when a note is tied to the previous
    #     # (also we solve the bad notation of having a start and a not specified stop, that can happen in music21)
    #     _ties_list = [False] * len(_general_ties_list)
    #     for i, t in enumerate(_general_ties_list):
    #         if t == 'start' and i < len(_ties_list) - 1:
    #             _ties_list[i + 1] = True
    #         elif t == 'continue' and i < len(_ties_list) - 1:
    #             _ties_list[i + 1] = True
    #             if i == 0: # we can have a continue in the first note if the tie is from the previous bar
    #                 _ties_list[i] = True
    #         elif t == 'stop':
    #             if i == 0: # we can have a stop in the first note if the tie is from the previous bar
    #                 _ties_list[i] = True
    #             else:
    #                 # assert (_ties_list[i] == True) #removed to import wrong scores even if it vould be correct
    #                 _ties_list[i] = True
    #     return _ties_list


    @staticmethod
    def get_type_num(duration: m21.duration.Duration) -> float:
        typeStr: str = duration.type
        if typeStr == 'complex':
            typeStr = m21.duration.quarterLengthToClosestType(duration.quarterLength)[0]
        typeNum: float = m21.duration.convertTypeToNumber(typeStr)
        return typeNum

    @staticmethod
    def get_type_nums(note_list):
        _type_list = []
        for n in note_list:
            _type_list.append(M21Utils.get_type_num(n.duration))
        return _type_list


    @staticmethod
    def get_rest_or_note(note_list):
        _rest_or_note = []
        for n in note_list:
            if n.isRest:
                _rest_or_note.append("R")
            else:
                _rest_or_note.append("N")
        return _rest_or_note


    @staticmethod
    def get_enhance_beamings(note_list):
        """create a mod_beam_list that take into account also the single notes with a type > 4"""
        _beam_list = M21Utils.get_beamings(note_list)
        _type_list = M21Utils.get_type_nums(note_list)
        _mod_beam_list = M21Utils.get_beamings(note_list)
        # add informations for rests and notes not grouped
        for i, n in enumerate(_beam_list):
            if len(n) == 0:
                rangeEnd: int = None
                if _type_list[i] != 0:
                    rangeEnd = int(math.log(_type_list[i] / 4, 2))
                if rangeEnd is None:
                    continue

                for ii in range(0, rangeEnd):
                    if (
                        note_list[i].isRest
                        and len(_beam_list) > i + 1
                        and len(_beam_list[i + 1]) > ii
                        and (
                            _beam_list[i + 1][ii] == "continue"
                            or _beam_list[i + 1][ii] == "stop"
                        )
                    ):  # in case of "beamed" rests, the next note is beamed at the same level):
                        _mod_beam_list[i].append("continue")
                    else:
                        _mod_beam_list[i].append("partial")
        # change the single "start" and "stop" with partial (since MEI parser is not working properly)
        new_mod_beam_list = _mod_beam_list.copy()
        max_beam_len = max([len(t) for t in _mod_beam_list])
        for beam_depth in range(max_beam_len):
            for note_index in range(len(_mod_beam_list)):
                if (
                    M21Utils.safe_get(_mod_beam_list[note_index], beam_depth) == "start"
                    and M21Utils.safe_get(M21Utils.safe_get(_mod_beam_list, note_index + 1), beam_depth)
                    is None
                ):
                    new_mod_beam_list[note_index][beam_depth] = "partial"
                elif (
                    M21Utils.safe_get(_mod_beam_list[note_index], beam_depth) == "stop"
                    and M21Utils.safe_get(M21Utils.safe_get(_mod_beam_list, note_index - 1), beam_depth)
                    is None
                ):
                    new_mod_beam_list[note_index][beam_depth] = "partial"
                elif (
                    M21Utils.safe_get(_mod_beam_list[note_index], beam_depth) == "continue"
                    and M21Utils.safe_get(M21Utils.safe_get(_mod_beam_list, note_index - 1), beam_depth)
                    is None
                    and M21Utils.safe_get(M21Utils.safe_get(_mod_beam_list, note_index + 1), beam_depth)
                    is None
                ):
                    new_mod_beam_list[note_index][beam_depth] = "partial"
                elif (
                    M21Utils.safe_get(_mod_beam_list[note_index], beam_depth) == "continue"
                    and M21Utils.safe_get(M21Utils.safe_get(_mod_beam_list, note_index - 1), beam_depth)
                    is None
                    and M21Utils.safe_get(M21Utils.safe_get(_mod_beam_list, note_index + 1), beam_depth)
                    is not None
                ):
                    new_mod_beam_list[note_index][beam_depth] = "start"

        return new_mod_beam_list


    @staticmethod
    def get_dots(note_list):
        return [n.duration.dots for n in note_list]


    @staticmethod
    def get_durations(note_list):
        return [Fraction(n.duration.quarterLength) for n in note_list]


    @staticmethod
    def get_norm_durations(note_list):
        dur_list = M21Utils.get_durations(note_list)
        if sum(dur_list) == 0:
            raise ValueError("It's not possible to normalize the durations if the sum is 0")
        return [d / sum(dur_list) for d in dur_list]  # normalize the duration


    @staticmethod
    def get_tuplets(note_list):
        return [n.duration.tuplets for n in note_list]


    @staticmethod
    def get_tuplets_info(note_list):
        """create a list with the string that is on the tuplet bracket"""
        str_list = []
        for n in note_list:
            tuple_info_list_for_note = []
            for t in n.duration.tuplets:
                if t.tupletNormalShow in ("number", "both"): # if there is a notation like "2:3"
                    new_info = str(t.numberNotesActual) + ":" + str(t.numberNotesNormal)
                else:  # just a number for the tuplets
                    new_info = str(t.numberNotesActual)
                # if the brackets are drown explicitly, add B
                if t.bracket:
                    new_info = new_info + "B"
                tuple_info_list_for_note.append(new_info)
            str_list.append(tuple_info_list_for_note)
        return str_list


    @staticmethod
    def get_tuplets_type(note_list):
        tuplets_list = [[t.type for t in n.duration.tuplets] for n in note_list]
        new_tuplets_list = tuplets_list.copy()
        # now correct the missing of "start" and add "continue" for clarity
        max_tupl_len = max([len(t) for t in tuplets_list])
        for ii in range(max_tupl_len):
            start_index = None
            # stop_index = None
            for i, note_tuple in enumerate(tuplets_list):
                if len(note_tuple) > ii:
                    if note_tuple[ii] == "start":
                        # Some medieval music has weirdly nested triplets that
                        # end up in music21 with two starts in a row.  This is
                        # OK, no need to assert here.
#                        assert start_index is None
                        start_index = ii
                    elif note_tuple[ii] is None:
                        if start_index is None:
                            start_index = ii
                            new_tuplets_list[i][ii] = "start"
                        else:
                            new_tuplets_list[i][ii] = "continue"
                    elif note_tuple[ii] == "stop":
                        start_index = None
                    else:
                        raise TypeError("Invalid tuplet type")
        return new_tuplets_list


    @staticmethod
    def get_notes(measure, allowGraceNotes=False):
        """
        :param measure: a music21 measure
        :return: a list of (visible) notes, eventually excluding grace notes, inside the measure
        """
        out = []
        if allowGraceNotes:
            for n in measure.getElementsByClass('GeneralNote'):
                if not n.style.hideObjectOnPrint:
                    out.append(n)
        else:
            for n in measure.getElementsByClass('GeneralNote'):
                if not n.style.hideObjectOnPrint and n.duration.quarterLength != 0:
                    out.append(n)
        return out


    @staticmethod
    def get_notes_and_gracenotes(measure):
        """
        :param measure: a music21 measure
        :return: a list of visible notes, including grace notes, inside the measure
        """
        out = []
        for n in measure.getElementsByClass('GeneralNote'):
            if not n.style.hideObjectOnPrint:
                out.append(n)
        return out

    @staticmethod
    def get_extras(measure: m21.stream.Measure, spannerBundle: m21.spanner.SpannerBundle) -> List[m21.base.Music21Object]:
        # returns a list of every object contained in the measure (and in the measure's
        # substreams/Voices), skipping any Streams, GeneralNotes (which are returned from
        # get_notes/get_notes_and_gracenotes), and Barlines.  We're looking for things
        # like Clefs, TextExpressions, and Dynamics...
        output: List[m21.base.Music21Object] = list(measure.recurse().getElementsNotOfClass((m21.note.GeneralNote,
                                                        m21.stream.Stream,
                                                        m21.layout.LayoutBase )))

        # we must add any Crescendo/Diminuendo spanners that start on GeneralNotes in this measure
        for gn in measure.recurse().getElementsByClass(m21.note.GeneralNote):
            dwList: List[m21.dynamics.DynamicWedge] = gn.getSpannerSites(m21.dynamics.DynamicWedge)
            for dw in dwList:
                if dw not in spannerBundle:
                    continue
                if dw.isFirst(gn):
                    output.append(dw)

        return output

    @staticmethod
    def note_to_string(note):
        if note.isRest:
            _str = "R"
        else:
            _str = "N"
        return _str


    @staticmethod
    def safe_get(indexable, idx):
        if indexable is None:
            out = None
        elif 0 <= idx < len(indexable):
            out = indexable[idx]
        else:
            out = None
        return out

    @staticmethod
    def clef_to_string(clef: m21.clef.Clef) -> str:
        # sign(str), line(int), octaveChange(int == # octaves to shift up(+) or down(-))
        sign: str = '' if clef.sign is None else clef.sign
        line: str = '0' if clef.line is None else f'{clef.line}'
        octave: str = '' if clef.octaveChange == 0 else f'{8 * clef.octaveChange:+}'
        return f'CL:{sign}{line}{octave}'

    @staticmethod
    def timesig_to_string(timesig: m21.meter.TimeSignature) -> str:
        if not timesig.symbol:
            return f'TS:{timesig.numerator}/{timesig.denominator}'
        if timesig.symbol in ('common', 'cut'):
            return f'TS:{timesig.symbol}'
        if timesig.symbol == 'single-number':
            return f'TS:{timesig.numerator}'
        return f'TS:{timesig.numerator}/{timesig.denominator}'

    @staticmethod
    def tempo_to_string(mm: m21.tempo.TempoIndication) -> str:
        # pylint: disable=protected-access
        # We need direct access to mm._textExpression and mm._tempoText, to avoid
        # the extra formatting that referencing via the .text propert will perform.
        if isinstance(mm, m21.tempo.TempoText):
            if mm._textExpression is None:
                return 'MM:'
            return f'MM:{M21Utils.extra_to_string(mm._textExpression)}'

        if isinstance(mm, m21.tempo.MetricModulation):
            # convert to MetronomeMark
            mm = mm.newMetronome

        # Assume mm is now a MetronomeMark
        if mm.textImplicit is True or mm._tempoText is None:
            if mm.referent is None or mm.number is None:
                return 'MM:'
            return f'MM:{mm.referent.fullName}={float(mm.number)}'
        if mm.numberImplicit is True or mm.number is None:
            if mm._tempoText is None:
                return 'MM:'
            # no 'MM:' prefix, TempoText adds their own
            return M21Utils.tempo_to_string(mm._tempoText)

        # no 'MM:' prefix, TempoText adds their own
        return f'{M21Utils.tempo_to_string(mm._tempoText)} {mm.referent.fullName}={float(mm.number)}'
        # pylint: enable=protected-access

    @staticmethod
    def barline_to_string(barline: m21.bar.Barline) -> str:
        # for all Barlines: type, pause
        # for Repeat Barlines: direction, times
        pauseStr: str = ''
        if barline.pause is not None:
            if isinstance(barline.pause, m21.expressions.Fermata):
                pauseStr = ' with fermata'
            else:
                pauseStr = ' with pause (non-fermata)'

        output: str = f'{barline.type}{pauseStr}'
        if not isinstance(barline, m21.bar.Repeat):
            return f'BL:{output}'

        # add the Repeat fields (direction, times)
        if barline.direction is not None:
            output += f' direction={barline.direction}'
        if barline.times is not None:
            output += f' times={barline.times}'
        return f'RPT:{output}'

    @staticmethod
    def extra_to_string(extra: m21.base.Music21Object) -> str:
        # object classes that have text content in a single field
        if isinstance(extra, (m21.key.Key, m21.key.KeySignature)):
            return f'KS:{extra.sharps}'
        if isinstance(extra, m21.expressions.TextExpression):
            return f'TX:{extra.content}'
        if isinstance(extra, m21.dynamics.Dynamic):
            return f'DY:{extra.value}'

        # object classes whose text is derived from class name
        if isinstance(extra, m21.dynamics.Diminuendo):
            return 'DY:>'
        if isinstance(extra, m21.dynamics.Crescendo):
            return 'DY:<'

        # object classes that have several fields to be combined into string
        if isinstance(extra, m21.clef.Clef):
            return M21Utils.clef_to_string(extra)
        if isinstance(extra, m21.meter.TimeSignature):
            return M21Utils.timesig_to_string(extra)
        if isinstance(extra, m21.tempo.TempoIndication):
            return M21Utils.tempo_to_string(extra)
        if isinstance(extra, m21.bar.Barline):
            return M21Utils.barline_to_string(extra)

        print(f'Unexpected extra: {extra.classes[0]}', file=sys.stderr)
        return ''
