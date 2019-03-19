import request from '@/utils/request'

export function getTaskCrontabPeriodicList(params) {
  return request({
    url: '/task/crontab/periodic/',
    method: 'get',
    params: params
  })
}

export function addTaskCrontabPeriodic(data) {
  return request({
    url: '/task/crontab/periodic/',
    method: 'post',
    data
  })
}

export function editTaskCrontabPeriodic(id, data) {
  return request({
    url: `/task/crontab/periodic/${id}/`,
    method: 'patch',
    data
  })
}

export function deleteTaskCrontabPeriodic(id) {
  return request({
    url: `/task/crontab/periodic/${id}/`,
    method: 'delete'
  })
}

