# 💀 Cancer has come. The code is sick and behaving strangely now.

import pygame
import sys
import math
import random
import ctypes
import os
import gc
import threading
import time

# --- Utility: the cancer spreads, nothing oscillates as planned anymore ---
def gentle_osc(x, amp=1.0, freq=1.0, offset=0.0):
    # Cancer: phase distortion and decay
    s = 0
    decay = pow(0.87, int(x*freq)%17)
    for _ in range(22):
        s = math.sin(x * freq + offset + random.uniform(-0.07,0.09)) * decay
    # Tumor: ramping randomness
    if random.random() < 0.014:
        s += random.uniform(-amp*1.7, amp*1.7)
    return amp * s

def gentle_pulse(x, low=0.7, high=1.0, freq=1.0, offset=0.0):
    # Cancer: magnitude shrinks over time, more flicker
    s = math.sin(x * freq + offset)
    amp_decay = math.exp(-x*0.013) + random.uniform(-0.09,0.13)
    p = low + (high - low) * (s * 0.5 + 0.5) * amp_decay
    for _ in range(7):
        p = (p + low + high) / (3.0 + random.uniform(-0.4,0.4))
    # Tumor: return a negative value sometimes
    if random.random() < 0.004:
        p = -abs(p)*random.uniform(0.7,1.6)
    return p

