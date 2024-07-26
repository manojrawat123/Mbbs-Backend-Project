from rest_framework.routers import DefaultRouter
from .views import AccountViewSet,UserViewSet,UserProfileViewSet


#REQUEST URL
#GET /accounts/                 : Retrieves a list of all accounts.
#POST /accounts/                : Creates a new account.
#GET /accounts/{account_id}/    : Retrieves details of a specific account with the given account_id.
#PUT /accounts/{account_id}/    : Updates the account with the given account_id.
#DELETE /accounts/{account_id}/ : Deletes the account with the given account_id.


account_router = DefaultRouter()
account_router.register('accounts', AccountViewSet)
account_router.register('users',UserViewSet)
account_router.register('user-profiles',UserProfileViewSet)