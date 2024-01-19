if __name__ == "__main__":
    import mitsuba as mi

    # We must set this before importing any other Mitsuba modules
    # mi.set_variant("scalar_spectral")
    mi.set_variant("llvm_ad_rgb")
    # mi.set_variant("scalar_rgb")
    mi.set_log_level(mi.LogLevel.Debug)

    from mitsuba_wrapper.my_scene import my_scene

    # mi_scene1 = mi.load_dict(scene1)
    # mi.xml.dict_to_xml(scene1, "scene1.xml")
    # image1 = mi.render(mi_scene1)
    # mi.Bitmap(image1).write("scene1.exr")

    # mi_scene2 = mi.load_dict(cbox.model_dump(mode="python", exclude_none=True))
    # mi.xml.dict_to_xml(cbox.model_dump(mode="python", exclude_none=True), "scene2.xml")
    # image2 = mi.render(mi_scene2)
    # mi.Bitmap(image2).write("scene2.exr")


    mi_scene = mi.load_dict(my_scene.model_dump(mode="python", exclude_none=True))
    assert isinstance(mi_scene, mi.Scene)

    image = mi.render(mi_scene, spp=31**2)
    mi.Bitmap(image).write("my_first_render.exr")
