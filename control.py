import threading
import cv2
import numpy as np
import pygame

class CameraProcessor:
    def __init__(self, cam_index=1):
        self.cap = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.frame = None
        self.thresh_frame = None
        self.running = True
        self.lock = threading.Lock()
        
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def _capture_loop(self):

        base_frame = None
        while self.running:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            
            if ret:
                frame = self.auto_gamma_correction(frame)
                frame = self.lut_stretch(frame)

                base_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                w, h, _ = frame.shape

                dimension = (int(h/16), int(w/16))
                
                
                pixelated_frame  = cv2.resize(frame, dimension, interpolation=cv2.INTER_NEAREST)
                pixelated_frame  = cv2.resize(pixelated_frame, (h, w), interpolation=cv2.INTER_NEAREST)
                _, thresh_frame = cv2.threshold(pixelated_frame, 90, 255, cv2.THRESH_BINARY)

               
                hsv_frame = cv2.cvtColor(pixelated_frame, cv2.COLOR_BGR2HSV)

                # Green Range
                lower_green = np.array([63, 70, 105])   
                upper_green = np.array([85, 130, 185]) 

                green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

                # Blue Range
                lower_blue = np.array([90, 140, 180])
                upper_blue = np.array([112, 255, 255])
                blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

                

                lower_red2 = np.array([160, 60, 190])
                upper_red2 = np.array([179, 255, 255])

                # Combine both ranges using bitwise_or
                red_mask = cv2.inRange(hsv_frame, lower_red2, upper_red2)
                
                # 3. Find contours directly on these pristine single-channel masks
                tracked_colors = [
                    (red_mask, (255, 0, 0)),    
                    (green_mask, (0, 255, 0)),  
                    (blue_mask, (0, 0, 255))   
                ]

                base_frame = np.ascontiguousarray(base_frame)
                
                pixelated_frame = cv2.cvtColor(pixelated_frame, cv2.COLOR_BGR2RGB)
                for mask, draw_color in tracked_colors:
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    for cnt in contours:
                        if cv2.contourArea(cnt) > 3000: 
                            M = cv2.moments(cnt)
                            if M["m00"] != 0:
                                cX = int(M["m10"] / M["m00"])
                                cY = int(M["m01"] / M["m00"])
                                cv2.circle(base_frame, (cX, cY), radius=6, color=draw_color, thickness=-1)
                                cv2.circle(pixelated_frame, (cX, cY), radius=6, color=draw_color, thickness=-1)
            
            pixelated_frame = pixelated_frame.swapaxes(0,1)
            base_frame = base_frame.swapaxes(0,1)
            with self.lock:
                if base_frame is not None:
                    self.frame = base_frame
                    self.thresh_frame = pixelated_frame

    def update(self, screen):
        with self.lock:
            if self.frame is not None:
                filtered_surface = pygame.surfarray.make_surface(self.thresh_frame)
                surface = pygame.surfarray.make_surface(self.frame)
                
                filtered_surface.set_colorkey((0, 0, 0))
                screen.blit(surface, (0, 0))
                # screen.blit(filtered_surface, (0,0))

    def auto_gamma_correction(self, frame, target_gamma=0.4):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        
        if mean_brightness < 1:
            mean_brightness = 1.0

        gamma = np.log(mean_brightness / 255.0) / np.log(target_gamma)
        
        
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 
                        for i in np.arange(0, 256)]).astype("uint8")
        
        return cv2.LUT(frame, table)

    def lut_stretch(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        min_val = np.min(gray)
        max_val = np.max(gray)
                
        lut = np.arange(256, dtype=np.float32)
        if max_val > min_val:
            lut = np.clip((lut - min_val) / (max_val - min_val) * 255, 0, 255)
        lut = lut.astype(np.uint8)

        return cv2.LUT(frame, lut)

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()