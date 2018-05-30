def video_timing (number_of_moves, length_minutes,
                    length_seconds, scenery_clips,
                    intro_sil, style,
                    transition_length):
    '''
    number_of_moves is an integer, the number of photos you're putting into video.
    length_minutes is integer
    lengh_minutes is integer
    scenery_clips is integer, between 2 and 9
    intro_sil is "yes" or "no", defaulted to "yes" if nothing entered
    style is "Traditional", "Contemporary", or "Custom"
    transition_length is integer: the total length in frames of transition between photos.
    
    Default Lengths of videos:
    Six minute: 6 minutes 8 seconds
    Nine minute: 9 minutes 0 seconds
    '''
    
    scenery_length = {   #Dictionary of how many frames of the video is taken up by the scenery used. Key is number of scenery clips//value is total frames
                    "0": 0,
                    "2": 3600,
                    "3": 3840,
                    "4": 4080,
                    "5": 4320,
                    "6": 4560,
                    "7": 4800,
                    "8": 5040,
                    "9": 5280
                    }
					
    style_options = {"traditional": 90, "contemporary": 30}

    if style == "custom":
        pass
    else:
        transition_length = style_options[style]
	
    # calculate the total frames in the video based on minutes and seconds:
    total_frames = (int(length_minutes) * 60 * 30) + (int(length_seconds) * 30)
    
    # Find the frames that the scenery will take up:
    total_scenery_length = scenery_length[scenery_clips]
    
    # divide the leftover frames by the number of photos being used.
    # add ninety frames to cover the transitions on either end of each photo.
    frames_per_photo = (total_frames - total_scenery_length)/number_of_moves + transition_length
        
    # if no intro sil, calculate the extra time taken up by the photos (12 seconds x 30 frames = 360).
    # Also, assumes cutting 4 seconds off the beginning of the scenery.
    if intro_sil == "no":
        frames_per_photo += (360/number_of_moves)

    # If contemporary style, we don't increase the length of first/last transitions.
    # Difference (120 frames = 4 seconds) is calculated here:
    if style == "contemporary" or style == "custom":
        frames_per_photo -= (120/number_of_moves)
    
    return round(frames_per_photo)
        
if __name__ == "__main__" :
    #The code below this is for testing the function before implementing in PyQt5 GUI
    print (video_timing(16, 6, 8, "9", "yes", "traditional", 0))
