import pygame
import sys
import math
import random

# --- ULTRAAUTISTIC CAT W/ MAXIMUM SAFE STIM, GLEAMING BUTTER, AND ECHOLALIA YOU CAN FEEL (!) ---
# Safe for epilepsy! No flashes, no rapid color inversion, no intense flicker.

LES_PHRASES = [
    "Йоб твою мать",
    "Чьо ти, сучара?",
    "Степан — дебіл",
    "Давайте щось пожремо",
    "Чьортова жаба",
    "А я вас всіх люблю",
    "Гнила інтелігенція",
    "Життя — хуйня, коти — сила",
    "Бутерброд з маслом найкращий",
    "Все з маслом стає краще",
    "AUTISTIC CAT LOVES BUTTER",
    "МАСЛО. БІЛЬШЕ МАСЛА.",
]

# --- Utility: gentle low flickers for safety ---
def gentle_osc(x, amp=1.0, freq=1.0, offset=0.0):
    return amp * math.sin(x * freq + offset)

def gentle_pulse(x, low=0.7, high=1.0, freq=1.0, offset=0.0):
    # normalized between low and high, never abrupt
    return low + (high - low) * (math.sin(x * freq + offset) * 0.5 + 0.5)

def get_cat_points(size, t=0, stim_repet=0, butter_repet=0):
    head_r = size // 4
    body_w = size // 2
    body_h = size // 3
    phase = 2 * math.pi

    stim_head_dx = (
        gentle_osc(t, 7, 3.8)
        + gentle_osc(t, 3, 7.2)
        + gentle_osc(stim_repet, 1.6, 6.3)
        + gentle_osc(butter_repet, 1.8, 9.1)
    )
    stim_head_dy = (
        gentle_osc(t, 2.4, 2.2) +
        gentle_osc(stim_repet, 1.4, 8.1)
        + gentle_osc(butter_repet, 1.2, 5.7)
    )

    stim_ear_l = (
        gentle_osc(t, 16, 12.6, phase * 0.1)
        + gentle_osc(t, 12, 2) + gentle_osc(stim_repet, 3.2, 13.0)
        + gentle_osc(butter_repet, 9, 8.6)
    )
    stim_ear_r = (
        gentle_osc(t, 17, 13.7, 1.9)
        + math.cos(t * 1.5 - stim_repet*1.3) * 10
        + gentle_osc(stim_repet, 3.2, 14.0)
        + math.cos(butter_repet*8.5+0.5)*8
    )

    stim_body_dx = (
        gentle_osc(t, 8, 3.1)
        + gentle_osc(stim_repet, 3.2, 7.6, 1)
        + gentle_osc(butter_repet, 4, 2.7)
    )
    stim_body_dy = (
        gentle_osc(t, 13, 6.7) + gentle_osc(butter_repet, 6.1, 4.9)
    )

    stim_tail_base = (
        gentle_osc(t, 16, 4.5)
        + gentle_osc(stim_repet, 15, 4.8)
        + gentle_osc(t, 7, 0.8)
        + math.cos(butter_repet*3.2) * 7
    )

    tail_pts = []
    num_tail_segments = 12
    for i in range(num_tail_segments):
        butter_tail = gentle_osc(butter_repet, 2.6, 2.8, i*0.9)
        x = (
            body_w // 2
            + 6 * i
            + stim_tail_base * (0.09 + 0.07*i)
            + gentle_osc(t, 4, 2.4, stim_repet*1.1+i)
            + butter_tail
        )
        y = (
            size//6
            + 9*i
            + gentle_osc(t, 7, 5.2, stim_repet*1.2+i*0.8)
            + math.cos(butter_repet*2.3+i*1.3)*2.3
        )
        tail_pts.append((x, y))

    flap_paws = (
        0.87
        + 0.30 * gentle_osc(stim_repet, 1, 13.1, t * 5.2)
        + 0.23 * gentle_osc(t, 1, 23, stim_repet)
        + 0.12 * gentle_osc(butter_repet, 1, 9.8, t*1.1)
    )

    return {
        "head": (stim_head_dx, -size // 6 + stim_head_dy, head_r),
        "left_ear": [
            (-head_r // 1.7 + gentle_osc(t, 5, 7.9, stim_repet + butter_repet), -size // 3 + stim_ear_l),
            (-head_r // 3.1 + gentle_osc(t, 2, 3.07, stim_repet * 0.8 + butter_repet*1.2), -size // 2 + stim_ear_l * 1.18),
            (gentle_osc(t, 2.8, 2.18, 1 + stim_repet * 0.6 + butter_repet * 0.7), -size // 3 + stim_ear_l)
        ],
        "right_ear": [
            (head_r // 1.7 + gentle_osc(t, 5, 7.5, stim_repet + butter_repet), -size // 3 + stim_ear_r),
            (head_r // 3.1 + gentle_osc(t, 2, 4.32, stim_repet * 0.8 + butter_repet*1.35), -size // 2 + stim_ear_r * 1.18),
            (gentle_osc(t, 2.8, 2.7, stim_repet * 0.45 + butter_repet*0.61), -size // 3 + stim_ear_r)
        ],
        "body": (0 + stim_body_dx, size // 8 + stim_body_dy, body_w, body_h),
        "tail": tail_pts,
        "flap_paws": flap_paws,
    }

def rotate_point(x, y, angle_deg):
    angle_rad = math.radians(angle_deg)
    cosA = math.cos(angle_rad)
    sinA = math.sin(angle_rad)
    xr = x * cosA - y * sinA
    yr = x * sinA + y * cosA
    return xr, yr

def rotate_shape(points, angle, is_polygon=True):
    return [rotate_point(x, y, angle) for (x, y) in points]

def draw_butter(surface, pos, angle, butter_time, butter_level=1.0, size=38):
    # Draw a shiny, wobbly, but safe butter :)
    x, y = pos
    phase = butter_time * 2.7 + gentle_osc(butter_time, 1, 7.1)
    butter_dx = gentle_osc(butter_time, 3.5, 6.7, angle*0.11)
    butter_dy = gentle_osc(butter_time, 2.7, 7.2, angle*0.11)

    butter_color = (
        int(236-20*gentle_osc(butter_time,1,2.18)),
        int(202+12*gentle_osc(butter_time,1,2.21)),
        int(82+16*gentle_osc(butter_time,1,1.89)),
    )
    slab_w = int(size*butter_level*1.10)
    slab_h = int(size*butter_level*0.59)
    corner = (x+butter_dx-slab_w//2, y+butter_dy-slab_h//2)
    slab_rect = pygame.Rect(corner, (slab_w, slab_h))
    safe_butter_color = tuple(max(0, min(255, int(c))) for c in butter_color)
    pygame.draw.rect(surface, safe_butter_color, slab_rect, border_radius=int(size*0.22))
    # Gentle pats of butter, ratcheted down for safety
    for i in range(4):
        theta = i*math.pi/2 + phase + gentle_osc(i+angle,0.5,1.19)
        dot_x = x + butter_dx + math.cos(theta)*(slab_w//2-8)
        dot_y = y + butter_dx + math.sin(theta)*(slab_h//2-8)
        pygame.draw.circle(surface, (255,240,176), (int(dot_x), int(dot_y)), int(4+math.sin(butter_time*2.4+i)))

    # Big butter shine - subtle, safe
    shine_radius = int(slab_w*0.27)
    shine_surf = pygame.Surface((shine_radius*2, shine_radius*2), pygame.SRCALPHA)
    pygame.draw.circle(shine_surf, (255,255,210,100), (shine_radius, shine_radius), shine_radius)
    surface.blit(shine_surf, (int(x+butter_dx-shine_radius), int(y+butter_dy-slab_h//2-shine_radius//4)), special_flags=pygame.BLEND_RGBA_ADD)

    # Sparkles (gentle, yellow)
    for i in range(3):
        sparkle_phase = butter_time*1.1+i*2
        sx = x + butter_dx + math.sin(sparkle_phase)*slab_w*0.38
        sy = y + butter_dy + math.cos(sparkle_phase)*slab_h*0.33
        alpha_surf = pygame.Surface((10,10), pygame.SRCALPHA)
        alpha = int(40 + 100*(0.5+0.5*gentle_osc(butter_time,1,4.8+i)))
        pygame.draw.circle(alpha_surf, (255,252,200,alpha), (5,5), 4)
        surface.blit(alpha_surf, (int(sx)-5, int(sy)-5), special_flags=pygame.BLEND_RGBA_ADD)

def draw_cat(surface, center, size, angle, t, stim_repet, phrase=None, butter_time=0.0):
    px, py = center
    butter_repet = t + stim_repet + gentle_osc(butter_time,1,1.2)
    cat = get_cat_points(size, t, stim_repet, butter_repet)

    stim_mag = (
        abs(gentle_osc(t,1,5.22) * math.cos(angle / 12)) +
        abs(gentle_osc(stim_repet,1,3.7)) +
        abs(gentle_osc(t,1,3.1, stim_repet*1.2)) * 0.35 +
        abs(gentle_osc(butter_time,1,2.1)) * 0.23
    )
    stim_color = (
        int(190 + 80 * stim_mag),
        int(74 + 80 * stim_mag),
        int(44 + 65 * stim_mag)
    )
    safe_stim_color = tuple(max(0, min(255, int(c))) for c in stim_color)

    pygame.draw.polygon(surface, safe_stim_color, [(int(px + x), int(py + y)) for (x, y) in rotate_shape(cat["left_ear"], angle)])
    pygame.draw.polygon(surface, safe_stim_color, [(int(px + x), int(py + y)) for (x, y) in rotate_shape(cat["right_ear"], angle)])

    bx, by, bw, bh = cat["body"]
    bxr, byr = rotate_point(bx, by, angle)
    pygame.draw.ellipse(surface, (142, 108, 52), (px + bxr - bw//2, py + byr - bh//2, bw, bh))

    hx, hy, hr = cat["head"]
    hxr, hyr = rotate_point(hx, hy, angle)
    pygame.draw.circle(surface, (204, 171, 100), (int(px + hxr), int(py + hyr)), hr)

    # More autistic: biggest joy is safe eye stim. Remove all dangerous sharp flicker.
    stare_mod = abs(gentle_osc(t,1,2.9) + gentle_osc(stim_repet,1,1.7) + gentle_osc(butter_time,1,2.38))
    stare_level = min(247, int(stare_mod*140)+65)
    eye_col = (
        stare_level,
        max(0, stare_level-68),
        53+int(abs(gentle_osc(butter_time,1,2.35))*17)
    )

    # Eyes, more wide-set (autistic!), subtle nystagmus, but no unsafe fast flickering
    blink = gentle_pulse(t, 0.94, 1.16, 1.2) * (1 + gentle_osc(stim_repet*1.2+butter_time*0.5,0.08,1.2))
    wide = 0.48 + 0.22 * abs(gentle_osc(t,1,3.1, stim_repet * 2 + butter_time))

    ex1_off = gentle_osc(stim_repet, 1.8, 7.1, butter_time*0.7)
    ex2_off = gentle_osc(stim_repet, 2.1, 9.1, butter_time*1.1)
    nyst1 = gentle_osc(t,1,8.4, butter_time*1.7)
    nyst2 = -gentle_osc(t,1,8.7, butter_time*2.5)

    ex1, ey1 = rotate_point(-hr//2.3 + ex1_off + nyst1, -hr//8 * blink, angle)
    ex2, ey2 = rotate_point(hr//2.3 + ex2_off + nyst2, -hr//8 * blink, angle)

    # Gentle highlight in eyes
    highlight_offset = hr//17
    for eye_x, eye_y in [(ex1, ey1), (ex2, ey2)]:
        # Butter pupil highlight (never flickers)
        if abs(gentle_osc(butter_time,1,2.6, t*1.8+eye_x*0.4)) > 0.37:
            high_x, high_y = int(px+hxr+eye_x+highlight_offset), int(py+hyr+eye_y-highlight_offset)
            pygame.draw.circle(surface, (246,240,103), (high_x, high_y), max(2,hr//18))

    # Subtle butter sparkle at times
    if math.fabs(gentle_osc(t,1,1.7, stim_repet*2.2 + butter_time)) > 0.83:
        pygame.draw.ellipse(surface, (255,240,110),
            (int(px + hxr + ex1)-hr//6, int(py + hyr + ey1)-hr//6, hr//3, int(hr//5 * 1.95)))
        pygame.draw.ellipse(surface, (255,240,110),
            (int(px + hxr + ex2)-hr//6, int(py + hyr + ey2)-hr//6, hr//3, int(hr//5 * 1.95)))

    # Render the actual "eye whites"
    pygame.draw.ellipse(surface, eye_col, (int(px + hxr + ex1) - hr//9, int(py + hyr + ey1) - hr//11, int(hr//6*wide), int(hr//7 * blink)))
    pygame.draw.ellipse(surface, eye_col, (int(px + hxr + ex2) - hr//9, int(py + hyr + ey2) - hr//11, int(hr//6*wide), int(hr//7 * blink)))

    # Darting, autistic pupils (gentle movements, not flashing!)
    pupil_color = (
        min(255,eye_col[0]-24),
        min(255,eye_col[1]+19),
        max(0, min(255, 29+int(gentle_osc(butter_time,1,2.1)%60)))
    )
    pupil_r = max(4,hr//15)
    pupil1_dx = gentle_osc(t,1.5,6.2, butter_time*0.78+stim_repet)
    pupil2_dx = gentle_osc(t,1.6,7.1, butter_time*0.59+stim_repet*1.13+1)
    pupil1_dy = gentle_osc(t,1.2,8.2, -butter_time*0.94)
    pupil2_dy = gentle_osc(t,1.3,7.8, butter_time*0.71)
    pygame.draw.circle(surface, pupil_color, (int(px + hxr + ex1 + pupil1_dx), int(py + hyr + ey1 + pupil1_dy)), pupil_r)
    pygame.draw.circle(surface, pupil_color, (int(px + hxr + ex2 + pupil2_dx), int(py + hyr + ey2 + pupil2_dy)), pupil_r)

    # Butter gleam in eyes: soft alpha, slow only
    butter_eye_alpha = int(120+70*gentle_osc(butter_time,1,0.9)+60*gentle_osc(t,1,0.5))
    if butter_eye_alpha > 170:
        surf1 = pygame.Surface((hr//6, hr//8), pygame.SRCALPHA)
        pygame.draw.ellipse(surf1, (252,240,153,butter_eye_alpha), (0,0,hr//6,hr//8))
        surface.blit(surf1, (int(px+hxr+ex1)-hr//12, int(py+hyr+ey1)-hr//15), special_flags=pygame.BLEND_RGBA_ADD)
        surf2 = pygame.Surface((hr//6, hr//8), pygame.SRCALPHA)
        pygame.draw.ellipse(surf2, (252,240,153,butter_eye_alpha), (0,0,hr//6,hr//8))
        surface.blit(surf2, (int(px+hxr+ex2)-hr//12, int(py+hyr+ey2)-hr//15), special_flags=pygame.BLEND_RGBA_ADD)

    # Butter on snout, safe speed
    if abs(gentle_osc(butter_time,1,0.47,t*0.51)) > 0.82:
        draw_butter(surface, (int(px+hxr), int(py+hyr+hr//8)), angle, butter_time+1.7, 0.44, size=hr//2)
        # butter drip, slower
        if abs(gentle_osc(butter_time,1,0.72,t*1.01)) > 0.85:
            draw_butter(surface, (int(px+hxr), int(py+hyr+hr//3)), angle, butter_time+2.12, 0.18, size=hr//3)

    # Nose - stims, but with gentle period
    nx, ny = rotate_point(gentle_osc(t+stim_repet*0.1,2.3,2.2), hr//8, angle)
    pygame.draw.circle(surface, (167, 105, 97), (int(px + hxr + nx), int(py + hyr + ny)), hr//11)

    # Mouth - stimming Les grin, but safe
    mx, my1 = rotate_point(0, hr//4, angle)
    mx2, my2 = rotate_point(hr//6, hr//4 + gentle_osc(t+stim_repet, 3.8, 1.3, butter_time), angle)
    mx3, my3 = rotate_point(-hr//6, hr//4 + gentle_osc(t-stim_repet, 3.3, 1.8, butter_time*0.6), angle)
    pygame.draw.lines(surface, (90, 61, 29), False, [
        (int(px+hxr+mx3), int(py+hyr+my3)),
        (int(px+hxr+mx), int(py+hyr+my1)),
        (int(px+hxr+mx2), int(py+hyr+my2))
    ], 2)

    # Butter tongue - hang out sometimes!
    if abs(gentle_osc(butter_time,1,0.61,t*0.97)) > 0.985:
        tongue_x, tongue_y = rotate_point(0, hr//2.6, angle)
        rect = pygame.Rect(int(px+hxr+tongue_x)-6, int(py+hyr+tongue_y), 12, 16)
        pygame.draw.ellipse(surface, (255,230,90), rect)
        # Butter drop!
        if abs(gentle_osc(butter_time,1,1.4, t*0.92)) > 0.93:
            draw_butter(surface, (int(px+hxr+tongue_x), int(py+hyr+tongue_y)+10), angle, butter_time+5.8, 0.15, size=10)

    # --- HAND FLAPPING PAWS: Ultra stim! Gentle ---
    flap_mag = int(hr//7.3 * cat["flap_paws"])
    paw_off = hr // 1.39
    paw_up_y = int(py + hyr + hr//2.38 - flap_mag)
    paw_down_y = int(py + hyr + hr//2.38 + flap_mag)
    # Butter paws - at very peak only
    if abs(gentle_osc(butter_time,1,0.61,t*0.83)) > 0.92:
        draw_butter(surface, (int(px+hxr-paw_off), paw_up_y), angle, butter_time, 0.7, size=hr//2)
        draw_butter(surface, (int(px+hxr+paw_off), paw_up_y), angle, butter_time+1.3, 0.7, size=hr//2)
    elif gentle_osc(stim_repet,1,1.33)%1 > 0.66:
        pygame.draw.circle(surface,(208,194,120),(int(px+hxr-paw_off), paw_up_y), hr//8)
        pygame.draw.circle(surface,(208,194,120),(int(px+hxr+paw_off), paw_up_y), hr//8)
    elif int(stim_repet*3.5)%2==0:
        pygame.draw.circle(surface,(196,157,88),(int(px+hxr-paw_off), paw_up_y), hr//8)
        pygame.draw.circle(surface,(196,157,88),(int(px+hxr+paw_off), paw_down_y), hr//8)
    else:
        pygame.draw.circle(surface,(196,157,88),(int(px+hxr-paw_off), paw_down_y), hr//8)
        pygame.draw.circle(surface,(196,157,88),(int(px+hxr+paw_off), paw_up_y), hr//8)

    # Extra third paw!
    mid_paw_x, mid_paw_y = rotate_point(0, hr*0.85+gentle_osc(t,9.5,0.95,stim_repet)+gentle_osc(butter_time,5.1,0.79), angle)
    if int(stim_repet*1.23)%13 == 0 and abs(gentle_osc(butter_time,1,0.79))>0.53:
        draw_butter(surface, (int(px+hxr+mid_paw_x), int(py+hyr+mid_paw_y)), angle, butter_time+2.1, 0.34, size=hr//2)
    else:
        pygame.draw.circle(surface, (203,178,109), (int(px+hxr+mid_paw_x), int(py+hyr+mid_paw_y)), hr//12)

    # Tail stim!
    tail_points = [(px + x, py + y) for (x, y) in rotate_shape(cat["tail"], angle, is_polygon=False)]
    for i in range(len(tail_points)-1):
        color = (183, 122 + i*11, 77+int(gentle_osc(butter_time,4,0.48+i)))
        width = max(2, 8 - i + int(1.4*abs(gentle_osc(t,1,1.1+i+stim_repet*0.88+butter_time*0.51))))
        if i == len(tail_points)-2 and abs(gentle_osc(stim_repet,1,1.17,t))>0.8:
            pygame.draw.line(surface, (240,238,180), tail_points[i], tail_points[i+1], 2)
        safe_color = (
            max(0, min(255, color[0])),
            max(0, min(255, color[1])),
            max(0, min(255, color[2]))
        )
        pygame.draw.line(surface, safe_color, tail_points[i], tail_points[i+1], width)
    # Butter always visible at tail tip!
    tx, ty = tail_points[-1]
    draw_butter(surface, (int(tx), int(ty)), angle, butter_time+1.2, 0.39, size=26)

    # Space bubble
    stim_bubble = abs(gentle_osc(t,1,1.13,stim_repet*1.19 + butter_time*0.92))
    if stim_bubble > 0.79:
        for r in range(hr+19, hr+37, 6):
            alpha_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            alpha = int(stim_bubble*128) + 30
            pygame.draw.circle(alpha_surf, (177,216,240,alpha), (r,r), r)
            surface.blit(alpha_surf, (int(px+hxr)-r, int(py+hyr)-r), special_flags=pygame.BLEND_RGBA_ADD)

    # SPECIAL: GOLDEN SAFE STIM AURA, slower!
    stim_aura = abs(gentle_osc(t,1,0.87,stim_repet*0.73+butter_time*0.82))
    if stim_aura > 0.88:
        for r in range(hr+11, hr+27, 4):
            alpha_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            alpha = int(stim_aura*175)
            pygame.draw.circle(alpha_surf, (255,248,175,alpha), (r,r), r)
            surface.blit(alpha_surf, (int(px+hxr)-r, int(py+hyr)-r), special_flags=pygame.BLEND_RGBA_ADD)
        # Overlay: poderviansky butter mode at stim
        butter_overlay = False
        if abs(gentle_osc(butter_time,1,0.53,t)) > 0.89:
            butter_overlay = True
        if phrase or butter_overlay:
            font = pygame.font.SysFont('Arial', 24, bold=True)
            if butter_overlay:
                butter_text = "МАСЛО! BUTTER! БУТЕРБРОД!"
                text = font.render(butter_text, True, (220, 174, 31))
                text_bg = pygame.Surface((text.get_width()+20, text.get_height()+12), pygame.SRCALPHA)
                text_bg.fill((255,252,189, 230))
                text_bg.blit(text, (10,6))
            else:
                text = font.render(phrase, True, (30, 20, 80))
                text_bg = pygame.Surface((text.get_width()+16, text.get_height()+8), pygame.SRCALPHA)
                text_bg.fill((255,255,220, 184))
                text_bg.blit(text, (8,4))
            surface.blit(
                text_bg,
                (int(px + hxr - text.get_width()//2),
                 int(py + hyr - hr//1.3 - text.get_height() * 2))
            )

pygame.init()
size = 500
screen = pygame.display.set_mode((size, size))
clock = pygame.time.Clock()
angle = 0
start_time = pygame.time.get_ticks() / 1000.0
stim_repet = 0
pygame.font.init()

# --- Ultra-autistic phrase cycling, poderviansky + butter but with safe cycles ---
phrase_time = 0
les_phrase = LES_PHRASES[0]
butter_time = 0.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Echolalia: Type = next Les phrase, space for butter!
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Butter phrase
                les_phrase = random.choice([
                    "МАСЛО!",
                    "BUTTER!",
                    "AUTISTIC CAT LOVES BUTTER",
                    "BUTTERED REPETITION",
                    "ЗМАЩУЙ МАСЛОМ!"
                ])
            else:
                les_phrase = random.choice(LES_PHRASES)

    t = pygame.time.get_ticks() / 1000.0 - start_time
    # Ultra-gentle stim repetition, never abrupt
    stim_repet += (
        0.011 +
        abs(gentle_osc(t,1,0.93))*0.009 +
        0.0075 +
        abs(gentle_osc(t,1,2.7))*0.006
    )
    butter_time += 0.016 + abs(gentle_osc(t,1,1.25+stim_repet*0.13))*0.007

    # Use a low-contrast, soft background
    screen.fill((236, 237, 231))
    # Big soft butter slab for the safe joy!
    draw_butter(screen, (size//2, size//2 + size//4), 0, butter_time*0.39, 1.19, size//1.5)
    # --- MODIFICATION: The cat's face always upright & visible! ---
    draw_cat(screen, (size//2, size//2), 220, 0, t, stim_repet, les_phrase, butter_time)
    pygame.display.flip()

    # Reduce angle motion slightly for more body-based stim (less head roll)
    # angle is still updated, but no longer used for face rotation
    angle = gentle_osc(t,14,0.75) + gentle_osc(stim_repet,3.7,0.92) + gentle_osc(butter_time,5.6,0.61)
    clock.tick(60)