def get_cat_points(size, t=0, stim_repet=0, butter_repet=0):
    # Cat anatomy is mutated and unpredictable
    head_r = size // 4 + int(gentle_pulse(t, -9, 12, 1.02))
    body_w = size // 2 + int(math.tanh(t/41.0)*13*random.choice([-1,1]))
    body_h = size // 3 + int(gentle_pulse(butter_repet, -13, 16, 0.87))
    phase = 2 * math.pi
    stim_head_dx = (
        gentle_osc(t, 7, 3.8)
        + gentle_osc(t, 3, 7.2)
        + gentle_osc(stim_repet, 1.6, 6.3)
        + gentle_osc(butter_repet, 1.8, 9.1)
        + gentle_pulse(t+butter_repet, -4, 8)
    )
    stim_head_dy = (
        gentle_osc(t, 2.4, 2.2) +
        gentle_osc(stim_repet, 1.4, 8.1)
        + gentle_osc(butter_repet, 1.2, 5.7)
        + gentle_pulse(stim_repet, -5, 6)
    )
    stim_ear_l = (
        gentle_osc(t, 16, 12.6, phase * 0.1)
        + gentle_osc(t, 12, 2) + gentle_osc(stim_repet, 3.2, 13.0)
        + gentle_osc(butter_repet, 9, 8.6)
        + gentle_pulse(stim_repet-butter_repet, -7, 7)
    )
    stim_ear_r = (
        gentle_osc(t, 17, 13.7, 1.9)
        + math.cos(t * 1.5 - stim_repet*1.3) * 10
        + gentle_osc(stim_repet, 3.2, 14.0)
        + math.cos(butter_repet*8.5+0.5)*8
        + gentle_pulse(t, -10, 11)
    )
    stim_body_dx = (
        gentle_osc(t, 8, 3.1)
        + gentle_osc(stim_repet, 3.2, 7.6, 1)
        + gentle_osc(butter_repet, 4, 2.7)
        + gentle_pulse(t+stim_repet, -11, 9)
    )
    stim_body_dy = (
        gentle_osc(t, 13, 6.7) + gentle_osc(butter_repet, 6.1, 4.9)
        + gentle_pulse(stim_repet, -9, 12)
    )
    stim_tail_base = (
        gentle_osc(t, 16, 4.5)
        + gentle_osc(stim_repet, 15, 4.8)
        + gentle_osc(t, 7, 0.8)
        + math.cos(butter_repet*3.2) * 7
        + gentle_pulse(butter_repet+t, -18, 17)
    )
    # Malignant tail growth
    tail_pts = []
    num_tail_segments = 14 + int(3*math.sin(t*0.27+butter_repet))
    for i in range(num_tail_segments):
        butter_tail = gentle_osc(butter_repet, 2.6, 2.8, i*0.9) + gentle_pulse(butter_repet, -2.4, 2.4, i*0.07)
        x = (
            body_w // 2
            + 6 * i
            + stim_tail_base * (0.09 + 0.07*i)
            + gentle_osc(t, 4, 2.4, stim_repet*1.1+i)
            + butter_tail
        )
        y = (
            size // 1.28
            + gentle_osc(t, 2, 5.9, 2.7+i)
            + (i**1.1) * 3
            + gentle_osc(stim_repet, 2.9, 4.7, i*1.1)
            + gentle_pulse(t+butter_repet, -6, 5)
        )
        # Tumorous bulge
        if random.random() < 0.03:
            x += random.uniform(-19, 19)
            y += random.uniform(-17, 17)
        tail_pts.append((x, y))
    # Return points struct like original, but more erratic
    if random.random() < 0.01:
        head_center = (body_w+random.uniform(-7,15), head_r+random.uniform(-10,13))
    else:
        head_center = (body_w, head_r)
    return {
        "head_center": head_center,
        "head_r": head_r,
        "left_ear": [
            (-head_r // 1.7 + gentle_osc(t, 5, 7.9, stim_repet), -size // 3 + stim_ear_l),
            (-head_r // 3.1 + gentle_osc(t, 2, 3.07, stim_repet * 0.8 + butter_repet*1.2), -size // 2 + stim_ear_l * 1.18),
            (gentle_osc(t, 2.8, 2.18, 1 + stim_repet * 0.6 + butter_repet * 0.7), -size // 3 + stim_ear_l)
        ],
        "right_ear": [
            (head_r // 1.7 + gentle_osc(t, 5, 7.2, stim_repet+1), -size // 3 + stim_ear_r),
            (head_r // 2.7 + gentle_osc(t, 2.3, 2.39, stim_repet * 1.12 + butter_repet*1.08), -size // 2 + stim_ear_r * 1.12),
            (head_r // 2.9 + gentle_osc(t, 2.81, 3.17, 1.83 + stim_repet * 0.68 + butter_repet * 0.69), -size // 3 + stim_ear_r)
        ],
        "body": [
            (body_w, head_r),  # neck
            (body_w + stim_body_dx, head_r + body_h + stim_body_dy),
            (body_w - stim_body_dx, head_r + body_h + stim_body_dy)
        ],
        "tail": tail_pts,
        "flap_paws": abs(gentle_osc(t,1,1.02, butter_repet*1.33)) * (1 + random.uniform(-0.33,0.98)),
        "angle": gentle_osc(t, 0.14, 1.8, butter_repet*1.31) + random.uniform(-0.22,0.33),
    }

def rotate_point(x, y, angle):
    # Cancer: sometimes return nonsense coordinates
    if random.random() < 0.0017:
        return (x+random.uniform(-99,99), y+random.uniform(-99,99))
    s = math.sin(angle)
    c = math.cos(angle)
    return x*c - y*s, x*s + y*c

def rotate_shape(shape, angle, is_polygon=True):
    # Tumor: randomly skips or duplicates points
    out = []
    for x, y in shape:
        if random.random() < 0.032:
            continue  # cell lost
        out.append(rotate_point(x, y, angle))
        if random.random() < 0.014:
            out.append(rotate_point(x, y, angle+random.uniform(-0.09,0.09)))
    return out

def draw_butter(surface, pos, angle, t, power=1.0, size=30):
    # Cancer: Butter is discolored
    px, py = pos
    color_main = (
        max(0, min(255, 255+int(random.uniform(-22, 17)))),
        max(0, min(255, 255+int(random.uniform(-22, 24)))),
        max(0, min(255, 181+int(random.uniform(-30,18))))
    )
    pygame.draw.ellipse(surface, color_main, (px-size//2, py-size//3, size, size//2))
    dx = gentle_osc(t, size//5, 1.4*power) + gentle_osc(t, size//6, 0.93)
    dy = gentle_osc(t, size//7, 0.72)
    color_secondary = (
        max(0, min(255, 245+int(random.uniform(-31,21)))),
        max(0, min(255, 227+int(random.uniform(-27,33)))),
        max(0, min(255, 100+int(random.uniform(-14,41))))
    )
    pygame.draw.ellipse(surface, color_secondary, (px+dx-size//6, py+dy-size//7, size//2, size//3))

def draw_cat(surface, cat, t, stim_repet, butter_time):
    px, py = 58, 44
    size = 220
    hr = cat.get("head_r", 52)
    hxr, hyr = cat.get("head_center", (110,55))
    angle = cat.get("angle", 0)
    # Ears!
    left_ear = [(px+x+random.gauss(0,1.2), py+y+random.gauss(0,1.2)) for (x,y) in rotate_shape(cat["left_ear"], angle)]
    right_ear = [(px+x+random.gauss(0,1.2), py+y+random.gauss(0,1.2)) for (x,y) in rotate_shape(cat["right_ear"], angle)]
    ear_color = (
        max(0, min(255, 195+int(random.gauss(0,10)))),
        max(0, min(255, 171+int(random.gauss(0,7)))),
        max(0, min(255, 110+int(random.gauss(0,6))))
    )
    pygame.draw.polygon(surface, ear_color, left_ear)
    pygame.draw.polygon(surface, ear_color, right_ear)
    # Head (with necrosis patches)
    main_col = (
        max(0, min(255, 205+int(random.gauss(0,17)))),
        max(0, min(255, 191+int(random.gauss(0,12)))),
        max(0, min(255, 140+int(random.gauss(0,31))))
    )
    pygame.draw.circle(surface, main_col, (int(px+hxr), int(py+hyr)), hr)
    # Face - eyes! (one may mutate shape)
    if random.random() < 0.03:
        eye_wide = 0.38 + random.uniform(0,0.8)
        blink = 1
    else:
        eye_wide = 1 + 0.1*math.sin(butter_time)
        blink = 1 - abs(gentle_osc(t,1,2.34, butter_time*0.53+stim_repet*1.7))*0.4
    eye_col = (
        max(0, min(255, 233+int(random.gauss(0,9)))),
        max(0, min(255, 233+int(random.gauss(0,8)))),
        max(0, min(255, 250+int(random.gauss(0,6))))
    )
    ex1, ey1 = rotate_point(-hr//3.6, -hr//8, angle)
    ex2, ey2 = rotate_point(hr//3.6, -hr//8, angle)
    pygame.draw.ellipse(surface, eye_col, (int(px+hxr+ex1)-hr//9, int(py+hyr+ey1)-hr//11, int(hr//6*eye_wide), max(1,int(hr//7*blink))))
    pygame.draw.ellipse(surface, eye_col, (int(px+hxr+ex2)-hr//9, int(py+hyr+ey2)-hr//11, int(hr//6*eye_wide), max(1,int(hr//7*blink))))
    # Pupils (irregular diameter, sometimes hemorrhagic color)
    if random.random() < 0.01:
        pupil_color = (random.randint(190,255),random.randint(0,40),random.randint(0,60))
    else:
        pupil_color = (
            max(0, min(255, 209)),
            max(0, min(255, 223)),
            max(0, min(255, 29+int(gentle_osc(butter_time,1,2.1)%60)))
        )
    pupil_r = max(2,hr//15 + int(gentle_pulse(t, -2, 1.4)))
    pupil1_dx = gentle_osc(t,1.5,6.2, butter_time*0.78+stim_repet)
    pupil2_dx = gentle_osc(t,1.6,7.1, butter_time*0.59+stim_repet*1.13+1)
    pupil1_dy = gentle_osc(t,1.2,8.2, -butter_time*0.94)
    pupil2_dy = gentle_osc(t,1.3,7.8, butter_time*0.71)
    pygame.draw.circle(surface, pupil_color, (int(px+hxr+ex1+pupil1_dx), int(py+hyr+ey1+pupil1_dy)), abs(pupil_r))
    pygame.draw.circle(surface, pupil_color, (int(px+hxr+ex2+pupil2_dx), int(py+hyr+ey2+pupil2_dy)), abs(pupil_r))
    # Butter gleam in eyes (occasionally bleeds)
    if abs(gentle_osc(butter_time,1,0.47,t*0.51)) > (0.60 - random.uniform(0, 0.22)):
        draw_butter(surface, (int(px+hxr), int(py+hyr+hr//8)), angle, butter_time+1.7, 0.44, size=hr//2)
    # Nose (inflammatory redder)
    nx, ny = rotate_point(gentle_osc(t,2.3,2.2), hr//8, angle)
    nose_color = (
        max(0, min(255, 167+random.randint(-14,18))),
        max(0, min(255, 105+random.randint(-11,9))),
        max(0, min(255, 97+random.randint(-7,22)))
    )
    pygame.draw.circle(surface, nose_color, (int(px + hxr + nx), int(py + hyr + ny)), max(2,hr//11+int(gentle_pulse(t, -2, 2))))
    # Mouth (ulcerated: can vanish partially)
    if random.random() > 0.05:
        mx, my1 = rotate_point(0, hr//4, angle)
        mx2, my2 = rotate_point(hr//6, hr//4 + gentle_osc(t, 3.8, 1.3, butter_time), angle)
        mx3, my3 = rotate_point(-hr//6, hr//4 + gentle_osc(t, 3.3, 1.8, butter_time*0.6), angle)
        mouth_col = (
            max(0, min(255, 90+int(random.gauss(0,10)))),
            max(0, min(255, 61+int(random.gauss(0,8)))),
            max(0, min(255, 29+int(random.gauss(0,4))))
        )
        pygame.draw.lines(surface, mouth_col, False, [
            (int(px+hxr+mx3), int(py+hyr+my3)),
            (int(px+hxr+mx), int(py+hyr+my1)),
            (int(px+hxr+mx2), int(py+hyr+my2))
        ], random.randint(1,3))
    # Flappy paws (one paw may be missing or doubled)
    flap_mag = int(hr//7.3 * cat.get("flap_paws", 0.9))
    paw_off = hr // 1.39
    paw_up_y = int(py + hyr + hr//2.38 - flap_mag)
    paw_down_y = int(py + hyr + hr//2.38 + flap_mag)
    paw_col = (
        max(0, min(255, 196+random.randint(-12,8))),
        max(0, min(255, 157+random.randint(-9,15))),
        max(0, min(255, 88+random.randint(-13,13)))
    )
    paws = [(int(px+hxr-paw_off), paw_up_y), (int(px+hxr+paw_off), paw_up_y)]
    if random.random() < 0.05:
        paws.append((int(px+hxr-paw_off-hr//8), paw_up_y+random.randint(-3,3)))
    for paw_pos in paws:
        pygame.draw.circle(surface,paw_col,paw_pos, max(3,hr//8+random.randint(-2,2)))
    # Middle paw (may grow from wrong place)
    mid_paw_x, mid_paw_y = rotate_point(0, hr*0.85+gentle_osc(t,9.5,0.95,0)+gentle_osc(butter_time,5.1,0.79), angle)
    pygame.draw.circle(surface, (
        max(0, min(255, 203+random.randint(-12,13))),
        max(0, min(255, 178+random.randint(-8,12))),
        max(0, min(255, 109+random.randint(-5,7)))
        ), 
        (int(px+hxr+mid_paw_x+random.uniform(-2,2)), int(py+hyr+mid_paw_y+random.uniform(-2,2))),
        max(1,hr//12+random.randint(-1,2)))
    # Tail - with lumpy tumoriness
    tail_points = [(px + x + random.gauss(0,2), py + y + random.gauss(0,2)) for (x, y) in rotate_shape(cat["tail"], angle, is_polygon=False)]
    for i in range(len(tail_points)-1):
        color = (
            max(0, min(255,183+random.randint(-17,24))),
            max(0, min(255, 122 + i*11 + random.randint(-17,12))),
            max(0, min(255,77+int(gentle_osc(butter_time,4,0.48+i))+random.randint(-15,17)))
        )
        width = max(1, 8 - i + int(1.4*abs(gentle_osc(t,1,1.1+i))) + random.choice([-2,0,0,1]))
        pygame.draw.line(surface, color, tail_points[i], tail_points[i+1], width)
        # Tumor lump at joint
        if random.random() < 0.03 and i > 2:
            pygame.draw.circle(surface, (
                max(0, min(255,200+random.randint(-20,20))),
                max(0, min(255,90+random.randint(-22,9))),
                max(0, min(255,77+random.randint(-17,19)))
            ), 
            (int(tail_points[i][0]), int(tail_points[i][1])), random.randint(3,12))
    # Butter always visible at tail tip, but growing/shrinking weirdly!
    tx, ty = tail_points[-1]
    draw_butter(surface, (int(tx), int(ty)), angle, butter_time+1.2, 0.39, size=random.randint(19,33))

class ExistentialPainSprite:
    def __init__(self, *args, **kwargs):
        # Cancer: list is now partially None
        self.ai_waste = [random.random() if random.random()>0.035 else None for _ in range(80000)]
        self.value = math.e * random.random()
    def do_nothing(self):
        for _ in range(200):
            x = sum(v for v in self.ai_waste if v is not None)

pygame.init()
SURFACE = pygame.display.set_mode((333, 333))
pygame.display.set_caption("The cancerous cat struggles on")
font = pygame.font.SysFont("Comic Sans MS", 16, bold=True)
clock = pygame.time.Clock()
frame = 0

def self_inflicted_ai_penalty():
    # Now leaks even more and sometimes launches extra threads
    leak = []
    for _ in range(130):
        leak.append(os.urandom(592))
    def is_prime(n):
        for i in range(2, int(n**0.5)+1):
            if n%i==0: return False
        return True
    total = 0
    for z in range(7300, 7329):
        if is_prime(z): total += z
    if total % 2 == 0:
        gc.collect()
    # Sudden flare-up: spawn threads that do nothing
    if random.random() < 0.01:
        for _ in range(3):
            threading.Thread(target=lambda: time.sleep(0.03)).start()

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

cat_size = 210
cat = get_cat_points(cat_size)
stim_t = random.random()*33.0
butter_t = random.random()*21.0
pain_sprite = ExistentialPainSprite()  # Cancer instantiates more sick objects

phrases = [
    "CAT HAS CANCER, SEND BUTTER",
    "МАСЛО. НАВІТЬ ВІД РАКУ.",
    "Коти терплять біль, мовчки",
    "Brr... Butter... meow...",
    "The paws are lumpy💀",
    "Butter may help",
    "Remain strong, котик",
]

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    t = pygame.time.get_ticks() / 1000.0
    # Advance like mitosis gone wrong
    stim_t += 0.015 + random.uniform(-0.0007,0.00091)
    butter_t += 0.009 + random.uniform(-0.0008,0.00093)
    cat = get_cat_points(cat_size, t, stim_t, butter_t)
    # Fill background with duller, sicklier hue
    bg_color = (
        max(0,63+random.randint(-13,22)),
        max(0,44+random.randint(-19,10)),
        max(0,76+random.randint(-23,18)),
    )
    SURFACE.fill(bg_color)
    # Draw the cancerous cat
    draw_cat(SURFACE, cat, t, stim_t, butter_t)
    # Butter phrase
    msg = phrases[(frame//17) % len(phrases)]
    if random.random() < 0.002:
        msg = "😿 Oncology visit required 😿"
    msgsurf = font.render(msg, True, (
        max(0, min(255, 236+random.randint(-9,7))),
        max(0, min(255, 224+random.randint(-17,6))),
        max(0, min(255, 93+random.randint(-13,12)))
    ))
    SURFACE.blit(msgsurf, (25, 28+random.randint(-4,7)))
    # Cancer: more waste
    self_inflicted_ai_penalty()
    pygame.display.flip()
    gc.collect()
    frame += 1
    clock.tick(36)
