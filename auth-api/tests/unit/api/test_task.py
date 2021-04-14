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
"""Tests to verify the Tasks API end-point.

Test-Suite to ensure that the /tasks endpoint is working as expected.
"""
import json

from auth_api import status as http_status
from auth_api.services import Org as OrgService
from auth_api.services import Task as TaskService
from auth_api.services import Affidavit as AffidavitService
from tests.utilities.factory_utils import (factory_auth_header,
                                           factory_task_service, factory_user_model, factory_user_model_with_contact)
from tests.utilities.factory_scenarios import TestJwtClaims, TestUserInfo, TestAffidavit, TestOrgInfo, \
    TestOrgProductsInfo
from auth_api.schemas import utils as schema_utils
from auth_api.utils.enums import TaskRelationshipType, TaskType, TaskStatus, AffidavitStatus, OrgStatus, \
    ProductSubscriptionStatus


def test_fetch_tasks(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that the tasks can be fetched."""
    user = factory_user_model()
    factory_task_service(user.id)

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.staff_role)
    rv = client.get('/api/v1/tasks', headers=headers, content_type='application/json')
    item_list = rv.json
    assert schema_utils.validate(item_list, 'paged_response')[0]
    assert rv.status_code == http_status.HTTP_200_OK


def test_fetch_tasks_no_content(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that the none can be fetched."""

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.staff_role)
    rv = client.get('/api/v1/tasks', headers=headers, content_type='application/json')
    assert rv.status_code == http_status.HTTP_200_OK


def test_fetch_tasks_with_status(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that the tasks can be fetched."""
    user = factory_user_model()
    factory_task_service(user.id)

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.staff_role)
    rv = client.get('/api/v1/tasks?type=PENDING_STAFF_REVIEW&status=OPEN',
                    headers=headers, content_type='application/json')
    item_list = rv.json
    assert schema_utils.validate(item_list, 'paged_response')[0]
    assert rv.status_code == http_status.HTTP_200_OK


def test_put_task_org(client, jwt, session, keycloak_mock):  # pylint:disable=unused-argument
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

    tasks = TaskService.fetch_tasks(task_type=TaskType.PENDING_STAFF_REVIEW.value,
                                    task_status=TaskStatus.OPEN.value, page=1, limit=10)
    fetched_tasks = tasks['tasks']
    fetched_task = fetched_tasks[0]

    update_task_payload = {
        'id': fetched_task['id'],
        'name': 'bar',
        'dateSubmitted': '2020-11-23T15:14:20.712096+00:00',
        'relationshipType': TaskRelationshipType.ORG.value,
        'relationshipId': org_id,
        'type': TaskType.PENDING_STAFF_REVIEW.value,
        'status': TaskStatus.COMPLETED.value,
        'relationshipStatus': AffidavitStatus.APPROVED.value
    }

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.staff_role)
    rv = client.put('/api/v1/tasks/{}'.format(fetched_task['id']),
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


def test_put_task_product(client, jwt, session, keycloak_mock):  # pylint:disable=unused-argument
    """Assert that the task can be updated."""
    # 1. Create User
    # 4. Create Product subscription
    # 5. Update the created task and the relationship

    """Assert that an org can be POSTed."""
    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.staff_admin_role)
    rv = client.post('/api/v1/users', headers=headers, content_type='application/json')
    rv = client.post('/api/v1/orgs', data=json.dumps(TestOrgInfo.org1),
                     headers=headers, content_type='application/json')
    assert rv.status_code == http_status.HTTP_201_CREATED
    dictionary = json.loads(rv.data)
    rv_products = client.post(f"/api/v1/orgs/{dictionary.get('id')}/products",
                              data=json.dumps(TestOrgProductsInfo.org_products1),
                              headers=headers, content_type='application/json')
    assert rv_products.status_code == http_status.HTTP_201_CREATED
    assert schema_utils.validate(rv_products.json, 'org_product_subscriptions_response')[0]

    tasks = TaskService.fetch_tasks(task_type=TaskType.PENDING_STAFF_REVIEW.value,
                                    task_status=TaskStatus.OPEN.value,
                                    page=1,
                                    limit=10)
    fetched_tasks = tasks['tasks']
    fetched_task = fetched_tasks[0]
    assert fetched_task['relationship_type'] == TaskRelationshipType.PRODUCT.value
    org_products = json.loads(rv_products.data)
    org_product = org_products.get('subscriptions')[0]

    update_task_payload = {
        'id': fetched_task['id'],
        'name': 'bar',
        'dateSubmitted': '2020-11-23T15:14:20.712096+00:00',
        'relationshipType': TaskRelationshipType.PRODUCT.value,
        'relationshipId': org_product.get('id'),
        'type': TaskType.PENDING_STAFF_REVIEW.value,
        'status': TaskStatus.COMPLETED.value,
        'relationshipStatus': ProductSubscriptionStatus.ACTIVE.value
    }

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.staff_role)
    rv = client.put('/api/v1/tasks/{}'.format(fetched_task['id']),
                    data=json.dumps(update_task_payload),
                    headers=headers, content_type='application/json')

    dictionary = json.loads(rv.data)
    assert rv.status_code == http_status.HTTP_200_OK
    assert dictionary['status'] == TaskStatus.COMPLETED.value


def test_fetch_task(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that the task can be fetched by id."""
    user = factory_user_model()
    task = factory_task_service(user.id)
    task_id = task._model.id

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.staff_role)
    rv = client.get('/api/v1/tasks/{}'.format(task_id), headers=headers, content_type='application/json')
    assert rv.status_code == http_status.HTTP_200_OK
    assert rv.json.get('name') == task._model.name
