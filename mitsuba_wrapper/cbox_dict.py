import mitsuba as mi

spp: int = 128
res: int = 256
max_depth: int = 6
integrator: str = "path"

d = {
    "type": "scene",
    "integrator": {
        "type": integrator,
        "max_depth": max_depth,
    },
    "sensor": {
        "type": "perspective",
        "fov_axis": "smaller",
        "near_clip": 0.001,
        "far_clip": 100.0,
        "focus_distance": 1000,
        "fov": 39.3077,
        "to_world": mi.ScalarTransform4f.look_at(  # type: ignore
            origin=[0, 0, 4],
            target=[0, 0, 0],
            up=[0, 1, 0],
        ),
        "sampler": {
            "type": "independent",
            "sample_count": spp,
        },
        "film": {
            "type": "hdrfilm",
            "width": res,
            "height": res,
            "pixel_format": "rgb",
            "component_format": "float32",
            "rfilter": {
                "type": "tent",
            },
        },
    },
    "gray": {
        "type": "diffuse",
        "reflectance": {
            "type": "rgb",
            "value": [0.85, 0.85, 0.85],
        },
    },
    "white": {
        "type": "diffuse",
        "reflectance": {
            "type": "rgb",
            "value": [0.885809, 0.698859, 0.666422],
        },
    },
    "green": {
        "type": "diffuse",
        "reflectance": {
            "type": "rgb",
            "value": [0.105421, 0.37798, 0.076425],
        },
    },
    "red": {
        "type": "diffuse",
        "reflectance": {
            "type": "rgb",
            "value": [0.570068, 0.0430135, 0.0443706],
        },
    },
    "glass": {
        "type": "dielectric",
    },
    "mirror": {
        "type": "conductor",
    },
    "light": {
        "type": "obj",
        "filename": "./scenes/meshes/cbox_luminaire.obj",
        "to_world": mi.ScalarTransform4f.translate([0, -0.01, 0]),  # type: ignore
        "emitter": {
            "type": "area",
            "radiance": {
                "type": "rgb",
                "value": [18.387, 13.9873, 6.75357],
            },
        },
        "bsdf": {
            "type": "ref",
            "id": "white",
        },
    },
    "floor": {
        "type": "obj",
        "filename": "./scenes/meshes/cbox_floor.obj",
        "bsdf": {
            "type": "ref",
            "id": "white",
        },
    },
    "ceiling": {
        "type": "obj",
        "filename": "./scenes/meshes/cbox_ceiling.obj",
        "bsdf": {
            "type": "ref",
            "id": "white",
        },
    },
    "back": {
        "type": "obj",
        "filename": "./scenes/meshes/cbox_back.obj",
        "bsdf": {
            "type": "ref",
            "id": "white",
        },
    },
    "greenwall": {
        "type": "obj",
        "filename": "./scenes/meshes/cbox_greenwall.obj",
        "bsdf": {
            "type": "ref",
            "id": "green",
        },
    },
    "redwall": {
        "type": "obj",
        "filename": "./scenes/meshes/cbox_redwall.obj",
        "bsdf": {
            "type": "ref",
            "id": "red",
        },
    },
    "mirrorsphere": {
        "type": "sphere",
        "to_world": mi.ScalarTransform4f.scale([0.5, 0.5, 0.5]).translate([-0.3, -0.5, 0.2]),  # type: ignore
        "bsdf": {
            "type": "ref",
            "id": "mirror",
        },
    },
    "glasssphere": {
        "type": "sphere",
        "to_world": mi.ScalarTransform4f.scale([0.25, 0.25, 0.25]).translate([0.5, -0.75, -0.2]),  # type: ignore
        "bsdf": {
            "type": "ref",
            "id": "glass",
        },
    },
}
