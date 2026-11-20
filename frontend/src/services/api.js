const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:5000/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    }
  })

  const payload = await response.json()

  if (!response.ok) {
    throw new Error(
      payload.error ||
      payload.message ||
      `Error del servidor (${response.status})`
    )
  }

  return payload
}

export const api = {
  health() {
    return request('/health')
  },

  getEstablishments() {
    return request('/establishments')
  },

  computeRoute(data) {
    return request('/routes/compute', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  },

  compareRoutes(data) {
    return request('/routes/compare', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }
}
