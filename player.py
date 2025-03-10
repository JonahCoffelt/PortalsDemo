import basilisk as bsk
import glm


class Player():
    
    def __init__(self, camera: bsk.FreeCamera) -> None:
        self.camera = camera
        
    @property
    def position(self) -> glm.vec3: return self.camera.position
    @position.setter
    def position(self, value) -> None: self.camera.position = value
        
    @property
    def near_points(self) -> list[glm.vec3]:
        """
        Gets the near clip plane coordinates of the camera in world space
        """
        player_corners: list[glm.vec4] = [glm.vec4(a, b, -1, 1) for a in (-1, 1) for b in (-1, 1)] # BL TL BR TR
        inv_proj: glm.mat4x4 = glm.inverse(self.camera.m_proj)
        inv_view: glm.mat4x4 = glm.inverse(self.camera.m_view)
        
        world_corners = []
        for corner in player_corners:
            view_pos = inv_proj * corner
            view_pos /= view_pos.w
            world_pos = inv_view * view_pos
            world_corners.append(glm.vec3(world_pos))
            
        return world_corners
            
    @property
    def radius(self) -> float:
        """
        Gets the radius of the circle drawn by the near clip plane if the camera was to turn 360 degrees around
        """
        bl, tl, br, tr = self.near_points
        r = (br + tr) / 2
        return glm.length(r - self.position)
        
        