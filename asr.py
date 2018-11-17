# The goal is to read a audio file ->  Create Frames
# Frame length = 25ms
# Frame Step   = 10 ms (15ms overlap)
import numpy as np 
import scipy.io.wavfile as wav
import math

# Read in the audio file
rate, data = wav.read('test.wav')

# find out how many frames we will need 
frame_duration = 0.025
overlap_duration = 0.015
frame_sample_len = math.ceil(frame_duration * rate)
overlap = math.ceil(overlap_duration * rate)
total_samples = len(data)

# calculate number of frames 
n_frame = math.ceil((total_samples - overlap)/(frame_sample_len - overlap))
# calculate padding required 
pad_len  = (n_frame *frame_sample_len) - ((n_frame -1)* overlap) - total_samples;


print('frame_sample_len ', frame_sample_len)
print('n_frame ', n_frame)

# pad the data 
data  = np.concatenate([data , np.zeros((pad_len,))]);


# Frame into 2D numpy array
# ith row represent ith frame
# jth col represents jth sample in frames

frame_matrix = np.zeros(shape=(n_frame, frame_sample_len),dtype=int)

i = 0
for x in range(0, n_frame):
    for y in range(0, frame_sample_len):
    	frame_matrix[x,y] = data[i]
    	i = i+1
    i = i - overlap

print(frame_matrix)

# Apply hamming window function on each frame
for i in range(0, n_frame):
	frame_matrix[i,:] = np.multiply(frame_matrix[i,:], np.hamming(frame_sample_len));


# Take dft of each frame

dft_frame_matrix = np.zeros(shape=(n_frame, 257),dtype=complex)
for i in range(0, n_frame):
	dft_frame_matrix[i,:] = np.fft.rfft(frame_matrix[i,:], 512)

print(dft_frame_matrix);


