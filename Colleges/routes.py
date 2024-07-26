from rest_framework import routers
from .views import CollegeInfoViewSet

#REQUEST URL

#GET  /colleges/      - Retrieves a list of colleges instances
#POST /colleges/      - Creates a new colleges instance
#GET  /colleges/{id}/ - Retrieves a specific colleges instance
#PUT  /colleges/{id}/ - Updates a specific colleges instance

college_router = routers.DefaultRouter()
college_router.register(r'colleges', CollegeInfoViewSet)


