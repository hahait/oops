import request from '@/utils/request'

export function getGroupList(params) {
  return request({
    url: '/group/',
    method: 'get',
    params: params
  })
}

export function addGroup(data) {
  return request({
    url: '/group/',
    method: 'post',
    data
  })
}

export function editGroup(id, data) {
  return request({
    url: `/group/${id}/`,
    method: 'patch',
    data
  })
}

export function deleteGroup(id) {
  return request({
    url: `/group/${id}/`,
    method: 'delete'
  })
}

export function getGroupRelateList(params) {
  return request({
    url: '/group/relate/',
    method: 'get',
    params: params
  })
}

export function editGroupRelate(id, data) {
  return request({
    url: `/group/relate/${id}/`,
    method: 'patch',
    data
  })
}
