import sys
sys.path.append("../")
from utils import measure_distance


class BallAquisitionDetector:
    def __init__(self):
        self.possession_threshold = 50
        self.min_frames = 11
        self.containment_threshold = 0.8
    
    def get_key_basketball_player_assignment_points(self, player_bbox, ball_center ):
        ball_center_x = ball_center[0]
        ball_center_y = ball_center[1]

        x1,y1,x2,y2 = player_bbox
        width = x2-x1
        height = y2-y1

        output_points = []
        if ball_center_y > y1 and ball_center_y < y2:
            output_points.append(x1, ball_center_y)
            output_points.append(x2, ball_center_y)

        if ball_center_x > x1 and ball_center_x < x2:
            output_points.append(ball_center_y, y1)
            output_points.append(ball_center_y, y2)


        output_points += [
             (x1,y1), #Top Left Corner
             (x2,y2), #Top Right Corner
             (x1,y1), #Bottom Left Corner
             (x2,y2), #Bottom Right Corner
             (x1+width//2,y1), #Top Center
             (x1+width//2,y2), #Bottom Center
             (x1, y1+height//2), #Left Center
             (x2, y1+height//2), #Right Center
        ]


        return output_points

    def find_minimum_distance_to_ball(self, ball_center, player_bbox):
        key_points = self.get_key_basketball_player_assignment_points(player_bbox, ball_center)

        return min(measure_distance(ball_center,key_points) for key_point in key_points)
    
    def calculate_ball_containment_ratio(self, player_bbox, ball_bbox):
        px1, py1, px2, py2 = player_bbox
        bx1, by1, bx2, by2 = ball_bbox

        ball_area = (bx2 - bx1) * (by2-by1)

        player_area = (px2 - px1) * (py2-py1)

        intersection_x1 = max(px1, bx1)
        intersection_y1 = max(py1, bx1)
        intersection_x2 = min(px2, bx2)
        intersection_y2 = min(py2, by2)

        intersection_area = (intersection_x2 - intersection_x1) * (intersection_y2 - intersection_y1)

        containment_ratio = intersection_area/ball_area

        return containment_ratio
    

    def find_best_candidate_for_possession(self, ball_center, player_tracks_frame, ball_bbox):

        high_containment_players = []
        regular_distance_players =[]

        for player_id,player_info in player_tracks_frame.items():
            pass