# -*- coding: UTF-8 -*-
from django.conf import settings

DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING

"""
数据库路由
"""
class DatabaseRouter(object): #配置app02的路由，去连接hvdb数据库
    """
    A router to control all database operations on models for different
    databases.

    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.

    Settings example:

    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}
    """

    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = DATABASE_MAPPING.get(obj1._meta.app_label)
        db_obj2 = DATABASE_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db in DATABASE_MAPPING.values():
            return DATABASE_MAPPING.get(app_label) == db
        elif app_label in DATABASE_MAPPING:
            return False
        return None
 

# class app01Router(object):
#     """
#     A router to control all database operations on models in the
#     aew application.
#     """
#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read aew models go to aew DB.
#         """
#         if model._meta.app_label == 'app01':
#             return 'default'
#         return None
 
#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write aew models go to aew DB.
#         """
#         if model._meta.app_label == 'app01':
#             return 'default'
#         return None
 
#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the aew app is involved.
#         """
#         if obj1._meta.app_label == 'app01' or obj2._meta.app_label == 'app01':
#             return True
#         return None
 
#     def allow_migrate(self, db, model):
#         """
#         Make sure the aew app only appears in the aew database.
#         """
#         if db == 'default':
#             return model._meta.app_label == 'app01'
#         elif model._meta.app_label == 'app01':
#             return False
#         return None