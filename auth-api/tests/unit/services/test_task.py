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
"""Tests for the Task service.

Test suite to ensure that the Task service routines are working as expected.
"""
import json
from datetime import datetime
from auth_api import status as http_status
from auth_api.services import Task as TaskService
from auth_api.services import Org as OrgService
from auth_api.services import Affidavit as AffidavitService
from auth_api.utils.enums import TaskStatus, TaskType, TaskRelationshipType, OrgStatus, AffidavitStatus
from tests.utilities.factory_scenarios import TestUserInfo, TestJwtClaims, TestAffidavit, TestOrgInfo
from tests.utilities.factory_utils import factory_task_service, factory_org_model, factory_user_model, \
    factory_user_model_with_contact, factory_auth_header


def test_fetch_tasks(session, auth_mock):  # pylint:disable=unused-argument
    """Assert that tasks can be fetched."""
    user = factory_user_model()
    task = factory_task_service(user.id)
    dictionary = task.as_dict()
    name = dictionary['name']

    fetched_task = TaskService.fetch_tasks(task_type=TaskType.PENDING_STAFF_REVIEW.value,
                                           task_status=TaskStatus.OPEN.value)

    assert fetched_task
    for item in fetched_task:
        assert item.name == name


def test_create_task(session, keycloak_mock):  # pylint:disable=unused-argument
    """Assert that a task can be created."""
    user = factory_user_model()
    test_org = factory_org_model()
    test_task_info = {
        'name': test_org.name,
        'relationshipId': test_org.id,
        'relatedTo': user.id,
        'dateSubmitted': datetime.today(),
        'relationshipType': TaskRelationshipType.ORG.value,
        'type': TaskType.PENDING_STAFF_REVIEW.value,
        'status': TaskStatus.OPEN.value
    }
    task = TaskService.create_task(test_task_info)
    assert task
    dictionary = task.as_dict()
    assert dictionary['name'] == test_org.name


def test_put_task(client, jwt, session, keycloak_mock):  # pylint:disable=unused-argument
    """Assert that the task can be updated."""
    # 1. Create User
    # 2. Get document signed link
    # 3. Create affidavit
    # 4. Create Org
    # 5. Update the created task and the relationship

    user_with_token = TestUserInfo.user_staff_admin
    user_with_token['keycloak_guid'] = TestJwtClaims.public_user_role['sub']
    user = factory_user_model_with_contact(user_with_token)

    affidavit_info = TestAffidavit.get_test_affidavit_with_contact()
    AffidavitService.create_affidavit(token_info=TestJwtClaims.public_bceid_user, affidavit_info=affidavit_info)

    org = OrgService.create_org(TestOrgInfo.org_with_mailing_address(), user_id=user.id,
                                token_info=TestJwtClaims.public_bceid_user)
    org_dict = org.as_dict()
    assert org_dict['org_status'] == OrgStatus.PENDING_STAFF_REVIEW.value
    org_id = org_dict['id']

    update_task_payload = {
        'id': 1,
        'name': 'bar',
        'dateSubmitted': '2020-11-23T15:14:20.712096+00:00',
        'relationshipType': TaskRelationshipType.ORG.value,
        'relationshipId': org_id,
        'type': TaskType.PENDING_STAFF_REVIEW.value,
        'status': TaskStatus.COMPLETED.value,
        'relationshipStatus': AffidavitStatus.APPROVED.value
    }

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.staff_role)
    rv = client.put('/api/v1/tasks/{}'.format(1),
                    data=json.dumps(update_task_payload),
                    headers=headers, content_type='application/json')

    dictionary = json.loads(rv.data)
    assert rv.status_code == http_status.HTTP_200_OK
    assert dictionary['status'] == TaskStatus.COMPLETED.value

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.public_user_role)
    rv = client.get('/api/v1/orgs/{}'.format(org_id),
                    headers=headers, content_type='application/json')
    assert rv.status_code == http_status.HTTP_200_OK
    dictionary = json.loads(rv.data)
    assert dictionary['id'] == org_id
    assert rv.json.get('orgStatus') == OrgStatus.ACTIVE.value