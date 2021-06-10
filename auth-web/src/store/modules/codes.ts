import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'

import { Code } from '@/models/Code'
import CodesService from '@/services/codes.service'

@Module({ namespaced: true })
export default class CodesModule extends VuexModule {
    suspensionReasonCodes: Code[] = []
    businessSizeCodes: Code[] = []
    businessTypeCodes: Code[] = []
    private suspensionReasonCodeTable: string = 'suspension_reason_codes'
    private businessSizeCodeTable: string = 'business_size_codes'
    private businessTypeCodeTable: string = 'business_type_codes'

    @Mutation
    public setSuspensionReasonCodes (codes: Code[]) {
      this.suspensionReasonCodes = codes
    }

    @Mutation
    public setBusinessSizeCodes (codes: Code[]) {
      this.businessSizeCodes = codes
    }

    @Mutation
    public setBusinessTypeCodes (codes: Code[]) {
      this.businessTypeCodes = codes
    }

    @Action({ commit: 'setBusinessSizeCodes', rawError: true })
    public async getBusinessSizeCodes (): Promise<Code[]> {
      const response = await CodesService.getCodes(this.businessSizeCodeTable)
      if (response && response.data && response.status === 200) {
        return response.data
      }
    }

    @Action({ commit: 'setBusinessTypeCodes', rawError: true })
    public async getBusinessTypeCodes (): Promise<Code[]> {
      const response = await CodesService.getCodes(this.businessTypeCodeTable)
      if (response && response.data && response.status === 200) {
        return response.data
      }
    }

    @Action({ commit: 'setSuspensionReasonCodes', rawError: true })
    public async getCodes (): Promise<Code[]> {
      const response = await CodesService.getCodes(this.suspensionReasonCodeTable)
      if (response && response.data && response.status === 200) {
        return response.data
      }
    }
}
