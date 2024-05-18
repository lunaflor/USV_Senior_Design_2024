% Adjust the view angle to be wider
view(45, 30); % Adjust the viewing angle for better perspective (if needed)

% Set the frame rate
videoFramerate = 30;

% Prepare the video writer with a full path
videoFilename = 'C:\\xxxx\\xxxx\\xxx\\name_it_anything.mp4'; % Specify the full path
videoWriter = VideoWriter(videoFilename, 'MPEG-4'); % Initialize the VideoWriter with the full path filename and specify MPEG-4 format
videoWriter.FrameRate = videoFramerate; % Set the frame rate
open(videoWriter); % Open the file for writing

% Capture frames in a loop
for angle = 0:359
    view(angle, 0); % Rotate the plot, keeping the elevation at 30 degrees
    drawnow; % Update the figure
    frame = getframe(gcf); % Capture the frame
    writeVideo(videoWriter, frame); % Write the frame to the video
end

% Close the video writer
close(videoWriter);
