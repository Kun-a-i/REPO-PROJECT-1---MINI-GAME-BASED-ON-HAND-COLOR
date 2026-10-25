import threading
import cv2
import numpy as np
import pygame

class CameraProcessor:
    def __init__(self, cam_index=1):
        self.cap = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.frame = None
        self.thresh_frame = None
        self.running = True
        self.lock = threading.Lock()
        
        # Start the background worker thread
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def _capture_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            ret, frame = self.cap.read()
            if ret:
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                min_val = np.min(gray)
                max_val = np.max(gray)
                
                lut = np.arange(256, dtype=np.float32)
                if max_val > min_val:
                    lut = np.clip((lut - min_val) / (max_val - min_val) * 255, 0, 255)
                lut = lut.astype(np.uint8)
                
                frame = cv2.LUT(frame, lut)
                base_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                base_frame = base_frame.swapaxes(0,1)
                h, w, _ = frame.shape

                dimension = (int(h/16), int(w/16))
                
                img = frame.astype(np.int16)

                max_vals = np.max(img, axis=2, keepdims=True)

                other_channels = np.where(img == max_vals, 0, img)

                second_max = np.max(other_channels, axis=2, keepdims=True)

                filtered_img = np.where(max_vals > (second_max + 60), frame, 0)

                filtered_frame = filtered_img.astype(np.uint8)

                filtered_frame = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2RGB)
                filtered_frame = filtered_frame.swapaxes(0, 1)
                pixelated_frame  = cv2.resize(filtered_frame, dimension, interpolation=cv2.INTER_NEAREST)
                pixelated_frame  = cv2.resize(pixelated_frame, (h, w), interpolation=cv2.INTER_NEAREST)
                _, thresh_frame = cv2.threshold(pixelated_frame, 100, 255, cv2.THRESH_BINARY)

                thresh_frame = cv2.resize(thresh_frame, (480, 640))
                base_frame = cv2.resize(base_frame, (480, 640))

            with self.lock:
                self.frame = base_frame
                self.thresh_frame = thresh_frame

    def update(self, screen):
        with self.lock:
            if self.frame is not None:
                filtered_surface = pygame.surfarray.make_surface(self.thresh_frame)
                surface = pygame.surfarray.make_surface(self.frame)
                
                filtered_surface.set_colorkey((0, 0, 0))
                screen.blit(surface, (0, 0))
                screen.blit(filtered_surface, (0,0))

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()