from security.roles import ROLE_PERMISSIONS


def has_access(role: str, document_type: str):

    permissions = ROLE_PERMISSIONS.get(
        role,
        []
    )

    if "all" in permissions:
        return True

    return document_type in permissions