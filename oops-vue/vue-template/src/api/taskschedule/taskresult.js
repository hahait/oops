import request from '@/utils/request'

export function getTaskResultList(params) {
  return request({
    url: '/task/result/',
    method: 'get',
    params: params
  })
}
