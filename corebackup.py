import math

class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scale):
        return Vec3(scale * self.x, scale * self.y, scale * self.z)
    
    def __rmul__(self, scale):
        return Vec3(scale * self.x, scale * self.y, scale * self.z)


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def normalize(v):
    length = math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
    return Vec3(v.x / length, v.y / length, v.z / length)


def cross(v1, v2):
    return Vec3(v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x)


def multiply(v1, v2):
    return Vec3(v1.x * v2.x, v1.y * v2.y, v1.z * v2.z)


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class Camera:
    def __init__(self, eye, lookat, distance):
        self.eye = eye
        self.lookat = lookat
        self.up = Vec3(0.0, 1.0, 0.0)
        self.distance = float(distance)  # distance of image plane form eye
        self._compute_uvw()

    def _compute_uvw(self):
        self.w = normalize(self.eye - self.lookat)  # w is in oposite direction of view
        self.u = normalize(cross(self.up, self.w))
        self.v = cross(self.w, self.u)
    
        # singularity
        if self.eye.x == self.lookat.x and self.eye.z == self.lookat.z\
                and self.eye.y > self.lookat.y:  # looking vertically down
            self.u = Vec3(0.0, 0.0, 1.0)
            self.v = Vec3(1.0, 0.0, 0.0)
            self.w = Vec3(0.0, 1.0, 0.0)

        if self.eye.x == self.lookat.x and self.eye.z == self.lookat.z\
                and self.eye.y < self.lookat.y:  # looking vertically up
            self.u = Vec3(1.0, 0.0, 0.0)
            self.v = Vec3(0.0, 0.0, 1.0)
            self.w = Vec3(0.0, -1.0, 0.0)

    def create_ray(self, x, y):
        direction = self.u * x + self.v * y - self.w * self.distance
        ray = Ray(origin=self.eye, direction=normalize(direction))
        return ray


class IsectPoint:
    def __init__(self, t, hit, normal, color):
        self.t = t
        self.hit = hit
        self.normal = normal
        self.color = color


class Sphere:
    def __init__(self, position, radius, color):
        self.position = position
        self.radius = radius
        self.color = color
    
    def intersect(self, ray):
        temp = ray.origin - self.position
        b = dot(temp, ray.direction) * 2.0
        c = dot(temp, temp) - self.radius * self.radius
        disc = b * b - 4.0 * c
        if disc < 0:
            return None

        e = math.sqrt(disc)
        t = (-b - e) * 0.5
        if t > 0.00005:
            hit = ray.origin + t * ray.direction
            normal = normalize(hit - self.position)
            return IsectPoint(t=t, hit=hit, normal=normal, color=self.color)

        t = (-b + e) * 0.5
        if t > 0.00005:
            hit = ray.origin + t * ray.direction
            normal = normalize(hit - self.position)
            return IsectPoint(t=t, hit=hit, normal=normal, color=self.color)


class PointLight:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity


class Scene:
    def __init__(self, width, height, samples_per_pixel, camera, shapes, lights):
        self.width = width
        self.height = height
        self.samples_per_pixel = samples_per_pixel
        self.camera = camera
        self.shapes = shapes
        self.lights = lights


def intersect_shapes(ray, shapes):
    min_t = None
    closest_isect = None
    for shape in shapes:
        isect = shape.intersect(ray)
        if isect is not None:
            if min_t is None or isect.t < min_t:
                min_t = isect.t
                closest_isect = isect
    return closest_isect


def visible(shapes, p1, p2):
    d = p2 - p1
    length = math.sqrt(d.x * d.x + d.y * d.y + d.z * d.z)
    ray = Ray(origin=p1, direction=normalize(d))
    isect = intersect_shapes(ray, shapes)
    if isect is not None:
        return isect.t >= length
    return True


def create_ray(scene, x, y, s, samples_per_pixels):
    spp_2 = math.sqrt(samples_per_pixels)
    subx = float(s % int(spp_2))
    suby = float(s // int(spp_2))
    posx = (subx + 0.5) / spp_2
    posy = (suby + 0.5) / spp_2
    screen_x = (float(x) + posx - float(scene.width) * 0.5)
    screen_y = (float(y) + posy - float(scene.height) * 0.5)
    return scene.camera.create_ray(screen_x, screen_y)


def render(scene):
    pixels = [Vec3(0.0, 0.0, 0.0)] * (scene.width * scene.height)
    # main rendering loop, this should be paralelized
    for y in range(scene.height):
        for x in range(scene.width):
            acum = Vec3(0.0, 0.0, 0.0)
            for s in range(scene.samples_per_pixel):
                ray = create_ray(scene, x, y, s, scene.samples_per_pixel)
                isect = intersect_shapes(ray, scene.shapes)
                if isect is not None:
                    for light in scene.lights:
                        if visible(scene.shapes, isect.hit, light.position):
                            lambertian = (1.0 / math.pi) * isect.color
                            wi = normalize(light.position - isect.hit)
                            theta = math.fabs(dot(isect.normal, wi))
                            color = multiply(lambertian, light.intensity) * theta
                            acum = acum + color
            acum = float(1.0 / scene.samples_per_pixel) * acum
            index = y * scene.width + x
            pixels[index] = acum
    return pixels


def create_scene_1():
    camera = Camera(eye=Vec3(0.0, 0.0, 0.0), lookat=Vec3(2.0, 0.0, 0.0), distance=800.0)
    shapes = [
        Sphere(position=Vec3(2.0, -0.12, 0.0), radius=0.2, color=Vec3(1.0, 0.4, 0.4)),
        Sphere(position=Vec3(1.5, 0.1, 0.1), radius=0.1, color=Vec3(1.0, 1.0, 0.4)),
        Sphere(position=Vec3(1.7, 0.1, -0.15), radius=0.1, color=Vec3(0.4, 0.4, 1.0)),
    ]
    lights = [
        PointLight(position=Vec3(0.0, 0.0, 0.0), intensity=Vec3(1.0, 1.0, 1.0)),
        PointLight(position=Vec3(1.0, 2.0, 0.0), intensity=Vec3(3.0, 3.0, 3.0)),
    ]
    width = 320
    height = 240
    samples_per_pixel = 1

    scene = Scene(width=width, height=height, samples_per_pixel=samples_per_pixel,
                  camera=camera, shapes=shapes, lights=lights)
    return scene


def write_raw_png(buf, width, height):
    import zlib
    import struct
    width_byte_4 = width * 4
    raw_data = b"".join(b'\x00' + buf[span:span + width_byte_4] for span in range((height - 1) * width * 4, -1, - width_byte_4))

    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return struct.pack("!I", len(data)) + chunk_head + struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head))
    return b"".join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(raw_data, 9)),
        png_pack(b'IEND', b'')])


def write_png(pixels, width, height, filename):
    # RGBA format
    buf = bytearray()
    for y in range(height):
        for x in range(width):
            p = pixels[y * width + x]
            r = min(255, int(p.x * 256.0))
            g = min(255, int(p.y * 256.0))
            b = min(255, int(p.z * 256.0))
            buf.append(r)
            buf.append(g)
            buf.append(b)
            buf.append(255)
    
    data = write_raw_png(buf, width=width, height=height)
    with open(filename, 'wb') as fp:
        fp.write(data)



if __name__ == "__main__":
    scene = create_scene_1()
    pixels = render(scene=scene)
    write_png(pixels, scene.width, scene.height, "test.png")
