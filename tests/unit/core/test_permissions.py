from __future__ import annotations

import unittest

from localweave.core.permissions import Action, PermissionEngine, PermissionTier


class PermissionEngineTests(unittest.TestCase):
    def test_read_is_allowed(self) -> None:
        decision = PermissionEngine().evaluate(Action.READ_VAULT)
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.tier, PermissionTier.READ_ONLY)

    def test_write_requires_explicit_approval(self) -> None:
        engine = PermissionEngine()
        self.assertFalse(engine.evaluate(Action.WRITE_VAULT).allowed)
        self.assertTrue(engine.evaluate(Action.WRITE_VAULT, approved=True).allowed)

    def test_unrestricted_shell_is_prohibited(self) -> None:
        decision = PermissionEngine().evaluate(Action.RUN_UNRESTRICTED_SHELL)
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.tier, PermissionTier.PROHIBITED)


if __name__ == "__main__":
    unittest.main()
