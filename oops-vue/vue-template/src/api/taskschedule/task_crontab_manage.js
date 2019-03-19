import request from '@/utils/request'

export function getTaskCrontabList(params) {
  return request({
    url: '/task/crontab/manage/',
    method: 'get',
    params: params
  })
}

export function addTaskCrontab(data) {
  return request({
    url: '/task/crontab/manage/',
    method: 'post',
    data
  })
}

export function editTaskCrontab(id, data) {
  return request({
    url: `/task/crontab/manage/${id}/`,
    method: 'patch',
    data
  })
}

export function deleteTaskCrontab(id) {
  return request({
    url: `/task/crontab/manage/${id}/`,
    method: 'delete'
  })
}

export function execTaskNow(data) {
  return request({
    url: '/task/exec/immediate/',
    method: 'post',
    data
  })
}
