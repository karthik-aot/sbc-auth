import { AxiosResponse } from 'axios'
import ConfigHelper from '@/util/config-helper'
import { Tasks } from '@/models/Task'
import { axios } from '@/util/http-util'

export default class TaskService {
  public static async getTasks (): Promise<AxiosResponse<Tasks>> {
    return axios.get(`${ConfigHelper.getAuthAPIUrl()}/tasks`)
  }
}
