from pgzero.actor import Actor
from pgzero import game
from time import time

WIDTH = 800


class AnimatedActor(Actor):
    def __init__(self, *args, pingpong=False, duration=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.pingpong = pingpong
        self.duration = duration
        self._stopped = False

        # TODO make it required
        self.height = kwargs['sprite'][1]
        self.width = kwargs['sprite'][0]

        # prepare frames
        self._frames = []
        for x_offset in range(int(self._orig_surf.get_width() / self.width)):
            surface = self._orig_surf.subsurface((x_offset * self.width, 0, self.width, self.height))
            self._frames.append(surface)

        # frame config
        self._current_frame = 0
        self.frame_duration = self.duration / len(self._frames)
        self.last_frame_update = time() * 1000
        self._next_frame_dx = 1

    def start(self):
        self._stopped = False

    def stop(self):
        self._stopped = True

    @property
    def current_frame(self):
        return self._current_frame

    @current_frame.setter
    def current_frame(self, index):
        if 0 < index < len(self._frames) -1:
            raise 'Frame index out of range.'
        self._current_frame = index

    def _update_frame(self):
        if not self._stopped:
            now = time() * 1000
            if now - self.last_frame_update > self.frame_duration:
                self.last_frame_update = now
                self._current_frame += self._next_frame_dx

                if self.pingpong:
                    if self._next_frame_dx == 1 and self._current_frame >= len(self._frames) - 1 or self._next_frame_dx == -1 and self._current_frame <= 0:
                        self._next_frame_dx *= -1
                else:
                    if self._current_frame == len(self._frames):
                        self._current_frame = 0

    def draw(self):
        self._update_frame()
        print(self._current_frame)
        game.screen.blit(self._frames[self._current_frame], self.topleft)



def draw():
    screen.clear()
    braid.draw()

def update(dt):
    
    # if braid.x > WIDTH:
    #     braid.x = 0
    if keyboard.space:
        if braid._stopped:
            braid.start()
        else:
            braid.stop()
            braid.current_frame = 0
    
    if not braid._stopped:
        braid.x += 1


braid = AnimatedActor('braid_run', sprite=(130, 150), duration=200, pingpong=True)
# braid.pos = (50, 50)
# b = B()
# b.mega()