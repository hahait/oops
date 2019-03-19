import request from '@/utils/request'

export function getUserList(params) {
  return request({
    url: '/user/',
    method: 'get',
    params: params
  })
}

export function addUser(data) {
  return request({
    url: '/user/',
    method: 'post',
    data
  })
}

export function editUser(id, data) {
  return request({
    url: `/user/${id}/`,
    method: 'patch',
    data
  })
}

export function deleteUser(id) {
  return request({
    url: `/user/${id}/`,
    method: 'delete'
  })
}

export function getUserInfo() {
  return request({
    url: '/user/info/',
    method: 'get'
  })
}
