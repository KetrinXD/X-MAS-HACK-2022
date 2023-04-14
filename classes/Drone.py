import asyncio
import multiprocessing as mp
from classes.Vector import Vector3
from classes.Controller import SimController
class Drone:
    def __init__(self, name, sim_object,
                 controller:SimController):
        self.max_velocity = 0.3
        self.max_acceleration = 0.025
        self.max_jerking = 80
        self.sim = sim_object
        self.name = name
        self.speed = Vector3([0, 0, 0])
        # self.object = self.sim.loadModel('hackaton_models/copter.ttm')
        self.position = None
        self.object = None
        self.target_object = None
        self.isAlive = 1
        self.controller = controller
        # print(f'Drone #{self.object} initialized!')

    def cb(self, pose, vel, accel, handle):
        self.sim.setObjectPose(handle, -1, pose)

    async def set_target_and_object(self):
        self.object = await self.sim.getObject(f'/{self.name}')
        self.target_object = await self.sim.getObject(f"/{self.name}/target")
        await self.sim.setObjectParent(self.target_object, -1, True)

    def get_drone_position(self):
        return self.sim.getObjectPose(self.object, -1)

    async def get_self_position(self):
        if self.isAlive:
            self.position = await self.sim.getObjectPose(self.target_object, -1)
            self.position = Vector3(self.position)
            return Vector3(self.position)

    #async def get_position(self, object):
    #       return await self.sim.getObjectPose(object, -1)

    async def move_target(self, next_pose_vector):
        target_pose = next_pose_vector.vector
        start_pose_target = await self.sim.getObjectPose(self.target_object, -1)
        steps = 200
        dx, dy, dz = (target_pose[0] - start_pose_target[0]) / steps, (target_pose[1] - start_pose_target[1]) / \
                     steps, \
                     (target_pose[2] - start_pose_target[2]) / steps
        for i in range(1, steps+1):
            position = [start_pose_target[0] + dx * i, start_pose_target[1] + dy * i, start_pose_target[2] + dz * i] \
                       + start_pose_target[3:]
            await self.sim.setObjectPose(self.target_object, -1, position)
            await asyncio.sleep(0)
        # self.sim.setObjectPose(self.target_object, -1, target_pose)
