
from fastapi import Depends, HTTPException, status

from security.auth import get_current_user


class RoleChecker:
    """
    Role-Based Access Control (RBAC)
    for Insurance Underwriting APIs.
    """

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        current_user: dict = Depends(get_current_user)
    ):

        user_role = current_user.get(
            "role",
            "guest"
        )

        if user_role not in self.allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"User role '{user_role}' "
                    f"is not authorized. "
                    f"Required roles: {self.allowed_roles}"
                )
            )

        return current_user


# ==================================================
# Insurance Role Presets
# ==================================================

require_advisor_or_underwriter = RoleChecker(
    ["advisor", "underwriter"]
)

require_underwriter_only = RoleChecker(
    ["underwriter"]
)