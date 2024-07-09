import cv2  #ComputerVision Library
import sys  #To use argv
import os   #To allow writing of pictures
from tqdm import tqdm  #To show the progress bar


def save_frame(frame, timestamp, output_dir):
    """
    Save a picture with the filename 'HH-MM-SS.jpg' in chosen directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = f"{timestamp}.jpg"
    filepath = os.path.join(output_dir, filename)
    cv2.imwrite(filepath, frame)


def detect_motion(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)  #Load the video
    
    #Now let's get infos about the video frame
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  #Total number of frames
    fps = cap.get(cv2.CAP_PROP_FPS)  #Video speed in FPS
    frame_skip = int(fps / 2)  #Number of frames to skip (half a second). We will skip frames to speed up the process

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  #Get video width
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  #Get video height
    
    #Calculate the mask region we are going to exclude (in my case, it's where the timestamp is printed on screen, and it's 1/3rd of width and 1/10th of height)
    exclude_width = width // 3
    exclude_height = height // 10
    exclude_region = (exclude_width, exclude_height)
    
    #Calculate the checking area (1/400th of total framesize)
    min_contour_area = (width * height) // 400
    
    ret, frame1 = cap.read()  #Read the first frame
    frame_count = 1  #Let's start a frame counter
    
    #Start the progress bar, too
    with tqdm(total=total_frames // frame_skip) as pbar:
        while cap.isOpened():
            #Skip the frames to only check every half a second
            for _ in range(frame_skip - 1):
                cap.grab()  #Ignore the frame
            ret, frame2 = cap.read()  #Read current frame
            
            if not ret:
                break  #End the cycle

            #Calculate the difference between two frames
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  #Get the greyscale version of the frame
            blur = cv2.GaussianBlur(gray, (5, 5), 0)  #Apply a Gaussian Blur to reduce noise
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  #Apply a binary threshold
            dilated = cv2.dilate(thresh, None, iterations=3)  #Fit the image
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  #Find contours

            for contour in contours:
                if cv2.contourArea(contour) < min_contour_area:
                    continue  #Ignore contours if too small

                #Get the bounding box
                (x, y, w, h) = cv2.boundingRect(contour)
                
                #Check if movement happened whitin the inclusion region
                if (x + w) > exclude_region[0] and (y + h) > exclude_region[1]:
                    continue  #Ignore if box falls within the excluding region

                #Calculate  current timestamp
                milliseconds = cap.get(cv2.CAP_PROP_POS_MSEC)
                seconds = milliseconds // 1000
                minutes = seconds // 60
                hours = minutes // 60
                timestamp = f"{int(hours)}:{int(minutes % 60)}:{int(seconds % 60)}"
                
                print(f"Found movement at: {timestamp}")
                save_frame(frame2, timestamp, output_dir)

                break  #If found, exit the loop

            frame1 = frame2  #Update the current frame
            frame_count += frame_skip  #Update frame counter
            
            #Update the progress bar
            pbar.update(1)

    cap.release()  #Close the video once everything is done

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python detect_motion.py <video_path> <output_dir>")
        sys.exit(1)  #Exit if no video path or no output directory

    video_path = sys.argv[1]  #Get video path as the first argument
    output_dir = sys.argv[2]  #Get output directory as second argument
    detect_motion(video_path, output_dir)  #Detect motion!
