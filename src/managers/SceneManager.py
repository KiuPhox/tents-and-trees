class SceneManager:
    scenes = {}
    current_scene = None

    @staticmethod
    def change_scene(name):
        if SceneManager.current_scene is not None:
            for game_object in SceneManager.current_scene.game_objects:
                game_object.destroy()

            SceneManager.current_scene.game_objects = []

        SceneManager.current_scene = SceneManager.scenes[name]
        SceneManager.current_scene.start()

    @staticmethod
    def update():
        SceneManager.current_scene.update()

    def register_scene(scene):
        SceneManager.scenes[scene.name] = scene
