import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirct in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
**/
export const constantRouterMap = [
  { path: '/login', component: () => import('@/views/login/index'), hidden: true },
  { path: '/404', component: () => import('@/views/404'), hidden: true },

  {
    path: '/',
    component: Layout,
    redirect: '/overview',
    // name: 'Dashboard',
    // hidden: false,
    meta: { title: 'Dashboard', icon: 'dashboard' },
    children: [
      {
        path: 'overview',
        name: '概览',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '概览', icon: 'overview' }
      },
      {
        path: 'portal',
        name: '内部portal',
        component: () => import('@/views/tree/index'),
        meta: { title: '内部 Portal', icon: 'portal' }
      },
      {
        path: 'health',
        name: '应用健康检查',
        component: () => import('@/views/tree/index'),
        meta: { title: '应用健康检查', icon: 'health' }
      }
    ]
  },

  {
    path: '/',
    component: Layout,
    name: '用户管理',
    meta: { title: '用户管理', icon: 'accounts' },
    children: [
      {
        path: 'user/info',
        name: '个人中心',
        component: () => import('@/views/accounts/myself/index'),
        meta: { title: '个人中心', icon: 'people-b' }
      },
      {
        path: 'user/list',
        name: '用户列表',
        component: () => import('@/views/accounts/user/index'),
        meta: { title: '用户列表', icon: 'peoples' }
      },
      {
        path: 'group/list',
        name: '用户组管理',
        component: () => import('@/views/accounts/group/index'),
        meta: { title: '用户组管理', icon: 'groups' }
      },
      {
        path: 'permission/list',
        name: '权限管理',
        component: () => import('@/views/accounts/permission/index'),
        meta: { title: 'API 权限管理', icon: 'permissions' }
      }
    ]
  },

  {
    path: '/',
    component: Layout,
    name: '资源管理',
    meta: { title: '资源管理', icon: 'resources' },
    children: [
      {
        path: 'server/list',
        name: 'CDMB管理',
        component: () => import('@/views/resources/cmdb/index'),
        meta: { title: 'CMDB管理', icon: 'servers' }
      },
      {
        path: 'idc/list',
        name: 'IDC 管理',
        component: () => import('@/views/resources/idc/index'),
        meta: { title: 'IDC 管理', icon: 'idc' }
      },
      {
        path: 'cabinet/:idc_id',
        name: 'cabinet',
        component: () => import('@/views/resources/cabinet/index'),
        hidden: true
      }
    ]
  },

  {
    path: '/',
    component: Layout,
    name: '应用管理',
    meta: { title: '应用管理', icon: 'appconfig' },
    children: [
      {
        path: 'appconfig',
        name: '应用配置管理',
        component: () => import('@/views/appmanager/appconfig/index'),
        meta: { title: '应用配置管理', icon: 'apps' }
      },
      {
        path: 'standard',
        name: '应用标准化文档',
        component: () => import('@/views/table/index'),
        meta: { title: '应用标准化文档', icon: 'docs' }
      }
    ]
  },

  {
    path: '/',
    component: Layout,
    name: 'monitor',
    meta: { title: '监控告警', icon: 'zabbix' },
    children: [
      {
        path: 'zabbix/appmonitor',
        name: 'appmonitor',
        component: () => import('@/views/monitor/appmonitor/index'),
        meta: { title: '应用监控大盘', icon: 'appmonitor' }
      },
      {
        path: 'zabbix/mointorconfig',
        name: 'appmonitorconfig',
        component: () => import('@/views/monitor/config/index'),
        meta: { title: '应用监控配置', icon: 'zabbixconfig' }
      },
      {
        path: '/mointor/alert',
        name: 'alertmanage',
        component: () => import('@/views/monitor/alert/index'),
        meta: { title: '告警事件管理', icon: 'monitor-alert' }
      }
    ]
  },

  {
    path: '/',
    component: Layout,
    name: 'taskschedule',
    meta: { title: '任务调度', icon: 'taskschedule' },
    children: [
      {
        path: 'task/periodic/config',
        name: 'taskperiodic',
        component: () => import('@/views/taskschedule/taskperiodic/index'),
        meta: { title: '任务周期配置', icon: 'taskperiodic' }
      },
      {
        path: 'task/crontab/manage',
        name: 'taskcrontab',
        component: () => import('@/views/taskschedule/crontabtask/index'),
        meta: { title: '定时任务管理', icon: 'crontabtask' }
      },
      {
        path: 'task/result',
        name: 'taskresult',
        component: () => import('@/views/taskschedule/taskresult/index'),
        meta: { title: '任务执行结果', icon: 'taskresult' }
      }
    ]
  },

  {
    path: '/example',
    component: Layout,
    redirect: '/example/table',
    name: 'Example',
    meta: { title: 'Example', icon: 'example' },
    children: [
      {
        path: 'table',
        name: 'Table',
        component: () => import('@/views/table/index'),
        meta: { title: 'Table', icon: 'table' }
      },
      {
        path: 'tree',
        name: 'Tree',
        component: () => import('@/views/tree/index'),
        meta: { title: 'Tree', icon: 'tree' }
      }
    ]
  },

  {
    path: '/form',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Form',
        component: () => import('@/views/form/index'),
        meta: { title: 'Form', icon: 'form' }
      }
    ]
  },

  {
    path: '/nested',
    component: Layout,
    redirect: '/nested/menu1',
    name: 'Nested',
    meta: {
      title: 'nested',
      icon: 'nested'
    },
    children: [
      {
        path: 'menu1',
        component: () => import('@/views/nested/menu1/index'), // Parent router-view
        name: 'Menu1',
        meta: { title: 'menu1' },
        children: [
          {
            path: 'menu1-1',
            component: () => import('@/views/nested/menu1/menu1-1'),
            name: 'Menu1-1',
            meta: { title: 'menu1-1' }
          },
          {
            path: 'menu1-2',
            component: () => import('@/views/nested/menu1/menu1-2'),
            name: 'Menu1-2',
            meta: { title: 'menu1-2' },
            children: [
              {
                path: 'menu1-2-1',
                component: () => import('@/views/nested/menu1/menu1-2/menu1-2-1'),
                name: 'Menu1-2-1',
                meta: { title: 'menu1-2-1' }
              },
              {
                path: 'menu1-2-2',
                component: () => import('@/views/nested/menu1/menu1-2/menu1-2-2'),
                name: 'Menu1-2-2',
                meta: { title: 'menu1-2-2' }
              }
            ]
          },
          {
            path: 'menu1-3',
            component: () => import('@/views/nested/menu1/menu1-3'),
            name: 'Menu1-3',
            meta: { title: 'menu1-3' }
          }
        ]
      },
      {
        path: 'menu2',
        component: () => import('@/views/nested/menu2/index'),
        meta: { title: 'menu2' }
      }
    ]
  },

  { path: '*', redirect: '/404', hidden: true }
]

export default new Router({
  // mode: 'history', //后端支持可开
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap,
  mode: 'history'
})
