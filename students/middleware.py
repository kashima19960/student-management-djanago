"""Audit log middleware — records create/update/delete actions."""

import json

from django.utils.deprecation import MiddlewareMixin


class AuditLogMiddleware(MiddlewareMixin):
    """Automatically log CRUD operations for audited models."""

    AUDITED_MODELS = {
        "student", "department", "classinfo", "teacher",
        "course", "enrollment", "attendance",
    }

    def process_response(self, request, response):
        # Audit logging will be fully implemented in Phase 2
        # when the AuditLog model is created.
        return response
