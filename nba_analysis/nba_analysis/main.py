from .utils import read_video, save_video
from .trackers import PlayerTracker, BallTracker
from .drawers import ( PlayerTracksDrawer, BallTracksDrawer, TeamBallControlDrawer, PassInterceptionDrawer, CourtKeypointDrawer, TacticalViewDrawer)
from .team_assigner import TeamAssigner
from .ball_acquisition import BallAquisitionDetector
from .interceptions_passes import PassAndInterceptionDetector
from .court_keypoint_detector import CourtKeyPointDector
from .tactical_view_coverter import TacticalViewConverter


def main():
   
    # Read Video

    video_frames = read_video("input_videos/video_3.mp4")

    # Initialize Tracker
    player_tracker = PlayerTracker('nba_analysis/models/player_detector.pt')
    ball_tracker = BallTracker('nba_analysis/models/ball_detector_model.pt')

    #  Initialize Court Keypoint Detector
    court_keypoint_detector = CourtKeyPointDector("nba_analysis/models/court_keypoint_detector.pt")

    # Run Trackers
    player_tracks = player_tracker.get_object_tracks(video_frames,
                                                     read_from_stub=True,
                                                     stub_path="stubs/player_track_stubs.pkl"
                                                     )
    
    ball_tracks = ball_tracker.get_object_tracks(video_frames,
                                                 read_from_stub=True,
                                                 stub_path="stubs/ball_track_stubs.pk1"
                                                )
    
    # Get Court Keypoints
    court_keypoints = court_keypoint_detector.get_court_keypoints(video_frames,
                                                                  read_from_stub=True,
                                                                  stub_path="stubs/court_keypoint_stubs.pk1"
                                                                  )
    
    
    # Remove wrong ball detections
    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)

    #  Interpolate Ball Tracks
    ball_tracks=ball_tracker.interpolate_ball_positions(ball_tracks)
    
    # Assign Player Teams
    team_assigner = TeamAssigner()
    player_assignment = team_assigner.get_player_teams_across_frames(video_frames, 
                                                                player_tracks, 
                                                                read_from_stub=True, 
                                                                stub_path="stubs/player_assignment_stub.pk1")

    # Ball Acquisition
    ball_aquisition_detector = BallAquisitionDetector()
    ball_aquisition = ball_aquisition_detector.detect_ball_possession(player_tracks, ball_tracks)

    # Detect Passes and Interceptions
    pass_and_interception_detector = PassAndInterceptionDetector()
    passes = pass_and_interception_detector.detect_passes(ball_aquisition, player_assignment)
    interceptions = pass_and_interception_detector.detect_interceptions(ball_aquisition, player_assignment)

    # Tactical Vieww
    tactical_view_converter = TacticalViewConverter(court_image_path="./nba_analysis/images/basketball_court.png")
    

    # Draw Output
    # Initialize Drawers
    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    team_ball_control_drawer = TeamBallControlDrawer()
    pass_and_interception_drawer = PassInterceptionDrawer()
    court_keypoint_drawer = CourtKeypointDrawer()
    tactical_view_drawer = TacticalViewDrawer()

    # Draw Object Tracks
    output_video_frames = player_tracks_drawer.draw(video_frames, player_tracks, player_assignment, ball_aquisition)
    output_video_frames = ball_tracks_drawer.draw(output_video_frames, ball_tracks)


    # Draw Team Ball Control
    output_video_frames = team_ball_control_drawer.draw(output_video_frames, player_assignment, ball_aquisition)

    # Draw Passes and Interception
    output_video_frames = pass_and_interception_drawer.draw(output_video_frames, passes, interceptions)

    #  Draw keypoints
    output_video_frames = court_keypoint_drawer.draw(output_video_frames,court_keypoints)

    #  Draw tatical view
    output_video_frames = tactical_view_drawer.draw(output_video_frames, 
                                                       tactical_view_converter.court_image_path, 
                                                       tactical_view_converter.width, 
                                                       tactical_view_converter.height)

    # Save Video    
    save_video(output_video_frames, "output_videos/output_video.avi")

if __name__ == "__main__":
    main()