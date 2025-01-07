# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.


from model.main_screen import MainScreenModel
from controller.main_screen import MainScreenController

screens = {
    "main screen": {
        "model": MainScreenModel,
        "controller": MainScreenController,
    },
}