import request from '@/utils/request'

export function getIdcList(params) {
  return request({
    url: '/idc/',
    method: 'get',
    params: params
  })
}

export function getIdcObj(id) {
  return request({
    url: `/idc/${id}`,
    method: 'get'
  })
}

export function addIdc(data) {
  return request({
    url: '/idc/',
    method: 'post',
    data
  })
}

export function editIdc(id, data) {
  return request({
    url: `/idc/${id}/`,
    method: 'put',
    data
  })
}

export function deleteIdc(id) {
  return request({
    url: `/idc/${id}/`,
    method: 'delete'
  })
}
