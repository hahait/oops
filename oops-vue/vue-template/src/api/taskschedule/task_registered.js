import request from '@/utils/request'

export function getTaskRegisteredList(params) {
  return request({
    url: '/task/registered/list/',
    method: 'get',
    params: params
  })
}
