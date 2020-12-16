# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Enum definitions."""
from enum import Enum


class MessageType(Enum):
    """Event Types."""

    REFUND_REQUEST = 'bc.registry.payment.refundRequest'
    PAD_ACCOUNT_CREATE = 'bc.registry.payment.padAccountCreate'
    NSF_LOCK_ACCOUNT = 'bc.registry.payment.lockAccount'
    NSF_UNLOCK_ACCOUNT = 'bc.registry.payment.unlockAccount'


class SubjectType(Enum):
    """Event Types."""

    NSF_LOCK_ACCOUNT_SUBJECT = 'Your account has been suspended.'
    NSF_UNLOCK_ACCOUNT_SUBJECT = 'Your account has been reactivated.'


class TemplateType(Enum):
    """Template Types."""

    NSF_LOCK_ACCOUNT_TEMPLATE_NAME = 'account_suspended_email'
    NSF_UNLOCK_ACCOUNT_TEMPLATE_NAME = 'account_restored_email'