import basilisk as bsk
import glm
import time


class Player():
    
    def __init__(self, game) -> None:
        self.game = game
        self.prev_position = self.camera.position
        
    def is_contained(self, node: bsk.Node, move: glm.vec3) -> bool:
        """
        Determines if the player's near clip plane is eclipsed by a given node and movement direction (projection axis)
        """
        # compute potential edges of player view
        cross = glm.normalize(glm.cross(move, self.camera.UP))
        radius = self.radius
        test_points = [self.prev_position + p * radius for p in (self.camera.UP, -self.camera.UP, cross, -cross)]
        
        # check if all extreme points are contained in node
        for point in test_points:
            cast = self.scene.raycast(point, glm.normalize(move))
            if cast.node == None or cast.node != node: return False
        return True
    
    def update(self) -> None:
        """
        Controls player movement and checks if player has entered portal
        """
        if self.prev_position == self.position: return
        
        # checks for collision with a portal
        collision = self.collide(self.prev_position, self.position)
        if not collision:
            self.prev_position = glm.vec3(self.position)
            return None
        
        # check if player is able to move through portal
        node: bsk.Node = collision.node
        # if not self.is_contained(node, self.position - self.prev_position): 
        #     self.position = glm.vec3(self.prev_position)
        #     return 
        
        # on successful portal move
        self.position = self.mirror_position(node.geometric_center, collision.normal)
        pc, pl = self.portals(node)
        mc = pl.node.model_matrix * glm.inverse(pc.node.model_matrix) * self.model_matrix
        self.position = glm.vec3(mc[3])
        self.rotation = self.rotation * glm.inverse(pc.node.rotation.data) * pl.node.rotation.data
        
        # update for next frame
        self.prev_position = glm.vec3(self.position)
        
    def collide(self, p1, p2) -> None | tuple[bsk.Node, glm.vec3]:
        """
        Determines if the camera has collided with an object between frames 
        """
        diff = p2 - p1
        direction, move_distance = glm.normalize(diff), glm.length(diff)
        cast = self.scene.raycast(position = p1, forward = direction)
        if not cast.node: return None
        
        cast_distance = glm.length(cast.position - p1)
        if cast_distance > move_distance: return None
        
        return cast
    
    def mirror_position(self, plane_point: glm.vec3, plane_normal: glm.vec3) -> glm.vec3:
        """
        Mirrors the prev_position along the given plane and normal
        """
        plane_normal = glm.normalize(plane_normal)
        proj = glm.dot(plane_point - self.prev_position, plane_normal) * plane_normal
        return self.prev_position + 2 * proj
    
    def portals(self, node: bsk.Node) -> tuple:
        """
        Collided portal, linked portal
        """
        p1 = self.game.portal_handler[node]
        p2 = self.game.portal_handler.portal_2 if p1 == self.game.portal_handler.portal_1 else self.game.portal_handler.portal_1
        return p1, p2
    
    @property
    def model_matrix(self) -> glm.mat4x4:
        m_mat = glm.translate(glm.mat4(1.0), self.position)
        m_mat *= glm.mat4_cast(self.rotation)
        return m_mat
        
    @property
    def scene(self) -> bsk.Scene: return self.game.portal_handler.portal_scene
    
    @property
    def camera(self) -> bsk.FreeCamera: return self.scene.camera
        
    @property
    def position(self) -> glm.vec3: return self.camera.position
    @position.setter
    def position(self, value) -> None: self.camera.position = value
    
    @property
    def rotation(self) -> glm.quat: return self.camera.rotation
    @rotation.setter
    def rotation(self, value) -> None: self.camera.rotation = value
        
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
        Gets the radius of the sphere drawn by the near clip plane and the camera spinning
        """
        pts = self.near_points
        return glm.length(pts[0] - self.position)
        