from copy import deepcopy
import sys
sys.path.append('../')
from utils import measure_distance

class TacticalViewConverter:
    def __init__(self, court_image_path):
        self.court_image_path = court_image_path
        self.width = 300
        self.height = 161

        self.actual_width_in_meters = 28
        self.actual_height_in_meters = 15

        
        
        self.key_points = [
            # left edge
            (0,0),
            (0,int((0.91/self.actual_height_in_meters)*self.height)),
            (0,int((5.18/self.actual_height_in_meters)*self.height)),
            (0,int((10/self.actual_height_in_meters)*self.height)),
            (0,int((14.1/self.actual_height_in_meters)*self.height)),
            (0,int(self.height)),

            # Middle line
            (int(self.width/2),self.height),
            (int(self.width/2),0),
            
            # Left Free throw line
            (int((5.79/self.actual_width_in_meters)*self.width),int((5.18/self.actual_height_in_meters)*self.height)),
            (int((5.79/self.actual_width_in_meters)*self.width),int((10/self.actual_height_in_meters)*self.height)),

            # right edge
            (self.width,int(self.height)),
            (self.width,int((14.1/self.actual_height_in_meters)*self.height)),
            (self.width,int((10/self.actual_height_in_meters)*self.height)),
            (self.width,int((5.18/self.actual_height_in_meters)*self.height)),
            (self.width,int((0.91/self.actual_height_in_meters)*self.height)),
            (self.width,0),

            # Right Free throw line
            (int(((self.actual_width_in_meters-5.79)/self.actual_width_in_meters)*self.width),int((5.18/self.actual_height_in_meters)*self.height)),
            (int(((self.actual_width_in_meters-5.79)/self.actual_width_in_meters)*self.width),int((10/self.actual_height_in_meters)*self.height)),
        ]

def validate(self, keypoints_list):

    keypoints_list = deepcopy(keypoints_list)
    for frame_idx, frame_keypoints in enumerate(keypoints_list):
        frame_keypoints = frame_keypoints.xy.tolist()[0]

        detected_indicies = [i for i, kp in enumerate(frame_keypoints) if kp[0]>0 and kp[1]>0]

        if len(detected_indicies) < 3:
            continue

        invalid_keypoints = []

        for i in detected_indicies:
            # Skip keypoints (0,0)
            if frame_keypoints[i][0] == 0 and frame_keypoints[i][1] == 0:
                continue

            other_indicies = [idx for idx in detected_indicies if idx != i and idx  not in invalid_keypoints]
            if len(other_indicies) < 2:
                continue

            j,k = other_indicies[0],other_indicies[1]

            d_ij = measure_distance(frame_keypoints[i], frame_keypoints[j])
            d_ij = measure_distance(frame_keypoints[i], frame_keypoints[k])
            
            t_ij = measure_distance(self.key_points[i], self.key_point[j])
            t_ij = measure_distance(self.key_point[i], self.key_point[j])

    return keypoints_list