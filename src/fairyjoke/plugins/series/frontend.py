from fairyjoke import Plugin

router = Plugin.Router()


@router.html("/")
def index():
    return router.template()
