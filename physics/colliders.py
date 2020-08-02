class Collider(object):
    def solve(self):
        raise NotImplementedError
    def reset(self):
        return

class GroundCollider(Collider):
    def __init__(self, partciles, bouncinnes=0.1, friction=.9, height=0.0):
        self.bouncinnes = bouncinnes
        self.friction = friction
        self.height = float(height)
        self.particles = partciles
    def solve(self):
        for each in self.particles:
            if each.isPinned():
                continue
            currPos = each.getPosition()
            if currPos[1] < self.height:
                prevPos = each.getPrevPosition()
                velocity = (currPos - prevPos) * self.friction
                currPos[1] = self.height
                each.setPosition(currPos)
                prevPos[1] = currPos[1]+(velocity[1] * each.getBounciness() * self.bouncinnes)
                each.setPrevPosition(prevPos)
