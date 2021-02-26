# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This manages a Suspended Account Reason Type record.

It defines the available reasons to suspend an account.
"""

from sqlalchemy import Column, Integer, String

from .base_model import BaseCodeModel

class SuspendAccountReasonCode(BaseCodeModel):  # pylint: disable=too-few-public-methods
    """SuspendAccountReason code table to store all the reason codes supported by auth system."""

    __tablename__ = 'suspend_account_reason_codes'

    @classmethod
    def find_by_id(cls, id):
        """Find a SuspendAccountReason instance that matches the id."""
        return cls.query.filter_by(id=id).one_or_none()