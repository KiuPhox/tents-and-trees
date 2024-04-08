class SceneManager:
    scenes = {}
    current_scene = None

    @staticmethod
    def change_scene(name):
        SceneManager.current_scene = SceneManager.scenes[name]
        SceneManager.current_scene.enter()

    @staticmethod
    def update():
        SceneManager.current_scene.update()