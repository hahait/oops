'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  // dev 环境后端api的地址
  BASE_API: '"http://10.0.0.1:20018"',
})
