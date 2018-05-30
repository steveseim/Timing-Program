import sys
from PyQt5 import QtWidgets
from guiv4 import Ui_MainWindow
from timing_calc import video_timing


class timingProgram(QtWidgets.QMainWindow):
    def __init__(self):
        super(timingProgram, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.goButton.clicked.connect(self.calculate)

        self.ui.helpButton.clicked.connect(self.help)

        self.ui.traditional_radio.setChecked(True)

        # Default information is empty:
        self.message = ""
        self.ui.additional_info.setText(self.message)

    def help(self):

        help_message = ("To make a custom video that fits our existing music: \n\n"
                        " - Select the relevant length and style on the left for a starting point. \n\n"
                        " - Click 'Calculate'. The right side will fill in correct details.  \n\n"
                        " - Select 'Custom' as your style option \n\n"
                        " - Change what you need under the custom options \n\n"
                        " - Leave 'intro sil' checked. This will ensure video starts and ends with music \n\n"
                        " - Click 'Calculate' again to get the correct frames. \n\n")

        QtWidgets.QMessageBox.about(self, "Help", help_message)

    def calculate(self):

        '''
        The main function that happens when the single button is pushed.
        It gathers all the inputs and calculates the frames output.
        '''

        style_options = {"traditional": 90, "contemporary": 30}

        self.message = ""

        # If custom is selected, run with these parameters:

        if self.ui.custom_radio.isChecked():
            length_minutes = self.ui.minutes_input.value()
            length_seconds = self.ui.seconds_input.value()
            scenery_clips = str(self.ui.scenery_clips_input.value())
            if 1 < int(scenery_clips) < 10:
                pass
            else:
                QtWidgets.QMessageBox.about(self, "Error", "Scenery clips must be between 2 and 9")
                return
            style = "custom"
            if self.ui.intro_sil_check.isChecked():
                intro_sil = "yes"
            else:
                intro_sil = "no"
                self.message += "--Cut 12 seconds from beginning of music, and 4 seconds from beginning of first scenery.\n"
            transition_length = self.ui.transition_length_input.value()
            self.message += "--Assumes NOT extending second/last transitions\n"

        # Otherwise, run with these parameters:

        # The Standard Style radio buttons:
        else:
            if self.ui.traditional_radio.isChecked():
                style = "traditional"
                intro_sil = "yes"
                self.ui.intro_sil_check.setChecked(True)
                transition_length = style_options[style]
                self.ui.transition_length_input.setValue(90)
                self.message += "--Default Transition: 90 frames|Cross Dissolve \n--Assumes extending second and last transitions\n"
            elif self.ui.contemporary_radio.isChecked():
                style = "contemporary"
                self.ui.intro_sil_check.setChecked(True)
                intro_sil = "yes"
                transition_length = style_options[style]
                self.ui.transition_length_input.setValue(30)
                self.message += "--Default Transition: 30 frames|Dip to White\n" \
                                "--Cut 12 seconds from beginning of music, and 4 seconds from beginning of first scenery.\n"
                if self.ui.six_with_radio.isChecked() or self.ui.nine_with_radio.isChecked():
                    self.message = "{}".format("**Contemporary Style is normally All Photo**\n\n" + self.message)


            else:
                QtWidgets.QMessageBox.about(self, "Error", "Please select a style option")
                return

            # The Production Type radio buttons:
            if self.ui.six_with_radio.isChecked():
                length_minutes = 6
                length_seconds = 8
                self.ui.minutes_input.setValue(6)
                self.ui.seconds_input.setValue(8)
                self.ui.scenery_clips_input.setValue(9)
                scenery_clips = "9"

            elif self.ui.six_without_radio.isChecked():
                length_minutes = 6
                length_seconds = 8
                self.ui.minutes_input.setValue(6)
                self.ui.seconds_input.setValue(8)
                self.ui.scenery_clips_input.setValue(2)
                scenery_clips = "2"

            elif self.ui.nine_with_radio.isChecked():
                length_minutes = 9
                length_seconds = 0
                self.ui.minutes_input.setValue(9)
                self.ui.seconds_input.setValue(0)
                self.ui.scenery_clips_input.setValue(9)
                scenery_clips = "9"

            elif self.ui.nine_without_radio.isChecked():
                length_minutes = 9
                length_seconds = 0
                self.ui.minutes_input.setValue(9)
                self.ui.seconds_input.setValue(0)
                self.ui.scenery_clips_input.setValue(2)
                scenery_clips = "2"
            else:
                QtWidgets.QMessageBox.about(self, "Error", "Please select a Production Type")
                return

        # The inputted number of moves:
        number_of_moves = self.ui.moves_input.value()

        if number_of_moves > 0:
            answer = video_timing(number_of_moves, length_minutes, length_seconds, scenery_clips, intro_sil, style,
                                  transition_length)
            self.ui.frames_output.setText(str(answer))
        else:
            QtWidgets.QMessageBox.about(self, "Error", "Please enter the correct number of photos")
            return

        photos_in_seconds = (answer / 30) - (transition_length / 30)

        # existing text is 32 pixels/characters long
        self.message += "\n{:^110}".format("Photos on screen for " + str(round(photos_in_seconds, 1)) + " seconds")

        # Display the 'message' variable in the window at the bottom.
        self.ui.additional_info.setText(self.message)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("windowsvista")
    timing_program = timingProgram()
    timing_program.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
