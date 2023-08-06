from rest_framework import routers

from .views import SwitchViewSet, DebugViewSet


router = routers.DefaultRouter()
router.register(r'switches', SwitchViewSet)
router.register(r'debug', DebugViewSet)

urlpatterns = router.urls
