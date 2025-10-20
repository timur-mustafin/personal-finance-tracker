
import axios from 'axios'

const api = axios.create({
  // use relative URL so it works behind nginx on 9080 (and in any env)
  baseURL: '/api/',
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access')
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api
