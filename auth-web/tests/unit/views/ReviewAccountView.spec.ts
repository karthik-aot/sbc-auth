import { createLocalVue, mount, shallowMount } from '@vue/test-utils'

import AccessRequestModal from '@/components/auth/staff/review-task/AccessRequestModal.vue'
import AccountAdministrator from '@/components/auth/staff/review-task/AccountAdministrator.vue'
import AccountInformation from '@/components/auth/staff/review-task/AccountInformation.vue'
import AccountStatusTab from '@/components/auth/staff/review-task/AccountStatus.vue'
import DownloadAffidavit from '@/components/auth/staff/review-task/DownloadAffidavit.vue'
import NotaryInformation from '@/components/auth/staff/review-task/NotaryInformation.vue'
import ReviewAccountView from '@/views/auth/staff/ReviewAccountView.vue'
import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuetify from 'vuetify'
import Vuex from 'vuex'

Vue.use(VueRouter)
Vue.use(Vuetify)
const vuetify = new Vuetify({})
const router = new VueRouter()

const mockSession = {
  'NRO_URL': 'Mock NRO URL',
  'NAME_REQUEST_URL': 'Mock Name Request URL'
}

// Prevent the warning "[Vuetify] Unable to locate target [data-app]"
document.body.setAttribute('data-app', 'true')

describe('ReviewAccountView.vue', () => {
  let wrapper: any
  let store: any
  const localVue = createLocalVue()
  localVue.use(Vuex)
  const staffModule = {
    namespaced: true,
    state: {
      accountUnderReview: {
        'accessType': 'REGULAR',
        'billable': true,
        'created': '2019-11-28T22:38:55.157811+00:00',
        'createdBy': 'test user',
        'id': 11,
        'loginOptions': [],
        'modified': '2020-10-13T16:52:24.905410+00:00',
        'modifiedBy': 'user test',
        'name': 'dsafa dsfasd',
        'orgType': 'BASIC',
        'orgStatus': 'ACTIVE',
        'products': [
          753,
          2521,
          3654
        ],
        'statusCode': 'ACTIVE'
      },
      accountUnderReviewAdmin: {
        'contacts': [
          {
            'created': '2019-11-28T22:37:28.307797+00:00',
            'createdBy': 'test ',
            'email': 'foo@bar.bar',
            'modified': '2020-03-12T19:30:29.914574+00:00',
            'modifiedBy': 'u1se',
            'phone': '(250) 555-1234',
            'phoneExtension': ''
          }
        ],
        'firstname': 'BCREGTEST Ciara',
        'id': 5,
        'lastname': 'FIFTEEN',
        'loginSource': 'BCSC',
        'modified': '2021-04-16T20:09:47.970773+00:00',
        'username': 'bcsc/e3iooqpkgjz3emmwajpdyvjwrxwiowkg'
      },
      accountUnderReviewAddress: {
        'city': 'Langley',
        'country': 'CA',
        'created': '2020-10-13T16:52:24.867015+00:00',
        'createdBy': 'user',
        'modified': '2020-10-13T16:52:24.867034+00:00',
        'postalCode': 'V3A 7E9',
        'region': 'BC',
        'street': '446-19705 Fraser Hwy',
        'streetAdditional': ''
      },
      accountUnderReviewAdminContact: {
        'city': 'Langley',
        'country': 'CA',
        'created': '2020-10-13T16:52:24.867015+00:00',
        'createdBy': 'user',
        'modified': '2020-10-13T16:52:24.867034+00:00',
        'postalCode': 'V3A 7E9',
        'region': 'BC',
        'street': '446-19705 Fraser Hwy',
        'streetAdditional': ''
      },
      accountUnderReviewAffidavitInfo: {
      }
    },
    actions: {
      syncTaskUnderReview: jest.fn(),
      approveAccountUnderReview: jest.fn(),
      rejectAccountUnderReview: jest.fn()
    },
    getter: {
      accountNotaryName: '',
      accountNotaryContact: ''
    }
  }

  const orgModule = {
    namespaced: true,
    actions: {
      fetchCurrentOrganizationGLInfo: jest.fn(),
      fetchOrgProductFeeCodes: jest.fn(),
      getOrgProducts: jest.fn(),
      createAccountFees: jest.fn(),
      syncCurrentAccountFees: jest.fn()
    },
    mutations: {
      resetCurrentAccountFees: jest.fn()
    },
    state: {
      currentOrgGLInfo: {}
    }
  }
  const taskModule = {
    namespaced: true,
    actions: {
      getTaskById: jest.fn().mockReturnValue({
        accountId: 2628,
        created: '2021-04-19T16:21:28.989168+00:00',
        createdBy: 'BCREGTEST Jing SIXTEEN',
        dateSubmitted: '2021-04-19T16:21:28.987006+00:00',
        id: 44,
        modified: '2021-04-19T16:21:28.989178+00:00',
        name: 'sb 16.3',
        relationshipId: 3674,
        relationshipStatus: 'PENDING_STAFF_REVIEW',
        relationshipType: 'PRODUCT',
        status: 'OPEN',
        type: 'Wills Registry',
        user: 31
      })
    }
  }

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  beforeEach(() => {
    sessionStorage.__STORE__['AUTH_API_CONFIG'] = JSON.stringify(mockSession)
    store = new Vuex.Store({
      state: {},
      strict: false,
      modules: {
        staff: staffModule,
        org: orgModule,
        task: taskModule
      }
    })
  })

  it('is a Vue instance', async () => {
    wrapper = shallowMount(ReviewAccountView, {
      store,
      vuetify,
      localVue,
      router,
      propsData: {
        orgId: 1
      },
      mocks: {
        $t: (mock) => mock
      },
      components: {
        DownloadAffidavit,
        AccountInformation,
        AccountAdministrator,
        NotaryInformation,
        AccountStatusTab,
        AccessRequestModal
      },
      stubs: {
        'AccountStatusTab': {
          template: `<div></div>`
        },
        'AccessRequestModal': {
          template: `<div></div>`
        }
      }
    })
    expect(wrapper.isVueInstance()).toBeTruthy()
    await Vue.nextTick()
    await Vue.nextTick()
    expect(wrapper.vm.taskRelationshipType).toBe('PRODUCT')
  })
})
