import pygame
import time
import random
import cv2
import math
import numpy as np
import threading
import queue

pygame.init()
mutex = threading.Lock()
message_queue = queue.Queue()
WIDTH,HEIGHT=1000,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Bomb Dodge")

BG=pygame.transform.scale(pygame.image.load("/Users/mauryadarsh07gmail.com/Downloads/DeepLearning/Vision&Shooting game/download.jpeg"),(WIDTH,HEIGHT))
GRAVITY=9.8
BOMB_WIDTH=40
BOMB_HEIGHT=40
BOMB_START=50
BOMB_RADIUS=20
OBS_INIT=600
SCORE=0

def draw(bomb,velocity,angle,obs):
    # try:
    #     result = result_queue.get()
    #     print(f"Received result from thread: {result}")
    # except queue.Empty:
    #     result=score
    # score=result
    WIN.blit(BG,(0,0))
    font = pygame.font.Font(None, 32)  
    text_color = (255, 255, 255)  
    velocity_text = f"velocity: {velocity:.1f}              angle:{angle:.1f}               score:{SCORE} "  # Format with one decimal place
    velocity_text_surface = font.render(velocity_text, True, text_color)
    
    WIN.blit(velocity_text_surface, (10, 10))
    pygame.draw.rect(WIN,"green",(obs.x,HEIGHT-60,BOMB_WIDTH+10,BOMB_HEIGHT+10))
    pygame.draw.rect(WIN,"blue",(BOMB_START,HEIGHT-60,BOMB_WIDTH,BOMB_HEIGHT))
    pygame.draw.circle(WIN,"red",(bomb.x+BOMB_RADIUS,bomb.y+BOMB_RADIUS),BOMB_RADIUS)
    line_length = int(velocity)  # Adjust factor for line length based on velocity
    end_x = int(BOMB_START+ BOMB_WIDTH // 2 + line_length * math.cos(math.radians(angle)))
    end_y = int(HEIGHT-60 + BOMB_HEIGHT // 2 - line_length * math.sin(math.radians(angle)))

    pygame.draw.line(WIN, (0, 255, 0), (BOMB_START+ BOMB_WIDTH // 2, HEIGHT-60+ BOMB_HEIGHT // 2), (end_x, end_y), 2)
    
    pygame.display.update()
    

def draw_projectile(bomb,obs):
    pygame.draw.circle(WIN,"red",(bomb.x+BOMB_RADIUS,bomb.y+BOMB_RADIUS),BOMB_RADIUS)
    
    pygame.draw.rect(WIN,"green",(obs.x,HEIGHT-60,BOMB_WIDTH+10,BOMB_HEIGHT+10))
    
    pygame.display.update()
    
result_queue = queue.Queue()

def fire(vx,vy,bomb,obs):
    
    clock1=pygame.time.Clock()
    ty=0
    tx=0
    f=0
    # bomb.x=BOMB_START
    while(bomb.y<=HEIGHT-60):
                clock1.tick(60)
                ty+=0.1
                tx+=0.1
                if(BOMB_START+ vx*tx>WIDTH):
                    vx=-vx
                    tx=0
                    f=1

                if(WIDTH+ vx*tx<0):
                    vx=-vx
                    tx=0
                    f=0
                if(f==0):
                    bomb.x= BOMB_START+ vx*tx
                else:
                    bomb.x= WIDTH+ vx*tx

                bomb.y=HEIGHT-60-( vy * ty - 0.5 * GRAVITY * ty**2)

                # collision
                if(abs(bomb.x-obs.x)<BOMB_WIDTH+10 and abs(bomb.y-obs.y)<BOMB_HEIGHT+10 and abs(bomb.y-obs.y)>=BOMB_HEIGHT):
                    global SCORE
                    SCORE+=1
                    # print(s)
                    obs.x=np.random.randint(600,900)
                    bomb.y=HEIGHT+100
                    break
                elif(abs(bomb.x-obs.x)<BOMB_WIDTH+10 and abs(bomb.y-obs.y)<BOMB_HEIGHT):
                    print(abs(bomb.y-obs.y))
                    bomb.y=HEIGHT+100
                    break
                
               
                
                message_queue.put([1,bomb,obs])
                
                
                


def ui_thread():
  """Simulates the UI thread"""
  while True:

    # Get data (if any) from the queue without blocking
    try:
        message = message_queue.get(timeout=0.1)  # Set a timeout to avoid blocking
    except queue.Empty:
        continue
    #   # No message in the queue, continue the loop
    #   continue
    if message == "quit":
      break
    # Update display element based on data
    
    if(message[0]==1):
        draw_projectile(message[1],message[2])
    if(message[0]==2):
        draw(message[3],message[1],message[2],message[4])
             
    
thread_ui=threading.Thread(target=ui_thread,args=())

def main():
    run=True
    cap = cv2.VideoCapture(0)
    bomb=pygame.Rect(BOMB_START,HEIGHT-60,BOMB_WIDTH,BOMB_HEIGHT)
    obst=pygame.Rect(OBS_INIT,HEIGHT-60,BOMB_WIDTH+10,BOMB_HEIGHT+10)

    clock=pygame.time.Clock()
    score=0
    start_time=time.time()
    elapsed_time=0
    f=True
    k=0
    space_pressed=False
    thread_ui.start()
    
    start_time1=0
    speed=10
    while run:
        clock.tick(10)
        k+=1
        elapsed_time=(time.time()-start_time)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                message_queue.put("quit")
                break

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        framel=frame[:,:,:frame.shape[2]//2]
        framer=frame[:,:,frame.shape[2]//2:]
        # Convert frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range of green color in HSV
        lower_green = np.array([40, 100, 100])
        upper_green = np.array([80, 255, 255])

        # Threshold the HSV image to get only green colors
        mask = cv2.inRange(hsv, lower_green, upper_green)
        framel=mask[:,:mask.shape[1]//2]
        framer=mask[:,mask.shape[1]//2:]
        # print(mask[mask==255].size)
        # break
        # Find contours of the green object
        contours, _ = cv2.findContours(framel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw a green rectangle around the largest contour
        if contours:
            # Find the largest contour by area
            max_contour = max(contours, key=cv2.contourArea)
            # Fit a line to the contour points
            vx, vy, x, y = cv2.fitLine(max_contour, cv2.DIST_L2, 0, 0.01, 0.01)
            if vx == 0:
                vx = 1
            if vy == 0:
                vy = 1
            # Calculate starting and ending points for the line to be drawn
            lefty = int((-x * vy / vx) + y)
            righty = int(((frame.shape[1] - x) * vy / vx) + y)
        
            # Draw the line on the frame
            cv2.line(frame, (frame.shape[1]-1, int(righty)), (0, int(lefty)), (0, 0, 255), 2)
            # conversion_factor = 180 // math.pi
            angle=np.arctan(-(righty-lefty)/(frame.shape[1]-1))
            velocity=framel[framel==255].size/50
            vx = math.cos(angle ) * velocity
            vy = math.sin(angle ) * velocity
    
            # time, x, y = projectile_motion(angle, velocity)
            # print(angle,velocity)
        
        # Display the processed frame n
            cv2.imshow('Processed Frame', mask)
            
            # print (k)
            # keys=pygame.key.get_pressed()
            if(framer[framer==255].size>5000 ):
            
                elapsed_time1=(time.time()-start_time1)
                thread_fire=threading.Thread(target=fire,args=(vx,vy,bomb,obst))
                if (f) :
                   
                    thread_fire.start()
                    start_time1=time.time()
                    f=False

            
            

            if(bomb.y>HEIGHT-60):
               
               bomb.x=BOMB_START
               bomb.y=HEIGHT-60
               f=True
            
            obst.x+=speed
            if(obst.x>900 or obst.x<600): speed=-speed
            message_queue.put([2,velocity,angle*180/math.pi,bomb,obst])
            
            
        
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
           break

    pygame.quit()

if __name__ == "__main__":
    main()