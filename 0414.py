import pygame,sys,random,math
pygame.init();W,H=850,600
s=pygame.display.set_mode((W,H));c=pygame.time.Clock()
F=pygame.font.SysFont(None,36);B=pygame.font.SysFont(None,80)

R=8;bw,bh=70,25
MAXDX=6
SPD0=5;SPD_MAX=11;SPD_INC=0.15;INC_T=180

sb=pygame.Rect(W//2-80,H//2,160,50)
rb=pygame.Rect(W//2-80,H//2+90,160,50)

def ng():
 p=pygame.Rect(W//2-60,H-40,120,15)
 b=[[pygame.Rect(35+x*80,60+y*35,bw,bh),3-y//2]for y in range(5)for x in range(10)]
 a=random.uniform(-math.pi/4,math.pi/4)
 v=[SPD0*math.sin(a),-SPD0*math.cos(a)]
 return p,[W//2,H-60],v,SPD0,3,b,0

p,(x,y),(dx,dy),spd,l,b,t=ng()
state=0   # 0:MENU  1:PLAY  2:GAMEOVER

while 1:
 c.tick(60);s.fill((0,0,0))

 for e in pygame.event.get():
  if e.type==pygame.QUIT:pygame.quit();sys.exit()
  if e.type==pygame.MOUSEBUTTONDOWN:
   if state==0 and sb.collidepoint(e.pos):
    state=1
   if state==2 and rb.collidepoint(e.pos):
    p,(x,y),(dx,dy),spd,l,b,t=ng()
    state=0

 # ================= PLAY =================
 if state==1:
  t+=1
  if t%INC_T==0 and spd<SPD_MAX:
   spd=min(SPD_MAX,spd+SPD_INC)
   m=math.hypot(dx,dy)
   dx,dy=dx/m*spd,dy/m*spd

  k=pygame.key.get_pressed()
  if k[pygame.K_LEFT] and p.left>0:p.x-=8
  if k[pygame.K_RIGHT] and p.right<W:p.x+=8

  x+=dx;y+=dy

  if x<R:x=R;dx=abs(dx)
  elif x>W-R:x=W-R;dx=-abs(dx)
  if y<R:y=R;dy=abs(dy)

  if y>H:
   l-=1
   if l<1:state=2
   else:
    x,y=p.centerx,p.top-R
    a=random.uniform(-math.pi/4,math.pi/4)
    dx,dy=SPD0*math.sin(a),-SPD0*math.cos(a)
    spd=SPD0;t=0

  ball=pygame.Rect(x-R,y-R,R*2,R*2)

  if ball.colliderect(p) and dy>0:
   offset=(x-p.centerx)/(p.width/2)
   dx,dy=offset*MAXDX,-abs(dy)
   m=math.hypot(dx,dy)
   dx,dy=dx/m*spd,dy/m*spd

  for i in b[:]:
   r=i[0]
   if ball.colliderect(r):
    ox=min(ball.right-r.left,r.right-ball.left)
    oy=min(ball.bottom-r.top,r.bottom-ball.top)
    dx*=-1 if ox<oy else 1
    dy*=-1 if ox>=oy else 1
    i[1]-=1
    if i[1]<1:b.remove(i)
    break

 # ================= DRAW =================
 if state==0:
  pygame.draw.rect(s,(180,180,180),sb)
  s.blit(F.render("START",1,(0,0,0)),(sb.x+45,sb.y+12))

 elif state==1:
  for i in b:
   pygame.draw.rect(s,((255,0,0),(255,255,0),(0,200,0))[i[1]-1],i[0])
  pygame.draw.rect(s,(255,255,255),p)
  pygame.draw.circle(s,(255,255,255),(int(x),int(y)),R)
  s.blit(F.render(f"Lives:{l}",1,(255,255,255)),(10,10))

 else:
  s.blit(B.render("GAME OVER",1,(0,120,255)),(W//2-210,H//2-180))
  pygame.draw.rect(s,(180,180,180),rb)
  s.blit(F.render("RESTART",1,(0,0,0)),(rb.x+35,rb.y+12))

 pygame.display.flip()
