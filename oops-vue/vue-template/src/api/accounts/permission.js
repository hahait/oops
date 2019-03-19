import request from '@/utils/request'

export function getPermissionList(params) {
  return request({
    url: '/content/type/',
    method: 'get',
    params: params
  })
}

export function getPermission(params) {
  return request({
    url: '/permission/',
    method: 'get',
    params: params
  })
}

export function editPermission(id, data) {
  return request({
    url: `/permission/${id}/`,
    method: 'patch',
    data
  })
}

