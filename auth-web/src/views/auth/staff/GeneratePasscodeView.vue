<template>
  <div>
    <ModalDialog
    max-width="680"
    :isPersistent="true"
    ref="generatePasscodeModal"
    :showCloseIcon="true"
    :showIcon="false"
    title="Generate Passcode"
    data-test="dialog-generate-passcode">
      <template v-slot:text>
        <p class="mb-7 mr-7">{{ $t('generatePasscodeText') }}</p>
        <v-form ref="generatePasscodeForm" id="generatePasscodeForm">
          <v-text-field
          filled
          label="Email Address"
          req
          persistent-hint
          :rules="emailRules"
          v-model="emailAddress"
          data-test="text-email-address"
          class="generate-passcode-input"
          >
          </v-text-field>
          <v-text-field
          filled
          label="Confirm Email Address"
          req
          persistent-hint
          :error-messages="emailMustMatch()"
          v-model="confirmedEmailAddress"
          data-test="text-confirm-email-address"
          class="generate-passcode-input"
          >
          </v-text-field>
        </v-form>
      </template>
      <template v-slot:actions>
        <v-spacer></v-spacer>
        <v-btn large @click="generate()" color="primary" data-test="btn-generate-passcode">Generate</v-btn>
        <v-btn large @click="close()" data-test="btn-close-generate-passcode-dialog">Close</v-btn>
      </template>
    </ModalDialog>
    <!-- Dialog for confirming passcode generation -->
    <ModalDialog
    ref="generatePasscodeSuccessDialog"
    title="Generate Passcode"
    :text="$t('generatePasscodeSuccessText')"
    dialog-class="notify-dialog"
    max-width="640"
    :isPersistent="true"
    >
      <template v-slot:icon>
        <v-icon large color="primary">mdi-check</v-icon>
      </template>
      <template v-slot:actions>
        <v-btn large color="primary" @click="generatePasscodeSuccessClose()" data-test="generate-passcode-success-button">OK</v-btn>
      </template>
    </ModalDialog>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import CommonUtils from '@/util/common-util'
import ModalDialog from '@/components/auth/common/ModalDialog.vue'
import { PasscodeResetLoad } from '@/models/business'
import { namespace } from 'vuex-class'

const BusinessModule = namespace('business')

@Component({
  components: {
    ModalDialog
  }
})
export default class GeneratePasscodeView extends Vue {
  private emailAddress = ''
  private confirmedEmailAddress = ''
  private emailRules = CommonUtils.emailRules()
  @Prop({ default: '' }) businessIdentitifier: string
  @BusinessModule.Action('resetBusinessPasscode') private resetBusinessPasscode!: (passcodeResetLoad: PasscodeResetLoad) => Promise<any>

  $refs: {
    generatePasscodeForm: HTMLFormElement,
    generatePasscodeModal: ModalDialog,
    generatePasscodeSuccessDialog: ModalDialog
  }

  public open () {
    this.$refs.generatePasscodeModal.open()
  }

  private emailMustMatch (): string {
    return (this.emailAddress === this.confirmedEmailAddress) ? '' : 'Email addresses must match'
  }

  private isFormValid (): boolean {
    return this.$refs.generatePasscodeForm?.validate() && !this.emailMustMatch()
  }

  public close () {
    this.$refs.generatePasscodeModal.close()
  }

  public generatePasscodeSuccessClose () {
    this.$refs.generatePasscodeSuccessDialog.close()
  }

  private async generate () {
    try {
      if (this.isFormValid() && this.businessIdentitifier) {
        await this.resetBusinessPasscode({ businessIdentifier: this.businessIdentitifier, passcodeResetEmail: this.emailAddress, resetPasscode: true })
        this.$refs.generatePasscodeModal.close()
        this.$refs.generatePasscodeSuccessDialog.open()
      }
    } catch (error) {
      // eslint-disable-next-line no-console
      console.log('Error during reset passcode event!')
    }
  }
}
</script>
<style lang="scss" scoped>
@import '@/assets/scss/theme.scss';
.generate-passcode-input{
    display: inline-block;
    width: 30rem;
}

.remove-btn {
    margin-left: 0.25rem;
    width: 7rem;
    height: 60px;
    vertical-align: top;
    font-weight: bold;
}
</style>
