from PIL import Image
import cv2
import tempfile

def validate_cheque(image):
    """Validate if uploaded image is a valid cheque"""
    width, height = image.size
    # Simple validation - real cheque should have certain dimensions
    MIN_CHEQUE_WIDTH = 300
    MIN_CHEQUE_HEIGHT = 150
    return width > MIN_CHEQUE_WIDTH and height > MIN_CHEQUE_HEIGHT

def mask_account_number(account_number):
    """Mask all digits except last 4"""
    if not account_number or len(account_number) < 4:
        return account_number
    return "*" * (len(account_number) - 4) + account_number[-4:]

def record_kyc_video():
    """Record a short video using webcam"""
    VIDEO_DURATION = 5  # seconds
    VIDEO_FPS = 20
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        return None, "Cannot access camera"
    
    # Setup video writer
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    video_filename = temp_file.name
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        video_filename, 
        fourcc, 
        VIDEO_FPS, 
        (640, 480)
    )
    
    # Record for specified duration
    max_frames = VIDEO_DURATION * VIDEO_FPS
    
    for _ in range(max_frames):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break
    
    # Cleanup
    cap.release()
    out.release()
    
    return video_filename, "Video recorded successfully"