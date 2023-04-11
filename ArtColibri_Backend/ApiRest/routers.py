from rest_framework.routers import Route, DynamicRoute, SimpleRouter, DefaultRouter


class ApiRouter(DefaultRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/<slug:slug>$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        # DynamicRoute(
        #     url=r'^{prefix}/{lookup}/{url_path}$',
        #     name='{basename}-{url_name}',
        #     detail=True,
        #     initkwargs={}
        # )
    ]