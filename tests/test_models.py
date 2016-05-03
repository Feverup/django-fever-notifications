#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-fever-notifications
------------

Tests for `django-fever-notifications` models module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from fevernotifications.models import Notification
from fevernotifications.shortcuts import create_notification


class TestFevernotifications(TestCase):

    def setUp(self):
        self.user_type = ContentType.objects.get_for_model(User)
        self.user = User.objects.create_user(
            username='john', email='john@domain.com', password='top_secret'
        )
        self.user2 = User.objects.create_user(
            username='Ada', email='ada@domain.com', password='top_secret'
        )

    def test_create_simple_notification(self):
        notification = Notification.objects.create(
            code="U2321", title="Test", message="Hello world",
            target=self.user
        )
        notification2 = Notification.objects.create(
            code="U2321", title="Test", message="Hello world",
            target=self.user2
        )
        self.assertEqual(notification.status, Notification.UNREAD)
        self.assertTrue(str(notification))

        self.assertIn(notification, Notification.objects.by_target(self.user))
        self.assertNotIn(notification2, Notification.objects.by_target(self.user))

    def test_soft_delete_notification(self):
        notification = Notification.objects.create(
            code="U2321", title="Test", message="Hello world",
            target=self.user
        )
        notification2 = Notification.objects.create(
            code="U2321", title="Test", message="Hello world",
            target=self.user2
        )
        notification.delete()
        self.assertNotIn(notification, Notification.objects.all())
        self.assertIn(notification, Notification.objects.all_with_deleted())
        self.assertIn(notification, Notification.objects.only_deleted())
        self.assertNotIn(notification2, Notification.objects.only_deleted())

    def test_create_with_shortcut(self):
        notification = create_notification(self.user, title="Test shortcut", message="Hello", code="1234")
        self.assertEqual(notification.status, Notification.UNREAD)
        self.assertEqual(notification.code, "1234")

    def tearDown(self):
        pass
